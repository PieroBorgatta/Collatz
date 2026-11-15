# S07 Uscite delle macro e reset del parametro

13 novembre 2026. Incarico di ricerca su `N(r,t)=18t·8^r−5`, r,t positivi. Stato dei risultati nuovi: deduzioni **su carta** e controlli interi esatti, senza nuove dichiarazioni Lean. Non è stato aggiunto un modulo `MacroExit.lean` che si limitasse a ripresentare un criterio già disponibile.

## Punto di partenza e distinzione dal lavoro esistente

`ReturnBlocks.lean` certifica r primi ritorni crescenti con parola `[1,2]^r` e terminale `18t·9^r−5`. Per t=1 il passo seguente è già `cancellationTower_exit_one (r+1)`, con esponente 3. Il problema utile è il raccordo fra una macro e la successiva: il clock consumato dentro la macro può ricomparire dopo l'uscita.

Per t dispari, ponendo `Z=27t·9^r−7`, l'esponente dopo il terminale è esattamente `1+ν₂(Z)`, e il prossimo valore è `Z/2^ν₂(Z)`. Il solo fatto che il clock iniziale sia sceso non controlla questo reset.

## Un dominio sufficiente di discesa e il suo costo

La condizione `2^r | Z` implica che il passo dopo la macro scende sotto N(r,t). Infatti, per r≥1,

`27·9^r−7 < 2^r(18·8^r−5)`.

La differenza dei coefficienti cresce a partire da `18·16−27·9=45`, e supera la correzione `5·2^r−7`; moltiplicare il coefficiente per t≥1 conserva l'ineguaglianza. Per il valore reale del passo si divide almeno per `2^r`.

È una sola classe di t modulo `2^r`. Un costo migliore si ottiene con b_r minimo tale che

`2^b_r · 8^r ≥ 3·9^r`,

e chiedendo `2^b_r | Z`. La minimalità dà `2^b_r < 6·9^r/8^r`, che controlla anche la correzione affine; il passo scende per ogni t positivo nella classe. Fra i parametri t dispari, la densità della classe è `2^(1−b_r)`, dell'ordine di `(8/9)^r`.

Questa è un'applicazione parametrica del criterio affine di `FirstBarrier`, non una nuova copertura universale. La quota si riduce con r e non controlla i parametri esclusi. Un test numerico più esteso della stessa condizione non darebbe il lemma globale mancante.

## Una vera interfaccia di primo ritorno e il reset arbitrario

Siano r,s≥1 e t,v positivi dispari che soddisfano

`8^(s+1)·v = 27·9^r·t + 13`.                                          (1)

Allora la parola

`[1,2]^r ++ [3,1,2]`

porta N(r,t) in `N(s−1,v)`. Per ogni r,s esistono infiniti tali t,v: poiché `c=27·9^r` è dispari, si sceglie un v dispari positivo con `2^(3s+3)v≡13 mod c`, sufficientemente grande, e si pone `t=(2^(3s+3)v−13)/c`. Il numeratore è dispari, quindi anche t è dispari.

La verifica dei tre passi finali è esplicita. Se `p=9^r t` e `q=8^(s−1)v`, (1) diventa

`64q=27p+13`.

Questo equivale a `p=9+64u`, `q=4+27u`, con u naturale. Si ha quindi la famiglia

| Tempo dopo il terminale | Valore | Esponente seguente |
|---:|---|---:|
| 0 | `157+1152u` | 3 |
| 1 | `59+432u` | 1 |
| 2 | `89+648u` | 2 |
| 3 | `67+486u` | — |

Le identità `3n+1=2^a m` e la disparità degli endpoint certificano gli esponenti. Sorgente e destinazione sono `13 mod18`. Gli intermedi sono `59 mod72` e `17 mod72`, incompatibili con i sei porti di E. Si tratta pertanto del **primo** ritorno alla sezione dopo il terminale della macro.

Questo ritorno di tre passi è localmente decrescente: la sorgente supera la destinazione di `90+666u`. Tuttavia, dopo una macro lunga, non recupera la crescita precedente. Per r≥9 tutti e tre i nuovi valori restano sopra N(r,t), perché

`27·9^r > 72·8^r`,

con verifica intera a r=9 e propagazione tramite 9>8. I primi due passi `[1,2]` del nuovo blocco sono anch'essi crescenti rispetto al suo inizio.

Il nuovo clock è `s−1`: infatti `ν₂(N(s−1,v)+5)=1+3(s−1)` per v dispari. A r fissato, s può essere arbitrariamente grande. Un rango che registrasse soltanto il numero dei blocchi consumati non controllerebbe il raccordo.

### Un autoarco del clock non è un ciclo dell'orbita

Prendendo s=r+1, il clock resta r. Per r≥8 si può avere v>t; anzi il coefficiente `27·9^r/8^(r+2)` supera 1. Un esempio esatto è

`r=9, t=11050630593, v=13456854401`,

con traiettoria composta da

`26697429560875548667 → 32510671627122376699`

lungo `[1,2]^9 ++ [3,1,2]`. Il valore e il cofattore aumentano, mentre il clock torna a 9.

Questo è un autoarco del quoziente dei parametri, non un ciclo reale o una traiettoria divergente. Ripeterlo esige nuove congruenze a ogni visita. Per r fissato la parola è espansiva quando r≥8; i risultati già presenti su `NoInfinite` e `PrecisionTax` spiegano perché una ripetizione arbitrariamente lunga a precisione finita non certifichi una ripetizione infinita da un intero positivo.

## Un conteggio esatto della coda dei reset su questo ramo

Il ramo finale `[3,1,2]` è caratterizzato da

`t·9^r ≡ 9 mod64`.

Al variare di t nella sua progressione modulo 64, il nuovo parametro q varia come

`q_j=q_0+(27·9^r)j`,

con passo dispari. Nel normale decomporsi `q=8^R t'`, `ν₂(t')<3`, il nuovo clock è `floor(ν₂(q)/3)`. La condizione che esso sia almeno R è esattamente `8^R|q`.

Poiché il passo è invertibile modulo `8^R`, questa condizione seleziona **una sola classe** di j modulo `8^R`. Fra U parametri consecutivi, il conteggio è quindi compreso fra `floor(U/8^R)` e `ceil(U/8^R)`. È un limite aritmetico di coda autentico per la famiglia, senza probabilità o ipotesi di mixing.

Questo potrebbe essere integrato come primo caso chiuso del kernel troncato o di un certificatore di macro: un reset può essere illimitato e avere comunque una coda media esatta. Non è lecito applicare tale frequenza ai parametri visitati da una singola orbita senza una nuova stima. Né il ramo `[3,1,2]` copre tutte le uscite della macro.

## Prova finita e confronto fra agenti

Lo script [s07_macro_exit.py](../experiments/s07_macro_exit.py) fissa prima dei calcoli i domini r=1,…,12, t dispari=1,…,127 e cap 64 per il prossimo punto della sezione; i test dei reset usano s=1,…,20. [Dati](../verification/s07_macro_exit.json): **768 casi**, **384 discese al primo passo d'uscita**, **zero ritorni marcati irrisolti nel cap**, **240 testimoni della relazione (1)**, **150 clock aumentati**, **5 esempi a stesso clock e cofattore maggiore**, **360 profili del conteggio esatto della coda**. Tutte le identità e le proprietà di primo ritorno controllate passano; il JSON è identico con e senza ottimizzazione Python.

S06 ha confrontato il costo della classe d'uscita con le sue ostruzioni alle trasformazioni a shift limitato. S08 ha segnalato che gli endpoint concatenati sono annidati e non formano un pool nonricorrente; il limite forte `Σω/R≤1/x` non è applicabile. S09 ha ricevuto l'autoarco del clock come esempio della distinzione fra ciclo del quoziente e realizzabilità infinita; ripetere un sieve su rotazioni non risolve quest'ultima.

## Prosecuzione e arresto

Il risultato utile è l'interfaccia esatta (1) con il suo conteggio di coda, non una promessa di rango globale. Un passo successivo circoscritto è formalizzare il primo ritorno di tre passi e la coda per r fissato, poi cercare un'analoga tassonomia completa delle altre uscite. La relazione espone il tradeoff fra clock e cofattore, ma non ne è stata trovata una combinazione ben fondata valida su tutte le transizioni.

Fermare la sintesi di un rango solo r o di un rango che assuma che ogni ritorno decrescente cancelli l'intera escursione precedente: le famiglie sopra lo smentiscono. Fermare anche il passaggio dalla frequenza in una progressione alla frequenza lungo un'orbita senza un'identità di misura o una stima indipendente. Non è stata ottenuta una nuova discesa uniforme della torre o della sezione.
