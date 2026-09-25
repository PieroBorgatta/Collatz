# La giunzione si propaga esattamente; il problema rimane nella coda

**25 settembre 2026.** Abbiamo esteso il controllo oltre la prima divisione.
Il risultato principale è un'identità esatta, valida a ogni tempo: tutte
le colonne ternarie originarie evolvono mediante semplici divisioni per
due. Le aggiunte determinate dalla parità occupano una coda separata.
Questo permette di trasferire le stime modulari alla giunzione effettiva,
senza un errore di bordo. Non controlla ancora il conteggio totale dei
passi dispari. Le prove sono su carta, con controlli indipendenti; non
aggiungono dichiarazioni Lean e non rivendicano originalità matematica.

## 1. Una decomposizione esatta per ogni intero

Per la mappa shortcut `T`, sia `j=J_n(t)` il numero dei passi dispari.
La [prova completa](PREFIX_PROPAGATION_IT.md) stabilisce

\[
 T^t(n)=3^j\left\lfloor\frac n{2^t}\right\rfloor
       +T^t(n\bmod2^t),\qquad
 0\le T^t(n\bmod2^t)<3^j.                         \tag{1}
\]

Quindi

\[
 \left\lfloor\frac{T^t(n)}{3^j}\right\rfloor
 =\left\lfloor\frac n{2^t}\right\rfloor.            \tag{2}
\]

La prima parte segue dalla congruenza delle parità; il limite sul resto
segue da un'induzione con soglie intere pari prima di ogni passo.
Una seconda lettura viene dal trasduttore ternario: la divisione legge
le cifre da sinistra e l'aggiunta di una cifra a destra non modifica
le cifre già lette.

Se `n` parte da `M` cifre e conserviamo gli zeri iniziali, dopo `t` passi
la parola ha larghezza `M+j`. Le sue prime `M` cifre rappresentano
`floor(n/2^t)`; le ultime `j` rappresentano il resto in (1). Il risultato
vale anche quando il primo blocco è diventato interamente zero.

## 2. Applicazione alla famiglia e al difetto dei riporti

Poniamo

\[
 r=v+3,\quad m=2^{r-2},\quad
 Q_v=(3^m-1)/2^r,\quad U_0=(3^{2m}-1)/2^r=2Q_{v+1}.
\]

Per `X_0=(3^M−1)/2^r`, `M=m` oppure `2m`, ogni prefisso originario
lungo `i≤M` nello stato al tempo `t` rappresenta

\[
                 \left\lfloor\frac{3^i}{2^{r+t}}\right\rfloor.
                                                               \tag{3}
\]

Il riporto uscente da quel prefisso, nella divisione per due con ingresso
zero, è il bit `r+t` di `3^i`. Definiamo sulla parola superiore

\[
 D_{r,t}=\sum_{i=1}^m
 \left[\operatorname{bit}_{r+t}(3^{i+m})-
       \operatorname{bit}_{r+t}(3^i)\right].          \tag{4}
\]

Questa formula è **esattamente** la differenza fra i riporti delle due
porzioni originarie dello stato superiore: vale per ogni `t`, senza
scartare cifre. A `t=0` recupera il difetto della fase precedente.
Le ultime `J_{U_0}(t)` colonne, prodotte dagli append, sono escluse
esplicitamente dalla definizione.

La [prova Fourier](FOURIER_PROPAGATION_IT.md) dà, uniformemente,

\[
 |D_{r,t}|\le B_{r,t}
 =\frac{\sqrt{2^{r+t+1}}}{4}(r-1)(r+t+1),\qquad
 2D_{r,t}^2\le m2^t(r-1)^2(r+t+1)^2.               \tag{5}
\]

Si può sempre prendere il minimo con il limite banale `m`.
Il limite (5) diventa inferiore a `m` sotto una condizione intera
verificabile; la sua profondità massima è
`r−4log₂r+O(1)`. L'identità (3) continua invece a valere a ogni tempo.

| Profondità `t` | Primo livello `v` con `B_(r,t)<m` |
|---:|---:|
| 0 | 15 |
| 1 | 17 |
| 2 | 18 |
| 4 | 21 |
| 8 | 27 |
| 16 | 37 |
| 32 | 55 |
| 64 | 90 |

Questa tabella valuta la maggiorazione dimostrata: non certifica nuove
orbite e non indica il primo livello in cui il difetto effettivo è piccolo.

## 3. Un raccordo esatto fra i riporti delle due orbite

Siano `C_L(t),C_U(t)` i conteggi di tutti i riporti nello stato inferiore
e superiore, al medesimo tempo `t`. Indichiamo con `A_L(t),A_U(t)` i
conteggi nelle sole code aggiunte, lunghe rispettivamente `j_L,j_U`.
Le prime `m` colonne superiori coincidono con quelle inferiori. Segue

\[
 C_U(t)-2C_L(t)=D_{r,t}+A_U(t)-2A_L(t),\qquad
 |A_U(t)-2A_L(t)|\le\max(j_U,2j_L)\le2t.           \tag{6}
\]

La [nota sui prefissi](PREFIX_PROPAGATION_IT.md) precisa le convenzioni
e dimostra (6). Il conteggio coincide con quello della scansione del
passo shortcut: l'eventuale cifra `1` aggiunta per il passo corrente
chiude il riporto a zero e non aggiunge un riporto uscente uguale a uno.

La formula confronta le due orbite **allo stesso tempo**. Il difetto
`E(m,L)` del progetto usa tempi diversi, `2L` e `L`, e conta le parità.
Non si possono identificare queste quantità. Inoltre il costo `2t`
sommato fino a un orizzonte dell'ordine di `m` è troppo grande per il
budget cercato. Il problema residuo è ora localizzato nelle code e nel
raccordo temporale.

## 4. Che cosa aggiunge la letteratura

La [ricerca mirata](LITERATURE_IT.md) verifica cinque fonti primarie.
Una specializzazione di Mérai–Shparlinski, pubblicata nel 2020, estende
il controllo delle somme modulari alla scala `r+t+1=o(r^(3/2))`.
Grazie a (3), la conclusione si trasferisce alla giunzione effettiva.
Le costanti del risultato non sono esplicitate: non ne ricaviamo nuove
soglie numeriche certificate. La scala resta molto più corta di `t≈m`.

Non tutte le richieste di bilanciamento possono essere vere: quando
`t=m`, la singola finestra iniziale di segni ha un contributo positivo
lineare dovuto a potenze troppo piccole per avere il bit considerato.
La nota dimostra questo ostacolo e lo distingue dal difetto fra due
finestre: non è un controesempio a una stima su `D`, `E` o `Δ_v`.

## 5. Verifica riproducibile

Il [probe](propagation_probe.py) confronta il trasduttore ternario della
fase precedente con l'iterazione sugli interi. Per ciascuno dei dodici
indici `v=5..16`, segue `Q_v` e `U_0=2Q_(v+1)` ai tempi distinti
nell'insieme `{0,1,2,4,8,16,32,r,2r}`: in totale **104 coppie di stati,
208 stati verificati**, fino al tempo 38. Sono prefissi di orbite già
studiate, non nuovi livelli certificati né nuovi orizzonti di discesa.

Per ciascuno stato sono verificati valore intero finale, parola di
parità, decomposizione affine, resto in (1), tutte le cifre e tutti i
riporti originari. Per ogni coppia sono verificati (4)–(6). Tutti i
104 errori fra giunzione osservata e modello sono esattamente zero,
come richiede la prova.

Per esempio, a `v=16`, i difetti ai tempi `t=0,2,4,8,16,32,38` sono
rispettivamente `740,876,247,−282,−169,−255,−660`. La maggiorazione (5)
è valida, ma per questo livello è già banale a `t=1`: il successo della
riproduzione esatta non equivale all'efficacia quantitativa del limite.

Gli [11 test](test_propagation.py) includono 8.188 casi dell'identità
generale del quoziente, tutti i 1.023 codici binari fino a nove passi
per gli estremi della costante affine, oracoli interi per le due parole,
le soglie delle maggiorazioni e alterazioni deliberate rifiutate dal
verificatore. I [risultati JSON](propagation_results.json) sono deterministici.

Dalla radice del repository:

```sh
python3 notes/post_v6_propagation_2026-09-25/test_propagation.py
python3 notes/post_v6_propagation_2026-09-25/propagation_probe.py --output /tmp/propagation_results.json
cmp notes/post_v6_propagation_2026-09-25/propagation_results.json /tmp/propagation_results.json
```

La [CI di propagazione](https://github.com/PieroBorgatta/Collatz/actions/runs/36155684360)
e la [build Lean con gli audit esistenti](https://github.com/PieroBorgatta/Collatz/actions/runs/36155684119)
sono passate sul commit `a65d2e2`. Tutti gli undici test passano anche
nella CI Linux; il JSON scaricato è identico byte per byte a quello locale.
La CI ripete le implementazioni archiviate: l'indipendenza deriva dagli
oracoli aritmetici distinti, non dal cambio di macchina. La build Lean
verifica le dichiarazioni esistenti e non formalizza queste nuove note.
Log e SHA-256 sono archiviati nel [manifesto](verification_manifest.json).
Gli input delle sei fasi precedenti e i due artifact pubblicati v6 sono
invariati; i manifesti precedenti restano riferimenti storici, compresi
i loro SHA del README.

## 6. Il prossimo problema concreto

La [nota successiva](NEXT_RESEARCH_IT.md) scrive l'evoluzione esatta della
coda come trasduttore alimentato dai bit dell'intero iniziale. Il compito
è trovare un controllo aggregato della coda, insieme al confronto dei
tempi, che sia più forte del costo lineare per singola scansione.
L'ostacolo non è più la perdita di una descrizione delle colonne originali:
quella descrizione ora è esatta. La discesa uniforme e il limite su `Δ_v`
rimangono aperti.
