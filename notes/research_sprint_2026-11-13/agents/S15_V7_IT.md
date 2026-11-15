# S15 Valutazione della prossima versione del paper

13 novembre 2026. Confronto del PDF v6 e del suo sorgente con i risultati post-v6 di settembre e con le integrazioni della sessione attuale. Non sono stati modificati i PDF pubblicati, predisposti depositi o avviati contatti esterni.

## Decisione

**Il materiale è sufficiente per preparare ora una v7 tecnica. Il deposito non è ancora pronto.** Non serve attendere una prova di H, una discesa universale o una nuova scoperta globale per giustificare la versione: esistono risultati post-v6 sostanziali, un collegamento nuovo fra sparsezza finita e costo d'altezza, strumenti formali riutilizzabili e limiti dimostrati dei metodi precedenti. Prima del deposito occorrono però il manoscritto v7 effettivo, le prove complete dei risultati centrali e un fascicolo di verifica riferito allo stesso snapshot.

La raccomandazione è iniziare la stesura con il perimetro nell'[outline](../V7_OUTLINE_IT.md). Presentarla come consolidamento matematico e formale del programma di trasporto. Non presentarla come prova parziale che renda prossima la soluzione di Collatz: la minorazione relativa di massa η rimane aperta e i cicli non banali sono un problema distinto.

## Perché una nuova versione è giustificata

La v6 del 24 settembre è centrata su cilindri esatti, tassa di precisione di una parola, switching, singolarità della codifica e vincoli sui cicli. Non contiene il successivo nucleo su sezione marcata, occupazione pesata, confronto dei bacini e ostruzioni H.1/H.2. Il nuovo contenuto non è quindi soltanto un aggiornamento bibliografico.

Il nucleo più coerente per la v7 è la separazione dei tre costi del trasporto:

1. **Altezza.** La deduzione S10 estende il conteggio di sparsezza a segmenti finiti iniettivi, con un bordo temporale esplicito. Ne segue un limite universale al prodotto affine e quindi all'altezza per trasformazioni che conservano lunghezza k e totale A. La deduzione è su carta, controllata da S12, non interamente in Lean.
2. **Carico delle immagini.** I pool non ricorrenti permettono un budget reciproco forte, ora provato localmente e collegato ai fratelli laterali. Per la surgery a shift finiti, S06/S12 danno inoltre un limite su carta del numero di sorgenti per immagine. Le collisioni fisiche mostrano perché il carico 1 sarebbe falso.
3. **Quota relativa η.** La conversione finita da massa e carico a conteggi è formalizzata, ma non è stata costruita la massa relativa richiesta. Esporre questo obbligo rimasto aperto è il punto scientifico della prosecuzione.

H.2 fornisce il risultato negativo complementare: tutte le correzioni del solo ultimo esponente hanno immagine o(X) entro una dilatazione fissa. È più informativo di un algoritmo che non ha trovato successi; il teorema asintotico resta su carta, con supporto aritmetico Lean.

Il ramo dei ritorni aggiunge un'ostruzione parametrica rigorosa: arbitrariamente molti primi ritorni consecutivi crescenti. Il raccordo S07 e la legge del clock S11 offrono poi un esempio limitato ma positivo di coda controllata e convergenza con errore sommabile. Questi risultati possono sostenere una sezione applicativa o un'appendice, senza sovraccaricare la tesi principale del paper.

## Priorità e attribuzioni

La sufficienza della sezione `20 mod27` è classica e va attribuita a Monks et al.; il contributo locale è il certificato e il collegamento agli episodi. I cilindri non diventano nuovi perché riscritti nel nuovo dizionario. Il criterio dei pool deriva dal meccanismo di Shaik e deve essere citato al commit fissato; la nuova prova locale e il collegamento ai fratelli sono l'integrazione del progetto. L'allocazione a soglia è un argomento finito di dualità/capacità, non una nuova teoria di ottimizzazione.

La sparsezza deriva dal meccanismo Garcia–Tal e dalla prova quantitativa di Curry letta direttamente. La finitezza dei segmenti, il costo del bordo e la conseguenza per il trasporto costituiscono qui una deduzione esplicita; questa sessione non certifica priorità assoluta del corollario. Il lemma del clock è aritmetica di progressioni e troncamento: il suo interesse è l'applicazione dichiarata al ramo, non una nuova legge statistica delle orbite.

La v7 deve citare queste provenienze accanto ai relativi enunciati. Il numero di moduli o di dichiarazioni non è un conteggio di scoperte indipendenti. La catena analitica esterna di densità non è stata importata dalla nuova integrazione finita e non va presentata come una nuova premessa acquisita implicitamente.

Il paragrafo bibliografico della v6 su Shaik descrive una fotografia precedente: la v7 deve sostituirlo con l'esatto ambito della fonte oggi fissata, senza trasformare controlli locali dichiarati in verifiche indipendenti completate. Per Hercher va citato anche il corrigendum del 14 giugno 2026. Date del manoscritto, commit e segnalazione pubblica devono rimanere distinte.

## Cosa manca concretamente prima del deposito

- Scrivere un manoscritto coerente, con prove autonome del lemma finito di sparsezza, delle conseguenze B e D₀, del carico a shift finiti e del lemma del clock. I rapporti degli agenti sono materiale preparatorio, non il manoscritto da depositare.
- Conservare la distinzione **F/C/E/H** per ogni risultato: F per dichiarazioni Lean elaborate e verificate nello snapshot finale; C per prove su carta; E per controlli esatti finiti; H per ipotesi aperte. Il solo adattatore `FiniteOrbitTransfer` non formalizza B o D₀.
- Completare build integrata, audit degli assiomi e associazione fra sorgenti, enunciati citati, log e hash dello stesso snapshot. Alla lettura S15 questi controlli finali erano ancora in corso; il loro esito viene registrato nel bilancio del coordinatore.
- Preparare e controllare il nuovo PDF, bibliografia, supplemento e manifest. La v6 resta immutata; la nuova versione deve descrivere esplicitamente il cambio di ambito.

La migrazione a un toolchain recente e una revisione specialistica esterna sono raccomandazioni utili per rafforzare la verifica e la credibilità. Non sono requisiti di autorizzazione introdotti da questa analisi, né si afferma che senza formalizzazione completa dei risultati C sia impossibile pubblicare un paper matematico. È necessario dichiarare con precisione il confine effettivamente raggiunto.

## Confronto fra agenti e verifica dello stato

S13 ha confermato senza mismatch i replay indipendenti di surgery, collisioni, macro, code del clock e troncamenti. Ha precisato che tali test non dimostrano B, D₀ o H. S14 ha completato la revisione semantica dei dieci moduli senza errori materiali e preparato l'audit delle nuove radici; l'audit completo dipende dal completamento della build integrata in corso. S12 ha controllato direttamente le due deduzioni su carta e le restrizioni della fonte rStation.

Il prossimo passo editoriale giustificato è dunque **scrivere la v7 a questo perimetro e chiudere il fascicolo di verifica**, non attendere indefinitamente la soluzione della congettura. Il prossimo passo matematico resta trovare o escludere una minorazione relativa η per una costruzione esatta dichiarata.
