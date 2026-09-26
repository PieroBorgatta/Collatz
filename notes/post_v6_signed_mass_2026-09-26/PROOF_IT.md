# H.2 — Anche tutte le correzioni firmate dell'ultimo esponente hanno immagine sparsa

26 settembre 2026. Piero Borgatta con assistenza Codex.

**Risultato:** per target dispari positivi distinti n,y, il metodo che
conserva tutti gli esponenti salvo l'ultimo produce soltanto o(X) immagini
distinte entro DX da sorgenti entro X. Questo vale includendo **tutte**
le correzioni intere ammissibili, positive e negative, e consentendo
**qualsiasi nuovo fattore diadico** all'immagine. D>0 è fissato ma può
dipendere da n,y. Non serve assumere densità positiva dei bacini.

Il risultato chiude il metodo dell'ultimo esponente come mezzo per
trasferire una massa di densità positiva a dilatazione fissa. Non confuta
H e non riguarda trasferimenti che cambiano anche gli esponenti precedenti.
È una prova matematica su carta; il modulo Lean verifica i suoi lemmi
aritmetici, non il passaggio asintotico completo. Nessuna rivendicazione
di priorità o di revisione umana indipendente.

## 1. Relazione di trasporto, non soltanto una funzione

Fissiamo n,y dispari positivi, n≠y. Per ogni u dispari positivo che raggiunge
n, prendiamo la parola w=(a₁,…,a_k) del **primo** arrivo. Quando n non ha
ritorni positivi, come nel dominio di H, questa è l'unica parola che
raggiunge n. Per k≥1 e per ogni δ∈Z tale che a_k+δ≥1, consideriamo la
parola w'=(a₁,…,a_(k−1),a_k+δ). Se w' è esatta da v>0 dispari a y,
ammettiamo **tutte** le immagini 2^f v, f≥0.

Sia I_D(X) l'insieme di queste immagini 2^f v≤DX ottenute da u≤X.
Il dominio include tutte le parti dispari delle sorgenti ordinarie ≤X;
non impone di conservare il loro fattore diadico. Per u=n, k=0, possiamo
aggiungere liberamente i numeri 2^f y≤DX: sono O(log X) e non cambiano
la conclusione.

**Teorema.** Per ogni n,y,D fissati come sopra,

\[
\boxed{|I_D(X)|=o(X)\quad(X\to\infty).}\tag{T}
\]

Si contano immagini **distinte**, non parole né sorgenti con molteplicità.
Non si assume una scelta ottimale di δ, un bound sulle fibre o una regola
di accoppiamento: tutte le possibilità sono già incluse nella relazione.

## 2. Due identità aritmetiche

Posti A=Σa_i e C=Σ_(j=0)^(k−1)3^(k−1−j)2^(a₁+…+a_j), abbiamo C>0 e

\[
3^k u+C=2^A n,\qquad 3^k v+C=2^{A+\delta}y.\tag{1}
\]

La stessa C compare perché non dipende dall'ultimo esponente. L'esponente
A+δ resta positivo. In aritmetica razionale, ponendo r=2^δ y/n,

\[
v=r u+(r-1)\frac C{3^k}.\tag{2}
\]

Quindi

\[
r\ge1\Rightarrow v\ge r u,\qquad
r\le1\Rightarrow v\le r u.\tag{3}
\]

Nel primo caso la sorgente si espande almeno del fattore r; nel secondo
la sua immagine si comprime almeno di quel fattore. Le collisioni non
possono aumentare il numero di immagini distinte.

Le identità (1) implicano inoltre

\[
\begin{cases}
3^k\mid 2^\delta y-n,&\delta\ge0,\\
3^k\mid y-2^{-\delta}n,&\delta<0.
\end{cases}\tag{4}
\]

Si cancella la potenza di 2, coprima con 3^k. Per ogni M fissato, i
numeratori in (4) per |δ|≤M sono interi **non nulli**: due dispari
positivi distinti non hanno rapporto uguale a una potenza intera di 2.
Il loro modulo è al più 2^M max(n,y). Scelto K con

\[
3^K>2^M\max(n,y),
\]

si ottiene

\[
k>K\quad\Rightarrow\quad |\delta|>M.\tag{5}
\]

Non si assume alcuna stima probabilistica sui logaritmi discreti.

## 3. Le immagini a profondità limitata sono o(X)

Per K fissato, il numero di predecessori ordinari di y entro DX che lo
raggiungono in al più K passi dispari è

\[
O_{K,D}((1+\log X)^{K+1})=o(X).\tag{6}
\]

Infatti la parte dispari v≤DX ha iterati iniziali S^j(v)≤2^jDX. Ogni
esponente della parola è al più log₂(DX)+K+2. Una parola e il target
determinano al più una sorgente dispari tramite (1); le lunghezze ≤K
danno O_K((1+log X)^K) parole, e i sollevamenti diadici al più un altro
fattore logaritmico. Questo conta direttamente le possibili **immagini**,
anche se provengono da molte sorgenti o molte correzioni.

## 4. Le due code delle correzioni

Fissiamo F≥0 e M abbastanza grande da avere
2^M>max(n/y,y/n). Il valore K è quello scelto nel §2.
Le immagini a profondità k≤K sono già coperte da (6).

**Correzioni positive δ>M.** Da (3), se 2^f v≤DX allora

\[
u\le\frac{Dn}{y}\,2^{-f-\delta}X.
\]

Per ogni coppia δ,f e per ogni sorgente dispari u, il primo arrivo a n
fissa w; cambiare l'ultimo esponente di δ determina al più una v. Non
serve che sorgenti diverse abbiano immagini diverse. Il numero di
immagini per quella coppia è al più il numero di sorgenti, maggiorato
dall'intervallo indicato. Sommando le due serie geometriche,

\[
\#\{\text{immagini con }\delta>M\}
\le\frac{2Dn}{y}\,2^{-M}X.\tag{7}
\]

La stima include tutte le correzioni positive e tutti i fattori diadici.

**Correzioni negative δ<−M.** Ora (3) implica

\[
v\le\frac yn2^{-M}X=\varepsilon_M X.
\]

Per f≤F, le immagini appartengono all'unione di F+1 copie di un insieme
di al più ε_M X interi; sono dunque al più (F+1)ε_M X. Per f>F, tutte
le immagini sono divisibili per 2^(F+1). Entro DX ce ne sono al più
DX/2^(F+1), indipendentemente da quante sorgenti o correzioni le producano.
Quindi

\[
\#\{\text{immagini con }\delta<-M\}
\le (F+1)\frac yn2^{-M}X+\frac D{2^{F+1}}X.\tag{8}
\]

## 5. Ordine dei limiti e conclusione

Le (5)–(8) esauriscono tutte le immagini. Per F,M fissati, e quindi K
fissato, facciamo prima X→∞:

\[
\limsup_{X\to\infty}\frac{|I_D(X)|}{X}
\le\left(\frac{2Dn}{y}+(F+1)\frac yn\right)2^{-M}
  +\frac D{2^{F+1}}.
\]

Facciamo poi M→∞ con F fissato, infine F→∞. Il limite superiore è zero;
il conteggio è nonnegativo, quindi vale (T). Non si scambia una densità
con una somma infinita di densità dei bacini. □

## 6. Conseguenza per il programma H

Se d_*(B(n))>0, nessuna selezione dentro questa relazione può fornire
\(|\text{immagini distinte entro }DX|\ge c_n|B(n)\cap[1,X]|-o(X)\)
con c_n>0 e D fissati. La positività serve soltanto per questa conseguenza;
il teorema (T) è incondizionato.

Questo rafforza il [risultato H.1](../post_v6_basin_transport_2026-09-26/RESULTS_IT.md):
non occorre più restringersi a δ≥0, a una scelta di δ, al sottobacino
B(11) o alla conservazione del fattore diadico. Anche i controlli geometrici
dei pesi sulle fibre non producono nuovi interi fuori dall'insieme I_D(X),
che ha densità zero.

**H resta aperta.** Il bacino di y può avere densità positiva grazie a
predecessori non ottenibili da sorgenti ≤X con questa relazione. Modificare
altri esponenti cambia C, quindi l'identità decisiva (2) non si applica.
Anche cambiare profondità esce dall'enunciato. Non è dimostrata qui
l'impossibilità di tali confronti più generali.

La decisione operativa è chiudere l'intera famiglia dei trasporti che
cambiano soltanto l'ultimo esponente. Per riaprire una ricerca di H serve
una costruzione che modifichi la costante affine C e controlli una massa
relativa di sorgenti, con altezza e molteplicità esplicite. Non abbiamo
ancora una tale costruzione.

## 7. Requisito algebrico per un metodo diverso

Se si mantengono k passi ma si cambia anche la costante affine da C a C',
ponendo r=2^(A'−A)y/n, l'identità generale diventa

\[
v=ru+\frac{rC-C'}{3^k}.
\]

Quindi, per ottenere un'immagine con 0<v≤Lu quando r>L, è necessario

\[
(r-L)3^ku+rC\le C'<r3^ku+rC.
\]

Questa finestra è soltanto una condizione algebrica necessaria: C' e A'
non sono parametri liberi, devono provenire dalla stessa parola ammissibile,
con tutte le divisioni esatte e le valutazioni prescritte. Inoltre servirebbe
realizzarla su una quota positiva di sorgenti, controllando le collisioni.
La formula rende concreto il prossimo problema ma non ne dà una soluzione;
non autorizza a dedurre H dalla sola possibilità di modificare C.
