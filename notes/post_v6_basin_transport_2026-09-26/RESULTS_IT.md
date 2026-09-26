# Trasporto dei bacini: un metodo esatto, i suoi costi e un limite asintotico

26 settembre 2026. Piero Borgatta con assistenza Codex.

**Esito:** H non è stata dimostrata né confutata. Il lavoro ha prodotto
un trasporto aritmetico esatto, formalizzato in Lean, e ostacoli rigorosi
ai metodi esaminati. Il più incisivo è asintotico: aumentando
soltanto l'ultimo esponente, non si conserva una quota positiva delle
sorgenti entro alcuna dilatazione fissa del cutoff. Non è una conclusione
tratta da un censimento più grande.

## 1. L'obiettivo rimane lo stesso

Per il bacino ordinario B(n), con densità naturale inferiore d_*(n),
la candidata precedente chiedeva

\[
d_*(h(n))\ge\frac{c}{1+\log n}\,d_*(n),\qquad c>0\text{ universale},
\]

con n dispari positivo, 3∤n, entrambi i target senza ritorni positivi, e
h(n)=4n+1 oppure 16n+5 secondo n modulo 3. H più la positività dei bacini
escluderebbe le orbite divergenti; resterebbero i cicli non banali.
Non si sono cambiati i quantificatori per adattarli ai risultati negativi.

## 2. Un trasferimento vero, con un costo inevitabile

Una parola esatta di k esponenti, somma A e costante C>0, porta u a n:

\[
3^k u+C=2^A n.
\]

La costante C non dipende dall'ultimo esponente. Aumentandolo di δ≥0,
con `2^δ y=n+3^k q`, si ottiene un vero predecessore di y:

\[
u'=u+2^Aq.
\]

Non si sta costruendo soltanto una soluzione razionale: tutti gli esponenti
sono quelli della vera dinamica Syracuse. Questo passaggio è formalizzato
in [`LastExponentTransport.lean`](../../lean/CollatzShadowing/LastExponentTransport.lean).
Il modulo assume esplicitamente la correzione intera; l'esistenza tramite
logaritmo discreto modulo 3^k è trattata su carta.

Se y>n, allora q≥1. Ne segue la disuguaglianza stretta, anch'essa in Lean,

\[
\boxed{n u'>(n+3^k)u.}\tag{1}
\]

Questo costo non è un difetto di un'implementazione particolare: vale
per ogni correzione nonnegativa dell'ultimo esponente.

## 3. Il limite asintotico dello schema

Manteniamo il fattore diadico di una sorgente ordinaria x=2^e u e
trasportiamola in x'=2^e u'. Fissiamo n, y e un qualunque fattore D>0,
anche dipendente da quei target. Fra le sorgenti x≤X nel bacino di n,
contiamo quelle per cui x'≤DX.

Per un intero K fissato:

- le sorgenti che arrivano a n in al più K passi dispari sono
  `O_K((1+log X)^(K+1))`: gli esponenti hanno un limite logaritmico,
  una parola determina al più una sorgente dispari e i fattori diadici
  aggiungono al più un ulteriore fattore logaritmico;
- per le altre, (1) impone `x<nDX/3^K`.

Dividendo per X e prendendo prima il limsup, poi K arbitrariamente grande,

\[
\limsup_{X\to\infty}\frac{\#\{x\le X:x'\le DX\}}X
\le\frac{nD}{3^K}\longrightarrow0.
\]

**Il trasferimento nonnegativo conserva densità zero entro ogni cutoff
dilatato di un fattore fisso.** Quando il bacino di n ha densità inferiore
positiva, questo esclude che lo schema trasferisca una sua frazione
positiva a quella scala. Non occorre assumere l'iniettività del trasporto.
La prova asintotica è su carta, verificata internamente da un secondo agente;
non è formalizzata in Lean né sottoposta a revisione umana.

Consentire δ negativi non elimina tutti i problemi. Per la coppia fissa
17 e 277, entrambe certamente senza ritorni, le sorgenti nel sottobacino
B(11) arrivano a 17 con ultimo esponente 1; esso non può essere diminuito.
Su quel sottobacino vale lo stesso limite. Il risultato non controlla
automaticamente la massa degli altri rami.

## 4. Cambiare tutte le lettere, conservando la profondità

È stato controllato anche un accoppiamento che cambia tutti gli esponenti.
Un risultato più generale del suo fallimento è il seguente. Per k≥0, t≥1,

\[
n=2t3^{k+2}-1,\quad u=18t2^k-1,\quad y=h(n),
\]

la sorgente u raggiunge n con k esponenti tutti uguali a 1. **Ogni**
predecessore v di y a profondità esattamente k soddisfa

\[
\boxed{23^k v>16\,33^k u.}\tag{2}
\]

La prova trasferisce la parola superiore al target negativo −11 e usa
soltanto un insieme finito chiuso per la mappa `oddpart(3q−1)`. Non assume
congetture sulle orbite negative. La dimostrazione e i controlli sono nella
[nota sul coupling](local_coupling_IT.md); (2) è provata su carta, non in Lean.

Esiste una sottofamiglia esplicita con `S(n)=S(h(n))=1`: anche nel dominio
esatto di H, un trasporto puntuale di **tutte** le sorgenti alla stessa
profondità non può avere dilatazione costante universale. Sono essenziali
due limiti: su quella sottofamiglia il bound non esclude un costo O(log n);
inoltre i testimoni puntuali possono essere scartati nell'errore o_n(X)
consentito da un confronto di densità. H rimane aperta.

## 5. Pesi, molteplicità e letteratura

Ottimizzare separatamente la correzione firmata distrugge l'iniettività.
Per esempio, per n=17 e y=277, le parole `(1,1)` e `(1,7)` partono da
7 e 483, ma entrambe vengono mandate alla parola `(1,6)`, con sorgente
3939. Le fibre sono infinite; i loro pesi hanno una somma geometrica
controllabile, ma il rapporto con il peso dell'immagine può ancora essere
enorme. Non è lecito passare dal conteggio di parole al conteggio di interi
senza questo controllo.

La [ricerca mirata delle fonti](SOURCES_IT.md) confronta Wirsching,
Krasikov–Lagarias, Mazur e Sharpe. Le stime disponibili sono assolute o
medie nella coordinata ternaria; non producono il rapporto H. Inoltre
`h(n)−n` non è divisibile per 3: la vicinanza reale dei target non li rende
vicini nella metrica 3-adica. L'ottimizzazione locale alla radice sesta è
conservata e non viene presentata come un nuovo risultato di questa fase.

La [nota critica](OBSTRUCTIONS_IT.md) dimostra anche perché positività,
packing e terminazione astratti non bastano, e perché una decomposizione
infinita dei bacini non autorizza a sommarne le densità senza controllare
le code.

## 6. Verifiche e confini

**Build integrata riuscita: 3379 job, exit 0**, senza errori o avvisi nel
log finale. **Audit rigoroso passato su tutte le sette dichiarazioni**:
sole dipendenze da `propext`, `Classical.choice` e `Quot.sound`. Entrambi
i probe esatti sono stati rieseguiti con `python3 -O`; i due JSON coincidono
byte per byte con i risultati salvati.

Il modulo Lean contiene sette dichiarazioni pubbliche: endpoint affine
esatto, costante invariata, trasporto effettivo, positività della correzione,
costo d'altezza e sue conseguenze. Il suo perimetro non comprende (2),
la prova di densità zero, H, o una nuova verifica dell'input analitico esterno.

I replay Python usano interi e frazioni: sette parole della famiglia
avversa, correzioni firmate e collisioni, permutazioni di residui, tabelle
modulo 9 e 27, parole inverse finite e testimoni delle famiglie esatte.
Nessun censimento degli inizi è stato ampliato e non viene stimata una
nuova densità. Gli esiti di build, audit e replay sono registrati con hash
in `verification_manifest.json`.

Toolchain e Mathlib rimangono ai pin esistenti, Lean 4.29.1 e revisione
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`. La build riusa dipendenze
compilate: non è un rebuild freddo di Mathlib, una verifica con kernel
indipendente o un nuovo replay della catena analitica esterna. Il workflow
CI è aggiornato; non si dichiara una nuova esecuzione remota.

Dalla directory `lean`:

```sh
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_basin_transport_2026-09-26/DependencyAudit.lean
python3 -O ../notes/post_v6_basin_transport_2026-09-26/transport_probe.py --output /tmp/last-exponent-results.json
cmp ../notes/post_v6_basin_transport_2026-09-26/transport_results.json /tmp/last-exponent-results.json
python3 -O ../notes/post_v6_basin_transport_2026-09-26/local_coupling_probe.py --output /tmp/local-coupling-results.json
cmp ../notes/post_v6_basin_transport_2026-09-26/local_coupling_results.json /tmp/local-coupling-results.json
```

## 7. Decisione

Si chiude il tentativo di ottenere H mediante aumento del solo ultimo
esponente o mediante un trasporto puntuale universale con profondità e
dilatazione costante conservate. Queste sono esclusioni di metodi, non di H.

Un prossimo risultato utile deve confrontare **masse di sorgenti per un
target fissato**: può cambiare più esponenti, cambiare profondità o scartare
parte delle sorgenti, ma deve quantificare la perdita, le molteplicità e
la dilatazione. Al momento non abbiamo costruito un tale meccanismo.
Ripetere i conteggi finiti o introdurre una generica ipotesi di mixing non
supererebbe gli ostacoli dimostrati qui.
