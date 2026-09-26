# Rinnovo della precisione: un limite ottimale per i certificati di prefisso

**26 settembre 2026.** Abbiamo sottoposto a un controllo preciso il
[certificato congiunto a blocchi proposto](../post_v6_tail_2026-09-25/NEXT_RESEARCH_IT.md).
Conservare soltanto il prefisso binario dell'input e la relazione
quadratica esatta lascia una libertà di completamento che si può
misurare completamente. Ne segue una regola di arresto ottimale per
questa classe di certificati. Sui dati già noti, al livello 23 essa
richiede il **99,9064% della precisione dell'orizzonte superiore**.

Questo è un limite del modello di informazione scelto, non un limite
generale ai metodi per Collatz. Le proprietà aritmetiche che definiscono
esattamente la torre possono escludere i completamenti avversari: lo
abbiamo controllato esplicitamente. Nessuna nuova discesa uniforme né
priorità matematica viene rivendicata; le prove sono su carta.

## Un massimo esatto, non una stima probabilistica

Siano `H=H_v`, `K=H_(v+1)`, `j_L=J_(Q_v)(H)` e
`f_v(x)=x+2^(v+2)x²`. Supponiamo di conoscere `Q_v mod2^M`, con
`H≤M≤K`, e di richiedere sempre che il secondo input sia `f_v(x)`.
Le prime `H` parità inferiori e le prime `M` superiori sono fissate.

La [prova completa](PROOF_IT.md) mostra che le restanti `K−M` parità
superiori sono **tutte liberamente realizzabili**, una volta ciascuna
fra le classi compatibili modulo `2^K`. Se `Z_U(M)` è il numero di
zeri già osservati nella parola superiore, il massimo difetto è

\[
 \boxed{\Delta_{\max}(M)=K-2j_L-Z_U(M).}
\]

Quindi un certificato valido per tutti gli input che condividono quei
dati garantisce `Δ≤g` se e soltanto se

\[
                 Z_U(M)\ge K-2j_L-g.
\]

La regola usa soltanto gli zeri osservati e il conteggio inferiore già
noto. Non assume indipendenza casuale e non richiede il valore futuro
di `Δ`. Ogni prefisso insufficiente ammette un completamento superiore
di soli uno che viola il limite. La molteplicità di ciascun peso del
suffisso è esattamente un coefficiente binomiale: è un conteggio delle
classi compatibili, non una probabilità attribuita a `Q_v`.

## Quanto costa sui livelli già studiati

Abbiamo mantenuto invariata la candidata precedente
`g(v)=2·2^ceil(v/2)`, proposta uniformemente da `v=16`.
Per ogni coppia `v=5..23` il probe calcola la precisione minima `M_*`
che rende valido il certificato. Per `v<16` l'applicazione della stessa
formula è solo diagnostica; non sposta l'ancora del criterio pesato.

| `v` | `Δ` effettivo | `g(v)` | `K` | Precisione minima `M_*` | Bit ancora non esposti |
|---:|---:|---:|---:|---:|---:|
| 16 | −479 | 512 | 126.147 | 124.179 | 1.968 |
| 17 | 875 | 1.024 | 252.293 | 251.946 | 347 |
| 18 | −1.106 | 1.024 | 504.585 | 500.225 | 4.360 |
| 19 | 1.219 | 2.048 | 1.009.169 | 1.007.489 | 1.680 |
| 20 | 23 | 2.048 | 2.018.338 | 2.014.173 | 4.165 |
| 21 | 1.657 | 4.096 | 4.036.675 | 4.031.733 | 4.942 |
| 22 | −1.845 | 4.096 | 8.073.350 | 8.061.409 | 11.941 |
| 23 | 722 | 8.192 | 16.146.700 | 16.131.588 | 15.112 |

La percentuale riguarda `M_*/K`, non la lunghezza dell'intero `Q_v`.
È un risultato finito: non è dimostrato che `M_*=K−O(g(v))`
uniformemente. Un lungo suffisso di soli uno, per esempio, non
richiederebbe la stessa esposizione di bit secondo questo criterio.

Il [JSON](renewal_results.json) registra il massimo alla soglia e
un bit prima. In tutte le 19 coppie la soglia supera `H`; un bit
prima il massimo è precisamente `g+1`, mentre alla soglia è `g`.
Questa verifica misura l'ottimalità rispetto all'informazione esposta.

## Il rinnovo locale non è gratuito

Nel confronto a tempi `(t,2t)`, la sorgente superiore è
`WW=2f_v(x)`: il suo primo passo è pari. Per `t≥1`, conoscere entrambe
le storie equivale a conoscere `x mod2^(2t−1)`. Per prevedere
esattamente il prossimo blocco inferiore di `b` passi e quello superiore
di `2b` passi occorrono, nel caso peggiore, **`2b` nuovi bit**.

Se `b≤t−1`, il prossimo blocco inferiore è già determinato dal passato
superiore, ma il nuovo blocco superiore resta del tutto libero. Il
coupling quadratico non rifornisce automaticamente la precisione.
Il probe costruisce tre testimoni che preservano entrambi i passati e
il prossimo blocco inferiore, raggiungendo esattamente i massimi del
premio congiunto: `2`, `2` e `8` per i tre esempi archiviati.
Non sono cicli di un'orbita della torre e non vengono presentati come tali.

Abbiamo costruito anche tre cammini finiti che diventano un **self-loop
nella proiezione sui due residui modulo `2^k`**. Lo stato proiettato
resta `(0,2^k−1)` per rispettivamente 8, 16 e 64 passi congiunti;
ciascun passo ha premio `+2`. I premi complessivi sono 16, 32 e 128.
Questi cammini conservano i primi `v+3` bit della sorgente effettiva,
la binade e la relazione quadratica, e cadono entro gli orizzonti scelti.
Non conservano l'intera parola inferiore di lunghezza `H_v`.

Un potenziale dei **soli due residui**, valido per tutte queste sorgenti,
ha differenza nulla sul self-loop e deve quindi pagare un costo almeno
due per passo. Ciò esclude un certificato senza tale costo su quella
proiezione. Non esclude potenziali con altri dati, vincoli di sorgente
più selettivi o compensazioni negli altri blocchi. Non prova che i tre
difetti complessivi superino `g(v)`. Il ciclo è della proiezione:
non abbiamo trovato un ciclo numerico di Collatz.

Un controllo separato osserva un singolo passaggio dello stesso tipo
anche nella sorgente effettiva `Q_5`: ai tempi inferiori 18 e 19,
corrispondenti ai tempi superiori 36 e 38, la coppia resta `(0,1)`
modulo due e il premio è `+2`. I due stati interi sono diversi e sono
archiviati nel JSON. È un ostacolo locale per un potenziale dei soli
due bit senza costo; non una violazione del budget totale, che può
compensare il premio in altri intervalli. Questo controllo usa l'orbita
diretta di `Q_5`, non la costruzione dei tre testimoni alternativi.

## I testimoni non sono punti della torre

Per `v=5..12`, abbiamo costruito otto interi positivi `X≠Q_v`, un bit
prima della soglia minima. Ciascuno conserva:

- tutti i bit inferiori già esposti e tutti i bit da `K` in su;
- la binade di `Q_v` e l'intera parola inferiore di lunghezza `H`;
- la relazione superiore esatta `Y=f_v(X)`.

Il loro difetto è `g(v)+1`. Gli interi sono archiviati esattamente in
esadecimale e verificati per iterazione elementare indipendente.

**Tutti e otto falliscono già il test di un antenato intero positivo.**
Questo controllo è decisivo per interpretare correttamente il risultato:
la [rigidità dimostrata nella fase degli antenati](../post_v6_ancestry_2026-09-25/RESULTS_IT.md)
assicura che due antenati interi positivi, la binade corretta e la parola
inferiore effettiva identificano `Q_v`. Questi vincoli aggiuntivi non
appartengono alla classe di informazione del limite sui prefissi.
L'unicità così ottenuta non maggiora però il peso della parola superiore.

## Verifiche e rapporto con i risultati precedenti

Il [programma](renewal_probe.py) riproduce 20 livelli storici `v=5..24`,
per **32.293.380 passi** complessivi e 19 confronti. Tutti i conteggi e
gli hash delle parole complete coincidono con il risultato congelato
della fase dei margini. Non sono nuove verifiche di livelli successivi
al 24. Il motore delle tracce e l'inversione affine sono riusati dagli
input congelati; la riproduzione non è una nuova implementazione
indipendente di quei motori.

I [14 test](test_renewal.py) verificano invece le nuove formule contro
l'enumerazione completa di piccoli cilindri, l'iterazione intera
elementare, i conteggi binomiali e i testimoni degli estremi. La
[revisione interna](REVIEW_IT.md) separa esplicitamente i quantificatori.

Le biezioni dei residui e dei codici di parità sono classiche; le
formule affini e il ruolo della parola di parità sono anche discussi
in [Rozier–Terracol, versione del 17 maggio 2026](https://arxiv.org/html/2502.00948v5).
La specializzazione qui dimostrata è un'analisi del modello di
certificato del progetto; non la attribuiamo a quel lavoro e non
ne rivendichiamo priorità indipendente.

Dalla radice del repository:

```sh
python3 notes/post_v6_renewal_2026-09-26/test_renewal.py
python3 notes/post_v6_renewal_2026-09-26/renewal_probe.py --output /tmp/renewal_results.json
cmp notes/post_v6_renewal_2026-09-26/renewal_results.json /tmp/renewal_results.json
```

La CI dedicata ripete test e produzione del JSON; l'evidenza verrà
archiviata dopo il push. Nessuna dichiarazione Lean viene aggiunta.

## Decisione per il tentativo successivo

Un potenziale costruito soltanto sul prefisso esposto, con rinnovo
libero dei bit restanti, deve pagare il massimo appena dimostrato.
I dati non sostengono questa scelta come scorciatoia verso un
certificato a bassa precisione.

La strada rimasta è incorporare un vincolo aritmetico che escluda
provabilmente i completamenti sfavorevoli, e poi ricavarne una
disuguaglianza sul peso. Il test degli antenati fornisce una selezione
reale; la sua sola capacità di identificare `Q_v` non fornisce ancora
quella disuguaglianza. Prima di ulteriori grandi simulazioni, il
prossimo criterio deve dimostrare questo passaggio quantitativo.
