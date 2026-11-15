# S05 Allocazione finita a soglia e controllo delle capacità

13 novembre 2026. Integrato e verificato il modulo locale `lean/CollatzShadowing/CapacityAllocation.lean`: **sette teoremi**, una definizione, elaborazione dedicata riuscita con exit 0 e log vuoto. Nessun `sorry`, `admit`, nuovo assioma o `native_decide`; nessuna modifica all'entrypoint o ad altri moduli. Il controllo delle dipendenze assiomatiche sarà svolto nell'audit integrato della sessione.

## Meccanismo esterno e prova locale

Le fonti sono i moduli `Counting/ProfileThreshold` e `Counting/ProfileDuality` di Idris Ali Shaik, al commit fissato `f0fda887ee60dc8ac4ef0d864935148b03734726`, letti nella selezione con licenza e hash raccolta da S01. La [fonte del certificato a soglia](https://github.com/shaikidris/CollatzConvergencePositiveDensity/blob/f0fda887ee60dc8ac4ef0d864935148b03734726/WordCertDensity/Counting/ProfileThreshold.lean) e la [fonte della dualità](https://github.com/shaikidris/CollatzConvergencePositiveDensity/blob/f0fda887ee60dc8ac4ef0d864935148b03734726/WordCertDensity/Counting/ProfileDuality.lean) sono attribuite nel nuovo modulo. Si tratta di un'integrazione locale del meccanismo finito: nessun sorgente esterno, ottimizzatore o risultato analitico è importato.

Per un insieme finito I di celle fisiche, coefficienti `0≤c_r≤C`, punteggi h_r e domanda pagata `p≤Σ c_r h_r`, ogni soglia t>0 dà

`max(p−C Σ max(h_r−t,0),0)/t ≤ Σ c_r`.

La prova (`threshold_lower_bound`, riga 52) parte dalla disuguaglianza puntuale

`c_r h_r ≤ t c_r + C max(h_r−t,0)`.

Il cap controlla quanto le poche celle dal punteggio alto possano pagare. La restante domanda richiede altre celle: questo usa l'intero profilo, invece del solo massimo. La forma dimostrata ammette anche punteggi firmati; nelle applicazioni ai conteggi si possono imporre punteggi nonnegativi.

`IsThresholdAllocation` richiede celle piene sopra la soglia e vuote sotto di essa, lasciando liberi i pareggi. `threshold_allocation_exact` (riga 84) prova che una tale allocazione con massa esatta p satura il bound. `threshold_certificate_le_competitor` (riga 108) confronta il certificato con ogni allocazione concorrente capped che paghi p. Non è dimostrata qui l'esistenza generale di un allocatore greedy. `threshold_at_score_upper_bound` (riga 120) recupera il bound uniforme `p/max h` scegliendo la soglia al massimo.

## Controllo esatto e miglioramento effettivo

Il [probe](../experiments/s05_capacity.py) usa soltanto frazioni esatte e controlli attivi anche con Python ottimizzato. Esamina **1.884 profili**, **33.912 disuguaglianze** e **1.026 certificati di uguaglianza**, tutti superati. L'output normale coincide byte per byte con quello prodotto con `-O`; i risultati sono conservati in [s05_capacity.json](../verification/s05_capacity.json).

Un esempio sintetico dimostra un guadagno anche dopo l'arrotondamento del conteggio: h=(10,1,1), C=1, c=(1,1,1), p=12. Il solo massimo dà `Σc≥6/5`, quindi almeno due celle intere; la soglia t=1 dà esattamente `Σc≥3`. Un secondo esempio c=(1,1/2,0), p=21/2 mostra il pareggio a soglia e la saturazione frazionaria `Σc=3/2`. Questi sono problemi finiti sintetici, non stime di masse Collatz.

Il probe conserva due test negativi. Eliminare il cap rende il bound falso: con h=(10,1), c=(2,0), p=20 e cap impropriamente fissato a 1, il bound pretenderebbe 11 mentre l'allocazione totale è 2. Inoltre due etichette della stessa cella non sono due interi distinti: i loro coefficienti vanno aggregati prima di applicare il cap.

## Confronto fra agenti e applicazione al progetto

Ho dialogato con S04 sul dizionario congiunto. A lunghezza k fissata, le parole esatte che terminano nello stesso target identificano sorgenti distinte: celle fisiche=parola/sorgente possono quindi avere cap C=1 per indicatori o frazioni selezionate. Aggregando invece per il solo residuo ternario, il cap 1 non segue: molte sorgenti possono occupare la stessa cella di residuo. A k e A entrambi fissati il peso è uniforme, dunque la soglia non migliora il bound; il vantaggio richiede punteggi variabili, per esempio cataloghi con A differenti che conservino k e identità delle sorgenti.

Ho inoltre scambiato osservazioni con S03 e S06. Gli endpoint successivi dei blocchi crescenti sono annidati e non soddisfano la condizione di pool nonricorrente: per loro rimane il budget dissipativo universale di S02. Le diverse surgery `(i,delta)` di S06 possono produrre la stessa immagine; il cap deve essere verificato sul carico aggregato per immagine, non sulle etichette delle trasformazioni.

Il risultato successivo del censimento S06 rende il limite concreto: alcune immagini hanno carico 2 anche dopo aver identificato le coppie duplicate `(u,v)`. L'iniettività del dizionario superiore parola→sorgente non impedisce che due diverse sorgenti inferiori siano trasportate allo stesso codice superiore. Il cap 1 di un catalogo fisico non diventa automaticamente un cap 1 per il flusso entrante; quel carico resta un obbligo distinto.

Una composizione utile con `RootPoolBudget` consiste dunque nel costruire prima un catalogo fisico con un cap dimostrato, assegnargli il punteggio della stessa incidenza e applicare il certificato a soglia. Se il catalogo è una vera linea d'arresto, il carico reciproco sharp può evitare una perdita aggiuntiva; se contiene ritorni, si usa la normalizzazione dissipativa. In entrambe le situazioni **la minorazione p resta una premessa esplicita**.

## Decisione scientifica e v7

Il modulo aggiunge un componente verificato, utile per progettare un flusso relativo senza perdere il profilo dei carichi. Il primo esperimento reale giustificato è un catalogo cross-A con sorgenti identificate, un cap per ciascuna cella fisica e una domanda p proveniente dallo stesso modello. Arrestare la pista se si usa una massa marginale di riferimento, si assumono cap su soli codici o si presenta l'ottimizzazione come generazione gratuita di massa.

È un'integrazione di un meccanismo finito già presente nella fonte e di algebra elementare, con attribuzione: può sostenere la sezione di strumenti verificati di una v7, ma da sola non costituisce una nuova minorazione di densità, una prova di H o un avanzamento puntuale della congettura. La novità matematica della prosecuzione deve essere cercata nella costruzione effettiva delle incidenze e della loro massa relativa.
