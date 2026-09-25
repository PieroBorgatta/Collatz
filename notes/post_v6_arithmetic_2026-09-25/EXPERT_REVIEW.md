# A specific parity-block question for a dyadic tower

Working note, 25 September 2026. Prepared for possible specialist review;
not sent externally. This is an open problem and an account of limitations
of attempted methods, not a proof of Collatz or a claim of priority.

Let \(T(x)=x/2\) for even \(x\), \((3x+1)/2\) for odd \(x\), and set

\[
 Q_v=(9^{2^v}-1)/2^{v+3},\qquad
 H_v=\lceil589\,2^v/612\rceil,\qquad D_v=128v^2.
\]

Write \(J_v(r)\) for the number of odd steps among the first \(r\)
iterations of \(T\) from \(Q_v\). A sufficient, currently unproved
working hypothesis is that every interval \([r,r+b)\subseteq[0,H_v)\)
with \(j=J_v(r+b)-J_v(r)\) satisfies

\[
 589j-305b\le D_v\qquad(v\ge15).
 \tag{A}
\]

This implies the previously established parity-count criterion for a
visit below the original source \(N_v=(2^{3\cdot2^v-5}-11)/3\).
It is stronger than what is needed for that descent. Exact checks through
\(v=24\) support (A) in the tested range; the coefficient 128 was frozen
before testing levels 22–24. Their complete parity traces were reproduced
by separate Python and C/GMP implementations. No statistical inference
to all levels is intended.

For a prescribed prefix \(\alpha\) of length \(r\) with \(k\) odd steps
and affine constant \(A\), followed by a block \(\beta\) of length
\(b\) with \(j\) odd steps and constant \(B\), put

\[
 C=3^jA+2^rB,\quad L=v+3+r+b,\quad E=2^{v+1}+k+j.
\]

The complete word is the parity prefix of \(Q_v\) if and only if

\[
 2^L\mid3^E+c,\qquad c=2^{v+3}C-3^{k+j}.
 \tag{B}
\]

For positive-loss blocks, \(c\ge2^{v+r+j+1}\) and
\(L\le2(v+r+j+1)\). Hence the explicit specialization

\[
 \nu_2(3^E+c)<180000\max\{\ln c,\ln2\}
                    \max\{\ln(E+1),800\}
\]

of Chim's two-logarithm bound, previously used in this project, has a
right-hand side exceeding \(36\,000\,000L\). This particular estimate
cannot exclude (B). It does not rule out sharper bounds or other encodings.

If \(a_\beta\equiv-3^{-j}B\pmod{2^b}\), an equivalent form is

\[
 2^L\mid3^{2^{v+1}+k}+c_s,\qquad
 c_s=2^{v+3}(A-2^ra_\beta)-3^k.
 \tag{C}
\]

Signed representatives of \(a_\beta\) permit cancellation; no uniform
lower bound of comparable strength has been proved here for the minimum
absolute representative of \(c_s\pmod{2^L}\). For a repeated word
\(w^t\), one may instead use the rational 2-adic fixed point
\(B_w/(2^d-3^s)\), where \(d,s\) are the length and odd count of \(w\).
The height can then depend on the period rather than all repetitions,
but the preceding prefix remains an uncontrolled cost.

The new digital-complexity literature is relevant to
\(3^{2^{v+1}}=1+2^{v+3}Q_v\), but no bridge from an interval violating
(A) to the required structure of the ordinary binary representation is
known to us. Even within parity words, a biased interval need not have
low factor complexity: coding every length-\(t\) binary word by
\(0\mapsto11010,1\mapsto10110\) and concatenating gives length
\(5t2^t\), odd count \(3t2^t\), loss \(242t2^t\), no `111`, and at
least \(2^t\) distinct factors of length \(5t\). For \(v=2t,t\ge8\)
this fits the horizon and exceeds \(D_v\). These are admissible parity
cylinders; they are not claimed to occur for \(Q_v\).

The exact parameterization
\(\mathcal F_v(q)=(\exp(2^vq\log9)-1)/2^{v+3}\) is a 2-adic
isometric bijection. Every finite parity cylinder is realized for some
parameter residue. The distinguished parameter \(q=1\) is the arithmetic
restriction that must be used.

Questions for review:

1. Can the special exponent \(2^{v+1}+k\), together with the valid
   prefix and (C), yield a useful uniform cancellation estimate? Which
   additional hypothesis would make it possible?
2. Can a violating interval be reduced, using the tower arithmetic, to
   a bounded-dimensional relation among S-units, or to a genuinely
   applicable digital-repetition condition? The number of terms of the
   raw affine sum is unbounded; invoking a fixed-dimensional subspace
   theorem directly would leave a gap.
3. Is there a weaker arithmetic statement sufficient for the final
   parity count, avoiding the maximum-over-all-intervals condition (A)?

Full derivations and reproducible finite evidence:
[RESULTS_IT.md](RESULTS_IT.md). Precise primary references, including
Chim (2025) and Bugeaud's August 2026 preprint:
[LITERATURE_IT.md](LITERATURE_IT.md). General proofs in this note are
paper-level arguments with internal review, not Lean-checked statements.
