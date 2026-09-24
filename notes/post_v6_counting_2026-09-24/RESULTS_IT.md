# Dai ritorni pesati al conteggio di predecessori distinti

24 settembre 2026. Continuazione del commit `6db72a9`. Il PDF e lo ZIP
della v6 pubblicata restano immutati.

## Risultato matematico

La stima sui tempi di visita è stata collegata alle parole esatte e al
conteggio delle sorgenti. La mappa che associa una parola alla sua sorgente
**può avere ripetizioni**: il controllo avviene sulla somma dei pesi di
ogni fibra. Non si assume che l'endpoint sia non periodico.

Siano W un insieme finito di parole esatte distinte, `x_w` le loro sorgenti
positive, R>0 l'endpoint comune e

\[
\omega(w)=\frac{3^{|w|}}{2^{\sum w}},\qquad K=R(3R+1).
\]

Per una sorgente fissata x, due parole esatte con la stessa lunghezza
coincidono. Inoltre la somma degli esponenti della parola coincide con
quella dell'orbita effettiva. Il precedente limite sui tempi si trasferisce
quindi senza perdere o duplicare termini:

\[
\sum_{\substack{w\in W\\x_w=x}}\omega(w)\le\frac Kx.
\]

Per `x_w≥X>0`, pesi selezionati `0≤v_w≤ω(w)` e una funzione g nonnegativa
sulle sorgenti, il raggruppamento per x dà

\[
\boxed{\quad
\sum_{w\in W}v_wg(x_w)
\le\frac KX\sum_{x\in\{x_w:w\in W\}}g(x).
\quad}
\]

La somma a destra contiene ogni intero una sola volta. In particolare,
se `Σv_w≥η`,

\[
\#\{x_w:w\in W\}\ge\frac{\eta X}K.
\]

Non è un risultato limitato a un campione o a una lunghezza massima.
Include la parola vuota e più giri intorno a un ciclo. Non permette invece
un multinsieme con copie arbitrarie della stessa parola: quello gonfierebbe
artificialmente il peso.

Un esempio chiarisce perché il controllo pesato è utile: da x=R=1,
le parole con k copie dell'esponente 2, per `0≤k≤M`, sono tutte esatte
e distinte ma hanno una sola sorgente. Il loro peso totale è
`4*(1-(3/4)^(M+1))`, sempre minore di K/x=4 e tendente a 4.
L'iniettività delle sorgenti fallisce, mentre la stima resta valida e
il limite universale è raggiunto asintoticamente in questo caso.

## Dalla massa a un conteggio della mappa ordinaria

Il modulo finale espande ogni segmento Syracuse da una sorgente dispari
in un segmento della mappa ordinaria `collatzStep`, con target R arbitrario.
Le sorgenti distinte, se minori di N, appartengono dunque all'insieme
`ordinaryPredecessorsBelow R N`.

Questo insieme finito è definito matematicamente filtrando gli interi sotto
N con la proprietà di raggiungere R. La definizione è noncomputabile:
non costituisce un algoritmo che decide la terminazione delle orbite.
Il dato operativo è la famiglia finita di percorsi già esatti.

Abbiamo anche isolato in un teorema condizionale il calcolo della costante.
Supponendo percorsi esatti da sorgenti dispari con `X≤x_w<N`,
`N=32X`, un intero positivo m e

\[
m^2\ge132KC_*,\qquad
\frac23\le\frac89\,3^m U+\frac{44KC_*}{m^2},
\qquad U=\sum_wv_w,
\]

segue

\[
U\ge\frac3{8\,3^m},\qquad
\boxed{\quad
\#\{0<x<N:\exists j,\ C^j(x)=R\}
\ge\frac3{256K\,3^m}N.
\quad}
\]

Qui `C^j` indica l'iterata della mappa ordinaria e `C_*` la costante
d'errore. La formalizzazione denomina la mappa `collatzStep` e la
costante reale `C`.

**La disuguaglianza analitica e la disponibilità dei percorsi sono ipotesi
esplicite.** Una condizione sufficiente per dedurre una densità inferiore
positiva è avere dati a tutte le scale sufficientemente grandi mantenendo
R, m e C_* fissati. Il punto essenziale è una costante positiva uniforme
in N: lasciare crescere m senza limite non la fornisce. Non abbiamo dimostrato
questo input analitico né la congettura di Collatz.

## Moduli e confine delle prove

| Modulo | Contenuto |
|---|---|
| `WeightedWords.lean` | Unicità della parola a lunghezza fissata; somma degli esponenti; uguaglianza dei pesi; limite per una fibra di parole. |
| `WeightedCounting.lean` | Raggruppamento di famiglie finite con sorgenti ripetute; pesi selezionati; minorazione della cardinalità; calcolo algebrico del termine principale. |
| `WeightedPredecessors.lean` | Applicazione alle parole Syracuse effettive; passaggio alla mappa ordinaria; conteggio condizionale sotto un cutoff. |

Il nucleo non importa risultati dal progetto esterno e non ne assume
teoremi come nuovi assiomi. Le ipotesi delle stime condizionali compaiono
nei relativi enunciati Lean.

## Audit dell'applicazione esterna

L'[audit mirato](EXTERNAL_AUDIT_IT.md) identifica il punto in cui il codice
esterno usa l'assenza di ritorni per ottenere iniettività. Nel caso con
un solo seme, le strutture interne sono identificabili dalle parole
esatte a stadio fissato; non introducono copie arbitrarie della stessa
parola. Sono stati controllati anche i lemmi che identificano i pesi.
L'indice del fan agisce sulle sorgenti dentro la funzione residua: non
cambia l'endpoint R del nostro limite.

La sostituzione combinatoria è quindi supportata dall'ispezione del codice,
oltre che dall'algebra. L'audit ha verificato gli hash degli archivi e
l'assemblaggio statico della chiusura dichiarata, senza ricompilarla.
Restano da compilare l'adattatore ai tipi esterni e da verificare la catena
analitica completa. Il rapporto distingue i controlli eseguiti dalle
dichiarazioni di verifica degli autori esterni.

La scelta di un seme sufficientemente grande in un residuo ternario può
allora usare una ricerca finita, senza un limite ignoto sull'altezza di
eventuali cicli. Questo rende costruttivo quel passaggio **dai parametri
finiti forniti**; non produce ancora un algoritmo completo che calcoli
tutte le costanti analitiche a partire da un target.

## Prossimo obiettivo

Il passo utile successivo è realizzare e compilare l'adattatore sulla
versione fissata del codice esterno, verificando che il suo risultato
pubblico segua con il nuovo limite e senza l'ipotesi no-return. È separato
da una ricompilazione e revisione integrale della parte analitica.
La stima sulle fibre perde il fattore quantitativo `3R+1`; l'eventuale
aumento di m peggiora ulteriormente la costante finale. Il vantaggio cercato
è eliminare una scelta non effettiva, non migliorare automaticamente la
costante di densità. Non rivendichiamo priorità assoluta per questa via.

## Verifica e riproduzione

La build integrata è passata con **3.369 job**, dopo le compilazioni mirate
dei tre nuovi moduli. Le dipendenze fissate usano la cache locale; non si
tratta di una ricompilazione da zero di Mathlib. Il progetto resta su Lean
4.29.1 e Mathlib `5e932f97dd25535344f80f9dd8da3aab83df0fe6`.

L'audit di 14 dichiarazioni principali riporta esclusivamente `propext`,
`Classical.choice` e `Quot.sound`. Nessuno dei nuovi moduli usa `native_decide`;
la scansione dei sorgenti della libreria non trova `sorry`, `admit` o
assiomi dichiarati dal progetto. Il controllo dei PDF pubblicati v1–v6 è
passato e gli hash del PDF e dello ZIP v6 coincidono con quelli precedenti.
Questo non sostituisce la migrazione di toolchain discussa in
[`lean/STATUS.md`](../../lean/STATUS.md).

I tre moduli aggiungono 24 dichiarazioni `theorem`/`lemma` in 434 righe:
sono conteggi del testo sorgente, non 24 risultati matematici indipendenti.
Il [manifest di verifica](verification_manifest.json) registra hash,
revisioni, audit locale e limiti dell'ispezione esterna. Gli output sono
[`lean_build.txt`](lean_build.txt) e [`axioms.txt`](axioms.txt).

Dalla radice del repository:

```bash
cd lean
lake build
lake env lean ../notes/post_v6_counting_2026-09-24/axioms.lean
cd ..
python3 scripts/check_published_pdfs.py
```

Su questo Mac i comandi Lake sono stati eseguiti con
`DEVELOPER_DIR=/Library/Developer/CommandLineTools`, usando il toolchain
fissato; non è stata modificata la configurazione del progetto.
