# Dopo le torri: libertà dei suffissi finiti e limite della strategia locale

24 settembre 2026. Continuazione del risultato sui predecessori, commit
`f198185`. **Stato iniziale: aritmetica del parametro compilata; collegamento
alle orbite e audit in verifica.**

La ricerca richiesta era un vincolo tra episodi consecutivi che obbligasse
una compensazione della crescita. Il trasporto esatto del parametro produce
un risultato diverso: fissata la fase e la valutazione v, **ogni parola finita
ammissibile dopo la raffica si realizza per infiniti parametri positivi**.
Non si può dunque escludere una continuazione finita soltanto perché segue
una torre della v6. Questo precisa il limite della strategia proposta;
non esclude vincoli che usino anche l'altezza reale o ulteriori restrizioni
sul parametro.

## 1. Il parametro conserva esattamente la precisione binaria

Per v≥1 e q naturale definiamo

\[
 Q_v(q)=\frac{9^{2^v q}-1}{2^{v+3}}.
\]

La divisione è esatta, anche per q=0. Per r<q, LTE e la fattorizzazione

\[
 9^{2^v q}-9^{2^v r}
 =9^{2^v r}\bigl(9^{2^v(q-r)}-1\bigr)
\]

danno

\[
 \nu_2\bigl(Q_v(q)-Q_v(r)\bigr)=\nu_2(q-r).
\]

Ne segue, per ogni b≥0,

\[
 Q_v(q)\equiv Q_v(r)\pmod{2^b}
 \quad\Longleftrightarrow\quad q\equiv r\pmod{2^b}.
\]

Sui residui finiti questo è un'iniezione di un insieme finito in sé, quindi
una biiezione. Inoltre `Q_v(q) mod 2 = q mod 2`. La dimostrazione non assume
una distribuzione casuale degli iterati.

Modulo Lean: [TowerParameter.lean](../../lean/CollatzShadowing/TowerParameter.lean).

## 2. Trasporto fino alle orbite effettive

Nella fase C poniamo d=2^v q e

\[
 n=\frac{2^{3d+1}-11}{3},\qquad y=\frac{9^d-5}{4}.
\]

Il reset, i d−1 blocchi `[1,2]` e l'uscita `[1,4]` già descritti nella v6
danno `S^(2d+1)(n)=y`. I successivi v passi di esponente 1 portano a

\[
 S^{2d+1+v}(n)=z=2\,3^v Q_v(q)-1.
\]

Nella fase B, l'uscita `9^(d+1)−10` percorre v+2 passi di esponente 1 e
arriva a `2·3^(v+4)Q_v(q)−1`. Le formule valgono per tutti i parametri positivi
nei domini indicati. Per q dispari le raffiche indicate sono massimali:
l'esponente seguente è almeno 2. La formalizzazione del teorema sui suffissi
certifica direttamente gli esponenti prescritti, senza assumere tale
massimalità come ipotesi.

Il modulo [TowerSuffix.lean](../../lean/CollatzShadowing/TowerSuffix.lean)
collega il trasporto di fase C alla sorgente originale tramite
`CancellationTower`; per B formalizza il tratto dall'uscita alla raffica.

## 3. Ogni parola finita ammissibile ha una sola classe del parametro

Sia w una parola finita non vuota, con primo esponente almeno 2 e tutti gli
altri positivi. Poniamo A=Σw, L=|w|, P=3^L e C=C_w, dove
`(Pz+C)/2^A` è l'estremo affine del suffisso. Scriviamo
`z=2·3^s Q_v(q)−1`, con s=v nella fase C e s=v+4 nella B.

Il teorema dei cilindri esatti già presente nel progetto dà

\[
 w\text{ è realizzata da }z
 \quad\Longleftrightarrow\quad
 Pz+C\equiv2^A\pmod{2^{A+1}}.
\]

Poiché P+C è divisibile per 4, la sostituzione di z e la cancellazione di
un fattore 2 danno precisamente

\[
 3^{L+s}Q_v(q)+\frac{C+P}{2}
 \equiv 2^{A-1}+P\pmod{2^A}.
\]

Il moltiplicatore è dispari e Q_v permuta i residui: esiste quindi una sola
classe `r mod 2^A`. La classe è dispari perché il termine a destra è dispari
e `(C+P)/2` è pari. Il risultato completo è

\[
 \exists r\in\{1,3,\ldots,2^A-1\}\quad
 \forall q>0:\quad
 \operatorname{Matches}(w,z(q))\iff q\equiv r\pmod{2^A}.
\]

Ogni rappresentante positivo `q=r+j·2^A` realizza la parola. Collegando questa
identità alla sorgente della fase C si ottiene il teorema sull'orbita concreta,
con parametri arbitrariamente grandi. In particolare si può prescrivere
`[2] ++ [1]^l` per qualsiasi l finito: dopo il passo di esponente 2 segue una
nuova raffica di crescita lunga quanto richiesto.

Questo enunciato specifica gli esponenti. **Non afferma che tutto il segmento
resti sopra il valore iniziale**, né dà un ritorno discendente alla sezione E.
L'esponente 2 può comportare una discesa locale; il confronto con l'origine
è un obbligo distinto.

## 4. Il ruolo dell'altezza e il criterio operativo

La stessa classe r fornisce un criterio esatto per un parametro limitato:

\[
 \exists\,0<q\le B:\ \operatorname{Matches}(w,z(q))
 \quad\Longleftrightarrow\quad r\le B.
\]

È il punto utile per una continuazione: trasportare insieme **residuo minimo,
modulo e limite del parametro**. Limitare solo il numero di parole o trattare
le valutazioni successive come indipendenti perde questa informazione.
Una ricerca successiva potrebbe verificare se le parole che evitano una
precisa discesa richiedano residui minimi superiori al limite consentito dalla
sorgente. Oggi non abbiamo un limite uniforme su tutte queste parole.

La libertà dei prefissi finiti non permette di scambiare i quantificatori:

\[
 \forall w\text{ finita}\ \exists q\in\mathbb N_{>0}
 \qquad\not\Rightarrow\qquad
 \exists q\in\mathbb N_{>0}\ \forall\text{ prefissi di una parola infinita}.
\]

Una successione compatibile di classi può convergere a un parametro 2-adico
che non è un naturale. Non abbiamo costruito orbite divergenti. Le frequenze
nei residui di q non sono densità naturali delle sorgenti n, che crescono
esponenzialmente in q.

## 5. Controlli, attribuzione e riproduzione

[transport_probe.py](transport_probe.py) usa soltanto interi esatti:

- tutte le 255 parole con primo esponente almeno 2 e somma al più 9;
- sei valori di v e entrambe le fasi: 3.060 classi uniche verificate;
- 533.460 controlli di appartenenza, inclusi rappresentanti oltre il primo periodo;
- 384 orbite di interi effettivamente costruiti, con quattro esponenti dopo la raffica;
- testimoni modulari per `[2] ++ [1]^l` fino a l=64.

L'algoritmo inverte Q_v bit per bit, usando potenze modulari: non costruisce
le sorgenti astronomiche degli ultimi testimoni. La prova Lean e i test finiti
hanno ruoli distinti. I risultati riproducibili sono in
[transport_results.json](transport_results.json).

La libertà generale dei prefissi e la codifica 2-adica sono classiche:
[Bernstein–Lagarias, 1996](https://doi.org/10.4153/CJM-1996-060-x) studiano la
coniugazione della mappa abbreviata, che induce permutazioni a ogni livello
finito; [Laarhoven–de Weger](https://arxiv.org/abs/1209.3495) collegano i grafi
modulari ai grafi di De Bruijn. Non rivendichiamo come nuova questa struttura,
né una coniugazione globale per Syracuse alla sua singolarità. Il contributo
locale è il suo trasporto dimostrato nella specifica famiglia esponenziale
delle torri della v6, con la congruenza esatta sul parametro originario.

```sh
cd lean
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_transport_2026-09-24/DependencyAudit.lean
python3 ../notes/post_v6_transport_2026-09-24/transport_probe.py
```

Il pin resta Lean/Mathlib 4.29.1. Il controllo completo delle dipendenze dei
nuovi teoremi è predisposto in [DependencyAudit.lean](DependencyAudit.lean).
Non è un replay con un kernel indipendente né una revisione matematica umana.
La v6 pubblicata e le sue evidenze rimangono immutate; questa è una nuova
continuazione del working tree. La congettura di Collatz resta aperta.
