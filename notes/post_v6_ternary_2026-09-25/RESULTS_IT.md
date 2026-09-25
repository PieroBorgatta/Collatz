# Parità e riporti ternari: una stima locale, senza propagazione ancora

**25 settembre 2026.** Il risultato teorico positivo di questa fase è una
stima uniforme per il **primo** difetto di riporto fra due blocchi ternari:
il suo valore assoluto è `O(sqrt(m)·log²m)`. La prova usa Fourier e somme
di Gauss classiche ed è riportata separatamente. Non controlla il difetto
Collatz completo `E(m,L)`, né dimostra il limite richiesto su `Δ_v`.
Il simulatore ternario fornisce un controllo aritmetico indipendente delle
orbite finite già considerate. Non aggiunge teoremi Lean e non viene
avanzata una rivendicazione di originalità.

## 1. La quantità da controllare e il tempo esatto

Usiamo la mappa abbreviata `T(n)=n/2` se `n` è pari e
`T(n)=(3n+1)/2` se `n` è dispari. Per `h≥0`,

\[
 J_x(h)=\sum_{i=0}^{h-1}(T^i(x)\bmod2).
\]

Il bit di indice `i` descrive lo stato **prima** del passo `i`.
Una scansione completa del simulatore vale un passo di `T`; la lettura
di una singola cifra non è un passo Collatz.

Per `v≥5` poniamo

\[
 m=2^{v+1},\qquad r=v+3,\qquad
 R_m=3^m-1=2^rQ_v,\qquad
 H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,
 \qquad L=H_v+r.
\]

`R_m` è la parola ternaria di `m` cifre tutte uguali a `2`.
LTE dà esattamente `ν₂(R_m)=r` e `ν₂(R_(2m))=r+1`.
Pertanto i primi `r` passi inferiori e i primi `r+1` passi superiori
sono pari, e

\[
 J_{R_m}(L)=J_{Q_v}(H_v)=j_v.
\]

Definiamo

\[
 E(m,L)=J_{R_{2m}}(2L)-2J_{R_m}(L),\qquad
 \Delta_v=j_{v+1}-2j_v.
\]

Per gli arrotondamenti vale
`σ_v=2H_v−H_(v+1)∈{0,1}`. Dopo le `r+1` divisioni iniziali,
il tempo superiore disponibile è

\[
 2L-(r+1)=H_{v+1}+\ell_v,
 \qquad \ell_v=r-1+\sigma_v\in\{r-1,r\}.
\]

Segue l'identità, con una coda **effettiva** dell'orbita superiore,

\[
 E(m,L)=\Delta_v+
 J_{T^{H_{v+1}}(Q_{v+1})}(\ell_v),
 \qquad 0\le E(m,L)-\Delta_v\le v+3.                \tag{1}
\]

Quindi un limite superiore per `E` darebbe un limite superiore per `Δ_v`.
Il passaggio conserva però l'informazione della coda; non è corretto
identificare esattamente `E` con `Δ_v`.

## 2. Il simulatore e il rapporto con Stérin–Woods

Il motore [C](ternary_engine.c) memorizza cifre ternarie ordinarie, dalla
più significativa alla meno significativa. Parte da un array di `2`,
senza costruire l'intero `3^m−1` e senza GMP. La parità di un intero è
la parità della somma delle sue cifre ternarie, equivalentemente del
numero delle cifre `1`.

Per un passo dispari si aggiunge una cifra `1` in fondo: questo realizza
esattamente `3n+1`. Si divide quindi per due, leggendo da sinistra:

\[
 3c_i+d_i=2q_i+c_{i+1},\qquad c_0=0,
 \qquad q_i\in\{0,1,2\},\ c_{i+1}\in\{0,1\}.        \tag{2}
\]

Il numeratore da dividere è sempre pari, dunque il riporto finale è zero.
Si rimuovono gli eventuali zeri iniziali dal quoziente. Il motore esporta
le parità in bit compattati, con indice crescente dal bit meno significativo
di ciascun byte; i bit inutilizzati dell'ultimo byte restano zero.

Stérin e Woods studiano un automa bidimensionale con regole locali,
bootstrap nonlocale e alfabeto ternario ridondante `3′`. La sua dualità
fra trasduttori e il teorema di conversione di base richiedono quella
struttura. Il presente motore è un simulatore aritmetico su cifre ordinarie,
**non un'implementazione completa del CQCA**. Il loro trasduttore `/2`
interpreta già un riporto iniziale `1` come l'aggiunta di `3^k` al blocco
letto: è il precedente pertinente al confronto delle giunzioni.
[Fonte primaria: Stérin–Woods, arXiv:2007.06979v4, §2.3 e Appendice B.2,
Remark 56](https://arxiv.org/html/2007.06979v4).

I risultati di complessità di quel lavoro non dimostrano né escludono
una stima uniforme per `E` sulla nostra famiglia specifica.

## 3. Quali bilanci sono soltanto identità

Indichiamo con `s₃(n)` la somma delle cifre ternarie e con `p=n mod2`
la parità prima del passo. Il motore conta come `C(n)` il numero dei
riporti **in uscita** uguali a `1`, includendo tutte le cifre del
numeratore; per il passo dispari è inclusa anche la cifra aggiunta.
Sommando (2) si ottiene esattamente

\[
             2s_3(Tn)=s_3(n)+p+2C(n).              \tag{3}
\]

Il riporto finale è zero, e il riporto iniziale è zero: queste condizioni
sono necessarie alla formula. Contare invece i riporti in ingresso sulle
sole cifre originali darebbe una convenzione diversa.

Per `h≥1`, siano `n_t=T^t(n_0)` e `C_tot=Σ_(t=0..h−1) C(n_t)`.
La somma di (3) dà

\[
 J_{n_0}(h)=\sum_{t=1}^{h-1}s_3(n_t)+2s_3(n_h)-s_3(n_0)-2C_{\rm tot}.
                                                               \tag{4}
\]

Per la lunghezza ternaria canonica `b(n)`, se `z(n)` conta gli zeri
iniziali eliminati al passo, vale analogamente

\[
 b(Tn)=b(n)+p-z(n),\qquad
 J_{n_0}(h)=b(n_h)-b(n_0)+\sum_{t=0}^{h-1}z(n_t).    \tag{5}
\]

Questi bilanci sono utili controlli di correttezza del simulatore.
Usare (4) o (5) per ricostruire `J`, e poi chiamare il risultato un
«budget dei riporti», non fornisce una disuguaglianza nuova. Occorre una
restrizione ulteriore, dimostrata senza assumere già il conteggio delle
parità da limitare.

### L'orologio della lunghezza è esatto nell'intervallo usato

Per l'input speciale `R_m`, si può precisare (5) senza simulare i
riporti. Se `4^t<3^m`, allora

\[
 b(T^t(R_m))=m+J_{R_m}(t)-\kappa(t),\qquad
 \kappa(t)=\lfloor\log_3(2^t)\rfloor.                \tag{5a}
\]

**Dimostrazione.** Il caso `t=0` è immediato. Per `t≥1`, posto
`j=J_(R_m)(t)`, la formula affine dà

\[
 T^t(R_m)=\frac{3^{m+j}-3^j+C}{2^t},
 \qquad 0\le C<3^j2^t.
\]

L'ultimo limite segue sommando i contributi additivi dei passi dispari:
`C/3^j` è una somma di termini `2^i/3^(J_(R_m)(i)+1)` ed è minore
di `2^t`. Posto `κ=κ(t)`, vale `3^κ<2^t<3^(κ+1)`; le differenze
sono interi positivi. Inoltre `κ+1≤m`. Il margine fra
`3^(m+j)` e `2^t·3^(m+j−κ−1)` è almeno
`3^(m+j−κ−1)≥3^j`, e copre il termine sottratto `3^j`.
Questo prova il limite inferiore
`T^t(R_m)≥3^(m+j−κ−1)`.

Per il limite superiore, `2^t3^κ≤4^t<3^m` implica
`3^(m+j−κ)>3^j2^t>C`. Il margine fra
`2^t·3^(m+j−κ)` e `3^(m+j)` è almeno `3^(m+j−κ)`.
Quindi `T^t(R_m)<3^(m+j−κ)`. I due confronti danno (5a).

Il dominio del lemma copre uniformemente gli orizzonti di questa nota:
per `v≥5`, `H_v≤2^v` e `v+3≤2^(v−1)`, dunque `L≤3m/4` e

\[
 4^L\le8^{m/2}<9^{m/2}=3^m.
\]

La stessa condizione, quadrata, copre l'input superiore `R_(2m)`
fino al tempo `2L`. Ne segue che il numero cumulativo di zeri iniziali
rimossi è esattamente `κ(t)`, e

\[
 E(m,L)=b(T^{2L}(R_{2m}))-2b(T^L(R_m))
       +\kappa(2L)-2\kappa(L),\qquad
 \kappa(2L)-2\kappa(L)\in\{0,1\}.                  \tag{5b}
\]

Nel codice `κ` si calcola confrontando potenze intere, senza logaritmi
in virgola mobile. La relazione (5b) chiarisce anche il limite di un
potenziale basato sulla sola lunghezza: stimare quel difetto di lunghezza
equivale, a una correzione di al più uno, a stimare `E` stesso.

## 4. Due limiti precisi ai potenziali troppo semplici

### Un bit di interfaccia può modificare un blocco intero

Da (2) segue `c_(i+1)=(c_i+d_i) mod2`. Due scansioni dello stesso blocco
di `b` cifre, con riporti iniziali opposti, conservano riporti opposti
a ogni posizione. Se i conteggi dei riporti in uscita sono `C_0,C_1`,

\[
 C_1=b-C_0,\qquad C_1-C_0=b-2C_0.                  \tag{6}
\]

Per un blocco di soli `2` si ha `C_0=0`, `C_1=b`. Tutte le cifre dei
due quozienti differiscono. Un'interfaccia descritta da un solo bit non
garantisce quindi un errore limitato indipendentemente dalla larghezza.
Non si afferma che ogni configurazione avversa così descritta sia
raggiungibile dalla torre.

Nel grafo locale `/2`, lo stato `c=1` ha inoltre un cappio sulla cifra
`0`, con riporto in uscita `1`. Un potenziale sui soli due stati che
pretenda un costo medio dei riporti `ρ<1` su **tutte** le transizioni
fallisce già su quel cappio. Esso è accessibile e richiudibile: la parola
pari `1·0^b·1` ha `b+1` riporti uguali a `1` su `b+2` cifre.

### Un certificato finito contro sei pesi additivi locali

Definiamo `N_cd(n)` sulle cifre ternarie **canoniche originali** di `n`,
prima di un eventuale append. Ogni cifra `d∈{0,1,2}` viene etichettata
dal riporto in ingresso `c∈{0,1}` della scansione `/2` con stato iniziale
zero. Ordiniamo i sei conteggi come `(00,01,02,10,11,12)`.

Consideriamo un potenziale della forma

\[
 \Phi(n)=\sum_{c,d}\alpha_{cd}N_{cd}(n),
 \qquad n\bmod2\le\rho+\Phi(n)-\Phi(Tn).            \tag{7}
\]

Se (7) deve valere per ogni intero positivo, necessariamente `ρ≥1`.
Un certificato esatto consiste nei due passi dispari

| Passo | Rappresentazioni ternarie | `N(n)−N(Tn)` |
|---|---|---|
| `51→77` | `1220→2212` | `(0,0,−2,1,0,1)` |
| `403→605` | `112221→211102` | `(0,0,2,−1,0,−1)` |

I vettori sono opposti. Sommando le due istanze di (7), il potenziale
si cancella e resta `2≤2ρ`. Le rappresentazioni e i vettori sono stati
ricalcolati indipendentemente.

L'ostacolo riguarda precisamente questa classe di potenziali lineari
additivi su sei tipi locali. Include combinazioni lineari di lunghezza,
somma delle cifre e numero delle cifre `1`, che sono funzioni lineari
dei sei conteggi. Non esclude potenziali non lineari, informazioni
posizionali, automi più ricchi o certificati limitati a stati la cui
raggiungibilità dalla famiglia speciale sia stata dimostrata. I due
esempi non vengono presentati come punti raggiunti da `Q_v`.

## 5. Il primo difetto possiede invece una struttura aritmetica utile

Dopo i primi `r` passi pari, la parola inferiore è
`Q_v=(3^m−1)/2^r`. Scriviamola con esattamente `m` cifre ternarie,
aggiungendo zeri a sinistra se necessario, e chiamiamola `W`.
Al medesimo tempo la parola superiore è `WW`, perché

\[
 \frac{3^{2m}-1}{2^r}=Q_v(3^m+1).
\]

`Q_v` è dispari. La divisione della parola superiore `WW` legge quindi
il primo blocco con riporto iniziale `0` e il secondo con riporto `1`.
Se `C_0` è il conteggio dei riporti in uscita della divisione grezza
di `W` per due, il difetto fra i due conteggi è `D_r=m−2C_0`.

Il prefisso di `W` lungo `i` cifre rappresenta esattamente

\[
 \left\lfloor\frac{Q_v}{3^{m-i}}\right\rfloor
 =\left\lfloor\frac{3^i}{2^r}\right\rfloor,
 \qquad 1\le i\le m.
\]

Il riporto dopo quel prefisso è la sua parità. Dunque

\[
 D_r=\sum_{i=1}^m\left(1-2\operatorname{bit}_r
                  (3^i\bmod2^{r+1})\right).        \tag{8}
\]

Questa è una somma su potenze modulari, indipendente dalle parità
Collatz future. La [dimostrazione separata](FIRST_SEAM_BOUND_IT.md)
stabilisce, per ogni `r≥3`,

\[
 |D_r|\le\sqrt{8m}\,h_{\rm odd}(4m)h_{\rm odd}(m)
 \le\frac{\sqrt{8m}}4(r^2-1),
 \qquad 2D_r^2\le m(r^2-1)^2,                       \tag{9}
\]

dove `h_odd(M)=Σ_(1≤a<M,a dispari)1/a`. Il limite polinomiale è
non banale da `v=15`; una variante più precisa lo è da `v=13`.
Si tratta delle soglie delle maggiorazioni, non di livelli aggiunti
alla verifica dell'orbita.

La prova sfrutta l'antiperiodicità del bit dopo mezzo periodo e
l'annullamento delle frequenze pari. Un carattere dispari delle unità
modulo `2^(r+1)` permette di applicare le somme di Gauss con le
normalizzazioni esplicitate nella nota. Il fatto classico è verificato
anche mediante una dimostrazione elementare con ortogonalità e Parseval.

Al primo disaccoppiamento, tuttavia, la traiettoria inferiore applica
`T(Q_v)=(3Q_v+1)/2`, con append, mentre quella superiore divide `WW`
per due. La struttura che ha permesso (8) non è stata provata stabile
nei passi successivi. Sommare il limite (9) lungo la traiettoria senza
questo nuovo lemma non sarebbe giustificato.

## 6. Verifica indipendente delle simulazioni

Il [driver Python](ternary_probe.py) e il [JSON prodotto](ternary_results.json)
conservano i risultati di `12` livelli, `v=5..16`, e di `11` coppie,
`v=5..15`, entro l'intervallo già studiato. Il C ha eseguito `126423`
passi abbreviati, con `10686998090` letture di cifre nelle scansioni.

Per tutti i dodici livelli sono stati verificati:

- la coincidenza SHA-256 della parola di `Q_v` con la precedente
  [baseline](../post_v6_margin_2026-09-25/margin_results.json);
- tutte le parità e lo stato finale mediante un replay indipendente di
  `T` sugli interi Python, con decodifica dello stato ternario finale;
- le identità di massa e lunghezza del registro, l'orologio (5a) a ogni
  passo e la rimozione iniziale dei fattori di due.

Il confronto con gli interi non usa il trasduttore ternario per costruire
la traiettoria attesa. Il registro dei riporti dei casi grandi soddisfa
le identità esatte; il confronto indipendente di **tutte** le sue colonne
passo per passo viene inoltre eseguito nei `42` casi C piccoli della
[suite di test](test_ternary.py). Le identità interne, da sole, non
sarebbero una verifica indipendente dell'orbita.

| `v` | `Δ_v` | `E(m,L)` | Dispari nella coda | Lunghezza della coda |
|---:|---:|---:|---:|---:|
| 5 | 6 | 9 | 3 | 7 |
| 6 | −2 | 3 | 5 | 8 |
| 7 | −12 | −8 | 4 | 10 |
| 8 | 28 | 33 | 5 | 11 |
| 9 | −53 | −46 | 7 | 11 |
| 10 | −15 | −7 | 8 | 12 |
| 11 | 53 | 58 | 5 | 14 |
| 12 | 99 | 110 | 11 | 15 |
| 13 | −164 | −152 | 12 | 16 |
| 14 | 75 | 85 | 10 | 17 |
| 15 | 47 | 53 | 6 | 17 |

Tutte le righe verificano sia (1) sia (5b). Questi valori sono un replay
finito, non una nuova validazione separata di una candidata uniforme.

Il primo difetto `D_r` è stato calcolato per `18` livelli, `v=5..22`.
Per `v=5..12`, otto confronti indipendenti con la parola ternaria `W`
completa e i due riporti iniziali confermano anche la formula modulare
(8). Per esempio, `D=-88` a `v=15`, `740` a `v=16` e `−6752` a `v=22`.
Tutti i diciotto valori soddisfano il certificato intero
`2D²≤m(r²−1)²`; la validità uniforme di tale limite discende dalla prova,
non dall'elenco finito.

La suite contiene `12` test, incluse alterazioni deliberate di parità e
stato finale per verificare che il replay indipendente le rifiuti.
Per riprodurre i dati dalla radice del repository su macOS:

```sh
DEVELOPER_DIR=/Library/Developer/CommandLineTools clang -std=c11 -O3 -Wall -Wextra -Wpedantic notes/post_v6_ternary_2026-09-25/ternary_engine.c -o /tmp/ternary_engine
python3 notes/post_v6_ternary_2026-09-25/ternary_probe.py --engine /tmp/ternary_engine --output /tmp/ternary_replay.json
cmp notes/post_v6_ternary_2026-09-25/ternary_results.json /tmp/ternary_replay.json
TERNARY_ENGINE=/tmp/ternary_engine python3 -m unittest discover -s notes/post_v6_ternary_2026-09-25 -p 'test_ternary.py' -v
```

Su un ambiente con compilatore C già configurato si può omettere
`DEVELOPER_DIR`. I dati non contengono tempi di esecuzione, così il replay
può essere confrontato byte per byte.

<!-- INTEGRARE DAL COORDINATORE SOLO DOPO ESITO: evidenza finale CI. -->

## 7. Il passaggio ancora necessario

La stima (9) è una disuguaglianza locale uniforme: supera il solo
ricalcolo di un bilancio e usa la forma esatta dell'input. Per arrivare
a `E(m,L)` serve controllare come i blocchi si trasformano dopo gli
append divergenti, e dimostrare un costo cumulativo utilizzabile.
Il certificato negativo (7) delimita una scelta semplice di potenziale,
senza esaurire le possibilità di un modello più informativo.

Non è stata dimostrata una stima uniforme per `E` o `Δ_v`, né una nuova
discesa della famiglia. Rimane aperto il collegamento fra la cancellazione
aritmetica del primo confronto e l'intera storia Collatz.
