#!/usr/bin/env python3
"""Tests of finite parity lifts, truncated valuations, and sufficiency."""
import unittest

import modular_certificate as cert
import verify_certificates as independent
from separation_probe import first_separation


def ordinary_prefix(n, length):
    count = 0
    for _ in range(length):
        if n % 2:
            n = (3*n+1)//2
            count += 1
        else:
            n //= 2
    return n,count


def direct_descent(v, cap):
    M = 2**v
    n = (2**(3*M-5)-11)//3
    x = (9**M-1)//2**(v+3)
    for k in range(cap+1):
        if x < n:
            return k
        x = 3*x+1
        while x % 2 == 0:
            x //= 2
    return None


class CertificateChecks(unittest.TestCase):
    def test_rational_bound_and_input_domain(self):
        self.assertLess(3**306,2**485)
        self.assertEqual(cert.precision_for(5,16),31)
        for v,budget in [(4,1),(5,0),(5,33)]:
            with self.assertRaises(ValueError):
                cert.precision_for(v,budget)

    def test_affine_blocks_on_all_small_residues_and_lifts(self):
        for width in range(1,9):
            for residue,(odd,multiplier,constant) in enumerate(cert.block_table(width)):
                for lift in (0,1,3):
                    x = residue+(lift << width)
                    endpoint,count = ordinary_prefix(x,width)
                    self.assertEqual(count,odd)
                    self.assertEqual((endpoint << width),multiplier*x+constant)

    def test_parity_counts_are_independent_of_block_boundaries(self):
        for bits in range(1,11):
            for residue in range(1 << bits):
                _,expected = ordinary_prefix(residue,bits)
                for width in (1,4,16):
                    self.assertEqual(cert.parity_count(residue,bits,width)[0],expected)

    def test_partial_last_syracuse_step_is_allowed(self):
        # 5 -> 1 is one Syracuse step with exponent 4. Three T steps
        # have only reached 2, but already certify exponent sum >=3.
        self.assertEqual(ordinary_prefix(5,3),(2,1))
        self.assertEqual(cert.parity_count(5,3)[0],1)
        self.assertEqual(cert.parity_count(1,1)[0],1)

    def test_initial_modular_powers_against_full_small_integers(self):
        for v in range(5,11):
            full = (9**(1 << v)-1)//(1 << (v+3))
            for bits in (1,16,64,cert.precision_for(v,1 << (v-1))):
                self.assertEqual(cert.initial_residue(v,bits),full % (1 << bits))

    def test_success_implies_actual_descent_in_small_cases(self):
        successes = 0
        for v in range(5,11):
            for budget in (1,2,16,1 << (v-1),1 << v):
                result = cert.certificate(v,budget)
                if result['certified']:
                    successes += 1
                    bound = result['descent_time_upper_bound']
                    self.assertLessEqual(bound,budget)
                    self.assertIsNotNone(direct_descent(v,bound))
        self.assertGreaterEqual(successes,6)

    def test_failed_certificate_does_not_refute_descent(self):
        result = cert.certificate(6,32)
        self.assertFalse(result['certified'])
        self.assertIsNone(result['descent_time_upper_bound'])
        self.assertEqual(direct_descent(6,32),28)

    def test_independent_verifier_rejects_altered_records(self):
        original = cert.certificate(5,16)
        evidence = independent.verify_attempt(original)
        self.assertEqual(evidence['odd_steps'],14)
        changes = [
            {'odd_steps':15,'descent_time_upper_bound':15},
            {'precision_bits':32},
            {'initial_residue_sha256':'0'*64},
            {'certified':False,'descent_time_upper_bound':None},
        ]
        for change in changes:
            with self.assertRaises(independent.VerificationError):
                independent.verify_attempt(dict(original,**change))

    def test_independent_last_exponent_is_a_lower_bound(self):
        evidence = independent.direct_syracuse_count(5,3)
        self.assertEqual(evidence['odd_steps'],1)
        self.assertEqual(evidence['final_exponent_lower_bound'],3)
        self.assertFalse(evidence['final_exponent_is_exact'])

    def test_separation_certificates_against_small_full_integers(self):
        for v in range(5,10):
            record = first_separation(v)
            for branch in record['branches']:
                j = branch['level']
                M = 1 << j
                x = (9**M-1)//(1 << (j+3))
                source = ((1 << (3*M-5))-11)//3
                for a in record['common_word']+[branch['exponent']]:
                    x = (3*x+1)//(1 << a)
                    self.assertEqual(x % 2,1)
                self.assertGreater(x,source)
        with self.assertRaises(ValueError):
            first_separation(6,bits=9)


if __name__ == '__main__':
    unittest.main()
