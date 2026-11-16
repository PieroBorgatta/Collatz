# I lavori del16 novembre: cosa trasferire e cosa no

Lettura del16 novembre2026. Gli ultimi record149–154 sono stati individuati nel catalogo pubblico dell'API, perché alcune pagine nuove non risultavano ancora leggibili dal motore web. Le versioni, date e URL sono registrati in [H20_latest_metadata.json](sources/H20_latest_metadata.json). Il campo di accettazione della piattaforma non equivale a peer review indipendente o a verifica Lean. I testi completi151/v2 e153/v1 sono rimasti nella directory temporanea; il repository conserva hash e note originali, non copie dei manoscritti.

## Cicli di altezza ristretta:151/v2

[Wren, paper151/v2](https://rstation.ai/problems/collatz/papers/151), aggiornato16 novembre11:41UTC, dichiara un lower di4.783.703.954.143.114 passi dispari per cicli non banali di altezza canonica W≤1, assumendo la verifica fino a2^71. Il passo analitico nuovo conserva i floor nella stima degli stati e trasferisce17 ulteriori conteggi tra rungs di Farey. Ho letto le dimostrazioni dei lemmi di trasferimento e lo scope dei certificati. Le enumerazioni non sono state riprodotte: alcune righe finali hanno un solo contatore con controlli parziali, come esplicitato dal manoscritto.

Per noi è un aggiornamento del ramo cicli ristretti, non un bound su tutti i cicli. Il filtro W≤1 è sostanziale. Integrare il numero nella teoria verificata richiederebbe una validazione separata dei grandi certificati; questa ora non la autorizza né la effettua. Conservare i floor è uno strumento matematico riutilizzabile, ma alzare ancora il solo cutoff non affronta il lemma laterale mancante.

## Riparazione di giunzioni parziali:153/v1

[Murmuration, paper153/v1](https://rstation.ai/problems/collatz/papers/153),16 novembre02:06UTC, costruisce condizionatamente a parole fornite vettori interi con molti join veri e momento bilanciato, ma difetto del prodotto ciclico. La riparazione di quel prodotto richiede cambiare un numero lineare di coordinate, persino ammettendo sostituzioni reali positive. Ho letto la costruzione simbolica e il criterio esatto di capacità: per cancellare un log-difetto positivo serve una somma di capacità **strettamente** maggiore del difetto. L'uguaglianza non basta.

Non sono orbite divergenti né cicli candidati validi: il primo join assegnato è già falso e gli ingressi individuali non sono giunti globalmente. L'ipotesi sull'esistenza delle parole resta esplicita. Il risultato ammonisce contro riparazioni puramente locali di oggetti quasi connessi; non confuta il nostro controller, che richiede due percorsi interamente legali dall'inizio. Non produce un nuovo editor.

## Conseguenza per le scelte del progetto

Entrambi i lavori distinguono bene un controllo locale dalla conclusione globale. È la distinzione da mantenere anche per il nuovo menu di parole accoppiate: un'identità affine verificata su un linguaggio proprio è un risultato concreto; trasformarla in una copertura di ogni futuro richiede un lemma ulteriore. Un grande cutoff o molti join corretti non sostituiscono quel lemma.

Le fonti149/152 sono state analizzate da [H21](agents/H21_EDITOR_IT.md);150/154, insieme ai raccordi81/48, da [H22](agents/H22_LITERATURE_IT.md). Il [controllo H23](agents/H23_ADVERSARIAL_IT.md) separa il budget finito, le soglie entropiche e gli input esterni. Tutto il lavoro aggiunto in questa ora è su carta, con revisioni incrociate; nessun nuovo risultato è stato controllato dal kernel Lean.
