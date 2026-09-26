# Una nuova domanda: quanta massa passa a un ramo inverso vicino?

26 settembre 2026. Piero Borgatta, con assistenza Codex.

**Stato:** proposta nuova per questo programma, senza rivendicazione di
priorità. Il nucleo combinatorio finito è formalizzato separatamente;
il confronto di densità qui richiesto è una congettura, non un risultato.
La riduzione condizionale elimina soltanto le orbite illimitate. Il problema
dei cicli non banali rimane separato.

## 1. Perché cambiare oggetto

I filtri della torre hanno tentato di controllare una parola eccezionale
attraverso informazioni finite della sorgente. Il nuovo oggetto è una
famiglia di interi che raggiungono uno stesso bersaglio. Qui il progetto
dispone già di identità di occupazione e di un collegamento alla teoria
analitica dei predecessori. La domanda cambia da «quante parità favorevoli
ha questa orbita?» a «quanto piccolo può essere un ramo laterale rispetto
al ramo adiacente che porta allo stesso successore?».

Sia Col la mappa ordinaria e, per r dispari positivo, definiamo

\[
B(r)=\{a\ge1:\exists k\ge0,\ \mathrm{Col}^k(a)=r\},\qquad
d_*(r)=\liminf_{X\to\infty}\frac{|B(r)\cap[1,X]|}{X}.
\]

Tutte le densità sono naturali inferiori: non si assume che il limite
ordinario esista. S è la mappa accelerata sui dispari positivi.

Per n dispari positivo con 3∤n, scegliamo **un solo** ramo laterale:

\[
h(n)=\begin{cases}4n+1,&n\equiv1\pmod3,\\16n+5,&n\equiv2\pmod3.\end{cases}
\]

Poiché S(4n+1)=S(n), valgono S(h(n))=S(n), n<h(n)≤16n+5,
h(n) dispari e 3∤h(n). La seconda scelta salta il fratello divisibile per
3, il cui bacino ordinario ha densità zero. Non si possono trascurare i
domini aritmetici del teorema sui predecessori.

## 2. Il lemma che manca

**Ipotesi H, aperta.** Esiste c>0, indipendente da n, tale che, per ogni
n dispari positivo, 3∤n, quando sia n sia h(n) non hanno ritorni positivi,

\[
\boxed{d_*(h(n))\ \ge\ \frac{c}{1+\log n}\,d_*(n).}\tag{H}
\]

Il nome informale «confronto di Harnack» indica soltanto un rapporto
uniformemente controllato fra due quantità positive. Non abbiamo uno
spazio armonico sul quale applicare un teorema classico con quel nome.
Non conosciamo una prova di H e non sappiamo se sia vera.

La positività separata d_*(n)>0 non implica H: una successione di masse
positive può avere somma finita. Il manoscritto esterno di Mazur produce
costanti dipendenti dal target; le ottimizzazioni dell'overlay locale non
le trasformano nel rapporto richiesto. [Confronto delle fonti](LITERATURE_IT.md).

## 3. Perché H avrebbe una conseguenza globale

**Proposizione condizionale, prova su carta.** Supponiamo H e la positività
del bacino di ogni target dispari positivo non divisibile per 3. Allora non
esistono orbite positive non eventualmente periodiche.

Sia x_i=S^i(x_0) una tale orbita. Scartando il primo termine se necessario,
possiamo assumere 3∤x_0. La sequenza è iniettiva: una ripetizione di una
mappa deterministica renderebbe periodica tutta la coda. Inoltre tende
all'infinito, perché ogni intervallo finito contiene soltanto un numero
finito di termini distinti.

Poniamo y_i=h(x_i). I seguenti passi non usano H.

1. **Nessun y_i è sulla spina x_j.** Se y_i=x_j, applicando S otteniamo
   x_(i+1)=x_(j+1); l'iniettività dà i=j, contro y_i>x_i.
2. **Ogni y_i è nonperiodico.** Dopo un passo la sua orbita è la coda
   iniettiva x_(i+1),x_(i+2),… . Anche ogni x_i è nonperiodico.
3. **I bacini B(y_i) sono disgiunti.** Una sorgente comune raggiungerebbe
   due y in successione. Dopo aver raggiunto il primo, il prossimo stato
   dispari è sulla spina, che non contiene il secondo. Se i tempi sono
   uguali, i target sono uguali e l'iniettività dei successori dà i=j.
   Gli stati pari intermedi della mappa ordinaria non cambiano l'argomento.
4. **I bacini principali sono crescenti:** B(x_0)⊆B(x_i). Dunque
   d_*(x_i)≥δ:=d_*(x_0)>0.
5. **La crescita superiore è elementare:** S(n)≤(3n+1)/2≤2n per n≥1
   dispari; quindi x_i≤2^i x_0.

Per ogni intero m, la disgiunzione dà esattamente

\[
\sum_{i<m}|B(y_i)\cap[1,X]|\le X.
\]

Si passa al liminf per questa somma **finita** e si usa H:

\[
1\ \ge\ \sum_{i<m}d_*(y_i)
\ \ge\ c\delta\sum_{i<m}\frac1{1+\log x_0+i\log2}.
\]

La somma a destra diverge al crescere di m, contraddizione. Non serve un
cutoff X uniforme nei target, né si scambia una somma infinita con un
liminf. La scelta di m precede il passaggio al limite in X. □

La parte finita è l'oggetto di `SiblingBasins.lean`: disgiunzione e budget
con pesi naturali su un insieme finito di sorgenti. La definizione Lean
ammette tempi di visita illimitati e usa appartenenza classica non
computabile; non certifica un algoritmo generale per decidere i bacini.
Il passaggio fra
predecessori ordinari e Syracuse può essere letto mediante la parte
dispari: ogni sorgente a si scrive univocamente a=2^e u con u dispari.
Per un target dispari r, Col raggiunge r da a se e solo se S raggiunge r
da u. Il peso di u al cutoff X è il numero di e≥0 con 2^e u≤X.
Questa specializzazione e l'argomento di densità sopra non sono dichiarati
come formalizzati integralmente in questa fase.

## 4. Perché il denominatore è un obiettivo sostanziale

Un confronto c/(1+log n)^p con p≤1 darebbe ancora una serie divergente.
Con p>1, il solo limite di crescita x_i≤2^i x_0 non basta più. Un costo
polinomiale in n consente una serie geometrica sommabile lungo una spina
esponenziale e non chiude questa dimostrazione. È quindi il **costo del
trasferimento relativo** la quantità da stimare, non la semplice esistenza
di molti predecessori.

L'ipotesi non deve essere estesa a tutti i fratelli L^k(n), L(n)=4n+1.
Fissato un successore, al più un suo predecessore può essere periodico.
Esistono infiniti L^k(n) non divisibili per 3 e nonperiodici. I loro bacini
sono disgiunti. Assegnare a ciascuno il medesimo lower bound positivo
relativo a n violerebbe già il budget finito. La restrizione a h(n), e
quindi al rapporto d'altezza limitato, è indispensabile.

## 5. Il trasporto più semplice è già escluso

Per una parola inversa di lunghezza k≥1, somma degli esponenti A e
costante affine C, un predecessore intero di n soddisfa

\[
3^k a+C=2^A n.
\]

Con la stessa parola e target y=h(n), la sorgente candidata sarebbe

\[
a'=a+\frac{2^A(y-n)}{3^k}.
\]

Ma y−n è 3n+1 oppure 5(3n+1), mai divisibile per 3. Quindi a' non è
intero. Nessuna traslazione banale delle **stesse** parole inverse dimostra
H. Serve un confronto fra parole diverse, con residui ternari, altezze,
molteplicità e masse effettive controllati. La perdita di una di queste
condizioni riprodurrebbe il problema già riscontrato nei filtri.

Un lemma finito sufficiente da cercare sarebbe, con A,c universali positivi,

\[
|B(h(n))\cap[1,AX]|\ge\frac{c}{1+\log n}|B(n)\cap[1,X]|-E_n(X),
\qquad E_n(X)=o_n(X).
\]

Dividendo per AX e passando al liminf darebbe H con c/A. Anche questo
lemma è aperto; non è un'ipotesi accertata di un teorema di mixing esistente.
La ricerca utile sarebbe costruire un accoppiamento di alberi inversi che
produca questa disuguaglianza e ne stimi il costo. Non basta stimare
separatamente una massa di parole che potrebbe contare più volte gli stessi
interi: proprio qui sono pertinenti i lemmi di occupazione del progetto.

## 6. Diagnostica finita: esito e interpretazione

Il [protocollo](PROTOCOL_IT.md) è stato scritto prima del censimento.
Sono stati controllati 340 target dispari, non multipli di 3, fra 5 e 1023,
a quattro cutoff fissati. Si contano tutti gli inizi ordinari 1≤a≤X,
anche quelli la cui orbita supera X prima di raggiungere il target.

| X | Minimo rapporto diagnostico `(1+log n) B(h(n);X)/B(n;X)` | n | h(n) | Conteggi n / h(n) |
|---:|---:|---:|---:|---:|
| 16384 | 0,0012098688 | 911 | 14581 | 6459 / 1 |
| 65536 | 0,0022366769 | 719 | 11509 | 23716 / 7 |
| 262144 | 0,0021418265 | 719 | 11509 | 95527 / 27 |
| 1048576 | 0,0019216208 | 593 | 9493 | 345889 / 90 |

I bacini adiacenti possono essere fortemente sbilanciati. Non è stata
adattata una costante c a questi dati. Nessun valore in tabella è una
densità asintotica certificata, un controesempio a H o una conferma della
sua uniformità. L'ultimo censimento ha 832482 nodi dispari effettivamente
visitati e ha verificato la terminazione di tutti gli inizi nel proprio
intervallo: questa verifica finita non è assunta per altri inizi.

Per i 40 fratelli ammissibili lungo l'orbita di 27 prima di 1, le somme
dei conteggi sono 5718, 23217, 93883 e 378044, tutte sotto il rispettivo X.
Questo controlla l'implementazione della disgiunzione, non la futura
stima relativa. Un replay indipendente con Col controlla tutti i conteggi
fino a 2048; i test includono gli inizi pari e il rifiuto di esplorazioni
che superano il limite fissato. [Dati completi](basin_results.json).

## 7. Decisione

Questa è la candidata principale da sottoporre a revisione, perché riusa
un risultato positivo del progetto e offre un primo obiettivo quantitativo
preciso. Non abbiamo evidenza sufficiente per chiamarla la strada definitiva.
H potrebbe essere falsa, oppure richiedere difficoltà comparabili al problema
di partenza. Il suo interesse non è una presunta facilità: è che separa un
budget combinatorio dimostrabile da un confronto analitico localizzato.

Il prossimo lavoro giustificato è un audit del confronto fra i due alberi
inversi, iniziando dal costo dei residui modulo 3^k. Se ogni costruzione
richiede perdite esponenziali in k o polinomiali in n senza compensazione,
si registra il limite e si sospende la proposta. Non si aumentano i cutoff
del censimento per sostituire quel lemma.

Anche una prova di H più l'input di densità darebbe **eventuale periodicità**,
non necessariamente arrivo a 1. Per risolvere Collatz servirebbe ancora
escludere tutti i cicli positivi non banali. Le condizioni `CycleConstraints`
e i risultati di Hercher/Knight non chiudono oggi quel secondo passaggio.
