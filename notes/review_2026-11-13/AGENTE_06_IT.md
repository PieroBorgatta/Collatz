# Analisi 6 Torre esatta e vincoli aritmetici

13 novembre 2026. Analisi in sola lettura del progetto al commit 5428e89. Nessuna sorgente del repository modificata, nessun nuovo livello della torre calcolato.

## Stato e domini da distinguere

La famiglia speciale è Q_v=(9^(2^v)−1)/2^(v+3), mentre Q_v(q) lascia variare un parametro dispari. TowerParameter.quotient_difference_valuation e quotient_residue_bijective (lean/CollatzShadowing/TowerParameter.lean:60,107) dimostrano l'isometria e la biiettività residue. TowerSuffix.tower_finite_suffix_arbitrarily_large (lean/CollatzShadowing/TowerSuffix.lean:243) realizza ogni suffisso finito usando parametri che possono dipendere dal suffisso. Non costruisce un singolo parametro naturale che realizzi una parola infinita e non dice che q=1 realizzi ogni parola.

Il risultato positivo sui livelli 22–24 è un controllo tenuto separato dalla calibrazione: il drawdown di C_v(r)=305r−589J_v(r) rimane sotto 128v². Sono 28.256.725 passi, non altrettanti campioni indipendenti. La candidata per tutti i v≥15 resta aperta; l'implicazione verso il certificato è dimostrata su carta (notes/post_v6_compensation_2026-09-25/RESULTS_IT.md:29–87). Anche una prova per tutti i Q_v non darebbe da sola la copertura di tutte le sorgenti Collatz.

Il budget interlivello m_(v+1)=2m_v−Delta_v è un'identità. Maggiorare le somme pesate dei Delta equivale a propagare i margini e non fornisce una stima indipendente. Le candidate Delta_v≤2·2^ceil(v/2) e Delta_v≤4v² sono sufficienti nelle basi dichiarate, ma retrospettive e aperte (notes/post_v6_margin_2026-09-25/RESULTS_IT.md:43–120).

## Che cosa è stato falsificato

- Un prefisso binario e la relazione quadratica lasciano libero ogni suffisso superiore. PrefixOptimality.prefixMaximum_exact e certificate_iff_zeros (lean/CollatzShadowing/PrefixOptimality.lean:164,205) danno il massimo realizzabile e il criterio esatto degli zeri osservati. La formalizzazione riguarda tutti gli interi del cilindro, senza vincoli aggiuntivi sugli antenati.
- Il rinnovo locale non ricrea precisione gratuitamente: al livello 23 il certificato del modello richiede il 99,9064% dell'orizzonte superiore. Gli otto completamenti avversari preservano parola inferiore, binade, bit alti e ricorrenza; falliscono tutti già il test di un antenato intero positivo (notes/post_v6_renewal_2026-09-26/RESULTS_IT.md:19–45,117–135).
- Due antenati interi positivi, binade e parola inferiore effettiva identificano Q_v. È rigidità del punto, non un limite sul peso della sua parola (notes/post_v6_ancestry_2026-09-25/RESULTS_IT.md:176–208).
- Aggiungere precisione ternaria troncata non basta: per ogni v≥6 un quarto della precisione completa è compatibile con margini avversi. Il trasporto della congruenza non guadagna informazione indipendente (notes/post_v6_mixed_2026-09-25/RESULTS_IT.md:64–106,135–160).
- I riporti già esposti dipendono dal prefisso: sono ridondanti e non eliminano i nove avversari. Le collisioni per ogni finestra finita sono provate per input ancorati generici, non per la sola cascata dal seme 3 (notes/post_v6_binary_carries_2026-09-26/RESULTS_IT.md:46–99).
- Il riporto futuro è un vero vincolo lineare sui bit liberi. Tuttavia il testimone v16 preserva parola inferiore, bit alti e riporto corretto 31655, con Delta=31168 anziché ≤512; Q_16 effettivo ha Delta=−479. È falsificata la classe di completamenti, non la torre (notes/post_v6_carry_constraint_2026-09-26/RESULTS_IT.md:3–15,23–48,92–105).

Il ramo ternario distingue correttamente le colonne originali dalla coda adattiva. La giunzione iniziale ha un limite O(sqrt(m) log²m); propagata al tempo t, la maggiorazione degrada come sqrt(2^t), diventando banale intorno a t=v−O(log v), molto prima dell'orizzonte O(2^v). La decomposizione affine continua a essere esatta a ogni tempo. Il telescopio della coda contiene cancellazioni numericamente enormi, ma non una loro maggiorazione uniforme (notes/post_v6_propagation_2026-09-25/RESULTS_IT.md:14–32,65–100; notes/post_v6_tail_2026-09-25/RESULTS_IT.md:13–28,54–96).

## Tre domande alternative con criteri di arresto

### 1 Fattori ciclotomici della sorgente e inventario dei primi

Una struttura esatta, crescente con v, è

Q_v = prodotto_(j=0)^(v−1) F_j,    F_j=(9^(2^j)+1)/2.

I F_j sono dispari >1 e a due a due coprimi. Se p divide F_j, allora ord_p(9)=2^(j+1), dunque p≡1 mod 2^(j+1). In questa particolare famiglia non serve neppure invocare Zsigmondy per garantire nuovi primi: la coprimalità dei fattori basta. È una deduzione elementare sulla sorgente, non un risultato sulla dinamica.

Primo compito: formalizzare prodotto, coprimalità e ordine moltiplicativo; poi cercare una formula provata che trasporti parte di questa struttura ai valori di un macro effettivo. Il test iniziale deve confrontare il supporto primo della sorgente con quello degli endpoint, usando soltanto piccoli v già archiviati. Se la struttura scompare già al primo 3n+1, registrare il limite. Non basta che Q_v abbia molti primi: è perfettamente compatibile con qualunque peso di parità finora non escluso. Richiedere tutti i fattori e l'altezza può semplicemente identificare Q_v, riproducendo il limite di rigidità già noto.

### 2 Certificati sull'inverso del parametro per classi complete di parole

TowerSuffix.finite_suffix_bounded_iff (lean/CollatzShadowing/TowerSuffix.lean:265) trasforma un bound sul parametro in un criterio sul rappresentante minimo della classe. La domanda utile non è aggiungere un altro filtro di prefisso: è provare, per una classe strutturale intera di parole sfavorevoli, che il parametro minimo necessario supera il cutoff ammesso. Il criterio deve dipendere dalla formula della parola, non dal conteggio dell'orbita osservata.

Primo lemma pilota: una famiglia a lunghezza variabile di corridoi di soli esponenti 1, inseriti dopo un macro fissato, con formula esplicita del residuo inverso e del suo rappresentante minimo. Provare una disuguaglianza di altezza per tutta la famiglia. Un test finito sui piccoli livelli può confutare una soglia candidata prima della formalizzazione. Arresto: se il lemma esclude soltanto parole già eliminate dalla positività/barriera, o la soglia è selezionata dopo aver osservato Q_v, non c'è un avanzamento. Il controllo di alcune lunghe run non controlla il numero totale di dispari: servirebbe una classificazione che copra davvero le parole dannose.

### 3 Potenziale non locale della cascata di quadrati

La ricorrenza dal seme R_0=3 genera davvero la sorgente. Le impossibilità di memoria finita valgono sul dominio generico; non escludono un invariante simbolico che conservi l'intera struttura delle righe R_(a+1)=R_a². Cercare un potenziale con dimensione o descrizione crescente, invece di comprimere la cascata in finestre di ampiezza fissa.

Primo obiettivo: una disuguaglianza per il premio di un blocco congiunto che si paghi con differenze di un potenziale definito dalle righe e dai riporti del circuito, senza usare le parità future. La telescopia dovrà lasciare un costo finale stimabile indipendentemente. I primi test si fanno sui casi storici 5–12 e sui vecchi avversari, marcando quali non appartengono alla cascata dal seme 3. Arresto: se il potenziale è definito usando Delta o il numero futuro di dispari, il metodo è circolare; se vale soltanto come identità, non è la stima cercata. Rischio alto: nessun invariante simile è stato ottenuto durante l'analisi.

## Controllo della nuova fonte sulle S unità

Il paper di Verger-Gaugry, caricato il 9 novembre 2026, assume un'orbita divergente e dimostra una restrizione sui primi generati dai minimi delle onde sotto un bound sulle altezze delle onde. Non dimostra Collatz. [Fonte primaria](https://arxiv.org/html/2611.14569v1), Teorema 1.2 e definizione di Prm(µ).

Una deduzione interna da sottoporre a controllo può precisarne l'interfaccia. Per ogni wave-minimum µ, l'altezza è almeno 2 e la definizione include T²(µ) anche quando l'altezza è esattamente 2. La formula locale della mappa shortcut dà

9(µ+1)−4 = 4 T²(µ).

Se tutti i primi generati appartenessero a un insieme finito P, poniamo S=P∪{2,3}. I razionali positivi U=9(µ+1)/4 e V=T²(µ) sarebbero S-unità e soddisferebbero U−V=1. Assumendo il classico teorema di finitezza delle soluzioni in S-unità, esisterebbero soltanto finitissime coppie (U,V), quindi finitissimi µ. Un'orbita divergente è iniettiva e ha infiniti minimi d'onda distinti: contraddizione. Questa deduzione sembra non richiedere un limite uniforme alle altezze delle onde; non è formalizzata e non rivendica priorità. È motivo per verificare la mappatura degli enunciati della nuova fonte prima di investirvi. In ogni caso infiniti primi generati restano compatibili con divergenza, e non forniscono il budget di parità.

Precisazione della revisione incrociata: se i minimi d'onda fossero finiti, una coda avrebbe solo run dispari shortcut di lunghezza uno, dunque esponenti Syracuse almeno 2 e discesa stretta sopra 1. Una run dispari infinita non è possibile per un positivo: la formula affine richiederebbe `2^k | n+1` per ogni k. Questo è il lemma necessario per giustificare gli infiniti minimi d'onda prima di applicare il teorema delle S-unità.

## Verifiche effettuate

Piccolo controllo in aritmetica intera: prodotto e coprimalità dei F_j per v=1..7; formula delle onde e identità a r=2 per 500 sorgenti µ≡3 mod4 sotto 2000. Tutti i controlli passano. Non sono prove degli enunciati uniformi e non aggiungono livelli della torre. Le identità e i limiti esposti sopra sono deduzioni su carta, non nuove dichiarazioni Lean.
