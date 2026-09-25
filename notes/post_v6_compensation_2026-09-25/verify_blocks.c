/* Independent finite replay of the Q_v parity balances, using GMP.
 *
 * Build on macOS with Homebrew GMP:
 *   DEVELOPER_DIR=/Library/Developer/CommandLineTools clang -O3 -std=c11 \
 *     -Wall -Wextra -Werror -I/opt/homebrew/include verify_blocks.c \
 *     -L/opt/homebrew/lib -lgmp -o /tmp/verify_blocks
 * On Linux with libgmp-dev, the explicit include/library paths are unnecessary.
 * Run one explicitly selected level: /tmp/verify_blocks --v 21
 * Optional --trace PATH writes packed parities: bit r is parity T^r(Q_v),
 * least-significant bit first; unused final bits are zero.
 *
 * Initial residues use Q_1=5 and Q_(u+1)=Q_u+2^(u+2)*Q_u^2 modulo 2^H.
 * This does not use the Python producer's modular power or its tables.
 * Each block is replayed directly on its low <=32 bits.  If j is its odd
 * count, T^take(n)=3^j*(n>>take)+T^take(n mod 2^take).  Only the still
 * available modular precision is retained.  The last block may be shorter.
 *
 * B(r)=306*r-589*J(r); C(r)=305*r-589*J(r).  Prefix extrema include r=0.
 * Equal extrema keep the earliest index.  Equal maximum drawdowns keep the
 * lexicographically earliest (start,end) pair.  This is a finite arithmetic
 * replay, not a proof of a uniform claim about the family.
 */

#include <errno.h>
#include <gmp.h>
#include <inttypes.h>
#include <limits.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#if ULONG_MAX < UINT64_MAX
#error "This verifier requires a platform with 64-bit unsigned long."
#endif

typedef struct {
    int64_t total;
    int64_t minimum;
    uint64_t minimum_at;
    int64_t maximum;
    uint64_t maximum_at;
    int64_t drawdown;
    uint64_t drawdown_from;
    uint64_t drawdown_to;
} Balance;

static void update_balance(Balance *s, int64_t change, uint64_t step) {
    s->total += change;
    if (s->total < s->minimum) {
        s->minimum = s->total;
        s->minimum_at = step;
    }
    if (s->total > s->maximum) {
        s->maximum = s->total;
        s->maximum_at = step;
    }
    const int64_t loss = s->maximum - s->total;
    if (loss > s->drawdown ||
        (loss == s->drawdown &&
         (s->maximum_at < s->drawdown_from ||
          (s->maximum_at == s->drawdown_from && step < s->drawdown_to)))) {
        s->drawdown = loss;
        s->drawdown_from = s->maximum_at;
        s->drawdown_to = step;
    }
}

static void print_balance(const Balance *s) {
    printf("{\"balance_end\":%" PRId64
           ",\"minimum_balance\":%" PRId64
           ",\"minimum_at_step\":%" PRIu64
           ",\"maximum_balance\":%" PRId64
           ",\"maximum_at_step\":%" PRIu64
           ",\"maximum_drawdown\":%" PRId64
           ",\"drawdown_from_step\":%" PRIu64
           ",\"drawdown_to_step\":%" PRIu64 "}",
           s->total, s->minimum, s->minimum_at, s->maximum, s->maximum_at,
           s->drawdown, s->drawdown_from, s->drawdown_to);
}

static int parse_unsigned(const char *text, unsigned long *out) {
    char *end = NULL;
    if (*text == '\0' || *text == '-') return 0;
    errno = 0;
    unsigned long value = strtoul(text, &end, 10);
    if (errno != 0 || *end != '\0') return 0;
    *out = value;
    return 1;
}

static void usage(const char *program) {
    fprintf(stderr, "Usage: %s --v LEVEL [--block-width WIDTH] [--trace PATH]\n"
                    "Require 5 <= LEVEL <= 24 and 1 <= WIDTH <= 32.\n", program);
}

int main(int argc, char **argv) {
    unsigned long v = 0, width = 32;
    int have_v = 0, have_width = 0;
    const char *trace_path = NULL;
    for (int i = 1; i < argc; ++i) {
        if (strcmp(argv[i], "--v") == 0 && !have_v && i + 1 < argc) {
            if (!parse_unsigned(argv[++i], &v)) {
                usage(argv[0]); return 2;
            }
            have_v = 1;
        } else if (strcmp(argv[i], "--block-width") == 0 && !have_width && i + 1 < argc) {
            if (!parse_unsigned(argv[++i], &width)) {
                usage(argv[0]); return 2;
            }
            have_width = 1;
        } else if (strcmp(argv[i], "--trace") == 0 && trace_path == NULL && i + 1 < argc) {
            trace_path = argv[++i];
            if (*trace_path == '\0') {
                usage(argv[0]); return 2;
            }
        } else {
            usage(argv[0]); return 2;
        }
    }
    if (!have_v || v < 5 || v > 24 || width < 1 || width > 32) {
        usage(argv[0]); return 2;
    }

    const uint64_t precision = (589 * (UINT64_C(1) << v) + 611) / 612;
    const size_t trace_bytes = (size_t)((precision + 7) / 8);
    unsigned char *trace = NULL;
    if (trace_path != NULL) {
        trace = calloc(trace_bytes, 1);
        if (trace == NULL) {
            fprintf(stderr, "Cannot allocate parity trace.\n"); return 1;
        }
    }
    mpz_t residue, temporary;
    mpz_init_set_ui(residue, 5);
    mpz_init(temporary);
    for (unsigned long u = 1; u < v; ++u) {
        mpz_mul(temporary, residue, residue);
        mpz_mul_2exp(temporary, temporary, u + 2);
        mpz_add(residue, residue, temporary);
        mpz_fdiv_r_2exp(residue, residue, (mp_bitcnt_t)precision);
    }

    Balance b = {0}, c = {0};
    uint64_t consumed = 0, odd_steps = 0;
    while (consumed < precision) {
        const uint64_t available = precision - consumed;
        const unsigned long take = available < width ? (unsigned long)available : width;
        const uint64_t low_mask = (UINT64_C(1) << take) - 1;
        uint64_t small = ((uint64_t)mpz_get_ui(residue)) & low_mask;
        unsigned long multiplier = 1;
        for (unsigned long i = 0; i < take; ++i) {
            const int odd = (int)(small & 1);
            if (trace != NULL) {
                trace[consumed >> 3] |= (unsigned char)(odd << (consumed & 7));
            }
            odd_steps += (uint64_t)odd;
            if (odd) {
                multiplier *= 3;
                small = (3 * small + 1) >> 1;
            } else {
                small >>= 1;
            }
            ++consumed;
            update_balance(&b, odd ? -283 : 306, consumed);
            update_balance(&c, odd ? -284 : 305, consumed);
        }
        mpz_fdiv_q_2exp(residue, residue, take);
        mpz_mul_ui(residue, residue, multiplier);
        mpz_add_ui(residue, residue, (unsigned long)small);
        mpz_fdiv_r_2exp(residue, residue, (mp_bitcnt_t)(precision - consumed));
    }

    if (trace_path != NULL) {
        FILE *output = fopen(trace_path, "wb");
        if (output == NULL) {
            perror("Cannot open parity trace");
            mpz_clear(temporary); mpz_clear(residue); free(trace); return 1;
        }
        int write_ok = fwrite(trace, 1, trace_bytes, output) == trace_bytes;
        if (fclose(output) != 0) write_ok = 0;
        if (!write_ok) {
            fprintf(stderr, "Cannot write complete parity trace.\n");
            mpz_clear(temporary); mpz_clear(residue); free(trace); return 1;
        }
    }

    printf("{\"v\":%lu,\"precision_bits\":%" PRIu64
           ",\"odd_steps\":%" PRIu64 ",\"block_width\":%lu,\"B\":",
           v, precision, odd_steps, width);
    print_balance(&b);
    printf(",\"C\":");
    print_balance(&c);
    printf("}\n");
    mpz_clear(temporary);
    mpz_clear(residue);
    free(trace);
    return 0;
}
