# H03 — Due direzioni provate contro i loro primi ostacoli

16 novembre 2026. Ricerca concettuale: lettura di fonti primarie, argomenti su carta e confronto con H01, H02 e root. Nessun esperimento, conteggio eseguito, build, nuovo Lean, GPU o codice esterno. Le due direzioni sono un editor con clock variabile e un rinnovo relativo sulle fibre rare. Non è stata trovata una costruzione che escluda la divergenza.

## 1. La pista aritmetica: liberare il clock, conservare l'offset

Il costo corretto di una parola alternativa non è il numero dei suoi edit o la lunghezza della sua descrizione. Se la parola originale ha lunghezza k e totale A, e quella nuova lunghezza k+d e totale A+h, il rapporto dei gain è

`Γ=3^d 2^(−h)=2^(−E)`, `E=h−d log₂3`.

Il contratto generale ammette anche differenze di clock o totale negative, purché le parole finali abbiano lunghezze e lettere valide. Nel mini-lemma intero che segue si prendono d,h≥0; le altre differenze richiedono di trattare le potenze negative come razionali e di eliminare i denominatori prima della congruenza.

Nel telescopio armonico del [programma minimo](../ROOT_MINIMAL_PROGRAM_IT.md), un witness unità che entra da un genitore laterale costa esattamente Γ. Una famiglia con somma dei Γ divergente darebbe la contraddizione cercata. Il bridge è stato ricostruito indipendentemente: la differenza armonica al root domina il peso di ogni parola laterale; dopo divisione per il gain originale, si sommano incrementi di un potenziale limitato. Non occorrono in aggiunta densità naturale, Q, collisione, F o cap. L'esistenza dei witness rimane aperta.

La libertà di clock può evitare alcuni no-go a profilo identico. Non crea però da sola la divisibilità ternaria. Ecco un mini-lemma che conserva tutti gli offset. Scrivere le due parole come `pα:u→n` e `pβ:v→n`, con prefisso letteralmente comune p di lunghezza r e totale P. La prima coda ha lunghezza L e totale B; la seconda lunghezza L+d e totale B+h. Con la costante forward C si ottiene esattamente

`3^(r+L+d)(v−u)=2^P R`,

`R=2^B n(2^h−3^d)−C(β)+3^d C(α)`.

La prova è la sottrazione delle due identità affini delle code, seguita dall'identità del prefisso comune. L'esistenza di v intero, positivo e unità non è una conseguenza di questa formula: è una condizione da conservare. Anche il colore finale deve essere diverso. Quando d=h=0 si recupera il residuo dei precedenti no-go; quando d>0 appare un termine realmente nuovo dipendente da n.

Un'idea tentata è usare approssimazioni di log₂3 per rendere piccolo il debito h−d log₂3. Ma per d≥1 e h≥0 si ha SEMPRE

`ν₃(2^h−3^d)=0`.

Quindi una risonanza reale molto accurata non paga una sola cifra della congruenza mancante. Deve intervenire una cancellazione con il vero C(β). Analogamente, descrivere in binario l'esponente enorme di un lifting non ne riduce il costo fisico h. Questo elimina una scorciatoia, senza escludere correzioni distribuite e ammortizzate.

### Quale nuovo lemma avrebbe valore

Il bersaglio sensato è l'OVERLAP di due famiglie sparse di parole, con colori diversi, condizionato alla parola effettiva originale e con costo E controllato. Una copertura quasi uniforme di tutti i residui è troppo forte: H01 mostra in [Sparse support](H01_SPARSE_SUPPORT_IT.md) che le parole a basso debito di lunghezza fissata occupano una frazione esponenzialmente piccola delle classi modulo3^k. La variante a clock diverso resta aperta, con il nuovo modulo e il nuovo costo dichiarati.

Neppure la sola dimensione dei supporti basta. Due coset disgiunti di un ideale di Z/3^kZ possono entrambi avere cardinalità 3^(βk) con β>1/2. Servirebbe una proprietà di nonconcentrazione condizionata, non il principio falso «dimensione maggiore di un mezzo implica incontro». Il metodo sum-product può essere uno strumento solo dopo aver verificato proprio questa ipotesi sulle parole reali.

## 2. Un'analogia interessante che fallisce al primo test: alberi ramificati

Le decomposizioni spinali di [Lyons–Pemantle–Peres](https://arxiv.org/html/math/0404083v1), §2, e di [Aïdékon](https://arxiv.org/html/1101.1810v3), §2, suggeriscono di confrontare i migliori discendenti in rami diversi. I modelli ramificati per Collatz sono già classici: [Kontorovich–Lagarias](https://arxiv.org/html/0910.1944v1), §6.2, non sono una nuova idea del progetto. I teoremi probabilistici presuppongono strutture di indipendenza e una legge sull'albero che il grafo intero deterministico non possiede automaticamente.

Un controllo esatto boccia l'indipendenza ingenua. Condizionare un root ternario N alla validità di una parola di profondità k fissa N modulo3^k. Il suo primo genitore x=(2^eN−1)/3 è allora fissato modulo3^(k−1). Ogni sibling `x'=4^s x+(4^s−1)/3` resta fissato allo stesso modulo. I primi k−1 livelli di informazione del sibling non sono quindi nuove cifre Haar indipendenti. Una versione utile dovrebbe dimostrare un confronto condizionato sulle fibre aritmetiche selezionate dal seed piccolo; non basta assegnare ai fratelli alberi indipendenti.

La dimensione tipica della legge tilted nel paper9 non risolve questa guardia. Il cilindro di −1 che contiene la parola tutta-1 ha massa almeno (3/4)^k; la sua dimensione locale superiore è al più log₃(4/3), inferiore a1/2. Il punto −1 è NEGATIVO: l'esempio non confuta un'eventuale proprietà ristretta ai root positivi da seed fissati. Impedisce soltanto di importare un bound Frostman globale dal valore della dimensione quasi ovunque; la proprietà ristretta avrebbe bisogno di una nuova prova aritmetica. Tengo l'analogia come formato della domanda, non come via già praticabile.

## 3. La pista analitica: un corollario relativo del rinnovo di Goldie

La fonte primaria [paper9/v1](https://rstation.ai/problems/collatz/papers/9/v1), §3, verifica gli input classici di Goldie per il perpetuity reale R e scrive già sia la coda `F̄(t)=P(R>t)~C/t` sia la likelihood esatta del prefisso. Il tilt `P_*(e)=3/4^e`, il joint tail e la transizione gaussiana in variazione totale sono precedenti espliciti, non nuove scoperte. Il teorema originale è [Goldie1991](https://doi.org/10.1214/aoap/1177005985); il suo testo integrale non è stato ricertificato qui.

Un piccolo corollario utile al progetto rafforza il confronto in forma RELATIVA, anche per eventi prefix rarissimi. Per q lettere,

`R=β_q+A_qR'`, `A_q≤λ^q`, `0≤β_q≤λ^q−1`, `λ=3/2`,

con R' indipendente. Sia s(t)→∞ e q≤log_λt−s(t). Per ogni evento E determinato da quelle q lettere,

**`P(R>t,E)=(C/t)P_*(E)(1+o(1))`, uniformemente in E.**

Prova. Porre ε=λ^(−s(t)) e `η(x)=sup_(z≥x)|zF̄(z)/C−1|`. Si ha β_q/t≤ε e `(t−β_q)/A_q≥(1−ε)/ε`. Quindi, prefisso per prefisso,

`|tF̄((t−β_q)/A_q)/(CA_q)−1|≤[η((1−ε)/ε)+ε]/(1−ε)→0`.

Integrare sull'evento E e usare dP_*/dP=A_q. Se P_*(E)=0 entrambi i membri sono zero. La prova è una conseguenza della likelihood già presente nella fonte9, senza un nuovo teorema scalare di rinnovo.

Per il cilindro `E={Z≡n mod3^q}`, con n positivo DISPARI unità come nel dominio intero del progetto, il fattore tilted è esattamente

`P_*(E)=3^(−q)ρ*_q(n)`,

dove ρ*_q è la somma dei quadrati dei gain di TUTTI i prefissi ammissibili, senza imporre unità al terminale troncato. Si ottiene così un confronto relativo reale/ternario nella finestra subcritica. Non è un valore della traccia canonica g a un intero.

### Il remainder che manca, senza nasconderlo in «mixing»

Per qualsiasi q ed E, fissare ε∈(0,1), L>0 e il buon insieme `G={β_q≤εt,A_q≤t/L}`. La stessa prova dà l'errore relativo sul buon insieme al più

`δ=[η((1−ε)L)+ε]/(1−ε)`.

L'errore totale, dopo divisione per P_*(E)>0, è quindi al più

`δ + [P_*(E∩Gᶜ)+(t/C)P(R>t,E∩Gᶜ)]/P_*(E)`.

Questo isola una nuova possibile stima microscopica: controllare i prefissi cattivi RISPETTO alla massa del cilindro raro, con il primo colore conservato. Un bound in variazione totale non condizionato non paga quel denominatore. Alla finestra critica con errore additivo limitato, λ^q è dell'ordine di t e la semplice stima uniforme precedente si arresta.

Ci sono inoltre due guardie decisive. Primo, il tilt produce ρ*_q, non il terminale g² del vero kernel a due copie. Secondo, anche una buona likelihood finita non giustifica lo scambio fra il limite a root fissato che definisce g e una sequenza di root mobili. Il nuovo corollario calibra un operatore e un remainder; non dimostra il clock critico.

Un esempio rende concreto il secondo limite: ponendo t=n, la coda reale R>n è FUORI dal supporto della fibra canonica Q_n. Ogni prefisso compatibile con l'intero positivo n ha infatti β_q<n, e l'intero codice compatibile soddisfa R≤n, con il gap relativo noto ai root nonperiodici. Il confronto finito di Goldie può quindi descrivere massa ancora ammessa dalla prima congruenza, ma destinata a fallire una congruenza successiva. Non è una massa della fibra intera già costruita. H02 ha controllato questa guardia, la prova uniforme e il bound del remainder.

## 4. Una pista da scartare e un'integrazione positiva

Il candidato potenziale lineare `y g(y)` non può essere dichiarato puro. Per ogni prefisso inverso di un root nonperiodico n, il prodotto locale già verificato dà `Ω_mY_m≥n/P₀`. Quindi

`K₂^m(y g)(n)=g(n)E_Q[Ω_mY_m]≥n g(n)/P₀`.

Il resto resta positivo sul VERO grafo, non soltanto in un modello astratto. La lettura del [paper19/v2](https://rstation.ai/problems/collatz/papers/19), §9.2, conferma la distinzione: la fibra reale canonica non è un condizionamento R=n e conserva un gap relativo al root nonperiodico.

Al contrario, il resto con terminale g² si annulla puntualmente al root nonperiodico usando il decadimento sugli antenati già noto da Valbuena/fonte12. Al root periodico si separa l'uscita finita dal ciclo, mentre la probabilità di restarvi per r circuiti è un fattore β^r con β<1. Root, H01, H02 e H03 hanno ricostruito il passaggio. La nonatomia a root fissato va dunque tolta dai nuovi obblighi; manca il tempo uniforme. È un'integrazione utile della letteratura, non una nuova priorità.

## Decisione

Terrei una sola pista aritmetica: editor a clock variabile e costo effettivo, con un lemma sul vero carry e sul colore. Terrei il corollario di Goldie come strumento di normalizzazione e di diagnosi, finché non esiste la stima relativa del remainder e il ponte alla traccia intera. Scarterei indipendenza ramificata assunta, dimensioni usate come garanzia di incontro e annullamento del potenziale lineare. Il lavoro precedente è servito a riconoscere questi errori e a formulare un contratto più sobrio; non ha ancora prodotto l'editor richiesto o una nuova stima laterale.
