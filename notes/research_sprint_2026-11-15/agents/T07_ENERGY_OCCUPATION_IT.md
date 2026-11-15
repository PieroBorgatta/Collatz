# T07 — Stabilizzazione locale della traccia, energia e clock inverso

15 novembre 2026. **Stato: deduzioni matematiche su carta, con contro-modello e controlli razionali indipendenti.** Nessun teorema sulla vera traccia è assunto o aggiunto a Lean. Il risultato utile è un nuovo obbligo quantitativo, alternativo a H: controllare il tempo al quale la media dei cilindri vede una quota fissa della traccia del target, uniformemente nell'altezza del target.

## 1. Oggetti e dipendenze effettive

La fonte primaria è Lucas Valbuena, [Collatz basin densities and canonical traces](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/tao-basin-densities.tex), insieme a [Positive stationary envelope](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/positive-stationary-envelope.tex) e [Quadratic cylinder energy](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/quadratic-cylinder-energy.tex). La fotografia, le licenze e i confini dell'audit esterno sono quelli T03; non è stato eseguito un replay esterno.

Scriviamo λ per Haar additiva di probabilità su Z₃, μ=Eλ per la legge stazionaria e

`C_m(n)=n+3^m Z₃`, `ρ_m(n)=3^m μ(C_m(n))`.

Quindi ρ_m è la **media** di E nel cilindro, non il suo infimo. L'envelope della fonte è invece

`e_m(x)=inf{g(q):q>0, q≡x mod3^m}`, `E(x)=sup_m e_m(x)`.

Esso soddisfa `E(n)=g(n)` ai positivi interi e `e_m≤E` ovunque. La fonte fornisce E∈L^q(λ) per ogni 1≤q<2, ma E∉L², e identifica g attraverso il limite Cesàro delle ρ_m a **target fissato**. Nessuna di queste affermazioni dà una velocità uniforme quando cresce il target.

Per target senza ritorni, T03 ha isolato `g(n)=δ n D_n`, con δ=log(4/3)/2 e `D_n≤d_n≤P₀D_n`. Il nuovo risultato T01 del progetto rende utilizzabile P₀=exp27 nel perimetro dei primi arrivi. La positività delle densità effettive e le identità della traccia restano risultati esterni dichiarati.

## 2. Un criterio locale sufficiente, con quantificatori

**Criterio del singolo cilindro.** Fissati θ>0 e un esponente a<2, supponiamo esistano C e N₀ tali che, per ogni target intero n≥N₀ senza ritorni, si possa scegliere un intero m(n)≥0 con

`m(n)≤a log₃n+C`, `ρ_(m(n))(n)≥θ g(n)`.

Allora `g(n)=o(n)` attraverso quei target.

**Prova.** Scegliere una volta per tutte q con `max(1,a)<q<2`. Hölder sul vero cilindro C_m(n), di misura 3^−m, dà

`ρ_m(n)≤||E||_q ·3^(m/q)`.

Dunque

`g(n)≤θ^−1 ||E||_q 3^(C/q) n^(a/q)`.

Poiché a/q<1, dividere per n dà il limite zero. θ,q,C precedono tutti i target. Non è stato sostituito un valore intero a un integrale; l'integrale è quello del cilindro effettivo.

È sufficiente anche la più forte condizione `e_m(n)≥θg(n)`, perché e_m≤E nel cilindro implica la stessa minorazione per la media ρ_m.

**Versione critica con un solo esponente.** Se si conosce soltanto E∈L^p per un p>1, la condizione `e_m(n)≥θg(n)`, `m≤p log₃n+C` implica ancora g(n)=o(n). Infatti, se g(n_j)≥εn_j lungo una successione divergente, allora

`∫_{E≥θε n_j} E^p dλ ≥ (θε)^p 3^−C >0`.

Il membro sinistro tende invece a zero per integrabilità. Con la sola media ρ_m si ottiene lo stesso risultato da Hölder e assoluta continuità dell'integrale su cilindri di misura tendente a zero. Non serve un'ipotesi di disgiunzione dei cilindri.

Questo criterio non è stato dimostrato per E. È una formulazione precisa di ciò che manca: **una stabilizzazione locale uniforme prima della scala critica 2 log₃n**.

## 3. Perché il criterio escluderebbe la divergenza e lascia i cicli

Supponiamo vi sia una spine divergente di target dispari n_j, iniziata da un u positivo non multiplo di3. I suoi valori sono distinti e tendono a infinito. Ogni bacino B(n_j) contiene B(u), perciò `d_(n_j)≥d_u>0`. Confrontando le medie pesate:

`g(n_j)/n_j = δ D_(n_j) ≥δ d_u/P₀ >0`.

Questo contraddice g(n)=o(n) sui target senza ritorni. Il passaggio usa i risultati esterni sulle vere densità; non proviene dalla sola integrabilità Haar. Un ciclo è finito e i suoi punti hanno ritorni: il criterio non esclude cicli non banali.

Viceversa, su una ipotetica spine divergente la stessa disuguaglianza, insieme a Hölder, forza ogni profondità che realizzi `ρ_m(n_j)≥θg(n_j)` a soddisfare, per ciascun q<2,

`m≥q log₃ n_j−O_q(1)`.

Quindi un lower sul tempo di stabilizzazione vicino a 2 log₃n è perfettamente compatibile con tutti i bounds L^q noti. Proprio un upper uniforme sotto quella soglia sarebbe una nuova informazione.

## 4. Formulazione attraverso il kernel inverso reale

Nel dominio dei target dispari senza ritorni e non multipli di3, la fonte costruisce il kernel Doob

`p_a(z)=3·2^−a g((2^a z−1)/3)/g(z)`

sulle branche integrali con traccia positiva. Le foglie divisibili per3 hanno g=0 e non sono stati trattenuti del kernel.

Definiamo pertanto

`ρ_m^U(n)=S_1^m 1_{3∤}(n)`,

dove S₁ è l'operatore inverso accelerato non normalizzato. Si ha `0≤ρ_m^U≤ρ_m=S_1^m1`. Il telescopio dei pesi lungo un prefisso inverso dà l'identità esatta

`E_n^Doob[1/g(Y_m)] = ρ_m^U(n)/g(n)`.

**Non** si può cancellare g all'endpoint e ottenere tutta ρ_m: le foglie a traccia zero sarebbero state aggiunte indebitamente.

La proposizione della fonte *Periodic marked first-hit mean*, applicata alla maschera periodica `p(q)=1_{q dispari,3∤q}`, la cui media ordinaria è 1/3, implica per ogni root n fissato senza ritorni

`(1/K) Σ_(m≤K)ρ_m^U(n) → (2/3)g(n)`.

L'inclusione o esclusione di un termine iniziale cambia la media di o(1). Ne segue un limite Cesàro 2/3 per le aspettative inverse del reciproco della traccia, a root fissato.

Un nuovo lemma sufficiente da cercare è allora:

> Esistono a<2, C e θ>0 tali che, per ogni target n grande nel dominio, esiste K(n)≤a log₃n+C con `(1/K(n))Σ_(m<K(n)) E_n^Doob[1/g(Y_m)]≥θ`.

Qualche m<K(n) soddisfa ρ_m^U(n)≥θg(n), e il §2 si applica. È un **bound uniforme sul tempo di rilassamento di un osservabile preciso**. Il clock quasi sicuro `log Y_m/m→log(4/3)` a root fissato non lo fornisce: non controlla g(Y_m), la velocità iniziale o l'uniformità in n.

## 5. Contro-modello esatto alle deduzioni basate solo sulla regolarità

Questo modello **non è stazionario per Syracuse e non è una traccia Collatz**. Serve soltanto a confutare l'implicazione astratta “floor + L^q + mixing globale + traccia ai positivi ⇒ stabilizzazione uniforme/sublinearità”.

Per j≥1 porre

`n_j=2·3^j−1`, `C_j=n_j+3^(2j)Z₃`, `c=3/4`,

`F(x)=c·1_U(x)+Σ_(j≥1)3^j·1_(C_j)(x)`.

Se l>j, `ν₃(n_l−n_j)=j<2j`; i cilindri C_j sono quindi disgiunti. Essi accumulano soltanto al punto −1, che non è un positivo intero. F è nonnegativa, semicontinua inferiormente e finita ovunque. È localmente costante a ogni positivo intero.

Le sue proprietà sono esatte:

- `∫F dλ=(3/4)(2/3)+Σ3^−j=1`; F è zero fuori dalle unità e ha floor 3/4 sulle unità.
- `F(n_j)=3/4+3^j`, dunque `F(n_j)/n_j→1/2`.
- F∈L^q per 1≤q<2 e F∉L²: il contributo dei C_j è comparabile a `Σ3^((q−2)j)`.
- Le medie di cilindro di F convergono **ordinariamente**, non soltanto in Cesàro, a F(n) a ogni positivo intero, perché F vi è localmente costante.
- F è il massimo rappresentante semicontinuo inferiore della propria densità. Fuori da −1 è localmente costante; in ogni cilindro attorno a −1 il background con valore c ha misura positiva, quindi quel valore non può essere alzato mantenendo semicontinuità e la stessa misura.

Per l'inf-envelope della restrizione di F ai positivi:

`e_m(n_j)=c` per `1≤m<2j`, mentre `e_m(n_j)=F(n_j)` per `m≥2j`.

Nel primo caso un intero di background nello stesso cilindro è `4·3^m−1` se m≤j, e `n_j+2·3^m` se j<m<2j. Nel secondo caso tutto il cilindro è contenuto in C_j. Pertanto il primo m con `e_m(n_j)≥F(n_j)/2` è esattamente **2j**. Non si può dedurre un upper `a log₃n+C` con a<2 dalle proprietà elencate.

Il modello non riproduce la stazionarietà Syracuse, i valori infiniti su un Gδ denso, l'illimitatezza della traccia in ogni classe di unità o le identità aritmetiche delle vere densità. Non è una confutazione di H, né è stato dimostrato che n_j formi una spine Collatz o che tutti i n_j siano nonperiodici.

## 6. Il contro-modello ha anche mixing rapido ed energia piccola

Sia f_m la media di F sui cilindri di profondità m. I bump già risolti hanno j≤floor(m/2). Per positività e contrattività della media condizionata:

`||F−f_m||_1 ≤2 Σ_(j>floor(m/2))3^−j=3^−floor(m/2)`.

La convergenza globale L¹ è quindi esponenziale, più forte di un bound superpolinomiale.

Un calcolo per la partizione esatta dà, per m≥1,

`∫f_m² =9/8+floor(m/2)+Σ_(floor(m/2)<j<m)3^(m−2j)+(9/4)3^−m`.

In particolare è al più `m/2+9/4`, quindi O(m) e certamente ≤32m². Anche un miglioramento da energia quadratica a lineare, da solo, non darebbe il criterio locale.

La stazionarietà fallisce già al punto2:

`F(2)=3/4`,
`(LF)(2)=(1/2)F(4)+(3/2)F(1)=3/2`.

Dunque la futura prova deve usare struttura aritmetica o stazionarietà effettiva, oltre alle norme globali.

## 7. Soglia impossibile per un semplice rafforzamento del mixing globale

Sia δ_m=ρ_(m+1)−ρ_m. Essendo costante su cilindri di misura 3^−(m+1), vale

`||δ_m||_2 ≤3^((m+1)/2)||δ_m||_1`.

È la disuguaglianza finita ℓ²≤ℓ¹ sui valori della partizione, con la normalizzazione Haar. Quindi un rate globale `||δ_m||_1≤Cθ^m` con θ<1/√3 renderebbe sommabile la serie in L². Il limite L¹ coinciderebbe con un limite L², contraddicendo E∉L² della fonte.

La soglia è raggiunta dal contro-modello: errore L¹ dell'ordine 3^−m/2 ed esponente critico2. Non è sensato richiedere al vero mixing globale un rate più rapido per ottenere automaticamente il confronto atomico. Una stima locale o condizionata aritmeticamente può invece essere una domanda diversa.

## 8. Occupazione: cosa non dà il packing

Il controllo universale dei reciproci vale per segmenti di **interi positivi iniettivi**. Non può essere applicato a generiche traiettorie 3-adiche della legge stazionaria.

Per un cammino inverso reale, i bounds di packing danno soltanto un cap del numero di visite sotto R dell'ordine R^β (o, dal solo budget81, 81R). Dividendo per logR questi cap divergono: non dimostrano l'uniforme integrabilità necessaria per passare dal clock quasi sicuro alle aspettative. L'upper matching della raw occupation rimane aperto.

Anche il contro-modello può essere modificato mettendo bump di altezza b·3^j su cilindri di profondità 2j+M. Scegliendo M grande si mantiene massa totale uno e un floor positivo, con b arbitrariamente grande. La sola sottosuccessione n_j contribuisce `b/(2log3)·logR+o(logR)` a `Σ_(n≤R)F(n)/n`. Quindi una costante superiore aritmetica non segue dai soli bounds Haar elencati.

## 9. Un correlatore affine da studiare separatamente

Dalla ricorrenza binaria effettiva della fonte

`ρ_(k+1)(x)=(1/2)ρ_(k+1)(2x)+(3/2)1_(x≡2mod3)ρ_k((2x−1)/3)`

si ricava, quadrando e cambiando variabile x=(3y+1)/2,

`N_(k+1)−N_k=(2/3)∫ρ_(k+1)(3y+1)ρ_k(y)dλ(y)`,

dove `N_k=∫ρ_k²`. Un cap uniforme di questo correlatore darebbe N_k=O(k). **Quel cap non è stato dimostrato.** L'identità è un sottobersaglio specifico per tecniche di collisione o mixing affine, ma il contro-modello mostra già che energia lineare non sarebbe una prova di η o di sublinearità della traccia.

## Verifiche e confronto fra agenti

Il protocollo del contro-modello è stato fissato prima dell'esecuzione in `research/research_sprint_2026-11-15/t07/protocol.json`: j=1,...,12, m=1,...,24, interi1,...,300, enumerazione completa dei residui ai primi7 livelli. Il programma usa Fraction e confronta formula chiusa con un calcolo indipendente delle intersezioni di cilindri.

PASS: 66 coppie disgiunte, 7.536 controlli di densità condizionata, 144 testimoni di background, 3.279 residui enumerati e difetto stazionario esplicito. Output normale e Python -O identici; SHA-256 dei dati `2f07bebc3e73d7890251bc1d32dc8674aac7b55e62f4579c1788823351f1933d`.

Il coordinatore ha controllato la normalizzazione del modello e la soglia locale. T08 sta usando lo stesso modello per distinguere mixing congiunto astratto e ricorrenza affine effettiva. T09 ha ricevuto criterio, dominio dei leaf e definizioni per revisione indipendente. Nessun nuovo modulo Lean, assioma o upgrade è stato introdotto da T07.

**Prosecuzione concreta:** tentare un lower quantitativo del Cesàro di `E_n^Doob[1/g(Y_m)]` entro una profondità ≤a log₃n+C con a<2, oppure trovare un meccanismo che lo renda falso. Le stime note a root fissato, il solo clock d'altezza e le norme Haar non soddisfano questo obbligo.

## Aggiornamento di revisione e correlatore, 20:46 UTC

T09 ha ricostruito indipendentemente il criterio di Hölder e il contro-modello. Ha anche semplificato l'energia esatta:

- m=2r≥2: `∫f_m²=r+5/4+(9/8)9^−r`;
- m=2r+1: `∫f_m²=r+3/2+(3/8)9^−r`.

È quindi al più `m/2+11/8`. Le formule sono coerenti con quelle del §6.

Le costanti del criterio possono dipendere da ε>0 e il rate può essere richiesto soltanto sui target con d_n≥ε: una divergentspine mantiene un tale lower. Nel quadro della tightness esterna, questi target hanno un piccolo antenato; se tutte le orbite sono eventualmente periodiche, per ogni ε il loro insieme è finito e il criterio grande-n diventa vacuo. Questa variante è dunque un criterio equivalente nel quadro esterno, non un lower già ottenuto dalle norme.

Per il correlatore effettivo del §9 è stato congelato un protocollo distinto prima dell'esecuzione: k=0,...,11, stessi livelli stazionari T03 fino alla profondità12, controllo Fraction esatto per k≤3. Il costruttore delle leggi finite T03 è riutilizzato dopo lettura; non si rivendica un secondo algoritmo indipendente per tali leggi. L'identità energetica nuova viene controllata separatamente, inclusa la somma su tutti i residui della profondità giusta.

PASS normale e Python -O, output identico, SHA-256 `cf5588e9ea7433e87e3fef269cd83b3f4c6347731514c16ea8936864c10dcf33`. A profondità12, N_12≈6.8029. I correlatori ai livelli2,...,11 vanno circa da0.692 a0.703: **non è una stima uniforme** e non viene ampliata la scansione.

Quel correlatore è anche una densità puntuale della convoluzione della legge di X−3Y, per X,Y indipendenti con legge μ. La sola informazione L^p, p<2, non dà il bound L∞ necessario per valutarla uniformemente nel punto1: un ulteriore gap di traccia rimane anche qui.

## Appendice: criterio di escape a blocchi, candidato da revisionare

Questa deduzione è emersa alla chiusura T07. Il coordinatore la affida a un revisore fresco; **non è ancora promossa a risultato revisionato**. L'ipotesi di rilassamento resta non dimostrata.

Il criterio Doob del §4 sembra sufficiente anche con

`a<log3/log(3/2)≈2.7095`,

senza usare L^p. Supponiamo una spine divergente u=n_0,n_1,... con densità base positiva. Per tutti i j, `D_(n_j)≥D_u/P₀`, dunque `g(n_j)≥c_u n_j→∞`. Poiché `n_j+1≤(3/2)^j(u+1)`, un tempo `m_j≤a log₃n_j+C` soddisfa `m_j≤b j+C'` con b<1. Il lower Cesàro dell'osservabile fornisce almeno un tale m_j con

`E_(n_j)^Doob[1/g(Y_(m_j))]≥θ`.

Sull'evento che i primi m_j passi ripercorrano esattamente la spine, l'endpoint è n_(j−m_j). Uniformemente su m_j≤b j+C', il suo indice tende a infinito, quindi il reciproco della traccia tende a zero. Fuori dall'evento il reciproco è al più1/c₀, dal floor globale. Per j grande, il lower θ forza pertanto una probabilità almeno c₀θ/2 di uscire da quel prefisso.

Si sceglie un indice J₀ oltre tutte le soglie. Ogni blocco porta j a j−m_j≥c j per un c>0 fissato e, per j≥J₀, m_j≥1. Per scendere da un j grande sotto J₀ occorrono almeno un numero di blocchi dell'ordine logj. Per la proprietà di Markov, la probabilità di seguire la spine in tutti questi blocchi è al più `(1−c₀θ/2)^(numero_blocchi)`, che tende a zero.

Tuttavia la probabilità di ripercorrere l'intera spine da n_j fino a u è, per telescopio,

`w_(n_j)(u) D_u/D_(n_j) ≥D_u/P₀>0`,

uniformemente in j. Questa è una contraddizione. Il caso m_j=0 non può essere il tempo selezionato per j grande, perché 1/g(n_j)→0.

I punti da verificare nella revisione sono la consistenza dello stesso kernel Doob al cambiare della root, la selezione dei tempi m_j e l'iterazione dei blocchi con soglie uniformi. Se corretta, questa prova amplia la soglia sufficiente da2 a log3/log(3/2), ma **non fornisce il lower uniforme dell'osservabile**. È un meccanismo di esclusione condizionale, non una prova della convergenza.
