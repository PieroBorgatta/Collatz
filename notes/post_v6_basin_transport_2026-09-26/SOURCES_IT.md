# Trasporto fra bacini: fonti pertinenti e costo di un confronto esatto

26 settembre 2026. Ricerca circoscritta alla disuguaglianza H del [programma sui bacini](../post_v6_reset_2026-09-26/NEW_DIRECTION_IT.md), non nuova rassegna generale. Non sono stati modificati altri file né riprodotti build esterni. I lemmi aritmetici sotto sono controlli autonomi su carta, senza rivendicazione di priorità; le piccole verifiche intere servono soltanto a controllare le formule.

**Esito.** Le fonti consultate non forniscono il rapporto relativo richiesto da H. Forniscono però oggetti precisi per studiarlo. Esiste un trasporto esatto ottenuto cambiando l'ultimo esponente della parola inversa: ne dimostriamo il costo e una famiglia nella quale il costo resta grande anche ammettendo correzioni negative. Non si ottiene così un confronto puntuale a costo uniforme. Il limite asintotico della variante nonnegativa è dimostrato separatamente in [OBSTRUCTIONS_IT.md](OBSTRUCTIONS_IT.md); le sole perdite puntuali della variante firmata non escludono ogni possibile ulteriore confronto pesato. H non è confutata.

## 1. Che cosa danno effettivamente le fonti

| Fonte primaria consultata | Meccanismo utilizzabile | Uniformità che manca per H |
|---|---|---|
| [Krasikov–Lagarias, *Acta Arithmetica* 109 (2003), §§2–3](https://arxiv.org/pdf/math/0205002) | Per il conteggio con altezza limitata `π*_a`, definiscono `φ_k^m(t)=inf_{a≡m mod3^k, a non ciclico} π*_a(2^t a)`. La Proposizione 2.1 dà ricorrenze con classi ternarie e minimo sui tre sollevamenti; un certificato positivo produce `φ_k^m(t)≥Δ c_m λ^t`. | Sono limiti inferiori a ciascun albero, non confronti fra i conteggi effettivi di due alberi. Con `λ<2`, dividere per il cutoff dà zero nel limite. Far tendere il livello `k` all'infinito richiede controllo simultaneo di coefficienti e soglie. Due limiti inferiori non danno il rapporto H. |
| [Wirsching, *DCDS* 9 (2003), 771–787](https://doi.org/10.3934/dcds.2003.9.771), testo originale letto | Le funzioni di conteggio `e_ℓ(k,a)` e i generatori `g_ℓ(k,a)` conservano la coordinata `a∈Z₃×`. Gli operatori `S_ℓ` convergono fortemente a un operatore che **media** quella coordinata; la componente reale è `W₃f(x)=(3/2)∫[3x−2,3x]f(t)dt`. | Il Teorema 3 controlla famiglie limitate equicontinue. Non autorizza l'applicazione uniforme ai generatori con risoluzione crescente. La Congettura 2, a p. 784, è precisamente il ponte verso il limite inferiore puntuale `(*3)`, ancora congetturale nel testo. Anche la conclusione perseguita `d_*(a)≥c/a` è assoluta, non relativa. |
| [Tavares, arXiv:2608.27617v1, §§3, 11–12](https://arxiv.org/html/2608.27617v1), 27 agosto 2026, preprint | Dichiara provate le Congetture 1 e 3 di Wirsching, lasciando aperto `(*3)`. Esplicita che il rapporto per `W₃` non contiene informazione sui residui. Distingue una costante uniforme in `a` dalla soglia eventuale, che può dipendere da `a`. | Non è una prova del confronto dei generatori a due target. Il suo trasferimento `g_ℓ→e_ℓ` conserva un limite inferiore già assunto: non lo crea. Consultati i passaggi pertinenti e confrontati con Wirsching; non revisionata integralmente la nuova prova. |
| [Mazur, *Positive Lower Density of Collatz Predecessors*, v1, §§2–4](https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/paper-v1.pdf), 6 settembre 2026 | La Proposizione 3.1 fornisce parole inverse pesate per un seed `R` in un residuo prescritto. Il peso è `ω=3^d/2^A`; la rimozione del peso ternario usa `ω x≤R` e un censimento in classi. La costante finale è `3/(256R·3^m)`. | La massa pesata è assoluta. Non è un confronto tra la massa selezionata per `n` e quella per `h(n)`. La perdita dipendente dal seed nel passaggio ai conteggi rimane essenziale; il buon comportamento medio delle funzioni residue non rende costanti i loro valori sui percorsi. |
| [Sharpe, `klbound.tex`, pin `ec8174b…`](https://github.com/msharpe248/collatz/blob/ec8174b567d5cab4960024782210b5f5db02bd3a/paper/klbound.tex) e [implementazione Krasikov](https://github.com/msharpe248/collatz/blob/ec8174b567d5cab4960024782210b5f5db02bd3a/lean/Collatz/Krasikov.lean) | Certificati più grandi nello stesso programma di disuguaglianze. Il paper scrive esplicitamente `π_a(x)≥x^0.895` per `x≥x₀(a)`; il codice distingue infimi di classe e conteggi a una radice. | Nessun limite superiore sul bacino di `n`, quindi nessun rapporto relativo. Le note di [trasporto affine](https://github.com/msharpe248/collatz/blob/ec8174b567d5cab4960024782210b5f5db02bd3a/paper/affine_transfer.tex) riguardano invece trasferimenti di convergenza equivalenti a problemi globali: non costituiscono un Harnack sui conteggi. Non eseguito un replay del repository. |

La vicinanza reale dei siblings non è vicinanza ternaria: per le due scelte di `h`,

`h(n)−n=3n+1` oppure `5(3n+1)`, dunque `ν₃(h(n)−n)=0`.

Una stima locale di continuità nella coordinata 3-adica non confronta quindi questi due target come punti vicini.

## 2. Uniformità già disponibile: non perdere l'ottimizzazione locale

Nel dominio di H il target `n` è già senza ritorni positivi. Ogni suo predecessore è allora senza ritorni: un predecessore periodico avrebbe una coda periodica contenente `n`. Questo elimina, **in questo dominio**, la scelta esistenziale di un bound sui cicli menzionata nella Remark 4.3 di Mazur.

La famiglia elementare del suo Lemma 2.3 è

\[
R_j=\frac{2^e n4^j-1}{3},\qquad
e=2\ (n\equiv1\bmod3),\quad e=1\ (n\equiv2\bmod3).
\]

I `3^q` indici di un blocco completo coprono tutti i residui modulo `3^q`. Per `n≥B₀`, scegliendo `1≤j≤3^q`, il seed prescritto soddisfa `n<R_j≤K n`, con `K=4^(3^q+1)` sufficiente e indipendente da `n`. Non serve decidere se esistano cicli ignoti. Questa osservazione riordina i quantificatori; non migliora da sola il rapporto dei bacini.

**Lo stato del progetto è già più avanzato della scelta numerica del manoscritto.** Sono stati letti il [README dell'overlay](../../research/weighted_predecessors_adapter/README.md), il [resoconto dell'ottimizzazione](../post_v6_optimization_2026-09-24/RESULTS_IT.md) e il relativo [audit semantico](../post_v6_optimization_2026-09-24/SEMANTIC_AUDIT_IT.md). L'overlay conserva il decadimento alla sesta potenza e sceglie il minimo `m≥1` con

\[
88TC\le m^6,\qquad c=\frac3{256T3^m}.
\]

Se `T≤K n`, questo coefficiente ha un limite inferiore della forma

\[
c\ge \frac{c_0}{n}\exp(-C_0 n^{1/6}),
\]

per costanti positive indipendenti dal target nel dominio considerato. Infatti `m≤1+(88KCn)^(1/6)`. La dipendenza è un'esponenziale negativa in una radice dell'altezza, non il costo logaritmico relativo di H. Il risultato è subordinato agli stessi input analitici esterni dell'overlay; il replay e gli audit locali documentati non vengono qui né ripetuti né sostituiti da una revisione matematica indipendente.

Anche un futuro limite assoluto `c/n` non basterebbe: per ottenere H occorre un confronto con **il vero `d_*(n)`**, che può essere molto maggiore del limite inferiore disponibile.

## 3. Un trasporto esatto cambiando l'ultimo esponente

Siano `n,y` positivi dispari non divisibili per 3, con `y>n`. Una parola esatta in ordine forward `w=(a₁,…,a_k)`, `k≥1`, porta `u` a `n`. Scriviamo

\[
A=\sum_{i=1}^k a_i,\quad A_j=\sum_{i=1}^j a_i,\quad A_0=0,\qquad
C=\sum_{j=0}^{k-1}3^{k-1-j}2^{A_j}.
\]

Allora `3^k u+C=2^A n`, e **C non dipende dall'ultimo esponente `a_k`**.

**Lemma del trasporto.** Sia `δ∈Z` tale che

\[
a_k+\delta\ge1,\qquad 2^\delta y\equiv n\pmod{3^k}.
\]

Per `δ<0` la congruenza usa l'inverso di 2 modulo `3^k`. La parola

`w'=(a₁,…,a_(k−1),a_k+δ)`

è esatta da un intero positivo dispari `u'` a `y`, dove

\[
u'=\frac{2^{A+\delta}y-C}{3^k}
   =u+\frac{2^A(2^\delta y-n)}{3^k}.
\tag{1}
\]

**Prova.** `A+δ≥1`, e la congruenza rende intero il primo quoziente in (1). La congruenza modulo 3 del numeratore, dopo aver cancellato la potenza di 2 del prefisso, impone `2^(a_k+δ)y≡1 mod3`. Il primo passo inverso `(2^(a_k+δ)y−1)/3` è quindi intero. Dividendo la congruenza completa per 3 si ripete l'argomento per il passo precedente, fino alla sorgente. Ogni passo inverso ha esponente positivo: da un intero positivo dispari produce, quando è intero, un intero ancora positivo dispari. Questo prova simultaneamente l'integrità degli stati e le valutazioni esatte. Non è necessario assumere separatamente `u'>0`. □

Per una famiglia di parole di lunghezza k, **con lo stesso δ fissato per tutte le parole**, il trasporto è iniettivo: modificare l'ultimo esponente è invertibile sulle parole e una sorgente determina un'unica parola di lunghezza k. Se si sceglie un δ fisso per ciascuna profondità, l'assenza di ritorni del target `y` impedisce inoltre rappresentazioni multiple della stessa sorgente attraverso lunghezze diverse. Queste affermazioni di iniettività **non** valgono per l'ottimizzazione parola per parola descritta sotto.

Il costo pesato è esatto:

\[
\omega(w')=2^{-\delta}\omega(w),\qquad \omega(w)=3^k2^{-A}.
\tag{2}
\]

Le correzioni negative non vanno scartate. Posto `L_k=2·3^(k−1)` e scelto il rappresentante `δ₀∈[0,L_k)` della congruenza, la modifica di costo minimo nell'insieme ammesso è

\[
\delta_{\min}=\delta_0+L_k
\left\lceil\frac{1-a_k-\delta_0}{L_k}\right\rceil.
\tag{3}
\]

L'esistenza e l'unicità modulo `L_k` seguono dall'ordine di 2 modulo `3^k`, che si ottiene da `ν₃(4^t−1)=1+ν₃(t)`.

**Fibre dell'ottimizzazione firmata.** Fissati il prefisso di lunghezza `k−1` e il target n, gli ultimi esponenti ammissibili sono `a=a₀+jL_k`, `j≥0`, con `1≤a₀≤L_k`. La scelta (3) li manda tutti nello stesso ultimo esponente `b∈[1,L_k]` per y: `δ_min=b−a`. Sorgenti distinte vengono quindi identificate. Esempio esatto: per `n=17`, `y=277`, `k=2`, le parole `(1,1)` e `(1,7)`, con sorgenti rispettivamente 7 e 483, sono entrambe mandate alla parola `(1,6)`, con sorgente 3939. L'assenza di ritorni di y non elimina una collisione fra parole diventate identiche.

Resta un controllo **pesato** della fibra. Posto `ω₀=3^k2^(−A_prefix−a₀)`, i pesi originali sono `ω_j=ω₀2^(−jL_k)`, dunque

\[
\sum_{j\ge0}\omega_j=\frac{\omega_0}{1-2^{-L_k}}\le\frac43\omega_0,
\qquad
\frac{\sum_{j\ge0}\omega_j}{\omega_{\mathrm{output}}}
=\frac{2^{b-a_0}}{1-2^{-L_k}}.
\tag{3a}
\]

Non si possono contare come distinte le sorgenti trasformate, ma la somma dei pesi entranti ha una maggiorazione esatta. Nella famiglia del §4 si avrà `a₀=1`, `b=L_k`: rispetto al peso d'uscita il fattore resta esponenzialmente grande. Il controllo della fibra non rimuove quella perdita.

**Un limite rigoroso dello schema nonnegativo.** Se `δ≥0`, il numero

`q=(2^δ y−n)/3^k`

è un intero positivo; quindi `u'≥u+2^A`. Poiché `C>0`, segue

\[
n u'>(n+3^k)u.
\tag{4}
\]

Per un target fissato, non esiste dunque una dilatazione universale del cutoff per questo schema, indipendente dalla profondità. L'ostacolo riguarda il trasporto specifico, non qualsiasi possibile accoppiamento.

## 4. Una famiglia che conserva l'ostacolo anche ammettendo δ negativi

Per `k≥1`, scegliamo il minimo rappresentante positivo **dispari**

\[
n_k\equiv-5\cdot14^{-1}\pmod{3^k},\qquad 0<n_k<2\cdot3^k,
\qquad y_k=16n_k+5.
\]

Si ha `n_k≡2 mod3`. Inoltre `y_k≡2n_k mod3^k`, perché `y_k−2n_k=14n_k+5`. La congruenza necessaria è allora

\[
2^\delta y_k\equiv n_k\pmod{3^k}
\iff \delta\equiv-1\pmod{L_k}.
\tag{5}
\]

Esistono parole esatte di lunghezza k che terminano in `n_k` con **ultimo esponente 1**. Il primo stato inverso è

\[
z_k=\frac{2n_k-1}{3}.
\]

È positivo dispari. Per `k≥2`, la congruenza `14n_k+5≡0 mod3^k` dà

`7z_k+4=(14n_k+5)/3≡0 mod3^(k−1)`,

quindi `z_k≡−4/7 mod3^(k−1)` è un'unità ternaria. Da qualsiasi unità positiva dispari si può prolungare l'albero inverso arbitrariamente mantenendo tutte le radici unità: fra i tre esponenti della parità corretta in un periodo modulo 6, due danno un predecessore non divisibile per 3. Ogni passo resta positivo dispari. Si ottengono così gli altri `k−1` passi. Per `k=1` non serve la proprietà di unità di `z_k`.

Poiché `a_k=1`, la condizione `a_k+δ≥1` forza `δ≥0`: **il rappresentante −1 è vietato**. Da (5), la modifica minima ammessa è

\[
\delta_{\min}=L_k-1=2\cdot3^{k-1}-1,
\qquad \omega(w')/\omega(w)=2^{-(L_k-1)}.
\tag{6}
\]

Questa è una famiglia esatta di perdite esponenziali nel periodo ternario, non una statistica sulle parole. I rappresentanti verificati sono:

| k | n_k | y_k | z_k | L_k | δ_min | Rapporto dei pesi |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 5 | 85 | 3 | 2 | 1 | 2^−1 |
| 2 | 17 | 277 | 11 | 6 | 5 | 2^−5 |
| 3 | 17 | 277 | 11 | 18 | 17 | 2^−17 |
| 4 | 17 | 277 | 11 | 54 | 53 | 2^−53 |
| 5 | 17 | 277 | 11 | 162 | 161 | 2^−161 |
| 6 | 989 | 15829 | 659 | 486 | 485 | 2^−485 |
| 7 | 3905 | 62485 | 2603 | 1458 | 1457 | 2^−1457 |

Il confronto con l'altezza non richiede monotonia stretta dei rappresentanti: `14n_k+5` è un multiplo positivo di `3^k`, dunque `(3^k−5)/14≤n_k<2·3^k`. In particolare `n_k→∞`, e

`δ_min≥n_k/3−1`, quindi `ω(w')/ω(w)≤2^(1−n_k/3)`.

Non è un limite superiore sul **rapporto dei bacini**. È il costo di questo accoppiamento, anche dopo l'ottimizzazione firmata (3). Altri percorsi verso `y_k` possono contribuire massa che l'accoppiamento ignora. La costruzione aritmetica non assume noReturn; quando serve iniettività fra lunghezze, tale ipotesi va aggiunta e verificata separatamente.

Più generalmente, per un target n e un ultimo esponente `a_k=a` fissati, i rappresentanti minimi ammessi della congruenza sono non decrescenti al crescere di k. Se fossero limitati, sarebbero infine costanti e si avrebbe l'uguaglianza razionale `2^δh(n)=n`. Questa è impossibile: nel caso `h=4n+1` imporrebbe `n|1`, e nel caso `h=16n+5` imporrebbe `n|5`; i candidati non hanno rapporto pari a una potenza di 2. Quindi anche a target fissato il costo del cambiamento dell'ultimo esponente non è uniformemente limitato sulla profondità, nelle sottoclassi dove quell'ultimo esponente rimane fissato.

Questo ultimo ostacolo si trova già **nel dominio senza ritorni di H**: `17→13→5→1` e `277→13→5→1` sotto S. Per n=17 l'ultimo esponente 1 parte da 11, un'unità ternaria, quindi si possono costruire parole di ogni profondità con quel medesimo ultimo esponente. Il costo minimo cresce senza limite e (4) impone dilatazione maggiore di `1+3^k/17`. Non occorre stabilire noReturn per tutta la famiglia variabile `n_k` per ottenere questo ostacolo allo schema.

## 5. Quale uniformità dovrebbe avere un meccanismo migliore

Non si può recuperare densità positiva usando soltanto una profondità limitata. Se `u≤X`, allora `S^i(u)≤2^iX`; ciascuna valutazione nei primi K passi è al più `log₂X+K+2`. A target fissato, ogni parola determina al più una sorgente dispari; i sollevamenti ordinari aggiungono al più `1+log₂X` scelte. Per K fissato, gli inizi che raggiungono il target in al più K passi dispari sono dunque `O_K((1+log X)^(K+1))`, di densità zero. Occorre confrontare profondità crescenti con il cutoff.

Il prossimo lemma utile deve quindi controllare, contemporaneamente:

1. modifica di **più** esponenti o di blocchi interi, per evitare il periodo esponenziale imposto a un solo esponente;
2. dilatazione reale della sorgente, molteplicità e peso delle parole trasferite;
3. una quota sufficiente della massa effettiva di `B(n)`, non soltanto un limite inferiore assoluto su `B(h(n))`;
4. perdita totale uniforme nella profondità, eventualmente dopo una somma pesata, e al più logaritmica nell'altezza del target.

Il quarto punto non segue dalla sola convergenza forte di operatori. Come controllo elementare del quantificatore: su `C(Z₃)`, le medie `E_ℓ` sui cilindri modulo `3^ℓ` convergono uniformemente all'identità per ogni funzione continua fissata; ma per `f_ℓ=1_[0 mod3^(ℓ+1)]` si ha `‖E_ℓf_ℓ−f_ℓ‖∞=2/3`. È un esempio generale, non un controesempio agli operatori di Wirsching: mostra quale ulteriore uniformità si dovrebbe dimostrare prima di applicare un limite a generatori sempre più fini.

## 6. Provenienza e verifiche

- Wirsching: recuperato il PDF originale tramite l'[endpoint PDF dell'editore](https://www.aimsciences.org/data/article/export-pdf?id=d61ef5bc-8c00-43d0-8b51-425b9c0ed07b), estratto in memoria; letti Definizione 1, Teoremi 1–3, operatori e Congettura 2. Il vecchio URL statico restituiva 404.
- Krasikov–Lagarias: lette definizioni, Proposizione 2.1 e impostazione dei certificati dal PDF arXiv; il PDF sul sito di Lagarias aveva testo estratto non leggibile.
- Tavares: letti i passaggi sul residuo e sui quantificatori, non ripetuti i calcoli assistiti; pin del repository `7afd2598742e0f62322db1ec28222b1bae460f1b`.
- Mazur e overlay: verificati gli enunciati pertinenti e le formule dei costi; nessun nuovo replay o nuova certificazione della parte analitica.
- Sharpe: letti sorgenti TeX e porzioni Lean pertinenti al pin `ec8174b567d5cab4960024782210b5f5db02bd3a`; nessun confronto relativo dei bacini identificato in questi file.
- Verifiche intere autonome: famiglia (5)–(6) per `k=1,…,7`; costruzione di una parola esatta a ogni livello, sua modifica e replay delle valutazioni; disuguaglianza (4). Verificata anche, fino a `k=6`, la bijettività fra residui `n≡1` o `2 mod3` e i rappresentanti **dispari** di δ nel periodo. Un controllo aggiuntivo ha verificato 704 trasporti firmati, inclusi 340 casi con δ negativo; l'esempio di collisione è verificabile con le tre identità `9·7+5=4·17`, `9·483+5=256·17`, `9·3939+5=128·277`. Nessuna estrapolazione numerica usata nelle prove.

Il risultato di questa verifica è circoscritto: un trasporto semplice esiste, ma il suo costo rigoroso è incompatibile con la stima cercata. Le fonti indicano che il passo successivo deve conservare la coordinata ternaria nel confronto di massa; sostituirla con la sua media lascerebbe aperto proprio il problema che H intende risolvere.
