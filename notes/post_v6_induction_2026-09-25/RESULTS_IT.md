# Trasferimento condizionale della discesa fra livelli

25 settembre 2026. Continuazione dei
[certificati modulari](../post_v6_certificates_2026-09-24/RESULTS_IT.md).

**Esito:** il criterio sufficiente generale di discesa è stato formalizzato
in Lean. Un lemma di trasferimento riduce il controllo dei tre coefficienti
quadratici a una sola disuguaglianza sui pesi moltiplicativi. Le regole
temporali più semplici falliscono sui dati disponibili e il cono proposto
non è invariante in generale. L'induzione sulla famiglia infinita resta
aperta. Non viene rivendicata priorità matematica per questi lemmi.

Entrambi i moduli hanno superato la compilazione locale. Le verifiche CI
sono in corso; lo stato conclusivo sarà registrato nel manifest di questa
cartella.

## 1. Criterio generale: la parte ora verificata da Lean

Indichiamo con S la mappa Syracuse e con

\[
 A_k(x)=\sum_{i<k}\nu_2(3S^i(x)+1),\qquad
 w_k(x)=3^k/2^{A_k(x)}.
\]

Il modulo [`DescentCertificate.lean`](../../lean/CollatzShadowing/DescentCertificate.lean)
dimostra, per x,N>0 e k<3N:

\[
 3^{k+1}x<2^{A_k(x)}(3N-k)
 \quad\Longrightarrow\quad
 \exists j\le k:\ S^j(x)<N.
\]

La conclusione riguarda una visita entro k; non richiede che l'endpoint
al tempo k sia sotto soglia. La somma A è quella dell'orbita effettiva.
Il termine additivo della dinamica è incluso nella dimostrazione.

La prova riusa il potenziale già formalizzato in `WeightedVisits`:
P_k=w_k/S^k(x). La dissipazione esatta dà P_k≤1/x e, se S^k(x)≥N,
la perdita al passo k è al più 1/(3Nx). Se nessuno dei primi k passi
è sotto soglia, P_k≥(3N-k)/(3Nx). Supponendo anche S^k(x)≥N,
si avrebbe P_k≤w_k/N, in contraddizione con il certificato.

Una seconda formulazione ammette un orizzonte conservativo K≥k e un
limite inferiore H≤A_k, purché K<3N e
3^(K+1)x<2^H(3N-K). Nessuna delle due formulazioni fornisce
automaticamente H.

## 2. Un solo coefficiente basta per trasferire la discesa

Consideriamo dapprima dati astratti interi X≥N>0 e c≥1, e poniamo

\[
 Y=X+cX^2,\qquad M=96N^2+704N+1287.
\]

Sia w un razionale positivo tale che wX<N. Fissiamo un tempo superiore
ℓ≤N e scriviamo w'=w_ℓ(Y). La condizione sufficiente è

\[
 \boxed{c w'\le96w^2.}
\]

Infatti wX<N≤X implica w<1. Quindi

\[
 w'Y\le96(wX)^2+96(wX)w/c<96N^2+96N.
\]

Il margine rispetto al certificato generale è esplicito:

\[
 3M-\ell-(288N^2+288N)=1824N+3861-\ell>0.
\]

Pertanto 3w'Y<3M−ℓ e il criterio della sezione 1 dà una visita sotto
M entro ℓ. Non abbiamo usato una discesa già osservata nell'orbita
superiore, né imposto limiti ai coefficienti lineare e costante.

Se S^k(X)<N, si può prendere w=w_k(X): il termine additivo dell'iterata
è non negativo, dunque wX≤S^k(X)<N. Attenzione: la sola informazione
«esiste j≤k con S^j(X)<N» non giustifica questa premessa al tempo k.
Si deve scegliere un tempo con endpoint inferiore effettivamente sotto
soglia, come il primo tempo di discesa.

Per la famiglia in studio, con v≥5,

\[
 Q_v=\frac{9^{2^v}-1}{2^{v+3}},\qquad
 N_v=\frac{2^{3\cdot2^v-5}-11}{3},
\]

abbiamo Q_(v+1)=Q_v+2^(v+2)Q_v² e
N_(v+1)=96N_v²+704N_v+1287. Con k=t_v, A=A_k(Q_v),
B=A_ℓ(Q_(v+1)), la condizione diventa

\[
 \alpha=2^{v+2+2A-B}3^{\ell-2k}\le96.
\]

In particolare, per ℓ=2k equivale esattamente a B≥2A+v−4.
Le potenze eventualmente negative si intendono razionali; il programma
usa solo prodotti e confronti di interi.

**Limite:** questo è un trasferimento condizionale. Manca una stima
uniforme della somma B a un tempo scelto indipendentemente dalla discesa
superiore. La relazione quadratica non fornisce tale stima.

## 3. Perché il cono precedente non si conserva

Per y=αx²+βx+γ e passi Syracuse effettivi con esponenti a,b,

\[
 \alpha'=\alpha 2^{2a-b}/3,\quad
 \beta'=2^{a-b}(\beta-2\alpha/3),\quad
 \gamma'=2^{-b}(\alpha/3-\beta+3\gamma+1).
\]

Il cono α≤96, β≤704, γ≤1287 non è invariante, nemmeno imponendo
β<0. Il controesempio x=5, y=96x²−x+2=2397 ha esponenti reali
(a,b)=(4,3), endpoint (1,899), e coefficienti successivi
(1024,−130,5).

Più in generale, per ogni a pari almeno 4, ponendo x=(2^a−1)/3,
y=96x²−x+2, si ottiene b=3 e
(α',β',γ')=(4·4^a,−65·2^(a−3),5). Il coefficiente principale può
crescere senza limite in un solo aggiornamento compatibile.

Questi esempi non sono stati mostrati raggiungibili dalla famiglia Q_v:
escludono l'invarianza dedotta dalle sole ipotesi del cono, non ogni
possibile proprietà specifica della famiglia.

## 4. Esplorazione retrospettiva con tempi deterministici

Il programma [`induction_probe.py`](induction_probe.py) ripercorre 13 coppie,
v=5,…,17, con quattro regole fissate nel codice a partire da v e dal
certificato inferiore k=t_v. Non cerca l'orizzonte aspettando la discesa
superiore. I tempi superiori già disponibili servono al confronto del
replay. Questo è un esperimento retrospettivo, non una preregistrazione
né una validazione su livelli nuovi.

| Tempo ℓ scelto | Trasferimento | Certificato generale diretto | Coppie ancora senza visita sotto soglia entro ℓ |
|---|---:|---:|---|
| 2k | 5/13 | 5/13 | 5, 7, 8, 11, 12, 14, 15, 17 |
| 2k+3v | 5/13 | 6/13 | 5, 8, 11, 12, 14, 15, 17 |
| 2k+v² | 6/13 | 7/13 | 8, 11, 12, 14, 15, 17 |
| 2k+2^(v−2) | 10/13 | 11/13 | 5, 8 |

Tutti i 52 tentativi, inclusi i fallimenti, sono conservati in
[`induction_results.json`](induction_results.json). In tutti i casi ℓ≤N_v.
Ogni trasferimento positivo implica il certificato generale e una visita
effettiva entro l'orizzonte, come controllato con aritmetica intera.

Il criterio è solo sufficiente. Ad esempio, per v=5 e ℓ=35 la discesa
superiore è già avvenuta al tempo 28, ma α≤96 fallisce. Per v=6,
il test α≤96 passa a ℓ=56 e fallisce a ℓ=74: non è monotono nel tempo.
Entrambi i tempi soddisfano comunque il certificato generale.
Il trasferimento riformula una condizione sufficiente utile per tentare
una ricorrenza fra livelli; non rafforza il certificato generale diretto.

Un dato particolarmente restrittivo è t_17=52527 e t_18=107678:
il ritardo rispetto al doppio è 2624. Qualsiasi proposta t_(v+1)≤2t_v+Cv
deve avere C≥2624/17 soltanto per superare questi dati; ciò non dimostra
che una costante uniforme esista. Analogamente, il fallimento di v²
non esclude ogni possibile multiplo costante di v².

La quarta regola passa per tutte le coppie osservate con v≥9, ma questa
osservazione non supera i precedenti certificati modulari diretti e non
costituisce evidenza sufficiente per una legge uniforme.

## 5. Obbligazione rimasta e criterio per il prossimo tentativo

Definendo E=A−k log₂3, il problema residuo è dimostrare, a un tempo
superiore specificato dalla regola,

\[
 E_{\rm superiore}\ge2E_{\rm inferiore}+v+2-\log_2 96.
\]

Cercare ℓ finché questa disuguaglianza riesce produce certificati finiti
validi; senza dimostrare che la ricerca termini per ogni livello non chiude
l'induzione. Una possibile strategia è trovare una proprietà preservata
delle parità effettive.
Per blocchi di Δk passi inferiori e Δℓ passi superiori, il moltiplicatore del
coefficiente è esattamente
2^(2ΔA−ΔB)3^(Δℓ−2Δk): questa è una formulazione concreta per tentare
una compensazione su blocchi, con tempi e ipotesi dichiarati prima.

Il risultato di questa fase è la separazione precisa tra un'implicazione
verificabile e l'ipotesi dinamica ancora da dimostrare. Non è stata provata
la discesa della famiglia infinita, né la congettura di Collatz.

## Riproduzione

```sh
python3 notes/post_v6_induction_2026-09-25/test_induction.py
python3 notes/post_v6_induction_2026-09-25/induction_probe.py --output /tmp/induction_results.json
cmp notes/post_v6_induction_2026-09-25/induction_results.json /tmp/induction_results.json
```

Gli otto test includono un replay aritmetico alternativo per livelli piccoli,
confronti con frazioni esatte, rifiuto di baseline alterate, i coefficienti
del controesempio ricavati dalla trasformazione generale e il caso
9→7→11 che distingue visita precedente ed endpoint finale.

La CI ripete tutte le 13 coppie e confronta l'intero JSON byte per byte.
Il controllo sperimentale non è una verifica formale del programma Python.
L'audit Lean verifica separatamente le dipendenze dei lemmi formalizzati.
Le identità e la specializzazione a Q_v riportate sopra non vanno confuse
con una formalizzazione completa della precedente procedura modulare T.
