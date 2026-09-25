/* Exact Collatz shortcut iteration on ordinary ternary digit arrays.
 *
 * Input R_m = 3^m - 1 is m digits equal to 2.  No complete integer value,
 * GMP, floating point, or binary Collatz arithmetic is used.
 *
 * Build: clang -std=c11 -O3 -Wall -Wextra -Wpedantic ternary_engine.c -o engine
 * Usage: engine --m M --steps N [--trace FILE] [--digits FILE] [--ledger FILE]
 * Trace: packed bits, bit r is the parity of T^r(R_m), LSB first.
 * Digits: final ordinary ternary digits, MSB first, ASCII, no newline.
 * Ledger: JSON array of [odd, length_before, length_after, sum_before,
 *   sum_after, carry_ones, leading_removed, ones_before, ones_after].
 * Length/sum before refer to the state BEFORE appending 1 for an odd step.
 * Carry counts include the outgoing carry after EACH scanned input digit.
 */

#include <errno.h>
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static void usage(const char *program) {
    fprintf(stderr, "Usage: %s --m M --steps N [--trace FILE] "
            "[--digits FILE] [--ledger FILE]\n", program);
}

static int parse_u64(const char *text, uint64_t *value) {
    if (!text[0] || text[0] == '-' || text[0] == '+') return 0;
    for (const char *p = text; *p; ++p)
        if (*p < '0' || *p > '9') return 0;
    errno = 0;
    char *end = NULL;
    unsigned long long parsed = strtoull(text, &end, 10);
    if (errno || !end || *end || parsed > UINT64_MAX) return 0;
    *value = (uint64_t)parsed;
    return 1;
}

static FILE *open_output(const char *path, const char *mode) {
    FILE *file = fopen(path, mode);
    if (!file) fprintf(stderr, "Cannot open %s: %s\n", path, strerror(errno));
    return file;
}

int main(int argc, char **argv) {
    uint64_t m = 0, steps = 0;
    int have_m = 0, have_steps = 0;
    const char *trace_path = NULL, *digits_path = NULL, *ledger_path = NULL;
    for (int i = 1; i < argc; ++i) {
        if (!strcmp(argv[i], "--help")) { usage(argv[0]); return 0; }
        if (i + 1 >= argc) { usage(argv[0]); return 2; }
        const char *option = argv[i++], *value = argv[i];
        if (!strcmp(option, "--m")) {
            if (have_m || !parse_u64(value, &m) || !m) {
                fprintf(stderr, "M must be a positive integer, specified once.\n");
                return 2;
            }
            have_m = 1;
        } else if (!strcmp(option, "--steps")) {
            if (have_steps || !parse_u64(value, &steps)) {
                fprintf(stderr, "N must be a nonnegative integer, specified once.\n");
                return 2;
            }
            have_steps = 1;
        } else if (!strcmp(option, "--trace") && !trace_path) trace_path = value;
        else if (!strcmp(option, "--digits") && !digits_path) digits_path = value;
        else if (!strcmp(option, "--ledger") && !ledger_path) ledger_path = value;
        else { fprintf(stderr, "Unknown or repeated option: %s\n", option); return 2; }
    }
    if (!have_m || !have_steps) { usage(argv[0]); return 2; }

    /* At most one digit is appended per step.  The stronger cell bound
     * also protects all aggregate digit sums and their doubled identities. */
    if (steps > UINT64_MAX - m || m + steps > UINT64_MAX / 4 ||
        m + steps > SIZE_MAX - 1 ||
        (steps && steps > (UINT64_MAX / 4) / (m + steps))) {
        fprintf(stderr, "Requested size exceeds exact counter/allocation limits.\n");
        return 2;
    }
    size_t capacity = (size_t)(m + steps + 1);
    unsigned char *digits = malloc(capacity);
    if (!digits) { fprintf(stderr, "Cannot allocate digit buffer.\n"); return 1; }
    memset(digits, 2, (size_t)m);
    size_t begin = 0, end = (size_t)m;
    uint64_t sum = 2 * m, ones = 0;
    uint64_t odd_count = 0, carry_total = 0, scanned_total = 0, removed_total = 0;
    uint64_t sum_before_total = 0, sum_after_total = 0;
    uint64_t carry_min = UINT64_MAX, carry_max = 0;
    FILE *trace = NULL, *ledger = NULL, *digit_file = NULL;
    int status = 1;
    unsigned int trace_byte = 0;

    if (trace_path && !(trace = open_output(trace_path, "wb"))) goto cleanup;
    if (ledger_path && !(ledger = open_output(ledger_path, "w"))) goto cleanup;
    if (ledger && fputs("[\n", ledger) == EOF) goto io_error;

    for (uint64_t step = 0; step < steps; ++step) {
        unsigned int odd = (unsigned int)(sum & 1);
        uint64_t length_before = (uint64_t)(end - begin), sum_before = sum;
        uint64_t ones_before = ones;
        odd_count += odd;
        if (trace) {
            trace_byte |= odd << (unsigned int)(step & 7);
            if ((step & 7) == 7) {
                if (fputc((int)trace_byte, trace) == EOF) goto io_error;
                trace_byte = 0;
            }
        }
        if (odd) digits[end++] = 1; /* 3*x + 1 in ordinary base three. */
        scanned_total += (uint64_t)(end - begin);
        unsigned int carry = 0;
        uint64_t carry_ones = 0;
        sum = 0;
        ones = 0;
        for (size_t pos = begin; pos < end; ++pos) {
            unsigned int value = 3 * carry + digits[pos];
            unsigned int quotient_digit = value >> 1;
            carry = value & 1;
            digits[pos] = (unsigned char)quotient_digit;
            sum += quotient_digit;
            ones += quotient_digit == 1;
            carry_ones += carry;
        }
        size_t old_begin = begin;
        while (begin + 1 < end && digits[begin] == 0) ++begin;
        uint64_t removed = (uint64_t)(begin - old_begin);
        uint64_t length_after = (uint64_t)(end - begin);
        if (carry != 0 || 2 * sum != sum_before + odd + 2 * carry_ones ||
            length_after + removed != length_before + odd) {
            fprintf(stderr, "Exact digit identity failed at step %" PRIu64 ".\n", step);
            goto cleanup;
        }
        carry_total += carry_ones;
        removed_total += removed;
        sum_before_total += sum_before;
        sum_after_total += sum;
        if (carry_ones < carry_min) carry_min = carry_ones;
        if (carry_ones > carry_max) carry_max = carry_ones;
        if (ledger && fprintf(ledger,
            "%s[%u,%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64
            ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 ",%" PRIu64 "]",
            step ? ",\n" : "", odd, length_before, length_after, sum_before,
            sum, carry_ones, removed, ones_before, ones) < 0) goto io_error;
    }
    if (trace && (steps & 7) && fputc((int)trace_byte, trace) == EOF) goto io_error;
    if (ledger && fputs("\n]\n", ledger) == EOF) goto io_error;
    if (!steps) carry_min = 0;
    if (2 * sum_after_total != sum_before_total + odd_count + 2 * carry_total ||
        (uint64_t)(end - begin) + removed_total != m + odd_count) {
        fprintf(stderr, "Exact aggregate digit identity failed.\n");
        goto cleanup;
    }

    uint64_t digit_counts[3] = {0, 0, 0};
    for (size_t pos = begin; pos < end; ++pos) ++digit_counts[digits[pos]];
    if (digits_path) {
        if (!(digit_file = open_output(digits_path, "wb"))) goto cleanup;
        for (size_t pos = begin; pos < end; ++pos)
            if (fputc('0' + digits[pos], digit_file) == EOF) goto io_error;
    }
    if (trace) { FILE *file = trace; trace = NULL; if (fclose(file)) goto io_error; }
    if (ledger) { FILE *file = ledger; ledger = NULL; if (fclose(file)) goto io_error; }
    if (digit_file) { FILE *file = digit_file; digit_file = NULL; if (fclose(file)) goto io_error; }

    if (printf("{\"m\":%" PRIu64 ",\"steps\":%" PRIu64
        ",\"odd_steps\":%" PRIu64 ",\"initial_length\":%" PRIu64
        ",\"final_length\":%" PRIu64 ",\"initial_digit_sum\":%" PRIu64
        ",\"final_digit_sum\":%" PRIu64 ",\"initial_count_ones\":0"
        ",\"final_count_ones\":%" PRIu64 ",\"final_digit_counts\":[%" PRIu64
        ",%" PRIu64 ",%" PRIu64 "]"
        ",\"total_leading_digits_removed\":%" PRIu64
        ",\"total_carry_ones\":%" PRIu64 ",\"total_scanned_digits\":%" PRIu64
        ",\"minimum_step_carry_ones\":%" PRIu64
        ",\"maximum_step_carry_ones\":%" PRIu64
        ",\"total_state_digit_sum_before\":%" PRIu64
        ",\"total_state_digit_sum_after\":%" PRIu64
        ",\"trace_encoding\":\"packed parity bits, LSB first\""
        ",\"scope\":\"Exact finite ternary computation; no uniform estimate.\"}\n",
        m, steps, odd_count, m, (uint64_t)(end - begin), 2 * m, sum, ones,
        digit_counts[0], digit_counts[1], digit_counts[2], removed_total,
        carry_total, scanned_total, carry_min, carry_max,
        sum_before_total, sum_after_total) < 0) goto io_error;
    if (fflush(stdout)) goto io_error;
    status = 0;
    goto cleanup;

io_error:
    fprintf(stderr, "Output write failed: %s\n", strerror(errno));
cleanup:
    if (trace) fclose(trace);
    if (ledger) fclose(ledger);
    if (digit_file) fclose(digit_file);
    free(digits);
    return status;
}
