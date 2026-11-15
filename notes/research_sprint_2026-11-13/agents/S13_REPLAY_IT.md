# S13 Replay indipendente dei nuovi esperimenti

13 novembre 2026. Controllo indipendente degli algoritmi di S06, S07 e S10 e dei bordi del lemma del clock di S11. Nessun sorgente Lean o dato degli altri agenti è stato modificato. Lo [script](../experiments/s13_independent.py), i [risultati](../verification/s13_independent.json) e la [ricevuta](../verification/s13_receipt.json) conservano domini e hash.

**Esito: PASS.** Nessun errore materiale nei risultati finiti verificati. I replay normale e con Python `-O` producono file identici byte per byte. I controlli critici usano eccezioni esplicite e non dipendono da `assert`.

## Trasformazioni di parole senza prefiltro

Il censimento indipendente riguarda sorgenti dispari fino a 1024, target `{5,7,31,593}` e shift `{-5,-3,-1,1,3,5}`. Ogni sorgente è seguita fino al primo arrivo al target oppure a 1, con un cap esplicito di 2048 passi accelerati e rilevamento dei cicli. Il primo arrivo a tempo zero è incluso.

L'immagine non viene costruita dal polinomio affine C e non viene applicato alcun prefiltro di congruenza terminale. Per ogni parola modificata con esponenti positivi, si parte dal bersaglio superiore e si eseguono tutte le inversioni, in ordine inverso:

`z ← (2^a z−1)/3`.

Una divisione non integrale scarta la parola. Per una parola accettata si ricontrollano positività, disparità, esponenti esatti e endpoint con iterazione diretta, usando divisioni ripetute per due. Solo dopo l'accettazione si verifica la congruenza necessaria proposta da S06; nessun caso accettato la viola.

Sono state esaminate **27.468 modifiche con esponenti positivi**. I **47 codici accettati** si distribuiscono come `10,20,17,0` per i quattro target. Tutti i campi confrontati con S06 coincidono: numero delle sorgenti di base, istogrammi delle profondità, codici, coppie fisiche, immagini distinte, carico massimo e conteggi sotto i fattori d'altezza `{1,4,16,64}`.

La collisione fisica viene ricostruita separatamente, fuori dal cutoff del piccolo censimento: `16853` e `16867` raggiungono 593 con parole `[7,1]` e `[1,7]`; la parola modificata `[4,4]` ha sorgente inversa `270021` al target `9493`. Il carico 1 sulle immagini non segue dall'iniettività di un catalogo di parole.

## Macro e primo ritorno

Per **96 coppie** `r=1,…,8`, `s=1,…,12`, vengono costruiti parametri positivi dispari t,v dalla congruenza completa modulo `2·8^(s+1)` e verificata l'identità

`8^(s+1)v=27·9^r t+13`.

La parola effettiva `[1,2]^r ++ [3,1,2]` porta da `18t8^r−5` a `18v8^(s−1)−5`. L'iterazione indipendente verifica tutte le valutazioni. I tempi marcati sono esattamente `2,4,…,2r,2r+3`: i due intermedi dell'ultimo ritorno sono esclusi dalla sezione. Anche il testimone a stesso clock r=9 è riprodotto.

Questo controllo certifica gli esempi e l'implementazione; non prova che le congruenze necessarie a ripetere un autoarco valgano indefinitamente.

## Code del clock e osservabili limitate

Sono stati controllati **648 profili** di coda e **180 periodi completi** per `q_j=q0+bj`, con q0 positivo, b positivo dispari, offset iniziali `{0,1,17}`, R da 0 a 4 e U tra 1 e i valori `8^R−1`, `8^R`, `8^R+1`. È incluso q0=`8^8`; q=0 viene rifiutato esplicitamente.

Il conteggio di `floor(ν₂(q_j)/3)≥R` soddisfa il limite floor/ceil. Nei periodi completi le frequenze troncate sono quelle geometriche dichiarate. Sono inoltre superati **3.240 confronti esatti dell'errore medio**, usando `F(k)=(-1)^k`, con media modello `7/9`, e gli indicatori `1_(k≥K)` per K in `{0,1,3,8}`, con media modello `8^-K`.

I test includono i casi R=0 e U=1. Verificano il caso `F(clock)`; non autorizzano la stessa conclusione per cofattori, bit length o distribuzioni dei parametri lungo una singola orbita.

## Segmenti finiti e prodotto affine

Per **480 segmenti** con sorgente dispari fino a 1024 e primo arrivo a 5 vengono verificate **480 identità esatte del prodotto affine**. La traiettoria shortcut viene ricostruita separatamente e si controlla che non ripeta valori.

I **3.355 troncamenti** comprendono N=0, piccoli N e i bordi N=L, N=L+1, N=L+5, dove L è l'ultimo indice. Sul prefisso ottenuto eliminando gli ultimi N punti, l'iterata T^N è iniettiva; i punti eliminati sono al più N. Per la sorgente già uguale al bersaglio, il primo arrivo a tempo zero è trattato correttamente.

È riprodotta anche la collisione di T^5 sull'intero segmento `7→11→17→26→13→20→10→5`: omettere il troncamento sarebbe scorretto. Nessuno di questi calcoli dimostra la stima uniforme delle finestre, il limite B o D₀: questi rimangono argomenti matematici da verificare su carta o in Lean.

## Confronto fra agenti

S12 ha richiesto esplicitamente i bordi N=L e N>L e la distinzione tra primo arrivo e ripetizione di un ciclo; sono inclusi nel controllo del prefisso. S11 ha precisato i domini q0,b,U e i casi R=0, q0 ad alta valutazione e offset non nullo; sono stati verificati e i risultati gli sono stati restituiti. A S14 è stata comunicata la corrispondenza fra cataloghi, immagini e normalizzazioni, senza attribuire ai replay un audit degli assiomi o una prova delle nuove stime asintotiche.

## Supplemento Accoppiamento fra profili congiunti

Richiesta supplementare del coordinatore dopo il congelamento del [protocollo dei profili](../PROFILE_TRANSPORT_PROTOCOL_IT.md) alle 16:16:45 UTC. Controllo eseguito fra le 16:18 e le 16:21 UTC. Il [programma indipendente](../experiments/s13_profile_matching.py), il [risultato](../verification/s13_profile_matching.json) e la [ricevuta](../verification/s13_profile_matching_receipt.json) sono separati dal primo replay.

Sono stati scelti otto casi del protocollo: X=256, target n in `{5,7,31,593}` e dilatazioni D in `{16,64}`. Le parole del primo arrivo sono ricostruite direttamente dall'iterazione Syracuse, per sorgenti dispari u≤X e immagini dispari v≤DX. Ogni intero compare una volta nel rispettivo catalogo. Un arco richiede uguali profili `(lunghezza, somma degli esponenti)` e `v≤D·u`.

L'algoritmo di controllo non usa il greedy a soglia del coordinatore. Costruisce il grafo bipartito esplicito, cerca cammini aumentanti e conserva un matching con capacità uno su entrambe le parti. L'esplorazione residua alternata produce inoltre un **vertex cover della stessa cardinalità del matching**; viene controllato che copra ogni arco. Questo certifica l'ottimalità finita del conteggio in ciascun caso, indipendentemente dall'argomento greedy.

| Target n | D | Sorgenti di base | Immagini entro DX | Massimo matching | Sorgenti con profilo assente |
|---:|---:|---:|---:|---:|---:|
| 5 | 16 | 120 | 48 | 0 | 70 |
| 5 | 64 | 120 | 203 | 47 | 60 |
| 7 | 16 | 18 | 471 | 15 | 3 |
| 7 | 64 | 18 | 1.933 | 15 | 3 |
| 31 | 16 | 9 | 190 | 5 | 4 |
| 31 | 64 | 9 | 740 | 5 | 4 |
| 593 | 16 | 40 | 0 | 0 | 40 |
| 593 | 64 | 40 | 2 | 0 | 40 |

Tutti i conteggi coincidono con quelli del coordinatore, inclusi i profili mancanti. Tutte le coppie di esempio riportate dalla fonte del confronto appartengono ai cataloghi fisici e rispettano profilo e altezza. Le coppie di un massimo matching non sono necessariamente uniche: il confronto riguarda la cardinalità e l'ammissibilità, non richiede uguaglianza degli hash delle coppie.

Nel caso n=5,D=64, gli 89 archi ammettono un matching di 47 coppie e un cover formato da 33 sorgenti e 14 immagini. Nei casi n=7 e 31 il numero dei profili assenti spiega già il deficit osservato del matching; per n=5,D=16 il vincolo d'altezza elimina tutti gli archi pur lasciando alcuni profili comuni.

I due replay, normale e `-O`, sono identici. Sono conteggi di **parti dispari** con capacità uno costruita dal matching, non una prova di comparazione dei bacini ordinari. L'ottimalità di questi grafi finiti non dimostra una minorazione asintotica di η, non controlla altri cutoff e non elimina il problema dei profili mancanti. I risultati sono stati comunicati al coordinatore prima di ogni ulteriore scelta dei parametri.
