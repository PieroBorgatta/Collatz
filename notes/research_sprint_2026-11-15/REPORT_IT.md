# Ricerca Collatz del 15 novembre 2026

La sessione ha prodotto un rafforzamento formale del controllo delle traiettorie e un nuovo ponte quantitativo fra atomi interi e regolarizzazione della legge di Syracuse. Ha anche escluso altre famiglie di trasporti e individuato un obbligo analitico preciso per proseguire. **La quota relativa η, H, l'esclusione generale dei cicli e la congettura di Collatz restano aperte.**

Ricerca svolta dalle **20:42:22 alle 22:42:38 di Roma**: **due ore e 16 secondi**. L'esplorazione è stata fermata prima di iniziare questa sintesi. Sono stati impiegati **11 agenti distinti**, con tre lavoratori contemporanei oltre al coordinatore. [Durata registrata](verification/duration_receipt.json), [protocollo iniziale](PROTOCOL_IT.md), [incarichi e dialoghi](AGENTI_IT.md).

## 1. Il punto di partenza e il risultato principale

Il problema rimasto dalla sessione precedente era la massa: controllare l'altezza delle immagini e le loro collisioni non basta a trasferire una parte positiva del bacino di n a quello del sibling canonico h(n). Una minorazione assoluta della densità dei predecessori non confronta i due bacini reali.

Il progresso più utile è duplice. Il budget universale dei reciproci, prima giustificato su carta con una costante molto grande, è ora interamente verificato in Lean con costante inferiore a 81. Inoltre la nuova letteratura del 14 novembre ha suggerito una regolarizzazione che possiamo collegare agli interi con **errore esplicito**, pagando anche il futuro infinito delle parole. Quel collegamento usa positività e unicità delle sorgenti già disponibili nel progetto.

Questa seconda parte non crea η. Sposta però un passaggio prima non controllato in una stima quantitativa, e lascia isolato il problema del rilassamento locale della misura regolarizzata.

## 2. Che cosa è stato integrato e verificato formalmente

Sono stati integrati sette moduli nel punto d'ingresso della libreria. I 56 enunciati pubblici sono dichiarazioni di implementazione, non 56 scoperte indipendenti.

| Modulo | Enunciati pubblici | Contenuto effettivo |
|---|---:|---|
| [OrbitReciprocal](../../lean/CollatzShadowing/OrbitReciprocal.lean) |19| Momenti esatti di parità, packing dyadico e budget globale dei reciproci |
| [WordProductEnvelope](../../lean/CollatzShadowing/WordProductEnvelope.lean) |7| Prodotto esatto, controllo esponenziale e altezza con coefficienti omogenei confrontabili |
| [FirstArrivalBudget](../../lean/CollatzShadowing/FirstArrivalBudget.lean) |13| Clock Syracuse/shortcut, iniettività del primo arrivo e altezza universale effettiva |
| [IntegerAtomTilt](../../lean/CollatzShadowing/IntegerAtomTilt.lean) |5| Budget quadratico degli atomi interi, condiviso fra profondità nel dominio senza ritorni |
| [TwoEditSparsity](../../lean/CollatzShadowing/TwoEditSparsity.lean) |5| Residui completi per entrambi i segni e budget elementare del totale degli esponenti |
| [TraceDensityBridge](../../lean/CollatzShadowing/TraceDensityBridge.lean) |4| Ponte algebrico condizionale fra confronto di tracce e densità |
| [CycleMinimumProduct](../../lean/CollatzShadowing/CycleMinimumProduct.lean) |3| Prodotto minimo e gap logaritmico classici per cicli esatti |

Per ogni segmento finito **positivo e iniettivo** della shortcut T:

`Σ_(x nel segmento)1/x ≤133547/1655<81`.

La prova usa momenti di parità e somme geometriche finite, senza assumere una stima analitica esterna. Un singolo giro di un ciclo, contato senza ripetizioni, è ammesso; ripetere i suoi punti con molteplicità non è ammesso.

Una parola di primo arrivo accelerato si espande in un primo arrivo shortcut. Gli stati intermedi di un episodio sono pari; il clock degli stati dispari è esattamente la somma degli esponenti. Ne segue, per il prodotto correttivo della parola,

`P=Π_(i<k)(1+1/(3x_i))=2^A n/(3^k u)≤exp(27)`.

Se una parola effettiva di immagine verso h(n) esiste e conserva (k,A), allora

`v≤21 exp(27)u`.

Si possono cambiare anche lunghezza e totale, purché il rapporto dei coefficienti `ρ=2^A/3^k` sia al più C; il limite diventa `v≤21C exp(27)u`. L'esistenza dell'immagine rimane un input. Questa stima non costruisce un matching né una massa positiva. [Derivazione e limiti](ROOT_HEIGHT_IT.md).

## 3. La nuova fonte web e il ponte agli atomi interi

È stata acquisita integralmente la fonte primaria [146/v1, *Exact critical tail and linear collision energy for the ternary Syracuse law*](https://rstation.ai/problems/collatz/papers/146), pubblicata il 14 novembre 2026 alle 16:51 UTC. Il testo argomenta una coda κt⁻², weak L² ed energia dei cilindri di ordine lineare. Il nucleo analitico, incluso il lemma sui supporti ritardati, è stato ricostruito da T10, T11 e dal coordinatore; non è emerso un errore bloccante nei passaggi letti. È un manoscritto pubblico con revisione sul sito, non una certificazione formale o una revisione accademica indipendente eseguita qui. [Fonte, licenza e hash](../../research/research_sprint_2026-11-15/t10/sources/manifest.json).

La fonte non dà incrementi energetici uniformemente limitati, un limite dell'energia divisa per la profondità o una traccia uniforme sugli interi. Nessun suo teorema è stato aggiunto come assioma Lean.

Il ponte costruito nella sessione riguarda il cap del **massimo moltiplicatore reale** H della parola casuale, distinto dal cap sugli esponenti della sezione seguente. Per un target positivo dispari n, ogni prefisso che contribuisce al suo atomo ternario ha identità

`n=B_i+A_iY_i`, con Y_i intero positivo.

Quindi A_i≤n. Il dizionario richiede di invertire l'ordine della parola rispetto alla convenzione forward locale.

Sotto la legge tilt `P*(e=j)=3·4⁻ʲ`, il contributo normalizzato di una parola è A_w². Nel nucleo Lean, A_w≤n/u e l'iniettività delle sorgenti danno

`Σ_w A_w²≤n²Σ_(u≥1)u⁻²≤2n²`.

Il bound è formale per cataloghi finiti. Il passaggio alle leggi infinite usa monotonia; nel dominio senza ritorni lo stesso budget è condiviso fra tutte le profondità, perché ogni sorgente raggiunge n a un solo tempo:

`Σ_(m≥0)ρ*_m(n)≤2n²`.

Sia σ_B la misura originale ristretta a H≤B, con B>n, e sia C_m(n)=n+3^mZ₃. La martingala del moltiplicatore paga gli attraversamenti futuri. Su carta otteniamo

`0≤ρ_m(n)−3^mσ_B(C_m(n))≤2n²/B`.

Per n senza ritorni l'errore è anche sommabile in m. L'errore fra i Cesàro di K termini è quindi al più

**`2n²/(BK)`**.

Con B=2n e g(n)≥cεn, l'errore relativo è Oε(1/K). Il passaggio dal cap finito a quello infinito è così pagato quantitativamente. **Il tempo di rilassamento della legge capped non è stato ottenuto.** [Prova del ponte](ROOT_MULTIPLIER_IT.md), [rapporto T10](agents/T10_STATIONARY_ATTACK_IT.md).

## 4. Strade escluse con prove e dominio esplicito

**Modifiche terminali limitate.** Per uno shift fissato, la surgery di due esponenti ha soltanto X^o(1) codici fisici con sorgente≤X, anche senza cutoff sull'immagine. La prova combina il residuo completo divisibile per 3^k, il budget `2^A n≤4^k u` e il [Corollario 2 di Evertse, p. 228](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf). T04 l'ha ricostruita indipendentemente e ampliata a sostituzioni di code di lunghezze fissate e variazione totale fissata, anche cambiando profondità. Per lunghezze diverse va esclusa la diagonale u=v; nei bacini sibling disgiunti è assente. L'unione non pesata di parametri che crescono con X non è esclusa. La miscela di primo arrivo pesata con 2⁻|δ| ha invece massa uscente o(X). L'asintotica è una prova su carta, non il contenuto del modulo Lean. [T02](agents/T02_SURGERY_ETA_IT.md), [T04](agents/T04_SURGERY_REVIEW_IT.md).

**Alberi a esponenti troppo limitati.** Se N_M conta predecessori ordinari con tutte le valutazioni≤M, una stima uniforme nel target è

`N_M(n,X)≤6X(1−2⁻ᴹ)^floor(floor(log₂X)/8)+8X^(3/4)`.

Quindi `2^M=o(log X)` implica N_M=o(X). Una quota lineare richiede almeno `M≥log₂log X−O(1)`, con costante dipendente dalla quota. Per un pool crescente di target occorre pagare anche la sua cardinalità. Il risultato usa cilindri effettivi, overflow del clock e momenti di parità; non ipotizza indipendenza lungo una singola orbita. È una prova su carta rivista da T09. [T08](agents/T08_JOINT_STRIP_IT.md), [T09](agents/T09_INDEPENDENT_MATH_IT.md).

**Accoppiamento ordinale e greedy.** Una famiglia analitica impone crescita esponenziale del costo puntuale dell'ordinale; le continuazioni danno input arbitrariamente grandi a target fissato, ma rimangono scartabili in o(X). Il greedy riduce l'altezza pagando collisioni e perdita di massa. Nel controtest 593, il 77,7% di codici entro altezza 64 porta solo lo 0,023% della massa armonica finita. Né questa massa né il numero di codici è η naturale. [T06](agents/T06_INVERSE_CONTROL_IT.md).

Non conviene quindi proseguire aumentando soltanto i cutoff, perfezionando il greedy sul medesimo albero a cap fisso o cambiando soltanto una finestra terminale fissata.

## 5. Le due prosecuzioni rimaste concrete

La prima è un confronto cumulativo dei cataloghi fisici ordinati per ρ. Se per ogni soglia t vale `m L_y(Ct)≥L_n(t)`, l'ordine costruisce un trasporto con carico≤m e altezza≤21C exp(27). Un errore additivo costante elimina soltanto finitissime sorgenti. Per H servirebbe un costo netto mC dell'ordine di 1+log n. **Il confronto dei cataloghi resta non dimostrato** ed è vicino, a costanti universali, al confronto di densità cercato; cambiare il linguaggio non lo risolve.

La seconda è controllare il rilassamento locale. Nel quadro delle identità esterne fra traccia g, densità d e medie pesate D, il vero kernel inverso soddisfa

`E_n^Doob[1/g(Y_m)]=ρ_m^U(n)/g(n)`.

Le foglie divisibili per 3 hanno g=0 e vanno escluse dalla cancellazione. Si ha inoltre `ρ_m^U≤ρ_(m+1)≤2ρ_m^U`, utile per passare a un lower della legge piena.

Usando anche il floor esterno `g(z)≥c₀>0` sulle unità positive, T07/T09 hanno dimostrato su carta un criterio di escape a blocchi. L'input preciso è: esista θ>0 tale che, per ogni target dispari positivo non periodico n sufficientemente grande e non divisibile per 3, esista un tempo m(n)≤K(n) con `E_n^Doob[1/g(Y_m(n))]≥θ`, dove

`K(n)≤log_(3/2)n−h(n)+C`, con h(n)→∞.

Una spine divergente conserva densità di bacino positiva e dunque g(n_j)≥c·n_j. Il lower forza una probabilità uniforme di abbandonare il backtracking in ciascun blocco. La concatenazione contraddice la probabilità positiva uniforme di risalire fino a un antenato fissato. I cicli non banali restano distinti.

La nuova weak L² offre anche un criterio locale alla scala `m≤2log₃n−h(n)+C`: il lower `ρ_m(n)≥θg(n)` implicherebbe g(n)=o(n). Il ponte σ_B permette ora di formulare il problema attraverso medie capped, con errore esplicito.

**Nessuno di questi lower uniformi è stato provato.** La versione ristretta ai target con d_n≥ε, per ogni ε>0, concentra il problema sugli antenati piccoli; nel quadro esterno è un criterio equivalente all'eventuale periodicità, non una scorciatoia già acquisita.

I contro-modelli costruiti mostrano perché mixing globale, energia lineare e L^p per p<2 non bastino da soli. Essi violano esplicitamente la stazionarietà Syracuse. La prova esistente del clock conserva inoltre un termine T_n(M), con veri tempi di arrivo da piccoli antenati: eliminarlo a root fissato non dà uniformità nel root. Il prossimo attacco deve usare questa struttura aritmetica, non una nuova assunzione di uniformità. [T07](agents/T07_ENERGY_OCCUPATION_IT.md), [T09](agents/T09_INDEPENDENT_MATH_IT.md).

## 6. Cicli e altre fonti

Il canale cicli ha integrato soltanto vincoli classici verificati. La fonte Alick del settembre 2026 dichiara almeno 102 minimi locali sotto due input espliciti: verifica numerica fino a 2^71 e bound di Rhin. Sono minimi locali shortcut, non 102 passi dispari. Sono stati letti enunciati e sorgenti fissati, senza replay esterno; quel risultato non è importato nella libreria.

Le fonti Nashida sui barrier count e Vasilyev sulle varianti sono state esaminate con i rispettivi quantificatori. Un count assoluto uniforme nei cutoff non dà H; una famiglia con switching non coincide con l'orbita deterministica. [Audit web/cicli T05](agents/T05_WEB_CYCLES_IT.md). Le nuove identità esterne sulla traccia sono state fissate e confrontate staticamente con i record pubblicati, senza ricompilarne i progetti. [T03](agents/T03_PROFILE_MASS_IT.md).

## 7. Verifica, provenienza e consegna

- **Build completa PASS:** 3400 job, sorgenti immutati durante le fasi.
- **Audit transitivo PASS:** 136 dichiarazioni nei sette moduli, comprese 14 dichiarazioni private codificate; soltanto propext, Classical.choice e Quot.sound. Nessun nuovo sorry, assioma dichiarato o native_decide.
- **Dieci replay PASS:** output normale e Python-O identici, inclusi controlli indipendenti di residui, clock, cap, atomi e correlazioni. Non sostituiscono le prove asintotiche.
- **Controllo semantico indipendente:** moduli, domini e indice verificati; applicate due precisazioni documentali. [T11](agents/T11_FORMAL_SEMANTICS_IT.md).
- Aggiornati punto d'ingresso, indice dei teoremi, README, stato, statistiche e controlli CI. La configurazione CI è verificata localmente; non è stato avviato un run remoto.

Le verifiche riusano il toolchain fissato Lean/Mathlib 4.29.1 e i suoi artefatti. Non sono un replay con kernel indipendente, una compilazione a freddo di Mathlib o una nuova compilazione dei progetti esterni 4.30/4.35. I sorgenti preesistenti sono preservati. Nessun nuovo livello della torre è stato calcolato; il precedente stop della campagna di filtri rimane valido. PDF pubblicati, versioni degli strumenti e storia Git non sono stati modificati; nessun deposito v7, push o contatto esterno è stato effettuato.

Il [manifest finale](verification_manifest.json) collega sorgenti, report e ricevute. La fotografia riuscita a sei moduli è conservata separatamente prima dell'aggiunta del ponte aritmetico. I risultati consentono una continuazione tecnica documentata; una soluzione richiede ancora il lower locale o la comparazione relativa sopra indicati.
