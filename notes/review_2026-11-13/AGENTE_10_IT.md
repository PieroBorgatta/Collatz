# Analisi 10 Revisione avversa e priorità finali

13 novembre 2026. Controllo in sola lettura della relazione coordinata, delle analisi 4–8 e dei lemmi Lean pertinenti. Nessuna nuova build o modifica ai sorgenti. Non ho trovato errori materiali nelle nuove formule aritmetiche esaminate; gli obblighi analitici restano aperti e non devono essere indeboliti durante l'implementazione.

## Verifica dei rilievi sulle note storiche

La critica a `notes/phase10_A0_weak_approximation_theorem_2026-05-25.md:169–185` è corretta. Nel caso a un solo stato con inclusioni e proiezioni identità, `K_(2^m)=(1+sin(log(m+1)))/2` è un kernel positivo substocastico. Gli incrementi tendono a zero, ma esistono sottosuccessioni con valori tendenti a 0 e a 1. Quindi l'ipotesi `D_N→0` non dimostra Cauchy. A0W7, se assume il limite, rende quella parte una premessa; nella lettura che vuole provare Cauchy non aggiunge il controllo mancante. Servono una maggiorazione sommabile, una stima fra scale arbitrarie o una struttura identificata che dia convergenza. Se variano E_N e I_N bisogna stimare la differenza degli approssimanti completi, non soltanto `I_N(K_(2N)−K_N)E_N`.

Anche la critica al campionamento Haar è corretta nella forma qualificata della relazione. Il §8.2 di `phase10_gate10B_conditional_closure.md:445–451` assume esplicitamente che l'osservabile sia costante sui cilindri. La sola limitatezza e misurabilità del successivo schema non consentono di sostituire un integrale condizionale con valori sui rappresentanti naturali: `1_(Z₂\N)` ha integrale 1 e ogni media puntuale considerata uguale a zero. Se la condizione B è invece letta come un'ipotesi che assume già l'identità con veri integrali, la proposizione non è confutata da questo esempio; è la verifica di B per gli script a rimanere aperta. Non trasformare il rilievo in un'accusa di errore nei risultati Lean.

## Verifica dei nuovi corollari aritmetici

Per `r,t≥1`, `0≤j≤r`, i punti `x_j=18t·8^(r−j)9^j−5` sono tutti positivi dispari e `13 mod18`. Per `j<r`, `y_j=216t·8^(r−j−1)9^j−7` è positivo dispari e `65 mod72`. Le identità esatte sono `3x_j+1=2y_j` e `3y_j+1=4x_(j+1)`. Il residuo 65 non è ammesso da alcun porto di `MarkedSection.lean:15–17`. Ogni segmento è dunque un primo ritorno di due passi, e l'incremento dichiarato è positivo. Inoltre `y_j−x_j=72t·8^(r−j−1)9^j−2>0`: non c'è neppure discesa interna ai segmenti. La conclusione di arbitrariamente molti primi ritorni consecutivi crescenti è valida. È un corollario dell'aritmetica delle torri, non una nuova esclusione di tutte le strategie di rango: un contatore parametrico può diminuire mentre l'intero cresce, ma bisogna controllarne il reset all'uscita.

Il budget multi-target è anch'esso una deduzione valida. `WeightedWords.matches_eq_of_length_eq`, riga 17, rende iniettiva la lunghezza su parole distinte esatte dalla stessa sorgente. `wordWeight_eq_weight_of_matches`, riga 67, identifica il peso con quello dell'orbita; l'endpoint è `S^[|w|] x`. Quindi ogni addendo `ω(w)/[R_w(3R_w+1)]` coincide con `loss(x,|w|)`, e `WeightedVisits.sum_loss_finset_le`, riga 107, conclude. Sono necessari W finito senza duplicati, matching esatto e x>0; endpoint positivi seguono dall'orbita. La parola vuota e i target periodici non creano problemi. Incidenze etichettate che ripetono una parola vanno aggregate con peso totale controllato. Non è una minorazione analitica della massa di radici: normalizzare pesi grandi può rendere molto piccola la massa disponibile e quel costo deve apparire nella stima successiva.

La fattorizzazione `Q_v=∏_(j<v)(9^(2^j)+1)/2` e la coprimalità dei fattori sono corrette. Ogni fattore divide una nuova differenza di potenze ed è congruo a 1 modulo ogni fattore precedente; non serve Zsigmondy per dedurre nuovi primi. La conclusione riguarda la sorgente, non l'ordine delle parità della sua orbita. L'analisi 6 distingue correttamente questo limite.

## Quantificatori del confronto aggregato

La spina va dichiarata positiva, dispari, iniettiva e con `3∤x_0`, scartando il primo termine se necessario. I fratelli canonici sono allora definiti a ogni indice. I blocchi `U_j` sono unioni dei bacini dei fratelli per `2^j≤i<2^(j+1)`; la disgiunzione tra blocchi è reale, non una disgiunzione di sole etichette.

La condizione sufficiente della relazione è corretta se c,D>0 sono indipendenti da j; possono dipendere dalla spina fissata. Per ogni j deve valere, a cutoff sufficientemente grandi, `|U_j∩[1,DX]|≥c|B(x_0)∩[1,X]|−E_j(X)`, con `E_j(X)=o_j(X)`. Non serve un cutoff uniforme in j.

Una prova diretta evita ogni ambiguità sul liminf: fissare J blocchi, sommare le J disuguaglianze al medesimo cutoff DX e usare il packing. Si ottiene `DX≥Jc|B(x_0)∩[1,X]|−Σ_(j<J)E_j(X)`. Passare a X→∞ dà `D≥Jcδ`, con δ>0 densità inferiore del bacino iniziale, contraddizione per J arbitrario. Nessuna somma infinita è scambiata con il liminf.

La formulazione è un obiettivo aperto forte. Raggruppare i fratelli può tollerare perdite individuali, ma non garantisce compensazione. Se si introducono dilatazioni D_j, carichi M_j e masse η_j variabili, occorre dimostrare la divergenza dei coefficienti netti disponibili, ad esempio della serie `Σ η_j/(D_j M_j)` nel modello appropriato. Non è sufficiente che ogni blocco abbia massa positiva. La proposta non va descritta come riduzione già dimostrata della difficoltà di H.

## Flusso e realizzazione congiunta

Il criterio dell'analisi 8 rende esplicito il costo che la ricerca deve controllare: `D_n M_n/η_n≤C(1+log n)`. È corretto consentire che altezza e carico dipendano dal target, purché il costo combinato soddisfi il bound uniforme. Il doppio conteggio è elementare; l'esistenza di un flusso sostenuto su parole effettive con quella massa relativa resta il nucleo aperto.

La surgery bilanciata è un buon test di fattibilità algebrica. Preservare A e modificare soltanto esponenti precedenti all'ultimo lascia C modulo 3 invariata e non trasferisce al fratello canonico. Toccare l'ultimo esponente con la parità necessaria supera soltanto il primo ostacolo ternario: non dimostra la congruenza modulo `3^k`, il matching o un costo d'altezza utile. Un enumeratore deve registrare le coppie effettivamente realizzabili `(A,C)` insieme alla profondità. Una finestra ammissibile per C non è una distribuzione uniforme di C, né la sua non-vacuità una quota di massa positiva.

## S-unità e invenzione di novità

La deduzione proposta da `9(µ+1)−4=4T²(µ)` ha una struttura coerente: per un insieme finito di primi generati, includendo 2 e 3, U e V sono S-unità e U−V=1. La finitezza classica delle soluzioni sarebbe incompatibile con infiniti minimi d'onda distinti. Va scritto il piccolo lemma dinamico che una traiettoria divergente ha infiniti minimi d'onda: altrimenti, dopo l'ultima onda, i successivi minimi di ripple diminuirebbero strettamente. Non basta chiamare questa infinità evidente senza collegare le mappe.

Questo controllo non certifica una correzione o un nuovo teorema sul paper esterno. Dimostra quale interfaccia occorra controllare e perché non è prudente trattare la sola nuova fonte come salto strategico. Infiniti primi sono compatibili con divergenza; manca una disuguaglianza che li colleghi al deficit di parità. La pista va mantenuta esplorativa finché quel lemma non esiste.

## Priorità e condizioni per proseguire

1. **Consolidamento circoscritto:** formalizzare il budget multi-target e il corollario dei primi ritorni, con test negativi per parole duplicate e pretesi primi ritorni che attraversano E. Sono risultati con dimostrazioni già identificate; non presentarli come avanzamenti globali. Documentare separatamente le due correzioni delle note spettrali.
2. **Esperimento matematico principale:** specificare un piccolo flusso di incidenze reali, costo netto e massa relativa fissati prima dell'enumerazione. Il primo deliverable è una proposizione completa, non un buon rapporto empirico. Fermarsi se la massa viene posta come normalizzazione, se si confrontano soltanto lower bound separati o se il supporto congiunto ha celle necessarie vuote.
3. **Programma dei ritorni in parallelo:** certificato di composizione e complemento esatto dei domini, seguito da una macro a durata variabile con uscita controllata. Fermarsi se ogni uscita rigenera lo stesso problema con un parametro non diminuito, oppure le nuove celle duplicano la copertura esistente.
4. **Ramo spettrale e S-unità:** riaprire solo su un lemma quantitativo nuovo e verificabile. Per il primo occorre un errore sommabile o una vera identificazione del limite; per il secondo un legame fra primi e dinamica, non soltanto il loro numero.

Il progetto è verificabile nel suo perimetro locale e conserva risultati utili. Le alternative hanno valore se producono un lemma indipendente e controllabile; la convergenza universale e l'esclusione dei cicli restano obblighi distinti.
