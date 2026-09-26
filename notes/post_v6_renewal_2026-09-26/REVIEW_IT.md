# Revisione matematica e verifica indipendente delle soglie

**26 settembre 2026.** Sono stati revisionati `renewal_probe.py`,
`PROOF_IT.md` e il rapporto dei risultati. Non sono stati individuati
errori materiali nelle formule aggregate, nel raccordo temporale locale
o nella costruzione dei testimoni. Questa è una revisione interna con
prove e controlli finiti; non è una revisione esterna, una formalizzazione
Lean o una verifica di originalità in letteratura.

## 1. Quantificatori del risultato

Il dominio del massimo è l'intero cilindro positivo

\[
 x\equiv Q_v\pmod{2^M},\qquad y=f_v(x),
 \qquad H_v\le M\le H_{v+1}=K.
\]

La relazione quadratica è mantenuta esattamente. La sua isometria
binaria, insieme alla biezione delle parole di parità, rende libere
tutte le `K−M` parità superiori non ancora fissate. Perciò

\[
 \max_x\bigl(J_{f_v(x)}(K)-2J_x(H_v)\bigr)
       =K-2J_{Q_v}(H_v)-Z_U(M)
\]

è un massimo raggiunto, non una maggiorazione prudenziale. Anche i
conteggi binomiali dei diversi pesi seguono dalla stessa biezione.
Non costituiscono un modello casuale per la sorgente effettiva.

La precisione minima è una proprietà di questa classe di informazione.
Il risultato non afferma che ogni algoritmo o ogni prova su `Q_v` debba
materializzare altrettanti bit. Una procedura che usi la definizione
esatta della potenza di tre, gli antenati interi o altri vincoli
selettivi opera su una classe più stretta.

La frazione di precisione osservata al livello 23 è un dato finito.
La formula del massimo non dimostra uniformemente
`M_*=K−O(g(v))`: per dedurlo servirebbe informazione ulteriore sulla
posizione degli zeri. Questo limite di portata è esplicitato nel rapporto.

## 2. Controllo delle diciannove soglie

Tutte le soglie registrate per `v=5,…,23` sono state controllate
con una procedura distinta dalla ricerca binaria del probe. Posto
`R=K−2j_L−g` e letto il valore candidato `M_*` dal JSON, si è
calcolata soltanto la parola superiore fino a `M_*`. Sono state
verificate le due condizioni

\[
                  Z_U(M_*)=R,
       \qquad p_{M_*-1}=0.                              \tag{1}
\]

Tutte le diciannove soglie sono strettamente maggiori di `H_v`.
Poiché il conteggio degli zeri è non decrescente, (1) implica
`Z_U(M_*−1)=R−1`: il massimo alla soglia è `g` e quello un bit
prima è `g+1`. Nessun prefisso precedente può certificare il limite.

Per `v≤12` il controllo ha usato l'intero `Q_(v+1)` e l'iterazione
elementare, bit per bit, della mappa shortcut. Per `v=13,…,23` ha
riusato il motore delle tracce già verificato, ma con precisione
iniziale e orizzonte **esattamente `M_*`**, ricontando gli zeri dai
byte canonici. Il controllo delle soglie è quindi separato dalla
ricerca binaria; il secondo gruppo non è una nuova implementazione
indipendente del generatore delle tracce.

Il probe principale determina retrospettivamente le soglie su
tracce storiche complete. La regola matematica degli zeri osservati
può invece arrestarsi al prefisso corrente: questo non equivale a
dire che la produzione dei dati abbia evitato il replay completo.

## 3. Testimoni globali e filtro degli antenati

Gli otto testimoni archiviati per `v=5,…,12` sono stati controllati
nuovamente con aritmetica intera elementare, senza chiamare le
funzioni di costruzione del probe. Per ciascuno sono stati verificati:

- `X>0`, `X≠Q_v` e `Y=X+2^(v+2)X²`;
- coincidenza dei bit nelle posizioni `0,…,M−1`, con `M=M_*−1`,
  e di tutti i bit da `K` in su;
- stessa binade di `Q_v` e stessa intera parola inferiore di
  lunghezza `H_v`;
- soli uno nel suffisso superiore dalle posizioni `M` a `K−1`;
- difetto esattamente `g(v)+1`.

La verifica dei bit alti riguarda `X`, non `Y`; non viene dedotta
la stessa binade superiore senza un controllo ulteriore.

È stato inoltre verificato con radice quadrata intera che nessuno
degli otto `X` ammette un antenato intero positivo. Il test è esatto:
un antenato tramite `f_(v−1)` richiederebbe

\[
 D=1+2^{v+3}X=s^2,\qquad s\equiv1\pmod{2^{v+2}},
 \qquad (s-1)/2^{v+2}>0.                              \tag{2}
\]

Questo risultato finito non va esteso a ogni completamento del
cilindro. Il vincolo uniforme disponibile è invece il precedente
[lemma dei due antenati](../post_v6_ancestry_2026-09-25/RESULTS_IT.md):
per `v≥5`, due antenati interi positivi, la binade di `Q_v` e la
sua intera parola inferiore effettiva identificano già `Q_v`.
Imponendo tutte queste condizioni, il cilindro avversario si riduce
a quel solo punto e il massimo generico non è più applicabile.
L'identificazione del punto non determina una maggiorazione del
peso della sua parola superiore.

## 4. Raccordo locale a tempi diversi

La sorgente superiore del confronto locale è `U=2f_v(x)`, il cui
primo passo è pari. Per `t≥1`, le storie a tempi `(t,2t)` fissano
precisamente `x mod2^(2t−1)`, quando sono compatibili.
Il nuovo blocco superiore di `2b` parità richiede una sorgente
modulo `2^(2t+2b−1)`; questa precisione comprende anche quella
necessaria al nuovo blocco inferiore di `b` passi.

Il fabbisogno generico è dunque `2b` nuovi bit. Quando `b≤t−1`,
la parola inferiore del nuovo blocco è già fissata, mentre tutte
le nuove parole superiori restano possibili. Per una precisione
intermedia

\[
 \max(t+b,2t-1)\le B\le2t+2b-1,
\]

la formula di `block_reward_envelope` sottrae il peso inferiore
fissato e lascia precisamente `2t+2b−1−B` bit superiori liberi.
Il requisito `B≥t+b` impedisce di trattare erroneamente il peso
inferiore come indipendente dal completamento.

I tre testimoni locali sono stati rieseguiti con iterazione intera
elementare: conservano entrambe le storie e il blocco inferiore
successivo e raggiungono i premi massimi `2`, `2`, `8`.
Questi esempi non sono una traiettoria ciclica della torre.

## 5. Cammini positivi nella proiezione sui residui

La costruzione `positive_loop` è stata controllata nei tre casi
predefiniti con un replay intero elementare separato. I parametri
e i risultati sono:

| `v` | `k` | `L` | Prefisso conservato `h` | Tempo iniziale `t` | Precisione sorgente `K` | Premio totale |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 3 | 8 | 8 | 12 | 42 | 16 |
| 8 | 4 | 16 | 11 | 21 | 77 | 32 |
| 12 | 8 | 64 | 15 | 73 | 281 | 128 |

Per ciascun esempio sono stati confrontati tutti gli `L+1` stati
alle coppie di tempi `(t+i,2t+2i)`. I due residui modulo `2^k`
restano `(0,2^k−1)` e ognuno degli `L` passi congiunti ha uscita
inferiore zero, due uscite superiori uno e premio `+2`.

Sono verificati la relazione esatta `U=2X+2^(v+3)X²`, la binade,
i bit alti da `K` in su e il prefisso effettivo di lunghezza
`h=v+3`. Tutti i cammini terminano entro `H_v` nel tempo inferiore.
In questi tre esempi `X≠Q_v` e l'intera parola inferiore di
lunghezza `H_v` **non** è conservata. Non sono quindi gli stessi
testimoni globali del paragrafo 3.

La compatibilità delle precisioni deriva da
`t=max(h,L+k+1)` e `a=t+L+k≤2t−1`. Fissare il passato superiore
fino a `2t` conserva la prescrizione inferiore fino ad `a`;
imporre poi `2L+k` uscite superiori uno garantisce tutti i residui
richiesti. La condizione `Q_v≥2^K`, controllata dal costruttore,
è necessaria per la particolare conservazione dei bit alti e della
binade. Non si deducono cammini arbitrariamente lunghi nella stessa
binade a livello `v` fissato.

È stato osservato e verificato separatamente anche un piccolo
cammino **della sorgente effettiva**: per `v=5`, agli istanti
accoppiati `(18,36)` e `(19,38)`, i residui modulo due sono in
entrambi i casi `(0,1)`. Il passo inferiore è pari e i due passi
superiori sono dispari, per un premio `+2`. Questo controllo è
un'iterazione diretta di `Q_5` e `2Q_6`; non si identifica con il
testimone prodotto automaticamente assegnando quei parametri al
costruttore, che fissa anche altri bit intermedi della sorgente.

Un potenziale dei soli due residui ha differenza nulla su questi
archi proiettati. Una disuguaglianza locale deve quindi attribuire
un costo almeno due al passo positivo. Il caso effettivo mostra
che imporre la sorgente esatta non elimina ogni arco positivo
di questa proiezione molto grossolana. Restano possibili costi
compensati altrove, controllo del numero di visite e stati più
informativi. Nessuno di questi cammini prova che il difetto
complessivo superi `g(v)` o costituisce un ciclo numerico di Collatz.

## 6. Conseguenza della revisione

La ricerca di un potenziale sul cilindro con completamenti liberi
deve rispettare il massimo esatto: un cambiamento di contabilità
non può abbassarlo. Per proseguire occorre restringere l'insieme
dei completamenti usando proprietà dimostrate della sorgente e
ottenere una disuguaglianza sul loro peso. La sola rigidità, la
sola cancellazione telescopica e i risultati finiti non completano
questo passaggio. Rimane aperta la maggiorazione uniforme di
`Δ_v`; questa fase non aggiunge livelli oltre il 24 né teoremi Lean.
