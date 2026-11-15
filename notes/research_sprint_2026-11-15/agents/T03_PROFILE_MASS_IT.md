# T03 — Massa relativa, traccia aritmetica e limiti di cilindro

15 novembre 2026. Il confronto relativo H rimane aperto. Il risultato
concreto di questo attacco è un ponte condizionale verso una nuova fonte
pertinente, con quattro lemmi algebrici Lean, una diagnosi controllata dei
due limiti e un accoppiamento locale esplicito degli alberi inversi.

## Fonte verificata nel suo perimetro

È stato individuato il repository di Lucas Valbuena,
[Collatz basin densities and Syracuse laws](https://github.com/x1xhlol/collatz-two-coordinate-obstruction),
fissato al commit `a7275d5a73814d3d9a400c6fe6577de9542b03a3`
(8 ottobre 2026, 12:48:51 UTC). È nuovo per questa analisi, non un lavoro
pubblicato dopo il precedente sprint. I testi e i sorgenti selezionati sono
archiviati in `research/research_sprint_2026-11-15/t03/sources`, con licenze,
attribuzioni e SHA-256. Nessun sorgente esterno è stato eseguito o importato.

La fonte dichiara l'esistenza della densità naturale d_N di ogni bacino e
un lower bound uniforme c/N per i target positivi non multipli di3. Fornisce
inoltre una traccia aritmetica g identificata ai positivi con un envelope
stazionario E. I record pubblicati riportano build e controlli del kernel,
con i tre assiomi standard; il nostro lavoro è un audit statico dei testi,
dei due teoremi finali e dei record, non un replay locale esterno.

Il record census contiene51 moduli,1697 costanti,89 private, tutti gli exit
code registrati a0. Gli hash dei due moduli finali acquisiti coincidono con
quelli del record. Il record envelope contiene1620 moduli,3242 comandi,
36651 righe di audit e36539 nomi distinti. In entrambi i record non sono
emersi assiomi estranei a `propext`, `Classical.choice`, `Quot.sound`.
Toolchain esterna4.30.0-rc2, diversa dalla4.29.1 del nostro progetto.
I dettagli sono in `sources/source_review.json`.

## Il ponte preciso verso H

Per un target senza ritorni, siano P_N(q) il prodotto di correzione sul
primo arrivo e w_N(q)=1/P_N(q), esteso a0 fuori dal bacino. Definendo D_N
come la media naturale dei pesi, le identità da usare sono

`D_N ≤ d_N ≤ P₀ D_N`,
`E(N)=g(N)=δ N D_N`, con `δ=log(4/3)/2>0`.

Il fattore ciclico vale1 soltanto nel dominio senza ritorni; non va omesso
per un target periodico. Per target dispari, i bacini ordinario e shortcut
coincidono: gli stati saltati dallo shortcut sono pari. Non compare quindi
un fattore2 nella densità di H.

Per n≤y≤Rn e L>0, un confronto trasverso

`E(y) ≥ κ E(n)/L`

implica esattamente

`d_y ≥ κ d_n/(R P₀ L)`.

Viceversa, `d_y≥c d_n/L` implica `E(y)≥c E(n)/(P₀L)`.
Ponendo y=h(n), R=21 e L=1+log n, H è dunque equivalente, a costanti
universali, a una disuguaglianza di Harnack **trasversa** fra i valori
aritmetici dell'envelope. Il nuovo bound P₀<exp27 di T01, una volta
verificato nel suo perimetro, rende esplicita la perdita del ponte.

Il modulo `lean/CollatzShadowing/TraceDensityBridge.lean` dimostra solo
questi passaggi algebrici, con tutte le ipotesi in ingresso. Non asserisce
la comparazione di E e non importa la fonte. I quattro teoremi sono
`density_of_trace_comparison`, `trace_of_density_comparison`,
`density_of_trace_floor_and_upper` e
`summed_density_of_normalized_trace_comparison`.

La compilazione locale finale termina con exit0 e log vuoto; nessun
`sorry`, `native_decide` o assioma è introdotto. Il receipt in
`research/research_sprint_2026-11-15/t03/trace_density_bridge_receipt.json`
fissa l'hash del sorgente compilato. L'audit delle dipendenze delle quattro
radici e l'integrazione nell'entrypoint spettano al controllo del coordinatore.

L'ultimo usa la normalizzazione appropriata per un pool F:

`Σ_(y∈F) E(y)/y ≥ (κ/L) E(n)/n`
`⇒ Σ_(y∈F) d_y ≥ κ d_n/(P₀L)`.

Per dedurne una contraddizione tramite somma di densità, la disgiunzione
dei bacini del pool è un obbligo aggiuntivo, già separato nei moduli del
precedente sprint.

Un floor uniforme E≥b insieme con E(n)≤C(1+log n) basterebbe per H.
Quest'ultimo upper bound NON è fornito dalla fonte. Il coordinatore ha
anche individuato un serio controtest: le iterazioni della branca inversa
di esponente1 danno

`E(2·3^k−1) ≥ (3/2)^k E(2^(k+1)−1)`.

Con il floor, un upper logaritmico su tutti gli interi è impossibile.
Questo non è una confutazione nel dominio ristretto senza ritorni: la
nonperiodicità di una famiglia infinita di tali target non è stata provata.

## Accoppiamento locale degli alberi inversi

Per un target dispari t non multiplo di3, tutti gli esponenti inversi
ammissibili hanno forma `a=a₀(t)+2j`, j≥0, con a₀ in{1,2}. Fra i tre
residui di j modulo3, uno produce un figlio multiplo di3, cioè una foglia
dell'albero inverso, e due producono nodi che possono continuare.

Se d₀<d₁ sono i due residui interni, l'r-esimo figlio interno ordinato usa

`j=3 floor(r/2)+d_(r mod2)`.

Per due target, i due elenchi ordinati di residui differiscono per al più1
in ciascuna posizione. Accoppiando gli r-esimi figli interni si ha perciò
`|b−a|≤3`. Accoppiando separatamente le r-esime foglie, `|b−a|≤5`.
È una costruzione locale esatta e biiettiva. Per target senza ritorni non
si creano duplicazioni fisiche fra profondità differenti.

Il problema è il drift cumulativo: il limite locale dà soltanto
`|A'−A|≤3k` lungo k nodi interni. La perdita di altezza può quindi crescere
come8^k, pur avendo il prodotto di correzione uniformemente limitato.
L'isomorfismo locale non fornisce H. Un eventuale trasduttore adattivo deve
controllare la somma degli shift, mantenendo insieme iniettività e massa.

## Il kernel inverso reale e il limite della nuova legge del clock

In termini della traccia, la probabilità di una branca inversa reale è

`p_a(z)=3·2^(−a)g((2^a z−1)/3)/g(z)`.

Per i due siblings n,h(n), il rapporto delle probabilità delle due branche
è `2^(a_n−a_h)g(h(n))/g(n)`, e `a_h−a_n` vale2 o4. H richiede quindi
un controllo logaritmico degli odds di due branche di questo stesso
kernel, non un confronto fra due cammini geometrici indipendenti.

Su un ipotetico forward spine divergente u=u₀,u₁,..., la probabilità che
il kernel inverso, partendo da u_j, ripercorra esattamente j passi fino a u
telescopa a

`D_u / [P(u→u_j) D_(u_j)] ≥ D_u/P₀ >0`.

Una legge quasi sicura del clock con **root fissato** non contraddice
questo fatto: qui il root varia con j. Servirebbe un controllo uniforme
nel target, o una comparazione trasversa equivalente a H. Non si può
sostituire l'uno all'altro scambiando i quantificatori.

## Diagnostica congelata dei cilindri stazionari

Il [protocollo](T03_STATIONARY_PROTOCOL_IT.md) fissa prima del calcolo
m=1,...,12; k=1,...,10; n_k=2·3^k−1 e h(n_k)=16n_k+5; controlli fissi
−1,−5,−17,−11. Lo script `t03/stationary_cylinders.py` risolve il ciclo
delle potenze di2 modulo3^m usando l'equazione stazionaria binaria.

Tutti i12 livelli superano i controlli di supporto, positività, massa e
residuo funzionale. A m≤4, massa ed equazione sono verificate anche con
Fraction e uguaglianze esatte. Gli output normale e con Python ottimizzato
coincidono byte per byte; SHA-256 dei dati:
`9f08259611c163083164f2131af90cabd57f2907d9ffdfc2e5030604788cbb7d`.

A m=12, rho_m(−1)≈189.59 e rho_m(−11)≈0.280. Per k=10, n=118097 e
h=1889557 danno rho_m≈142.59 e0.722, mentre le medie Cesàro sulle dodici
profondità sono≈40.33 e0.491. Questi numeri indicano una forte asimmetria
finita; non sono bounds sulla traccia E.

La fonte identifica la traccia mediante un limite di profondità a target
fissato. Sulla diagonale k≥m, invece, n_k è identico a−1 modulo3^m e h(n_k)
è identico a−11: il target cambia insieme con la risoluzione. Inoltre la
semicontinuità inferiore, anche se E(−11) fosse finito, non darebbe un
upper bound lungo questa successione. Nessun caso è stato promosso a
controesempio di H e non è stata estesa la griglia dopo i risultati.

## Cosa cambia nella prosecuzione

La conservazione esatta di(k,A) resta una via possibile, ma non è stata
ottenuta una minorazione delle capacità relative dei profili. La nuova
fonte permette di formulare un obbligo più diretto: confrontare i valori
effettivi della traccia su siblings o la loro massa normalizzata su pool
non ricorrenti. Positività assoluta, regolarità Haar e decadimento Fourier
globale non forniscono automaticamente tale confronto atomico.

Il passaggio più promettente da isolare è un controllo quantitativo
uniforme dei due odds del kernel inverso reale, oppure un Harnack
aggregato che conservi la massa di base. Il bound locale sugli shift e la
diagnostica degli spike sono strumenti per tentare e confutare proposte
in questa direzione, non una prova della quota eta.
