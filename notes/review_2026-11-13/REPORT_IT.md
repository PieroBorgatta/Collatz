# Revisione del progetto Collatz e alternative di ricerca

13 novembre 2026. Revisione interna con dieci agenti, coordinata da Codex per Piero Borgatta. Base analizzata: ramo `phase10-wip`, commit `5428e89`; stato iniziale pulito, cinque commit locali oltre `origin/phase10-wip`.

Il progetto ha una base formale consistente e una documentazione utile degli approcci confutati. Il problema aperto rimane il controllo universale delle orbite: nessuna delle riduzioni attuali ne dimostra la convergenza, né offre una misura attendibile della distanza da una soluzione. La scelta più giustificata è concentrare la ricerca su confronti aggregati fra bacini inversi e su famiglie parametriche di ritorni, mantenendo separato il problema dei cicli.

Questa revisione aggiunge analisi e registrazioni delle verifiche. I sorgenti Lean, i certificati generati, i documenti pubblicati e le dipendenze fissate sono conservati.

## Risultati già ottenuti

| Fase | Risultato da conservare | Limite matematico |
|---|---|---|
| Shadowing e precisione | Congruenze esatte, impossibilità di seguire per sempre una stessa parola periodica espansiva, budget di precisione | Cambiare parola durante l'orbita esce dal singolo budget |
| Operatori finiti | Certificati Collatz–Wielandt, inclusi `ρ≤3/4` e `ρ≤97/2000` per matrici specificate | Nessuna approssimazione dell'operatore infinito o conclusione puntuale universale è stata dimostrata |
| Cilindri e barriere | Una parola positiva è realizzata esattamente tramite una congruenza modulo `2^(A+1)`; criterio affine di discesa | Occorre produrre e controllare parole e domini per tutte le sorgenti |
| Sezione aritmetica | Ogni orbita positiva raggiunge 1 oppure una sezione di sei progressioni; se non raggiunge 1, ritorna alla sezione arbitrariamente tardi | Copertura e ricorrenza non garantiscono discesa; l'esistenza del rango proposto equivale a Collatz |
| Torri | Formule universali di cancellazione, trasporto del parametro e realizzazione di ogni suffisso finito ammissibile | La torre speciale non copre tutti gli inizi; un parametro che realizza un prefisso non realizza necessariamente una parola infinita |
| Occupazione e predecessori | Limite universale ai pesi delle visite, conteggi senza duplicare sorgenti, coppie limitate di semi senza ritorno | La libreria principale mantiene esplicite le premesse analitiche; la catena esterna è un progetto separato |
| Bacini fratelli | Disgiunzione e budget finito dei bacini lungo un'orbita iniettiva; fratello canonico di altezza al più `16n+5` | La comparabilità relativa delle densità, chiamata H, rimane aperta |
| Trasporto H.1 e H.2 | Identità aritmetiche Lean e prove su carta dei costi del trasporto | Modificare soltanto l'ultimo esponente produce `o(X)` immagini entro ogni dilatazione fissa: questo metodo non trasferisce una quota positiva di massa |

Le fasi empiriche iniziali sono di aprile–maggio; il nucleo Lean nasce a maggio, i certificati finiti si consolidano fra maggio e giugno e la v6 precede la continuazione del 24–26 settembre. Gli ultimi commit del 26 settembre chiudono prima i filtri della torre, poi le correzioni del solo ultimo esponente. La ricostruzione e i riferimenti sono nelle [dieci analisi](ANALISI_AGENTI_IT.md).

## Verifica eseguita oggi

La compilazione integrata ha avuto esito positivo: **3.380 passaggi, exit 0**. È una build incrementale con le dipendenze installate, non un replay con kernel indipendente. L'unico avviso riguarda un'ipotesi inutilizzata in `SignedTransport.lean:25`.

Sono stati rieseguiti quattro audit stretti: 10 dichiarazioni di `PrefixOptimality`, 14 di `SiblingBasins`, 7 di `LastExponentTransport` e 6 di `SignedTransport`. Tutte le **37 dichiarazioni** dipendono soltanto da un sottoinsieme di `propext`, `Classical.choice` e `Quot.sound`. L'elaborazione fresca di `ExactCylinders.lean` è riuscita.

Il conteggio corrente distingue **43 file d'autore, 13.199 righe e 557 dichiarazioni** da **26 file generati, 43.513 righe e 966 dichiarazioni**. Sono conteggi testuali, non numeri di risultati matematici indipendenti; entrambe le classi sono state prodotte con assistenza AI. Il totale è 69 file Lean e 56.712 righe. Gli import principali coprono 68 file; l'escluso `Inventory.lean` è un quaderno tecnico dichiarato.

La scansione non trova `sorry`, `admit`, `sorryAx`, `unsafe`, `implemented_by` o assiomi dichiarati nel progetto. Esistono nove usi di `native_decide`, confinati a controlli finiti e consentiti dalla CI; non compaiono nelle dipendenze delle 37 radici appena sottoposte ad audit. I [log conservati](verification/) e il [manifest](verification_manifest.json) delimitano la verifica.

Il progetto principale usa Lean 4.29.1; l'overlay analitico usa 4.30.0-rc2 e non è stato ricompilato in questa revisione. Le [note ufficiali di Lean 4.34.0](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/) documentano correzioni successive del kernel. Una replica isolata con una versione stabile aggiornata e Mathlib compatibile è quindi un passo utile per consolidare la verifica; non è stata individuata una dipendenza del progetto dai difetti descritti.

## Approcci da mantenere chiusi

- Il trasporto della stessa parola fra i fratelli scelti fallisce già modulo 3.
- Anche tutte le correzioni firmate del solo ultimo esponente, con fattori diadici liberi, hanno immagine di densità zero a dilatazione fissa. H.2 è una prova su carta sostenuta da sei lemmi Lean, non un teorema asintotico già formalizzato.
- Un accoppiamento puntuale a profondità invariata e dilatazione universale è escluso da famiglie avverse. Cambiare profondità o controllare masse aggregate resta fuori da questo risultato negativo.
- Prefissi, sette antenati e vincoli di riporto aggiuntivi non hanno dato un budget uniforme. I controesempi riguardano le classi ampliate dei test, non la torre esatta né Collatz.
- Aumentare soltanto una matrice, un cutoff o un orizzonte non colma un obbligo infinito. La compensazione `128v²`, pur superando i livelli tenuti separati 22–24, resta una congettura della torre.

Fonti locali: [reset](../post_v6_reset_2026-09-26/RESULTS_IT.md), [mappa critica](../post_v6_reset_2026-09-26/CRITICAL_MAP_IT.md), [H.1](../post_v6_basin_transport_2026-09-26/RESULTS_IT.md), [H.2](../post_v6_signed_mass_2026-09-26/PROOF_IT.md).

## Due inferenze da correggere nelle note spettrali

La [nota sulla weak approximation](../phase10_A0_weak_approximation_theorem_2026-05-25.md), righe 169–185, conclude Cauchy da errori fra scale successive che tendono a zero. Questa implicazione richiede un'ipotesi aggiuntiva. Il kernel a un solo stato

`K_(2^m)=(1+sin(log(m+1)))/2`

è positivo e substocastico: la differenza tra termini consecutivi tende a zero, ma la successione non converge. Servono errori sommabili sulle scale diadiche, una stima tra scale arbitrarie o un vero teorema di convergenza. Se cambiano anche inclusioni e proiezioni, va controllata la loro compatibilità. La clausola A0W7, quando assume già il limite, lo pone tra le premesse; nell'altra lettura non colma il salto.

La [chiusura condizionale Gate10B](../phase10_gate10B_conditional_closure.md), §8.2, dimostra l'identità con Haar per osservabili costanti sui cilindri. Il §8.3 la usa per medie puntuali senza aver dimostrato una proprietà sufficiente degli osservabili concreti. La sola misurabilità non basta: `g=1_(Z₂\N)` ha integrale Haar 1 e valore zero su tutti i rappresentanti naturali. Se la condizione B assume direttamente veri integrali condizionali, la proposizione può conservarsi, ma l'identificazione con il generatore resta da dimostrare. Occorrono cilindricità dopo troncamenti, regolarità appropriata o una stima di discrepanza.

Sono rilievi sulle **note propositive storiche**, non difetti individuati nei teoremi Lean compilati. La [relazione specialistica](AGENTE_04_IT.md) precisa controesempi, quantificatori e possibili riparazioni. Le note originali sono conservate; questi passaggi non vanno usati come lemmi acquisiti.

## Corollari aritmetici utili esplicitati nella revisione

### Arbitrariamente molti primi ritorni crescenti

Per `r,t≥1`, ponendo

`x_j=18t·8^(r−j)9^j−5`, per `0≤j≤r`,

si ottengono r primi ritorni consecutivi alla sezione E, tutti crescenti. Per `j<r`, il punto intermedio è

`y_j=216t·8^(r−j−1)9^j−7`.

Le identità `3x_j+1=2y_j` e `3y_j+1=4x_(j+1)` certificano esponenti esatti `[1,2]`. Gli x sono `13 mod18`, gli y sono `65 mod72` e quindi fuori da E. Inoltre `x_(j+1)−x_j=18t·8^(r−j−1)9^j>0`. Ne segue che neppure un numero fissato di ritorni garantisce discesa. È un corollario delle torri esistenti, esplicitato qui su carta, senza rivendicazione di priorità e senza nuova dichiarazione Lean. [Dettagli](AGENTE_05_IT.md).

### Un budget condiviso per parole con target differenti

Per una sorgente positiva x e un insieme finito W di parole distinte esatte da x, con endpoint positivi `R_w` e peso `ω(w)=3^|w|/2^sum(w)`, l'infrastruttura di dissipazione dà

`Σ_(w∈W) ω(w)/[R_w(3R_w+1)] ≤ 1/x`.

Ogni addendo è la dissipazione al tempo `|w|`; le lunghezze di parole distinte esatte dalla stessa sorgente sono distinte. Il budget aiuta a trattare insiemi di radici senza spendere separatamente una costante per ogni target. Etichette duplicate della stessa parola vanno aggregate. Occorre ancora minorare analiticamente la massa con questi stessi pesi: il lemma non la produce gratuitamente. È una deduzione su carta da risultati Lean esistenti, da formalizzare. [Dettagli](AGENTE_07_IT.md).

### Fattori coprimi della torre

La fattorizzazione

`Q_v=∏_(0≤j<v) (9^(2^j)+1)/2`

espone fattori dispari maggiori di uno, a due a due coprimi. Garantisce nuovi primi all'aumentare di v, ma non controlla il peso delle parità della traiettoria. Non serve invocare Zsigmondy per questa specifica conclusione. [Analisi aritmetica](AGENTE_06_IT.md).

Le tre osservazioni sono state ricontrollate con aritmetica esatta: **180 segmenti di ritorno**, **3.200 identità di dissipazione**, fattorizzazione e coprimalità per **v=1,…,7**. Il [replay](review_checks.py) dà lo stesso [risultato](verification/review_checks.json) con e senza ottimizzazione Python. I calcoli sono verifiche finite delle formule; le argomentazioni simboliche sono quelle sopra, non nuove prove Lean.

## Progressi esterni da integrare con condizioni esplicite

La [bibliografia annotata](FONTI_WEB_IT.md) riporta fonti e stato di verifica al 13 novembre. Gli aggiornamenti più utili rispetto a settembre sono il controllo più esteso dichiarato da ProofAtlas sulla catena dei predecessori, i nuovi punteggi di insiemi di radici nel progetto Shaik e l'attenzione al mixing congiunto di offset ternario e somma delle valutazioni. Sono strumenti da estrarre in enunciati finiti precisi; nessuno fornisce già H.

Il lavoro di Verger-Gaugry caricato il 9 novembre suggerisce un oggetto diverso: onde e fattori primi. L'analisi 6 osserva che l'identità `9(µ+1)−4=4T²(µ)` sembra consentire una deduzione con il teorema classico delle S-unità senza il bound uniforme sulle altezze usato nel risultato citato. È una deduzione interna su carta da sottoporre a controllo della mappatura delle definizioni, non una rivendicazione su una congettura esterna. Anche ottenere infiniti primi lungo un'orbita divergente è compatibile con la sua esistenza.

Il collegamento deve includere il lemma «divergenza implica infiniti minimi d'onda». Una coda senza onde avrebbe tutti gli esponenti Syracuse almeno 2, quindi sarebbe strettamente decrescente sopra 1; una coda di soli passi shortcut dispari è impossibile per un positivo, poiché richiederebbe `2^k | n+1` per ogni k. Questo giustifica l'esistenza di infiniti inizi d'onda prima di usare la finitezza delle S-unità. Non aggiunge un limite al numero dei primi e quindi non chiude il problema.

Per i cicli, la bibliografia deve includere il corrigendum di Hercher, distinto dal risultato principale del 2023. I risultati di Tao rimangono statistici; la soglia verificata della pagina Barina rimane finita. Nessuna di queste informazioni va convertita in una proprietà di tutti gli inizi.

## Alternative ordinate per il prossimo risultato verificabile

| Direzione | Primo risultato concreto | Evidenza che giustifica continuare | Criterio di arresto |
|---|---|---|---|
| Budget per insiemi di radici e trasporto aggregato | Formalizzare il budget normalizzato; poi costruire un flusso finito fra sorgenti e immagini raggiungibili, con altezza e carico controllati | Una minorazione **relativa** alla massa del bacino inferiore per le stesse incidenze | Si confrontano solo due lower bound assoluti, si usa indipendenza non provata o il carico cresce senza compensazione |
| Ritorni parametrici composti | Certificato con dominio, parola esatta, primi ritorni, endpoint e complemento della copertura; comprimere i blocchi crescenti arbitrariamente lunghi | Un'interfaccia d'uscita provata diminuisce un parametro senza assumere discesa globale | Si accumulano progressioni già coperte, si fissa il numero di ritorni o il reset richiede la conclusione |
| Ponte analitico troncato | Dimostrare un errore di raddoppio sommabile su una famiglia finita di rami biaffini con dominio completo | Identificazione esatta del campionamento e controllo separato di profondità, alte valutazioni e bit length | Il drift tende solo a zero, il campionamento usa sola misurabilità o una media viene applicata a ogni percorso |
| Cicli e interfacce diofantee | Lemmi esatti su rotazioni, minimo ciclico e numero dei minimi locali nella mappa corretta | Collegamento verificabile a una classe esclusa o a un nuovo vincolo parametrico | Una sottoclasse è trattata come tutti i cicli o una verifica computazionale esterna viene assunta come teorema Lean |
| Torre e inventario dei primi | Formula dei fattori e primo lemma che colleghi l'aritmetica esatta al deficit di parità | Una nuova disuguaglianza quantitativa valida su una famiglia a lunghezza variabile | La fattorizzazione o l'unicità della sorgente sono usate come se stimassero già le parità |

Le prime due direzioni riusano maggiormente i risultati recenti. Il budget normalizzato è il compito formale più circoscritto; il confronto aggregato è la scommessa matematica a rischio maggiore. Il programma dei ritorni può produrre risultati parziali indipendenti, ma deve trattare la durata arbitraria e le transizioni d'uscita. Nessuna stima di probabilità di risolvere Collatz è giustificata da questi elementi.

## Confronto aggregato fra blocchi di bacini

H chiede un rapporto per ogni coppia di fratelli. Una variante da esaminare può assorbire lo sbilanciamento dei singoli rami: su un'ipotetica orbita Syracuse iniettiva `x_i=S^i(x_0)`, con x_0 positivo dispari e `3∤x_0`, raggruppare i fratelli canonici nei blocchi `2^j≤i<2^(j+1)` e chiamare U_j l'unione dei relativi bacini ordinari.

Un lemma sufficiente sarebbe, per c,D positivi indipendenti da j, eventualmente dipendenti dalla spina fissata,

`|U_j∩[1,DX]| ≥ c |B(x_0)∩[1,X]|−E_j(X)`, con `E_j(X)=o_j(X)`.

Se il bacino iniziale ha densità inferiore δ>0, ogni blocco avrebbe densità almeno `cδ/D`. I blocchi sono disgiunti; applicando il budget a una somma finita di un numero arbitrario di blocchi si ottiene una contraddizione. Il cutoff non deve essere uniforme in j: si fissa prima una famiglia finita di blocchi e poi si passa al limite.

Equivalentemente, per J blocchi fissati si sommano le disuguaglianze allo stesso cutoff DX, ottenendo `DX≥Jc |B(x_0)∩[1,X]|−Σ_(j<J)E_j(X)`. Dividendo per X e passando al limite risulta `D≥Jcδ`, impossibile per ogni J. L'errore resta nullo perché la somma è finita.

Questo è **un obiettivo aperto**, non una stima ottenuta. Richiede una costruzione indipendente che cambi parole o profondità e controlli la massa relativa, non soltanto la positività separata. La conseguenza eventuale sarebbe assenza di orbite non periodiche; i cicli non banali rimarrebbero da escludere. La variante non va promossa a scorciatoia prima di produrre il lemma finito.

Per un singolo confronto, la [revisione del trasporto](AGENTE_08_IT.md) rende esplicito il costo. Se un flusso produce almeno `η_n` volte la massa di base, ha carico massimo `M_n` su ogni immagine e altezza al più `D_n X`, è sufficiente cercare

`D_n M_n / η_n ≤ C(1+log n)`.

Altezza e carico possono dipendere dal target: conta il costo combinato. La formula è un criterio condizionale di doppio conteggio; non costruisce il flusso. Per una versione a blocchi con costi diversi servirebbe una serie divergente dei coefficienti netti, non basta raggruppare i fratelli.

Un vincolo algebrico evita un'altra ricerca inefficace: una modifica bilanciata di due esponenti che preservi la somma e lasci invariato l'ultimo non trasferisce ai fratelli canonici, già modulo 3. Una surgery che conservi la somma deve cambiare anche la parità dell'ultimo esponente; superare questo primo test non dà ancora integrità modulo `3^k` o controllo della massa.

## Il ramo dei cicli richiede una propria interfaccia

La [relazione sui cicli](AGENTE_09_IT.md) distingue il numero dei minimi della mappa shortcut da quello dei minimi della sequenza solo dispari. Per un ciclo non banale primitivo, il conteggio pertinente a Hercher è il numero degli esponenti Syracuse `a_i≥2`; ripetere una parola moltiplica il conteggio e non produce un nuovo periodo primitivo.

Due lemmi aritmetici sono adatti a una prima formalizzazione. Se `D=2^A−3^L>0` e si ruota una parola spostando l'esponente iniziale a in fondo, allora `2^a C_rot=3C_w+D`. I test di divisibilità per divisori di D sono quindi invarianti per rotazione: ripeterli non aggiunge nuovi vincoli. Se ogni membro dispari del ciclo è almeno M>0, il prodotto delle identità dei passi dà `2^A M^L≤(3M+1)^L`. Questa forma intera evita approssimazioni non certificate.

Questi vincoli sono classici o deduzioni elementari dell'infrastruttura; l'obiettivo è integrarli correttamente, non rivendicarne la scoperta. Il limite verificato da Barina resta una premessa esterna finché non viene certificato o importato con il suo preciso confine di fiducia.

## Sequenza operativa proposta

1. Consolidare il punto di partenza: formalizzare i due corollari di dissipazione e primi ritorni, documentare le correzioni delle note condizionali, predisporre una replica isolata del toolchain. Sono risultati circoscritti e controllabili.
2. Fissare il modello finito del trasporto: coordinate congiunte, parole reali, intervalli di altezza, carico massimo e termine d'errore. Congelare le soglie prima di cercare controesempi. Il passaggio non dimostrato resta la massa relativa.
3. In parallelo, certificare un dominio di ritorni composti e una macro a durata variabile, verificando se l'uscita dà una diminuzione parametrica e copertura nuova.
4. Trattare i cicli con un'interfaccia separata e fonti corrette. Non presentare un eventuale avanzamento su H come soluzione della congettura completa.

Non sono stati avviati contatti esterni, pubblicazioni, modifiche alle dipendenze o nuovi livelli della torre. Le proposte indicano il lavoro successivo; le verifiche effettivamente svolte sono elencate nel manifest.
