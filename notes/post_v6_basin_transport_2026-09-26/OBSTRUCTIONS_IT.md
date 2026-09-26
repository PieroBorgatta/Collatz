# Ostacoli al trasporto dei bacini: che cosa è confutato e che cosa resta aperto

26 settembre 2026. Nota matematica interna, senza rivendicazione di
originalità. Le dimostrazioni sotto sono su carta; questa nota non introduce
una formalizzazione Lean, un nuovo censimento o una verifica dei teoremi
analitici esterni.

**Esito:** non troviamo una confutazione dell'ipotesi H sulle densità
asintotiche. Otteniamo però un ostacolo asintotico a un metodo preciso:
a target fissato, cambiare soltanto l'ultimo esponente aumentandolo trasporta
entro ogni cutoff moltiplicativo fisso soltanto un insieme di sorgenti di
densità zero. Il risultato vale per l'intero bacino; permettendo diminuzioni
dell'esponente, vale ancora sul sottobacino B(11) della coppia 17/277.
Separatamente, un accoppiamento puntuale arbitrario che conservi la profondità
deve talvolta pagare una dilatazione crescente, anche sul dominio di
nonritorno richiesto da H. Il packing, da solo, non confuta H e nemmeno una
sua versione simmetrica locale sufficientemente debole.

## 1. Enunciato da non alterare durante il test

Per n dispari positivo non divisibile per 3, poniamo

\[
h(n)=\begin{cases}4n+1&n\equiv1\pmod3,\\16n+5&n\equiv2\pmod3.\end{cases}
\]

Vale `S(h(n))=S(n)`, con S accelerata sui dispari. Sia B(n) il bacino
ordinario positivo di n, e `d_*(n)` la sua densità naturale inferiore.
La [proposta precedente](../post_v6_reset_2026-09-26/NEW_DIRECTION_IT.md) è

\[
\tag{H}
\exists c>0\quad
d_*(h(n))\ge\frac{c}{1+\log n}\,d_*(n)
\]

per tutti i target ammessi per i quali sia n sia h(n) non hanno ritorni
positivi. Non si assume l'esistenza della densità naturale ordinaria.
La positività del bacino di ogni target non divisibile per 3 è un input
analitico esterno distinto. Una prova di H insieme a quell'input escluderebbe
le orbite illimitate; non escluderebbe i cicli non banali.

## 1bis. L'ultimo esponente nonnegativo perde massa a target fissato

Questo risultato riguarda sorgenti di un **medesimo** bacino e il limite
`X→∞`. È quindi più forte, per il metodo considerato, dell'esibizione di una
sola sorgente cattiva per ogni target. Usiamo la formula affine del trasporto
di [SOURCES_IT.md, §3](SOURCES_IT.md); ne riportiamo gli elementi necessari
per rendere controllabile il passaggio asintotico.

Fissiamo due dispari positivi `n<y`. Per una sorgente ordinaria positiva
`x=2^e u`, con u dispari e `x∈B(n)`, sia k il primo tempo in cui `S^k(u)=n`.
Se `k≥1`, la sua parola esatta `(a_1,…,a_k)` ha tutti gli esponenti positivi.
Scriviamo `A=Σa_i`. L'identità affine è

\[
3^k u+C=2^A n,\qquad
C=\sum_{j=0}^{k-1}3^{k-1-j}2^{a_1+\cdots+a_j}>0,
\tag{A1}
\]

dove la somma vuota nell'esponente è zero. In particolare C non dipende
dall'ultimo esponente `a_k`.

Un trasporto dell'ultimo esponente conserva i primi `k−1` esponenti e
trasforma l'ultimo in `a_k+δ`, con `a_k+δ≥1`, in modo che la parola termini
in y. Per `δ≥0`, la condizione aritmetica è

\[
2^\delta y\equiv n\pmod{3^k},\qquad
q=\frac{2^\delta y-n}{3^k}\in\mathbb N_{>0}.
\]

La sorgente trasformata soddisfa esattamente

\[
u'=u+2^Aq,\qquad x'=2^e u'.
\]

Poiché `q≥1` e, per (A1), `n2^A>3^k u`, segue

\[
\boxed{n x'>(n+3^k)x.}
\tag{A2}
\]

La scelta di δ può dipendere da tutta la sorgente, dalla parola, dalla
profondità e dal fattore diadico. Non occorre che il trasporto sia iniettivo.
Si richiedono soltanto la modifica indicata e la conservazione di `2^e`.

**Proposizione asintotica.** Sia T qualsiasi regola di questo tipo sul bacino
B(n), eventualmente definita soltanto su una sua parte. Per ogni numero
reale fisso `D>0`, l'insieme delle sorgenti `x≤X` per le quali T è definita e
`T(x)≤DX` ha cardinalità `o(X)`. Il valore D può dipendere arbitrariamente
dai target n,y, che restano fissati durante il limite.

**Prova.** Fissiamo un intero `K≥1`. Per `x≤X`, anche la parte dispari
`u≤X`; inoltre `S^j(u)≤2^jX`. Per tutti i passi di una parola di lunghezza
al più K, la valutazione esatta soddisfa

\[
a_i\le\log_2(3\,2^KX+1)\le\log_2X+K+2.
\]

Posto `M_X=⌊log_2 X⌋+K+3`, ci sono al più `Σ_(j=0)^K M_X^j`
parole di lunghezza al più K. Ogni parola, insieme al target n, determina
al più una sorgente dispari tramite (A1). Ogni sorgente dispari ha al più
`1+⌊log_2 X⌋` sollevamenti diadici fino a X. Le sorgenti con `k≤K`,
compreso `k=0`, sono perciò

\[
O_K\bigl((1+\log X)^{K+1}\bigr)=o(X).
\tag{A3}
\]

Per le rimanenti sorgenti, `k>K` e (A2), insieme a `T(x)≤DX`, implica

\[
x<\frac{nDX}{3^k}\le\frac{nDX}{3^K}.
\]

Il loro numero è quindi al più `nDX/3^K`. Dividendo per X e passando al
limite superiore otteniamo un valore al più `nD/3^K`. Poiché questo vale
per ogni K, il limite superiore è zero. La regola applicata alle sorgenti
di profondità zero è irrilevante: esse sono la sola successione `2^e n`,
già inclusa nel termine (A3). □

Se si assume `d_*(B(n))>0`, segue anche che la frazione di B(n) fino a X
che il metodo porta entro DX tende a zero. La sola conclusione `o(X)` è
incondizionata; la positività necessaria per parlare di frazione relativa
è l'input analitico esterno. Il teorema non esclude una grande massa in
B(y) prodotta da altre sorgenti, né un diverso trasporto del bacino.

### La variante con δ firmato: un sottobacino esplicito

Consideriamo la coppia fissa `n=17`, `y=h(17)=277`. Sono entrambi nel dominio
senza ritorni di H, come certificano le orbite

\[
11\longmapsto17\longmapsto13\longmapsto5\longmapsto1,
\qquad277\longmapsto13\longmapsto5\longmapsto1.
\]

Per ogni sorgente di B(11), la parola fino al primo arrivo in 17 termina
con il passo `11→17`, il cui esponente è 1. Non può esserci stato un arrivo
precedente in 17, perché l'orbita successiva di 17 non visita 11. Pertanto
`a_k=1` e la condizione `a_k+δ≥1` forza `δ≥0`, anche quando il metodo in
generale permette shift negativi. La proposizione si applica dunque a
tutte le sorgenti del sottobacino B(11): a ogni dilatazione D finita, soltanto
`o(X)` di esse vengono portate entro DX dal cambio dell'ultimo esponente.

Con l'input `d_*(B(11))>0`, il metodo non trasporta una frazione positiva
di quel sottobacino. Questo è un ostacolo sul dominio effettivo di H e a
target fissato. **Non** dimostra il fallimento di H: un confronto di densità
può usare altri rami di B(17), cambiare più esponenti, variare la profondità
o confrontare masse senza un accoppiamento di questa forma. Non estendiamo
automaticamente il risultato firmato a tutto B(17), perché un'unione
numerabile di sottobacini richiede il controllo delle code discusso nel §5.

## 2. Un ostacolo a tutti i trasporti puntuali a profondità uguale

Per `k≥1` e `t≥1` interi, definiamo

\[
n_{k,t}=2t3^{k+2}-1=18t3^k-1,\qquad
u_{k,t}=18t2^k-1,\qquad
y_{k,t}=h(n_{k,t})=288t3^k-11.
\]

La formula per h è corretta perché `n_(k,t)≡2 mod3`. La sorgente u ha
esattamente k esponenti iniziali tutti uguali a 1:

\[
S^j(u_{k,t})=18t3^j2^{k-j}-1\quad(0\le j\le k).
\]

Per j<k, infatti, il numeratore del passo è
`2(27t3^j2^(k−j)−1)`, con fattore fra parentesi dispari. Dunque
`S^k(u_(k,t))=n_(k,t)`.

**Proposizione.** Qualunque v dispari positivo con
`S^k(v)=y_(k,t)` soddisfa

\[
\boxed{\frac{v}{u_{k,t}}>16\left(\frac{33}{23}\right)^k.}
\tag{1}
\]

La parola di v può essere completamente diversa da quella di u. Non si
preserva alcun esponente individuale, somma di esponenti o residuo della
sorgente: l'unico vincolo aggiunto è l'uguaglianza della profondità k.

### 2.1 Trasferimento esatto a un'orbita negativa

Leggiamo al contrario la parola effettiva che porta v a y. Siano
`v_0=y`, `v_k=v` e `b_i≥1` gli esponenti letti in questo ordine; allora

\[
3v_i=2^{b_i}v_{i-1}-1,\qquad B_i=\sum_{j=1}^i b_j.
\]

Poniamo `q_0=11` e

\[
3q_i=2^{b_i}q_{i-1}+1.
\tag{2}
\]

Questi q sono interi, non soltanto razionali. Infatti

\[
v_i+q_i=288t3^{k-i}2^{B_i}\qquad(0\le i\le k).
\tag{3}
\]

La formula segue per induzione dalle due ricorrenze e dalla base
`y+11=288t3^k`. Il membro destro è intero per tutti gli indici usati,
quindi q_i è intero. La (2) mostra anche positività e disparità. Inoltre
`3q_i−1=2^(b_i)q_(i−1)`, con q_(i−1) dispari, certifica l'esponente esatto.

Introduciamo la dinamica sui moduli degli interi negativi dispari

\[
U(q)=\frac{3q-1}{2^{\nu_2(3q-1)}}.
\]

Abbiamo `U(q_i)=q_(i−1)` e quindi `U^i(q_i)=11`. L'insieme

\[
E_- = \{1,3,5,7,9,13,19\}
\]

è invariante in avanti, come mostrano tutte le sue transizioni:

\[
1\to1,\quad3\to1,\quad5\to7\to5,\quad9\to13\to19\to7.
\]

Poiché `11∉E_-`, nessun q_i appartiene a E_-. In particolare, tutti gli
interi dispari positivi minori di 11 sono esclusi:

\[
q_i\ge11\qquad(0\le i\le k).
\tag{4}
\]

### 2.2 Costo degli esponenti e dilatazione

Nella (2), `2^(b_i)q_(i−1)≥22`. Pertanto

\[
3q_i\le\frac{23}{22}\,2^{b_i}q_{i-1},\qquad
q_k\le11\left(\frac{23}{66}\right)^k2^B,
\]

con `B=B_k`. Usando `q_k≥11` otteniamo

\[
2^{B-k}\ge\left(\frac{33}{23}\right)^k.
\tag{5}
\]

Serve anche una maggiorazione elementare distinta. Per R≥2,
`(R+1)/3≤R/2`; applicata alla (2) dà

\[
q_k\le11\,2^{B-k}.
\tag{6}
\]

La (3) all'ultimo indice dice `v=288t2^B−q_k`. Ne segue

\[
v-16\,2^{B-k}u_{k,t}
 =16\,2^{B-k}-q_k
 \ge5\,2^{B-k}>0.
\]

La combinazione con (5) prova (1). Non è usato alcun conteggio statistico
né un comportamento non dimostrato di un'orbita positiva. □

### 2.3 Primo perimetro: target generali

Per t=1, `log n_(k,1)=k log3+O(1)`. La (1) esclude quindi qualsiasi
trasporto che mandi **ogni** predecessore di n a profondità k in un
predecessore di h(n) alla stessa profondità, con dilatazione
`O((log n)^p)` per un p fissato.

Il quantificatore su ogni predecessore è essenziale: u è un testimone e la
(1) vale per tutti i possibili suoi partner v. Non è però dimostrato che
tutte queste coppie `n_(k,1),h(n_(k,1))` siano nonperiodiche. Questo primo
risultato confuta il trasporto sul dominio di tutti i target unità modulo 3;
da solo non confuta quel trasporto ristretto al dominio esatto di H.

## 3. Una sottoclasse certamente terminante

Il problema di dominio si risolve per una famiglia più alta. Siano

\[
p=k+2,\qquad
t_k=\frac{2^{3^p}+1}{3^{p+1}}.
\tag{7}
\]

Il parametro t_k è un intero positivo. Si può verificarlo senza usare un
teorema esterno: se `A_p=2^(3^p)+1` e `z=2^(3^p)`, allora
`A_(p+1)=(z+1)(z²−z+1)`. Poiché `z≡−1 mod3`, il secondo fattore è
divisibile per 3. Partendo da `A_0=3`, l'induzione dà `3^(p+1)∣A_p`.

Sostituendo (7),

\[
n_k=n_{k,t_k}=\frac{2^{3^p+1}-1}{3},\qquad
3n_k+1=2^{3^p+1}.
\]

Quindi `S(n_k)=1` e `S(h(n_k))=1`. Entrambi i target sono maggiori di 1,
dispari e non divisibili per 3; non hanno ritorni positivi. Le coppie
appartengono al dominio di H senza assumere la congettura di Collatz.

La (1) vale ancora. Questo dimostra una conclusione negativa autentica:

> Anche sul dominio di nonritorno di H, non esiste una dilatazione costante
> universale per un trasporto puntuale di tutti i predecessori che conservi
> la loro profondità.

La scala va però ricalcolata. Qui

\[
\log n_k=9(\log2)3^k+O(1),\qquad
\beta=\frac{\log(33/23)}{\log3}\in(0,1).
\]

Il costo minimo imposto da (1) è quindi dell'ordine di
`(log n_k)^β`. Esclude dilatazioni `o((log n)^β)`, ma **non esclude una
dilatazione O(log n)**, né ogni diversa modalità di confronto dei bacini.

### Perché questo non è un controesempio a H

Il risultato riguarda una sorgente per target e una profondità esatta.
H riguarda il bacino completo, ammette partner a profondità diversa e non
richiede un accoppiamento di ogni sorgente. Nel lemma finito proposto in
precedenza è ammesso anche un errore `E_n(X)=o_n(X)`: eliminare una sorgente
è compatibile con tale errore.

Anche le sorgenti ordinarie `2^e u_(k,t)` sono soltanto `O(log X)` entro X:
aggiungerle non produce una frazione positiva di un bacino. Variare t
produce molti testimoni, ma cambia contemporaneamente il target. Non si
può trasformare questo fatto in una massa positiva di testimoni cattivi
nel bacino di un singolo n fissato.

## 4. Il packing fra fratelli non confuta H

C'è una catena concreta utile per controllare formulazioni troppo forti:

\[
r_0=5,\qquad r_{i+1}=h(r_i),
\]

\[
r_{2j}=\frac{2^{6j+4}-1}{3},\qquad
r_{2j+1}=\frac{2^{6j+8}-1}{3}.
\tag{8}
\]

I primi valori sono `5,85,341,5461,…`. Tutti hanno successore S uguale a 1,
sono nonperiodici e non divisibili per 3. Le formule si provano alternando
`L²` e L, con `L(n)=4n+1`. Scrivendo `a=log8`,

\[
1+\log r_i=ai+O(1).
\tag{9}
\]

I bacini B(r_i) sono disgiunti: dopo il target, l'unico successivo stato
dispari è 1. Se `d_i=d_*(r_i)`, il solo packing dà

\[
\sum_{i<m}d_i\le1\quad\text{per ogni }m.
\tag{10}
\]

H imporrebbe `d_(i+1)≥c d_i/(1+log r_i)`. Iterando, il lower bound è un
prodotto di fattori dell'ordine di `c/(ai)`; i suoi valori sono sommabili.
Non c'è contraddizione con (10).

Nemmeno una versione simmetrica locale viene esclusa automaticamente. La
successione astratta `d_i=2^(−i−1)` ha somma 1 e rapporti consecutivi 1/2.
Soddisfa entrambi i confronti

\[
d_{i+1}\ge\frac{d_i}{1+\log r_i},\qquad
d_i\ge\frac{d_{i+1}}{1+\log r_{i+1}}.
\]

Il primo usa `1+log r_i≥1+log5>2`; il secondo è ancora più debole.
Questi numeri non sono attribuiti ai veri bacini: dimostrano solo che
positività, disgiunzione e le due disuguaglianze sono logicamente compatibili.

### Una versione quasi conservativa è invece impossibile

Supponiamo, lungo la stessa catena e almeno da un indice in poi, che

\[
d_{i+1}\ge\left(1-\frac{C}{1+\log r_i}\right)d_i,
\qquad0\le C\le\log8,
\tag{11}
\]

con un d_i iniziale positivo. Tale positività è disponibile dall'input
analitico esterno per questi target, oppure può essere assunta esplicitamente
come premessa del seguente argomento.

Per i abbastanza grande, il fattore è positivo. La (9) implica

\[
z_i=\frac{C}{1+\log r_i}=\frac{C}{ai}+O(i^{-2}),\qquad
\log(1-z_i)=-\frac{C}{ai}+O(i^{-2}).
\]

La seconda espansione è rigorosa scegliendo un indice oltre il quale
`0≤z_i≤1/2`; l'errore di `log(1−z)+z` è limitato da una costante per z².
Poiché la serie degli errori converge, il prodotto dei fattori fra un
indice fisso e m è limitato inferiormente da `K m^(−C/a)`, con K>0.
La (11) forza quindi `d_m≥K' m^(−C/a)`, con K'>0. Per `C/a≤1` la somma
diverge, in contraddizione con (10).

Questo confuta **(11)**, anche sulla famiglia terminante (8). Non confuta H:
H richiede una frazione residua dell'ordine di `1/log n`, mentre (11)
richiede una frazione prossima a 1. Sostituire l'una con l'altra cambierebbe
radicalmente il problema.

## 5. Una decomposizione dei bacini non dà automaticamente una legge di massa

Se n non ha ritorni positivi, il suo bacino ordinario si decompone in
`{2^e n:e≥0}` e nei bacini dei predecessori dispari immediati u con `S(u)=n`.
Sono parti disgiunte. Il primo insieme ha densità zero, ma la famiglia degli
altri è infinita. Non è lecito concludere senza ulteriori ipotesi che la
densità del bacino sia la somma delle densità dei rami.

L'ostacolo sussiste persino per densità ordinarie esistenti e positive.
Per i≥0, poniamo

\[
C_i=\{m\ge1:m\equiv2^i-1\pmod{2^{(i+1)^2}}\},\qquad
q_i=2^{-(i+1)^2}.
\]

I C_i sono disgiunti, perché nei loro bit bassi la prima cifra zero ha
posizione i. Ciascuno ha densità q_i. Inoltre
`⋃_(i≥K) C_i⊆{m:2^K∣m+1}`, quindi la coda ha densità superiore al più
`2^(−K)`. Ne segue che l'unione dei C_i ha densità `Σq_i<1`.
Il complemento R è infinito; enumeriamolo come `s_0,s_1,…` e poniamo
`D_i=C_i∪{s_i}`. I D_i partizionano tutti i positivi e ciascuno ha ancora
densità q_i>0, ma

\[
1=d\left(\bigcup_iD_i\right)>\sum_i d(D_i)=\sum_iq_i.
\]

Sono insiemi aritmetici, non bacini Collatz. L'esempio confuta l'inferenza
di additività numerabile delle densità; non confuta H. Un approccio che
tratti i bacini come una misura di probabilità sui rami deve prima controllare
la massa che fugge verso indici sempre più grandi con il cutoff X.

## 6. Appendice: positività e terminazione astratte non forzano H

È possibile realizzare rapporti che violano H in una dinamica deterministica
artificiale, con tutti gli iterati strettamente decrescenti prima di 1 e con
bacino di densità inferiore positiva per **ogni** target. La costruzione serve
a delimitare ciò che si può dedurre dal solo nucleo combinatorio; non è una
variante della mappa Syracuse e non è un controesempio a H per Collatz.

Usiamo i r_i della (8), il loro insieme P e i C_i della sezione precedente.
P ha densità zero, perché r_i cresce esponenzialmente. Definiamo

\[
A_i=\{r_i\}\cup\{m\in C_i:m>r_i,\ m\notin P\}.
\]

Gli A_i sono disgiunti, hanno minimo r_i e densità `q_i=2^(−(i+1)²)`.
La loro unione ha densità `Σq_i`: per ogni K la coda è contenuta in
`⋃_(i≥K)C_i∪P`, di densità superiore al più `2^(−K)`. Il complemento A_*
ha quindi densità `q_*=1−Σq_i>0` e minimo 1. Ad esempio `Σq_i≤13/16<1`,
confrontando con `Σ2^(−i−1)=1` e usando il miglioramento stretto al termine i=1.

Ordiniamo `A_i={a_(i,1)=r_i<a_(i,2)<…}`. Per j≥2 poniamo
`F(a_(i,j))=a_(i,floor(j/2))`, e poniamo `F(r_i)=1`. Facciamo lo stesso
con l'enumerazione crescente di A_*, radicata in 1, e definiamo `F(1)=1`.
Ogni intero positivo appartiene a una sola di queste componenti. Tutte le
frecce diverse da `1→1` diminuiscono, quindi ogni orbita raggiunge 1.

I bacini dei r_i sono esattamente A_i. In particolare,

\[
F(r_i)=F(h(r_i))=1,\qquad
\frac{d_F(h(r_i))}{d_F(r_i)}
 =\frac{q_{i+1}}{q_i}=2^{-(2i+3)}.
\]

Poiché `1+log r_i=O(i+1)`, il rapporto richiesto da H tende a zero e nessuna
costante c>0 funziona per F su queste coppie.

La positività non è limitata alle radici. Per un indice j nell'heap binario,
gli indici discendenti contengono gli intervalli
`[j2^r,(j+1)2^r)` per tutti r≥0. Fra i primi N indici, scegliendo il più
grande blocco interamente contenuto, il loro numero è almeno
`N/(2(j+1))+O(1)`. Se la componente ha densità q>0, il bacino del suo
j-esimo elemento ha quindi densità inferiore almeno `q/(2(j+1))>0`.
Questo vale per tutte le componenti, compreso A_*; il bacino di 1 è l'intero
insieme dei positivi. Non restano sorgenti con il solo bacino singleton.

Il modello conserva la crescita superiore elementare, la terminazione,
la positività dei bacini, il packing e l'identità di successore **sulle
coppie r_i,h(r_i)**. Non conserva la formula `3n+1`, la conversione fra
dinamica ordinaria e accelerata, né la legge di lift su tutti i target.
Non dimostra che H sia falsa assumendo Collatz: dimostra che una prova
basata soltanto su quelle proprietà astratte deve usare informazione
aritmetica ulteriore.

## 7. Criterio per proseguire

Il cambio nonnegativo del solo ultimo esponente perde asintoticamente
quasi tutte le sorgenti entro qualsiasi dilatazione finita, a target
fissato. Il cambio firmato ha lo stesso difetto almeno sul sottobacino
esplicito B(11) per la coppia 17/277. È inoltre escluso il trasporto puntuale
universale con profondità conservata e dilatazione costante. È infine
ingiustificata la sostituzione delle densità con una misura numerabilmente
additiva senza un controllo delle code. Nessuno di questi risultati esclude
un trasporto che modifichi più esponenti, cambi profondità o sia valido per
una frazione sufficiente delle sorgenti di ciascun bacino.

Il prossimo lemma dovrebbe quindi dichiarare quali sorgenti può scartare,
quanto cambia la profondità, quale molteplicità produce e come controlla
uniformemente la loro altezza. Deve produrre un confronto di massa relativo
per un target fissato. Ampliare il censimento, variare il target insieme
alla sorgente o scegliere una nuova costante da rapporti finiti non sostituisce
tale lemma. H rimane aperta; gli ostacoli chiudono metodi più forti, non
autorizzano né ad abbandonarla come confutata né a considerarla confermata.
