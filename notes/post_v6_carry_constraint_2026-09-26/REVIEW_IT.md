# Revisione interna: vincolo lineare e controesempio al livello 16

26 settembre 2026. Il lavoro matematico e i test sono stati affidati a
due agenti, con implementazione principale separata. Questa è una
revisione interna, non una revisione umana esterna o una verifica Lean.

## Controlli matematici

Il riporto scolastico è il pavimento della convoluzione **troncata**
`F_N`, non del quadrato dell'intero prefisso. La ricostruzione del
termine costante da `C_N(P0)` e `P0² mod2^N` è stata verificata contro
prodotti triangolari su tutti gli ingressi dei piccoli domini.

L'assenza di prodotti fra due bit liberi richiede
`2(r+H)>=r+K`; l'ipotesi usata `K<=2H` la garantisce. I prodotti misti
si contano nei due ordini, da cui il fattore due dei pesi. Il filtro
seleziona una fascia semiaperta di ampiezza `2^N`, con frontiera
superiore stretta. Tutti i bit di sorgente da K in su sono irrilevanti
per il riporto, ma vengono conservati per mantenere l'altezza.

L'intervallo delle ultime B colonne è rigoroso perché il riporto
omesso è compreso fra zero e `max(N-B-1,0)`. La coincidenza dei due
estremi è necessaria per accettare quel blocco come certificato; il
programma aumenta B quando non basta. I test coprono anche il caso
di precisione zero e ingressi con bit alti aggiuntivi.

Le formule inverse delle parole con pochi zeri tengono conto del
numero di zeri già incontrati. Usare per il secondo zero l'esponente
del caso a un solo zero sarebbe errato. Sono state confrontate con
la biezione completa dei residui ottenuta tramite iterazione diretta.
L'inversione quadratica simultanea conserva sia la congruenza della
radice sia quella dell'inverso della derivata alla precisione raddoppiata.

## Test fissato e ordine dei candidati

Il sondaggio ai livelli 5..12 precede il protocollo e ha motivato la
famiglia scelta: non viene presentato come validazione cieca. Gli
agenti non hanno generato candidati al livello 16 prima di congelare
protocollo ed elenco. La ricerca archiviata usa soltanto quel livello.

Il valore inferiore corretto è `H=63074`, ottenuto dal soffitto
intero; è stato fissato prima del salvataggio degli hash e della
generazione dei candidati. Il suffisso ha lunghezza `K-H=63073`.
L'eliminazione dei duplicati preserva l'ordine e dà 988 candidati.
La fase si arresta al primo fallimento: indice zero-based 280,
ossia 281 verifiche. Tutti i 280 record precedenti hanno riporto
diverso dal bersaglio. Il protocollo e l'elenco sono protetti da
digest letterali; il replay rifiuta una loro alterazione.

## Testimone e indipendenza dei controlli

I bit bassi fino a H e quelli da K in su coincidono con `Q_16`.
Ne segue l'intera parola inferiore, che viene comunque riprodotta.
La binade riguarda la **sorgente X**: non si introduce retroattivamente
un vincolo aggiuntivo sullo stato superiore o sugli antenati.

Il riporto richiesto è 31655. Il testimone lo conserva, mentre il
conteggio superiore è 94394 contro 62747 della torre. Il difetto
31168 supera sia il bersaglio 512 sia 2310, il doppio del margine
inferiore. Il calcolo `2*1155-31168=-28858` controlla il bilancio.
La decomposizione ancorata è stata controllata separatamente anche
sul testimone: `C_(K-r)(X)=31653` e il termine di pavimento aggiunge
due, ricostruendo il riporto 31655.

Il programma verifica la parola mediante il motore modulare e poi
con l'iterazione diretta degli interi completi. I test ricostruiscono
anche il riporto con la normalizzazione di tutte le colonne di un
prodotto impacchettato, distinta dal certificato delle sole colonne
finali e dal vincolo lineare. Le cinque piccole fibre vengono
enumerate interamente con convoluzione triangolare e iterazione diretta.
Le tre sorgenti preliminari sono verificate separatamente.

Il replay finale controlla l'ordine fino al primo fallimento e deve
riprodurre il JSON byte per byte. È ripetizione dello stesso programma,
non un ulteriore oracolo matematico. Le quattro sorgenti congelate,
i log e gli hash delle prove e dei programmi sono elencati nel
[manifesto](verification_manifest.json).

## Quantificatori della conclusione

Il controesempio respinge l'implicazione su **tutti i completamenti**
con prefisso, bit alti e singolo riporto futuro uguali a quelli della
sorgente effettiva. Non riguarda i soli punti della torre, non impone
la cascata completa dal seme 3 e non soddisfa per ipotesi ulteriori
condizioni di antenati o congruenze ternarie.

Non è un controesempio a Collatz o al bersaglio sul solo `Q_16`.
Non esclude un certificato diverso che ricavi un bilancio dalla
generazione esatta. Le prove restano su carta, con controlli Python;
nessuna nuova dichiarazione Lean, CI riuscita o build aggregata viene
attribuita a questa fase locale.
