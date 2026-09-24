#!/usr/bin/env python3
"""Boundary and independent-arithmetic checks for the level experiment."""
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import levels_probe as probe


def slow_step(n):
    n = 3*n+1
    a = 0
    while n % 2 == 0:
        n //= 2
        a += 1
    return n, a


class LevelChecks(unittest.TestCase):
    def test_recurrence_and_nonadjacent_levels(self):
        values = {v:probe.quotient(v) for v in range(1,12)}
        for v in range(1,11):
            self.assertEqual(values[v+1],values[v]+(1 << (v+2))*values[v]**2)
            for w in range(v+1,12):
                self.assertEqual(probe.valuation(values[w]-values[v]),v+2)
                pair = probe.common_prefix(values[v],values[w],v)
                x,y = values[v],values[w]
                for a in pair['word']:
                    x,ax = slow_step(x)
                    y,ay = slow_step(y)
                    self.assertEqual((ax,ay),(a,a))
                _,ax = slow_step(x)
                _,ay = slow_step(y)
                self.assertNotEqual(ax,ay)
                self.assertLessEqual(pair['common_sum'],v+1)
                self.assertGreater(pair['common_sum']+ax,v+1)
                self.assertGreater(pair['common_sum']+ay,v+1)
                self.assertEqual(min(ax,ay),v+2-pair['common_sum'])

    def test_larger_divergent_exponent_is_only_a_lower_bound(self):
        # At v=6, 9 input bits certify [3,1,1], then [3, >=4].
        # The higher level's actual exponent is 8, not 4.
        x,y = probe.quotient(6),probe.quotient(7)
        pair = probe.common_prefix(x,y,6)
        self.assertEqual(pair['word'],[3,1,1])
        self.assertEqual(pair['larger_divergent_exponent_at_least'],4)
        for _ in pair['word']:
            x,_ = slow_step(x)
            y,_ = slow_step(y)
        self.assertEqual((slow_step(x)[1],slow_step(y)[1]),(3,8))
        # Any lifts of those 9-bit residues retain the certified prefix.
        for i in range(4):
            for j in range(4):
                self.assertEqual(probe.common_prefix(probe.quotient(6)+512*i,
                    probe.quotient(7)+512*j,6),pair)

    def test_ambiguous_precision_stops_before_claiming_an_exponent(self):
        self.assertEqual(probe.certified_prefix(1,2),([],2))
        # 1 and 5 are equal modulo 4 but their exact exponents are 2 and 4.
        self.assertEqual((slow_step(1)[1],slow_step(5)[1]),(2,4))
        self.assertEqual(probe.certified_prefix(61,6),([3,1,1],1))

    def test_three_independent_limit_formulas(self):
        for bits in range(1,65):
            residue = probe.limit_from_recurrence(bits)
            self.assertEqual(residue,probe.limit_from_log_series(bits))
            self.assertEqual(residue,probe.quotient_mod(max(1,bits-2),bits))
            self.assertEqual(residue % 2,1)

    def test_cap_records_censoring_and_exact_boundary(self):
        pair = probe.common_prefix(probe.quotient(5),probe.quotient(6),5)
        old = {'status':'descended','tau':'8','steps_observed':'8','exponent_sum':'17'}
        for cap in (0,4):
            row = probe.actual_case(5,pair,cap=cap)
            self.assertEqual(row['status'],'censored')
            self.assertIsNone(row['tau_from_Q'])
            self.assertEqual(row['steps_observed'],cap)
            probe.compare_previous(row,old)
        row = probe.actual_case(5,pair,cap=5)
        self.assertEqual(row['status'],'descended')
        self.assertEqual(row['tau_from_Q'],5)
        self.assertEqual(row['exponent_sum'],12)
        probe.compare_previous(row,old)
        old_censored = {'status':'censored','tau':'','steps_observed':'3',
                        'exponent_sum':'5'}
        probe.compare_previous(row,old_censored)
        probe.compare_previous(probe.actual_case(5,pair,cap=0),old_censored)
        # A claimed old descent before the new censoring time is inconsistent.
        with self.assertRaises(AssertionError):
            probe.compare_previous(probe.actual_case(5,pair,cap=4),
                dict(old,tau='7',steps_observed='7'))

    def test_small_valid_cli_configuration(self):
        with tempfile.TemporaryDirectory() as output:
            subprocess.run([sys.executable,str(Path(probe.__file__)),
                '--levels','5','--precision','8','--actual-max-v','5',
                '--output-dir',output],check=True,capture_output=True,text=True)
            result = json.loads((Path(output)/'levels_results.json').read_text())
            self.assertEqual(result['modular_level_pairs'],5)
            self.assertEqual(result['actual_steps'],5)
            self.assertEqual(result['censored_levels'],[])


if __name__ == '__main__':
    unittest.main()
