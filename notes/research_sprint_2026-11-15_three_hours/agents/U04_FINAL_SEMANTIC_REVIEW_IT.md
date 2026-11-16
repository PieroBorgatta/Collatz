# U04 — Audit finale del rinnovo e del prototipo massimo

16 novembre 2026. Lettura indipendente dei due snapshot indicati nella ricevuta. Nessun esperimento, build, importazione nel progetto principale o modifica degli originali.

**PASS:** U15_LADDER_OBSTRUCTION_IT.md, SHA `2a993d34425e1178f4b438e7a66bc43218e57a0d4695f5ac158d0b4eda5ba182`; MaxEnvelopePrototype.lean, SHA `c640f8cd46ee70772c5f0f3c0dc1795b912b05923bd9a3d6e92c7c8343562836`. La compilazione e l'audit degli assiomi del secondo sono quelli registrati da U06, non una nuova esecuzione di U04.

## 1. Rinnovo di primo crossing

Il primo crossing inverso stretto di uno appartiene al catalogo finito. Solo un ultimo esponente uno può attraversare, quindi 1<a≤3/2; il termine affine positivo implica u<n. Il cap1 e la partizione di primo crossing danno h=g−Tg. Ogni record finale si decompone univocamente in crossing successivi relativi, e viceversa; l'altezza intera scende a ciascuno, quindi il rinnovo al root è una somma finita di potenze di T. La stessa decomposizione del witness ottimale prova F=max(1,max_C aF(u)). Il rango è il numero di record e non controlla la durata fra essi.

Per un crossing u→n al root nonreturn, ogni prefisso forward non vuoto ha gain≥a>1: il suffisso inverso complementare è proprio e ha gain≤1. Gli stati restano quindi sopra u. Con l'input high-tail sui cammini distinti, il prodotto correttivo è 1+O(u^(−δ)). Il primo bound u≥n/[(3/2)P₀] permette di sostituire u con n nell'errore e dà la località enunciata. I cicli ripetuti sono esclusi da questo passaggio.

## 2. Modello astratto: ciò che effettivamente ostruisce

Le unità dispari hanno gap al più quattro, quindi la catena n_j definita nella nota cresce geometricamente. La densità dei monomi 3^k/2^E permette di imporre il deficit d_j=n_j−a_jn_(j−1)∈(1,2), con E fra k e2k scegliendo k grande. I gain possono persino essere ordinati come un firstcross astratto: prima gli esponenti due, poi gli uno; siccome 1<a_j<3/2, ogni prefisso proprio ha gain≤1. Questo fatto non aggiunge l'offset affine mancante.

L'identità h=g−Tg, il floor h>1/n₀ e il limite F(n_j)/n_j=(1/n₀)Π(1−d_i/n_i)>0 sono corretti. La catena ha O(log X) elementi fino a X, quindi le medie di h sulle unità di ogni classe residua fissa ammissibile tendono a uno. Un solo arco uscente produce surplus ladder zero.

È un ostacolo nel sistema astratto dichiarato. Non realizza i veri offset Syracuse né tutti i genitori interi, e non definisce il surplus fisico A del problema originale. Non confuta una prova che usi tali informazioni aggiuntive.

## 3. Sei enunciati del massimo: corrispondenza semantica

`IsUnitSeed` richiede positività, disparità e non divisibilità per tre. `Admissible n w` richiede un seed di quel tipo e una parola effettiva con endpoint n. Non impone primo arrivo o assenza di ritorni. Il catalogo BoundedSlopeCatalogue(n,1) include tutte le parole di gain≥1 da sorgenti positive; filtrarlo per Admissible produce esattamente la parte unità desiderata. Inserire il gain uno rende totale la definizione anche fuori dal dominio valido.

| Enunciato | Contenuto effettivo e dominio | Esito |
|---|---|---|
| one_le_envelope | F≥1 a ogni target naturale | PASS |
| wordWeight_le_envelope | Ogni parola ammissibile è dominata, anche sotto uno | PASS |
| exists_maximizing_word | A target unità valido, il massimo ha un vero witness unità; la baseline è realizzata dalla parola vuota | PASS |
| envelope_le_target | F≤n a target unità valido, dal potenziale Ωu≤n e u≥1 | PASS |
| optimal_source_bound | Qualunque sorgente positiva di una parola che realizza F soddisfa u≤n/F | PASS |
| envelope_le_of_word_majorant | F è il minimo maggiorante numerico dei gain ammissibili al target valido | PASS |

I cicli non richiedono eccezioni perché il catalogo finito contiene tutte le parole sopra soglia, incluse quelle con ritorni. `optimal_source_bound` è leggermente più generale nella sorgente: la prova usa solo positività e il potenziale, non un nuovo requisito di unità. Le conclusioni di raggiungimento e F≤n conservano correttamente la guardia sul target. La definizione noncomputabile non fornisce un criterio per escludere arrivi ignoti mediante timeout.

Il lemma finale riguarda un maggiorante dei gain di tutte le parole al medesimo target. Non è ancora una supersoluzione per archi o una ricorrenza max-plus. Nessun g, Q, densità, lower di A, rate di clock o conclusione Collatz compare nelle sei specifiche. L'audit transitivo presente nel sorgente ammette soltanto gli assiomi standard dichiarati; la sua esecuzione è documentata dalla ricevuta U06.

## 4. Minimo unità e asintotica del surplus

Audit aggiuntivo di U15_MINIMUM_SEED_ASYMPTOTIC_IT.md, SHA `671e584f107f0570350e3a47507cbe056703681863ca7209d3817deacb634bec`. Il primo arrivo dal minimo seed unità m a n ha tutti gli stati dispari unità≥m, perché sono anch'essi seed che raggiungono n. Gli stati shortcut pari sono almeno il successivo odd e quindi anch'essi≥m. Il segmento è iniettivo anche a target periodici. La coda U09 si applica con R=floor(log₃₂m), dando P≤exp(E(m)/3) e quindi

`exp(−E(m)/3)n/m≤F(n)≤n/m`.

Il prodotto affine di un solo ramo restituisce esattamente il fattore `1−1/(2^e n)` nel confronto M_x/n con 1/m_U(x). Non si identifica per questo il minimo seed con il seed ottimale.

Su una spine divergente, ogni seed unità limitato può raggiungere un ramo laterale soltanto al suo primo ingresso nella spine; dopo l'ingresso il suo predecessore fisico è quello osservato. Il pool finito dei seed≤R contribuisce quindi soltanto finitissimi indici laterali. Ne segue che il minimo M_j di tutti i minimi laterali tende uniformemente a infinito.

La somma S_j=Σ_off1/m_U(x) è finita: E(m)≤82 e il fattore affine è almeno1/2, quindi il lower per coordinate la confronta con LF(n_j)/n_j tramite una costante positiva uniforme. Dopo la stabilizzazione del ramo ottimale, A è esattamente la somma dei M_x laterali. La sandwich della nota, con E(M_j)→0 e n_j→∞, dà

`A(n_j)/n_j=(1+o(1))S_j`.

**PASS** con l'input high-tail U09 e la stabilizzazione già verificata. La costante asintotica è uno ma non è noto un rate del minimo laterale. Il minimo seed globale è inoltre intero non crescente lungo la spine, dunque si stabilizza; questo non identifica il suo gain con l'ottimo. Nessun lower S_j≥c/log n_j è stato ottenuto.

## 5. Estensione algebrica standalone: semantica

Su CompositionPrototype.lean congelato, SHA `d199434cf12f96c042e133810d269437773cac1d65295f853f06d156b39faefa`, il prefisso core è identico byte per byte e i nuovi enunciati pubblici sono tre. U04 dà **PASS semantico**. U06 ha completato il secondo controllo con exit0 e audit transitivo degli assiomi PASS: 18 dichiarazioni core, di cui8 private, più4 dichiarazioni dell'estensione, di cui una privata. U04 non ha rieseguito la build.

`envelope_composition` sceglie un vero witness ottimale v verso u e lo concatena forward con la parola w da u a n. Il gain moltiplica e la parola composta è ammissibile, quindi Ω(w)F(u)≤F(n). Non serve nonritorno.

`maximizing_seed_baseline` applica questa disuguaglianza a una parola ottimale di gain F(n) e cancella F(n)>0; F(u)≤1, unito alla baseline, dà F(u)=1.

`maximizing_prefix_calibrated` applica la composizione al suffisso e cancella il suo gain positivo. Ottiene F(z)≤Ω(prefisso), mentre l'effettività del prefisso dà il verso opposto. La validità unità dell'intermedio z è un'ipotesi esplicita hz, non una conclusione formalizzata automaticamente. Prefissi e suffissi vuoti sono inclusi. Non vengono aggiunti g, densità, profili, lower o algoritmi effettivi.
