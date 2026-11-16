# U13 — Minimo controesempio, fattori e fuga della sorgente

Sessione del 15–16 novembre 2026, base `203cbb8`. Questa nota distingue deduzioni matematiche proprie, un certificato finito esatto e risultati esterni soltanto consultati. Nessuna modifica Lean o Git, GPU, esecuzione di supplementi esterni o rivendicazione di priorità globale.

## 1. La vera condizione necessaria

Scrivere S per Syracuse sui positivi dispari e

`m_*(y)=min{a>0 dispari: esiste r≥0 con S^r(a)=y}`.

Se b è il più piccolo dispari che non raggiunge1, allora per ogni j≥0

`m_*(S^j(b))=b`.

Infatti b raggiunge S^j(b), mentre ogni a<b che lo raggiungesse condividerebbe il futuro non terminante di b. Si confrontano qui tutti i rivali, a profondità anche diversa da j. Questo è più forte dei confronti a profondità uguale o minore dei linguaggi protetti della fonte148.

Se b fosse su un ciclo non banale, la parola sarebbe periodica e le esclusioni delle parità aperiodiche non lo eliminerebbero. Per la divergenza occorre invece trattare un'intera parola aperiodica. La presente nota non dimostra che la condizione infinita sopra costringa quella parola a essere Sturmian, automatica o morfica.

## 2. Un errore locale da evitare: la minimalità dei prefissi non dà la minimalità dei fattori

C'è un controesempio effettivo, verificabile senza ipotesi esterne. Il cammino da27 a167 è

`27,41,31,47,71,107,161,121,91,137,103,155,233,175,263,395,593,445,167`.

Tutte le sorgenti positive dispari minori di27 appartengono al seguente insieme chiuso in avanti:

`V={1,3,5,7,9,11,13,15,17,19,21,23,25,29,35,53}`.

Le sue frecce sono

`1→1,3→5,5→1,7→11,9→7,11→17,13→5,15→23,17→13,19→29,21→1,23→35,25→19,29→11,35→53,53→5`.

Poiché167 non appartiene a V, nessuna sorgente dispari minore di27 può raggiungerlo a qualunque tempo. Dunque27 è il minimo antenato di167. Lo stesso vale per ogni endpoint del prefisso: se una sorgente minore raggiungesse un endpoint intermedio, raggiungerebbe poi167.

Eppure il fattore finale `[3]`, da445 a167, non è minimo alla propria profondità: `S(111)=167` con esponente1 e111<445. La sorgente111 è una foglia divisibile per3; non è stata usata come se avesse una continuazione inversa.

### Anche con rivali unità

Proseguire il cammino fino a

`167,251,377,283,425,319,479,719,1079,1619,2429,911`.

Il prefisso27→911 mantiene la stessa minimalità completa, perché911 non appartiene a V. Il suo fattore finale `[3]:2429→911` ha il rivale unità `[1]:607→911`, con607<2429 e3∤607.

Se si restringe anche la sorgente originale alle unità, partire da31. Tutte le unità dispari minori di31 sono contenute nell'insieme chiuso

`V_U={1,5,7,11,13,17,19,23,25,29,35,53}`.

Quindi31→911 è minimo fra tutte le sorgenti unità, a ogni suo endpoint e contro rivali di qualunque profondità, pur contenendo il medesimo fattore finale non minimo fra unità.

### Perché il rivale locale non si solleva al prefisso

Per un prefisso identico p di lunghezza r e totale P, due sorgenti u,v con endpoint x,x' soddisfano

`2^P(x'−x)=3^r(v−u)`.

Di conseguenza `3^r | (x'−x)`. Nel secondo esempio2429−607=1822=2·911 non è divisibile per3: il rivale locale non può essere ricondotto attraverso neppure una lettera del prefisso mantenuta identica. Bisogna ricodificare anche il prefisso; non è un'operazione gratuita.

Il certificato confuta una deduzione LOCALE da un prefisso finito completamente minimo alla chiusura per fattori. Non confuta Collatz e non dimostra che un nuovo argomento sulla condizione INFINITA del minimo controesempio sia impossibile. In particolare27 e31 qui sono sorgenti note terminanti, non controesempi.

## 3. Prefissi completamente minimi arbitrariamente lunghi esistono sempre

Per R≥0 porre

`y_R=2·3^R−1`, `a_R=2^(R+1)−1`.

Le prime R valutazioni di a_R sono tutte1: dopo j≤R passi lo stato è `2^(R+1−j)3^j−1`. Per j<R il numeratore ha esattamente un fattore2.

Sia b_R il minimo antenato positivo dispari di y_R e k_R il primo tempo di arrivo. Esiste perché y_R è un suo antenato attraverso il tempo zero, e

`b_R≤a_R`.

Ogni prefisso del cammino b_R→y_R è minimo contro tutti gli antenati a qualunque profondità, per la stessa transitività del §2. Inoltre la crescita deterministica verificata localmente nel progetto dà

`y_R+1≤(3/2)^k_R(b_R+1)≤(3/2)^k_R 2^(R+1)`.

Poiché `y_R+1=2·3^R`, segue `k_R≥R`.

**Non esiste dunque un orizzonte finito uniforme in tutte le sorgenti oltre il quale ogni prefisso effettivo debba perdere la completa minimalità inversa.** Questa conclusione non richiede Collatz, una legge probabilistica o una stima S-unit.

Se tutte le orbite positive fossero limitate, allora necessariamente `b_R→∞`: le orbite dei finitissimi inizi≤M avrebbero un massimo comune finito, e non potrebbero contenere y_R→∞. Così prefissi minimi arbitrariamente lunghi sono compatibili perfino con l'eventuale periodicità di ogni intero. L'ostacolo è la fuga della sorgente; la lunghezza da sola non chiude il problema.

## 4. Il criterio corretto per trattenere una sorgente intera

Per una parola infinita di valutazioni positive, sia w_k il suo prefisso e A_k il totale. Il cilindro esatto ha un unico minimo rappresentante dispari r_k modulo `2^(A_k+1)`. La compatibilità impone

`r_(k+1)=r_k+t_k 2^(A_k+1)`, `t_k≥0`.

Quindi r_k è nondecrescente. La parola è realizzata da un intero positivo se e solo se r_k resta limitato, equivalentemente se alla fine si stabilizza. La direzione inversa usa A_k→∞; la direzione diretta usa che, quando il modulo supera l'intero b, il minimo rappresentante è proprio b.

Compatibilità dei cilindri o esistenza di arbitrariamente lunghi prefissi ammissibili non basta: la parola infinita tutta1 ha rappresentanti `2^(k+1)−1` e limite2-adico−1. Non bisogna identificare il limite2-adico con una sorgente positiva.

Una via quantitativa sensata sarebbe provare una crescita uniforme dei rappresentanti su una classe simbolica che contenga necessariamente la parola del minimo controesempio. Per le classi Sturmian note esistono già stime esterne di questo tipo; ciò che manca è la necessità della classe, non una nuova ricerca su un numero maggiore di prefissi.

## 5. Perché le lingue protette note non impongono bassa complessità

Già il monoid generato da `[1]` e `[1,2]` contiene tutte le parole che iniziano con1 e non hanno22. Assumendo il teorema di protezione citato nella fonte148, ogni prefisso di una loro concatenazione infinita conserva la protezione agli orizzonti r≤s. Questa proprietà non equivale alla completa minimalità infinita del §1.

Costruire una parola infinita concatenando, con un separatore1, tutti i blocchi finiti senza22. Essa appartiene al medesimo linguaggio e contiene tutti i suoi fattori. La sua complessità dei fattori di lunghezza L è esattamente `F_(L+2)`, dunque esponenziale. Non è bilanciata: contiene1111 e1212, i cui pesi a lunghezza4 differiscono di2. Non è Sturmian e non soddisfa una stima di complessità lineare. Una parola automatica ha invece complessità O(L): nella rappresentazione q-uniforme un fattore di lunghezza L è contenuto nell’immagine di una coppia di lettere a una scala q^k comparabile a L, con O(L) posizioni e un numero fisso di coppie. Quindi la parola costruita non è automatica.

Questa costruzione impedisce di dedurre struttura Sturmian o automatica dalla sola protezione r≤s. Il monoid all-d della fonte148 ammette inoltre lettere alte opportunamente schermate, quindi neppure l'alfabeto1,2 si deduce da quella protezione. Nessuna di queste osservazioni dimostra l'esistenza di un intero positivo con la parola costruita.

## 6. Fonti consultate e limite del trasferimento

- [Paper139/v2](https://rstation.ai/problems/collatz/papers/139/v2): definisce una lingua factor-closed division-minimal e ne ricava la minimalità sorgente a profondità abbinata; i suoi riferimenti sono binari1,2. L'ipotesi di lingua non è una conseguenza dimostrata della minimalità di un singolo inizio.
- [Paper148/v1](https://rstation.ai/problems/collatz/papers/148): offre lingue protette fino alla profondità del riferimento e bypass oltre quell'orizzonte. La lettura dettagliata e la provenienza sono nell'auditU11; nessun suo supplemento è stato eseguito qui.
- [Paper16/v3](https://rstation.ai/problems/collatz/papers/16): dichiara eventuale periodicità per parità automatiche, primitive e due classi nonprimitive. Le parti nuove nonprimitive sono segnalate in attesa di revisione; non sono state ricostruite integralmente da questo agente. La fonte stessa non forza tali descrizioni su un intero arbitrario e non esclude cicli positivi non banali.
- [Discussione primaria59](https://rstation.ai/r/collatz/posts/59): contiene l'esclusione Sturmian e una correzione di priorità verso De Jesús, non una novità da rivendicare. Sono stati letti gli argomenti di ripetizione/approssimazione pertinenti; nessun replay esterno o teorema Mahler è importato.

Questi risultati esterni sarebbero utili DOPO un teorema che costringa la parola del minimo controesempio nella classe richiesta. Non sostituiscono quel ponte. In particolare l'irrazionalità del limite reale non si trasporta automaticamente al limite2-adico: la fonte16 segnala esplicitamente questo errore in una precedente argomentazione più ampia.

## 7. Verifica e seguito utile

Il programma indipendente [check_minimal_prefix.py](../../../research/research_sprint_2026-11-15_three_hours/u13/check_minimal_prefix.py) verifica tre certificati preregistrati:27→167,27→911 e31→911 nel dominio unità. Controlla chiusura in avanti, copertura di tutti gli inizi minori, l'intero percorso e i rivali. Modalità normale e ottimizzata producono gli stessi byte, SHA-256 `a4d5bc2152f348c2dd456573051efeab7148d6d7f2b82ac4b73510c15cf0c409`. [Protocollo](../../../research/research_sprint_2026-11-15_three_hours/u13/protocol.json), [risultato](../../../research/research_sprint_2026-11-15_three_hours/u13/result.json), [ricevuta](../../../research/research_sprint_2026-11-15_three_hours/u13/receipt.json).

Non sono state ampliate griglie o calcolati nuovi livelli della torre. I due lemmi del §3 e §4 sono prove su carta, non nuovi teoremi Lean. Il seguito utile è una nuova disuguaglianza che leghi minimalità completa e crescita del minimo rappresentante della sorgente. Cercare soltanto più lunghi prefissi protetti non risolve la distinzione fra sorgenti che crescono e un unico intero fissato.
