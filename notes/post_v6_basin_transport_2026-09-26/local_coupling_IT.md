# Accoppiamenti degli alberi inversi: un'ostruzione esatta alla profondità comune

26 settembre 2026. Piero Borgatta, con assistenza Codex.

**Esito.** Cambiare soltanto gli esponenti delle parole, mantenendone la
lunghezza, non permette un trasporto punto per punto con dilatazione
d'altezza universale. La prova seguente riguarda **tutte** le parole
superiori della lunghezza prescritta, non soltanto un algoritmo greedy.
Non confuta H: non confronta masse asintotiche e non esclude di cambiare
profondità o di scartare un insieme di sorgenti di densità zero.

Questa nota contiene una dimostrazione matematica e controlli Python
esatti; non dichiara una formalizzazione Lean del nuovo teorema.

## 1. Un accoppiamento locale effettivo, con parole diverse

Per un target dispari non divisibile per 3, i figli inversi sono

\[
I_a(n)=\frac{2^a n-1}{3},\qquad a\ge1.
\]

Il figlio è intero, dispari e ancora non divisibile per 3 esattamente
quando \(2^a n\equiv4\) oppure \(7\pmod9\). Gli esponenti continuabili
sono dunque due classi modulo 6:

| n mod 9 | esponenti in {1,…,6} | h(n) mod 9 | esponenti superiori | differenze per rango |
|---:|:---:|---:|:---:|:---:|
| 1 | 2, 4 | 5 | 3, 5 | +1, +1 |
| 2 | 1, 3 | 1 | 2, 4 | +1, +1 |
| 4 | 2, 6 | 8 | 1, 5 | −1, −1 |
| 5 | 3, 5 | 4 | 2, 6 | −1, +1 |
| 7 | 4, 6 | 2 | 1, 3 | −3, −3 |
| 8 | 1, 5 | 7 | 4, 6 | +3, +1 |

Scrivendo gli esponenti come \(e_j+6r\), \(j\in\{0,1\}\),
\(r\ge0\), si manda il figlio di rango \((r,j)\) del primo target in
quello dello stesso rango del secondo. È una biezione dei figli
continuabili, iterabile su parole diverse. Dopo il primo passo i due
target non sono in generale legati da h: si ricalcolano entrambe le
classi modulo 9. Tra due classi qualsiasi la differenza per passo è
compresa fra −5 e +5. Questo controllo locale non limita la somma
delle differenze lungo una parola.

L'enumerazione modulo 27 nel JSON registra tutti i 36 casi del primo
passo: 18 classi del target per due ranghi. Non è un censimento di
sorgenti e non produce una stima di densità.

## 2. Il ciclo del quoziente non è una prova di realizzabilità

Se si conservano soltanto le due classi modulo 9 e si permettono
sollevamenti indipendenti modulo 27, compaiono sei autoanelli di costo
positivo \(b-a\). **Nessuno dei sei sollevamenti è compatibile con
\(y=h(n)\pmod{27}\) al primo passo.** Per esempio lo stato (8,7)
ammette nel quoziente l'autoanello \((a,b)=(1,4)\), ma richiede
\((n,y)\equiv(26,25)\pmod{27}\), mentre
\(h(26)\equiv16\pmod{27}\).

Questi autoanelli escludono un potenziale con costo nullo valido su
tutto quel quoziente sovrabbondante. Da soli non provano alcuna
ostruzione per gli alberi effettivi dei fratelli. La dimostrazione
seguente conserva invece esattamente la relazione h.

## 3. Teorema: ogni parola superiore della stessa profondità paga

Siano \(k\ge0\), \(t\ge1\), e poniamo

\[
n=2t3^{k+2}-1,\qquad y=h(n)=16n+5,
\qquad u=18t2^k-1.
\]

Le k inversioni inferiori con esponente 1 sono intere e positive:

\[
u_i=2^{i+1}t3^{k+2-i}-1\quad(0\le i\le k),
\qquad u_0=n,\ u_k=u.
\]

**Teorema.** Sia \(b_1,\ldots,b_k\) una qualsiasi parola di
esponenti positivi che, partendo da y e applicando le inversioni in
quest'ordine, produce interi dispari positivi
\(v_0=y,v_1,\ldots,v_k=v\). Allora

\[
\boxed{\quad 23^k v>16\,33^k u,\qquad
\frac vu>16\left(\frac{33}{23}\right)^k.\quad}       \tag{1}
\]

Non si impone al figlio finale di essere continuabile. Per i passi
intermedi la non divisibilità per 3 è già necessaria all'integralità
del passo successivo.

### Dimostrazione

Scriviamo \(B_i=b_1+\cdots+b_i\), \(B_0=0\). Trasportiamo
la **stessa parola superiore** sul target negativo −11 e definiamo

\[
q_0=11,\qquad q_i=\frac{2^{b_i}q_{i-1}+1}{3}.
\]

All'inizio \(y=32t3^{k+2}-11\). Per induzione sulle identità
affini delle inversioni,

\[
v_i=32t3^{k+2-i}2^{B_i}-q_i.                         \tag{2}
\]

Poiché \(i\le k\), il primo termine a destra è un intero pari.
Quindi q_i è intero e dispari, e la sua ricorrenza mostra che è positivo.
Non si è assunta la realizzabilità indipendente di una parola negativa:
l'integralità deriva dalla parola positiva effettiva e da (2).

Introduciamo la mappa ausiliaria sui dispari positivi

\[
U(q)=\operatorname{oddpart}(3q-1).
\]

La ricorrenza dà \(3q_i-1=2^{b_i}q_{i-1}\), con q_{i−1}
dispari; dunque \(U(q_i)=q_{i-1}\) e \(U^i(q_i)=11\).
Il seguente insieme finito è chiuso sotto U e non contiene 11:

\[
E=\{1,3,5,7,9,13,19\},
\]

\[
1\mapsto1,\quad3\mapsto1,\quad5\mapsto7,\quad7\mapsto5,
\quad9\mapsto13,\quad13\mapsto19,\quad19\mapsto7.
\]

Nessun q_i appartiene a E. Essendo dispari positivo, soddisfa quindi
\(q_i\ge11\). In particolare \(2^{b_i}q_{i-1}\ge22\), da cui

\[
q_i=\frac{2^{b_i}q_{i-1}+1}{3}
\le\frac{23}{66}\,2^{b_i}q_{i-1}.
\]

Iterando e usando \(q_k\ge11=q_0\), otteniamo

\[
2^{B_k}\ge\left(\frac{66}{23}\right)^k,
\qquad 2^{B_k-k}\ge\left(\frac{33}{23}\right)^k.     \tag{3}
\]

D'altra parte \((z+1)/3\le z/2\) per \(z\ge2\), quindi
\(q_i\le2^{b_i-1}q_{i-1}\) e
\(q_k\le11\,2^{B_k-k}\). Ponendo \(D=B_k-k\ge0\), (2) dà

\[
v-16\,2^D u
=16\,2^D-q_k\ge5\,2^D>0.
\]

Combinando con (3) si ottiene (1). □

La mappa U è qui soltanto un dispositivo aritmetico ausiliario:
non si assume alcuna congettura sulle orbite negative. Serve esclusivamente
il controllo dei sette valori elencati.

## 4. Quantificatori, dominio di H e limite dell'ostruzione

Per \(t=1\), si ha \(n+1=18\,3^k\), e il limite inferiore è

\[
16\left(\frac{n+1}{18}\right)^\alpha,
\qquad \alpha=\log_3(33/23)>0.
\]

Su **tutti** i target unità, un trasporto che preservi profondità e ogni
sorgente non può dunque avere dilatazione \(O((1+\log n)^p)\), per
alcun p fissato. Non è però dimostrata qui l'assenza di ritorni positivi
per tutta la famiglia t=1, richiesta dal dominio di H.

Si può comunque escludere una dilatazione **universale costante** anche
entro il dominio di H, tramite una sottofamiglia certificata terminante.
Posti \(p=k+2\), \(a=3^p+1\), scegliamo

\[
t=\frac{2^{3^p}+1}{3^{p+1}},\qquad
n=\frac{2^a-1}{3}=2t3^p-1.
\]

L'integralità di t segue da
\(2^{3^p}\equiv-1\pmod{3^{p+1}}\): la base è 2≡−1 modulo 3,
e il passo induttivo si ottiene elevando al cubo.
L'esponente a è pari e
\(3n+1=2^a\), \(3h(n)+1=2^{a+4}\). Pertanto
\(S(n)=S(h(n))=1\); entrambi i target sono maggiori di 1 e non
hanno ritorni positivi. La disuguaglianza (1) vale anche per essi.

Per questa sottofamiglia, tuttavia, \(\log n\asymp3^k\): il
limite inferiore è dell'ordine di \((\log n)^\alpha\), con
\(0<\alpha<1\). **Non esclude una dilatazione O(log n) sul dominio
di H.** Non trasferire la conclusione più forte di t=1 a questa
sottofamiglia: i target hanno altezze diverse.

Un secondo limite, indipendente, è decisivo: (1) riguarda sorgenti
specifiche. Una disuguaglianza di densità con errore \(o_n(X)\) può
scartare un numero finito di sorgenti per ogni target n. Qui non si è
dimostrata una massa positiva di sorgenti costose per uno stesso target.
L'ipotesi H resta aperta anche se tutte le disuguaglianze di questa
nota sono vere.

## 5. Una seconda ostruzione: un insieme finito di relazioni affini

Consideriamo stati descritti da un insieme finito di mappe
\(F_s(z)=c_s z+d_s\), con \(c_s>0\). Supponiamo che una regola
di accoppiamento chiuda ogni figlio inverso tramite identità

\[
I_b(F_s(n))=F_r(I_a(n))                               \tag{4}
\]

valide su classi infinite di target, per tutti gli esponenti a
ammissibili, che sono illimitati. Il confronto dei coefficienti di n
in (4) forza

\[
c_r=c_s2^{b-a},\qquad
3d_r=2^b d_s+c_r-1.                                  \tag{5}
\]

Per uno stato iniziale di h si ha d_s=1 oppure 5. La finitezza dei
c_r positivi implica b=a+O(1). Quando a tende all'infinito lungo una
classe ammissibile, il secondo membro di (5) diverge, mentre i d_r
appartengono a un insieme finito. Contraddizione.

Questa è un'ostruzione agli **stati costituiti da relazioni affini
esatte**, con copertura di tutti i figli a profondità uguale. Non è
un teorema d'impossibilità per qualsiasi automa finito, algoritmo che
legga cifre, trasporto non affine o trasporto con profondità variabile.
In particolare un contatore/intercetta non limitato esce da questo
modello.

## 6. Controlli finiti e decisione operativa

Il file `local_coupling_probe.py` verifica con soli interi e frazioni:

- le sei righe modulo 9 e tutte le 36 transizioni iniziali modulo 27;
- i sei autoanelli positivi del quoziente e la loro incompatibilità
  iniziale con h modulo 27;
- un albero binario ristretto ai primi due figli, fino a profondità 14,
  per sei target che coprono le unità modulo 9;
- la chiusura dell'insieme E e le identità (2)–(3) su testimoni reali
  alle profondità 0,1,2,4,8,16,32,64;
- tutte le parole superiori con esponenti in {1,…,6}, lunghezze 1,…,5
  e t=1,2, includendo i figli finali divisibili per 3;
- cinque membri della sottofamiglia terminante, per k=0,…,4.

I conteggi dell'albero finito sono conteggi di **parole**, con
molteplicità; non sono conteggi di interi distinti né masse dei bacini.
Per esempio, già alla profondità 12 dal target 17 il coupling per rango
produce un testimone con endpoint inferiore 31.949 e superiore
9.386.400.192.277, somma delle differenze degli esponenti 24.
Questo esempio illustra il costo; la conclusione uniforme deriva dalla
dimostrazione del paragrafo 3, non dall'estrapolazione del probe.

Comando riproducibile, dalla directory `lean`:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 ../notes/post_v6_basin_transport_2026-09-26/local_coupling_probe.py --output ../notes/post_v6_basin_transport_2026-09-26/local_coupling_results.json
```

Esito osservato: exit 0, tutti i controlli esatti superati. Nessun
censimento di sorgenti è stato ampliato e nessuna densità è stata stimata.

**Candidato circoscritto per Lean:** formalizzare il teorema (1), nella
forma intera \(23^k v>16\,33^k u\), insieme al certificato finito E.
Prima di una nuova campagna di calcolo su H, la ricerca dovrebbe
esplicitare come il trasporto cambia profondità, quale parte dei bacini
conserva e come limita la molteplicità. Sono le possibilità lasciate
aperte da questi risultati, non meccanismi già dimostrati sufficienti.
