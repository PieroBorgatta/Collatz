# Cambiare rappresentazione può aiutare; dimenticare il percorso no

16 novembre 2026, lettura concettuale di tre fonti primarie. Nessun solver, esperimento o compilatore è stato avviato. Questa nota serve a valutare un possibile strumento, non a proporre un'altra soluzione nominale della congettura.

## Semigruppi e percorsi effettivi

[Applegate–Lagarias, The 3x+1 Semigroup, v2](https://arxiv.org/html/math/0411140v2), introduzione e Theorem1.1, prova una caratterizzazione completa del semigruppo moltiplicativo generato dai rapporti delle transizioni. Gli autori distinguono esplicitamente la fattorizzazione nel semigruppo dall'esistenza di una vera traiettoria: si possono concatenare fattori senza che gli stati intermedi siano quelli richiesti dalla mappa. Il risultato è pubblicato in [Journal of Number Theory117 (2006),146–159](https://doi.org/10.1016/j.jnt.2005.06.010).

Per il nostro controller, un'identità fra gain o una fattorizzazione di un grande carry non basta. Occorre un lemma di sollevamento che mantenga gli stati interi, positivi e unità, e il colore del primo genitore. Anche una rappresentazione corta nel gruppo affine può usare inverse o passaggi che non sono rami Collatz leciti. Non è stata dimostrata una scorciatoia di questo tipo.

## Il limite di un metodo dipende dalla codifica

[Yolcu–Aaronson–Heule, An Automated Approach, v3](https://arxiv.org/html/2105.14697v3), §§3.1.1–3.2, dimostra un'impossibilità per interpretazioni matriciali naturali della codifica unaria studiata, anche con dependency pairs. Il passaggio a rappresentazioni miste binarie–ternarie conserva il significato aritmetico dei passi e sfugge a quello specifico argomento negativo. Le loro prove automatiche riguardano varianti e indebolimenti, non la congettura completa.

Questa è una ragione concreta per non giudicare inutile ogni riformulazione equivalente. Una nuova codifica può consentire una classe di prove prima esclusa. Tuttavia, per il progetto, va indicata la nuova regola o disuguaglianza che diventa accessibile: il solo cambio di nomi da traiettoria a F, rango o linguaggio non lo dimostra.

Un possibile uso strumentale è descrivere il controller come riscrittura relativa fra due cammini validi, con regole di cambio base che conservino il valore. Il suo debito fisico resta però `E=(B−A)−Δℓlog₂3`: scrivere un esponente enorme in pochi simboli non ne riduce il costo B. La terminazione di una normalizzazione sintattica non è un bound sul debito né la produzione di un altro ramo. Il primo lemma utile dovrebbe conservare questi due dati, non soltanto la lunghezza della descrizione.

## Frontiere probabilistiche e interi eccezionali

[Brofferio, The Poisson boundary of random rational affinities](https://www.numdam.org/articles/10.5802/aif.2191/), Annales de l'Institut Fourier56 (2006),499–515, descrive sotto ipotesi di momento la frontiera mediante le componenti reali e p-adiche che contraggono in media. Il risultato riguarda il random walk della legge data; non identifica automaticamente ogni condizionamento eccezionale a un intero con una fibra reale diagonale.

Per la legge Doob del progetto, l'ipotesi ingenua che il perpetuity reale sia uguale al target intero è anzi smentita dal bound di primo arrivo: sui root nonperiodici `A_mY_m≥n/P₀`, quindi il residuo reale resta positivo. La fibra va identificata nella versione canonica corretta, come controllato da H03 nella fonte19. Questo abbandona un'applicazione sbagliata della teoria delle frontiere, non la teoria stessa.

## Decisione

Tenere le codifiche che conservano offset e legalità, e la distinzione fra comportamento medio e fibre aritmetiche. Abbandonare come argomenti sufficienti fattorizzazioni senza percorsi, compressione della descrizione senza bound sul debito, o condizionamenti reali assunti senza identificarne la legge. Nessuna di queste letture fornisce ancora l'editor o il lower laterale mancanti.
