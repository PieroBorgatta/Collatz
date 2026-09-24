# Passaggio fra livelli: prefisso comune e ostacolo alla discesa

24 settembre 2026. Continuazione dello
[studio dei tempi residui](../post_v6_descent_2026-09-24/RESULTS_IT.md).

**Esito:** la relazione esatta fra livelli conserva soltanto prefissi che
restano sopra la sorgente originale. Inoltre, usando il teorema classico di
Mahler, il numero di passi residui necessario non può essere uniformemente
limitato al crescere del livello. Questa è una delimitazione della strategia,
non una prova di discesa per la famiglia infinita e non una prova di divergenza.
Le dimostrazioni sotto sono informali, con revisione interna; non sono nuove
dichiarazioni Lean e non ne rivendichiamo l'originalità matematica.

I calcoli esatti coprono 512 confronti modulari fra livelli e 14 orbite di
interi completi, per 213.894 passi residui. Tutte le 14 orbite scendono sotto
la rispettiva sorgente, dopo la separazione dal livello successivo.
Tredici di questi casi erano già presenti nello studio precedente: non sono
tredici nuovi casi indipendenti. Il nuovo caso è q=131071.

La [CI 36023967396](https://github.com/PieroBorgatta/Collatz/actions/runs/36023967396)
ha ripetuto tutti i controlli al commit
`c2a194962870b157bf6dc6f216baf49eb000f9f3`. I due file di risultati
scaricati dalla CI coincidono byte per byte con quelli locali.
Sono passati anche build e audit del progetto nella
[CI Lean 36023967347](https://github.com/PieroBorgatta/Collatz/actions/runs/36023967347).
[Manifest di verifica](verification_manifest.json) e
[log della corsa sperimentale](ci_36023967396.log.gz).

## 1. La sottofamiglia e il significato di discesa

Scriviamo S(x)=(3x+1)/2^{ν₂(3x+1)} per x positivo dispari. Definiamo

\[
 Q_v=\frac{9^{2^v}-1}{2^{v+3}}\quad(v\ge1),\qquad
 N_v=\frac{2^{3\cdot2^v-5}-11}{3}\quad(v\ge5).
\]

Per q=2^{v−1}−1, la sorgente dello studio precedente è proprio N_v=n_q.
Il suo endpoint z_q=(3·81^q−11)/8 segue la parola esatta

\[
 [2,2,v-4],\qquad S^3(z_q)=Q_v.
\]

Infatti, posto h=v−1≥4, q=2^h−1≡15 (mod 16) dà
81^q≡177 (mod 256). I primi due endpoint sono
(9·81^q−25)/32 e (27·81^q−43)/128. Il successivo numeratore è
(81^{2^h}−1)/128; LTE dà ν₂(81^{2^h}−1)=h+4, quindi il terzo esponente
è h−3=v−4. La somma dei tre esponenti è v.

Questa ricodifica porta il parametro a 1 nella notazione Q_v(1), ma aumenta
il livello e **non riduce il valore sotto la sorgente**. Per v≥5 vale
Q_v>6N_v, come dimostrato nella sezione 4. Anche i due endpoint intermedi
restano sopra N_v: dallo studio precedente z_q/N_v>(9/16)(81/64)^q>18,
e ciascuno dei primi due passi moltiplica il valore per più di 3/4.

Misuriamo dunque

\[
 t_v=\min\{k\ge0:S^k(Q_v)<N_v\},
\]

con t_v=∞ se l'insieme è vuoto. Quando finito, t_v+3=τ(q) dello studio
precedente. Non è il tempo fino a 1, né necessariamente il primo tempo
di discesa dell'intera orbita partita da N_v.

## 2. Ricorrenza esatta e precisione fra livelli

La fattorizzazione della differenza di quadrati dà

\[
 \boxed{Q_{v+1}=Q_v+2^{v+2}Q_v^2.}
\]

Poiché Q₁=5, ogni Q_v è dispari. L'incremento ha valutazione esattamente
v+2. Per ogni w>v, la somma degli incrementi da v a w−1 ha un unico
termine di valutazione minima, il primo. Di conseguenza

\[
 \boxed{\nu_2(Q_w-Q_v)=v+2\quad\text{per ogni }w>v.}
\]

La stessa relazione fornisce un modo economico di calcolare Q_v modulo
2^B senza costruire un intero con un numero di bit proporzionale a 2^v.
Un controllo modulare a v=512 non equivale a calcolare tutta l'orbita
dell'intero Q₅₁₂.

## 3. Quale parte delle orbite è davvero comune

Sia a=(a₁,…,a_k) una parola iniziale **effettivamente seguita da Q_v**,
con A=Σa_i, inclusa la parola vuota con A=0. Per ogni w>v:

\[
 \boxed{Q_w\text{ segue la stessa parola }a\iff A\le v+1.}
\]

**Sufficienza.** Una parola esatta di somma A dipende dal residuo iniziale
modulo 2^{A+1}; il bit aggiuntivo garantisce la disparità dell'endpoint.
Se A≤v+1, Q_w≡Q_v (mod 2^{A+1}). Si può anche verificare passo per passo:
prima del passo j la differenza ha valutazione v+2−Σ_{i<j}a_i>a_j,
quindi i numeratori hanno la stessa valutazione a_j.

**Necessità.** Per una parola condivisa, la differenza degli endpoint è

\[
 S^k(Q_w)-S^k(Q_v)=\frac{3^k(Q_w-Q_v)}{2^A}.
\]

Entrambi gli endpoint sono dispari, quindi la differenza ha valutazione
almeno 1. La valutazione del membro destro è v+2−A, da cui A≤v+1. □

Il prefisso comune massimo è finito, perché gli esponenti sono positivi.
Se ha somma A, al primo passo diverso gli esponenti b_v e b_w soddisfano

\[
 \min(b_v,b_w)=v+2-A,\qquad \max(b_v,b_w)>v+2-A.
\]

Infatti i due numeratori differiscono per un numero di valutazione v+2−A;
quando le loro valutazioni sono diverse, la minore è esattamente quella
della differenza. Questo individua la prima separazione, ma **non determina
l'esponente maggiore**. Con soli v+3 bit iniziali, quest'ultimo è certificato
soltanto come almeno v+3−A.

Esempio: Q₆ e Q₇ condividono [3,1,1], di somma 5. Al passo successivo
gli esponenti reali sono [3,8]. I 9 bit modulari impiegati per questo
confronto possono certificare [3,≥4], non [3,4]. Il software conserva
esplicitamente questa distinzione.

## 4. Il prefisso ereditato non arriva sotto N_v

Poniamo R=81/64 e u=2^{v−1}. Dalle definizioni segue

\[
 \frac{Q_v}{N_v}
 >3\,2^{2-v}R^u.
\]

Per verificare il segno, si confrontano (81^u−1)/(64^u/32−11) e
81^u/(64^u/32): la differenza ha numeratore 11·81^u−64^u/32>0.
Poiché R³>2 e u≥3(v−1) per v≥5, otteniamo Q_v/N_v>6.

Per v≥6 vale la stima più forte u≥6v−6. La base è 32≥30;
il passo induttivo segue da 12v−12≥6v per v≥2. Pertanto

\[
 \frac{Q_v}{N_v}>3\,2^{2-v}2^{2v-2}
 =3\,2^v>2^{v+1}.
\]

Qualsiasi prefisso condiviso con un livello superiore ha A≤v+1 e costante
affine C≥0. Il suo endpoint soddisfa

\[
 S^k(Q_v)=\frac{3^kQ_v+C}{2^A}
 \ge\frac{Q_v}{2^A}>N_v.
\]

Per v=5 il prefisso comune massimo è [3,1,1], di somma 5: basta calcolare
Q₅≡189 e Q₆≡61 (mod 256). Il primo passo è maggiore di (3/8)Q₅>
(9/4)N₅ e i due passi con esponente 1 aumentano il valore.
Anche in questo caso ogni endpoint comune rimane sopra N₅. □

Esiste dunque una compressione locale, valida per tutti i v≥4:
Q_v≡61 (mod 64) e

\[
 S^3(Q_v)=\frac{27Q_v+49}{32}<Q_v.
\]

La congruenza segue da Q₄≡61 e dalla ricorrenza; Q_v>49/5 dà la
disuguaglianza. È una discesa rispetto a Q_v, ma non raggiunge N_v.
Ripeterla senza dimostrare il rinnovo della congruenza sarebbe illegittimo.

In termini reali, il divario da recuperare è

\[
 \log_2\frac{Q_v}{N_v}
 =(\log_2 9-3)2^v-v+\log_2 3+2+o(1).
\]

Il numero di divisioni per 2 ereditate è al più v+1; il logaritmo del
rapporto da recuperare cresce invece come 2^v. Questa spiegazione
asintotica è coerente con la disuguaglianza esatta appena dimostrata.

## 5. Limite 2-adico e tempi residui non uniformemente limitati

La ricorrenza mostra che Q_v converge in ℤ₂ a un dispari L, con
ν₂(Q_v−L)=v+2. Le identità usuali fra esponenziale e logaritmo 2-adici
identificano il limite:

\[
 L=\frac{\log_{\mathbb Q_2}(9)}8
 =\sum_{j\ge1}(-1)^{j+1}\frac{2^{3j-3}}j.
\]

Infatti, posto β=log_{ℚ₂}(9), ν₂(β)=3 e
Q_v=(exp(2^vβ)−1)/2^{v+3}→β/8 in ℚ₂. La valutazione esatta della
differenza segue anche sommando gli incrementi della ricorrenza: il primo
ha valutazione v+2 e tutti i successivi almeno v+3. Il simbolo
log_{ℚ₂} indica il logaritmo p-adico, distinto dal log₂ reale della sezione 4.

**Dipendenza dalla letteratura.** Il teorema di Mahler afferma che, per
un argomento algebrico non nullo nel disco di convergenza, l'esponenziale
p-adico è trascendentale. Se β fosse algebrico, |β|₂=1/8<1/2 e exp(β)=9
lo contraddirebbero. Quindi β e L sono trascendentali su ℚ. È un risultato
classico esterno, non dimostrato qui né verificato in Lean. La formulazione
è confermata dalla prova del Teorema 2.7.2, p. 21, di
[Calegari–Dimitrov–Tang](https://www.math.uchicago.edu/~fcale/papers/L2chi.pdf).
Il riferimento originale è
[Mahler, J. reine angew. Math. 169, 61–66](https://doi.org/10.1515/crll.1933.169.61).
È disponibile anche la [ristampa EMS](https://ems.press/books/dms/252/4974);
il titolo della ristampa indica 1932, mentre il DOI originale indica 1933.

S estende la sua definizione agli interi 2-adici dispari diversi da −1/3.
Ogni iterato ottenuto da L tramite una parola finita è un'espressione
affine razionale non costante in L, dunque trascendentale. Nessun iterato
è −1/3: ogni esponente successivo è finito e l'intera orbita 2-adica è
definita. Questa non è un'orbita di interi naturali positivi.

**Corollario, con l'input di Mahler.** Per ogni K finito esiste V tale che
per ogni v≥V e ogni j=0,…,K vale S^j(Q_v)>N_v. Di conseguenza,

\[
 \boxed{t_v\longrightarrow+\infty\quad(v\to\infty),}
\]

dove i singoli t_v possono a priori valere ∞.

**Prova.** Fissato K, i primi K esponenti dell'orbita di L hanno somma
finita A_K. Se v+2>A_K, Q_v e L seguono lo stesso prefisso, per il criterio
di precisione della sezione 3 applicato a un dispari 2-adico. Per j≤K,
scriviamo S^j(Q_v)=(3^jQ_v+C_j)/2^{A_j}, con C_j≥0. La costante
c_K=min_{0≤j≤K}3^j/2^{A_j} è positiva. Poiché Q_v/N_v→+∞ in ℝ,
per v sufficientemente grande c_K Q_v>N_v, simultaneamente per tutti
questi j. □

I quantificatori sono ∀K ∃V ∀v≥V, t_v>K. Non affermano che ciascun t_v
sia finito, che t_v cresca monotonamente, o che esista un singolo intero
con orbita divergente. Il risultato esclude una soluzione con un numero
uniformemente limitato di passi Syracuse dopo Q_v. Non esclude formule
compatte che rappresentino un numero crescente di passi, come quelle
già usate per le torri.

## 6. Esperimento finito e controlli

Il programma usa soltanto interi esatti e la libreria standard Python.

- 512 coppie adiacenti (Q_v,Q_{v+1}), v=1,…,512, calcolate modularmente;
  8 livelli confrontati anche con l'esponenziazione modulare diretta.
- L modulo 2^4096 calcolato in tre modi: ricorrenza, serie del logaritmo,
  esponenziazione modulare. I residui coincidono.
- Un prefisso del limite di 2.032 passi, somma 4.094: restano 2 bit.
  Il passo seguente ha esponente almeno 2, non determinato esattamente.
- 14 orbite complete a partire da Q_v, v=5,…,18, fino al primo valore
  inferiore a N_v, con cap 8·2^v. Nessuna censura, 213.894 passi in tutto.
- Sei test di regressione: confronti fra livelli anche non adiacenti,
  precisione insufficiente, limite inferiore dell'esponente maggiore,
  tre formule del limite, censura al cap e configurazione CLI minima.

| v | q | Passi comuni | Somma comune | t_v | Somma fino alla discesa |
|---:|---:|---:|---:|---:|---:|
| 5 | 15 | 3 | 5 | 5 | 12 |
| 6 | 31 | 3 | 5 | 28 | 54 |
| 8 | 127 | 4 | 9 | 67 | 146 |
| 10 | 511 | 6 | 11 | 392 | 790 |
| 12 | 2047 | 6 | 11 | 1584 | 3200 |
| 14 | 8191 | 7 | 14 | 6444 | 12988 |
| 16 | 32767 | 8 | 17 | 27279 | 54366 |
| 18 | 131071 | 8 | 17 | 107678 | 215196 |

L'ultimo Q_v ha 830.956 bit; la sua sorgente ne ha 786.426. I tredici
casi v≤17 coincidono esattamente con lo studio precedente, togliendo
3 passi e v divisioni dal suo conteggio. La coppia modulare v=512 ha
254 passi comuni, di somma 510: questo dato riguarda il prefisso,
non il tempo di discesa dell'intero Q₅₁₂.

I test con divisioni ripetute forniscono un controllo aritmetico distinto
dei prefissi per piccoli livelli; non sono una seconda implementazione
indipendente dell'intero esperimento. Le tre formule del limite verificano
un residuo finito: non sono una prova computazionale di trascendenza.

Dati: [confronti e orbite](levels_results.json),
[prefisso del limite](limit_prefix.json), [codice](levels_probe.py),
[test](test_levels.py). Da radice del repository:

```sh
python3 notes/post_v6_levels_2026-09-24/test_levels.py
python3 notes/post_v6_levels_2026-09-24/levels_probe.py --output-dir /tmp/tower-levels
cmp notes/post_v6_levels_2026-09-24/levels_results.json /tmp/tower-levels/levels_results.json
cmp notes/post_v6_levels_2026-09-24/limit_prefix.json /tmp/tower-levels/limit_prefix.json
```

## 7. Decisione di ricerca

Il tentativo «trasferire la discesa dal livello v a v+1 attraverso il
prefisso comune» incontra l'ostacolo dimostrato nella sezione 4. La parte
di orbita trasferibile termina prima della discesa richiesta. Una parola
fissa di lunghezza limitata è esclusa anche dalla sezione 5.

La questione utile rimasta è il **controllo dopo la prima separazione**:
serve una famiglia di parole a lunghezza variabile, con stime uniformi
sulla somma degli esponenti e sul termine affine, oppure un'induzione che
colleghi endpoint effettivamente più piccoli. La ricorrenza quadratica
Q_{v+1}=Q_v+2^{v+2}Q_v² e il solo minimo dei due esponenti divergenti
non forniscono tale stima. Al momento non abbiamo trovato quel meccanismo.

Il linguaggio dei cilindri e della precisione p-adica appartiene alla
letteratura classica: si vedano
[Bernstein–Lagarias (1996)](https://doi.org/10.4153/CJM-1996-060-x) e
[Rozier, *Parity sequences of the 3x+1 map on the 2-adic integers*](https://www.ipgp.fr/~rozier/pub/Parity.pdf).
Qui li applichiamo alla specifica famiglia Q_v. Una ricerca bibliografica
non dimostra che questa specializzazione sia originale. La continuazione
non modifica la v6 pubblicata, né aggiunge dichiarazioni al nucleo Lean.
