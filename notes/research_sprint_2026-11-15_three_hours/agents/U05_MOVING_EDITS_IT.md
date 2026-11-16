# U05 — Pochi edit sparsi: un no-go per corridoi lunghi, non per blocchi generici

Sessione del 15–16 novembre 2026, base `203cbb8`. Prova su carta proposta al coordinatore; nessuna formalizzazione Lean, scansione numerica o GPU. L'input esterno è il Corollario 2 di Evertse (1984), già letto e auditato in T02/T04. Non si rivendica una priorità bibliografica globale.

## 1. Dominio e risultato nuovo per il progetto

Fissare interi positivi dispari distinti n,y e un intero s≥0. Contiamo i codici fisici

`(u,p,α,β,v)`, con `u≤X`,

per cui `pα` è una parola effettiva da u a n e `pβ` una parola effettiva da v a y. Il prefisso p è identico; le code hanno la stessa lunghezza L e lo stesso totale B. Ciascuna coda contiene al più s esponenti diversi da 1. I valori di tali esponenti, L e la distanza fra le modifiche possono crescere senza alcun bound fissato. Nessun cutoff è imposto a v. Le copie di una medesima tupla non sono codici nuovi.

**Proposizione.** Il numero di questi codici è `X^o(1)`: per ogni ε>0 esiste C_(ε,n,y,s) con count≤C X^ε per X≥2. Sono quindi subpolinomiali anche le sorgenti coperte e le immagini distinte.

Il risultato estende T04 a una classe di code di lunghezza crescente: pochi eventi non-1 separati da corridoi tutti-1 arbitrariamente lunghi. Include strategie con un numero fissato di edit quando tutte le posizioni inalterate della coda hanno esponente 1. Non riguarda un numero fissato di edit separati da blocchi di complessità non limitata.

Il sibling canonico del progetto è `4n+1` quando questo è ammissibile e altrimenti `16n+5`. In entrambi i casi y−n non è divisibile per 3. La proposizione, però, vale per qualsiasi coppia dispari positiva distinta.

## 2. Compressione esatta della costante affine

Per una coda a=(a₁,…,a_L), porre `A_i=Σ_(j≤i)a_j`, A₀=0 e A_L=B. La costante forward locale è

`C(a)=Σ_(i=1)^L 3^(L−i)2^(A_(i−1))`.

Definire

`F(a)=Σ_(i:a_i≥2) [2^(A_(i−1)+1)−2^(A_i)]3^(L−i)`.

Il telescopio di `3^(L−i)2^(A_(i−1))(3−2^a_i)` dà esattamente

**`C(a)=3^L−2^B−F(a)`**.

Ogni esponente 1 scompare da F. Se a contiene al più s non-1, F è dunque una somma di al più 2s coordinate del tipo ±2^b3^j, con `0≤b≤B` e `0≤j<L`. Non si è dichiarato costante il numero di termini della costante affine non compressa.

Siano r=|p|, P=Σp, k=r+L e A=P+B. L'identità di concatenazione di T04 elimina il prefisso e dà

`3^k(v−u)=2^P R`,

`R=2^B(y−n)+F(β)−F(α)`.

Quindi `3^k|R`. Inoltre R≠0: R=0 imporrebbe u=v; due parole effettive di lunghezza k dalla stessa sorgente hanno lo stesso endpoint, in contraddizione con n≠y. In questo dominio a profondità uguale non serve un'ulteriore ipotesi di bacini disgiunti. Essa è necessaria nell'estensione storica T04 che cambia profondità, non qui.

## 3. Evertse vede il prefisso, non deve limitare tutta la coda

R è una somma non nulla di al più 4s+1 coordinate S-unità, con S formato da infinito, 2, 3 e i primi di y−n. Il numero di coordinate e S sono fissati. Eventuali sottosomme nulle sono ammesse dal Corollario 2; non occorre eliminare coordinate in modo dipendente dalla parola.

Il minimo dei valori assoluti ternari delle coordinate è almeno

`3^(-max(L−1,ν₃(y−n)))`.

La loro altezza reale è al più `C_(n,y)2^B3^L≤C_(n,y)6^B`, poiché L≤B per code non vuote. Applicando il Corollario 2 con parametro arbitrariamente piccolo si ottiene, per ogni τ>0,

`ν₃(R)≤L+τA+C_(τ,n,y,s)`.

L'eventuale coda vuota si tratta direttamente: R=y−n e il prefisso comune ha lunghezza≤ν₃(y−n). Per le altre, da k≤ν₃(R) segue

**`r≤τA+C_τ`**.                                             (1)

La differenza rispetto a T04 è essenziale: non abbiamo ottenuto k=o(logX). Il costo L della potenza ternaria rimane e viene pagato con la struttura della coda.

## 4. Clock elementare delle code con pochi non-1

Per ogni stato positivo dispari x, un passo non-1 soddisfa `S(x)+1≤x+1`; un passo 1 soddisfa `S(x)+1=(3/2)(x+1)`. Una corsa di ℓ esponenti 1 obbliga `2^ℓ|(x+1)`, dunque `ℓ≤log₂(x+1)`. La sua altezza finale spostata è al più `(x+1)^(log₂3)≤(x+1)²`.

Una coda con al più s passi non-1 ha al più s+1 corse di 1. Partendo dallo stato z del prefisso, il totale delle loro lunghezze è al più

`(2^(s+1)−1)log₂(z+1)`.

Questa maggiorazione include il punto fisso 1: ogni sua ripetizione ha esponente 2 ed è già contata fra gli s passi non-1. Non si assume iniettività, primo arrivo o nonperiodicità.

La crescita deterministica del prefisso dà `z+1≤(3/2)^r(u+1)`. Con `C_s=2^(s+1)−1` segue

`L≤s+C_s[log₂(X+1)+r]`,

`k≤(1+C_s)r+C_s log₂(X+1)+s`.                              (2)

Il budget di qualunque parola effettiva, `2^A n≤4^k u`, dà `A≤2k+log₂X`. Inserendo (2) in (1), e scegliendo prima τ abbastanza piccolo per assorbire il coefficiente di r, otteniamo k,A=O_s(logX), con un additivo dipendente dai target e dal parametro scelto. Reinserendo questo bound in (1), valido per ogni τ>0, si conclude

**`r=o(logX)`**, mentre **`L,A=O(logX)`**.

Le costanti di Evertse rimangono ineffettive. Nessuna soglia numerica uniforme è stata prodotta.

## 5. Conteggio corretto dei codici

Il prefisso positivo ha lunghezza r=o(logX) e totale≤A=O(logX). Sommando le composizioni positive, il numero dei prefissi è limitato da

`Σ_(r≤o(logX)) binom(O(logX),r)=exp(o(logX))=X^o(1)`.

Non si usa il bound grezzo A^r, che perderebbe il controllo al bordo. Per ogni coda, scegliere L=O(logX), al più s posizioni non-1 e i loro valori≤A costa al più `O((logX)^(2s+1))`. Le due code e l'eventuale scelta della decomposizione aggiungono soltanto fattori polilogaritmici.

Una parola originale e il target n determinano al più una sorgente u; la parola nuova e y determinano al più una v. Il numero dei codici fisici è dunque X^o(1), senza cutoff sull'uscita. Le collisioni possono soltanto diminuire il numero di immagini.

Per un flusso normalizzato con massa uscente≤1 per sorgente, una relazione che copra soltanto queste sorgenti ha massa uscente o(X). Il conteggio di più etichette non può trasformarla in una quota relativa positiva di un bacino di densità inferiore positiva. Questo non è una confutazione di H.

## 6. Perché il caso di pochi edit generici rimane aperto

Fra due edit il rapporto cumulativo dei fattori di 2 è costante. Se è `2^D`, la differenza scalata `z_j=2^D x'_j−x_j` soddisfa sui passi inalterati

`2^a_j z_j=3z_(j−1)+(2^D−1)`.

Per D>0, z_j è dispari; se resta integrale segue un'autentica dinamica di tipo `3z+(2^D−1)` con le valutazioni comuni. Quando D<0 si usa l'analoga normalizzazione intera. Gli offset di un lungo blocco generico conservano perciò una dinamica reale, non pochi parametri S-unità fissati. Senza un controllo della sua complessità non segue il bound del §3 con 4s+1 termini.

Una coda finale inalterata di lunghezza q impone `3^q|(y−n)`. Per i sibling canonici q=0: almeno l'ultimo esponente deve cambiare. T02 copre due edit di shift fissato, uno interno e quello finale. Il passaggio a tre o più edit con blocchi intermedi generici non è chiuso da questa nota.

## Fonti e stato

- T02 e T04 del 15 novembre: residui completi, quantificatori e audit della versione minima del Corollario 2 di Evertse.
- [Evertse, Compositio 53 (1984), p.228](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf): unico input di approssimazione diofantea.
- `WordSurgery.constant_append` e identità affini effettive locali: convenzione forward usata sopra.

La prova non usa il bound analitico profondo sulle escursioni a budget non-1 fissato del post23: il clock elementare basta perché il coefficiente di logX può dipendere da s. Il risultato va sottoposto a revisione indipendente prima di promuoverlo nella sintesi finale.
