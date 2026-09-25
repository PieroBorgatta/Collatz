# Margine globale: un criterio condizionale e un limite del trasferimento quadratico

25 settembre 2026. Continuazione dello [studio aritmetico](../post_v6_arithmetic_2026-09-25/RESULTS_IT.md).

**Esito.** Il controllo del conteggio totale richiede meno della precedente
compensazione su ogni intervallo. Abbiamo ricavato un budget esatto degli
errori fra livelli e una base numerica da cui un loro limite uniforme
sarebbe sufficiente per la discesa. Quel limite rimane da dimostrare.
Abbiamo inoltre dimostrato che non può seguire dalla sola ricorrenza
quadratica, nemmeno conservando un certificato inferiore completo e una
fascia d'altezza: esistono interi compatibili con queste informazioni che
violano il budget superiore. Questi interi **non sono i punti Q_v**.

Le prove sono su carta con revisione interna. Nessuna nuova dichiarazione
Lean, prova uniforme della famiglia o priorità matematica è rivendicata.
L'esperimento riutilizza esclusivamente livelli già studiati, da 5 a 24.

## 1. Obiettivo sufficiente e identità esatte

Usiamo \(T(x)=x/2\) per \(x\) pari e \((3x+1)/2\) per \(x\) dispari.
Per un intero iniziale \(x\), \(J_x(h)\) conta i passi dispari nei primi
\(h\) passi. Per la torre poniamo

\[
 Q_v=\frac{9^{2^v}-1}{2^{v+3}},\quad
 H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,\quad
 j_v=J_{Q_v}(H_v),\quad m_v=2^{v-1}-j_v.
\]

Il [certificato precedente](../post_v6_certificates_2026-09-24/RESULTS_IT.md)
mostra che \(m_v\ge0\), per \(v\ge5\), è sufficiente per una visita
sotto la sorgente \(N_v=(2^{3\cdot2^v-5}-11)/3\). Non è una condizione
necessaria per una discesa successiva. Ai livelli 6, 7 e 9 questo budget
fallisce, ma erano già disponibili certificati con un orizzonte diverso.

Definiamo l'errore fra livelli

\[
 \Delta_v=j_{v+1}-2j_v.
\]

Allora, senza alcuna ipotesi dinamica aggiuntiva,

\[
 \boxed{m_{v+1}=2m_v-\Delta_v},\qquad
 \boxed{m_{v+n}=2^n\left(m_v-
       \sum_{i=0}^{n-1}\frac{\Delta_{v+i}}{2^{i+1}}\right)}.
 \tag{1}
\]

La seconda identità segue per induzione dalla prima. È una riscrittura
esatta dei conteggi, non una stima degli errori futuri. Gli arrotondamenti
degli orizzonti sono conservati:
\(\varepsilon_v=2H_v-H_{v+1}\in\{0,1\}\).
Se \(d_v=2j_v-H_v\), allora
\(\Delta_v=(d_{v+1}-2d_v-\varepsilon_v)/2\); il termine di arrotondamento
non può essere omesso in questa seconda formulazione.

## 2. Un budget che propagherebbe il margine

**Lemma condizionale.** Sia \(g(w)\ge0\) una funzione per cui

\[
 S_g(v)=\sum_{i\ge0}\frac{g(v+i)}{2^{i+1}}<\infty.
\]

Se \(\Delta_w\le g(w)\) per **ogni** \(w\ge v\) e
\(m_v\ge S_g(v)\), allora, per ogni \(w\ge v\),

\[
 m_w\ge2^{w-v}\bigl(m_v-S_g(v)\bigr)+S_g(w)\ge0.
 \tag{2}
\]

**Prova.** In (1) maggioriamo ogni errore con \(g\). Per \(n=w-v\),
la somma dei primi \(n\) termini di \(S_g(v)\) è
\(S_g(v)-2^{-n}S_g(w)\). La sostituzione dà (2). □

Più in generale, basta maggiorare tutte le somme parziali pesate in (1)
con \(m_v\). L'uso dei soli errori positivi dà una condizione sufficiente
più forte e rinuncia ai recuperi dovuti a errori negativi.

Due costi di coda sono calcolabili esattamente:

\[
 g(w)=Cw^2\quad\Longrightarrow\quad S_g(v)=C(v^2+2v+3),
 \tag{3}
\]

\[
 g(w)=C2^{\lceil w/2\rceil}\quad\Longrightarrow\quad
 S_g(2a)=C2^{a+1},\qquad S_g(2a+1)=3C2^a.
 \tag{4}
\]

Per (3) si usano le somme di \(1,i,i^2\) con pesi \(2^{-i-1}\),
pari a \(1,1,3\). Per (4) si raggruppano gli indici pari e dispari;
il rapporto fra coppie successive è \(1/2\).

Ne segue un obiettivo concreto, tuttora **non provato**:

\[
 \Delta_w\le2\,2^{\lceil w/2\rceil}\quad\text{per ogni }w\ge16.
 \tag{5}
\]

Infatti \(m_{16}=1155\) e il costo della coda in (4) è \(1024\).
Se (5) fosse dimostrata, (2) darebbe
\(m_w\ge131\,2^{w-16}+S_g(w)>0\) per ogni \(w\ge16\).
La base 16 è la prima fra i livelli storici 5–24 che soddisfa quel costo.
I livelli precedenti sono già coperti dai certificati finiti esistenti.

Anche \(\Delta_w\le4w^2\) per ogni \(w\ge17\) sarebbe sufficiente:
il costo alla base 17 è \(1304<2789=m_{17}\). Alla base 16 costa
\(1164\), superiore di 9 al margine disponibile. La stima quadratica è
asintoticamente più restrittiva di quella in (5).

**Questi coefficienti e queste basi sono scelte retrospettive.** Non
costituiscono una preregistrazione o una validazione su dati nuovi. Non
abbiamo dedotto nessuna delle due stime dall'aritmetica della torre.
Nemmeno un'analogia con fluttuazioni casuali giustifica un multiplo fisso
della scala radice per tutti i livelli. (5) serve a rendere quantitativo
il lemma mancante, non a dichiararlo plausibile per evidenza statistica.

## 3. Cosa produce realmente la ricorrenza quadratica

La relazione iniziale è

\[
 Q_{v+1}=Q_v+c_vQ_v^2,\qquad c_v=2^{v+2}.
\]

Scriviamo le due iterazioni ai rispettivi orizzonti come

\[
 x=\frac{3^{j_v}Q_v+A}{2^{H_v}},\qquad
 y=\frac{3^{j_{v+1}}Q_{v+1}+B}{2^{H_{v+1}}}.
\]

Sostituendo \(Q_v=(2^{H_v}x-A)/3^{j_v}\), si ottiene una relazione
\(y=\alpha_vx^2+\beta_vx+\gamma_v\) con

\[
 \boxed{\alpha_v=2^{v+2+\varepsilon_v}3^{\Delta_v}}.
 \tag{6}
\]

È un'identità razionale, anche quando \(\Delta_v<0\). Pertanto
maggiorare il coefficiente principale equivale a maggiorare l'errore di
conteggio: la sostituzione affine non fornisce automaticamente una stima.
Riproporre (6) come controllo di \(\Delta_v\), senza un vincolo
indipendente su \(\alpha_v\), sarebbe circolare.

## 4. Un limite esatto delle informazioni conservate

Fissiamo \(v\) e \(f_v(X)=X+2^{v+2}X^2\). Per interi distinti \(X,Z\),

\[
 f_v(X)-f_v(Z)=(X-Z)\bigl(1+2^{v+2}(X+Z)\bigr).
\]

Il secondo fattore è dispari. Dunque \(f_v\) conserva esattamente la
valutazione 2-adica delle differenze ed è una permutazione modulo ogni
potenza di 2. Combinata con la biezione dei cilindri di parità, questa
osservazione dà il seguente fatto.

**Proposizione sui lift.** Siano \(1\le L\le K=H_{v+1}\),
\(X\equiv a\pmod{2^L}\) e \(j=J_{f_v(a)}(L)\). Fra i lift positivi
di quella classe, i possibili conteggi \(J_{f_v(X)}(K)\) sono esattamente

\[
 \{j,j+1,\ldots,j+K-L\}.
 \tag{7}
\]

**Prova.** Il prefisso superiore di lunghezza \(L\) è fissato. Ogni
possibile coda di \(K-L\) parità definisce una classe superiore modulo
\(2^K\) che solleva \(f_v(a)\). La permutazione \(f_v\) ha un unico
lift inverso di \(a\) per quella classe. Ogni classe contiene interi
positivi. Il conteggio della coda può assumere ogni valore fra 0 e
\(K-L\). □

Se \(L\ge H_v\), tutti questi lift conservano **l'intera parola
inferiore**, quindi anche il suo margine. Per certificare il budget
superiore su tutti gli interi di quella classe, la condizione necessaria
e sufficiente è

\[
 j+K-L\le2^v.
 \tag{8}
\]

Questo limita un preciso insieme di informazioni: la ricorrenza
quadratica e un cilindro inferiore fissato. Non limita gli argomenti che
sfruttano ulteriori proprietà aritmetiche dell'intero esatto \(Q_v\).

### Margine positivo sotto, negativo sopra, per ogni v≥6

Poniamo \(M=2^v\), \(H=H_v\), \(K=H_{v+1}\), e imponiamo
\(X\equiv1\pmod{2^H}\). La parola inferiore coincide con quella
del ciclo \(1,2\), perciò

\[
 J_X(H)=\lceil H/2\rceil\le M/2-1.
\]

Abbiamo usato \(H\le M-2\), valido per \(v\ge6\). Il prefisso
superiore coincide con quello di \(n=1+2^{v+2}\). In un'orbita positiva
ogni passo dispari moltiplica al più per 2 e ogni passo pari divide per 2.
Se il suo conteggio su \(H\) passi è \(j\), quindi,

\[
 1\le T^H(n)\le2^{2j-H}n,
 \qquad j\ge\left\lceil\frac{H-v-2}{2}\right\rceil.
\]

Scegliendo in (7) una coda tutta dispari, e usando \(K\ge2H-1\):

\[
 J_{f_v(X)}(K)\ge\frac{3H-v-4}{2}>M.
\]

L'ultimo confronto segue da \(H\ge3M/4\) e \(M/4>v+4\), già veri
a \(v=6\) e persistenti. Inoltre l'errore di trasferimento soddisfa

\[
 J_{f_v(X)}(K)-2J_X(H)\ge\frac{H-v-6}{2}.
 \tag{9}
\]

La perdita possibile è dell'ordine di \(2^v\). Pertanto nessun limite
uniforme di ordine \(o(2^v)\), incluso (5), può discendere dalle sole ipotesi
generiche indicate.

Anche l'altezza può essere mantenuta. Sia \([Z,2Z)\) la fascia delimitata
da potenze consecutive di 2 che contiene \(Q_v\). Poiché

\[
 Q_v\ge2^{3M-v-3},\qquad Z\ge2^{3M-v-3}\ge2^{2M}\ge2^K,
\]

ogni classe modulo \(2^K\) ha un rappresentante in quella fascia.
Più precisamente, se \(r\) è il rappresentante costruito, possiamo porre
\(X=2^K\lfloor Q_v/2^K\rfloor+r\). Restano uguali tutti i bit di
\(X\) e \(Q_v\) sopra la posizione \(K-1\), e
\(|X-Q_v|<2^K\). Inoltre \(f_v(X)/Q_{v+1}\in(1/4,4)\).
La stessa fascia esatta per i due valori superiori non è garantita.

Un controesempio molto piccolo alla sola implicazione di trasferimento
è già \(v=6,X=1,Y=257\):
\(J_X(62)=31<32\), ma \(J_Y(124)=67>64\).
Non ha l'altezza della torre; i lift costruiti dal programma aggiungono
quel requisito. Nessuno di questi esempi è un controesempio di Collatz o
della discesa dei punti \(Q_v\).

## 5. Confronto con la precedente compensazione

Sia \(F_v(r)=305r-589J_{Q_v}(r)\), e poniamo
\(K_v=589\,2^{v-1}-305H_v\). Allora

\[
 F_v(H_v)=589m_v-K_v.
\]

La precedente candidata, che limita ogni caduta di \(F_v\) con
\(D_v=128v^2\), implica \(F_v(H_v)\ge-D_v\) e quindi
\(m_v\ge(K_v-D_v)/589\). Per \(v\ge15\), \(K_v>D_v\):
alla base \(K_{15}=31391>28800\), mentre
\(K_{v+1}=2K_v+305\varepsilon_v\) e \(2D_v>D_{v+1}\).

Il solo budget globale richiede meno. Il converso fallisce già su parole
astratte: ponendo \(s=\lfloor D_v/284\rfloor+1\), la parola
\(1^s0^{H_v-s}\) ha perdita iniziale \(284s>D_v\) ma conteggio totale
\(s\le v^2\le2^{v-1}\) per \(v\ge15\). Questo confronto logico non
afferma che tali parole siano raggiunte da \(Q_v\).

## 6. Dati retrospettivi e controlli

[margin_probe.py](margin_probe.py) riproduce i conteggi ai livelli 5–24,
confronta i dati di riferimento e, dove già disponibili, gli hash delle
parole complete. Ogni coppia verifica anche la ricorrenza quadratica
modulo \(2^{H_v}\) e la scomposizione del conteggio superiore in prefisso
di lunghezza \(H_v\) e coda di lunghezza \(H_{v+1}-H_v\).

| v | margine m_v | errore Δ_v verso v+1 |
|---:|---:|---:|
| 15 | 601 | 47 |
| 16 | 1 155 | −479 |
| 17 | 2 789 | 875 |
| 18 | 4 703 | −1 106 |
| 19 | 10 512 | 1 219 |
| 20 | 19 805 | 23 |
| 21 | 39 587 | 1 657 |
| 22 | 77 517 | −1 845 |
| 23 | 156 879 | 722 |
| 24 | 313 036 | non calcolato |

La regola \(\Delta_v\le0\) fallisce ripetutamente; quella
\(\Delta_v\le v^2\) fallisce a 17, 19, 21 e 23. I limiti
\(4v^2\) e \(2\,2^{\lceil v/2\rceil}\) passano su tutte le
19 coppie disponibili. Questo controllo non stabilisce una legge futura.

Dalla base 15, la somma dei soli errori positivi osservati, pesati come
in (1), è \(47535/256\). Restano \(106321/256\) delle 601 unità
iniziali prima di eventuali errori futuri. Quel residuo non è un limite
dimostrato sulla coda infinita; gli errori negativi, omessi in questo
conto conservativo, spiegano perché il margine effettivo è maggiore.

Il programma costruisce inoltre sei coppie positive con relazione
quadratica esatta e bit alti uguali a quelli di \(Q_v\). Tre usano
la classe inferiore artificiale 1, ai livelli 6, 10 e 12. Le altre tre,
ai livelli 8, 10 e 12, conservano **esattamente tutta la parola inferiore
di Q_v**. Tutte hanno margine inferiore positivo e margine superiore
negativo; le code superiori prescritte sono verificate con iterazione
elementare sugli interi completi. Gli interi, in esadecimale, e tutti i
conteggi sono salvati in [margin_results.json](margin_results.json).

| Classe inferiore conservata | margine inferiore | margine superiore del lift |
|---|---:|---:|
| parola completa di Q_8 | 8 | −120 |
| parola completa di Q_10 | 29 | −426 |
| parola completa di Q_12 | 93 | −1 841 |

Inoltre, su tutte le 19 coppie già note, il prefisso superiore osservato
viola (8) quando si ammette una coda arbitraria. Per i livelli 10–23,
il margine inferiore effettivo è positivo: la proposizione sui lift
mostra quindi che il suo certificato completo e i bit alti, conservati
nel modo descritto, non determinano da soli un certificato superiore.
Il valore reale \(Q_v\) rimane distinto dai lift sfavorevoli.

Non sono stati calcolati nuovi livelli della torre. La riproduzione usa
il motore Python già congelato; i precedenti hash C/GMP restano evidenza
indipendente per le parole di riferimento già verificate. Il nuovo
replay CI è una riproduzione dello stesso programma, non un secondo
motore indipendente per l'intero esperimento.

```sh
python3 notes/post_v6_margin_2026-09-25/test_margin.py
python3 notes/post_v6_margin_2026-09-25/margin_probe.py --output /tmp/margin_results.json
cmp notes/post_v6_margin_2026-09-25/margin_results.json /tmp/margin_results.json
```

Gli 11 test separati controllano le somme finite con resto esatto,
l'identità telescopica con errori di entrambi i segni, gli arrotondamenti,
le permutazioni e i lift contro enumerazione esaustiva di piccoli moduli,
gli avversari contro iterazione elementare e il rifiuto di riferimenti
alterati. Due agenti hanno revisionato indipendentemente il testo;
un controllo separato ha ripercorso anche tutti e sei gli interi
controesempio. La revisione ha corretto «subesponenziale» in
\(o(2^v)\): il limite (5) è esponenziale nel parametro \(v\), sebbene
di ordine inferiore a \(2^v\). Non è una revisione umana esterna.

Il [replay completo in CI](https://github.com/PieroBorgatta/Collatz/actions/runs/36137449224)
e la [build Lean con gli audit esistenti](https://github.com/PieroBorgatta/Collatz/actions/runs/36137449166)
sono passati sul commit `b03b2a10795e7dac4b22f418fe60cc4403616aa8`.
Il risultato scaricato dalla CI coincide byte per byte con il JSON locale.
Il [manifest di verifica](verification_manifest.json) archivia gli hash,
i collegamenti e i log compressi. La build Lean controlla il progetto
esistente, non formalizza gli argomenti di questa nota. Le modifiche
successive al commit verificato riguardano documentazione ed evidenze.

## 7. Fonti e decisione di ricerca

La biezione fra parole finite e classi residue è classica: si veda
Bernstein–Lagarias, *The 3x+1 Conjugacy Map* (1996), §1 e Appendice A,
[testo primario](https://www.cambridge.org/core/services/aop-cambridge-core/content/view/6975BB4A8C46CF6842217043AAF9EC13/S0008414X0004606Xa.pdf/3x_1_conjugacy_map.pdf).
L'argomento sui lift combina quel fatto con la semplice fattorizzazione
di \(f_v(X)-f_v(Z)\). Non attribuiamo il risultato specifico sui margini
a quell'articolo e non ne rivendichiamo la priorità.

La ricerca mirata sulle correlazioni di parità non ha fornito una stima
puntuale applicabile agli errori di questa torre. Per confronto,
[Inselmann, v3, Teorema 1.6](https://arxiv.org/html/2402.03276v3)
controlla gli scarti dei conteggi su un insieme di densità naturale 1.
Non identifica i singoli eccezionali e non garantisce che la successione
sparsa \(Q_v\) li eviti. Non sostituisce l'ipotesi futura del lemma.
Questa ricerca è mirata e non certifica l'assenza di altri risultati.

Il tentativo ha ora un esito preciso: (2) fornisce un criterio
quantitativo utilizzabile, ma la sola relazione quadratica, anche con
un intero certificato inferiore, non basta a soddisfarlo. L'informazione
aggiuntiva deve distinguere il punto esatto \(Q_v\) dai lift costruiti.
La stima (5) è una formulazione possibile di ciò che manca, non una nuova
prova né una conseguenza dei dati. Prima di ulteriori formalizzazioni
serve un argomento aritmetico che produca tale distinzione.
