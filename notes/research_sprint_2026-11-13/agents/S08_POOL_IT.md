# S08 Il pool dei fratelli laterali e il carico reciproco

13 novembre 2026. Nuovo modulo esclusivo `lean/CollatzShadowing/SiblingPool.lean`. Il risultato collega il meccanismo dei pool non ricorrenti, integrato indipendentemente dalla fonte Shaik in `RootPoolBudget`, alla geometria effettiva dei fratelli già formalizzata nel progetto.

## Il ponte matematico

Sia f una funzione deterministica, x una sorgente con spina `i↦f^[i](x)` iniettiva e y_i un fratello laterale diverso da `f^[i](x)` ma con lo stesso successore `f(y_i)=f^[i+1](x)`. Allora il pool `range(y)` non contiene nessun iterato positivo di un suo membro, incluso il membro stesso.

La prova combina due fatti già presenti in `SiblingBasins`: se un fratello raggiunge un altro fratello, gli indici coincidono; un fratello non ha ritorni positivi. Ne segue non soltanto il nonritorno separato delle singole radici, ma l'assenza di collegamenti fra tutte le radici del pool. Ogni sottoinsieme conserva la proprietà.

La specializzazione `y_i=canonicalSibling(S^[i](x))` usa il successore comune e la crescita stretta del fratello canonico. Questa implicazione geometrica non richiede ulteriori ipotesi di parità, positività o non divisibilità per 3 sulla spina; l'iniettività resta una premessa esplicita. I domini aritmetici richiesti da H e dalle stime sui predecessori rimangono distinti.

## Nuova applicazione del carico forte

Per una sorgente z>0, un insieme finito W di parole distinte esatte da z, con endpoint R_w appartenenti a un blocco finito o all'intero pool dei fratelli canonici, si ottiene

`Σ_(w∈W) ω(w)/R_w ≤ 1/z`.

Il limite non cresce con il numero dei fratelli. Se metadati diversi duplicano la stessa parola, il coefficiente totale per parola deve essere limitato da M≥0 e il limite diventa M/z. La corrispondenza con `RootPoolBudget` conserva esattamente la normalizzazione e le parole fisiche; non usa una distribuzione di riferimento o un'ipotesi di mixing.

Le otto dichiarazioni pubbliche sono: `nonrecurrentPool_mono`, `sibling_range_nonrecurrent`, `sibling_subpool_nonrecurrent`, `canonical_range_nonrecurrent`, `canonical_finite_nonrecurrent`, `canonical_word_charge_le`, `canonical_finite_word_charge_le` e `canonical_labeled_word_charge_le`.

È un'integrazione formale di un meccanismo esterno con risultati locali, non una rivendicazione di nuova priorità per il principio elementare del pool. Il codice della fonte non viene importato o copiato nel modulo; l'attribuzione e il commit della fonte sono registrati nel modulo e nel rapporto `RootPoolBudget`/S02.

## Cosa manca per H aggregata

Il limite reciproco controlla un **carico superiore** per sorgente. Non dimostra che una quota positiva delle sorgenti del bacino di base generi parole che arrivano al blocco dei fratelli. Non costruisce il flusso relativo e non stima le altezze delle immagini.

Per applicare `RelativeMassFlow.disjoint_block_flow_budget` restano tre obblighi fisici:

1. Costruire le stesse incidenze effettive fra sorgenti di base e immagini nei bacini dei fratelli, con parole esatte, fonte e destinazione specificate, e cutoff d'altezza verificato.
2. Usare il budget sul lato corretto delle incidenze, dopo aver raggruppato per intero fisico. Un cap sulle etichette di una parola non è automaticamente il carico incoming delle immagini di un altro trasporto.
3. Minorare la massa relativa di quelle incidenze rispetto al conteggio del bacino di base, con errori sublineari e coefficienti netti che non siano sommabili sui blocchi. È la parte ancora aperta.

Il carico reciproco è `1/v` alla sorgente fisica v della parola inversa, non un cap numerico costante. Per sostituirlo con `1/X` serve una fascia con `v≥X`, dopo la quale si può riscalare il flusso di un fattore X. Un solo cutoff superiore `v≤DX` non dà tale maggiorazione. In alternativa bisogna conservare il profilo variabile `1/v` nell'allocazione a soglia e dimostrare la minorazione con gli stessi pesi. È un punto di raccordo quantitativo da dichiarare, non una stima gratis dal pool.

Il ponte Syracuse→mappa ordinaria per un'unione di radici deve includere la parte dispari delle sorgenti e i lift diadici. La mappa S del progetto è totale sui naturali, ma le sue applicazioni alla dinamica ordinaria richiedono il dominio corretto: il budget astratto da solo non sostituisce questa identificazione.

Anche se il confronto riuscisse e fosse unito alla positività iniziale, la conseguenza prevista riguarderebbe orbite non periodiche; i cicli non banali resterebbero separati.

## Confronto fra agenti

Ho inviato a S06 la distinzione fra carico per parola e incoming per immagine, e la necessità di conservare le sorgenti fisiche e i lift ordinari. A S07 ho segnalato che gli endpoint consecutivi delle macro `[1,2]^r` sono annidati sulla stessa orbita e non costituiscono questo pool: per loro si conserva il budget dissipativo generale, non quello forte.

L'iniettività dell'intera spina è diversa dall'iniettività di un prefisso campionato. Su un'orbita convergente, un pool finito può essere certificato con percorsi completi che escludano collegamenti fra le radici; un semplice prefisso non basta. Questa è una condizione di validità del certificato, non un ostacolo numerico eliminato dai nuovi lemmi.

## Verifica

Elaborazione dedicata **PASS, exit 0**, senza errori o avvisi. Comando dalla directory `lean`: `lake env lean CollatzShadowing/SiblingPool.lean`. Il log `verification/s08_pool.log` è vuoto. Le otto dichiarazioni usano l'ambiente locale Lean 4.29.1 e le dipendenze compilate già disponibili: non è una build fredda o un replay con kernel indipendente.

Ricevuta con hash sorgente e log in `verification/s08_pool.json`. Audit predisposto in `verification/s08_pool_axioms.lean`, non eseguito da S08; il controllo complessivo viene lasciato al reviewer della sessione. Nessun altro modulo, entrypoint o dipendenza modificato da S08.
