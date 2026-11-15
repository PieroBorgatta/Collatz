# T08 Fasce critiche, mixing congiunto e un limite necessario sui cap

15 novembre 2026. Ricerca iniziata alle20:24 UTC. **Stato:** prove matematiche su carta, controlli finiti completati e revisione indipendente T09 superata per i bound dei cap e il criterio cumulativo. Nessun nuovo risultato asintotico è dichiarato in Lean da questo agente. Non è stata costruita la quota relativa η.

## 1 Un risultato dinamico che non usa mixing

Per un target positivo dispari n e un intero M≥1, indichiamo con A_M(n) i predecessori dispari u il cui cammino di primo arrivo accelerato a n usa soltanto esponenti fra1 e M. Si ammette la parola vuota u=n. Per sorgenti ordinarie si rimuove prima la potenza di due: il cap riguarda gli esponenti Syracuse, non questo fattore iniziale. Non occorre che n sia senza ritorni: il primo arrivo è sempre ben definito per una sorgente che lo raggiunge. Se esiste un cammino con cap, il suo prefisso di primo arrivo ha lo stesso cap.

Poniamo θ_M=1−2^(−M). Per ogni r≥0 e ogni cutoff reale X≥1 vale la disuguaglianza finita

`#(A_M(n)∩[1,X]) ≤ Σ_(0≤k<r) M^k + (X/2) θ_M^r + M^r`.       (1)

La prova separa gli arrivi in meno di r passi dagli altri. Per ogni lunghezza k<r ci sono M^k parole, e una parola e il target determinano al più una sorgente: il primo termine è quindi un upper bound, anche se parole diverse producono lo stesso intero.

Ogni sorgente con almeno r passi appartiene a un cilindro dyadico dei primi r esponenti. Per una parola w positiva di totale A, quel cilindro fra gli input dispari è una sola classe modulo2^(A+1), dunque contiene al più X/2^(A+1)+1 inizi fino a X. I cilindri di parole diverse sono disgiunti. Sommando sulle M^r parole si ottiene

`Σ_w 2^(−A−1) = (1/2)(Σ_(a=1)^M 2^(−a))^r = θ_M^r/2`.

La somma degli errori di arrotondamento è al più M^r. Per r=0 il cilindro è semplicemente l'insieme degli input dispari, con count≤X/2+1: non si usa la parola vuota, che da sola non impone parità.

Questo è un impiego diretto della legge esatta dei cilindri, già formalizzata nel progetto. Non richiede indipendenza ipotizzata lungo una singola orbita, né un risultato di terminazione.

### Upper bound uniforme e cap crescente

Per M≥2 definiamo

`α_M = log M / log(M/θ_M) < 1`.

Scegliendo r=floor(log X/log(M/θ_M)) in(1), e usando la somma geometrica degli arrivi brevi, segue

`#(A_M(n)∩[1,X]) ≤ 3 X^(α_M)`.                              (2)

Infatti M^r≤X^α, X θ_M^r≤θ_M^(−1)X^α e

`Σ_(k<r)M^k + M^r ≤ [M/(M−1)]M^r`.

Il coefficiente è al più1/(2θ_M)+M/(M−1)≤2/3+2<3. Il bound è uniforme nel target e nel cap M≥2, inclusi target periodici e cutoff piccoli.

Il passaggio alle sorgenti ordinarie somma sui fattori di due:

`#(A_M^ord(n)∩[1,X]) ≤ 3 X^α Σ_(e≥0)2^(−eα) ≤ 9 X^α`.       (3)

Per l'ultima costante osserviamo M θ_M²≥2(3/4)²>1, quindi α_M≥2/3, e2^(−2/3)<2/3 (il cubo riduce a27<32). La geometrica è dunque al più3. Il medesimo M resta fissato anche nei cutoff X/2^e: non si sostituisce con M(X/2^e).

Per M=1, la versione(1) con r=ceil(log₂X) dà O(log X) sorgenti dispari e O((log X)²) lift ordinari. In particolare ogni cap fisso produce densità naturale zero.

La perdita quantitativa soddisfa

`1−α_M = [−log θ_M]/[log M−log θ_M] ≥ 2^(−M)/(2 log M)`,     (4)

perché 2^(−M)≤1/4, −log(1−t)≥t e −log(1−t)≤t/(1−t)≤1/3≤log M.

Ne segue una forma più utile per la progettazione di trasporti. Se0<ε<1 e il cap intero dipendente dal cutoff soddisfa, per tutti gli X abbastanza grandi,

`M(X) ≤ (1−ε) log₂ log X`,

allora anche il numero di predecessori ordinari con quel cap è o(X). Si può sostituire M con max(2,M). Per M≥2, da(4)

`(1−α_M)log X ≥ (log X)^ε/(2 log log X) →∞`,

usando il denominatore più largo log log X per rendere il limite immediato. Il bound(3), uniforme in M, chiude la prova.

### Rafforzamento: il cap deve raggiungere log₂log X meno una costante

Un secondo argomento usa il budget elementare di T02 e il momento di parità esatto di T01. È più forte per i cap crescenti. Poniamo L=floor(log₂X), r=floor(L/8), X≥1, e θ=1−2^(−M), con M≥1. Si ottiene il bound finito

`N_M^odd(X;n) ≤ X θ^r +3 X^(3/4)`,
`N_M^ord(X;n) ≤6 X θ^r +8 X^(3/4)`.                         (5)

**Arrivi brevi.** Se il primo arrivo ha k<r, il budget `2^A n≤4^k u≤4^k X` e l'integrità di A danno A≤L+2k≤L+2r. Questo non richiede il cap. Il numero di parole positive di lunghezza k e totale≤B è binom(B,k), inclusa la parola vuota per k=0. Per q=1/4,

`Σ_(k≤r)binom(L+2r,k) ≤4^r(5/4)^(L+2r) ≤2^(3L/4)≤X^(3/4)`.

L'ultima disuguaglianza segue da r≤L/8 e dal certificato intero `5^10<2^24`.

**Prefissi completati.** Per un input con almeno r passi prima del target, sia A_r la somma dei primi r esponenti effettivi. Se A_r≤L e sono tutti≤M, il suo cilindro ha modulo q=2^(A_r+1)≤2X. Una singola classe positiva contiene al più ceil(X/q)≤2X/q punti, poiché X/q≥1/2. Sommando i cilindri si ottiene al più Xθ^r. Il caso r=0 usa il dominio dispari, con modulo2; X≥1 assicura ancora q≤2X.

**Overflow di precisione.** Se A_r>L, i primi L stati shortcut contengono al più r stati dispari: ogni stato dispari è un punto del clock accelerato, e il r-esimo punto successivo all'iniziale non è ancora stato raggiunto. Quindi J(u,L)≤r. Il momento esatto

`Σ_(s<2^L)(1/4)^J(s,L)=(5/4)^L`

fornisce al più `4^r(5/4)^L≤2^(3L/4)` residui. Per ogni residuo ci sono al più due input fino a X, perché2^L≤X<2^(L+1). Il certificato per la potenza è `5^8<2^20`. L'overflow costa quindi al più2X^(3/4). Per r=0 l'evento A_0>L è vuoto. Sommando i tre contributi si ottiene la prima riga di(5).

**Lift ordinari.** M resta lo stesso a tutti i cutoff X/2^e. Per e≤L, il nuovo parametro è r_e=floor((L−e)/8), e r−r_e≤ceil(e/8). Siccome θ≥1/2,

`θ^(r_e) ≤2·2^(e/8) θ^r`.

La parte principale si somma con `Σ2^(−7e/8)≤3`, perché2^(−7/8)≤2/3. Il resto si somma con `Σ2^(−3e/4)≤8/3`, perché2^(−3/4)≤5/8. Sono disuguaglianze verificabili elevando alla potenza8 e4; il lift dà la seconda riga di(5).

Da(5), usando θ^r≤exp(−r2^(−M)), segue la densità zero per ogni cap M=M(X) con

`2^M=o(log X)`.

In particolare basta `M(X)≤log₂log X−g(X)` per qualunque g(X)→∞, anche lentissimo. Per un cap la cui famiglia di predecessori ordinari abbia invece almeno δX elementi lungo una successione di cutoff, δ>0, la stessa formula impone

`2^M ≥r/log(12/δ)`

per cutoff sufficientemente grandi: il termine8X^(3/4) è allora≤δX/2. Quindi **una quota positiva obbliga M≥log₂log X−O_δ(1)** lungo quella successione. È una condizione necessaria, non una costruzione di una quota. I bound(2)–(4) rimangono utili per M fissato, ma non sono la soglia crescente più forte ottenuta qui.

### Conseguenza per η

Un trasporto entro altezza D X, con D fissato, che usi soltanto immagini i cui cammini verso il target superiore hanno un cap M(X) come sopra, dispone di o(X) immagini fisiche, anche nel regime più forte `2^M=o(log X)` di(5). Se il carico incoming per immagine è limitato da K, il flusso totale è al più K·o(X)=o(X). Lo stesso ostacolo vale se si limita con quel cap la parola delle sorgenti selezionate.

Quindi questi meccanismi non possono trasferire una quota η>0 di un bacino di densità inferiore positiva. L'obbligo costruttivo è concreto: servono massimi esponenti almeno alla scala log₂log X, a meno di rinunciare al controllo di altezza/carico o di trovare un'altra relazione. Superare questa soglia non garantisce η.

Per un pool di J(X) target occorre addebitare il numero dei target: il bound forte si somma a J(X)[6Xθ^r+8X^(3/4)]. Non si deduce un no-go per un pool infinito senza controllo di J; per esempio le parole vuote su tutti i target coprirebbero ogni input. Per un singolo target, anche dipendente da X, i bound sono uniformi.

Il sottoalbero binario dei primi due figli interni, usato nello stress-test T06, ha cap≤6 e ricade nel caso fisso. Una percentuale positiva dei suoi codici non può perciò essere trasformata in una percentuale positiva del bacino mediante il solo limite di profondità.

Non si rivendica priorità bibliografica di questa conseguenza elementare della legge dei cilindri. Il nuovo uso qui è come criterio esplicito di arresto per i trasporti di massa e come vincolo sulla crescita del cap nelle costruzioni successive.

## 2 Cosa conta una fascia del coefficiente omogeneo

Per una parola effettiva w:u→n, siano k la lunghezza, A il totale e ρ=2^A/3^k. Il nuovo budget del coordinatore dà

`1≤P(u→n)≤P₀=exp27`, `u=ρ n/P`.

Una fascia R≤ρ≤CR contiene quindi soltanto sorgenti in[Rn/P₀,CRn]. Viceversa una sorgente in[Rn,CRn/P₀] appartiene alla fascia, quando l'intervallo non è vuoto.

Nel dominio senza ritorni le parole effettive verso n sono fisicamente uniche anche fra lunghezze diverse. Il catalogo cumulativo

`L_n(R)=#{w effettiva verso n: 2^A/3^k≤R}`

è finito e soddisfa

`#B_n^odd(Rn/P₀) ≤ L_n(R) ≤ #B_n^odd(Rn)`.

È quindi un modo esatto di esprimere capacità fisiche a cutoff confrontabili, non una nuova minorazione della loro massa.

Per k≥1,A≥k, il dizionario esatto su target dispari dà

`N_n(k,A)=2^A P(X_k=n mod3^k, S_k=A)`,

dove X_k è l'offset di Syracuse nell'orientamento inverso rispetto alla parola forward locale. La reversal della lista conserva la legge e il totale. L'identità usa gli stessi atomi congiunti e le sorgenti intere: non si ricava da due marginali.

Sul bordo critico log₂ρ=A−k log₂3≈log₂R, un A è vicino al centro2k quando k≈log R/log(4/3). Una finestra centrale contiene O(√k) profili a profondità vicine, ma ogni conteggio moltiplica la probabilità atomica per2^A≈R3^k. Perciò un errore assoluto ε_(k,A) nell'atomo produce un errore di conteggio2^A ε_(k,A), e un confronto aggregato richiede il controllo di

`Σ_(k,A nella fascia) 2^A ε_(k,A)`,

in scala o(R), o rispetto alla massa effettiva del catalogo di base. Un errore globale di mixing più piccolo di ogni potenza di k non paga da solo il fattore3^k. Sommare una finestra di O(√k) termini non cambia questa difficoltà. Non si assume una cancellazione di errori con segno non controllato in una minorazione di conteggi positivi.

Questo identifica il prossimo input specifico: un confronto relativo di un potenziale di rinnovo congiunto, pesato con2^A sulla fascia, oppure un trasporto effettivo che controlli contemporaneamente massimi esponenti crescenti, collisioni e altezza. Non basta allargare il matching finito a tutte le coppie di altezza ammissibile.

### Un criterio finito esatto per il trasporto globale

Questo catalogo consente una costruzione che evita di progettare a mano un trasduttore locale. Siano U,V insiemi finiti di sorgenti fisiche, con chiavi positive ρ, C>0 e m≥1 intero. Esiste una mappa f:U→V con

`ρ(f(u))≤Cρ(u)`, `#f⁻¹(v)≤m`,

se e soltanto se per ogni soglia t

`m·#{v∈V:ρ(v)≤Ct} ≥ #{u∈U:ρ(u)≤t}`.

La necessità conta le sorgenti sotto la soglia e le loro immagini ammissibili. Per la sufficienza si ordinano U e V per chiave, con indici da1. L'i-esima sorgente viene mandata all'immagine di rango ceil(i/m). Il confronto cumulativo alla chiave della sorgente assicura che quel rango esista entro Cρ(u_i); ogni rango è usato al più m volte. Le parità di chiavi si risolvono con un ordine fisico secondario e non creano copie di uno stesso intero. È una caratterizzazione finita, non un'ipotesi probabilistica.

Applicata ai cataloghi di primo arrivo, una disuguaglianza

`m_n L_y(Ct) ≥ L_n(t)−K_n`

per ogni t sufficientemente grande permette di scartare soltanto finitissime sorgenti e poi usare il trasporto di rango. Qui K_n può dipendere dal target ma non da t. Se il difetto è scritto proprio in questa forma, scartare ceil(K_n) sorgenti iniziali, oltre a quelle sotto la soglia iniziale, è sufficiente. Al cutoff X, i loro lift ordinari sono O_n(log X).

Il lemma d'altezza del coordinatore dà allora `v≤21C exp27·u`, il carico è m_n e la massa uscente di ogni sorgente conservata è1. Per H basterebbero C universale e `m_n≤K(1+log n)`, con K universale. Non serve imporre a priori la stessa profondità o lo stesso totale. La riscrittura è globale e perciò non ricade nell'ostruzione dei blocchi terminali fissi.

**Il confronto cumulativo non è dimostrato.** Questa formulazione colloca precisamente il lavoro analitico: una comparazione dei potenziali di rinnovo congiunti sul bordo critico. Non si sta deducendo quel confronto dalla sola esistenza di densità, né dalle norme globali di mixing. L'enumerazione globale può essere non effettiva se non si dispone di un criterio per escludere parole di arrivo ancora più profonde: qui si prova l'esistenza del trasporto date le capacità, non un algoritmo terminante per calcolarle tutte.

## 3 Contro-modello delle sole norme di mixing

T07 ha costruito la densità astratta

`F=(3/4)1_(Z₃×)+Σ_(j≥1)3^j 1_(n_j+3^(2j)Z₃)`, `n_j=2·3^j−1`.

I cilindri degli spike sono disgiunti, F ha integrale1, floor3/4 sulle unità, appartiene a L^p per1≤p<2 ma non a L² ed è il massimo rappresentante semicontinuo inferiore della propria misura. La traccia a ogni intero positivo è finita e le medie di cilindro vi convergono ordinariamente. Questa è una costruzione astratta, non una legge stazionaria Syracuse.

Il sibling canonico y_j=16n_j+5 soddisfa y_j+1=32·3^j−10, di valutazione ternaria0. Nessuno y_j appartiene a uno spike, mentre n_j sì. Quindi

`F(y_j)=3/4`, `F(n_j)=3/4+3^j`.

Un Harnack logaritmico fra questi valori fallisce. Non è un controesempio alla H dei bacini: F non è la traccia dinamica effettiva e non è stata stabilita la nonperiodicità della famiglia n_j per Collatz.

Siano μ_m le leggi dei cilindri ottenute integrando F, eρ_m le relative densità. Troncando gli spike a j≤floor(m/2), la parte troncata è misurabile alla profondità m, e la massa della coda è(1/2)3^(−floor(m/2)). Contrattività delle aspettative condizionate dà, per n≥m,

`||ρ_n−ρ_m||₁ ≤3^(−floor(m/2))`.

Anche le frequenze primitive hanno un bound esponenziale: per profondità n≥2 possono contribuire soltanto spike con2j≥n, dunque

`|μ̂_n(ξ)| ≤(3/2)3^(−ceil(n/2))`, per3∤ξ.

Questo è più piccolo di ogni potenza negativa della profondità. Il rate è alla soglia critica1/√3, coerente con il mancato L² osservato da T07.

Si possono ora definire leggi congiunte artificiali

`Q_k(r,s)=μ_k(r) π_k(s)`, `π_k(s)=binom(s−1,k−1)2^(−s)`.

Hanno la corretta marginale del totale geometrico e ogni slice condizionata è μ_k. La somma in s delle oscillazioni congiunte è esattamente l'oscillazione di μ_k, quindi soddisfa un analogo dell'input averaged(J), addirittura esponenziale. Ciononostante non fornisce il confronto trasverso della traccia.

Il confine è verificabile, non solo nominale. Questa famiglia NON rispetta la generazione affine effettiva. Già k=1,s=1 ha Q_1(1,1)=1/8, mentre l'unica parola di totale1 ha X_1=2 mod3, quindi quell'atomo effettivo deve essere zero. Inoltre2^sQ_1(1,1)=1/4 non è nemmeno un conteggio intero di parole. La F viola anche l'equazione stazionaria binaria: F(2)=3/4, mentre(1/2)F(4)+(3/2)F(1)=3/2.

Il contro-modello esclude soltanto l'inferenza da norme globali, marginali e regolarità alla Harnack. Un uso della vera legge deve sfruttare in modo essenziale le identità affini, i conteggi interi e la stazionarietà, che qui falliscono.

## 4 Fonti primarie e loro perimetro

- Valbuena, *Fourier decay for truncated Syracuse affine laws*, 7 ottobre2026: sorgente già fissato e acquisito da T03. Il decadimento primitivo resta valido dopo conditioning su totali di massa almeno polinomiale, ma non è un confronto relativo di atomi a scala3^k.
- [rStation10 v3](https://rstation.ai/problems/collatz/papers/10), 22 ottobre2026: il floor congiunto e il bound cX/n dipendono dall'input esterno averaged(J) di altri preprint. Il dizionario esatto è valido sui target dispari; il bound assoluto non confronta due bacini effettivi.
- [Tao, esposizione primaria del2019](https://terrytao.wordpress.com/2019/09/10/almost-all-collatz-orbits-attain-almost-bounded-values/): la stabilizzazione è una norma di variazione totale delle leggi finite; il passaggio a un singolo atomo non è una conseguenza automatica.
- [rStation37 v2](https://rstation.ai/problems/collatz/papers/37/v2), 25 ottobre2026: l'accessibilità di classi ternarie migliora il budget totale a scala sublineare del modulo e il conteggio con cap fisso resta di esponente strettamente minore di1. Dipendenze analitiche sono dichiarate, nessun progetto formale esterno è stato verificato localmente. La routing termina in una classe, non crea una quota di immagini a dilatazione costante.
- [rStation18](https://rstation.ai/problems/collatz/papers/18), 22 ottobre2026: il count-law transfer prende prima il limite di densità alla scala di banda fissata; momenti interi senza cap e l'upper mean restano obblighi aperti. Non è stato usato come nuovo teorema del progetto.

Il PDF SSRN Luo/Kolpakov/al-Jammas indicato dal coordinatore ha restituito403; non ne è stata dedotta un'ipotesi utilizzabile dalla sola descrizione. Nessun sorgente scaricato è stato eseguito.

## 5 Verifiche e decisione

Il protocollo è stato congelato alle20:38 UTC in `research/research_sprint_2026-11-15/t08/protocol.json`. Due programmi indipendenti dalle implementazioni T01–T07 hanno superato l'esecuzione normale e quella con Python -O, con output identici:

- `check_capped_prefixes.py`:3.822 replay esatti di cilindri,241.627 coppie controllate disgiunte,4.096 sorgenti dispari,5.292 disuguaglianze finite con Fraction. Le490 verifiche numeriche dei power bounds e dei lift sono diagnostiche floating, non certificati della potenza irrazionale. SHA dei dati `9f063fc17baabffd9c99edbe0242296f079ac51bb5edfdb7b6587248adf720cd`.
- `check_abstract_joint.py`:9.840 residui di compatibilità proiettiva e45 coppie di profondità con errori L1 controllati in Fraction, oltre ai valori degli spike e ai due fallimenti dinamici espliciti. SHA `10a50cd93dc0c35ce6ee5e6b4bd35d10010df8ad6fbf7d557cf5835bca3f99a0`.

- `check_overflow_bound.py`, con addendum congelato prima dell'esecuzione:1.026 controlli binomiali,67.080 guardie del lift,67.584 controlli di clock (15 casi di overflow effettivo), quattro certificati interi. Normale e -O identici; SHA `3f760ccd478a63f8df0f81a8cca3268c6b9371d960f05dcb49fa9f787bbfb0cb`.

La ricevuta `research/research_sprint_2026-11-15/t08/receipt.json` fissa ambito, hash dei dati e dei programmi, protocolli e confini della revisione. I controlli finiti verificano cilindri e formule; non sostituiscono le prove dei limiti. Nessun sorgente esterno è stato eseguito e nessun nuovo modulo Lean è stato aggiunto da T08. T09 ha ricostruito indipendentemente i bound(2)–(5), il limite per cap crescente e il trasporto cumulativo con ties, confermando i caveat riportati. La sua verifica fisica indipendente è registrata dal revisore e dal coordinatore, separatamente da questi programmi.

La prosecuzione sensata richiede un meccanismo che ammetta grandi esponenti alla scala necessaria e che preservi una quota fisica. Per l'analisi, il bersaglio è un confronto locale o di rinnovo della vera legge congiunta, con errore relativo dopo il peso2^A. Il solo mixing globale, anche molto rapido, non elimina quel passaggio.
