# Audit mirato dell'applicazione ai predecessori

24 settembre 2026. Audit di sorgenti e compatibilità matematica: **non è una
ricompilazione né una revisione completa dell'analisi esterna**.

**Esito:** il controllo pesato dei ritorni consente di eliminare la scelta di
un seme non periodico nel conteggio del manoscritto. L'applicazione resta
condizionata al suo input analitico. I tipi concreti del codice esterno non
introducono duplicazioni incontrollate delle parole, quando si fissa lo stadio
e si usa il seme singleton del teorema pubblico. Sono identificati i lemmi
necessari all'adattatore; quell'adattatore non è stato compilato qui.

## 1. Fonti esatte e verifica effettuata

Il [manoscritto v1.0 di Mazur](https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/paper-v1.pdf),
§§3–4 e Appendice A, separa una stima su parole inverse dal conteggio delle
sorgenti. La Proposizione 3.1 non assume assenza di ritorni; la richiede invece
il Lemma 4.1 per ottenere iniettività. Il manoscritto precisa che la
Proposizione 3.1 è una combinazione espositiva, non un'unica dichiarazione
formale controllata. Il fattore di riferimento nel vecchio conteggio è R;
il suo Remark 4.3 collega la non effettività alla scelta fuori da un possibile
ciclo.

La [pagina attuale di formalizzazione](https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/)
riporta una verifica successiva dell'intera chiusura locale di 388 moduli,
checkout `c290ac229b379d2b51026d3e86140496870d6f39`, e tre assiomi standard.
Questo aggiorna, senza cancellarlo, il vecchio record di 11 moduli ricompilati
del supplemento/PDF. Anche il controllo successivo riusa dipendenze compilate
esterne e non è LeanChecker indipendente. Queste sono dichiarazioni del
fornitore, non esiti di una nostra esecuzione.

Ho scaricato e verificato entrambi gli archivi pubblici:

| Pacchetto | Byte | SHA-256 |
|---|---:|---|
| [Supplemento v1.1](https://www.proofatlas.ai/papers/positive-lower-density-collatz-predecessors/positive-lower-density-collatz-predecessors-v1.1-source.zip) | 55 103 | `55ceb4df0cca17ae728dc65b30bf5077000e1b47f2dc322454eea9f637ac75b3` |
| [Baseline slim v2.1](https://www.proofatlas.ai/papers/positive-density-log-time-collatz/positive-density-log-time-collatz-v2.1-source.zip) | 914 975 | `23f5cac4d66e696401144658752cf180a13ce70373a122f00693e1e1fe969c1f` |

La baseline registra la revisione `830b9d3f38f2a8da8cd921bf6a9310dd69336fd0`,
Lean `4.30.0-rc2`, Mathlib `5450b53e5ddc75d46418fabb605edbf36bd0beb6`.
Lo script ufficiale `scripts/assemble.py`, letto prima dell'esecuzione,
ha autenticato i manifest e ricostruito 389 file Lean: 388 della chiusura
pubblica più `Verification.ReleaseAudit`. Risultato esplicito:
`static_import_closure_complete=true`, `lean_replayed=false`; 377 sorgenti
della baseline e 10 moduli di implementazione del supplemento, oltre
all'interfaccia e all'audit. I download e l'assemblaggio sono rimasti in
`/tmp/collatz-predecessor-audit`; nessun sorgente esterno è stato incorporato.

## 2. Traccia nel codice, oltre la formulazione del PDF

I riferimenti seguenti sono percorsi dentro gli archivi autenticati. Salvo
indicazione diversa, il prefisso è `Erdos1135/ND/PositiveDensity/`.

| Punto | Dichiarazione e posizione | Uso effettivo |
|---|---|---|
| Interfaccia | `CollatzPredecessorDensity.lean:36`, `predecessors_positive_lower_density` | Richiama il teorema generale. |
| Assemblaggio del risultato | `GeneralTargetPositiveDensity.lean:7`, `generalTarget_predecessors_positive_lower_density` | Ottiene seme, massa e conteggio; passa `hseed` a entrambi gli ultimi due. |
| Scelta del seme | `GeneralTargetFrozenSeed.lean:7,44,64` | Trasporta la proprietà no-return come componente del risultato. |
| Primo uso della non periodicità nel conteggio | `GeneralTargetSeedNonreturn.lean:56,88` | Unicità della rappresentazione tramite `(ancestor,source)`, quindi maggiorazione della somma pesata. |
| Rimozione del peso residuo | `GeneralTargetTerminalCensus.lean:27,55,147,181` | Propaga quella maggiorazione al termine d'errore e alla massa selezionata. |
| Cardinalità finale | `GeneralTargetTerminalCensus.lean:212` e `GeneralTargetPredecessorCount.lean:13` | Usa di nuovo la stessa maggiorazione; la raggiungibilità è separata. |

La parte analitica precedente è effettivamente separabile: in
`ExplicitUnitSupportedFrozenSeed.lean:75`,
`explicit_good_marked_margin_logarithmic_full` assume la massa iniziale,
mixing e vincoli geometrici; non richiede che il seme converga o sia
non periodico. In `GeneralTargetFrozenSeed.lean:82–119`, `hnonreturn` è
restituito nella tupla, ma non entra nella dimostrazione della stima finale.
La selezione residua è `ExplicitUnitSupportedCoreSeed.lean:56`,
`exists_unit_rootCoreBackwardMark_ge_full_product`. Le riduzioni quantitative
immediate sono in `PredecessorAnalyticSupport.lean:27,40,54,147`.
Ho ispezionato questi enunciati e corpi; non ho rivalutato tutti i lemmi
analitici che richiamano, né i 388 file riga per riga.

## 3. Il problema delicato: parole oppure etichette duplicate?

Il risultato locale sui ritorni vale per tempi distinti e quindi per parole
esatte distinte. Non permetterebbe di eliminare arbitrariamente duplicati
presenti in un multinsieme esterno.

Il codice offre però una risposta precisa. In
`Geom2ShiftedWideSymmetricRootSideGeometricFullTerminalCount.lean`:

- `FullTerminalAt` (:95) è l'incidenza terminale dopo uno stadio fissato.
- `forwardLabel_tail_eq_of_append` (:60) ricostruisce la suddivisione nei
  blocchi a partire dall'antenato e dalla parola concatenata.
- `fullTerminal_eq_of_ancestor_word_eq` (:113) prova uguaglianza delle
  incidenze da uguaglianza dell'antenato e dell'intera parola.
- `fullTerminalPath_word_eq_reverse` (:152) identifica quest'ultima con la
  parola esatta del percorso, invertendone soltanto l'ordine.

Nessuno di questi lemmi assume no-return. Il seme usato dal teorema pubblico
ha etichetta `Unit`: l'antenato è automaticamente unico. **A stadio, shift
e cap fissati, la parola esatta identifica quindi l'incidenza.** Per più
antenati bisogna invece raggruppare anche per antenato; non è autorizzato
cancellarne l'etichetta. Il conteggio usa un solo stadio per ciascuna scala;
non serve confrontare rappresentazioni provenienti da stadi diversi.

La definizione concreta, in
`Geom2ShiftedWideSymmetricRootSideBoundedOvershootPhysicalIncidence.lean:80`,
è una somma dipendente di etichetta, profondità e parola nel relativo insieme
finito. Il lemma `...eq_of_label_eq_of_commonPrefix` (:441) usa l'unicità
della profondità di primo attraversamento e poi l'estensionalità; i campi di
prova non producono ulteriori copie. Ho seguito questo tratto della prova.

Anche i pesi coincidono, non soltanto il loro limite superiore. La definizione
di peso terminale (:200–216 nello stesso file) è il peso esterno moltiplicato
per `3^depth` e per la probabilità della parola. Il lemma
`geom2PNatListPMF_apply_length_toReal_eq_weight`, in
`Erdos1135/Tao/Syracuse/ValuationDistribution.lean:93`, identifica quella
probabilità con `2^(-sum)`.
In `Geom2ShiftedWideSymmetricRootUniformGroupedCapacity.lean:193`,
`forwardWeight_eq_ownerWeight_mul_wordAtom` identifica il peso ereditato
con peso dell'antenato per peso della parola precedente; :20 fornisce la
moltiplicatività per concatenazione. **Deduzione nostra:** combinando queste
identità, il peso totale è precisamente il peso iniziale dell'antenato per
`3^length/2^sum` della parola intera. Per il singleton il peso iniziale è 1.
Questa composizione in un adattatore esterno resta da compilare.

Il fan non cambia gli endpoint: in
`Geom2ShiftedWideSymmetricTerminalDepthShiftCensus.lean:206`,
`forwardGoodDepthShiftUnitMass_le_full_cap_one_fan` applica `Ψ_j` alla
**sorgente** dell'incidenza ridotta, dentro la funzione residua. L'indice j
è una somma esterna con coefficiente `4^(-j)`, non un ulteriore duplicato
di `FullTerminalAt`. Il limite nuovo si applica per ciascun j alla funzione
nonnegativa `δ ∘ Ψ_j`; soltanto dopo si sommano quei coefficienti.

## 4. Deduzione nostra: sostituzione del conteggio e seme finito

Assumiamo l'input della Proposizione 3.1 con i suoi dati e poniamo
`K = R(3R+1)`. Per il nostro lemma e l'unicità delle parole a lunghezza
fissata, ogni fibra di sorgente x ha massa al più `K/x`.
Per `x ≥ X > 0`, raggruppare le fibre dà

\[
\sum_w v_w g(x_w)\le\frac KX\sum_{x\in\{x_w\}}g(x).
\]

Applicando questa formula alle funzioni residue e il conteggio elementare
delle classi si ottiene `33K⟨g⟩`. La somma del fan introduce al più `4/3`;
il termine d'errore è dunque `44KC_*/m²`.
Scegliendo un intero positivo con `m² ≥ 132KC_*`, segue

\[
U\ge\frac{3}{8\,3^m},\qquad
\#\bigl(P(a)\cap[1,Y)\bigr)\ge\frac{3}{256K\,3^m}Y
\quad\text{per }Y\ge32(H+1),
\]

dove H è un intero almeno pari alla soglia analitica. Non occorre decidere
se R sia periodico. Si perde quantitativamente un fattore `3R+1` nella
costante di fibra, ma si elimina l'obbligo di escludere i cicli.

**Scelta costruttiva di R, una volta forniti a, q, y e la soglia B:**
per un target `a>0` non divisibile per 3, scegliere `e=2` se
`a≡1 mod3`, altrimenti `e=1`; porre
`r₀=(2^e a−1)/3`, `R_k=(2^e a·4^k−1)/3`.
Enumerare `k₀∈{0,…,3^q−1}` fino a `R_k₀≡y mod3^q`, quindi usare

\[
k=k_0+(B+1)3^q,\qquad R=R_k.
\]

La ricerca finita termina perché la mappa dei residui è una permutazione.
La periodicità in k conserva il residuo e `R_k≥k>B`; per k positivo R è
dispari e `C^{2k+e+1}(R)=a`. Il calcolo del residuo può essere fatto modulo
`3^(q+1)` prima della divisione per 3, senza materializzare la potenza intera.
Le giustificazioni aritmetiche si trovano già in
`GeneralTargetResidueCoverage.lean:16,21,33,48,53,60,76`; il ramo che usa
un limite su un possibile ciclo (:101) non serve più.

Questo rende effettiva **la scelta del seme dai dati finiti forniti**.
Non dimostra ancora un algoritmo completo target→costanti: qui H resta
esistenziale e non è stato implementato il calcolo dei parametri analitici.
Il codice esterno contiene già una formula `ndExplicitRootIntervalHeight`
e un coefficiente di mixing esplicito; ciò indica un possibile lavoro
successivo, non autorizza a dichiarare quell'obiettivo già verificato.

## 5. Matrice delle affermazioni

| Affermazione | Stato di questo audit |
|---|---|
| Identità dei due ZIP pubblici | Verificata direttamente, byte e SHA-256. |
| Chiusura pubblica assemblabile, 388 moduli | Verificata staticamente con manifest; nessuna compilazione nostra. |
| Rebuild esterno di 388 moduli e tre assiomi standard | Dichiarato dal sito, distinto dal vecchio record degli 11 moduli. |
| No-return assente nella stima analitica immediatamente precedente | Controllato negli enunciati e corpi indicati, senza audit analitico transitivo completo. |
| Duplicazioni della stessa parola esatta nel singleton a stadio fissato | Escluse dai lemmi strutturali letti; nessuna ipotesi no-return necessaria. |
| Compatibilità dei pesi | Identità di base controllate; composizione dell'adattatore dedotta, non compilata. |
| Sostituzione `R → R(3R+1)` nel conteggio | Deduzione matematica condizionata all'input analitico e al ponte sulle parole. |
| Ricerca del seme senza classificare cicli | Costruzione finita esplicita dai dati `a,q,y,B`. |
| Teorema esterno ricompilato con il nostro lemma | Non eseguito. |
| Priorità scientifica o soluzione di Collatz | Non rivendicate. |
