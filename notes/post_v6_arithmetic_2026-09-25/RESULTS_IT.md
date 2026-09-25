# Blocchi sfavorevoli: traduzione aritmetica e limite della stima scelta

25 settembre 2026. Continuazione dello [studio di compensazione](../post_v6_compensation_2026-09-25/RESULTS_IT.md).

**Esito.** Abbiamo una condizione aritmetica necessaria e sufficiente per
una parola completa della torre, conservando il prefisso che precede un
blocco sfavorevole. Per questa rappresentazione, la specializzazione
esplicita del teorema di Chim già adottata nel progetto dà sempre un limite
troppo grande per escludere il blocco. La dimostrazione di questo limite
è generale; i controlli sui livelli 22–24 sono soltanto verifiche finite
delle formule. Una rappresentazione con costante di segno variabile lascia
aperta la possibilità di cancellazioni. Non abbiamo dimostrato la
compensazione uniforme né aggiunto dichiarazioni Lean. Originalità non
accertata; revisione interna, senza referee umano esterno.

## 1. Il problema preciso

Usiamo la mappa con un solo dimezzamento per passo:

\[
 T(x)=\begin{cases}x/2,&x\equiv0\pmod2,\\(3x+1)/2,&x\equiv1\pmod2.\end{cases}
\]

Per \(v\ge15\), siano

\[
 Q_v=\frac{9^{2^v}-1}{2^{v+3}},\quad
 H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,\quad D_v=128v^2.
\]

Se \(J_v(r)\) conta i passi dispari nei primi \(r\) passi di \(T\),
poniamo \(F_v(r)=305r-589J_v(r)\). Cambiamo qui il nome della funzione
di credito rispetto alla nota precedente per riservare \(C\) alla costante
affine. La candidata congelata afferma

\[
 \max_{0\le r\le r+b\le H_v}\bigl(F_v(r)-F_v(r+b)\bigr)\le D_v.
 \tag{1}
\]

Un blocco di lunghezza \(b\) con \(j\) dispari ha perdita
\(589j-305b\). (1) implica il criterio sufficiente di discesa già
documentato nello studio precedente. Qui cerchiamo di escludere
aritmeticamente i blocchi con perdita superiore a \(D_v\).

## 2. La parola intera conserva l'informazione del prefisso

Per una parola binaria cronologica \(\omega\), di lunghezza \(n\), con
\(p\) uno nelle posizioni \(i_0<\cdots<i_{p-1}\), definiamo

\[
 C_\omega=\sum_{h=0}^{p-1}2^{i_h}3^{p-1-h}.
\]

Il cilindro esatto di parità e la mappa affine associata sono

\[
 x\equiv-3^{-p}C_\omega\pmod{2^n},\qquad
 T^n(x)=\frac{3^px+C_\omega}{2^n}.
 \tag{2}
\]

L'integralità dell'endpoint prescritto è sufficiente per l'intera parola:
riducendo il numeratore modulo 2 si ottiene la prima parità; rimosso il
primo passo, si ripete il ragionamento per induzione. Non è un controllo
che trascura la validità dei passi intermedi. Queste sono identità
classiche dei cilindri, non risultati di originalità rivendicata.

Scriviamo \(\omega=\alpha\beta\): il prefisso \(\alpha\) ha lunghezza
\(r\), \(k\) dispari e costante \(A\); il blocco \(\beta\) ha lunghezza
\(b\), \(j\) dispari e costante \(B\). Allora

\[
 n=r+b,\qquad p=k+j,\qquad C=3^jA+2^rB.
\]

Sostituendo \(Q_v\) in (2) si ottiene l'equivalenza esatta

\[
 \boxed{\omega\text{ è il prefisso di parità di }Q_v
 \quad\Longleftrightarrow\quad 2^L\mid3^E+c},
 \tag{3}
\]

\[
 L=v+3+r+b,\qquad E=2^{v+1}+k+j,\qquad
 c=2^{v+3}(3^jA+2^rB)-3^{k+j}.
\]

La condizione riguarda l'intera parola: applicare una congruenza al solo
blocco \(\beta\) come se iniziasse da \(Q_v\) perderebbe il prefisso.
Per \(p\ge1\), gli estremi classici della costante sono

\[
 3^p-2^p\le C\le2^{n-p}(3^p-2^p).
 \tag{4}
\]

Seguono spostando gli uno rispettivamente tutti a sinistra o tutti a
destra: \(h\le i_h\le n-p+h\). Sono anche contenuti nel Teorema 2.4 di
[Rozier–Terracol, v5](https://arxiv.org/html/2502.00948v5).
Per \(v\ge5\), \(c>1\) è dispari e non divisibile per 3: l'ultimo
termine di \(C\) è l'unico non nullo modulo 3. Pertanto \(3\) e \(-c\)
sono moltiplicativamente indipendenti, e

\[
 \ln c<(v+3+n-p)\ln2+p\ln3.
\]

## 3. Perché la specializzazione esplicita di Chim non esclude questi blocchi

La [specializzazione già verificata nel progetto](../post_v6_certificates_2026-09-24/CHIM_OBSTRUCTION_IT.md)
del [Teorema 2.1 di Chim](https://doi.org/10.1016/j.jnt.2024.07.012) è

\[
 \nu_2(3^E+c)<R(E,c),\quad
 R(E,c)=180000h\max\{\ln(E+1),800\},\quad h=\max\{\ln c,\ln2\}.
 \tag{5}
\]

L'applicazione è lecita per la costante positiva in (3). Il problema è
quantitativo, anche usando la sua altezza esatta invece di maggiorarla.

**Proposizione.** Se \(589j-305b>0\), allora, per la rappresentazione (3),
\(R(E,c)>36\,000\,000L\). In particolare (5) non contraddice la
divisibilità richiesta da (3).

**Dimostrazione.** La perdita positiva implica \(b<2j\), dunque
\(j\ge1\). L'ultimo uno della parola è in posizione almeno \(r+j-1\),
quindi \(C\ge2^{r+j-1}\). Il primo termine della somma dà
\(3^p\le3C\). Pertanto

\[
 c\ge(2^{v+3}-3)C\ge2^{v+2}2^{r+j-1}=2^s,
 \qquad s=v+r+j+1.
\]

Poiché \(b\le2j-1\), si ha \(L\le2s\). Da \(\ln2>1/2\) segue
\(h\ge s\ln2>L/4\). Sostituendo nella definizione di \(R\):

\[
 R(E,c)>180000(L/4)800=36\,000\,000L.\qquad\square
\]

Questa proposizione limita **la specifica stima (5) e la rappresentazione
(3)**. Non dimostra l'impossibilità di ogni applicazione del teorema
originale con altri parametri, di ogni stima di logaritmi 2-adici, o di ogni
rappresentazione alternativa. Non è un controesempio a (1).
Anche l'esempio generico \(E=1,c=2^M-3\), \(M\ge3\), dà valutazione \(M\) con
\(\ln c\asymp M\); ricorda perché l'altezza non può sparire da una
stima valida per costanti arbitrarie. Non è un esempio raggiunto dalla torre.

## 4. Una rappresentazione che lascia aperte le cancellazioni

Sia \(a_\beta\) il rappresentante in \([0,2^b)\) del cilindro del blocco:
\(a_\beta\equiv-3^{-j}B\pmod{2^b}\). Un'altra forma di (3) è

\[
 2^L\mid3^{E_s}+c_s,\quad E_s=2^{v+1}+k,\quad
 c_s=2^{v+3}(A-2^ra_\beta)-3^k.
 \tag{6}
\]

La costante è dispari ma può essere negativa. Sostituendo
\(a_\beta\) con \(a_\beta+t2^b\), si cambia \(c_s\) di un multiplo
di \(2^L\). Possiamo scegliere la costante \(c_*\) con minimo valore
assoluto nella classe, centrata fra \(-2^{L-1}\) e \(2^{L-1}\).
Questo è un minimo fra tali rappresentanti, non fra tutte le possibili
riformulazioni aritmetiche.

Non abbiamo dimostrato per \(c_*\) un limite inferiore uniforme analogo
a quello della sezione 3. Se una costante alternativa ha valore assoluto
pari a una potenza di 3, viene meno l'indipendenza delle basi e occorre
usare direttamente la formula di valutazione, non (5).

Due casi strutturati meritano di essere conservati:

- Per \(b\) passi tutti dispari si può scegliere \(a_\beta=-1\), dando
  \(c_s=2^{v+3}(A+2^r)-3^k\), indipendente da \(b\). L'altezza dipende
  ancora dal prefisso, che può avere lunghezza dell'ordine di \(2^v\).
- Per una parola \(w\) di lunghezza \(d\ge1\), \(s\ge1\) dispari e
  costante \(B_w\), il punto fisso 2-adico è
  \(z_w=B_w/(2^d-3^s)\). Seguire \(w^t\) equivale a
  \(x\equiv z_w\pmod{2^{dt}}\). Il denominatore è dispari: il costo
  aritmetico della descrizione può dipendere dal periodo invece che da
  tutte le ripetizioni. Questo tratta parole strutturate, non tutti i
  blocchi di perdita positiva.

L'inversione 2-adica della torre rende altrettanto esplicito il problema.
La mappa

\[
 \mathcal F_v(q)=\frac{\exp(2^vq\log9)-1}{2^{v+3}}
\]

è una biezione isometrica di \(\mathbb Z_2\), con inversa
\(\mathcal G_v(z)=\log(1+2^{v+3}z)/(2^v\log9)\).
Infatti \(\nu_2(\log9)=3\) e
\(\nu_2(\exp u-\exp w)=\nu_2(u-w)\) per \(u,w\in4\mathbb Z_2\);
la normalizzazione rimuove esattamente \(v+3\) fattori di 2.
L'inversa scritta sopra appartiene a \(\mathbb Z_2\) per ogni
\(z\in\mathbb Z_2\), mostrando anche la suriettività. Posto
\(z_\beta=(2^ra_\beta-A)/3^k\), la parola è raggiunta da \(Q_v\)
esattamente quando

\[
 \mathcal G_v(z_\beta)\equiv1\pmod{2^{r+b}}.
\]

È una riformulazione coerente con la biezione finita già presente nel
progetto. Ogni cilindro corrisponde a una classe di parametri: il problema
è distinguere il parametro fissato \(q=1\), non mostrare che esiste un
parametro che realizza il cilindro.

## 5. La pista della complessità: il ponte mancante è sostanziale

La [rassegna mirata](LITERATURE_IT.md) include il preprint di Bugeaud del
24 agosto 2026 sulle rappresentazioni binarie delle potenze di 3. La
pertinenza alla torre è l'identità
\(3^{2^{v+1}}=1+2^{v+3}Q_v\). Tuttavia, i bit ordinari dell'intero e
le parità successive della sua orbita sono oggetti distinti. Non abbiamo
un'implicazione che trasformi la violazione di (1) nelle ipotesi digitali
del preprint.

Anzi, la sola densità di dispari non impone bassa complessità alla parola
di parità. Una costruzione esplicita lo dimostra. Usiamo il codice

\[
 \phi(0)=11010,\qquad\phi(1)=10110.
\]

Sia \(U_t\) la concatenazione in ordine lessicografico di tutte le parole
binarie di lunghezza \(t\); sia \(W_t=\phi(U_t)\). Allora

\[
 b=5t2^t,\quad j=3t2^t,\quad 589j-305b=242t2^t.
\]

La parola non contiene `111`, neppure ai confini dei codici. I fattori
allineati di lunghezza \(5t\) includono le \(2^t\) immagini distinte,
quindi \(p_{W_t}(5t)\ge2^t\): nessuna costante universale può limitare
la complessità con \(K\ell\) per tutte queste parole e tutte le lunghezze.
Per \(v=2t\), \(t\ge8\), inoltre

\[
 b\le2^{2t-1}<H_{2t},\qquad 242t2^t>128(2t)^2.
\]

Il primo confronto segue da \(10t\le2^t\), il secondo da
\(242\,2^t>512t\); entrambi si verificano a \(t=8\) e persistono
per induzione. Dunque esistono parole che superano la capacità proposta,
senza lunghe sequenze di dispari e con complessità elevata. Sono cilindri
ammissibili per interi positivi; essendo il primo bit 1, anche la biezione
della torre generalizzata le realizza per opportuni parametri dispari.
**Non sono per questo parole del parametro fissato \(q=1\).**
Il calcolo per \(t=8,10\) verifica espressamente che non sono i prefissi
di \(Q_{16},Q_{20}\). Nessun controesempio alla candidata è stato trovato.

## 6. Controlli esatti e riproducibilità

[arithmetic_probe.py](arithmetic_probe.py) ricostruisce le parole dei
livelli 22–24 con il motore congelato precedente, ne confronta gli hash,
estrae i blocchi di massima perdita già registrati e verifica (3), (4),
(6), la versione centrata e tutti i confronti interi della sezione 3.
Gli estremi non sono scelti nuovamente. I risultati completi sono in
[arithmetic_results.json](arithmetic_results.json).

| v | prefisso r | blocco b | dispari j | perdita | L | bit di c | bit di \(\lvert c_*\rvert\) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 22 | 2 354 901 | 7 872 | 4 163 | 51 047 | 2 362 798 | 2 362 803 | 2 362 796 |
| 23 | 7 081 505 | 3 382 | 1 831 | 46 949 | 7 084 913 | 7 084 920 | 7 084 912 |
| 24 | 9 716 549 | 4 954 | 2 653 | 51 647 | 9 721 530 | 9 721 537 | 9 721 529 |

Il numero di bit è \(\lfloor\log_2|c|\rfloor+1\), non l'altezza
logaritmica naturale \(h\). In questi tre esempi neppure la centratura
rende la costante piccola; questo dato finito non dà un limite uniforme.
Le parole complete erano già state verificate indipendentemente in C/GMP
nello studio precedente. Qui i nuovi controlli aritmetici sono in Python,
con test separati contro l'iterazione elementare; il replay CI usa lo
stesso nuovo programma, non una seconda implementazione della sua algebra.

Dal repository:

```sh
python3 notes/post_v6_arithmetic_2026-09-25/test_arithmetic.py
python3 notes/post_v6_arithmetic_2026-09-25/arithmetic_probe.py --output /tmp/arithmetic_results.json
cmp notes/post_v6_arithmetic_2026-09-25/arithmetic_results.json /tmp/arithmetic_results.json
```

Nessun test finito verifica il teorema esterno di Chim o la prova generale
della sezione 3. Nessun file del protocollo precedente viene modificato.

## 7. Decisione di ricerca

Non investire altri calcoli nel tentativo di ricavare (1) dalla sola
stima (5) applicata a (3): la sezione 3 ne quantifica l'insufficienza.
La via ancora sensata è cercare un vincolo specifico del parametro
\(q=1\) che consenta cancellazioni controllate in (6), oppure una
decomposizione in blocchi strutturati con costo aritmetico dimostrabilmente
limitato. La costruzione della sezione 5 impone di usare l'aritmetica della
torre: densità e assenza di lunghe sequenze dispari, da sole, non bastano.

Abbiamo preparato [una nota tecnica per revisione specialistica](EXPERT_REVIEW.md),
con il quesito aperto e i limiti dei metodi tentati. Non è stata inviata
a ricercatori. La priorità è verificare quel passaggio aritmetico prima
di presentare nuove congetture come progressi verso una prova uniforme.
