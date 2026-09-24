# Discesa dopo le torri: esperimento esatto e vincolo sul minimo residuo

24 settembre 2026. Continuazione del [trasporto dei parametri](../post_v6_transport_2026-09-24/RESULTS_IT.md).

**Esito:** tutti i 4.130 parametri esaminati tornano sotto la sorgente.
Il massimo campionario del tempo residuo diviso per q è 24/11.
Una deduzione matematica con prova sotto mostra inoltre che una parola
discendente non vuota può valere per **al massimo un parametro**, il minimo
residuo della sua classe. Non abbiamo dimostrato la discesa di una famiglia
infinita, né stabilito l'originalità di questa deduzione. Nessun nuovo modulo
Lean è aggiunto: le prove di questa nota sono matematiche informali.

## 1. Oggetto e tempo misurato

Per q positivo dispari poniamo

\[
 n_q=\frac{2\,64^q-11}{3},\qquad z_q=\frac{3\,81^q-11}{8},
 \qquad S(x)=\frac{3x+1}{2^{\nu_2(3x+1)}}.
\]

Il ponte già formalizzato dà `S^(4q+2)(n_q)=z_q`. Studiamo

\[
 \tau(q)=\min\{k\ge0:S^k(z_q)<n_q\},
\]

con valore infinito se l'insieme fosse vuoto. È un tempo dalla fine della
raffica **sotto la sorgente originale**, non sotto z_q e non fino a 1.
Per q=1, n=39 e z=29, quindi τ=0. Per q=3 l'orbita era già scesa a 132859
sotto n=174759 prima della raffica; risale a z=199289 e qui τ=1.
Il tempo registrato non è dunque, in generale, il primo tempo globale dalla
sorgente. Il prefisso ha 4q+2 passi Syracuse, somma degli esponenti 6q+4
e 10q+6 passi della mappa ordinaria non abbreviata.

## 2. Disegno e risultati finiti

Il pilot iniziale q≤1023 ha orientato il costo della ricerca; un controllo
successivo q≤4095 ha verificato la metrica e il certificato del termine
additivo. La corsa archiviata usa:

- tutti i 4.096 q dispari fra 1 e 8191;
- i vicini `2^h±1`, h=10,…,16;
- 24 q campionati senza ripetizioni fra 8193 e 65535, seed 20260924;
- parametri di parole `[2] ++ [1]^l`, l=4,…,16: minimo residuo e prime due
  traslazioni, quando q≤65537. Più parole possono selezionare lo stesso q.

Tolte le sovrapposizioni, sono **4.130 q distinti**, 34 oltre la griglia
esaustiva. Il massimo q è 65537: non abbiamo verificato tutti i q fino a
65537. Il calcolo diretto esegue **14.846.206 passi Syracuse dopo z**.
Il limite operativo è 16q+256; una mancata discesa entro il limite sarebbe
registrata come censura, senza dedurre divergenza. Non ci sono casi censurati.
Non si tratta di una preregistrazione o di un test statistico di indipendenza.

| Limite candidato su τ/q | Violazioni osservate |
|---|---:|
| 1 | 62 |
| 3/2 | 5 |
| 2 | 1: q=11, τ=24 |
| 5/2 | 0 |
| 3 | 0 |

Il caso q=11 **smentisce** il limite universale τ≤2q. L'assenza di violazioni
di τ≤(5/2)q non lo dimostra. La parola del caso peggiore è

```
[2,1,1,1,2,2,1,2,1,1,1,3,2,1,1,1,1,1,3,2,2,1,4,4]
```

Ha lunghezza 24 e somma 41. I record successivi nel rapporto non aumentano
oltre 24/11, anche nei controlli aggiuntivi.

| Intervallo esaustivo di q | Στ/Σq | Massimo τ/q |
|---|---:|---:|
| 513–1023 | 0,811732 | 1,140770 |
| 1025–2047 | 0,816275 | 1,015670 |
| 2049–4095 | 0,817618 | 1,019944 |
| 4097–8191 | 0,821350 | 0,953338 |

Στ/Σq è un rapporto di somme, non la media aritmetica dei singoli rapporti.
Le frazioni esatte sono nel [riepilogo JSON](descent_summary.json); gli
arrotondamenti della tabella non partecipano ai controlli.
Per q=65537, τ=52510, A=105499 e la sorgente ha 393222 bit.

## 3. Il limite del parametro deriva dalla discesa

Sia w una parola effettiva non vuota dopo z_q, di lunghezza k, somma A e
costante affine C≥0. Il primo esponente è almeno 2, dunque A≥2, e

\[
 S^k(z_q)=\frac{3^kz_q+C}{2^A}.
\]

**Proposizione.** Se `S^k(z_q)<n_q`, allora `q≤3(A−k)<3A` e `q<2^A`.
Se r_w è il minimo residuo positivo della classe parametrica già formalizzata,
allora necessariamente **q=r_w**.

**Prova.** Sia R=81/64. L'identità

\[
 16\,64^qz_q-9\,81^qn_q=33\,81^q-22\,64^q>0
\]

dà `z_q/n_q>(9/16)R^q`. Posto d=A−k≥1, dalla discesa e k≥1 segue

\[
 2^d>(9/16)(3/2)^k R^q\ge(27/32)R^q.
\]

Poiché `R^3>2` (531441>524288) e `(27/32)R=2187/2048>1`,
q≥3d+1 darebbe `(27/32)R^q>2^d`, assurdo. Quindi q≤3d.
Per A≥2 vale `3(A−1)<2^A`: base 3<4; nell'induzione basta
aggiungere 3 e usare 3<2^A. Siccome k≥1, segue q≤3(A−k)≤3(A−1)<2^A.
Infine il teorema dei suffissi dà `q mod 2^A=r_w`; con 0<q<2^A si ha
q=r_w. □

Una condizione necessaria più precisa, senza logaritmi, è

\[
 3^{4q+2+k}<2^{6q+4+A}.
\]

Segue dalla stessa minorazione di z/n ed equivale alla contrazione del
coefficiente moltiplicativo dell'intero tratto sorgente–estremo.

**Portata esatta.** La parola w può portare sotto la sorgente per al massimo
un q; non affermiamo che r_w scenda. Inoltre parole diverse possono certificare
lo stesso q. Un elenco finito di parole concrete può quindi certificare solo
finiti q. Una prova per una famiglia infinita deve controllare parole che
variano con q, o usare un altro meccanismo. Il criterio non dimostra che tali
parole discendenti esistano per ogni parametro.

## 4. Il termine additivo viene controllato, non trascurato

Scriviamo y_j=S^j(z), A_j=Σ_{i<j}a_i. Il prodotto esatto è

\[
 y_k=\frac{3^kz}{2^{A_k}}
       \prod_{j<k}\left(1+\frac1{3y_j}\right).
\]

Se tutti i y_j≥n per j<k, e k<3n, allora

\[
 \prod_{j<k}\left(1+\frac1{3y_j}\right)
 \le(1+1/(3n))^k\le\frac1{1-k/(3n)}.
\]

L'ultima disuguaglianza segue dal binomio: per t≥0 e kt<1,
`(1+t)^k≤Σ_{j≥0}(kt)^j=1/(1−kt)`.
Otteniamo il certificato sufficiente interamente intero

\[
 k<3n,\quad 3^{k+1}z<2^{A_k}(3n-k)
 \quad\Longrightarrow\quad \exists j\le k:\ y_j<n.
\]

Se una discesa precedente è già avvenuta, il certificato non afferma
necessariamente che l'estremo y_k sia sotto n. La conclusione è «entro k».

Il probe registra anche il primo attraversamento omogeneo
`h(q)=min{k≥0:3^k z_q<2^(A_k)n_q}`. In tutti i campioni **h(q)=τ(q)**.
È un confronto con la soglia n_q, non la congettura CST generale.
Il certificato razionale è soddisfatto al tempo τ in ogni caso non vuoto.

Per verificare l'assenza di un attraversamento omogeneo anteriore senza
moltiplicazioni grandi a ogni passo, il codice controlla `τ<2n` e
`min_{j<τ}y_j≥n+τ`. Per j<τ il prodotto dà
`3^j z/2^(A_j)≥y_j(1−j/(3n))≥(n+τ)(1−τ/(3n))>n`.
Se queste condizioni fallissero, il codice ricalcolerebbe il tempo omogeneo
direttamente. Tutti i campioni con τ>0 soddisfano le condizioni; q=1 è
trattato separatamente, senza minimo di un insieme vuoto. Il verificatore
separato usa comunque il confronto omogeneo diretto nei casi ripercorsi.

## 5. Letteratura e originalità

- **Andrei–Kudlek–Niculescu (2000)**, *Some results on the Collatz problem*,
  Acta Informatica 37, 145–160,
  [DOI](https://doi.org/10.1007/s002360000039),
  [testo degli autori](https://www.researchgate.net/profile/Stefan-Andrei-2/publication/220198003_Some_results_on_the_Collatz_problem/links/557ad62a08aee4bf82d596f3/Some-results-on-the-Collatz-problem.pdf),
  Lemma 3.1(ii) e Teorema 3.1(ii): la mappa ordinaria manda
  `2^(3m)s−5` in `3^(2m)s−5` dopo 5m passi. È un precedente diretto della
  compressione `[1,2]^m`; nella nostra formulazione Syracuse le valutazioni
  esatte richiedono il dominio già specificato, con cofattore pari.
- **Rozier–Terracol**, [v5 del 17 maggio 2026](https://arxiv.org/html/2502.00948v5),
  pubblicato in Discrete Mathematics 349, 115167 (2026): il Teorema 4.2,
  equazione (10), usa già il prodotto dei fattori additivi e la media armonica.
  Il controllo con il minimo n qui sopra è una specializzazione elementare.
  La distinzione fra stopping time e coefficient stopping time compare
  nella Definizione 1.2; l'uguaglianza universale non è assunta.
- L'euristica con esponenti medi pari a 2 suggerisce
  `τ/q≈log(81/64)/log(4/3)≈0,818842`. La vicinanza dei dati è un confronto
  descrittivo. [Inselmann, v3](https://arxiv.org/abs/2402.03276v3) studia
  comportamenti tipici in densità naturale; non si possono trasferire
  automaticamente a questa sottosequenza esponenziale di densità zero.
- [Niu, 2605.13886](https://arxiv.org/abs/2605.13886), emerso nella ricerca,
  è ritirato in v2 il 20 maggio 2026 per duplicazione di Rozier–Terracol.
  Non è una conferma indipendente.

Non abbiamo identificato un precedente specifico della proposizione q=r_w
in questa ricognizione mirata. **Questo non stabilisce priorità.** La prova
combina una struttura classica con disuguaglianze elementari per la famiglia.
«Nuovo nel repository», «verificato in Lean» e «originale nella letteratura»
rimangono proprietà diverse.

## 6. Riproduzione e decisione scientifica

```sh
python3 notes/post_v6_descent_2026-09-24/descent_probe.py --output-dir /tmp/tower-descent-replay
python3 notes/post_v6_descent_2026-09-24/verify_descent.py --data-dir /tmp/tower-descent-replay --output /tmp/tower-descent-verification.json
```

Le decisioni del probe usano soltanto interi e frazioni esatte della libreria
standard Python. [CSV completo](descent_cases.csv), [riepilogo](descent_summary.json),
[parole selezionate e parametri prescritti](descent_witnesses.json),
[verifica separata](verification_results.json). Il verificatore ripercorre
84 parametri (235.770 passi) usando divisioni ripetute, ricostruisce il termine
affine e controlla direttamente i due tempi e i certificati in quei casi.
Controlla inoltre 64 ponti dalla sorgente con la mappa ordinaria e tutti i
255 cilindri con A≤9 su tre rappresentanti ciascuno. Dal CSV completo
ricontrolla i conteggi di base e le violazioni dei limiti candidati.
Cinque test di regressione coprono censura, soglie intere e semintere,
campo CSV vuoto e differenza fra primo tempo globale e tempo residuo.
Non è estrazione da Lean,
né revisione matematica umana indipendente. La CI dedicata ripete il probe
completo e confronta i file byte per byte.

La domanda sperimentale `τ(q)≤(5/2)q` sopravvive; non la promuoviamo a teorema.
Non è emersa una ricorrenza dimostrata sulle parole discendenti. Il criterio
q=r_w rende esplicito l'obbligo residuo: provare che **ogni q della famiglia
scelta** sia il minimo residuo di una parola con sufficiente compensazione.
Una proprietà che selezioni i q in base alla discesa già osservata sarebbe
circolare. Aumentare soltanto il campione non colma questo obbligo.

Questa tappa si chiude con dati riproducibili, un limite candidato smentito,
un criterio necessario dimostrato su carta e attribuzioni più precise.
La discesa uniforme, la convergenza a 1 e un ritorno discendente alla sezione E
rimangono non dimostrati. La v6 pubblicata resta immutata.
