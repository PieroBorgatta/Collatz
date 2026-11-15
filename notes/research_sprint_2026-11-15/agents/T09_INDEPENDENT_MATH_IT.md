# T09 Revisione matematica indipendente: cap, traccia e rilassamento

15 novembre 2026. **Esito: le deduzioni T07/T08 e l'avversario puntuale T06 resistono alla ricostruzione indipendente**, nei domini specificati sotto. Sono prove su carta e controlli finiti; T09 non ha modificato moduli Lean né importato nuovi assiomi o risultati esterni. La velocità uniforme di rilassamento e la quota η restano aperte.

## 1 Conteggio con cap: ricostruzione e bordi

Sia n un target positivo dispari. Scegliere il primo arrivo di ogni sorgente dispari che lo raggiunge con esponenti tutti in {1,…,M}. Ciò è lecito anche per target periodici: il primo arrivo è un prefisso di ogni cammino con cap. Una parola di lunghezza k e il target determinano al più una sorgente, per l'identità affine.

Per ogni r≥0 e X≥1, il conteggio fisico dispari soddisfa

`N_M^odd(n,X) ≤ Σ_(k<r) M^k + (X/2)(1−2^−M)^r + M^r`.

Gli arrivi brevi danno il primo termine. Gli altri inizi hanno un prefisso di r esponenti con cap; una parola di totale A è una classe dispari modulo 2^(A+1), quindi il count è al più X/2^(A+1)+1. Sommando le M^r parole, il peso è `(1/2)(Σ_(a=1)^M 2^−a)^r` e l'errore al più M^r. Questo usa cilindri esatti della mappa, non indipendenza postulata su una singola orbita.

Per r=0, occorre tenere il dominio dispari: il count è≤X/2+1. La parola vuota presa da sola non impone parità. Il termine di arrivo vuoto u=n è incluso nel primo termine appena r≥1.

Con θ=1−2^−M, M≥2, e `α=log M/log(M/θ)`, porre `r=floor(log X/log(M/θ))`. Si ha

`M^r≤X^α`, `Xθ^r≤θ^−1 X^α`,

`Σ_(k<r) M^k+M^r≤[M/(M−1)]M^r`.

Il coefficiente totale è≤2+2/3<3; dunque `N_M^odd(n,X)≤3X^α`. Tutte le costanti sono uniformi in n,M,X. Poiché `Mθ²≥2(3/4)²>1`, segue α≥2/3; inoltre 2^−2/3<2/3, quindi la somma dei lift ordinari dà

`N_M^ord(n,X)≤9X^α`.

Il medesimo M resta fissato nei cutoff X/2^e, anche quando viene scelto come M(X). Si applica il bound dispari ai cutoff≥1; quelli sotto uno hanno count zero. Infine

`1−α≥2^−M/(2 log M)`.

Questo dimostra già o(X) per `M(X)≤(1−ε)log₂log X`, 0<ε<1. Per M=1 la formula iniziale dà O(log X) sorgenti dispari e O((log X)²) lift.

## 2 Rafforzamento con overflow del clock

Ho ricostruito separatamente il successivo bound T08, più forte. Porre `L=floor(log₂X)`, `r=floor(L/8)`. Si ottiene, per tutti M≥1,

`N_M^odd(n,X)≤Xθ^r+3X^(3/4)`,

`N_M^ord(n,X)≤6Xθ^r+8X^(3/4)`.

I tre passi sono:

1. Se il primo arrivo ha k<r, il budget esatto `2^A n≤4^k X` implica A≤L+2k. Il numero di parole è≤Σ_(k≤r)binom(L+2r,k)≤4^r(5/4)^(L+2r)≤X^(3/4). L'ultima stima segue da `5^10<2^24`.
2. Per un prefisso lungo r con A_r≤L, il modulo q=2^(A_r+1) è≤2X. Il count di una classe è≤ceil(X/q)≤2X/q perché X/q≥1/2. Sommando si ottiene Xθ^r, senza errore M^r.
3. Se A_r>L, tra i primi L passi shortcut vi sono al più r stati dispari: tutti appartengono ai primi r episodi accelerati. Ogni classe modulo 2^L ha al più due input≤X. L'identità dei momenti di parità con parametro 1/4 limita questo overflow a `2·4^r(5/4)^L≤2X^(3/4)`; basta `5^8<2^20`.

Per i lift, `floor(L/8)−floor((L−e)/8)≤ceil(e/8)` e θ≥1/2. Quindi la parte principale è≤`2Xθ^r Σ2^(−7e/8)≤6Xθ^r`. La coda di errore è≤`3X^(3/4)/(1−2^(−3/4))≤8X^(3/4)`, usando 2^(−3/4)<5/8. I bordi r=0 e L<8 danno semplicemente una maggiorazione grossolana ma valida.

Ne segue o(X) sotto la condizione più debole

`2^(M(X))=o(log X)`,

ossia `M(X)≤log₂log X−h(X)` con h(X)→∞. Un count lineare≥δX impone viceversa `M(X)≥log₂log X−O_δ(1)`: dal bound ordinario, θ^r≥δ/12 per X grande, quindi r2^−M≤log(12/δ). Superare tale soglia non garantisce una quota η.

Il limite si applica a immagini di un flusso con altezza≤DX e carico incoming limitato: se il loro intero primo arrivo è soggetto a questo cap, vi sono soltanto o(X) immagini e il flusso totale è o(X). Per un pool di J(X) target, l'uniformità fornisce anche un upper moltiplicato per J(X); occorre controllare quel fattore prima di concludere.

## 3 Criterio locale da Hölder: corretto ma condizionale

Sia μ=Eλ la vera legge stazionaria della fonte, con Haar additiva λ, `ρ_m(n)=3^m μ(n+3^mZ₃)` e E∈L^q per q<2. La media del cilindro non è il valore intero della traccia g.

Se θ>0, a<2 e C sono uniformi e ogni target grande nel dominio possiede m≤a log₃n+C con ρ_m(n)≥θg(n), scegliere `max(1,a)<q<2`. Hölder dà

`g(n)≤θ^−1||E||_q·3^(C/q)n^(a/q)=o(n)`.

Non occorre che cilindri distinti siano disgiunti. Alla soglia m≤p log₃n+C, con E∈L^p, la stessa conclusione richiede usare l'assoluta continuità dell'integrale sul cilindro, o un inf-envelope che forzi una coda L^p non piccola. T07 distingue correttamente queste due formulazioni.

È sufficiente richiedere il bound, con costanti dipendenti da ε, soltanto sui target nonperiodici con d_n≥ε, per ogni ε>0. Una spine divergente mantiene d_n≥d_base>0 e vi ricade. Questa variante non è un nuovo teorema analitico: nel quadro esterno, se tutte le orbite sono eventualmente periodiche, i target di massa≥ε sono finiti per la tightness dei bacini senza piccoli antenati. Il criterio sui target grandi diventa allora vacuo. La sua utilità è isolare un obbligo quantitativo, non ricavarlo dalle norme note.

## 4 Doob reale: seed, normalizzazione e rilassamento

Il kernel inverso trattiene solo figli con g>0, cioè positivi dispari non multipli di tre. Il telescopio dei pesi dà esattamente

`E_n^Doob[1/g(Y_m)]=ρ_m^U(n)/g(n)`, `ρ_m^U=S_1^m1_(3∤)`.

È scorretto sostituire ρ_m^U con tutta ρ_m: le foglie a traccia zero non sopravvivono alla divisione. Si ha però ρ_m^U≤ρ_m, sufficiente al criterio precedente. La proposizione *Periodic marked first-hit mean* nel sorgente `positive-stationary-envelope.tex`, applicata alla maschera odd-unità di media 1/3, dà il limite Cesàro 2g(n)/3 a root fissato; quindi le aspettative inverse hanno limite Cesàro 2/3. Non dà una velocità uniforme nei target.

### Criterio di escape a blocchi, senza L^q

Ho ricostruito indipendentemente anche il nuovo candidato T07. È valido su carta, assumendo un floor globale c>0 della vera traccia sulle unità e le identità esterne fra g,D,d.

Supporre θ>0 uniforme e, per ogni grande target nonperiodico, l'esistenza di m(n)≤K(n) con `E_n[1/g(Y_m)]≥θ`. È sufficiente un upper

`K(n)≤a log₃n+C`, `a<log3/log(3/2)`.

Su una spine divergente n_j=S^j(u), i bacini sono annidati e dunque `g(n_j)≥c_u n_j→∞`. Inoltre `n_j+1≤(3/2)^j(u+1)`, perciò `m_j≤bj+C_u`, b<1. Sul backtracking esatto di m_j passi l'osservabile è `1/g(n_(j−m_j))→0`, uniformemente perché j−m_j→∞. Fuori da quel prefisso è≤1/c. Un'aspettativa≥θ forza quindi una probabilità di escape≥θc/2, per tutti i j grandi.

Concatenare i blocchi deterministici j→j−m_j fino a una soglia fissa J. Il loro numero tende a infinito. Per la proprietà Markov, la probabilità di backtracking completo è≤(1−θc/2)^(numero_blocchi)→0. Ma il telescopio esatto fornisce

`P(full backtrack j)=D_u/[P(u→n_j)D_(n_j)]≥D_u/P₀>0`,

poiché D_(n_j)≤1 e P≤P₀. Contraddizione. Il caso m=0 non crea un buco: sulla spine grande il suo valore è 1/g(n_j)<θ, quindi la scelta efficace ha m≥1.

Un rafforzamento T09 riduce il margine richiesto a un deficit additivo divergente:

`K(n)≤log_(3/2)n−h(n)+C`, `h(n)→∞`.

Infatti j−m_j≥h(n_j)−O_u(1)→∞. La mappa f(j)=j−m_j soddisfa f(j)<j e f(j)→∞; per ogni numero fisso R di blocchi, f^R(j)→∞. Il numero di blocchi necessario per scendere a J diverge ancora. La stessa prova si applica. **Nessuno di questi upper uniformi sul tempo di rilassamento è stato dimostrato.**

## 5 Contro-modello T07: audit esatto

Con `n_j=2·3^j−1`, `C_j=n_j+3^(2j)Z₃`, il modello

`F=(3/4)1_unità+Σ3^j1_Cj`

ha le proprietà dichiarate. I C_j sono disgiunti perché la valutazione ternaria di n_l−n_j è min(j,l). La massa è `(3/4)(2/3)+Σ3^−j=1`. L^p è finito esattamente per p<2, p≥1. F è localmente costante fuori da −1, dunque in ogni positivo intero, e la sua restrizione ai positivi dà il massimo rappresentante lsc della stessa densità. Presso −1 ogni intorno ha background di misura positiva, impedendo di alzare il valore lsc mantenendo uguaglianza quasi ovunque.

Per le medie f_m del modello, ho derivato indipendentemente le formule più precise:

- m=2r≥2: `∫f_m²=r+5/4+(9/8)9^−r`;
- m=2r+1: `∫f_m²=r+3/2+(3/8)9^−r`.

Quindi `∫f_m²≤m/2+11/8`, mentre `||F−f_m||_1≤3^−floor(m/2)` e l'ordine esponenziale è esattamente 3^(−m/2). Il sibling di n_j è `16n_j+5≡1 mod3`, dunque ha F=3/4; il rapporto trasverso decade come 3^−j, molto più rapidamente di 1/log n_j.

Il modello **non** è stazionario Syracuse: F(2)=3/4, ma `(LF)(2)=(1/2)F(4)+(3/2)F(1)=3/2`. Non riproduce neppure tutte le altre proprietà della vera envelope (valori infiniti su Gδ denso, trace illimitata in ogni classe). Confuta solo l'implicazione dai bounds astratti effettivamente usati, non H o le formule della legge affine reale.

Si può rendere il contrasto con l'occupazione uniforme: bump b·3^j a profondità2j+M, con M≥2log₃b, mantengono uniformi in b bounds L^p per p<2, energia O(m) e rate L¹ alla soglia3^(−m/2), dopo normalizzazione del background. I centri contribuiscono invece almeno `b/(2log3)·logR+o(logR)` alla somma aritmetica dei reciproci pesati. Neppure la costante superiore di quell'occupazione aritmetica può venire dai soli bounds Haar uniformi.

Per rendere esplicita quest'ultima uniformità, prendere b≥1, M intero con 3^M≥b² e background `c_b=(3/2)(1−b/(2·3^M))`, compreso fra3/4 e3/2. Il contributo dei bump alla norma L^p è controllato da `b^p3^−M Σ3^((p−2)j)`, uniformemente in b per p<2. Separando i bump già risolti da quelli di coda, con J=floor((m−M)/2), la coda ha massa `(b/2)3^−M3^−max(J,0)`. Contrattività L¹ dà un errore≤√3·3^(−m/2) per m≥1, mentre il bound finito L¹→L² sulla partizione dà energia della coda≤3/4. Ogni bump risolto aggiunge al più b²3^−M≤1 all'energia. Includendo il background si ottiene, per esempio, `∫f_m²≤m/2+15/4` uniformemente in b. La nonappartenenza a L² resta vera per ogni b,M fissati: vi sono infiniti bump, ciascuno con energia positiva b²3^−M.

## 6 CDF delle capacità e avversario ordinale

Il nuovo criterio CDF T08 è corretto per liste fisiche finite: con capacità incoming m≥1, un'assegnazione di ogni u a v con ρ(v)≤Cρ(u) esiste se e solo se `m V(Ct)≥U(t)` per tutte le soglie. Ordinando, assegnare u_i a v_(ceil(i/m)); il caso di valori ρ uguali non crea problemi, perché U(ρ(u_i))≥i. La disuguaglianza CDF resta un input non dimostrato per i due veri cataloghi.

L'avversario ordinale T06 è coerente in segni e indici. Il ramo negativo minimo interno da z₀=−11 non raggiunge−1, quindi |z_i|≥3. Il telescopio dà `2^(B_t−t)≥(3/11)(9/7)^t`. Per `n_t=18·3^t−1`, la base ha prefisso inverso tutto1 e sorgente `u_t=18·2^t−1`; l'immagine è `v_t=288·2^B_t+z_t≥277·2^B_t`. Segue `v_t/u_t≥(277/66)(9/7)^t`. La continuazione di rango2R dà input arbitrariamente grandi a target fissato, ma solo O(log X) di essi fino a X. Non è un no-go di massa dopo scarto o(X).

## 7 Replay indipendente e limiti della verifica

Il protocollo T09 è stato fissato alle20:42:56 UTC prima dell'esecuzione. Il programma non importa i programmi T07/T08: conta direttamente orbite forward di 1024 sorgenti dispari≤2048 e costruisce le medie Haar sommando i cilindri disgiunti, con coda geometrica esatta.

PASS: 12.096 controlli razionali sulle disuguaglianze cap, 336 righe finite cap/target/cutoff, 9.841 controlli di compatibilità delle medie condizionate, 29.524 residui ai livelli0…9. Il confronto dei bounds ottimizzati con α usa Decimal a70 cifre solo come controllo finito, non come prova dell'ottimizzazione analitica. Output normale e Python -O identici, SHA-256 `0712ffe8507f2e214e563baa17943770a1b74eea0c6c30649f0018a9bf3b709d`.

File: `research/research_sprint_2026-11-15/t09/{protocol.json,independent_audit.py,independent_result.json,independent_result_optimized.json,receipt.json}`. Nessun risultato su carta di questa revisione viene presentato come teorema Lean o come soluzione di Collatz.

## 8 Un limite per un tentativo di Lyapunov a stato finito

Questo è un vincolo su una possibile prova del rate Doob, non una confutazione di quel rate. Sia h nonnegativa, positiva su qualche cilindro di unità, e dipendente da un numero fisso di cifre ternarie. Per f=1/g, il kernel reale soddisfa

`Q(fh)(n)=S_1(1_U h)(n)/g(n)`.

Un drift uniforme `Q(fh)≥λfh`, λ>1, su tutti i target grandi nonperiodici implicherebbe `S_1(1_Uh)≥λh` su un insieme denso di unità. Tale densità non richiede Collatz: i target `(4^a−1)/3>1` arrivano in un solo passo a1 e sono densi nelle classi ternarie. Infatti4 ha ordine3^m modulo3^(m+1), come si verifica per induzione dalla valutazione `ν₃(4^(3^m)−1)=m+1`.

L'operatore S_1 porta una funzione cilindrica a un'altra funzione cilindrica, aumentando la profondità finita al più di uno. La disuguaglianza su un insieme denso si estenderebbe quindi a tutte le unità. Ma S_1 preserva l'integrale Haar delle densità e produce zero fuori dalle unità:

`∫_U S_1(1_Uh)dλ=∫_U h dλ`.

L'integrazione della disuguaglianza con λ>1 dà una contraddizione. La stessa osservazione vale per un orizzonte fisso di più passi. Non esclude moltiplicatori con conduttore crescente, tempi dipendenti dall'altezza, un criterio a blocchi o una restrizione ai soli target di massa positiva fissata: questi ultimi non sono l'insieme denso usato nell'argomento.

## 9 Dove entra il root variabile nella prova del clock della fonte

Ho letto anche il passaggio della fonte `tao-basin-densities.tex`, sezione *An almost-sure clock for the actual inverse law*. Il trasferimento finito dei clock conserva la correzione

`T_n(M)=max{k_n(y): y≤M, y dispari, y∈B_n}`

oltre a logM/λ. Essa è finita a n,M fissati e può essere eliminata dividendo per logaritmi di barriere che tendono a infinito. La prova non dà un controllo di T_n(M) uniforme nel target n. Al cambiare del root, questa quantità contiene veri tempi di primo arrivo da piccoli antenati; il budget81 e le sole norme Haar non la limitano. Questo identifica il punto esatto in cui il clock quasi sicuro esistente non produce il nuovo upper uniforme del tempo di rilassamento. Non è stata trovata una nuova stima che chiuda quel passaggio.
