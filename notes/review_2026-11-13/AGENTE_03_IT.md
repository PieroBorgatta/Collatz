# Analisi 3 Storia scientifica e obblighi residui

Incarico svolto dall'agente `03_storia_gap`, tramite cronologia Git, documentazione corrente e note post-v6.

La sequenza scientifica passa dai tentativi empirici e quasi-Lyapunov di aprile–maggio alla formalizzazione Lean di maggio, quindi ai certificati spettrali finiti e al problema del ponte infinito. I risultati di precisione, switching, cilindri e cicli sono integrati nella v6. La continuazione del 24 settembre costruisce sezione aritmetica, torri, occupazione e adapter dei predecessori; le ottimizzazioni dell'overlay sono il risultato quantitativo positivo più concreto di questa fase.

Fra il 24 e il 26 settembre, i tentativi sulla torre `Q_v` producono certificati sino a v24 e numerosi controesempi alle classi semplificate. Il commit `1f5d481` chiude i filtri e introduce il confronto relativo H; `e9e99fb` e `5428e89` delimitano ed escludono i trasporti più semplici. La prova asintotica di H.2 è su carta, con sei lemmi di supporto Lean.

Le tre domande da mantenere distinte sono convergenza universale, discesa della torre speciale e densità dei predecessori. Risolvere la torre non dà una copertura globale. La positività dei bacini, con costanti dipendenti dal target, non dà H. Anche H insieme alla positività escluderebbe orbite non eventualmente periodiche, lasciando il problema dei cicli non banali.

Tre alternative individuate: domini esatti dei ritorni composti; trasformazioni di parole inverse che cambino costante affine e profondità; confronto aggregato di blocchi di fratelli. Quest'ultimo può tollerare forti asimmetrie fra singoli bacini, ma richiede una vera disuguaglianza relativa finita con errori controllati. Non basta scrivere la divergenza della massa desiderata come nuova ipotesi.

Fonti locali principali: `notes/post_v6_reset_2026-09-26/CRITICAL_MAP_IT.md:27,72,118`, `NEW_DIRECTION_IT.md:42,61,197`, `notes/post_v6_signed_mass_2026-09-26/RESULTS_IT.md:5,19`. Nessuna contraddizione matematica sostanziale trovata tra lo stato corrente e i teoremi consultati. I conteggi correnti sono stati riprodotti distinguendo prove d'autore e certificati generati.
