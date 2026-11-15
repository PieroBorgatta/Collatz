# Analisi 7 Densità dei predecessori e pool di radici

13 novembre 2026. Analisi interna in sola lettura di sorgenti e documenti; nessun rebuild dell'overlay. La libreria principale e l'overlay mantengono correttamente separati i loro confini di verifica. La prossima difficoltà utile è il confronto relativo di masse selezionate con controllo dei singoli interi, non una nuova ottimizzazione dei lower bound assoluti.

## Cosa è già ottenuto

`WeightedVisits.lean:107` limita la somma delle dissipazioni lungo qualunque insieme finito di tempi a `1/x`. Il suo corollario per visite al target R (`:117`) dà `Σω≤R(3R+1)/x`. `WeightedWords.lean:17` prova che due parole esatte della stessa lunghezza e stessa sorgente coincidono; il limite alle visite passa così alle parole senza contare più volte lo stesso tempo. `WeightedPredecessors.lean:33` controlla ogni fibra di sorgenti e `:150` converte massa selezionata in un conteggio di predecessori ordinari distinti. La stima analitica e il suo budget restano premesse esplicite a `:172`.

`NonreturnCounting.lean:19` rende unico il tempo di arrivo a un target senza ritorni positivi. Si sostituisce così il coefficiente `K=R(3R+1)` con `K=R`, ma la minorazione analitica resta assunta a `:173`. Le coppie di semi (`TwoSeed.lean:18,74,123`) garantiscono una scelta limitata senza ritorni, anche quando il loro successore è periodico; non decidono il candidato e non provano convergenza.

L'overlay già compone queste idee con il mixing esterno. `OptimizedDensity.lean:85` espone il parametro di mixing e `:163` il conteggio condizionale; `:139–158` definisce limite della radice, conduttore e coefficiente. La nota `post_v6_optimization_2026-09-24/RESULTS_IT.md` documenta l'ottimizzazione verificata di semi e decadimento di ordine sei: coefficiente maggiore e cutoff minore rispetto alla precedente via uniforme dei due semi. Sono miglioramenti quantitativi effettivi dello stesso risultato assoluto, senza comparabilità fra bacini diversi.

La verifica storica riportata è di 399 moduli, con 398 ricevute riusate e uno ricompilato nell'ultimo run; non un rebuild freddo completo né un kernel indipendente. La ricognizione web coordinata segnala un successivo rebuild ProofAtlas dei 388 moduli locali esterni e nuovi root scores nel repository Shaik di ottobre. Non ho ricompilato né adottato quelle nuove dipendenze.

## Perché la positività non dà H

H richiede `d_*(B(h(n)))≥c/(1+log n)·d_*(B(n))` nel dominio senza ritorni, con c uniforme. I coefficienti dell'overlay danno solo `d_*(B(n))≥c_n>0`. Anche una formula esplicita favorevole per `c_h/c_n` non controlla il rapporto delle densità vere: la densità di base può essere molto maggiore del proprio lower bound. Né un limite `d_*(B(a))≥c/a` basta lungo una spina di crescita esponenziale, perché la serie dei reciproci può essere sommabile.

Per i pool c'è un ulteriore requisito: il nonritorno di ciascuna radice non impedisce che due radici siano sulla stessa traiettoria e abbiano bacini annidati. Occorre una linea d'arresto/antichain nella raggiungibilità, oppure un budget di carico condiviso che tolleri esplicitamente tale sovrapposizione. Le diverse etichette di una costruzione non sono automaticamente sorgenti distinte.

## Primo lemma proposto Un budget normalizzato per più target

Stato C: deduzione su carta dai lemmi Lean esistenti, non nuova dichiarazione compilata e senza rivendicazione di priorità.

Siano x>0 e W un insieme finito di parole distinte, tutte esatte da x. Per ogni w sia `R_w=evalSyracuseWord(w,x)>0` e `ω(w)=3^|w|/2^sum(w)`. Allora

`Σ_(w∈W) ω(w)/[R_w(3R_w+1)] ≤ 1/x`.

Ogni addendo è esattamente `loss(x,|w|)`. Le lunghezze delle parole sono iniettive per `WeightedWords.matches_eq_of_length_eq`, e `WeightedVisits.sum_loss_finset_le` applicato alla loro immagine conclude. Sono ammessi la parola vuota, target differenti, ritorni e target periodici. Per incidences etichettate che ripetono una stessa parola occorre prima aggregare le etichette e imporre coefficiente totale al più uno.

Questo evita di spendere un budget indipendente per ciascuna radice. Se tutte le sorgenti sono almeno X, il consueto raggruppamento dà `massa normalizzata ≤ card(sorgenti)/X`. L'input analitico deve però minorare proprio questa massa normalizzata: il risultato non produce gratuitamente un nuovo coefficiente di densità.

Controllo E aggiuntivo: 3.200 verifiche con frazioni esatte (40 sorgenti dispari 1..79, 80 passi), sia telescopio completo sia sottoinsiemi di tempi, incluse visite ripetute a 1. Il test controlla l'identità implementata; la dimostrazione generale è quella sopra.

## Tre enunciati finiti per un confronto effettivo

1. **Incidenze congiunte e altezza.** Per famiglie inverse selezionate registrare insieme profondità k, somma A, costante affine C e residuo ternario, verificando `3^k v+C=2^A y`, positività, valutazioni esatte e `v≤DX`. La selezione deve avere un budget fissato prima del censimento; cambiare profondità e più esponenti evita il dominio chiuso da H.2. Una legge marginale dell'offset non dà la legge congiunta sotto il vincolo d'altezza. Test: enumerazione indipendente dei piccoli `(k,A)` e ricerca di celle ammesse ma vuote, con cutoff e tempi espliciti.

2. **Carico condiviso delle immagini.** Costruire pesi nonnegativi `q(u,v)` sulle incidenze effettive fra sorgenti del bacino inferiore e immagini ammissibili del bacino superiore. Provare `Σ_u q(u,v)≤M` per ogni intero v, con M controllato uniformemente. Il lemma normalizzato sopra è una possibile infrastruttura; se si usano altri pesi, serve il loro confronto esplicito con la dissipazione. Test: sorgenti duplicate, radici annidate, differenti etichette della stessa parola e ritorni. Arrestare se il carico cresce col numero di radici senza compensazione.

3. **Massa relativa, l'obbligo nuovo.** Provare `Σ_(u,v)q(u,v)≥θ_n |B(n)∩[1,X]|−E_n(X)`, dove `θ_n≥c/(1+log n)` ed `E_n(X)=o_n(X)`, per le stesse incidenze dei due lemmi precedenti. Allora `|B(h(n))∩[1,DX]|≥θ_n/M·|B(n)∩[1,X]|−E_n(X)/M`. Questa conversione è elementare; la minorazione relativa è la parte non dimostrata. I root scores aiutano solo se misurano una frazione della massa di base effettiva, o se forniscono anche un upper bound comparabile della densità di base. Arrestare se si confrontano soltanto due lower bound assoluti o si assume l'indipendenza dei residui lungo la traiettoria.

## Variante aggregata per blocchi

Sia `x_i=S^i(x_0)` una spina iniettiva ammissibile e siano `y_i=h(x_i)` i fratelli. I bacini dei y_i sono disgiunti per `SiblingBasins.lean:77` e il packing finito è a `:113,133`. Poniamo `U_j=∪_(2^j≤i<2^(j+1)) B(y_i)`.

Un enunciato sufficiente alternativo a H sarebbe: esistono c,D>0, indipendenti da j (possono dipendere dalla spina fissata), tali che per ogni j e X sufficientemente grande,

`|U_j∩[1,DX]| ≥ c |B(x_0)∩[1,X]|−E_j(X)`, con `E_j(X)=o_j(X)`.

Se `δ=d_*(B(x_0))>0`, ogni blocco avrebbe densità inferiore almeno `cδ/D`. I blocchi sono disgiunti, quindi una somma finita di J blocchi avrebbe densità almeno `Jcδ/D≤1`, impossibile per J arbitrario. Non occorre un cutoff X uniforme in j: si sceglie prima un numero finito di blocchi e poi si passa al limite. Lo stesso vale per errori controllati separatamente in ogni blocco.

H puntuale fornirebbe un lower bound uniforme della somma delle densità nei blocchi, usando `x_i≤2^i x_0`. La variante può tollerare singoli fratelli estremamente piccoli e permettere compensazioni fra costi ternari. Tuttavia rimane un'ipotesi forte: senza una costruzione finita indipendente il nuovo enunciato riformula soltanto la massa divergente desiderata. Il primo esperimento utile è un flusso finito tra un pool della base e l'unione delle immagini del blocco, con conteggi interi distinti, carico e costi di altezza espliciti; non un altro rapporto stimato su cutoff più grandi.

La conclusione eventuale escluderebbe orbite non periodiche. Il ramo dei cicli non banali rimane distinto.
