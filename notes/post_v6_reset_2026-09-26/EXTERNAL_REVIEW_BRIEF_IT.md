# Nota per una revisione matematica esterna

26 settembre 2026. **Bozza preparata per un revisore umano; non inviata.**
Oggetto: risultati della v6 e sviluppi del 24–26 settembre. Non si chiede
di validare una dimostrazione di Collatz: il progetto non ne contiene una.
Non si rivendica originalità matematica o priorità bibliografica.

## 1. Richiesta e conclusione dell'audit interno

Chiediamo una valutazione dei quantificatori, delle dipendenze e dell'utilità
dei risultati intermedi, distinguendo tre obiettivi: convergenza universale,
discesa di una torre speciale, densità dei predecessori. La nostra conclusione
provvisoria è che **non sia giustificato proseguire aggiungendo filtri alla
torre dopo ogni controesempio**. Il limite uniforme sulle sue parità rimane
aperto; anche dimostrarlo non fornirebbe da solo una copertura di tutte le
orbite positive. Il ramo dei predecessori ha invece prodotto modifiche
quantitative autonome, con un input analitico esterno da valutare separatamente.

Il presente audit è una lettura dei sorgenti e delle note, non una verifica
con kernel indipendente o una peer review. Le espressioni «verificato in Lean»
sotto rimandano alle dichiarazioni e alle evidenze archiviate; i nuovi controlli
del consolidamento sono registrati separatamente nella [relazione](RESULTS_IT.md).
La catena analitica esterna non è stata ricompilata in questa fase.
La v6 pubblicata e il suo archivio sono fotografie congelate: non contengono
automaticamente i risultati successivi del working tree.

## 2. Risultati effettivi e loro perimetro

Si usano due mappe diverse: `T(n)=n/2` per n pari e `(3n+1)/2` per n dispari;
`S(n)=(3n+1)/2^ν₂(3n+1)` sui dispari positivi. I tempi delle due mappe non sono
intercambiabili.

**V6, aritmetica locale.** La libreria formalizza il cilindro di una parola
Syracuse esatta, compreso il bit che certifica l'endpoint dispari; la perdita
di precisione a ogni ripetizione di una parola espansiva fissata; il trasporto
compatibile delle etichette affini; condizioni necessarie sui cicli e criteri
finiti di discesa. Controesempi delimitano i ranghi proposti. I bound spettrali
riguardano matrici finite, non un operatore infinito. La separazione aritmetica
alla singolarità è formalizzata; la ricostruzione generale delle parole
infinite e la conclusione topologica hanno stato di prove su carta.

**Sezione con copertura universale.** È formalizzato che ogni orbita positiva
di T raggiunge 1 oppure `20 mod 27` entro `13n+4` passi. Una sezione E di sei
progressioni descrive esattamente gli episodi Syracuse marcati corrispondenti.
Ogni orbita dispari raggiunge 1 oppure E; se non raggiunge 1, visita E a tempi
arbitrariamente grandi. Esistono famiglie di ritorni discendenti, ma il primo
ritorno può crescere (`31 → 121`). Le torri di cancellazione producono sorgenti
in E senza discesa per un orizzonte arbitrariamente lungo. Le loro formule
universali sono formalizzate; il loro endpoint non è automaticamente un primo
ritorno a E.

**Torre speciale.** Il ramo successivo studia

\[
Q_v=\frac{9^{2^v}-1}{2^{v+3}},\qquad
H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,
j_v=J_{Q_v}(H_v),\qquad \Delta_v=j_{v+1}-2j_v.
\]

Un criterio sufficiente trasforma conteggi finiti in visite sotto le sorgenti
originali `N_v=(2^(3·2^v−5)−11)/3`. Le verifiche finite arrivano a `v=24`;
non sono tempi di arrivo a 1. Il criterio generale Syracuse e un trasferimento
quadratico condizionale sono formalizzati; la procedura modulare specifica e
le prove sulle ultime trasformazioni digitali non lo sono integralmente.
La candidata `Δ_v≤2·2^ceil(v/2)` per ogni `v≥16` resta aperta.

**Predecessori e due semi.** Una stima formalizzata controlla l'occupazione
pesata di un bersaglio R senza assumere convergenza o nonperiodicità.
L'identità `S(4n+1)=S(n)` produce due semi distinti, almeno uno dei quali non
ritorna a sé stesso: una funzione è iniettiva sui propri punti periodici.
Questo non decide quale seme funzioni, né esclude cicli del successore.
La libreria principale dà conteggi condizionati a ipotesi analitiche esplicite.
Un overlay separato compone questi lemmi con la catena analitica esterna di
Lech Mazur e migliora le precedenti costanti uniformi mediante semi compatti
e decadimento di ordine sei. Il teorema esterno e il mixing restano attribuiti
alla loro fonte. Densità positiva dei predecessori non significa convergenza
di ogni orbita.

## 3. Dove si trova l'ostacolo

La ricorrenza `Q_(v+1)=Q_v+2^(v+2)Q_v²` conserva esattamente la precisione
2-adica. Composta con la codifica delle parità, trasporta tutte le possibili
code di un cilindro: non ne limita il peso. La generalizzazione con parametro
dispari libero `q`, già formalizzata, realizza ogni suffisso finito ammissibile
per parametri arbitrariamente grandi. Ciò non costruisce un unico intero con
un suffisso infinito prescritto e non riguarda automaticamente `q=1`.

Le fasi successive distinguono bene identità e stime, ma non colmano il ponte:

- La conversione aritmetica di un blocco sfavorevole è esatta. La specifica
  specializzazione del bound 2-adico di Chim risulta troppo grande per
  escluderlo; non è un teorema di impossibilità per tutta l'analisi 2-adica.
- Due antenati interi, binade e parola inferiore effettiva completa isolano
  `Q_v`. L'unicità non stima le parità. Conservare invece il solo margine,
  sette antenati e le congruenze ternarie proposte fallisce al livello 11.
- Il primo difetto ternario ammette una stima uniforme su carta
  `O(sqrt(m)·log²m)`. La propagazione delle colonne originali è esatta, ma
  il bound perde efficacia molto prima dell'orizzonte richiesto. Le code
  adattive e il confronto fra tempi diversi restano da controllare.
- Il bilancio completo delle code ricostruisce il conteggio: non è una sua
  maggiorazione. I limiti di memoria dimostrati riguardano input generici,
  non escludono ogni argomento specifico sulla torre.
- Per i certificati basati sui prefissi, il massimo compatibile è esattamente
  `K−2j_L−Z_U(M)`. I riporti già esposti non aggiungono informazione. Un
  singolo riporto futuro aggiunge una fascia lineare sui bit, ma fallisce
  anch'esso come certificato: a `v=16` un testimone conserva l'intera parola
  inferiore, i bit alti e il riporto richiesto, con `Δ=31168>512` e margine
  `−28858`. La torre ha invece `Δ=−479`. Non è un controesempio a Collatz.

## 4. Ipotesi che non vanno presentate come riduzioni risolutive

`UniformStrictDescentHypothesis` è ancora aperta. Per ogni dispari positivo
diverso da 1 chiedere un iterato strettamente minore è equivalente alla
congettura, usando induzione forte in un verso e l'arrivo a 1 nell'altro.
L'esistenza di `SectionReturn.RankDescent` è formalmente equivalente a Collatz
accelerata. Non è un'ipotesi più debole ottenuta grazie alla sola sezione.

L'esclusione di **tutte** le parole non eventualmente periodiche dai positivi
equivale invece alla sola assenza di orbite illimitate: resta distinto il
problema dei cicli. Le ipotesi A0 coprono soltanto la loro famiglia. Il bound
sui `Δ_v` è sufficiente per i certificati della torre, non è dichiarato
equivalente a Collatz. Il telescopio
`m_(v+n)=2^n(m_v−Σ Δ_(v+i)/2^(i+1))` è equivalente al corrispondente margine:
senza un limite indipendente sulla somma non produce informazione nuova.

## 5. Una candidata diversa: confronto relativo dei bacini

La discussione del reset propone di riusare il ramo dei predecessori in modo
più sostanziale. Sia `B(n)` il bacino dei predecessori ordinari positivi di n
e `d_*(B(n))` la sua densità naturale inferiore. Per n dispari non divisibile
per 3, scegliamo `y=4n+1` se `n≡1 mod3`, `y=16n+5` se `n≡2 mod3`.
Allora `3∤y`, `S(y)=S(n)` e `y≤16n+5`.

Il nuovo **lemma richiesto, non dimostrato**, sarebbe l'esistenza di una
costante universale c>0 tale che, quando n e questo y non hanno ritorni
positivi,

\[
d_*(B(y))\ge\frac{c}{1+\log n}\,d_*(B(n)).
\]

È un confronto relativo fra i soli fratelli selezionati. Senza restrizione
sulla scelta/altezza di y, il medesimo enunciato per tutti i predecessori con
lo stesso successore è falso: infiniti fratelli nonperiodici avrebbero bacini
disgiunti e un identico lower bound positivo.

**Riduzione condizionale verificabile su carta.** Su un'ipotetica orbita
Syracuse illimitata `x_i`, i bacini `B(x_i)` sono crescenti e hanno densità
inferiore almeno `d_*(B(x_0))>0`, usando il risultato analitico esterno con
`3∤x_0`. I fratelli selezionati `y_i` sono fuori dall'orbita e i loro bacini
sono disgiunti. Inoltre `x_i≤2^i x_0`. Il lemma darebbe una somma armonica
divergente di densità inferiori di insiemi disgiunti, impossibile. Per questo
ragionamento bastano le unioni finite: non si scambia un liminf con una
somma infinita. Si escluderebbero orbite illimitate, non cicli non banali.

L'input esistente dà positività assoluta con costanti molto piccole, non
questo rapporto uniforme. Una verifica di conteggi finiti non certifica né
confuta direttamente densità asintotiche senza errori o soglie efficaci.
Una prova mediante parole inverse identiche è già esclusa aritmeticamente:
sostituire n con y cambia una sorgente a profondità k di
`2^A(y−n)/3^k`, non intero per k≥1. Servirebbe confrontare famiglie diverse
di parole. Non sappiamo se il confronto relativo sia vero; non ne è
accertata l'originalità. Il criterio di arresto è non avviare un censimento
estensivo in assenza di un primo confronto uniforme con costi controllati.

## 6. Decisione e pilota sui ritorni

Proponiamo di congelare il ramo dei filtri e sottoporre a revisione separata
i risultati positivi locali e quelli quantitativi sui predecessori. Se si
vuole ancora sondare la direzione universale, l'oggetto pertinente è una
composizione di **ritorni effettivi a E**, con dominio e copertura dichiarati.
Non basta una macro che termina fuori da E o che presuppone già la discesa.

Un lemma pilota non tautologico, qui derivato su carta e non ancora
formalizzato in questa nota, è la seguente famiglia:

\[
n=205087+1179648t\quad(t\ge0),\qquad
S^5(n)=778693+4478976t>n,\qquad
S^6(n)=146005+839808t<n.
\]

Gli esponenti sono `[1,1,1,1,2,4]`; n e `S^5(n)` sono `13 mod18`,
`S^6(n)` è `853 mod1152`, e nessuno dei primi quattro intermedi appartiene
a E. Sono quindi due primi ritorni consecutivi, il primo crescente e la
coppia discendente. I domini si ricavano da congruenze esatte, non da una
stima assunta sul conteggio. La prova e i limiti sono nella mappa allegata.
Si tratta di un pilota locale classico, non di una novità rivendicata o di
evidenza che esista un'induzione globale.

**Criterio di arresto:** ottenere soltanto questo certificato universale di
famiglia, verificare se aggiunge davvero sorgenti alla copertura esistente
e registrare esplicitamente il complemento non coperto. Non aumentare
orizzonte, modulo o lista di famiglie per inseguire i casi residui. La ricerca
globale riparte solo se emerge un meccanismo a parametri non limitati che
riduca quel complemento con un rango ben fondato. La via dei due semi rimane
un possibile progetto autonomo di risultati quantitativi, senza promesse su
Collatz universale.

## 7. Materiale e quesiti al revisore

Lettura minima: [v6, sorgente](../../paper/collatz_spectral_reduction_v6.tex),
[stato Lean](../../lean/STATUS.md), [sezione e torri](../post_v6_section_2026-09-24/RESULTS_IT.md),
[due semi](../post_v6_adapter_2026-09-24/RESULTS_IT.md),
[ottimizzazione](../post_v6_optimization_2026-09-24/RESULTS_IT.md),
[margine](../post_v6_margin_2026-09-25/RESULTS_IT.md),
[ultimo controesempio](../post_v6_carry_constraint_2026-09-26/RESULTS_IT.md)
e [mappa critica](CRITICAL_MAP_IT.md).

Chiediamo: i quantificatori e i domini sono corretti? Il risultato sui
predecessori conserva le ipotesi della catena analitica originale? Esiste un
confronto relativo dei bacini pertinente al lemma proposto, oppure un
ostacolo noto? La stima
ternaria locale ha un uso autonomo, anche senza propagazione orbitale? È
motivato cercare una grammatica di ritorni con parametri non limitati, oppure
il materiale attuale giustifica soltanto una sistemazione dei risultati?

I replay storici usano Lean/Mathlib fissati e, nell'overlay, una diversa
toolchain. Gli audit selezionati riportano i tre assiomi standard; alcune
vecchie prove finite usano `native_decide`. Il dossier non sostituisce la
migrazione della toolchain, il controllo delle dipendenze o una revisione
umana della matematica. Queste attività devono avere evidenze proprie.
