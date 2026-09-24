# Il primo passo diverso non basta: applicazione di Chim (2025)

24 settembre 2026. Nota complementare ai [certificati modulari](RESULTS_IT.md).

**Conclusione.** Per ogni v≥5, si confrontino le orbite di Q_v e Q_{v+1}
fino al loro primo esponente Syracuse diverso. Dopo quel passo entrambi
gli endpoint sono ancora sopra le rispettive sorgenti N_v e N_{v+1}.
La prova usa un risultato esterno di Chim per v≥37 e 32 confronti
modulari finiti per 5≤v≤36. Non controlla i passi successivi.

È una deduzione specifica del presente studio, non un enunciato attribuito
all'articolo di Chim. Originalità non accertata; dimostrazione informale e
parte finita computazionale, senza formalizzazione Lean o peer review esterna.

## 1. La relazione esatta al punto di separazione

Come nello [studio precedente](../post_v6_levels_2026-09-24/RESULTS_IT.md),
Q_j=(9^{2^j}−1)/2^{j+3} e N_j=(2^{3·2^j−5}−11)/3.
Il prefisso comune massimo di Q_v e Q_{v+1} ha lunghezza k, somma A≤v+1
e costante affine C≥0:

\[
 S^k(Q_j)=\frac{3^kQ_j+C}{2^A},\qquad j=v,v+1.
\]

Poniamo P=3^{k+1}, B=3C+2^A, p=v+2−A e X=Q_v. La ricorrenza
Q_{v+1}=X+2^{v+2}X² dà, dopo aver rimosso 2^p dai due numeratori,

\[
 U=\frac{PX+B}{2^{v+2}},\qquad U+F,\qquad F=PX^2.
\]

U è intero e F è dispari. Uno dei due numeri è dispari, l'altro ha
valutazione r≥1. Per i due endpoint x'=S^{k+1}(Q_v), y'=S^{k+1}(Q_{v+1}):

\[
 \begin{cases}
 x'=U,\quad y'=(U+F)/2^r,&U\text{ dispari},\\
 x'=U/2^r,\quad y'=U+F,&U\text{ pari}.
 \end{cases}
\]

Quindi 2^r y'−x'=F oppure y'−2^r x'=F. Questo è un accoppiamento
esatto con un termine quadratico positivo; non è una contrazione.
Il solo prefisso comune non controlla r.

Per studiare entrambe le valutazioni, scriviamo il numeratore del passo
successivo anche nella forma

\[
 3S^k(Q_j)+1
 =\frac{3^{E_j}+c_j}{2^{j+3+A}},\qquad
 E_j=2^{j+1}+k+1,\quad c_j=2^{j+3}B-P.
\]

c_j è un intero positivo dispari. Per k≥1, C≥3^{k−1}, quindi
2^{j+3}B>P; per k=0 si verifica direttamente. Inoltre

\[
 C\le2^A(3^k-1)/2,\quad
 B<2^{A-1}3^{k+1},\quad
 c_j<2^{2v+4}3^{v+2}=12^{v+2},\quad E_j+1\le2^{v+3}.
\]

Abbiamo usato k≤A≤v+1 e j≤v+1. Se a_j è l'esponente di questo passo,
il totale delle divisioni effettuate dal principio è esattamente

\[
 \boxed{D_j=A+a_j=\nu_2(3^{E_j}+c_j)-j-3.}
\]

## 2. L'input quantitativo esterno e la coda infinita

Il [Teorema 2.1 di Chim, pp. 298–299](https://tugraz.elsevierpure.com/ws/portalfiles/portal/92346766/1-s2.0-S0022314X24001793-main.pdf)
si applica a 3^E−(−c) con p=2, D=e=f=g=1, esponenti E,1,
log A₁=ln3 e log A₂=h=max(ln c,ln2), quando c non è una potenza di 3.
Le basi sono unità 2-adiche moltiplicativamente indipendenti. Specializzando
le costanti C=4250, Z₁=4 si ottiene

\[
 \nu_2(3^E+c)<180000\,h\max\{\ln(E+1),800\}.
\]

L'arrotondamento segue da 0,69<ln2<0,70 e ln3<1,10:
il coefficiente è 8500(2ln2+4,85)ln3/(ln2)³<180000; le due soglie
costanti sono <800. Il termine variabile è
ln(E/h+1/ln3)+ln ln2≤ln(E+1). Se c=3^b, incluso b=0,
si usa invece direttamente ν₂(3^E+3^b)≤2.
Questa applicazione di un teorema esterno non è verificata dal programma.

Con i limiti specifici della sezione 1, ln12<2,5 e
max{ln(E_j+1),800}≤v+803 danno, in entrambi i casi,

\[
 \nu_2(3^{E_j}+c_j)<R(v),\qquad
 R(v)=450000(v+2)(v+803).
\]

Per ogni v≥37 vale R(v)<2^v/6. La base è il confronto intero

\[
 6R(37)=88\,452\,000\,000
 <137\,438\,953\,472=2^{37}.
\]

L'induzione segue da
2(v+2)(v+803)−(v+3)(v+804)=v²+803v+800>0, dunque R(v+1)<2R(v).

Resta da confrontare la valutazione con l'altezza reale. Dalle definizioni
e da (9/8)^6>2 segue

\[
 \log_2(Q_j/N_j)>2^j/6-j+2+\log_2 3.
\]

Infatti Q_j/N_j>3·2^{2−j}(9/8)^{2^j}; qui log₂ è il logaritmo reale.
Usando D_j<R(v)−j−3 e j≥v:

\[
 \log_2(Q_j/N_j)-D_j
 >5+\log_2 3+(2^j-2^v)/6>0.
\]

Il termine affine dell'orbita è non negativo, perciò
S^{k+1}(Q_j)≥Q_j/2^{D_j}>N_j. Questo prova la conclusione per tutti
i v≥37 e per entrambi i rami, anche quello con la valutazione maggiore. □

## 3. I 32 casi finiti e la portata della conclusione

Per ciascun v=5,…,36 il programma calcola Q_v e Q_{v+1} modulo 2^256
in due modi: esponenziazione modulare e ricorrenza quadratica. Ricostruisce
il prefisso comune e determina **esattamente entrambi** gli esponenti
divergenti; se la precisione non bastasse, il controllo fallirebbe.

Per j=v,v+1 e D_j così ottenuto verifica il confronto intero

\[
 3^{k+2}>2^{\delta_j},\qquad
 \delta_j=j+D_j-\lfloor2^j/6\rfloor-2,
\]

automatico quando δ_j≤0. Dal limite inferiore della sezione 2 segue
S^{k+1}(Q_j)/N_j>3^{k+2}/2^{δ_j}>1. Sono verificati tutti i 64 rami;
il programma evita di costruire le potenze gigantesche quando δ_j<0.
I test confrontano inoltre i casi v=5,…,9 con gli interi completi.

I [dati finiti](separation_results.json) comprendono parole comuni,
esponenti, somme e confronti; il [programma](separation_probe.py) verifica
anche la base v=37 e gli arrotondamenti razionali delle costanti.
Questi controlli non dimostrano il teorema di Chim o la sua applicazione
infinita: quella dipendenza rimane esplicita nella prova sopra.

Combinando parte finita e coda infinita, il primo passo distinto non
raggiunge la sorgente per nessun v≥5. Il risultato precedente riguardava
solo i passi comuni; questo aggiunge il primo passo oltre la separazione.
Non dimostra che una discesa successiva esista e non fornisce una stima
uniforme per l'intera orbita.

## 4. Una possibile induzione ancora da chiudere

Le sorgenti soddisfano una ricorrenza utile al confronto:

\[
 N_{v+1}=96N_v^2+704N_v+1287.
\]

Anche una relazione y=αx²+βx+γ fra due endpoint resta quadratica dopo
passi Syracuse di esponenti effettivi a,b:

\[
 \alpha'=\alpha 2^{2a-b}/3,\qquad
 \beta'=2^{a-b}(\beta-2\alpha/3),\qquad
 \gamma'=2^{-b}(\alpha/3-\beta+3\gamma+1).
\]

I coefficienti iniziali sono (2^{v+2},1,0) e α rimane positivo.
A tempi eventualmente diversi k,ℓ, con somme degli esponenti A_k,B_ℓ,
il coefficiente principale è

\[
 \alpha=2^{v+2+2A_k-B_\ell}3^{\ell-2k}.
\]

Se x=S^k(Q_v) è già in (0,N_v), y=S^ℓ(Q_{v+1})=f(x), ed entrambi
f(0) e f(N_v) sono ≤N_{v+1}, la convessità stretta di f dà y<N_{v+1}.
La condizione più forte α≤96, β≤704, γ≤1287 è sufficiente.

È un criterio algebrico per un'eventuale induzione. Non abbiamo dimostrato
che quei limiti sui coefficienti si realizzino a tempi scelti uniformemente;
gli esponenti delle due orbite restano da controllare. Non presentiamo
quindi la relazione quadratica come una prova di discesa fra livelli.

Riferimento esterno: K. C. Chim, *Lower bounds for linear forms in two
p-adic logarithms*, Journal of Number Theory 266 (2025), 295–349,
[DOI](https://doi.org/10.1016/j.jnt.2024.07.012), online dal 21 agosto 2024.
