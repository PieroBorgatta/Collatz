# Three short precisions: exact SCT obstruction

Date: 2026-07-23

## Question

Can the three short phantom precisions

\[
p_1(n)=\nu_2(n+1),\qquad
p_5(n)=\nu_2(n+5),\qquad
p_7(n)=\nu_2(n+7)
\]

alone provide a size-change termination argument for the expansive macros
`[1]`, `[1,2]`, and `[2,1]`?

No.  They are useful local traces, but the library is not closed under
composition.  This is an exact algebraic obstruction, not a failure found by
sampling.

## Exact local size-change matrices

For one accelerated step \(2^e m=3n+1\), a shift \(C\) transports to \(C'\)
with an exact loss of \(e\) bits precisely when

\[
1+2^e C'=3C.
\]

Inside the short library \(\{1,5,7\}\), the only transports are

\[
\begin{array}{c|c}
e=1 & 1\to1,\quad 5\to7\\
e=2 & 7\to5.
\end{array}
\]

Consequently the universal strict size-change relations are:

\[
\begin{array}{c|l}
\text{macro} & \text{relations}\\ \hline
[1]   & p'_1<p_1,\quad p'_7<p_5,\\
[1,2] & p'_5<p_5,\\
[2,1] & p'_7<p_7.
\end{array}
\]

All displayed inequalities are actually exact:

\[
p'_1+1=p_1,\quad p'_7+1=p_5,\quad
p'_5+3=p_5,\quad p'_7+3=p_7,
\]

in the corresponding rows.

There is no trace through the matrix product `[1] ; [1,2]`: after `[1]` the
available target labels are \(1\) and \(7\), whereas `[1,2]` only accepts
label \(5\) as a source trace.  Thus the ordinary SCT product is already
empty.

## The missing relations really are absent

The sparse matrices are not an artifact of a weak proof.  Exact infinite
families make each missing target precision arbitrarily large while all
three source precisions stay fixed.

For `[1,2]`, define

\[
q_0=1,\qquad q_{s+1}=64q_s+49.
\]

Induction gives

\[
9q_s+7=2^{6s+4},\qquad q_s\equiv1\pmod4.
\]

With \(n_s=11+16q_s\), the word `[1,2]` matches exactly and

\[
(p_1,p_5,p_7)(n_s)=(2,5,1),
\]
\[
\operatorname{eval}_{[1,2]}(n_s)
 =13+18q_s=2^{6s+5}-1.
\]

Therefore the destination \(p_1\) equals \(6s+5\), although every source
trace is bounded by \(5\).  A symmetric family obtained from
\(9t_s+10=2^{6s+6}\) makes destination \(p_7\) unbounded while the source
triple is \((2,4,1)\).

Analogous one-line constructions show:

- under `[1]`, solve \(3n+11=2^{R+1}\); the source triple is
  \((3,2,1)\) while destination \(p_5=R\);
- still under `[1]`, \(n=2^R-1\) makes destination \(p_1=R-1\)
  exceed source \(p_5=2,p_7=1\), while \(n=2^R-5\) makes destination
  \(p_7=R-1\) exceed source \(p_1=2,p_7=1\);
- under `[2,1]`, solve \(3t+2=2^R\) or \(9t+8=2^R\); the source triple can
  be held at \((1,1,4)\) while destination \(p_1\) or \(p_5\) diverges.

Hence no additional pairwise `≤` edge between the three short traces is
universally sound.

## Exact feasible lasso, not merely an abstract matrix path

The bad macro lasso is

\[
[1]\ ;\ [1,2],
\]

equivalently the exponent word \(W=[1,1,2]\).  Its affine action is

\[
F(n)=\frac{27n+19}{16},
\]

with formal 2-adic fixed point

\[
n_*=-\frac{19}{11}.
\]

At the boundary \(n_*\) and after the first macro:

\[
\begin{array}{c|c}
\text{position} & (p_1,p_5,p_7)\\ \hline
n_* & (3,2,1)\\
(3n_*+1)/2=-23/11 & (2,5,1)\\
F(n_*)=n_* & (3,2,1).
\end{array}
\]

This 2-adic lasso has arbitrarily long exact natural prefixes.  An explicit
family is

\[
N_k=\frac{2^{10k+13}-19}{11},
\]

or, without division,

\[
N_0=743,\qquad N_{k+1}=1024N_k+1767.
\]

It satisfies

\[
11N_k+19=2^{10k+13}.
\]

More generally, if

\[
11n+19=a\,2^r,\qquad a\ \text{odd},
\]

then one matched copy of \(W\) produces \(m=F(n)\) with

\[
11m+19=27a\,2^{r-4}.
\]

As long as \(r\) remains above the finite matching threshold, every macro
boundary has trace triple \((3,2,1)\), and every middle state has
\((2,5,1)\).  Choosing \(k\) large gives an arbitrarily long feasible
repetition.  Exact cylinder guards therefore do not remove the SCT
counterpath.

## What survives: compatible dynamic labels

The obstruction kills the fixed short library, not trace switching itself.
The lasso carries the affine labels

\[
(11,19)\xrightarrow{e=1}(11,23)
\xrightarrow{e=1}(11,29)
\xrightarrow{e=2}(11,19).
\]

Each edge satisfies the compatibility equations

\[
3D'=3D,\qquad D'+2^eC'=3C.
\]

Thus

\[
\nu_2(11m+19)+4=\nu_2(11n+19)
\]

after one lasso.  The rank omitted by the three short traces is exactly the
precision relative to \(-19/11\).

## Kill criterion and design decision

A proposed finite trace library must be rejected if an admissible macro
lasso has:

1. arbitrarily long exact natural realizations;
2. a repeated finite trace/control state;
3. no infinitely descending thread in the product of its universal
   size-change matrices.

The library \(\{n+1,n+5,n+7\}\) fails all three conditions on
`[1] ; [1,2]`.

The appropriate replacement is closure under the compatible affine
transport equations for pairs \((D,C)\), with the current label included in
the certificate.  Free relabeling is unsound: compatibility is what prevents
an arbitrary precision reset.
