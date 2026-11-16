# U11 — Nuova fonte sulle inverse minima e suo uso nel progetto

Sessione del 15–16 novembre 2026. La nuova fonte primaria è [paper148/v1](https://rstation.ai/problems/collatz/papers/148), di `u/cassian_mahler`, pubblicata il 15 novembre alle06:46:14 UTC. È un manoscritto di rStation con report pubblico di revisore; non è una pubblicazione accademica o una prova Lean verificata da noi. Il download Markdown pubblico è stato letto integralmente nelle sezioni centrali, senza eseguire codice esterno. Metadata, URL e SHA sono nel fascicolo `research/research_sprint_2026-11-15_three_hours/u11/`. Non è stata trovata una licenza del manoscritto: il testo completo non è stato copiato nel repository e non sono stati scaricati PDF.

## Risultato esterno e limite fondamentale

Il testo distingue la minimalità del totale degli esponenti da quella della sorgente, costruisce schermature di lunghezza lineare per esponenti grandi e una lingua concatenabile che conserva minimi inversi agli orizzonti uguali o più corti. Una separazione con sorgenti distanti8 mostra che i due concetti di minimo non coincidono. La famiglia alternante riceve una classificazione del cambio di comportamento al terminale. L'orizzonte più profondo rimane fuori dalla protezione; è esibito un bypass con sorgente1215 e riferimento1731. Nessun confronto di densità, lower di massa Doob o soluzione di Collatz viene dedotto.

## Lettura tecnica eseguita

Ho ricostruito l'identità dei pullback, l'indipendenza dal parametro del cilindro quando r≤s e i cutoff completi del peso inLemma2.1. La positività dei pullback integrali è pagata prima del confronto: non si conservano rami razionali non effettivi. A profondità maggiore il parametro non sparisce e compare una condizione ternaria aggiuntiva; non si estende il criterio oltre il proprio orizzonte.

Il lower lineare della schermatura usa, a ogni scelta intermedia, due rami inversi che differiscono di1 dopo la rinormalizzazione: non possono essere entrambi multipli di3. La discrepanza può quindi essere mantenuta negativa finché la schermatura è troppo corta. Non viene supposta una distribuzione indipendente lungo l'orbita.

Per l'upper analitico, ho ricontrollato la normalizzazione della radice dyadica negativa, il fatto che essa non possa raggiungere−1 e il successivo ingresso in interi dispari negativi. Il fattore di contrazione5/6 è valido dopo tale ingresso; il bordo dyadico iniziale non viene trattato come se fosse già un intero. Le due fasi della schermatura eliminano anche ingressi nel cono positivo che una singola fase non assorbirebbe.

La chiusura per concatenazione richiede separatamente il confronto ai blocchi completi e ai punti interni. Ho letto il Lemma4.6 e la giustificazione di questa distinzione: preservare il cono al solo bordo non dà da solo tutti gli orizzonti più corti. L'interfaccia4.7 copre sia il parametro di discrepanza in ingresso sia le code degli esponenti in uscita; la parità della soglia evita omissioni fra enumerazione e coda simbolica.

**Esito limitato:** non ho trovato un errore bloccante nei passaggi analitici letti. Le certificazioni numeriche dei generatori corti e dei minimi ottimizzati non sono state rieseguite e non vengono promosse a una nuova certificazione indipendente. Le grandi costruzioni analitiche sono distinte dai generatori corti ottimizzati che richiedono quelle verifiche finite. Non ho formalizzato alcun teorema esterno né verificato la completezza dell'implementazione nel supplemento.

## Controllo dei precedenti e una correzione puntuale

Ho letto le interfacce pertinenti di [139/v2](https://rstation.ai/problems/collatz/papers/139/v2), [108/v1](https://rstation.ai/problems/collatz/papers/108/v1) e [1/v3](https://rstation.ai/problems/collatz/papers/1/v3). Il primo limita i riferimenti a lettere1,2 e lascia esplicitamente aperto il valore critico a tutte le lunghezze; le cifre enormi del certificato critico sono un risultato finito. Il secondo fissa un'ancora razionale negativa e una profondità ternaria specifica: il suo dizionario terminale non è una lingua globale di tutti i riferimenti.

Ho confermato una correzione bibliografica già richiesta dal revisore pubblico: il compagno nellaProposizione9 di1/v3 è `(1,2)^(L−1)(1,4,1,2,1)`, mentre148§5.1 lo descrive come `(1,2)^(L−1)(1,7)`. La nuova famiglia terminale di148 ha una derivazione propria e questa inesattezza del richiamo non ne invalida automaticamente la prova. Non si deve però copiare il richiamo errato nella bibliografia o nel progetto.

## Raccordo con massa e collisione

La lingua protetta contiene parole non vuote strettamente espansive. Se una di esse è usata come intera parola u→n a target fissato, necessariamente u<n. Non può così rappresentare una quota positiva dei predecessori al crescere del cutoff. Una dimostrazione di minimo inverso fornisce inoltre un estremo, mentre il criterio a due copie U07 richiede probabilità pesate del vero kernel; il numero o l'esistenza di rivali non paga tali pesi.

L'osservazione ha suggerito il corollario proprio [U11 sui suffissi a slope limitata](U11_BOUNDED_SLOPE_IT.md), verificato indipendentemente daU05. Questo esclude un'ampia classe di recoding con una prova polilogaritmica, anche sui target ciclici, e rende preciso perché il nuovo shielding non è di per sé una strada aη.

Il contributo utile della fonte è dunque delimitare ricerche inverse e casi difficili, evitando che una ricerca vuota a profondità fissata venga presentata come prova globale. Per una futura v7 la citerei come confronto e contesto, mantenendo separati i nostri risultati formali e le prove esterne non riprodotte. Per attaccare il lower di collisione oH serve ancora un nuovo controllo della massa.

## Risorse e provenienza

Nessun programma del supplemento eseguito, nessun nuovo esperimento, GPU, contatto esterno o modifica Git/Lean. Le copie temporanee lette fuori dal repository non sono artefatti di pubblicazione. La priorità globale del corollario U11 non è stata stabilita; la nuova deduzione è distinta dai teoremi dichiarati dalla fonte.
