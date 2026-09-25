# La storia della torre come vincolo: rigidità e limite del risultato

**25 settembre 2026.** Questa nota studia una condizione assente dai
controesempi locali delle fasi precedenti: possedere antenati interi positivi
lungo la ricorrenza della torre. Si ottiene un risultato di rigidità:
**due antenati, la binade corretta e l'intera parola di parità effettiva
di `Q_v` identificano il punto della torre**. Non si ottiene una stima sul numero di
dispari della parola identificata, né una nuova dimostrazione di discesa.
Le proposizioni sono dimostrate su carta; non sono nuovi teoremi Lean.
Non viene avanzata una rivendicazione di originalità.

## 1. Oggetti e distinzione fra due tipi di storia

Per `v≥1` poniamo

\[
 e_v=2^{v+1},\qquad a_v=2^{v+3},\qquad
 Q_v=\frac{3^{e_v}-1}{a_v},\qquad
 f_v(x)=x+2^{v+2}x^2.
\]

Vale `Q_(v+1)=f_v(Q_v)`. La mappa Collatz abbreviata è
`T(x)=x/2` per `x` pari e `T(x)=(3x+1)/2` per `x` dispari.
La parola di lunghezza `h` registra le parità di
`x,T(x),…,T^(h−1)(x)`. Essa determina esattamente `x mod 2^h`.

La **storia della torre** riguarda le mappe `f_v` fra livelli; la **storia
Collatz** riguarda gli iterati di `T` dentro un livello. I risultati sotto
collegano i rispettivi residui, senza identificare le due dinamiche.

Per `v≥5` usiamo l'orizzonte già fissato

\[
 H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,
 \qquad Z_v=2^{\lfloor\log_2 Q_v\rfloor}.
\]

La binade di `Q_v` è l'intervallo di interi `[Z_v,2Z_v)`.

## 2. Le potenze pure con esponente libero realizzano ogni parola

Introduciamo, per un intero positivo `k`,

\[
 F_v(k)=\frac{3^{e_vk}-1}{a_v}.
\]

**Proposizione 1.** Per `k≠ℓ` interi non negativi,

\[
 \nu_2(F_v(k)-F_v(\ell))=\nu_2(k-\ell).                 \tag{1}
\]

Infatti, posto `B=3^(e_v)`, il lemma LTE dà
`ν₂(B−1)=v+3` e `ν₂(B^t−1)=v+3+ν₂(t)` per `t>0`.
Il fattore `B^min(k,ℓ)` è dispari. Dividendo per `a_v` si ottiene (1).
Quindi `F_v` induce una permutazione modulo ogni `2^h`; inoltre
`F_v(k)≡k mod 2`.

Ogni parola finita che inizia con un dispari è dunque realizzata da una
classe unica di esponenti dispari `k mod 2^h`, e da infiniti `k>0`.
Non si tratta soltanto di coppie di livelli: per ciascun `k` fissato vale

\[
 F_{v+1}(k)=f_v(F_v(k))
\]

a tutti i livelli. Sono torri intere coerenti, con identità esatta di
potenza pura. La libertà consiste nel cambiare l'esponente e l'altezza.

**L'altezza distingue `k=1`.** Per `k≥2`,
`F_v(k)≥F_v(2)=(3^(e_v)+1)Q_v>2Q_v≥2Z_v`.
Pertanto `k=1` è l'unico parametro positivo che produce un punto nella
binade di `Q_v`. Questo isola il punto speciale, ma non limita il peso di
Hamming della sua parola. Imporre direttamente l'esponente esatto `e_v`
identifica già `Q_v` per definizione.

## 3. Una binade intera determina le binadi degli antenati

**Lemma discreto di altezza.** Siano `w≥1`, `x≥1` intero,
`B=⌊log₂x⌋` e `c=2^(w+2)`. Allora

\[
 c2^{2B}\le f_w(x)<4c2^{2B}.
\]

Il limite superiore usa `x≤2^(B+1)−1`, non soltanto `x<2^(B+1)`.
Scrivendo `b=2^B`,

\[
 4cb^2-\bigl(c(2b-1)^2+(2b-1)\bigr)
 =(4c-2)b-c+1>0.
\]

Segue

\[
 \lfloor\log_2 f_w(x)\rfloor=w+2+2B+\varepsilon,
 \quad\varepsilon\in\{0,1\},\qquad
 B=\left\lfloor
 \frac{\lfloor\log_2 f_w(x)\rfloor-w-2}{2}\right\rfloor.       \tag{2}
\]

La binade del successore determina quindi univocamente quella del suo
eventuale antenato intero positivo. Per induzione, una catena di antenati
interi che termina nella binade di `Q_v` attraversa le stesse binadi della
catena `Q_u,…,Q_v`. L'affermazione non si estende senza modifiche agli
antenati reali: il margine discreto nell'ultima riga è essenziale.

## 4. Intervallo radice e conteggio esatto delle parole ammissibili

Per una profondità `1≤t≤v−1`, poniamo `u=v−t`, `d=2^t`, `A=a_u` e

\[
 G_{u,t}=f_{v-1}\circ\cdots\circ f_u,
 \qquad
 G_{u,t}(x)=\frac{(1+Ax)^d-1}{Ad}.                    \tag{3}
\]

La formula deriva iterando l'identità
`1+a_(w+1)f_w(x)=(1+a_w x)^2`.
Di conseguenza un intero `X>0` possiede questi `t` antenati interi positivi
se e solo se `1+a_vX=z^d` per un intero `z>1` con `z≡1 mod A`;
l'antenato iniziale è `(z−1)/A`. La sola potenza perfetta non basta:
per `v=2`, `X=7` si ha `1+32X=15²`, ma `15≢1 mod 16`, quindi non
esiste un primo antenato intero positivo.

Gli antenati interi positivi che terminano nella binade di `Q_v` sono
esattamente gli interi nell'intervallo reale semiaperto

\[
 I_{v,t}=\left[
 \frac{(1+AdZ_v)^{1/d}-1}{A},
 \frac{(1+2AdZ_v)^{1/d}-1}{A}
 \right).                                             \tag{4}
\]

Per evitare ambiguità sui bordi, siano `L=ceil(inf I)`,
`U=ceil(sup I)−1` e `N=U−L+1`. Gli estremi si possono calcolare mediante
confronti interi con `G`, senza logaritmi o radici in virgola mobile.

Per ogni `w`,

\[
 f_w(x)-f_w(y)=(x-y)\bigl(1+2^{w+2}(x+y)\bigr),
\]

e il secondo fattore è dispari. Quindi `G` è un'isometria 2-adica e una
permutazione modulo `2^h`. Composta con la codifica delle parità, essa
induce ancora una biezione fra residui dell'antenato e parole terminali.
Poiché `[L,U]` contiene interi consecutivi, il numero esatto di parole
terminali distinte di lunghezza `h` è

\[
                     \min(N,2^h).                    \tag{5}
\]

In particolare ogni parola ammette al più un antenato nell'intervallo
esattamente quando `N≤2^h`. Se si restringe agli antenati dispari e `h≥1`,
la formula diventa `min(N_odd,2^(h−1))`, dove `N_odd` conta gli interi
dispari di `[L,U]`; le parole considerate iniziano con un dispari.

Si ha anche un limite elementare utile. Posto `q=Q_u`, la lunghezza reale
di (4) soddisfa

\[
 |I_{v,t}|<(q+1/A)(2^{1/d}-1)\le(q+1/A)/d,
 \qquad N\le\lfloor q/d\rfloor+1.                    \tag{6}
\]

Per la prima disuguaglianza si usa `Z_v≤G(q)` e
`1+2AdZ_v<2(1+AdZ_v)`; per la seconda, la convessità di `2^s` su `[0,1]`.
Se `2^t>Q_u`, l'altezza e i `t` antenati bastano già a isolare `Q_v`,
senza una parola di parità: (6) dà `N≤1` e l'antenato `Q_u` esiste.

## 5. Due antenati bastano per la rigidità del prefisso effettivo

**Proposizione 2.** Sia `v≥5`. Per ogni parola di parità di lunghezza
`H_v`, esiste al più un intero `X` nella binade di `Q_v` che realizza
la parola prescritta e ammette due antenati interi positivi

\[
 X=f_{v-1}(f_{v-2}(x)).
\]

Se la parola prescritta è quella di `Q_v`, necessariamente
`x=Q_(v−2)` e `X=Q_v`.

**Dimostrazione.** Il lemma (2) forza `x` nella binade di `q=Q_(v−2)`.
Posto `M=2^v`, la disuguaglianza `3^3<2^5` dà

\[
 q=\frac{3^{M/2}-1}{2^{v+1}}
 <2^{5M/6-v-1},\qquad
 2q<2^{5M/6-v}<2^{H_v},                              \tag{7}
\]

poiché `589/612>5/6`. Ogni antenato ammissibile è quindi positivo e
minore di `2^H_v`. Una parola terminale fissa una sola classe modulo
`2^H_v` dell'antenato, per l'isometria di `G`; in quell'intervallo ne
esiste al più un rappresentante. Per la parola di `Q_v`, `q` è già
un rappresentante ammissibile. Questo conclude la prova.

Il conteggio (5) rende quantitativa la scarsità: le parole ammissibili
sono `N`, su `2^H_v` parole totali, e (6) dà
`N≤floor(Q_(v−2)/4)+1`. Sono escluse molte parole costruibili con i soli
vincoli locali. Una cardinalità piccola, tuttavia, non controlla il peso
di Hamming dei singoli elementi rimasti.

## 6. Che cosa cambia rispetto agli ostacoli precedenti

Le note su [margine](../post_v6_margin_2026-09-25/RESULTS_IT.md) e
[vincoli misti](../post_v6_mixed_2026-09-25/RESULTS_IT.md) costruivano
punti alternativi con prefisso inferiore corretto, altezza corretta,
ricorrenza quadratica verso il livello successivo e molta precisione
3-adica. Non imponevano due antenati interi positivi.

La Proposizione 2 mostra che questi punti alternativi non possono
soddisfare anche quest'ultima condizione mantenendo il prefisso effettivo
di `Q_v`: diventerebbero `Q_v` stesso. È un filtro aritmetico aggiuntivo
con una prova uniforme, distinto dal trasporto dello stesso vincolo CRT.

La Proposizione 1 delimita però il ruolo di questo filtro. Storie intere
coerenti e potenze pure con esponente libero realizzano tutte le parole
finite; è la combinazione con l'altezza prescritta a rimuovere la libertà.
Non è dimostrato che tale rigidità faciliti il controllo delle parità.

## 7. Verifiche finite e controesempi con antenati

Il [probe](ancestry_probe.py) e i [risultati esatti](ancestry_results.json)
conservano gli interi e le parole in esadecimale. Non è stato calcolato un
nuovo livello della torre oltre quelli già verificati. Gli esperimenti
seguenti sono esplorativi, senza separazione training/holdout.

### Intervalli e soglie del prefisso

Per due antenati, `h_all=ceil(log₂N)` è la soglia dalla quale **tutte** le
parole hanno al più un antenato. La soglia `h_Q`, relativa alla sola
classe di `Q_(v−2)`, può essere più piccola:

\[
 h_Q=\left\lceil\log_2
 \bigl(1+\max(Q_{v-2}-L,U-Q_{v-2})\bigr)\right\rceil.
\]

| `v` | `H_v` | Bit di `Q_(v−2)` | `h_all` | `h_Q` |
|---:|---:|---:|---:|---:|
| 6 | 62 | 44 | 42 | 41 |
| 8 | 247 | 194 | 192 | 191 |
| 10 | 986 | 801 | 799 | 799 |
| 12 | 3943 | 3234 | 3231 | 3231 |

Un calcolo indipendente con radici quarte intere ha confermato gli
intervalli e `h_all`. Nei dodici vecchi esempi misti conservati nel JSON,
nessuno possiede già un primo antenato intero positivo.

### Un antenato non basta, anche conservando tutta la parola

Sono state costruite due catene alternative **dispari** dai livelli
`v−1` a `v+1`, nelle corrette binadi a tutti e tre i livelli. A ogni
livello `w` conservano almeno `e_w/4` cifre ternarie rispetto a `Q_w`.
Al livello `v` conservano l'intera parola effettiva di lunghezza `H_v`.

| `v` | Antenati prima di `v` | Margine inferiore alternativo | Margine superiore alternativo | Margine superiore di `Q_(v+1)` |
|---:|---:|---:|---:|---:|
| 10 | 1 | 29 | −33 | 73 |
| 12 | 1 | 93 | −282 | 87 |

La costruzione parte dall'antenato
`x=Q_(v−1)+2^H_v 3^(e_(v−1)/4)t` e sceglie `t` entro l'intervallo radice
della binade finale. L'inversione 2-adica della catena permette di imporre
rispettivamente `216` e `909` parità dispari consecutive dopo il prefisso
superiore lungo `H_v`; il resto della parola è poi calcolato esattamente.
Il fallimento del bilancio superiore è verificato sull'intera parola:
non viene dedotto soltanto dal tratto imposto.

Questi esempi mostrano che un solo antenato non può sostituire i due
antenati nella Proposizione 2, nemmeno con questi vincoli ternari
aggiuntivi. Non dimostrano un fallimento analogo a ogni livello.

### Più antenati non sostituiscono l'informazione persa sulla parola

Se si conserva soltanto un margine inferiore positivo, al livello
`v=10` esistono anche queste catene alternative dispari:

| Antenati prima di `v` | Livello dell'antenato iniziale `u` | Primo `t` trovato | Margine inferiore | Margine superiore |
|---:|---:|---:|---:|---:|
| 2 | 8 | 4 | 23 | −2 |
| 3 | 7 | 21 | 14 | −21 |
| 4 | 6 | 28 | 29 | −16 |
| 5 | 5 | 16 | 4 | −1 |

La ricerca usa `x=Q_u+2·3^(e_u/4)t`. Il fattore `2` conserva la parità
dispari dell'antenato e dell'intera catena. Sono verificate tutte le
binadi fino a `v+1` e le precisioni ternarie di un quarto dell'esponente.
L'intera parola inferiore **non** coincide con quella di `Q_10`.
Questi quattro esempi non contraddicono la Proposizione 2; mostrano che
il solo segno del margine non può sostituire la sua ipotesi sul prefisso.
Non coprono tutte le profondità o tutti i livelli.

### Un piccolo intervallo esaurito: 911 antenati, poi 12

Per `v=10`, con antenato al livello `u=3` e binade terminale quella di
`Q_11`, l'intervallo intero esatto è `[672594,674416]`. Contiene `911`
antenati dispari. Sono stati enumerati tutti, con questi risultati:

| Condizione | Numero di antenati |
|---|---:|
| Totale dei dispari | 911 |
| Margine inferiore non negativo | 815 |
| Margine superiore negativo | 36 |
| Margine inferiore non negativo e superiore negativo | 33 |

Imponendo anche `x≡Q_3 mod 3^4`, con `Q_3=672605`, restano esattamente
`12` antenati: `672605+162t`, `0≤t≤11`. Tutti hanno margine superiore
positivo; il minimo è `6`. Undici hanno margine inferiore non negativo;
l'altro ha margini `−4→41`. Il filtro elimina dunque tutti i `33`
fallimenti di trasferimento presenti nel campione completo.

Questo è un esito positivo **finito** della combinazione tra storia e
precisione ternaria, non una stima uniforme o una predizione validata
su dati separati. Un replay indipendente, con la formula chiusa
`X=((1+64x)^128−1)/(64·128)` e iterazione elementare di `T`, ha confermato
tutti i conteggi sui `911` antenati e i margini dei dodici superstiti.

### Parametri di potenza pura e riproducibilità

Il JSON conserva inoltre due certificati modulari della Proposizione 1,
ai livelli `v=10,12`: esponenti dispari `k>1` realizzano le vecchie
parole avversarie con margini `29→−426` e `93→−1841`.
Non è necessario costruire le enormi potenze intere: si verificano
`F_v(k) mod 2^H_(v+1)` e `F_(v+1)(k) mod 2^H_(v+1)`.
Queste torri pure hanno esponente diverso da quello prescritto e sono
fuori dalla binade di `Q_v`.

Dalla radice del repository:

```sh
python3 notes/post_v6_ancestry_2026-09-25/ancestry_probe.py --output /tmp/ancestry_replay.json
python3 -m unittest discover -s notes/post_v6_ancestry_2026-09-25 -p 'test_ancestry.py' -v
cmp notes/post_v6_ancestry_2026-09-25/ancestry_results.json /tmp/ancestry_replay.json
```

I test confrontano radici, estremi, inverse, conteggi e parole con
enumerazioni piccole indipendenti. La verifica computazionale è distinta
dalle prove uniformi delle Proposizioni 1 e 2.

Sul commit `77fe96a194ba931a8528f85cb67e68af2df0c6a7` sono passati tutti
i **13 test**, compresi i replay indipendenti delle sei catene e di tutte
le 911 righe. Il
[replay CI 36147736152](https://github.com/PieroBorgatta/Collatz/actions/runs/36147736152)
è riuscito e il file scaricato coincide byte per byte con quello locale.
Anche la
[build Lean e gli audit preesistenti](https://github.com/PieroBorgatta/Collatz/actions/runs/36147736081)
sono passati sullo stesso commit; non formalizzano questa nuova fase.
Le prove e i dati sono stati sottoposti a revisione interna degli agenti,
non a peer review umana esterna. I log compressi e il
[manifest delle verifiche](verification_manifest.json) archiviano l'evidenza.
Il successivo commit aggiunge soltanto documentazione e materiale di verifica;
la nota sulla pista ternaria non introduce una nuova stima dimostrata.

## 8. Il problema sul peso della parola resta aperto

Ponendo `j_v=J_(Q_v)(H_v)`, `m_v=2^(v−1)−j_v` e
`Δ_v=j_(v+1)−2j_v`, si ha esattamente

\[
                       m_{v+1}=2m_v-\Delta_v.         \tag{8}
\]

L'obiettivo sufficiente resta dimostrare
`Δ_v≤2·2^ceil(v/2)` per ogni `v≥16`: con `m_16=1155`, la somma pesata
dei costi futuri è `1024`. Le verifiche precedenti fino a `v=24` restano
finite; la rigidità non estende quell'intervallo e non prova il limite.

Un esempio della difficoltà è l'identità affine per una parola effettiva
di `n` passi, con `j` dispari e costante `C`:

\[
 2^nY=3^jQ_v+C,\qquad
 a_v2^nY=3^{e_v+j}+a_vC-3^j.                         \tag{9}
\]

La costante `C` contiene una somma con `j` termini dipendenti dalla
posizione dei dispari; l'intero terminale `Y` non è necessariamente una
unità rispetto ai primi `{2,3}`. Non si può applicare direttamente un
teorema sulle equazioni in S-unità trattando `Y` come tale, né sostituire
una dimensione crescente con una dimensione fissata. La
[rassegna aritmetica precedente](../post_v6_arithmetic_2026-09-25/LITERATURE_IT.md)
discute i limiti delle stime digitali e p-adiche già esaminate.

Il prossimo lemma utile dovrebbe sfruttare l'intervallo degli antenati e
l'esponente esatto per controllare **il peso o la discrepanza della parola
del punto `Q_v`**, senza assumere già una stima equivalente sulle parità.
L'unicità dell'antenato per ciascuna parola non significa che sia ammessa
una sola parola: il loro numero resta quello di (5).
Identificare il punto è un progresso nella selezione dei candidati;
stimare la sua orbita è ancora il passaggio mancante.

La [pista ternaria successiva](NEXT_RESEARCH_IT.md) formula questo problema
come controllo del difetto prodotto dal raddoppio della parola ternaria
di `3^m−1`. La nota distingue l'identità esatta da una stima ancora assente
e mostra perché non è giustificato supporre che i riporti perdano memoria
entro un numero costante di cifre.
