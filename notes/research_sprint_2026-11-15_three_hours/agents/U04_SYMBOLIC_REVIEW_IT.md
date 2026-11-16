# U04 — Audit dei prefissi minimi e calibrati di U13

Revisione indipendente su carta di `U13_INFINITE_MINIMAL_IT.md` e `U13_CALIBRATED_COUNTEREXAMPLE_IT.md`, senza modificare i testi o rieseguire i programmi. **PASS entro i domini dichiarati.** Le conclusioni esterne sulle classi automatiche, morfiche o Sturmian non sono state ricostruite integralmente e non entrano nei certificati propri.

## 1. Minimalità completa, dominio delle unità e fattori

Il minimo controesempio dispari b, se esistesse, sarebbe il minimo antenato di ogni punto della sua orbita: un antenato più piccolo condividerebbe il futuro non terminante e contraddirebbe la scelta di b. Questa condizione riguarda tutti i tempi e non soltanto profondità confrontabili. Non forza da sola una lingua chiusa per fattori.

Ho controllato algebricamente le frecce dei due insiemi finiti V e V_U: sono effettivamente chiusi per Syracuse, contengono rispettivamente tutti i dispari<27 e tutte le unità dispari<31, ed escludono167 e911. La transitività esclude antenati minori anche per ogni endpoint intermedio dei cammini esibiti.

Nel primo controesempio,111 è un rivale dispari di445 verso167 ma è multiplo di3; U13 non gli attribuisce una continuazione inversa. Nel controesempio unità,607 e2429 sono entrambi unità e raggiungono911 con esponenti rispettivamente1 e3. La differenza1822 non è divisibile per3, dunque il rivale non si solleva mantenendo neppure una lettera di prefisso identica. Non si conclude che ogni ricodifica del prefisso sia impossibile.

Sono controesempi a una deduzione locale da prefissi finiti;27 e31 sono sorgenti terminanti, non minimi controesempi infiniti.

## 2. Calibrazione globale di tutti i prefissi31→911

Il cammino contiene27 passi e totale38; Ω_end=3²⁷/2³⁸. La quantità n_i/Ω_i cresce esattamente di1/(3Ω_i) per passo. Il valore finale911/Ω_end è strettamente inferiore a35, con il margine razionale positivo registrato.

Tutti i seed unità>31 sono almeno35:32 e34 sono pari,33 è divisibile per3. Per ogni tale seed e ogni parola effettiva verso n_i, il potenziale universale dà `Ω≤n_i/u≤n_i/35<Ω_i`. I seed unità<31 sono esclusi dal set chiuso V_U. La traiettoria completa risolta di31 non ripete nessuno degli endpoint>1, dunque31 dà un unico cammino a ogni n_i. Questo prova esattamente F(n_i)=Ω_i per tutti i prefissi, incluso F(31)=1; non è un'estrapolazione da un cutoff finito.

Il fattore finale ha gain3/8, inferiore al gain3/2 del rivale607. Ma nessun seed unità≤31 raggiunge607, e il potenziale dà `F(607)≤607/35`. Il suo ramo pesato è quindi al più1821/70, strettamente inferiore a F(911). La ricorrenza max-plus pesata rimane valida. È soltanto la chiusura grezza per fattori a fallire.

## 3. Orizzonti lunghi e sorgente che fugge

La famiglia `a_R=2^(R+1)−1`, `y_R=2·3^R−1` realizza R esponenti uno. Il minimo antenato b_R di y_R è al più a_R; la crescita shifted dà `y_R+1≤(3/2)^k_R(b_R+1)` e quindi k_R≥R. Ogni suo prefisso è completamente minimo per transitività. Non esiste perciò un orizzonte uniforme per tutte le sorgenti che elimini ogni prefisso minimo.

Se tutte le orbite fossero limitate, b_R dovrebbe comunque tendere a infinito, perché l'unione delle orbite di finitissimi piccoli inizi sarebbe finita. È corretto distinguere prefissi arbitrariamente lunghi con sorgenti variabili da una sola parola infinita realizzata da un intero fissato.

I minimi rappresentanti dei cilindri esatti soddisfano `r_(k+1)=r_k+t_k2^(A_k+1)`, t_k≥0. Essi rappresentano un intero positivo se e solo se sono limitati, equivalentemente se si stabilizzano. A_k→∞ rende corretta anche la direzione inversa. La parola tutta uno ha invece rappresentanti2^(k+1)−1 e limite2-adico−1; non definisce una sorgente positiva.

## 4. Protezione sintattica non è bassa complessità

La costruzione di una parola universale senza22, concatenando tutti i blocchi legali con separatori1, conserva il vincolo e realizza ogni fattore legale. La sua complessità è Fibonacci, dunque esponenziale;1111 e1212 ne mostrano anche la mancata bilanciatezza. Una parola automatica ha complessità O(L), attraverso la rappresentazione uniforme a blocchi, quindi quella costruzione non è automatica.

Il trasferimento della protezione alla parola universale resta condizionato al teorema esterno citato da U13. Anche assumendolo, la protezione fino a una profondità non impone la completa minimalità infinita del minimo controesempio. Le note non forniscono un ponte che costringa una reale orbita eccezionale nelle classi simboliche escluse.

## Ambito della verifica

I certificati finiti si combinano con disuguaglianze universali per escludere tutti i rivali; non sono una scansione di grandi orbite. Ho verificato il loro significato matematico e i casi limite, senza rieseguire il codice. Nessuna conclusione su Collatz o H, nessuna importazione di teoremi esterni in Lean e nessuna priorità globale accertata.
