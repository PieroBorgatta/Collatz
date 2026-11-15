# Ricerca Collatz integrazioni e prosecuzione

13 novembre 2026. **Ricerca dalle 16:32:23 alle 17:32:38 Europe/Rome: 60 minuti e 15 secondi.** Dopo questa soglia sono state fermate le nuove esplorazioni e sono stati raccolti risultati e verifiche. Quindici agenti distinti hanno lavorato in gruppi paralleli, con scambi diretti; la piattaforma consente tre agenti operativi oltre al coordinatore. [Incarichi e confronti](AGENTI_IT.md), [protocollo](PROTOCOL_IT.md).

Il risultato più utile è un collegamento quantitativo fra **sparsezza di segmenti finiti e altezza dei trasporti**. Per le trasformazioni che conservano lunghezza e somma degli esponenti, otteniamo su carta un limite universale d'altezza. Per una famiglia di modifiche di due esponenti abbiamo anche un controllo del carico delle immagini. Il problema principale di questa strategia diventa la **quota relativa di massa η**, che non è stata dimostrata. H rimane aperta e il problema dei cicli non banali resta distinto.

Sono stati integrati **10 moduli Lean con 69 dichiarazioni pubbliche**, verificati dalla build completa e da un audit stretto di tutte le nuove radici. Sono dichiarazioni finite, parametriche o condizionali; non 69 scoperte indipendenti. Il limite universale di sparsezza e le sue conseguenze analitiche restano prove su carta, chiaramente separate dal codice.

**Decisione sulla v7:** il materiale basta per iniziare ora una versione tecnica coerente. Il deposito non è ancora pronto: occorre scrivere il manoscritto completo e prepararne PDF e supplemento. Non serve attendere una prova di H o di Collatz per giustificare questa versione. [Ambito, titolo, abstract e indice proposti](V7_OUTLINE_IT.md).

## Che cosa è stato preso dalle nuove fonti

| Fonte e meccanismo | Integrazione locale | Confine conservato |
|---|---|---|
| [Shaik, sorgenti sui pool e sulle capacità](https://github.com/shaikidris/CollatzConvergencePositiveDensity), commit `f0fda887ee60dc8ac4ef0d864935148b03734726` | Prove locali del carico reciproco dei pool non ricorrenti e dell'allocazione a soglia | Nessuna importazione della catena analitica esterna o della sua conclusione di densità |
| [rStation paper 10 v3](https://rstation.ai/problems/collatz/papers/10), dizionario fra atomi congiunti e predecessori | Congruenza ternaria, positività automatica, parole esatte e conteggio delle sorgenti distinte | La conclusione Syracuse richiede target dispari; nessuna stima di mixing acquisita |
| [Curry, conteggio quantitativo per finestre](https://doi.org/10.5281/zenodo.22087163), con attribuzione al metodo Garcia–Tal | Estensione su carta ai segmenti finiti iniettivi e conseguente limite d'altezza; adattatore finito astratto in Lean | La stima entropica completa, B e D₀ non sono formalizzati; nessuna certificazione di priorità assoluta |

Le fonti Shaik usano un toolchain diverso: sono state lette e attribuite, poi i meccanismi scelti sono stati dimostrati nel progetto locale. Una selezione di sorgenti è archiviata con licenze, avvisi e hash; non è una nuova dipendenza eseguibile. Il PDF primario Curry è stato letto e controllato visivamente, con provenienza e hash registrati, senza ripubblicarlo nel repository. [Relazione sulle fonti](agents/S01_WEB_IT.md).

Nel dizionario rStation è stata precisata una restrizione di dominio: il Lemma 3.1 stampato per target positivo arbitrario non dà una conclusione Syracuse per target pari. Il caso a=2, k=A=1 produce una sorgente shortcut ma non `S(x)=2`. Questo rilievo non contesta il successivo uso del lemma su target dispari.

## Il nuovo controllo d'altezza

Sia `z_j=T^j(u)`, per `0≤j≤L`, un segmento shortcut senza ripetizioni. Per una finestra di ampiezza X≥2, poniamo `N=floor(log₂X)`. Sul prefisso che esclude gli ultimi N punti, T^N è iniettiva: un'uguaglianza di immagini sarebbe una ripetizione fra indici ancora dentro il segmento. Il bordo temporale costa al più N punti.

La prova primaria del conteggio per finestre richiede soltanto questa iniettività al tempo N. Si ottiene quindi, scegliendo i parametri razionali indicati nella prova, per la banda `[2^j,2^(j+1))`,

`numero di punti ≤ j+12(j+1)2^(49j/50)`.

Sommando i reciproci sulle bande:

`Σ_(x nel segmento) 1/x ≤ B`,

`B=12/(1−2^(−1/50))²−9 < 120000`.

La costante è indipendente da sorgente, bersaglio e lunghezza. È volutamente molto grossolana. Un primo arrivo a un bersaglio positivo dà un segmento iniettivo; il nonritorno del target, previsto nel dominio H, è sufficiente ma non necessario.

Per una parola Syracuse effettiva da u a n, di lunghezza k e totale A,

`P=Π_(j<k)(1+1/(3n_j))=2^A n/(3^k u) ≤ exp(B/3)`.

Se una nuova parola effettiva da v a y conserva gli stessi k,A, la sua costante affine non negativa dà

`v ≤ (y/n)P·u`.

Per il fratello canonico `y≤16n+5≤21n`, segue

**`v ≤ D₀u`, con `D₀=21 exp(B/3)` universale.**

È una conseguenza condizionata all'esistenza di una vera parola superiore con lo stesso profilo, non una costruzione di tale parola. Non contraddice le precedenti ostruzioni al trasporto: alcune sorgenti non ammettono il profilo richiesto e una comparazione di massa deve trattare i profili mancanti. H.2 riguarda invece modifiche del totale A attraverso l'ultimo esponente.

S10 e S12 hanno controllato separatamente la prova e i quantificatori sulla fonte primaria. Il codice `FiniteOrbitTransfer` formalizza il solo adattatore finito, con il conteggio numerico come ipotesi esplicita. [Prova e costanti](agents/S10_SPARSE_IT.md), [revisione avversa](agents/S12_ADVERSARIAL_IT.md).

## Carico delle immagini e limite dei piccoli cambiamenti

La modifica bilanciata di due esponenti impone una congruenza che confina la posizione modificata vicino al termine quando lo shift è limitato. La parte aritmetica positiva è formalizzata in `WordSurgery`; il conteggio completo del carico è su carta.

Per un insieme finito di shift δ e target superiore y senza ritorni, ogni immagine determina un'unica parola modificata. Per ogni δ vi sono al più Q_δ posizioni possibili. Ne segue `M_odd≤ΣQ_δ`, indipendente dal cutoff. Il costo è O(1+log n) per shift limitati.

Il controllo finale del coordinatore e di S06 estende il conteggio a cataloghi finiti con tutti gli shift, usando pesi `2^(−|δ|)`:

`M ≤ 2log₃(max(n,y))+4log₃2`.

Le etichette duplicate devono essere identificate o condividere il loro coefficiente. Preservare il fattore diadico nell'immagine conserva il carico. La coda dei grandi shift è però uniformemente sommabile: questa pesatura non aggirerebbe una futura prova che ogni shift fissato trasferisce massa asintoticamente nulla. Non è stata ottenuta η.

Il censimento S06, congelato prima dei calcoli, ha esaminato **3.137.835 modifiche** e trovato **368 trasporti**, tutti osservati a profondità al più 7. È un risultato finito, non un limite generale della profondità. Inoltre `16853` e `16867` producono la stessa immagine `270021` verso `9493`: presumere carico uno prima della selezione sarebbe falso. [Dettagli e appendice pesata](agents/S06_SURGERY_IT.md).

## Un'alternativa concreta con intere parole

Il coordinatore ha costruito una relazione più ampia: cambiare tutta la parola conservando solo il profilo `(k,A)`. A ciascun profilo si associano le sorgenti reali dei due bacini; un matching con vincolo `v≤Du` seleziona immagini distinte con carico uno. I parametri n, X e D sono stati fissati prima del calcolo.

S13 ha controllato otto casi con un algoritmo indipendente a cammini aumentanti e un vertex cover di cardinalità uguale al matching. Il risultato non dipende quindi dal solo greedy del coordinatore. Tutti i replay normali e ottimizzati coincidono.

Preservando `2^e u→2^e v`, lo stesso matching dà un accoppiamento di inizi ordinari. Occorre pesare ogni parte dispari con il numero dei suoi fattori di due ammessi. A X=4096 e D=64:

| Target n | Fratello y | Inizi ordinari di base | Inizi ordinari accoppiati |
|---:|---:|---:|---:|
| 5 | 85 | 3839 | 1842 |
| 7 | 29 | 731 | 702 |
| 31 | 125 | 373 | 341 |
| 593 | 9493 | 1343 | 4 |

Il caso 593/9493 resta fortemente sbilanciato. Queste cifre non sono densità certificate, non provano uniformità e non confutano H. Mostrano una costruzione finita effettiva e rendono visibili i profili mancanti. Il prossimo lemma deve comparare **la capacità dei profili rispetto alla massa effettiva di base**, oppure cambiare anche profilo o profondità. [Protocollo, prove del matching e passaggio ordinario](PROFILE_TRANSPORT_IT.md).

## Ritorni e un caso positivo di convergenza

`ReturnBlocks` dimostra ora in Lean che, per ogni r, esiste una sorgente con r veri primi ritorni consecutivi alla sezione, tutti crescenti. È un'ostruzione a ogni ricerca che fissi il numero dei ritorni entro cui deve avvenire la discesa; non costruisce un'orbita infinita crescente.

S07 ha trovato un raccordo esplicito con parola finale `[3,1,2]`. Il clock della macro può aumentare arbitrariamente, anche mantenendosi uguale mentre il valore cresce. Un autoarco del quoziente dei clock non è un ciclo reale: ripeterlo richiede nuove congruenze.

Su quel ramo, con parametro libero j, il nuovo quoziente ha forma `q_j=q₀+bj`, con q₀,b positivi e b dispari. Il clock è `floor(ν₂(q_j)/3)`. La coda clock≥R seleziona una sola classe modulo `8^R`. Per un osservabile limitato da M, la sua media su U parametri converge alla miscela geometrica con errore

`≤4M/8^R+2M(8^R+1)/U`,

e, scegliendo la soglia, `≤36M/√U`. Questo tasso è sommabile sulle scale diadiche.

È un vero esempio limitato di troncamento, coda e convergenza, controllato su carta e con replay indipendenti. Non riguarda tutte le righe del kernel o i parametri visitati da una singola orbita. I due vecchi schemi analitici sono stati corretti: drift successivo tendente a zero non implica Cauchy; sola misurabilità non identifica campioni naturali e integrali Haar. Gate 10.B rimane aperto. [Raccordo](agents/S07_MACRO_IT.md), [correzioni e prova del clock](agents/S11_KERNEL_IT.md).

## Integrazione Lean e verifica effettiva

| Modulo nuovo | Dichiarazioni pubbliche | Contenuto |
|---|---:|---|
| `RootPoolBudget` | 12 | Budget dissipativo condiviso e carico reciproco per pool non ricorrenti |
| `SiblingPool` | 8 | Pool dei fratelli laterali e specializzazione canonica |
| `JointAtomDictionary` | 10 | Sorgenti esatte, congruenze, cutoff e conteggi senza duplicazione |
| `AffinePositivity` | 5 | Positività automatica e dizionario completo a target dispari |
| `CapacityAllocation` | 7 | Certificati finiti a soglia; massa inferiore esplicitamente assunta |
| `RelativeMassFlow` | 6 | Costo altezza/carico/massa e budget di blocchi disgiunti |
| `ReturnBlocks` | 8 | Arbitrariamente molti primi ritorni crescenti |
| `WordSurgery` | 4 | Identità e vincolo di profondità terminale |
| `CycleRotation` | 6 | Identità di rotazione e invarianza del sieve di divisibilità |
| `FiniteOrbitTransfer` | 3 | Troncamento finito per applicare stime di iniettività |

La build integrata è riuscita: **3393 passaggi, exit 0**. Tutte le **69 radici** sono passate nell'audit stretto con soli `propext`, `Classical.choice`, `Quot.sound`. Nessun nuovo `native_decide`, placeholder o assioma di progetto. Restano quattro segnalazioni non bloccanti: una precedente ipotesi inutilizzata, due istanze decidibili ridondanti e un suggerimento di semplificazione.

La verifica usa Lean/Mathlib 4.29.1 con dipendenze compilate già installate. Non è un rebuild freddo o un replay tramite kernel indipendente; l'overlay analitico separato non è stato ricompilato. Sorgenti e hash sono rimasti invariati durante build e audit.

Il workflow CI è stato esteso all'audit delle 69 radici e ai replay indipendenti. Gli stessi comandi sono verificati localmente; non è stato avviato un nuovo run CI remoto.

I nuovi moduli aggiungono 1279 righe, più dieci import. La libreria conta ora 79 file e 58.001 righe, distinguendo 53 file d'autore assistiti da AI da 26 certificati generati invariati. Le dichiarazioni sono un conteggio testuale, non una misura della distanza da una soluzione.

[Build e ricevuta](verification/integration_receipt.json), [audit completo](verification/s14_receipt.json), [indice delle dichiarazioni](../../lean/CollatzShadowing/THEOREM_INDEX.md), [manifest finale](verification_manifest.json).

## La prosecuzione giustificata

Per questa strategia, il criterio è `D·M/η≤C(1+log n)`. Il controllo d'altezza D è disponibile su carta per stessi k,A; il carico M è controllato per le costruzioni precisate. Nessuno dei due fornisce una minorazione di η.

Il prossimo lavoro matematico dovrebbe essere un **lemma di confronto relativo fra cataloghi fisici di profili**, con insiemi, errori, altezza e carico dichiarati. I casi mancanti devono comparire nell'enunciato. Il confronto aggregato fra blocchi di fratelli resta una variante ammissibile, con costi uniformi o coefficienti netti non sommabili, ma non è una scorciatoia già provata.

Prima di investire in altre scansioni, conviene tentare di confutare la massa della surgery limitata: una prova di sparsezza per ogni shift fissato chiuderebbe anche la versione con pesi sommabili. In tal caso la ricerca va spostata alle intere parole, ai profili o a profondità diverse, non a shift sempre più grandi dello stesso modello.

La formalizzazione del conteggio per finestre e del limite B è un compito di consolidamento concreto; non sostituisce il nuovo confronto di massa. Il caso del clock offre un modello corretto per studiare rami troncati, ma il kernel completo richiede ancora controllo dei cofattori, delle etichette e delle sorgenti non assegnate. I cicli positivi non banali continuano a richiedere un argomento separato.

## Decisione sulla versione 7

**Preparare la v7 ora è giustificato; depositarla adesso sarebbe prematuro.** Il contenuto post-v6 e il nuovo ponte d'altezza bastano per una continuazione tecnica. Il nucleo proposto è *Finite Orbit Budgets and Predecessor Transport in Syracuse Dynamics*, centrato su altezza, carico e massa relativa.

Le verifiche locali di build e assiomi sono ormai completate. Restano da scrivere il manoscritto v7 e le prove autonome dei risultati centrali, distinguere F/C/E/H accanto agli enunciati, compilare e controllare il PDF e preparare il supplemento dello stesso snapshot. Non è necessario aspettare H, una formalizzazione totale di B o una soluzione di Collatz; è necessario descrivere correttamente ciò che è provato.

Le idee di pool e allocazione vanno attribuite alle fonti; la sparsezza al metodo classico e alla prova quantitativa consultata. Non è stata certificata priorità assoluta del corollario d'altezza. Una revisione specialistica esterna e una replica con toolchain recente sono raccomandazioni per rafforzare il lavoro, non nuove autorizzazioni obbligatorie.

[Valutazione dettagliata](agents/S15_V7_IT.md), [titolo, abstract e indice](V7_OUTLINE_IT.md). Nessun PDF pubblicato, dipendenza fissata, nuovo livello della torre o deposito esterno è stato modificato.
