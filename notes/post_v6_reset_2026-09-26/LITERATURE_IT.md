# Collatz: letteratura, verifica delle pretese e direzione dopo i filtri

**Ricerca eseguita il 26 settembre 2026.** Fonti primarie consultate nuovamente sul web; lettura mirata degli enunciati e dei passaggi pertinenti, non revisione integrale di ogni articolo. Sono state lette anche le rassegne locali del 24–25 settembre e le sezioni di ambito/priorità del paper v6. Questa ricognizione non certifica completezza bibliografica, priorità assoluta o accettazione indipendente delle formalizzazioni esterne.

**Esito:** non è emersa una prova verificata della congettura, né una stima pubblicata che controlli tutte le parità della famiglia esatta `Q_v=(9^(2^v)−1)/2^(v+3)`. Ci sono risultati recenti utili, ma riguardano quantificatori diversi. Un ingresso matematico più promettente per cambiare domanda è la sparsezza dei **valori di una singola orbita divergente**, che consente di controllare la correzione reale cumulativa. Non risolve il raccordo fra fase reale e aritmetica 2-adica. Almeno una pretesa strutturale del grande preprint di Chang è inoltre incompatibile con un controesempio esplicito descritto sotto.

## 1. Risultati e loro ambito esatto

Nella tabella, “preprint” non significa falso e “pubblicato” non sostituisce il controllo dell'enunciato. Le tre mappe da distinguere sono la mappa ordinaria `Col`, quella abbreviata `T(n)=n/2` oppure `(3n+1)/2`, e quella dispari-dispari `S(n)=(3n+1)/2^ν₂(3n+1)`.

| Fonte primaria e stato verificato | Enunciato utile | Limite per il progetto |
|---|---|---|
| [Tao, arXiv:1909.03562v7](https://arxiv.org/abs/1909.03562v7); *Forum Math. Pi* 10 (2022), e12. Ultima revisione 16 luglio 2026. | Teorema 1.3: per ogni `f(n)→∞`, il minimo dell'orbita è sotto `f(n)` per quasi tutti gli inizi in **densità logaritmica**. La v7 corregge anche l'enunciato del Lemma 7.9; non cambia il quantificatore principale. [Testo](https://arxiv.org/html/1909.03562v7). | Il trasporto ai tempi di primo ingresso impedisce una concatenazione probabilistica ingenua. Non identifica le singole eccezioni e non permette `f=1`. Nessun trasferimento automatico a tutti i `Q_v`. |
| [Inselmann, arXiv:2402.03276v3](https://arxiv.org/abs/2402.03276v3), 13 agosto 2024; preprint nella scheda consultata. | Il Teorema 1.6 controlla, in densità naturale uno, lo scarto delle parità da `k/2` entro `ε log₂ n`, simultaneamente fino a `k=log₂ n/(1−log₂√3)`. [Testo](https://arxiv.org/html/2402.03276v3). | Anche una famiglia intera di torre può appartenere all'insieme eccezionale. Inoltre `log Q_v` ha ordine `2^v`: l'errore non ha scala polinomiale in `v`. |
| [Rozier–Terracol, arXiv:2502.00948v5](https://arxiv.org/abs/2502.00948v5), 17 maggio 2026; *Discrete Mathematics* 349 (2026), 115167, [DOI](https://doi.org/10.1016/j.disc.2026.115167). | Analisi dei segmenti paradossali: il coefficiente `3^q/2^j<1` non basta, da solo, a far scendere un segmento finito. Teorema 2.4: limiti estremali della correzione affine. Lemma B.2 corretto nella v5. [Testo](https://arxiv.org/html/2502.00948v5). | Serve l'ordine delle parità e il controllo del resto. La finitezza generale dei segmenti paradossali è proposta congetturale, non un fatto da importare. |
| [Niu, arXiv:2605.13886v1](https://arxiv.org/abs/2605.13886v1), 11 maggio 2026; preprint. | Teorema 2: ogni parola di `k` parità occupa una classe modulo `2^k`, con conteggio fra `floor(N/2^k)` e `ceil(N/2^k)`. Altri risultati contano i segmenti paradossali di **lunghezza fissata/limitata**. [Testo](https://arxiv.org/html/2605.13886v1). | Non si può scambiare il limite `N→∞` con una lunghezza illimitata dipendente dall'orbita. È prior art vicino ai conteggi finiti, non una discesa universale. |
| [Barina, progetto attivo](https://pcbarina.fit.vut.cz/); articolo *J. Supercomputing* 81 (2025), 810, [DOI](https://doi.org/10.1007/s11227-025-07337-0). | La pagina consultata riporta verifica di tutti gli inizi sotto `2075·2^60`; il traguardo `2^71` è datato 15 gennaio 2025. | Soglia finita, utile come base solo se un teorema porta **ogni** inizio sotto di essa. Il numero dinamico va accompagnato dalla data del controllo. |
| [Angeltveit, arXiv:2602.10466v1](https://arxiv.org/abs/2602.10466v1), febbraio 2026; preprint. | Migliora il costo dell'algoritmo di verifica esaustiva: il raddoppio dell'intervallo non richiede il raddoppio del lavoro. [Testo](https://arxiv.org/html/2602.10466v1). | Accelerare una certificazione finita non chiude il quantificatore infinito. Non motiverebbe riavviare una campagna di filtri priva di stima nuova. |
| [Hercher, arXiv:2201.00406](https://arxiv.org/abs/2201.00406); *Journal of Integer Sequences* 26 (2023), 23.3.5. | Esclusione dei cicli non banali con al più 91 minimi locali. | Non è esclusione di ogni ciclo; i minimi locali non sono la lunghezza totale. |
| [Knight, *Collatz high cycles do not exist*](https://www.sciencedirect.com/science/article/pii/S0012365X25004200), *Discrete Mathematics* 349(3), marzo 2026, 114812. | Esclude la classe tecnica dei *high cycles* interi positivi, costruita tramite parole di Christoffel; ipotesi di coprimalità e positività nel quadro del paper. | Il titolo non esclude tutti i cicli. Utile per il ramo periodico, non per orbite irregolari divergenti. |
| [Fernández–Ibáñez, arXiv:2607.24844v1](https://arxiv.org/abs/2607.24844v1), 24 luglio 2026; preprint. | Le parole di Christoffel massimizzano, a meno di rotazione, il minimo del numeratore affine fra le rotazioni a lunghezza e numero di dispari fissati. [Testo](https://arxiv.org/html/2607.24844v1). | Un estremo combinatorio non implica che tutti i candidati siano estremali. Il collegamento con `CycleConstraints` sarebbe applicazione specifica, non nuova scoperta della struttura di Christoffel. |
| [Chim, *Lower bounds for linear forms in two p-adic logarithms*](https://tugraz.elsevierpure.com/en/publications/lower-bounds-for-linear-forms-in-two-p-adic-logarithms/), *J. Number Theory* 266 (gennaio 2025), 295–349. | Teorema 2.1 per basi algebriche moltiplicativamente indipendenti: stima esplicita della valutazione, lineare nel parametro logaritmico degli esponenti, con prodotto delle altezze delle basi. [Testo pubblicato](https://tugraz.elsevierpure.com/ws/portalfiles/portal/92346766/1-s2.0-S0022314X24001793-main.pdf). | Per `3^E+c` resta dipendenza da `log c`; se `c` nasce da un prefisso lungo non è una costante uniforme. Una somma con molti termini non diventa automaticamente una forma in due logaritmi. |
| [Bugeaud, arXiv:2608.23017v1](https://arxiv.org/abs/2608.23017v1), 24 agosto 2026; preprint. | Teorema 1.2: una famiglia di cifre con complessità lineare uniformemente limitata e un'ipotesi di non divisibilità non può contenere infinite `S`-unità; soglia ineffettiva. Teorema 1.6: limite effettivo all'esponente di ripetizione digitale `W^t`. [Testo](https://arxiv.org/html/2608.23017v1). | Applicabile a potenze di 3 in base 2. Un eccesso di dispari Collatz non implica però bassa complessità delle cifre di `3^E`: manca proprio questa deduzione. |
| [Garcia–Tal, *A note on the generalized 3n+1 problem*](https://matwbn.icm.edu.pl/ksiazki/aa/aa90/aa9033.pdf), *Acta Arithmetica* 90(3) (1999), 245–250. | Meccanismo di collisione fra classi di parità; sparsezza di Banach delle orbite infinite nel regime del paper, che comprende Collatz. [Scheda editore](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/90/3). | Riguarda i **valori lungo un'orbita**: è un asse distinto dalla densità dell'insieme degli inizi. Non esclude quell'orbita. |
| [Curry, DOI 10.5281/zenodo.22087163](https://doi.org/10.5281/zenodo.22087163), 24 agosto 2026; preprint di cinque pagine. | Quantifica il meccanismo precedente: per un insieme senza collisioni simultanee, il numero di punti in ogni finestra di ampiezza `X` è `O(X^β log X)` per `β>0,9653844…`. Ne segue la sommabilità dei reciproci lungo un'orbita divergente. | Non riguarda cicli e non prova Collatz. Recuperato via API Zenodo e letto integralmente; non è un risultato assunto sulla sola base di un README. Ulteriore controllo sotto. |

**Prior art più vicina all'idea di “altezza del realizzatore”.** [Rozier, *The 3x+1 problem: a lower bound hypothesis*](https://arxiv.org/abs/1510.01610), pubblicato in *Functiones et Approximatio* 56 (2017), 7–23, formula già la LBH

`n ≥ j^(−C)·2^((1−H(q/j))j)`

per gli inizi con `q` dispari in `j` passi abbreviati. La LBH è **ipotesi aperta**, con conseguenze più forti di Collatz; non è una stima disponibile. Il [testo dell'autore](https://www.ipgp.fr/~rozier/pub/LBHv4.pdf), §§2–4, impedisce di presentare come nuova la sola proposta di dimostrare un limite inferiore entropico dei realizzatori. Anche l'identità di prodotto che controlla la correzione affine compare nel suo Lemma 2.5.

## 2. Formalizzazioni recenti e pretese di prova

| Fonte primaria | Cosa è stato verificato in questa ricerca | Stato da conservare |
|---|---|---|
| [Morris, `gotrevor/tao-collatz`](https://github.com/gotrevor/tao-collatz) | README e struttura dichiarata: formalizzazione dei risultati di Tao e controlli degli enunciati. | Qui non è stato riprodotto il build completo. Anche un replay riuscito proverebbe il teorema di Tao, non Collatz. |
| [Mazur/ProofAtlas, densità naturale in tempo logaritmico](https://www.proofatlas.ai/formalizations/natural-density-log-time-collatz/) | La pagina ora presenta review interne accettate, specificando reviewer AI e assenza di indipendenza affermata. Gli enunciati pubblici distinguono `145 log N` passi Syracuse e `436 log N` ordinari, soglia tendente a infinito e domini di densità. | Aggiorna la fotografia locale precedente: “accepted formalization” è lo stato della piattaforma, non peer review umana indipendente identificata. Non arriva a 1 e lascia eccezioni di densità zero. |
| [Mazur/ProofAtlas, convergenza di densità positiva](https://www.proofatlas.ai/formalizations/positive-density-log-time-collatz/) | Pagina della formalizzazione e confini dichiarati del risultato. | Proposta di avanzamento parziale, da sottoporre a replay e verifica degli enunciati. Densità positiva non è densità uno. Non usata come premessa. |
| [Mazur/ProofAtlas, predecessori di densità inferiore positiva](https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/), manoscritto 6 settembre 2026. | Tre enunciati pubblici: molti predecessori di ogni target positivo non divisibile per 3; controesempio implica non convergenza di densità inferiore positiva; convergenza di densità superiore uno implica Collatz. La pagina dichiara riuso di dipendenze compilate. | Nessuna prova della premessa “convergenza di densità superiore uno”. La pagina esclude un rebuild integrale freddo e un checker indipendente di tutta la libreria. I controlli non sono stati riprodotti qui. |
| [Sharpe, `msharpe248/collatz`](https://github.com/msharpe248/collatz) | Repository come fonte dei propri enunciati: risultati sui predecessori, barriere ai potenziali finiti, parole meccaniche, ombre 3-adiche. | Prior art rilevante; la descrizione di un risultato come verificato non sostituisce un replay nostro. Né esponenti di predecessori minori di 1 né teoremi di impossibilità locali eliminano tutti i controesempi. |
| [De Jesús, `eoc-lean-verification`](https://github.com/innerlightr-wq/eoc-lean-verification), revisione 5, settembre 2026. | Il repository descrive già realizzatori esatti modulo `2^(S+1)`, ancore fisse/mobili, occupazione e universalità finita di osservabili Chang. Dichiara aperta `PowerOfTwoDangerousWindowSparsity`, relativa a finestre di pressione aritmetica; gli enunciati successivi sono condizionali. | Sovrapposizione sostanziale con il nostro linguaggio: non rivendicare novità per “moving anchor” o per ribattezzare il nodo anti-concentrazione. La milestone `ShapeTail` del 16 settembre è un controllo d'insieme, non puntuale. Non è stato eseguito un replay del repository. |
| [Chang, arXiv:2603.11066v6](https://arxiv.org/abs/2603.11066v6), 22 aprile 2026, 233 pagine; e [arXiv:2603.25753v1](https://arxiv.org/abs/2603.25753v1), 24 marzo 2026. | Il primo dichiara espressamente di non provare Collatz; il secondo lascia aperto il bilanciamento delle visite dell'orbita. Il conteggio di residui non è il conteggio di visite lungo ogni orbita. | Non assumere “esaurimento dei paradigmi” come teorema generale di impossibilità. La pretesa di unica misura non atomica del primo ha l'obiezione esplicita del §3. |
| [AIDoctrine/CollatzLayerA](https://github.com/AIDoctrine/CollatzLayerA) | Il README espone due assiomi propri: convergenza sotto `2^109` e `odd_steps_certificate`. | Il theorem finale è condizionale. Il primo assioma supera la verifica esaustiva pubblicata; l'altro assume uniformità dei segmenti che non può essere dedotta da una build senza `sorry`. |
| [Sousa–Mazzoni, *La conjecture de Syracuse enfin démontrée ?*](https://revuechercheur.com/index.php/home/article/view/1872), *Revue Internationale du Chercheur* 7(3), 6 settembre 2026. | L'abstract primario dice che resta in corso la ricorrenza strutturale dei raccordi necessaria alla prova incondizionata. | Una presentazione secondaria come “prova completa di settembre” è eccessiva rispetto alla fonte. Il titolo interrogativo non è una certificazione; non è stato revisionato l'intero manoscritto. |

Non vanno confuse quattro evidenze: codice compilato, assiomi elaborati del theorem finale, corrispondenza con l'enunciato matematico desiderato, e revisione indipendente. Qui sono state controllate fonti e formulazioni; non si certificano le intere import closure dei progetti esterni.

## 3. Obiezione riproducibile all'unicità non atomica di Chang

La [Proposizione C.48 del PDF v6](https://arxiv.org/pdf/2603.11066v6), pagina stampata 180, assume un gap spettrale uniforme `|λ₂(M_K)|≤c<1` e ne deduce che Haar è l'unica misura di probabilità Borel `S`-invariante non atomica sui dispari 2-adici. L'antecedente è essenziale: non presentiamo la proposizione come un enunciato senza ipotesi. Il passaggio precedente sostiene che ogni misura invariante proietti a una distribuzione stazionaria del kernel finito mediato. Quell'inferenza richiede un'ipotesi di compatibilità delle distribuzioni condizionali che non segue dalla sola invarianza.

Il seguente è **un controllo matematico autonomo della conclusione**, non una citazione di un risultato del paper.

Sia `a=(a₁,a₂,…)` una successione con `a_i∈{1,2}`, con legge prodotto equiprobabile, e sia `A₀=0`, `A_j=Σ_{i=1}^j a_i`. Definiamo

\[
 x(a)=-\sum_{j\ge0}\frac{2^{A_j}}{3^{j+1}}\quad\text{in }\mathbb Z_2.
\]

La serie converge uniformemente, perché `A_j≥j`. Il primo termine è dispari e tutti gli altri sono pari, quindi `x(a)` è dispari. Se `σ` elimina il primo simbolo, il calcolo diretto dà

\[
 3x(a)+1=2^{a_1}x(\sigma a).
\]

Poiché `x(σa)` è dispari, la valutazione è esattamente `a₁`, e `S(x(a))=x(σa)`. Si recupera quindi l'intera successione di simboli dall'orbita: `x` è iniettiva. La misura immagine della legge prodotto è Borel, invariante e non atomica. È diversa da Haar: assegna massa zero all'insieme `ν₂(3x+1)≥3`, al quale Haar sui dispari assegna massa `1/4`.

Questa costruzione evita anche il punto singolare `−1/3`, perché `3x(a)+1` è sempre non nullo. Mostra che la conclusione di unicità non vale per lo spazio di misure indicato. Da sola non certifica il gap uniforme assunto nell'antecedente, né confuta tutti gli altri risultati del manoscritto; rende incompatibile il pacchetto «gap valido + deduzione proposta + conclusione».

Il difetto di proiezione è visibile già modulo 8. Ordinando i residui dispari come `(1,3,5,7)`, la misura costruita ha distribuzione `ν=(1/2,1/4,0,1/4)`. Il kernel ottenuto mediando rispetto a Haar **entro ogni cilindro sorgente** ha righe `U,(1/2,0,1/2,0),U,(0,1/2,0,1/2)`, dove `U=(1/4,1/4,1/4,1/4)`. Quindi `ν M=U≠ν`, benché la misura originale sia S-invariante. Il kernel Haar usa distribuzioni condizionali diverse da quelle di questa misura. Questo calcolo finito controlla precisamente l'inferenza contestata, senza dover verificare il gap per ogni K.

L'argomento non è stato formalizzato in Lean in questa nota. È sufficiente per non usare l'unicità come premessa e per richiedere una correzione o restrizioni esplicite dello spazio delle misure. La v6 pubblicata del nostro progetto non viene riscritta; la presente obiezione è una nuova nota critica.

## 4. Meccanismi trasferibili, con il lemma mancante

### A. Sparsezza dei valori e correzione reale sommabile

Il [preprint di Curry](https://zenodo.org/records/22087163/files/occupation_note_clean.pdf?download=1), Teorema 2.3, è stato controllato integralmente. La dimostrazione trasla una finestra mediante multipli di `2^N`, fissa il numero di dispari, e separa parole numerose da immagini contrattive. Nel secondo caso troppe immagini impongono una collisione simultanea; le orbite divergenti non ne ammettono. Il ragionamento è corretto al livello della lettura svolta, senza una verifica formale indipendente. Una versione meno precisa usa `γ=3/5`, `β=49/50`; i confronti degli esponenti si riducono a

`5^50 < 2^69·3^30`, `3^30 < 2^49`.

La seguente conseguenza per la **fase reale** è una deduzione da ricontrollare e utilizzare con attribuzione ai suoi input, non una rivendicazione di priorità. Scriviamo una vera orbita dispari come `n_j`, le sue valutazioni come `a_j`, e poniamo

\[
 \alpha=\log_2 3,\quad A_j=\sum_{i<j}a_i,\quad
 E_j=\sum_{i<j}\log_2\left(1+\frac1{3n_i}\right).
\]

L'identità esatta è

\[
 \log_2 n_j=\log_2 n_0+j\alpha-A_j+E_j.
\]

Per un'orbita divergente, la sparsezza rende `Σ_j 1/n_j` finita; quindi `E_j→E_∞<∞`. Sulla circonferenza,

\[
 \{\log_2 n_j\}=\{j\alpha+c+o(1)\},\qquad
 c=\log_2 n_0+E_\infty.
\]

Poiché `α` è irrazionale, la fase è equidistribuita. Si può anche controllare la coda spaziale dei reciproci sopra `M` con ordine `M^(−1/50) log M`, mediante annuli diadici. È un vincolo su una singola eventuale orbita divergente, diverso da una media sugli inizi.

**Manca il raccordo:** l'equidistribuzione della mantissa non determina i bit bassi e non implica una media delle valutazioni superiore ad `α`. Un possibile nuovo oggetto di studio è la distribuzione congiunta di fase reale, classe 2-adica e altezza del quoziente, con il vincolo che siano coordinate dello **stesso intero positivo**. Parlare genericamente di indipendenza sarebbe ingiustificato. Per i cicli occorre un argomento separato.

**Obiezione preventiva.** Nel modello affine reale con `a_j=1` prescritto,

`y_j=(3/2)^j(y₀+1)−1`

è positivo e divergente per `y₀>0`, ha reciproci sommabili e fase asintoticamente rotante; la stessa parola ha realizzatore 2-adico `−1`. Sono dunque compatibili deriva positiva, fase regolare e realizzabilità 2-adica. Non formano una vera orbita intera positiva con lo stesso seed nelle due immersioni. Il lemma cercato deve utilizzare esattamente questa compatibilità aritmetica; eliminare la sola deriva del modello sarebbe falso.

**Prior art della rotazione.** [Shakibaei Asli, arXiv:2601.04289v1](https://arxiv.org/html/2601.04289v1), 7 gennaio 2026, propone la coordinata `{log₆(x+1/5)}` per la mappa ordinaria, con errore locale `O(1/x)`. La nota presente usa il cociclo Syracuse elementare. Non assume le sue affermazioni globali sulla perturbazione: un errore piccolo a ogni passo non è automaticamente sommabile. Inoltre un intervallo di mantisse contiene interi arbitrariamente grandi, quindi entrarvi non forza l'ingresso in una regione numericamente limitata. La rotazione, isolatamente, non è un'idea risolutiva nuova.

### B. Bilanciamento delle potenze solo dove il teorema lo consente

[Mérai–Shparlinski](https://arxiv.org/abs/1812.08837), *Math. Comp.* 89 (2020), 911–922, tratta sequenze inversive modulo potenze di 2, con specializzazione alle potenze di 3. La rassegna locale del 25 settembre controlla già il trasferimento alle colonne originarie della torre, nel regime `r+t+1=o(r^(3/2))`. [Vandehey](https://arxiv.org/abs/1606.07911), *J. Analyse Math.* 138 (2019), fornisce un riferimento complementare sulle somme esponenziali a moduli con primi fissati.

**Manca:** una stima che includa i pesi determinati dalla dinamica e le colonne aggiunte adattivamente, sul tempo necessario alla discesa. Non si può ampliare il dominio del teorema per analogia. Aggiungere filtri a profondità finita non produce quel controllo.

### C. Rigidezza digitale e altezze: una possibile via aritmetica, ancora senza ponte

Bugeaud e Chim suggeriscono due condizioni sfruttabili: una rappresentazione digitale troppo ripetitiva, oppure una forma logaritmica con poche basi e altezze effettivamente controllate. Applicarle richiederebbe dedurre una di queste condizioni dalla **raggiungibilità esatta** di un segmento persistente della torre. Nessuna delle due discende dal suo solo numero di dispari. La dimensione della somma affine cresce con la parola; usare un teorema del sottospazio in dimensione fissata ignorando tale crescita non è valido.

Questa pista ha un criterio di avanzamento chiaro: prima un lemma che comprima la relazione aritmetica senza perdere l'informazione decisiva, poi la stima. Finché quel lemma manca, non è giustificato finanziare un'altra lunga scansione di filtri.

### D. Confronto relativo fra bacini di predecessori: candidata del nuovo programma

La proposta elaborata durante questa revisione è cercare, per target dispari ammissibili senza ritorno, un confronto fra il bacino `B(n)` e quello del fratello `h(n)`, dove

`h(n)=4n+1` se `n≡1 (mod 3)`, e `h(n)=16n+5` se `n≡2 (mod 3)`.

Entrambi non sono divisibili per 3 e soddisfano `S(h(n))=S(n)`. La candidata è una disuguaglianza **non dimostrata** del tipo

\[
 \underline d(B(h(n)))\ \ge\
 \frac{c}{1+\log n}\,\underline d(B(n)),\qquad c>0\text{ uniforme}.
\]

La parola “Harnack” descrive qui il tipo di confronto; non autorizza l'applicazione di un teorema classico di Harnack a questi bacini.

**Confronto primario preciso.** Il [manoscritto Mazur v1, 6 settembre 2026](https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/paper-v1.pdf), §§4.2–4.3, dà una positività separata per ogni target scegliendo un predecessore `R` senza ritorno nel residuo opportuno. La scelta è `m=132RC_*+1`, e la costante finale è `c_a=3/(256R·3^m)`. La Remark 4.3 segnala esplicitamente la dipendenza esistenziale da `R` e l'assenza di un procedimento uniforme nel target. Queste stime non confrontano due bacini e non forniscono la candidata. Anche l'input analitico del manoscritto resta da sottoporre a replay indipendente prima di diventare una premessa certificata del progetto.

Il problema di densità dei predecessori è molto anteriore: [Wirsching, *DCDS* 9(3) (2003), 771–787](https://www.aimsciences.org/article/doi/10.3934/dcds.2003.9.771), presenta tre gap come congetture. Il recente [manoscritto e codice di Tavares](https://github.com/faculdade/wirsching-conjectures-1-and-3/tree/7afd2598742e0f62322db1ec28222b1bae460f1b) dichiara chiuse le Congetture 1 e 3, lasciando aperta la condizione `(*3)` e la Congettura 2 quale via ad essa. Il pin è quello letto oggi; README, stato dichiarato e corrispondenza delle sezioni sono stati consultati, non revisionata integralmente la prova. Non è un risultato di confronto fra i nostri due target.

**Perché la candidata è interessante e forte.** Lungo un'orbita divergente iniettiva `x_i`, i bacini laterali `B(h(x_i))` sono disgiunti e `B(x_0)⊆B(x_i)`. Se il bacino iniziale ha densità inferiore positiva, la candidata e `x_i≤2^i x_0` imporrebbero una somma armonica divergente di densità inferiori di insiemi disgiunti, impossibile. Il passaggio deve essere formulato usando somme **finite** prima del limite. Non esclude i cicli; lì l'iniettività dell'orbita manca.

**Ostacoli da non nascondere.** Positività target per target consente masse laterali sommabili. Nemmeno una stima uniforme assoluta `d(B(a))≥c/a`, proposta nel programma classico, darebbe il confronto relativo logaritmico: lungo valori esponenziali la serie `Σ1/x_i` può convergere. Una traduzione affine dei predecessori di `n` non preserva automaticamente integrità e valutazioni per il target `h(n)`: le condizioni sono modulo potenze crescenti di 3. Serve un argomento nuovo sul rapporto dei bacini, non un cambio del nome dell'ipotesi statistica.

Nelle ricerche `Collatz predecessors density Harnack`, `inverse trees density ratio 4n+1`, e nei testi primari sopra non è stato identificato lo stesso confronto. **Non è una certificazione di novità.** La candidata merita una verifica indipendente e tentativi di confutazione prima di essere promossa a strategia principale; al momento è un'ipotesi quantitativa che, unita a un input forte sui predecessori, eliminerebbe soltanto il ramo divergente.

## 5. Ricerca svolta, verifiche e limiti

Sono stati ricontrollati gli URL delle rassegne locali; cercati lavori 2025–2026 su parità, densità, cicli, verifica computazionale, logaritmi p-adici e cifre; seguiti i riferimenti pertinenti dei repository più vicini. Le ricerche comprendevano, fra le altre, `Collatz 2026 September advances proof density`, `Rozier parity density Collatz`, `Chim lower bounds two p-adic logarithms`, `Collatz Christoffel 2026`, `An Explicit Windowed Sparsity Bound`, e il titolo Sousa–Mazzoni. I risultati secondari sono stati usati come indici, non come fondamento dei teoremi.

Per Curry, il normale accesso web a Zenodo non funzionava: sono stati letti i metadati da `https://zenodo.org/api/records/22087163` e il PDF primario tramite il relativo endpoint dei file, estratto in memoria senza alterare altri file del progetto. È stata letta la prova intera di cinque pagine. Per Chang sono stati letti abstract, sezioni sulle pretese universali e il passaggio C.48, non tutte le 233 pagine. Per le formalizzazioni si è controllata la documentazione delle evidenze; non sono stati eseguiti rebuild esterni.

Le fonti nuove più utili rispetto alla fotografia locale sono **Niu**, **Curry/Garcia–Tal**, il programma **EOC** come confronto di priorità e di ostacoli, e **Wirsching/Tavares** per la pista inversa. Il risultato operativo della ricerca non è “abbiamo trovato la prova”: è una ragione concreta per sostituire il bilanciamento da memoria finita con due domande precise — compatibilità reale/2-adica e confronto relativo dei bacini — accompagnate dalle rispettive ipotesi ancora aperte.
