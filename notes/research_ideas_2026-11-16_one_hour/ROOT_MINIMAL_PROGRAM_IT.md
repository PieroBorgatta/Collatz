# Un contratto più piccolo per il prossimo tentativo

16 novembre 2026. Deduzione su carta, controllata indipendentemente da H02 e H03 durante l'ora concettuale. Nessuna nuova prova Lean, compilazione o ricerca numerica. Il risultato è una semplificazione del programma, non la costruzione degli editor mancanti né una rivendicazione di priorità.

## 1. Gli input effettivi

Si supponga una traiettoria Syracuse divergente e quindi iniettiva `n_j=S^j(b)`, con b positivo dispari unità. Sia `A_j` la somma dei primi j esponenti e `Ω_j=3^j/2^A_j`. Il prodotto di primo arrivo già verificato nel progetto dà

`n_j=b Ω_j P_j`, con `1≤P_j≤P₀`.

Per il criterio locale seguente bastano una funzione g sulle unità positive dispari nonperiodiche e tre proprietà:

1. Superarmonicità positiva sui veri genitori unità: `g(n)≥Σ_(Sx=n) (3/2^e_x)g(x)`; l'uguaglianza è sufficiente ma non necessaria.
2. Floor assoluto `g(x)≥c₀>0` sulle unità positive dispari nonperiodiche.
3. Upper `g(n)≤Cn` sui target **nonperiodici**.

Questi input analitici sono esterni: traccia canonica e upper da Valbuena, floor dall'atom estimate di El Jaouhari, con le dipendenze e le versioni discusse da [H01](agents/H01_PRIMARY_LITERATURE_IT.md). Non sono nuovi teoremi Lean del progetto. La via qui non richiede densità naturale dei bacini, CLT, Leen, una legge Q, collisioni, F o cap della traccia. Il bound P₀ riguarda i veri primi arrivi e non importa quelle dipendenze.

L'[ultima riduzione dell'ora](ROOT_ATOM_FLOOR_CORE_IT.md) elimina anche la necessità di usare la traccia canonica di Valbuena: il solo floor degli atomi, insieme a stime aritmetiche, produce una superfunzione adatta. Per il solo budget globale esiste una via ancora più corta mediante densità logaritmica inferiore, già nel primario12. La funzione canonica rimane una possibile scelta, non un prerequisito di quel criterio.

## 2. Il telescopio diretto

Porre `R_j=g(n_j)/Ω_j`. Per j≥1, riservare nella disuguaglianza superarmonica il genitore osservato `n_(j−1)`, con peso `ω_j=Ω_j/Ω_(j−1)`. Gli altri termini sono positivi, dunque R è crescente. Inoltre

`R_j≤CbP₀`.

Sia w_j una **vera** parola alternativa da un seed unità v_j a n_j, che entri attraverso un ultimo genitore diverso da `n_(j−1)`. Iterare la superarmonicità soltanto dentro quel ramo dà

`g(n_j)≥ω_j g(n_(j−1))+Ω(w_j)g(v_j)`.

Pertanto

`R_j−R_(j−1)≥Γ_j g(v_j)≥c₀ Γ_j`, dove `Γ_j=Ω(w_j)/Ω_j`.

Per ogni famiglia finita di indici,

**`Σ_j Γ_j≤[CbP₀−g(b)]/c₀`.**

Non si usano disgiunzione di bacini, limiti di densità o un argomento di secondo momento. Il bound è il telescopio del rapporto armonico già presente in U07, applicato direttamente ai witness. È il collegamento da conservare come nucleo del prossimo attacco.

## 3. Il clock non deve essere uguale

Se w_j ha lunghezza ℓ_j e totale B_j,

`Γ_j=3^(ℓ_j−j) 2^(A_j−B_j)=2^(−E_j)`,

`E_j=(B_j−A_j)−(ℓ_j−j)log₂3`.

Con clock diverso E è un numero reale; Γ è il rapporto razionale di gain e non richiede approssimazioni numeriche. Il vincolo `ℓ_j=j` usato nel primo controller era una scelta della costruzione, non una necessità della contraddizione. Dare libertà al clock evita una restrizione non giustificata del problema.

Il target è costruire witness su un insieme di indici per cui `Σ_j Γ_j=∞`. Una condizione sufficiente, ancora **non dimostrata**, sarebbe `Γ_j≥c/[j log j]` per tutti i j abbastanza grandi. Basta anche una famiglia più irregolare con somma divergente. Non occorre promettere un editor a ogni passo se si può provare un bilancio totale adeguato.

Va evitato un nuovo ottimismo nominale: essendo anche il cammino alternativo un primo arrivo, il suo prodotto correttivo P_alt è tra1 e P₀. Esattamente

`Γ_j=bP_j/(v_j P_alt)`,

`E_j=log₂(v_j/b)+log₂(P_alt/P_j)`.

Il debito è quindi il logaritmo del nuovo seed, entro un errore assoluto≤log₂P₀. Dar libertà al clock serve alla costruzione; non trasforma il problema degli antenati piccoli in una risorsa nuova indipendente.

## 4. Masse di parole, non solo il miglior seed

Si può usare una famiglia finita W_j di parole inverse off-spine, purché sia prefix-free nell'orientazione **dal target alla sorgente**. Le parole forward salvate nel progetto vanno quindi invertite prima di controllare questa proprietà. La parola vuota è esclusa.

Aggiungendo il singolo arco di backtracking, la famiglia resta prefix-free perché tutti gli altri colori iniziali sono off-spine. Sviluppare la superarmonicità fino alla massima profondità della famiglia dà

`R_j−R_(j−1)≥Σ_(w∈W_j) Γ_w g(v_w)≥c₀Σ_(w∈W_j)Γ_w`.

Il medesimo budget finito vale quindi per la somma di tutte queste masse relative. Parole incomparabili possono stare nello STESSO primo ramo laterale; non vanno invece sommate parole annidate. Una parola per primo genitore è una sufficiente condizione semplice, non l'unica scelta.

Questo amplia il bersaglio rispetto a F o al massimo di un solo seed per ramo: una massa di molti witness piccoli può bastare senza che uno abbia un seed particolarmente piccolo. Non è stata costruita tale massa; riformulare il target come somma non la produce.

## 5. Che cosa rende utile la semplificazione

Il prossimo lemma dovrebbe produrre un catalogo legale off-spine, con un costo relativo complessivo non sommabile. Deve controllare contemporaneamente l'offset affine vero, l'integrità e l'unità degli stati, il colore iniziale e il costo Γ. Il controller con carry è uno strumento per conservarne esattamente la legalità; il lifting esponenzialmente costoso non paga ancora il bilancio.

I no-go precedenti hanno quantificatori precisi su target fissi, profili e famiglie di edit. Non dimostrano automaticamente l'impossibilità di questo problema a target mobili e clock variabile. Viceversa questa libertà non costituisce una prova di esistenza.

Una versione più circoscritta da tentare è un correttore che funzioni su una finestra della fase reale e copra tutti i pattern locali di lunghezza L con valutazioni≤M. [H01, §5](agents/H01_PRIMARY_LITERATURE_IT.md) mostra che, scelto M abbastanza grande, l'unione di questi contesti ha densità temporale inferiore positiva sulla possibile spine; il prodotto convergente e il budget medio degli esponenti lo danno senza indipendenza dei residui. Un costo≤log₂j+log₂log j+O_b(1) su tutta quell'unione sarebbe sufficiente. Un singolo pattern che ricorre infinite volte, o soltanto con densità superiore positiva, non dà automaticamente la stessa conclusione al peso1/(j log j). La finitezza dei contesti NON rende finito il carry dell'intero prefisso: proprio quello deve essere trattato dal nuovo lemma aritmetico.

Il guadagno reale di questa ora è ridurre le dipendenze e gli oggetti indispensabili. Non abbiamo ottenuto un nuovo lower, un rate uniforme o una contraddizione alla divergenza. La via ai cicli non banali resta distinta.

## 6. Che cosa rimane senza gli input analitici

Per un solo witness per indice, i seed laterali v_j sono distinti: se uno raggiungesse due ingressi laterali diversi, dopo il primo ingresso seguirebbe già la spine e non potrebbe entrare dall'altro ramo. Il prodotto dà `Γ_j≤bP₀/v_j`. Il budget reciproco-quadratico già usato nel progetto implica allora

`Σ_j Γ_j²≤2(bP₀)²`.

Un editor più forte che costruisse una massa quadratica non sommabile darebbe quindi una contraddizione senza g. Questo non paga il target di primo ordine `Γ_j≈1/(j log j)`: tutti i momenti p>1 restano compatibili con tale sequenza. Il floor armonico esterno consente il criterio meno esigente sull'editor, non è stato dimostrato necessario a ogni possibile approccio. Moltiplicare variazioni dei medesimi upper quadratici non costruisce la massa di primo ordine mancante.
