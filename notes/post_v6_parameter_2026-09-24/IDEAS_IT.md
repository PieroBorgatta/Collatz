# Due direzioni ulteriori: masse dei predecessori e aritmetica delle torri

24 settembre 2026. Continuazione del commit `d5a50da`, successiva alla
[v6 pubblicata](https://doi.org/10.5281/zenodo.22936057) e alla
[prima continuazione formale](../post_v6_section_2026-09-24/RESULTS_IT.md).
Questa nota distingue deduzioni aritmetiche, controlli finiti e obiettivi
di ricerca. Non rivendica una dimostrazione di Collatz né una priorità
bibliografica assoluta per le identità proposte.

La prossima ricerca non deve necessariamente continuare a cercare un rango
sulla sezione. Propongo due oggetti più delimitati. Il primo offre un
possibile miglioramento di un passaggio combinatorio esterno; il secondo
descrive precisamente cosa accade dopo l'ostacolo già formalizzato.

## 1. Un limite alla massa dei ritorni, senza escludere i cicli

Sia `n_k=S^k(x)`, con x positivo dispari, e siano

\[
a_k=\nu_2(3n_k+1),\quad A_k=\sum_{i<k}a_i,\quad
\omega_k=\frac{3^k}{2^{A_k}},\quad p_k=\frac{\omega_k}{n_k}.
\]

Le ricorrenze esatte danno

\[
\boxed{\quad p_k-p_{k+1}
=\frac{\omega_k}{n_k(3n_k+1)}>0.\quad}
\]

Infatti `ω_(k+1)/n_(k+1)=3ω_k/(3n_k+1)`. Sottraendo da `ω_k/n_k`
si ottiene l'identità, senza approssimazioni e senza alcuna ipotesi sulla
convergenza. Per ogni N finito,

\[
\sum_{k=0}^N\frac{\omega_k}{n_k(3n_k+1)}
=\frac1x-\frac{\omega_{N+1}}{n_{N+1}}\le\frac1x.
\]

Se H è qualsiasi insieme finito di tempi distinti con `n_k=R`, R positivo,
la positività degli addendi permette di restringere la somma:

\[
\boxed{\quad \sum_{k\in H}\omega_k\le\frac{R(3R+1)}x.\quad}
\]

Quindi, per un insieme finito W di **parole esatte distinte** da x a R,

\[
\sum_{w\in W}\frac{3^{|w|}}{2^{\sum w}}
\le\frac{R(3R+1)}x.
\]

Il passaggio è lecito perché un'orbita deterministica determina l'unica
parola esatta di ogni lunghezza. La formula non vale per un multinsieme
con duplicazioni arbitrarie. Ammette la parola vuota, se x=R. Non occorre
conoscere un periodo, escludere cicli non banali, né individuare il primo
arrivo. Il fattore è ottimale almeno per R=x=1: le parole `[2]^j` hanno
pesi `(3/4)^j`, con somma limite 4.

### Perché questo risultato può servire

Nel [preprint di Mazur del 6 settembre 2026, §3–4 e Remark 4.3](https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/paper-v1.pdf),
i pesi sono esattamente questi. Il conteggio sceglie un endpoint senza
ritorni per rendere iniettive le sorgenti; la scelta contribuisce alla
non effettività delle costanti. L'input analitico dichiarato non richiede
questa ipotesi. Non abbiamo ricontrollato qui tutte le sue dipendenze
analitiche o ricompilato il progetto esterno.

**Deduzione nostra, condizionata a quell'input:** posto `K=R(3R+1)`, per
sorgenti `x_w≥X>0`, pesi selezionati `0≤v_w≤ω(w)` e `g≥0`, raggruppare
per sorgente dà

\[
\sum_w v_wg(x_w)\le\frac KX\sum_{x\in\{x_w\}}g(x).
\]

Si può dunque sostituire l'iniettività con una maggiorazione della
molteplicità pesata. Il costo è un fattore peggiore, ma esplicito.
L'algebra del successivo conteggio resta coerente sostituendo R con K:
`m²≥132KC_*`, `U≥3/(8·3^m)`, coefficiente finale `3/(256K·3^m)`.
La soglia analitica `H(R,m)` rimane da auditare: **non** segue ancora un
algoritmo effettivo completo per le costanti di ogni target.

Questo è il candidato che metterei al primo posto: un lemma indipendente
con una possibile applicazione precisa. Il test dell'applicazione è la
compatibilità completa dei pesi e delle ipotesi con la costruzione inversa.
Il test non è una nuova verifica numerica di Collatz. Il risultato autonomo
resta valido anche se l'applicazione esterna non supera l'audit.

Il metodo del telescopaggio è elementare; l'eventuale novità riguarda
l'applicazione e la sua formalizzazione, da confrontare ulteriormente con
la letteratura. La quantità `ω_k/n_k` dipende dalla storia: la sua discesa
non implica la discesa di `n_k`. Un peso totale finito è compatibile con
infiniti ritorni, come mostra già il punto fisso 1.

## 2. Dopo la prima torre: il parametro diventa dinamico

La continuazione precedente segueva `n_k=(2^(k+1)−11)/3` fino all'uscita
dalle ripetizioni `[1,2]^r`, con `k=3r+h`, `h∈{1,2,3}`. Ora studiamo
il tratto **successivo**. Le formule seguenti hanno una derivazione
universale su carta; non sono ancora formalizzate in Lean.

Per un dispari positivo q e `v≥1`, poniamo

\[
Q_v(q)=\frac{9^{2^vq}-1}{2^{v+3}}.
\]

L'identità elementare `ν₂(9^m−1)=3+ν₂(m)` mostra che Q è un intero
dispari. Si prova fattorizzando per m dispari e osservando che ogni
raddoppio dell'esponente aggiunge esattamente un fattore 2.

Per un qualsiasi dispari positivo y, con `d=ν₂(y+1)`, seguono esattamente
`d−1` passi Syracuse di esponente 1. Durante questi passi
`S^j(y)+1=3^j(y+1)/2^j`; il valore di `ν₂(S^j(y)+1)` cala di uno a
ogni passo. All'estremo è 1, quindi il prossimo esponente è almeno 2.

Applicando questa osservazione alle due fasi:

| Fase | Parametro | Uscita già nota y | Nuovi esponenti 1 | Estremo z |
|---|---|---|---|---|
| B, h=2 | `r=2^v q` | `9^(r+1)−10` | `v+2` | `2·3^(v+4)Q_v(q)−1` |
| C, h=3 | `r+1=2^v q` | `(9^(r+1)−5)/4` | `v` | `2·3^vQ_v(q)−1` |

Le parità imposte da k pari garantiscono `v≥1`. Le due forme soddisfano
`z_B+1=81(z_C+1)` quando sono parametrizzate dagli stessi v,q.
I rispettivi esponenti successivi sono

\[
a_B=1+\nu_2(3^{v+5}Q_v(q)-1),\qquad
a_C=1+\nu_2(3^{v+1}Q_v(q)-1).
\]

Non c'è pertanto una compensazione immediata garantita: dopo la prima
torre può esserci una seconda raffica, di lunghezza controllata dai bit
del suo indice r.

### Un caso infinito completamente esplicito

Da `Q_v(q)≡5q mod8` segue, per q=1 in entrambe le fasi,

\[
a_v=2\ \text{se v è pari},\qquad a_v=3\ \text{se v è dispari}.
\]

Per verificare la congruenza, si parte da
`Q_1(q)=(81^q−1)/16≡5q mod8` mediante il binomio, e si usa
`Q_(v+1)(q)=Q_v(q)(9^(2^v q)+1)/2`; l'ultimo fattore è 1 modulo 8.
Per `k=3·2^v` il nuovo suffisso è `[1]^v[a_v]`; per `k=3·2^v+2` è
`[1]^(v+2)[a_v]`. Il segmento non scende neppure sotto y, rispettivamente
per `v≥2` e `v≥1`.

Infatti, posto L uguale alla lunghezza della raffica, il rapporto
omogeneo dell'intero suffisso è `M=3^(L+1)/2^(L+a_v)>1` nei domini
indicati. Se w è il suo estremo,
`w+1=M(y+1)+1−2^(1−a_v)`, dunque w>y; tutti i passi intermedi crescono.
È un'estensione della famiglia di ostacoli, non una prova di divergenza.

### Classificare le risonanze, senza costruire gli interi enormi

Per q≠q', LTE dà

\[
\nu_2(Q_v(q)-Q_v(q'))=\nu_2(q-q').
\]

Quindi Q induce una permutazione dei residui dispari modulo `2^b`.
Per ciascun v fissato, entrambe le equazioni che definiscono
`a_B,a_C` hanno un'unica classe radice a ogni precisione, compatibile
con le precedenti. Si può costruirla bit per bit. Fra i q dispari,

\[
\operatorname{dens}(a=j)=2^{1-j}\quad(j≥2),\qquad
\operatorname{dens}(a≥j)=2^{2-j}.
\]

L'aspettativa rispetto a questa legge sui residui (misura di Haar
2-adica) è 3, uniformemente in v. Le singole densità sul **parametro**,
per ciascun v fissato, seguono dai conteggi esatti periodici. Non
abbiamo invece dimostrato la convergenza della media aritmetica di
`a(q)` per q≤N, che richiede un controllo aggiuntivo delle code.
Queste leggi non sono indipendenza fra passi successivi di un'orbita.

Anche la fase A ha una descrizione esatta. Con `k=6t+4`,

\[
y_t=(27·81^t-7)/4,\qquad
a_t=\nu_2(81^{t+1}-17)-2.
\]

Per ogni j≥0 esiste un'unica classe `b_j mod2^j`, soluzione di
`81^b_j≡17 mod2^(j+4)`, tale che
`a_t≥j+2` se e solo se `t+1≡b_j mod2^j`.
L'esistenza e l'unicità seguono da `ν₂(81^m−1)=4+ν₂(m)`.
L'enunciato non richiede introdurre logaritmi 2-adici in Lean.

Questi strumenti hanno precedenti: per esempio le
[note di macindoe, §14.2](https://github.com/macindoe/collatz/blob/main/reverse.md)
usano già isometrie e leggi di valutazione tramite radici p-adiche.
Non rivendichiamo come nuovi né LTE né il principio delle radici sollevate.
Qui l'oggetto specifico sono le tre uscite della famiglia v6.

Il prossimo esperimento utile deve trasportare queste rappresentazioni
attraverso **più** uscite, conservando le condizioni esatte sul parametro
e il confronto con la sorgente originaria. Un solo ramo risonante ancora
aperto per ogni valutazione non significa un solo ramo non convergente:
anche tutti i rami classificati richiedono analisi successiva.
Se ogni composizione introduce nuovi parametri senza vincoli controllabili,
questa descrizione locale non basta per una strategia globale.

## 3. Verifiche riproducibili e scelta del prossimo obiettivo

`parameter_probe.py` controlla con interi esatti 2048 raffiche B/C,
1024 passi della fase A, 24 casi delle due sott famiglie q=1, e le
permutazioni dei residui a 12 bit per
`v∈{1,2,3,4,7,16,64,128}`. Verifica 16 distribuzioni e costruisce le
relative radici a 96 bit. Le potenze con esponente enorme vengono
calcolate modulo una potenza di 2, senza materializzare `9^(2^v q)`.

`weighted_visits_probe.py` controlla 81.000 identità razionali su 1000
sorgenti dispari e 25.688 coppie sorgente/target; include il caso limite
R=x=1. Questi test sono controlli delle formule, non prove universali.

Il modulo `lean/CollatzShadowing/WeightedVisits.lean` formalizza invece
la prima direzione **sulla mappa Syracuse concreta**: somma degli esponenti,
peso razionale, identità di perdita, telescopaggio e maggiorazione per
qualsiasi insieme finito di tempi d'arrivo. Richiede soltanto x>0, senza
ipotesi aggiuntiva di disparità. La traduzione in insiemi di parole
distinte, il raggruppamento per sorgente e l'applicazione esterna restano
deduzioni su carta. Le formule della seconda torre non sono in Lean.

**Verifica formale completata:** build aggregata riuscita, 3366 job;
cinque dichiarazioni principali controllate con `#print axioms`, tutte
con soli `propext`, `Classical.choice`, `Quot.sound`. Il nuovo modulo
non contiene `sorry`, `admit`, assiomi dichiarati o `native_decide`.
I log sono [lean_build.txt](lean_build.txt) e [axioms.txt](axioms.txt);
[verification_manifest.json](verification_manifest.json) registra i file
e i controlli. È stato usato il pin esistente Lean/Mathlib 4.29.1,
senza una migrazione della toolchain. La CI del commit base `d5a50da`
è [passata](https://github.com/PieroBorgatta/Collatz/actions/runs/35988486673);
questo esito precede e non copre le aggiunte presenti in questa nota.

```sh
python3 notes/post_v6_parameter_2026-09-24/parameter_probe.py
python3 notes/post_v6_parameter_2026-09-24/weighted_visits_probe.py
cd lean
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_parameter_2026-09-24/axioms.lean
```

Il lemma sui tempi di visita è ora formalizzato. Sceglierei come
prossima consegna il suo collegamento formale alle parole esatte e
l'audit della possibile applicazione ai predecessori. In parallelo,
la seconda torre offre un
teorema specifico da formalizzare e un banco di prova severo per i
certificati parametrici. Nessuna delle due piste giustifica ancora una
nuova versione che annunci la soluzione della congettura.
