# Analisi 4 — Operatori finiti e ponte analitico

13 novembre 2026. Analisi in sola lettura del repository al commit `5428e89`; nessuna nuova build o scansione numerica pesante. Questa revisione distingue il codice Lean dalle note condizionali storiche.

## Valutazione

Il ramo spettrale conserva una buona libreria di certificazione finita, ma non possiede ancora un operatore infinito identificato con i dati generati e capace di controllare ogni orbita. Prima di rilanciare il programma occorre correggere due inferenze nelle note di chiusura condizionale. Sono problemi delle proposte analitiche, non controesempi ai teoremi Lean esistenti.

## Che cosa è effettivamente provato

- `lean/CollatzShadowing/Bound.lean:356` dimostra che un certificato Collatz–Wielandt per una matrice finita non negativa maggiora il suo raggio spettrale reale. I certificati generati `3/4` e `97/2000` sono applicazioni finite valide. Il certificato K16 usa un alfabeto diverso da `PhaseState`; non si può identificarlo automaticamente con la discretizzazione del ramo A0.
- `lean/CollatzShadowing/WeakBridge.lean:72` prova che la distanza media pesata fra righe controlla l'errore dell'azione su osservabili limitati. È un ponte fra due kernel finiti, non una convergenza.
- `WeakBridge.lean:1116` e `:1141` provano il conteggio e la massa della coda sorgente ad alta valutazione, limitata da `2^-R` nel modello dichiarato.
- `WeakBridge.lean:585`, `:707`, `:811` controllano i bordi di bit length per rami affini/biaffini: fuori dagli attraversamenti di potenze di due, il peso `2^-delta` resta invariato sotto uno shift fissato.
- Gli schemi `LabelSplit.BranchCover` e `BranchPartition` trasferiscono la risoluzione dei rami a sorgenti già coperte. Non costruiscono la copertura infinita concreta.

Lo stato A0 è più avanzato del vecchio master report: `lean/TODO.md:133` registra la risoluzione finita delle etichette per 5.292 righe; `:241` importa una contabilità semantica a cap 100 senza perdite sui 114.240 campioni dichiarati. Rimane una certificazione finita. Inoltre tutti i rami di ritorno osservati sono crescenti coefficiente per coefficiente (`TODO.md:166`): concatenarli soltanto non produce discesa; occorre una transizione a un vero drop o un altro meccanismo.

## Due correzioni necessarie nelle note analitiche

### 1. Differenze consecutive piccole non implicano Cauchy

`notes/phase10_A0_weak_approximation_theorem_2026-05-25.md:169`–185 conclude che gli approssimanti sono Cauchy dalla tendenza a zero del drift `D_N=||K_{2N}-K_N||` e degli altri errori. Questa deduzione non è valida senza un'ipotesi ulteriore.

Controesempio: un solo stato, peso sorgente 1, proiezioni e inclusioni identità, tutti gli altri errori nulli, e kernel substocastico

`K_N = (1 + sin(log(log(N + e)))) / 2`.

Si ha `0≤K_N≤1` e `|K_{2N}-K_N|→0`, perché l'incremento della fase tende a zero. Tuttavia la fase cresce senza limite e attraversa ripetutamente massimi e minimi del seno, dunque `K_N` non converge. Il controesempio persiste lungo le scale diadiche. Un'alternativa ancora più semplice su tali scale è `K_{2^m}=(1+sin(log(m+1)))/2`.

La condizione A0W7 (`:148`) o assume già la convergenza a U, oppure dichiara che il risultato vuole provare Cauchy: nella seconda lettura non fornisce la stima mancante. Inoltre, se `E_N/I_N` cambiano, serve controllare anche la compatibilità fra scale: una stima di `I_N(K_{2N}-K_N)E_N` da sola non stima la differenza dei due approssimanti completi.

Riparazioni possibili: una maggiorazione sommabile `D_{2^m}≤C2^{-alpha m}`, con errori e mappe compatibili; una stima diretta fra qualunque due scale sufficientemente grandi; oppure un vero argomento di convergenza per aspettative condizionali identificate.

### 2. I rappresentanti naturali non campionano ogni funzione misurabile secondo Haar

`notes/phase10_gate10B_conditional_closure.md:445`–451 prova correttamente la formula per una funzione costante sui cilindri fini. Il successivo passaggio `:588` identifica invece le medie puntuali dello script con medie delle aspettative condizionali, mentre la proposizione `:346` richiede soltanto limitatezza e misurabilità.

Controesempio minimo: `g=1_(Z₂\N)`, dove N sono i naturali immersi in Z₂. N è numerabile e ha misura di Haar zero; quindi g ha integrale 1, ma ogni valutazione su un rappresentante naturale è zero. Tutte le medie campionarie dello script sarebbero zero. Lo stesso vale dentro ogni cilindro sorgente.

La condizione B (`:348`) è ambigua: se assume direttamente identità con veri integrali condizionali, il controesempio non la soddisfa, ma proprio quell'identità deve allora essere dimostrata per i generatori. Se significa la media puntuale esplicita del §4, non basta. La proprietà della torre dice inoltre che mediare i veri integrali dei sottocilindri restituisce già l'integrale sul cilindro padre; non autorizza a sostituirli con valori sui rappresentanti.

Occorre imporre cilindricità dopo troncamenti con errore controllato, regolarità sufficiente al campionamento, oppure una stima esplicita di discrepanza. Il progetto già riconosce correttamente un altro limite: `drop below start` e `delta` di bit length non sono osservabili intrinseci di Z₂ (`gate10B_conditional_closure.md:620`).

## Tre direzioni attaccabili

### A. Prima un teorema aritmetico per kernel troncati

Fissare profondità S e cap A. Partizionare esattamente per parola, congruenze delle etichette e disuguaglianze affini; ogni ramo diventa `source=q*u+r`, `target=a*u+b`, con dominio e primo ritorno certificati. Cercare un limite delle medie diadiche del peso `2^-biAffineDelta`, con errore esplicito `C(S,A) log(N)/N` per la parte a rami finiti.

Il primo lemma è il confronto per raddoppio del parametro, `u→2u` e `u→2u+1`: le due forme affini differiscono dalle loro dilatazioni per costanti fisse. I lemmi di attraversamento e `bitLength_two_mul` danno strumenti già disponibili. Non usare invece il bound per shift fissato con `p=N`: il suo costo cresce con N e non prova il decadimento desiderato.

Primo esperimento: scegliere una piccola famiglia di rami già estratta, dimostrarne il dominio completo e confrontare esattamente l'errore del raddoppio con il bound dei bordi. Arresto: nessun progresso se la prova usa soltanto rappresentanti o se il primo ritorno non è certificato su tutto il ramo. Questo darebbe un risultato limitato ma autentico prima di affrontare le code.

### B. Spazio simbolico numerabile e operatore di rinnovo killed

Usare come stato la parola/esposizione del ritorno e un contatore di profondità, invece di comprimere subito a `PhaseState`. Tenere drop e budget come esiti distinti. Obiettivo: per ogni soglia sorgente R, dimostrare un controllo uniforme della massa dei percorsi ancora irrisolti dopo S e della coda delle valutazioni intermedie.

Primo lemma da cercare: `lim_{S→∞} limsup_N mass_N(unresolved after S; v2<R)=0`, senza assumere Collatz. Test iniziale: tassonomia esatta di una famiglia a durata arbitraria usando le torri note, per vedere se si può sommare una coda con pesi che non nascondano gli stessi percorsi.

Arresto: se il bound usa la terminazione, o se si passa da una media a un singolo percorso, il problema è soltanto rinominato. Anche ottenere questo controllo più A non fornirebbe ancora un gap spettrale né l'esclusione puntuale delle eccezioni.

### C. Modello aritmetico con scala reale e certificati parametrici

Per riprodurre fedelmente il killing, conservare scala/altezza oltre ai residui: ad esempio una coordinata reale normalizzata insieme a una classe 2-adica e a una parola finita. La misura deve provenire dagli effettivi interi campionati; non assumere indipendenza fra mantissa e residui. In alternativa usare direttamente domini affini interi e una relazione deterministica sui parametri, senza postulare un operatore probabilistico.

Primo obiettivo: un certificato verificabile che collega due macro, include espansione iniziale e successivo drop, e fornisce diminuzione di un parametro ben fondato per un'intera famiglia infinita. I ritorni soltanto espansivi già archiviati sono un test negativo obbligatorio.

Arresto: se per ogni estensione il numero di parametri cresce senza una formula di compressione, oppure il rango equivale nuovamente alla conclusione senza lemma strutturale, fermare la sintesi. Questa via è meno elegante analiticamente, ma rispetta l'ordine naturale e può produrre risultati parametrici finiti senza aspettare l'intero ponte funzionale.

## Decisione

Priorità immediata ad A e alla correzione dei due schemi di convergenza. B resta ad alto rischio; C è una strada per risultati circoscritti. Il risultato H.2 di settembre chiude un particolare trasporto fra bacini, ma non risolve questi obblighi spettrali. Nessuna delle tre proposte è al momento un nuovo teorema globale.
