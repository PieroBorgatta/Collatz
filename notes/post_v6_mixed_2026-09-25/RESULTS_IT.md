# Vincoli binari e ternari: trasporto, altezza e controesempi

25 settembre 2026 — continuazione post-v6, separata dagli artefatti pubblicati.

La combinazione delle congruenze introduce informazione aritmetica reale,
ma il suo trasporto affine non produce una nuova stima sulle parità. Inoltre,
un quarto della precisione ternaria della torre è compatibile, a ogni livello
v≥6, con esempi generici aventi margine inferiore positivo e superiore
negativo. È un limite delle informazioni troncate considerate qui, non
un'impossibilità per altri metodi misti e non un controesempio della torre.

La [sintesi per una revisione specialistica](SCIENTIFIC_BRIEF_IT.md) presenta
il problema aperto e distingue formalizzazione, prove su carta e calcoli.
Nessun documento è stato inviato a terzi. L'originalità matematica di questi
argomenti non è accertata; in questa fase non aggiungiamo dichiarazioni Lean.

## 1. Notazione e domanda verificabile

Usiamo T(x)=x/2 sui pari e T(x)=(3x+1)/2 sui dispari. Poniamo

\[
M=2^v,\quad e=2M,\quad a=2^{v+3},\quad
Q=Q_v=\frac{3^e-1}{a},\quad
H=\left\lceil\frac{589M}{612}\right\rceil,\quad K=H_{v+1}.
\]

Sia Z=2^{⌊log₂Q⌋}; la binade [Z,2Z) è la fascia degli interi con la
stessa lunghezza binaria di Q. La ricorrenza è

\[
Q_{v+1}=f_v(Q_v),\qquad f_v(X)=X+\frac a2X^2.
\tag{1}
\]

L'obiettivo aperto della [fase precedente](../post_v6_margin_2026-09-25/RESULTS_IT.md)
è controllare Δ_v=J_{Q_{v+1}}(K)−2J_Q(H). La maggiorazione

\[
\Delta_v\le2\cdot2^{\lceil v/2\rceil}\quad(v\ge16)
\tag{2}
\]

sarebbe sufficiente a propagare il margine nonnegativo, con base m₁₆=1155
e costo futuro 1024. È una candidata retrospettiva, non un risultato.
Qui chiediamo se i vincoli modulo potenze di 2 e di 3, insieme all'altezza,
forniscano una stima nuova del tipo (2).

## 2. Trasporto esatto della congruenza ternaria

Fissiamo una parola di parità di lunghezza n con j passi dispari. La sua
costante affine C soddisfa, per ogni X che la realizza,

\[
2^nY=3^jX+C,\qquad Y=T^n(X).
\]

Moltiplicando per a si ottiene

\[
a2^nY-aC+3^j=3^j(aX+1).
\tag{3}
\]

Per s≥0, essendo a e 2 invertibili modulo 3^{s+j}, segue l'equivalenza

\[
aX+1\equiv0\pmod{3^s}
\quad\Longleftrightarrow\quad
Y\equiv2^{-n}(C-a^{-1}3^j)\pmod{3^{s+j}}.
\tag{4}
\]

La congruenza ternaria aggiunge un vincolo rispetto alla sola parola
binaria. Tuttavia le j cifre apparentemente guadagnate in (4) non sono
informazione indipendente: l'intervallo iniziale di ampiezza Z diventa
un intervallo di ampiezza 3^jZ/2^n. Esattamente,

\[
\frac{3^{s+j}}{3^jZ/2^n}=\frac{2^n3^s}{Z}.
\tag{5}
\]

Non è soltanto un confronto di ampiezze. Esiste una biezione fra i candidati
iniziali nella classe CRT modulo 2^n3^s entro [Z,2Z) e gli interi Y nella
classe (4) entro

\[
\left[\frac{3^jZ+C}{2^n},\frac{2\cdot3^jZ+C}{2^n}\right).
\]

Infatti (4) implica 2^nY−C≡0 modulo 3^j, quindi
X=(2^nY−C)/3^j è intero. Modulo 2^n, questo X appartiene alla classe
−C(3^j)^{-1}, che realizza esattamente la parola prescritta. L'altezza e
la congruenza ternaria tornano a quelle iniziali. Trasportare la medesima
condizione non elimina altri candidati.

Per il punto speciale X=Q, (3) diventa

\[
a2^nY=3^{e+j}+aC-3^j.
\tag{6}
\]

Si ritrova la rappresentazione 3^E+c della
[nota aritmetica](../post_v6_arithmetic_2026-09-25/RESULTS_IT.md),
con E=e+j e c=aC−3^j. Non abbiamo ottenuto un nuovo controllo di C o di j.

## 3. Il raddoppio ternario appartiene alla ricorrenza generica

Un'identità valida per ogni X è

\[
1+2a f_v(X)=(1+aX)^2.
\tag{7}
\]

Quindi ν₃(1+2a f_v(X))=2ν₃(1+aX) per ogni intero positivo X.
Non occorre che X sia Q. Se X=Q+3^s t, 0≤s<e e 3∤t,

\[
f_v(X)-Q_{v+1}=3^{2s}t\left(3^{e-s}+\frac a2t\right),
\tag{8}
\]

il cui ultimo fattore è un'unità modulo 3. La precisione della differenza
raddoppia esattamente: ν₃(f_v(X)−Q_{v+1})=2s. Anche e raddoppia, perciò
la frazione s/e resta invariata. Più in generale, se s≤e e X≡Q modulo
3^s, allora f_v(X)≡Q_{v+1} modulo 3^{2s}. Non estendiamo questa ultima
asserzione a s>e: se ν₃(X−Q)=s>e, la valutazione superiore è e+s.

La normalizzazione z_v=1+a_vX_v riduce la ricorrenza a z_{v+1}=z_v².
Scrivendo z_v=3^s u con 3∤u, il cofattore diventa u². La torre ha u=1;
conservare una quota della valutazione ternaria non impone questa purezza.

## 4. Un quarto della precisione completa non elimina le code avversarie

Fissiamo una classe avversaria r modulo 2^K. Aggiungiamo

\[
X\equiv r\pmod{2^K},\qquad X\equiv Q\pmod{3^s},\qquad 0\le s\le e.
\tag{9}
\]

La seconda condizione equivale ad aX+1≡0 modulo 3^s. Il teorema cinese
dei resti dà una classe modulo P=2^K3^s. Quando P≤Z, **ogni** classe
binaria r ha ancora un rappresentante entro [Z,2Z).

**Proposizione.** Per ogni v≥6 e s=M/2=e/4, si ha P<Z.

**Prova.** K≤2M e 9^M−1≥8^M danno Z≥2^{3M−v−3}. Inoltre
M≥6v+18 per v≥6: vale alla base 64≥54 e si conserva raddoppiando M
e incrementando v. Da 3³<2⁵ segue

\[
P^6=2^{6K}3^{3M}<2^{12M+5M}=2^{17M}
\le2^{18M-6v-18}\le Z^6.
\tag{10}
\]

Questo prova l'asserzione senza usare approssimazioni logaritmiche. □

Per collegarla ai margini, ricordiamo il seguente argomento della nota
precedente. La differenza

\[
f_v(X)-f_v(W)=(X-W)\left(1+2^{v+2}(X+W)\right)
\]

ha la stessa valutazione binaria di X−W. La funzione f_v permuta quindi
le classi modulo ogni potenza di 2. Fissato X≡1 modulo 2^H, il conteggio
inferiore è ⌈H/2⌉<M/2; ogni coda superiore di K−H parità è realizzabile
tramite un opportuno lift r modulo 2^K.

Il prefisso superiore coincide con quello di n₀=1+2^{v+2}. Se contiene
j dispari, 1≤T^H(n₀)≤2^{2j−H}n₀ implica
j≥⌈(H−v−2)/2⌉, perché 2^{v+2}<n₀<2^{v+3}. Scegliendo la coda
tutta dispari e usando K≥2H−1, otteniamo

\[
J_{f_v(X)}(K)\ge\frac{3H-v-4}{2}>M,
\quad
J_{f_v(X)}(K)-2J_X(H)\ge\frac{H-v-6}{2}.
\tag{11}
\]

Qui H≤M−2, H≥3M/4 e M/4>v+4 per v≥6 giustificano i confronti.
La scelta CRT (9) conserva entrambe le parole e dunque tutti questi
conteggi, aggiungendo s=e/4 cifre ternarie e l'altezza della torre.

Ne segue un ostacolo uniforme alle stime o(2^v) dedotte dalle sole
ipotesi generiche (1), (9), altezza e margine inferiore positivo. Questa
costruzione uniforme usa il prefisso di 1. Non afferma che si possa
conservare a ogni livello il prefisso effettivo di Q con margine positivo.
Produce una coppia locale per ciascun livello; non dimostra che tutte queste
coppie appartengano a una medesima torre alternativa originata a un livello
fisso. Un invariante che imponga ulteriore storia aritmetica non è escluso
da questo argomento.

### Costruzione esatta e bit alti conservati

Poniamo

\[
t\equiv(Q-r)(2^K)^{-1}\pmod{3^s},\quad 0\le t<3^s,
\quad r_s=r+2^Kt.
\]

Con R=⌈log₂P⌉ e A=2^R⌊Q/2^R⌋, scegliamo

\[
X=A+((r_s-A)\bmod P).
\tag{12}
\]

Poiché P≤2^R≤Z, abbiamo A≤X<A+2^R entro la binade. Tutti i bit
nelle posizioni ≥R coincidono con quelli di Q e |X−Q|<2^R.
Non sono conservati in generale tutti i bit ≥K: R è maggiore di K
quando s>0. La fascia d'altezza superiore è soltanto comparabile:
1/4<f_v(X)/Q_{v+1}<4; non imponiamo la medesima binade superiore.

## 5. Dodici esempi e due soglie diverse

Il programma parte dalle sei classi avversarie archiviate nella fase sui
margini e costruisce per ciascuna due rappresentanti: a s=e/4 e all'ultimo
s per cui 2^K3^s≤Z. I nuovi esempi con prefisso inferiore effettivo sono:

| v | s=e/4 | Bit alti conservati | Margine inferiore | Margine superiore |
|---:|---:|---:|---:|---:|
| 8 | 128 | 105 | +8 | −120 |
| 10 | 512 | 450 | +29 | −426 |
| 12 | 2048 | 1838 | +93 | −1841 |

Per gli ultimi due, |X−Q|/Q è inferiore rispettivamente a 2^{-449} e
2^{-1837}. Restano comunque interi diversi da Q. Il margine negativo
segnala il fallimento di quel certificato superiore, non la mancata
convergenza dell'orbita.

Quanto alla classe inferiore effettiva, per 0≤s≤e i vincoli
X≡Q modulo 2^H e aX+1≡0 modulo 3^s equivalgono a
X≡Q modulo N=2^H3^s. Il numero esatto di candidati nella binade è

\[
1+\left\lfloor\frac{Q-Z}{N}\right\rfloor
 +\left\lfloor\frac{2Z-1-Q}{N}\right\rfloor.
\tag{13}
\]

L'unicità equivale precisamente a

\[
N\ge U:=\max(Q-Z+1,\ 2Z-Q).
\tag{14}
\]

Definiamo s_bad=max{s:2^K3^s≤Z} e s_iso=min{s:2^H3^s≥U}.
La prima è una soglia **sufficiente** a garantire tutti i lift avversari;
la seconda è la soglia **esatta** che isola Q nella cella inferiore.

| v | Precisione completa e | s_bad | s_iso | Candidati a s_iso−1 | A s_iso |
|---:|---:|---:|---:|---:|---:|
| 6 | 128 | 43 | 83 | 2 | 1 |
| 8 | 512 | 193 | 349 | 3 | 1 |
| 10 | 2048 | 795 | 1418 | 3 | 1 |
| 12 | 8192 | 3207 | 5695 | 3 | 1 |

Fra le soglie non dimostriamo né presenza né assenza generale di code
avversarie. Superare una garanzia sufficiente non dimostra l'esclusione.
Inoltre s<e non significa necessariamente molti candidati: già s=e−1
isola Q nella binade, poiché 3^{e−1}=(aQ+1)/3>Q per v≥5.
Identificare esattamente Q non controlla ancora la sua orbita.

## 6. Confronto con le fonti primarie

In [Tao, versione arXiv v7 del 16 luglio 2026](https://arxiv.org/html/1909.03562v7),
il lemma 5.3 combina esplicitamente classi binarie e ternarie via CRT;
la dimostrazione del risultato principale usa distribuzioni su gruppi
3-adici. Il teorema 1.3 riguarda quasi tutti gli interi in densità
logaritmica. Non dà una stima puntuale sulla presente torre. L'uso congiunto
dei due primi non è una nuova idea in sé.

[Stérin–Woods, versione v4 del 27 febbraio 2022](https://arxiv.org/abs/2007.06979v4)
costruiscono un automa che simula Collatz in base 2 lungo le righe e in
base 3 lungo le colonne, incorporando una conversione ternario-binaria.
Questo è un precedente specifico per l'approccio a due basi. I loro
risultati di complessità non dimostrano l'impossibilità di una stima sulle
nostre parità.

Il [precedente esame della letteratura](../post_v6_arithmetic_2026-09-25/LITERATURE_IT.md)
discute separatamente i risultati digitali e p-adici fino al 2026.
La verifica attuale delle fonti primarie non fornisce un ponte dalla
purezza 3^e alla maggiorazione (2). Gli argomenti dei §§2–5 sono deduzioni
del progetto, non teoremi attribuiti alle fonti appena citate.

## 7. Riproduzione e stato della verifica

Dalla radice del repository:

```bash
python3 notes/post_v6_mixed_2026-09-25/test_mixed.py
python3 notes/post_v6_mixed_2026-09-25/mixed_probe.py --output /tmp/mixed/mixed_results.json
cmp notes/post_v6_mixed_2026-09-25/mixed_results.json /tmp/mixed/mixed_results.json
```

Il file [mixed_results.json](mixed_results.json) conserva gli interi X,Y
in esadecimale, le parole complete, i moduli CRT, le valutazioni ternarie,
il trasporto affine e le soglie. I test enumerano piccoli casi e confrontano
i dodici esempi con T elementare. Il replay CI ripete lo stesso programma;
non costituisce un'altra implementazione indipendente. Nessun nuovo livello
della torre è stato calcolato e le verifiche finite non sostituiscono le
prove su carta dei risultati uniformi. Il nucleo Lean preesistente non
formalizza questa fase.

Verifica completata sul commit `9f866ba94d3071783ec40f136ba80a580c700294`:
**14 test superati**, revisione matematica interna di due agenti e controllo
indipendente degli esempi con iterazione elementare. Il
[replay CI 36145117577](https://github.com/PieroBorgatta/Collatz/actions/runs/36145117577)
è riuscito; il risultato scaricato coincide byte per byte con quello locale.
Anche la
[build Lean e gli audit preesistenti](https://github.com/PieroBorgatta/Collatz/actions/runs/36145117197)
sono riusciti sul medesimo commit. I PDF pubblicati v1–v6, l'archivio v6 e
gli artefatti storici verificati sono invariati. I log compressi e il
[manifest delle verifiche](verification_manifest.json) archiviano l'evidenza;
il successivo commit modifica soltanto documentazione e materiale di verifica.
Questa revisione interna non è una peer review umana esterna.

Il prossimo obiettivo matematico resta una stima puntuale che usi il
cofattore esatto u=1 in (7), o controlli direttamente la somma pesata degli
errori Δ_v. Una proposta utile deve distinguere Q dagli esempi (12) e
produrre una disuguaglianza dinamica; l'aggiunta o il trasporto delle stesse
congruenze non assolve questo compito.
