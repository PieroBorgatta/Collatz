# H02 — Valore reale del lavoro e contratto minimo da perseguire

16 novembre 2026. Audit concettuale sullo snapshot iniziale `c74fe0c`: lettura di README, stato Lean, ambito della v6 e note dei tre sprint. Nessun esperimento, calcolo numerico, build o nuovo codice formale. Le deduzioni sono su carta; gli input analitici esterni restano tali.

## Giudizio

Il lavoro non è completamente inutile. Ha prodotto un nucleo aritmetico controllabile, risultati di discesa su famiglie esplicite, correzioni di errori e ostacoli che eliminano classi precise di trasporti. Questi sono risultati e strumenti reali. Il numero di moduli, audit o versioni non misura però la distanza dalla soluzione: nessuno dei risultati attuali esclude una generica orbita divergente, e i cicli non banali restano un problema distinto.

I controlli finiti precedenti sono stati utili soprattutto per falsificare euristiche: molti codici non significano molti interi, altezza ridotta non significa massa conservata e il difetto di un catalogo troncato non è un lower del vero difetto. Allargare quegli stessi censimenti senza una nuova previsione discriminante aggiungerebbe poco.

## Il controfattuale che deve sopravvivere a ogni racconto di progresso

Una spine divergente ipotetica può soddisfare i budget reciproci, la finitezza dei cataloghi, l'esistenza del massimo F, la sua stabilizzazione e la sommabilità dei contributi laterali. Gli stessi dossier lo dimostrano condizionalmente alla sua esistenza. Non abbiamo costruito un controesempio né provato indipendenza logica; abbiamo verificato che le conclusioni note non producono ancora una contraddizione.

In particolare `F=o(n)` e i lower asintotici richiesti sulle classi F-heavy sono qualitativamente equivalenti alla nondivergenza nel quadro dichiarato: se non vi è divergenza, ciascuna classe heavy è finita e l'enunciato sui root sufficientemente grandi diventa vacuo. È una riformulazione potenzialmente utile, non una riduzione già quasi risolta. F e i minimi antenati usano inoltre raggiungibilità globale: la finitezza esistenziale non offre un tempo per calcolarli.

Il precedente ramo spettrale ha un problema diverso, non un dettaglio di implementazione: un bound su ogni oggetto finito non controlla automaticamente il limite. Le compressioni finite dello shift unilaterale sono nilpotenti, mentre lo shift infinito ha raggio spettrale uno. Questo esempio non confuta i certificati locali del progetto; mostra perché la stima di trasferimento e della coda è essenziale. Tenere chiusa la campagna dei filtri è una decisione giustificata.

Anche una densità positiva del bacino di un seed divergente b è compatibile con [Tao](https://arxiv.org/abs/1909.03562v7): ogni grande antenato passa per b, quindi sotto qualsiasi funzione divergente del valore iniziale; il futuro dopo b può ancora sfuggire. Un risultato statistico sui grandi antenati non determina il destino di b.

## Un'integrazione utile trovata nell'ora

Il resto quadratico a root fissato non va lasciato fra gli obblighi aperti del quadro esterno. [Fonte12/v1](https://rstation.ai/problems/collatz/papers/12), dopo Theorem9, attribuisce già a Valbuena il decadimento della massima massa dei cilindri. Di conseguenza

`K₂^m(g²)(n)/g(n)² = Σ p_w² ≤ max p_w → 0`.

La deduzione è stata ricostruita indipendentemente da root, H01 e H03. Ai root periodici, la probabilità di restare nel ciclo per r giri perde il fattore β^r, β<1; dopo un'uscita finita si applica il caso nonperiodico. Ciò chiude il resto puntuale, senza un nuovo Green e senza una nuova priorità.

Il terminale lineare `y·g(y)` è diverso: al root nonperiodico il prodotto locale dà `Ω_mY_m≥n/P₀`, quindi `K₂^m(y g)(n)≥n g(n)/P₀`. Quel resto non scompare. Non vi è contraddizione fra i due enunciati.

Resta tutto il problema del tempo uniforme su root mobili. Nemmeno `O(log n)` generico basta: il coefficiente critico e l'errore ammesso contano. Una legge nonatomica può avere un prefisso iniziale quasi deterministico arbitrariamente lungo.

## Tre decisioni, senza aggiungere un altro apparato

1. **Abbandonare come motore autonomo:** altri momenti, altri upper di Green o la sola positività del rinnovo. Per seed distinti, la sommabilità di potenze reciproche di ordine maggiore di uno è compatibile con l'infinità. Questi upper non costruiscono la massa laterale di primo ordine. I vecchi no-go restano validi nei loro quantificatori: non vanno estesi automaticamente a target mobili o clock diversi.
2. **Tenere come strumenti:** parole effettive, offset completo, prodotto P₀ e certificati colorati verificabili. Il massimo F e la traccia capped possono organizzare una nota tecnica, ma non devono essere prerequisiti del prossimo tentativo aritmetico. Per un nuovo witness conta il primo genitore fisico; sorgenti annidate nello stesso ramo non si possono sommare senza una vera antichain inversa.
3. **Giocare una sola pista:** un editor a clock variabile con costo ammortizzato, formulato nel [programma minimo di root](../ROOT_MINIMAL_PROGRAM_IT.md). Non è stata costruita una policy con il costo richiesto. Il test discriminante è una disuguaglianza sul carry INTEGRALE che preservi il colore, non una stima media su residui senza condizionamento.

Per chiarezza, lungo una spine da b, con gain originale Ω_j e nuovo witness di lunghezza ℓ_j e totale B_j, porre

`E_j=(B_j−A_j)−(ℓ_j−j)log₂3`, `Γ_j=2^(−E_j)`.

Armonicità nel ramo laterale dà direttamente

`g(n_j)/Ω_j−g(n_(j−1))/Ω_(j−1) ≥ Γ_j g(v_j)`.

L'upper nonperiodico, il prodotto e il floor unità rendono sommabile ΣΓ_j. Questa deduzione non richiede densità naturale, Q, collisione, F o cap. L'editor dovrebbe produrre una famiglia con somma divergente. Per famiglie finite di witness si sommano soltanto parole inverse prefix-free; root espone il contratto completo. L'esistenza di questi witness è la parte sostanziale rimasta aperta.

Il debito non è una nuova risorsa indipendente: il prodotto di primo arrivo lo identifica con `log₂(v_j/b)` entro l'errore assoluto `log₂P₀`. Senza gli input analitici resta invece un budget quadratico puramente locale; un editor più forte, con massa quadratica divergente, darebbe una contraddizione anche senza g. Non è stato dimostrato che quelle fonti siano necessarie a ogni possibile approccio. Il loro vantaggio qui è permettere un bersaglio di primo ordine meno esigente sull'editor.

Un solo witness per blocco geometrico non basta: con seed di grandezza k log k in un unico indice per blocco `[2^r,2^(r+1)]`, i reciproci restano sommabili. Serve massa totale non sommabile sui blocchi, oppure una frequenza inferiore di successi quantitativa. Anche una densità superiore positiva può essere insufficiente per il peso `1/(j log j)`, se i blocchi dei successi sono troppo lacunari. Dire soltanto «accade infinite volte» perderebbe il passaggio decisivo.

## Un half-bridge da leggere con la normalizzazione corretta

La fonte12, eq(48), confronta campioni fisici completi su `(X/4,X]` con la legge naturale mediante il fattore `K₀ X d_n/N_n(X)`, non mediante una costante assoluta dopo condizionamento. Qui N conta TUTTE le sorgenti dispari che prima o poi raggiungono n; la misura a sinistra è soltanto RISTRETTA ai label di genitore unità, non ricondizionata su tali label. Non si postula una densità delle sole sorgenti unità.

Su una classe F-heavy, pool finito e densità naturali positive dei seed danno un onset comune non effettivo e quindi un fattore dipendente soltanto dalla classe. La riduzione alle sorgenti dispari usa l'esatta invarianza per raddoppio dei bacini. Non segue dispersione né un tempo per decidere tutti gli hit. Se per i seed si usa soltanto una lower density positiva, il medesimo argomento va fatto su `[1,X]`, non su ogni guscio fisso: la versione cumulativa si ricava partizionando in gusci, e l'eventuale sorgente n a tempo zero va esclusa dal conteggio dei genitori. Non vengono così rimosse le altre dipendenze del Theorem17. È uno strumento opzionale più carico di input del telescopio diretto, non il nuovo core.

## v7

Una v7 è difendibile come consolidamento tecnico selettivo: formalizzazioni locali, no-go, raccordi e attribuzioni corretti. Non è una tappa matematica verso Collatz per il solo fatto di esistere, e non dovrebbe occupare la prossima ora di ricerca al posto del lemma discriminante. Eviterei un elenco di tutte le note: separerei risultati noti integrati, nuovi enunciati locali e obbligo aperto. Il guadagno strategico di quest'ora è aver tolto un falso obbligo qualitativo e ridotto l'apparato necessario al tentativo, non aver provato un nuovo lower.
