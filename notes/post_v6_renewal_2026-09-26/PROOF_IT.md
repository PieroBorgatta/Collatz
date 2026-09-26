# Precisione necessaria per un certificato basato sui prefissi

**26 settembre 2026.** Si determina esattamente il massimo difetto fra
livelli compatibile con un prefisso binario dell'input, conservando la
relazione quadratica fra i due livelli. Il risultato dà un criterio di
arresto ottimale per questa classe di certificati. Non è un limite alla
possibilità di usare altre proprietà aritmetiche della sorgente esatta,
non è una prova di discesa e non comporta una rivendicazione di priorità.

## 1. Dati e classe di informazione

Si usa la mappa shortcut `T(x)=x/2` per `x` pari e `T(x)=(3x+1)/2`
per `x` dispari. Indichiamo con `w_k(x)` la parola delle prime `k`
parità, indicizzata da zero, e con `J_x(k)` il suo numero di uno.

Fissiamo `v≥0` e la mappa

\[
             f_v(x)=x+2^{v+2}x^2.
\]

Per la torre del progetto,

\[
 Q_v=\frac{9^{2^v}-1}{2^{v+3}},\qquad Q_{v+1}=f_v(Q_v).
\]

La dimostrazione seguente vale più generalmente per un intero
positivo `Q`, orizzonti `1≤H≤K` e precisione `H≤M≤K`.
Poniamo

\[
 j_L=J_Q(H),\qquad j_U(M)=J_{f_v(Q)}(M),\qquad
 \Delta_Q=J_{f_v(Q)}(K)-2j_L.
\]

La classe di input compatibili con la precisione esposta è

\[
                    \mathcal C_M=\{x>0:x\equiv Q\pmod{2^M}\}.
                                                               \tag{1}
\]

Per ogni suo elemento il secondo input è **esattamente `f_v(x)`**.
Non si rende indipendente la sorgente superiore. Il prefisso
inferiore di lunghezza `H` è già fissato, poiché `M≥H`.

Il certificato studiato deve garantire
`J_(f_v(x))(K)−2J_x(H)≤g` per tutti gli `x` compatibili con (1).
L'espressione simbolica pura di `Q_v`, o ulteriori vincoli che
selezionino un sottoinsieme di (1), non vengono assunti nel modello
di informazione. Questa distinzione è essenziale per i quantificatori.

## 2. Due biezioni che conservano esattamente la precisione

Per due interi distinti `x,y`,

\[
 f_v(x)-f_v(y)
 =(x-y)\bigl(1+2^{v+2}(x+y)\bigr).
\]

Il secondo fattore è dispari; quindi

\[
                  \nu_2(f_v(x)-f_v(y))=\nu_2(x-y).              \tag{2}
\]

La mappa `f_v` induce pertanto una biezione modulo ogni `2^k`,
che manda un cilindro di precisione `M` su un cilindro della
stessa precisione. L'inversa conserva le stesse congruenze.

Anche la mappa `x mod2^k → w_k(x)` è una biezione. Una prova
elementare procede per sollevamenti: i due rappresentanti `a` e
`a+2^k` hanno le stesse prime `k` parità; dopo `k` passi i loro
valori differiscono di `3^(J_a(k))`, quindi le parità successive
sono opposte. Ogni parola di lunghezza `k` ammette precisamente
le due estensioni possibili. La base `k=0` è immediata.

Queste sono le codifiche congruenziali classiche utilizzate nel
progetto; non si attribuisce novità alle due biezioni.

## 3. Completamenti del blocco superiore e massimo esatto

Sia `β=w_M(f_v(Q))` il prefisso superiore osservato. Applicando
le due biezioni, ogni parola `σ∈{0,1}^(K−M)` è realizzata da
**esattamente una** classe

\[
 x\pmod{2^K},\qquad x\equiv Q\pmod{2^M},
 \qquad w_K(f_v(x))=\beta\sigma.                              \tag{3}
\]

Infatti `βσ` determina una classe superiore modulo `2^K`; il suo
prefisso `β` la colloca nella classe di `f_v(Q)` modulo `2^M`.
L'inversa di `f_v` la riporta in un'unica classe di `Q` modulo
`2^M`. Ogni classe ha rappresentanti positivi.

Poiché `J_x(H)=j_L` per tutti questi completamenti, i difetti
raggiungibili sono precisamente tutti gli interi dell'intervallo

\[
 \boxed{\displaystyle
 j_U(M)-2j_L
 \ \le\ J_{f_v(x)}(K)-2J_x(H)\ \le\
 j_U(M)+(K-M)-2j_L.}                                          \tag{4}
\]

Posti `L=K−M` e `d_0=j_U(M)−2j_L`, il numero di classi modulo
`2^K` che realizzano il valore `d_0+s` è esattamente

\[
                         \binom{L}{s},\qquad0\le s\le L.       \tag{5}
\]

Non si tratta di una distribuzione probabilistica postulata per
`Q_v`: è un conteggio deterministico dei completamenti della classe
di informazione. Il numero di completamenti che violano un limite
intero `g` è, con gli estremi troncati a `[0,L]`,

\[
                         \sum_{s>g-d_0}\binom{L}{s}.            \tag{6}
\]

Indichiamo con `Z_U(M)=M−j_U(M)` gli zeri osservati nel prefisso
superiore e con `Z_U[M,K)` gli zeri del suffisso superiore effettivo
nelle posizioni `M,…,K−1`. Il massimo in (4) si può scrivere in
due forme equivalenti:

\[
 \boxed{\displaystyle
 \Delta_{\max}(M)
 =K-2j_L-Z_U(M)
 =\Delta_Q+Z_U[M,K).}                                        \tag{7}
\]

La seconda forma misura quanto il massimo compatibile supera il
difetto effettivo. La prima è quella operativa: non richiede di
conoscere la parte futura della traiettoria né `Δ_Q`.

## 4. Regola di arresto basata sugli zeri osservati

Fissiamo un limite intero desiderato `g` e definiamo

\[
                         R=K-2j_L-g.                          \tag{8}
\]

Dalla prima forma di (7), la precisione `M` certifica il limite
per tutti gli input compatibili **se e soltanto se**

\[
                              Z_U(M)\ge R.                     \tag{9}
\]

La regola operativa è quindi: si parte da `M=H` e si estende il
prefisso superiore fino ad aver osservato almeno `R` zeri.
Se `R≤0`, il requisito è già soddisfatto. Più generalmente,
se gli zeri sono già sufficienti a `M=H`, ci si arresta lì.

La precisione minima è esattamente

\[
                  M_* =\min\{M\in[H,K]:Z_U(M)\ge R\}.          \tag{10}
\]

Quando `R>0` e il requisito è realizzabile, sia `ζ_R` la posizione
del `R`-esimo zero della parola superiore, contata da uno.
Allora `M_*=max(H,ζ_R)`. Se non esistono abbastanza zeri,
nessuna precisione in `[H,K]` certifica il limite. Questo avviene
esattamente quando

\[
             Z_U(K)<R
             \quad\Longleftrightarrow\quad\Delta_Q>g.         \tag{11}
\]

**Ottimalità nel modello dei prefissi.** Prima della soglia (10),
il completamento superiore con tutti uno realizza un difetto
strettamente maggiore di `g`. Per (3), quel completamento rispetta
il prefisso inferiore, il prefisso superiore e la relazione
quadratica esatta. Nessun certificato valido per l'intera classe
di informazione può dunque fermarsi prima. Alla soglia, (7)
garantisce il limite per tutti i completamenti.

L'algoritmo di arresto usa soltanto `H,K,j_L,g` e gli zeri del
prefisso già esposto; non usa `Δ_Q` per decidere. L'uguaglianza
con la seconda forma di (7) è una verifica a posteriori utile,
non una dipendenza circolare della regola.

## 5. Testimoni esatti con i bit alti conservati

La costruzione dei completamenti è esplicita. Per una parola
completa `ω=βσ` di lunghezza `K`, peso `j` e costante affine

\[
 C_\omega=\sum_{\substack{0\le i<K\\\omega_i=1}}
                      2^i3^{\#\{\ell>i:\omega_\ell=1\}},
\]

la classe superiore è

\[
                       y_\omega\equiv-3^{-j}C_\omega
                                      \pmod{2^K}.              \tag{12}
\]

È l'inversa della biezione delle parole di parità. Si risolve poi

\[
                         f_v(a_\omega)\equiv y_\omega
                                      \pmod{2^K},
 \qquad0\le a_\omega<2^K.                                    \tag{13}
\]

La soluzione è unica e può essere costruita un bit alla volta:
fra `a` e `a+2^k`, le immagini mediante `f_v` differiscono di
`2^k` modulo `2^(k+1)`, per (2).

Se `Q≥2^K`, poniamo

\[
 A=2^K\left\lfloor Q/2^K\right\rfloor,
 \qquad x_\omega=A+a_\omega.                                \tag{14}
\]

Allora `x_ω` è positivo, conserva **tutti i bit di `Q` nelle
posizioni `K,K+1,…`**, conserva quelli nelle posizioni `0,…,M−1`
e realizza esattamente la parola superiore `ω`. Essendo nel
medesimo blocco binario di lunghezza `2^K` con parte alta positiva,
è anche nella stessa binade di `Q`. Ogni completamento ha un unico
rappresentante in quel blocco.

Per il progetto, con `v≥5`, `H=H_v`, `K=H_(v+1)` e
`H_w=ceil(589·2^w/612)`, la condizione `Q_v≥2^K` è automatica.
Infatti, posti `N=2^v` e `r=v+3`, valgono `K≤2N`, `N≥r+1` e

\[
 Q_v=\frac{9^N-1}{2^r}
       \ge2^{3N-r}\ge2^{2N+1}>2^K,
\]

poiché `9^N−1≥8^N`.

Non si afferma che i bit alti di `f_v(x_ω)` siano anch'essi uguali
a quelli di `f_v(Q)`, né che `x_ω` conservi la purezza ternaria
della sorgente originale. Il testimone conserva i vincoli esposti
in questa nota e l'uguaglianza quadratica.

## 6. Blocchi locali ai tempi `t` e `2t`

Il conteggio della precisione vale anche al confine fra blocchi,
ma qui la sorgente superiore è `U(x)=2f_v(x)`. Fissiamo `t≥1`
e due storie compatibili: la parola inferiore di lunghezza `t`
e quella superiore di lunghezza `2t`.

La prima impone una classe di `x` modulo `2^t`. La seconda inizia
con uno zero, seguito da `2t−1` parità di `f_v(x)`; per le due
biezioni del paragrafo 2 impone una classe di `x` modulo
`2^(2t−1)`. Poiché `2t−1≥t`, quest'ultima è l'intera informazione
congiunta dei due prefissi, quando sono compatibili.

Per determinare esattamente i prossimi `b≥1` passi inferiori e
`2b` superiori serve, nello stesso modello di precisione,

\[
                    x\pmod{2^{2t+2b-1}}.                      \tag{15}
\]

Ci sono esattamente `2^(2b)` completamenti della classe precedente.
Ognuna delle `2^(2b)` parole superiori del nuovo blocco è realizzata
una sola volta; essa determina anche il blocco inferiore. La
precisione richiesta passa quindi da `2t−1` a `2t+2b−1`: sono
**`2b` nuovi bit**, non un loro numero ridotto dalla relazione
quadratica.

Se `b≤t−1`, il nuovo blocco inferiore è già interamente fissato
dal passato superiore, perché `t+b≤2t−1`. Tutte le parole del
nuovo blocco superiore restano comunque libere. Se `b>t−1`,
prescrivere in aggiunta un blocco inferiore compatibile fissa
`b−t+1` ulteriori bit della sorgente: determina i primi
`b−t+1` bit del nuovo blocco superiore e lascia liberi gli altri
`b+t−1`.

Per un limite sul premio aggregato locale occorre precisare
quale blocco inferiore è già noto. Poniamo

\[
 S=2t-1,\qquad E=2t+2b-1,
 \qquad \max(t+b,S)\le B\le E,                              \tag{16}
\]

dove `B` è il numero di bit iniziali della sorgente fissati.
In quella classe, definiamo i conteggi noti

\[
 d_L=J_x(t+b)-J_x(t),\qquad
 a_B=J_{f_v(x)}(B)-J_{f_v(x)}(S).
\]

Il premio del nuovo blocco è

\[
 D_b(x)=J_{2f_v(x)}(2t+2b)-J_{2f_v(x)}(2t)
                    -2\bigl(J_x(t+b)-J_x(t)\bigr).
\]

I primi `B−S` bit superiori del blocco sono fissati; i rimanenti
`E−B` sono arbitrari. Pertanto l'intervallo esatto è

\[
 \boxed{a_B-2d_L\le D_b(x)\le a_B-2d_L+(E-B).}                \tag{17}
\]

Tutti i valori intermedi sono realizzati, con molteplicità
binomiali sui `E−B` bit liberi. Il requisito `B≥t+b` in (16)
è essenziale: senza di esso non si può trattare `d_L` come una
costante indipendente dal completamento superiore.

Per `b≤t−1` si può scegliere `B=S`, ottenendo
`−2d_L≤D_b≤2b−2d_L`. Per `b>t−1`, la scelta minima è `B=t+b`
e lascia `t+b−1` bit superiori liberi, come sopra.

Il caso iniziale `t=0` va separato: il primo bit di `U=2f_v(x)`
è già zero, quindi i blocchi iniziali di lunghezze `b,2b` richiedono
`2b−1` bit della sorgente. Dopo che quel bit deterministico è
stato consumato, vale il conteggio `2b` del caso `t≥1`.

Questi sono limiti di precisione per la classe di informazione
indicata, non limiti universali al tempo di calcolo di ogni
possibile algoritmo o prova aritmetica.

### 6b. Un ciclo nei soli residui, realizzato da sorgenti positive

Un limite più concreto riguarda l'astrazione che conserva soltanto
la coppia degli stati evoluti modulo `2^k`. Qui si deve distinguere
la lunghezza `h` del prefisso iniziale prescritto dall'orizzonte
`H_v` del certificato.

Fissiamo `k≥1`, una durata `L≥1`, un prefisso inferiore di lunghezza
`h≥0` effettivamente realizzabile, e poniamo

\[
 t=\max(h,L+k+1),\qquad a=t+L+k\le2t-1,
 \qquad K=2t+2L+k-1.                                      \tag{18}
\]

**Costruzione.** Si prolunghi il prefisso inferiore prescritto con
zeri fino alla lunghezza `a`, e sia `x_0 mod2^a` la corrispondente
classe, scegliendone il rappresentante nonnegativo minimo.
Si prenda come prefisso superiore la parola di `f_v(x_0)` di
lunghezza `2t−1`, seguita da `2L+k` uno. Questa parola ha
lunghezza `K`. Le inverse del paragrafo 5 producono un intero
positivo `X` che la realizza attraverso `f_v(X)`.

Poiché il prefisso superiore fino a `2t−1` è quello di `f_v(x_0)`,
l'isometria forza `X≡x_0 mod2^(2t−1)` e quindi conserva l'intera
parola inferiore prescritta fino ad `a`. Per `2f_v(X)` occorre
aggiungere soltanto il primo zero deterministico: gli uno forzati
occupano le posizioni `2t,…,2t+2L+k−1`.

Per ogni `0≤i≤L`, la traiettoria inferiore ha almeno `k` zeri
successivi a partire dal tempo `t+i`; quella superiore ha almeno
`k` uno successivi a partire dal tempo `2t+2i`. I cilindri delle
parole `0^k` e `1^k` sono rispettivamente `0` e `−1` modulo
`2^k`. Ne segue

\[
 \boxed{\left(T^{t+i}(X),\ T^{2t+2i}(2f_v(X))\right)
                    \equiv(0,-1)\pmod{2^k},\quad0\le i\le L.} \tag{19}
\]

Ogni passaggio da `i` a `i+1` contiene un passo inferiore pari e
due passi superiori dispari. Il premio «dispari superiori meno
due volte i dispari inferiori» è quindi esattamente `2` a ogni
passaggio.

È una singola sorgente positiva che realizza `L` ripetizioni del
ciclo nell'astrazione dei residui. La sorgente può cambiare con
`L`: non si dimostra una singola orbita positiva infinita con
questo comportamento, né un ciclo numerico della mappa Collatz.

Se il prefisso prescritto è quello di `Q_v` e `Q_v≥2^K`, si può
scegliere `X` come in (14), conservandone anche la binade e tutti
i bit nelle posizioni almeno `K`. Per ottenere esempi entro il
clock del certificato si può usare il **prefisso breve** `h=v+3`
e controllare separatamente `t+L≤H_v`. Tre costruzioni finite,
verificate anche mediante iterazione intera indipendente, sono:

| `v` | `h` | `k` | `L` | `t` | `t+L` | `H_v` | `K` |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 5 | 8 | 3 | 8 | 12 | 20 | 31 | 42 |
| 8 | 11 | 4 | 16 | 21 | 37 | 247 | 77 |
| 12 | 15 | 8 | 64 | 73 | 137 | 3943 | 281 |

La costruzione conserva soltanto le prime `h` parità effettive
inferiori, non garantisce la conservazione dell'intera parola
di lunghezza `H_v`. Se si scegliesse invece `h=H_v`, il medesimo
lemma sarebbe valido, ma darebbe `t≥H_v`: quel ciclo sarebbe
fuori dall'orizzonte inferiore del certificato.

Per un potenziale `Φ` che dipenda soltanto dalla coppia di residui,
una disuguaglianza universale su questi passaggi della forma

\[
       \text{premio}_i\le c+\Phi(s_i)-\Phi(s_{i+1})
\]

richiede necessariamente `c≥2`, perché `s_i=s_(i+1)=(0,−1)` e
il premio vale `2`. Il risultato riguarda potenziali validi per
questa classe di sorgenti, che include gli esempi costruiti.
Non esclude un potenziale che conservi il clock, altre informazioni
sulla storia, antenati interi o vincoli della sorgente esatta.

## 7. Portata del risultato e vincoli sugli antenati

La relazione fra livelli non elimina i completamenti del blocco
superiore: è un'isometria che li trasporta in modo biunivoco. Per
certificare un difetto aggregato non è sempre necessario conoscere
tutte le parità; è necessario e sufficiente aver esposto gli zeri
richiesti da (8). Quanti bit restino ignoti è determinato dalla loro
posizione effettiva, non da un'ipotesi probabilistica sulla densità.

Qui l'input superiore è `Q_(v+1)=f_v(Q_v)`. Se si usa invece
`WW=2Q_(v+1)`, la sua parola di parità contiene un primo zero
deterministico, seguito dalla parola di `Q_(v+1)`: occorre togliere
quel passo prima di confrontare le precisioni.

L'ottimalità dimostrata riguarda certificati basati sulla classe
di prefissi (1), anche se si aggiungono i bit alti conservati in
(14). Non riguarda prove che sfruttino la forma esatta
`2^(v+3)Q_v+1=3^(2^(v+1))`, condizioni ulteriori sugli antenati,
o altre proprietà che escludano i testimoni costruiti. Né implica
che un algoritmo debba materializzare tutti i bit che un argomento
aritmetico potrebbe controllare simbolicamente.

In particolare, il [lemma dei due antenati](../post_v6_ancestry_2026-09-25/RESULTS_IT.md)
dimostra che, per `v≥5`, la binade di `Q_v`, la sua intera parola
inferiore di lunghezza `H_v` e l'esistenza di due antenati interi
positivi attraverso `f_(v−2)` e `f_(v−1)` forzano già `x=Q_v`.
Aggiungendo tutti questi vincoli, i completamenti alternativi
costruiti qui vengono esclusi e il limite di precisione del
modello (1) non può essere applicato a quella classe più stretta.

Il [probe finito](renewal_results.json) costruisce otto testimoni,
ai livelli `v=5,…,12`, immediatamente prima della soglia di
arresto. Tutti conservano la binade e la parola inferiore, ma
nessuno ammette neppure un antenato intero positivo tramite
`f_(v−1)`. Questa è una verifica dei singoli testimoni, distinta
dal teorema generale sui due antenati. Non sono controesempi
alla sorgente effettiva della torre.

La nota identifica quindi un limite preciso dei certificati per
completamenti e una regola di arresto utilizzabile; non fornisce
una nuova maggiorazione uniforme di `Δ_v`.
