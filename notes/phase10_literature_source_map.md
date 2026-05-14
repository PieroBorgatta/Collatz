# Phase 10 Literature Source Map

Date: 2026-05-13

Status: source-audit note.  This file records which local primary or
near-primary documents support the Phase 10 literature matrix.  It does
not import any result into the Collatz project without checking its
hypotheses.

## 1. Transfer-operator core

| Topic | Local source | Usable hypothesis pattern | Phase 10 warning |
|---|---|---|---|
| Baladi positive transfer operators | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/ocr_text/baladi_positive_transfer_operators.ocr.txt` and corresponding PDF | Lasota-Yorke discipline, positive operators, decay/quasi-compact language | does not define our operator; no direct spectral gap transfer |
| Keller-Liverani stability | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/03_Keller_Liverani_1999.pdf` | mixed strong-to-weak convergence plus uniform bounds for spectral stability | unusable until `FULL_T` is proved to approximate an operator `L` |
| Hennion spectral theorem | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/sur-un-theoreme-spectral-et-son-application-aux-noyaux-4vxcqomst7.pdf` | essential spectral radius bounds from compactness/LY-type hypotheses | all local compactness and LY hypotheses are currently open |

## 2. Countable symbolic systems

| Topic | Local source | Usable hypothesis pattern | Phase 10 warning |
|---|---|---|---|
| Sarig thermodynamic formalism | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/ocr_text/pr_4.ocr.txt` | countable Markov shifts, Gurevich pressure, positive recurrence, RPF | requires an actual CMS and recurrence/summability proofs |
| Sarig Gibbs/BIP criterion | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/ocr_text/gibbs1.ocr.txt` | summable variation, finite pressure, BIP for Gibbs measures | BIP is not automatic for episode graphs |
| Topological Markov shifts with holes | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/arxiv_top50/pdf/2207.08085 - Quasi-compactness of transfer operators for topological Markov shifts with holes.pdf` | countable TMS, weak Lipschitz/summable potential, holes, quasi-compactness | relevant only after an episode/CMS model is constructed |
| Bowen finite symbolic thermodynamics | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/Bowen_LN_Math_470_second_ed_v2013.pdf` | finite Markov partitions, bounded distortion, equilibrium states | useful intuition, dangerous if applied to countable/killed case |

## 3. Countable branches, GDMS, and certified numerics

| Topic | Local source | Usable hypothesis pattern | Phase 10 warning |
|---|---|---|---|
| Countably many interval branches | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/arxiv_top50/pdf/2406.19929 - Quasi-compactness of Frobenius-Perron Operator for Piecewise Convex Maps with Countable Branches.pdf` | BV/L1 LY inequality for countable monotone/convex interval branches | geometry differs from Collatz residue/return dynamics |
| GDMS | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/HGDMS_09-19-2008.pdf` | graph-directed Markov systems with contracting branches and pressure | current project has transition statistics, not contracting maps yet |
| Certified spectral approximation | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/arxiv_top50/pdf/2602.19435 - Certified spectral approximation of transfer operators and the Gauss map.pdf` | finite-rank spectral certification from explicit approximation/DFLY bounds | helpful only after explicit approximation error is available |

## 4. p-adic and non-Archimedean sources

| Topic | Local source | Usable hypothesis pattern | Phase 10 warning |
|---|---|---|---|
| p-adic shadowing/stability | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/arxiv_top50/pdf/2001.02737 - Shadowing and Stability in p-adic dynamics.pdf` | p-adic stability and locally scaling maps | supports profinite intuition, not transfer spectral theory |
| non-Archimedean zeta functions | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/Studi_Operatori_Trasferimento/2508.19374v2.pdf` | Ruelle zeta functions for non-Archimedean rational maps | related language only; not a current model for `full_T` |

## 5. Chang 2026

| Topic | Local source | Usable hypothesis pattern | Phase 10 warning |
|---|---|---|---|
| Chang human-LLM Collatz survey | `/Volumes/AFUOCO/SVILUPPO/TEORIE/arxiv-affini/arxiv_top50/pdf/2603.11066 - Exploring Collatz Dynamics with Human-LLM Collaboration.pdf` | residue/Syracuse transfer operators on odd residues modulo powers of two; phantom-cycle terminology | not the same operator as killed weighted first-return `full_T`; verdict: partially compatible, no direct leverage |

The Chang PDF checked locally is arXiv `2603.11066v6`, dated
`22 Apr 2026`, and explicitly says it does not prove the Collatz
conjecture.

Online primary-source check:

```text
https://arxiv.org/abs/2603.11066
```

As of 2026-05-13, arXiv lists the latest version as `v6`, last revised
`22 Apr 2026`, with DOI `10.48550/arXiv.2603.11066`.

## 6. Operational Rule

Do not cite any theorem from this map as applicable to Phase 10 unless
the local operator `L`, Banach spaces, projection scheme, and all named
hypotheses have been matched explicitly.

## 7. Online Primary-Source Checks

These checks are bibliographic controls only.  They do not make any
theorem applicable to Phase 10.

| Topic | Primary online source | Checked fact | Phase 10 use |
|---|---|---|---|
| Keller-Liverani | `https://eudml.org/doc/84369` | Keller and Liverani, "Stability of the spectrum for transfer operators", Annali della Scuola Normale Superiore di Pisa, 28(1), 141-152, 1999 | cite for mixed strong/weak spectral stability only after a genuine approximating family is defined |
| Hennion | `https://www.ams.org/proc/1993-118-02/S0002-9939-1993-1129880-8/` | Hennion, "Sur un theoreme spectral et son application aux noyaux lipchitziens", Proc. Amer. Math. Soc. 118, 627-634, 1993 | cite for essential spectral radius/quasi-compactness skeleton only after LY-type compactness hypotheses are proved |
| Sarig | `https://doi.org/10.1017/S0143385799146820` | Sarig, "Thermodynamic formalism for countable Markov shifts", Ergodic Theory and Dynamical Systems 19(6), 1565-1593, 1999 | cite for CMS/RPF/positive recurrence only after an actual countable Markov shift and summable potential are built |
| Chang 2026 | `https://arxiv.org/abs/2603.11066` | arXiv lists `2603.11066v6`, last revised `22 Apr 2026`; the abstract explicitly says the work is not a proof of Collatz | cite as concurrent Collatz/phantom/transfer-operator context, not as a kernel identification for `full_T` |

Compatibility verdicts:

- Keller-Liverani: compatible only with a future mixed-norm convergence
  theorem; currently premature.
- Hennion: compatible only with a future LY/compactness theorem;
  currently premature.
- Sarig: plausible language for an episode/CMS branch, but false analogy
  unless positive recurrence, pressure, and summable variation are
  established.
- Chang: partially compatible terminology and Collatz context; operator
  compatibility remains unclear to unlikely for the current `full_T`
  objects.
