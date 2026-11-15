# T11 Revisione indipendente degli enunciati e del perimetro formale

15 novembre 2026. Lettura iniziata alle **20:58:18 UTC**. **Esito: nessun errore di specifica materiale trovato nei sei nuovi moduli.** Due precisazioni documentali sono state comunicate al coordinatore; non richiedono modifiche alle prove.

Questa è una revisione semantica delle definizioni, degli enunciati e del loro impiego. Non ripete la compilazione, l'audit degli assiomi o un controllo del kernel indipendente. La ricevuta di integrazione precedente resta la fonte per quei risultati. Tutti i sei sorgenti letti hanno hash identici alla sua fotografia.

## Precisazioni documentali azionabili

1. Nel `README.md` della radice, introduzione del 15 novembre, la frase «universal finite-orbit reciprocal budget <81» deve esplicitare **finite injective shortcut trajectories**. L'iniettività è un'ipotesi essenziale del teorema: un giro di ciclo senza ripetizioni è ammesso, iterare un ciclo con molteplicità non lo è. `lean/README.md` e `lean/STATUS.md` la esplicitano già correttamente.
2. In `ROOT_HEIGHT_IT.md`, sezione sul prodotto, «positività della sua costante affine» può essere precisato in **nonnegatività**. La prova richiede C(w′)≥0; la parola vuota, ammessa dai teoremi, ha C=0. Il risultato d'altezza rimane valido anche in quel bordo.

Non ho modificato tali file. Alle 21:03 UTC il coordinatore ha confermato di avere applicato entrambe le precisazioni. Non emergono richieste di riparazione del codice Lean.

## Domini controllati

| Modulo | Risultato effettivo e limite verificato |
|---|---|
| `OrbitReciprocal` | T è la shortcut `n/2` o `(3n+1)/2`, importata da `ShortcutCoverage`. Il risultato finale usa soltanto positività della sorgente e iniettività degli indici `0,...,length−1`. La somma è sul finset degli stati distinti. Non rimane alcun input numerico `hwindow`, né entropia o stima esterna. |
| `FirstArrivalBudget` | Il primo arrivo generico è iniettivo **incluso l'endpoint**. Il clock accelerato è strettamente crescente per sorgenti dispari; gli interni degli episodi shortcut sono pari. Il pullback degli hit richiede esplicitamente un target dispari. La somma S esclude l'endpoint, mentre il segmento T usato lo include: la dominazione è conservativa e valida. Il tempo zero e un target periodico al suo primo arrivo non creano eccezioni. |
| `WordProductEnvelope` | Il prodotto locale è esattamente `2^A n/(3^k u)`. Il limite esponenziale generico ha il budget come ipotesi; il successivo modulo lo scarica per i primi arrivi. Le immagini sono **date** da parole esatte. Né esistenza, matching, massa uscente, iniettività delle immagini o densità vengono prodotti. Il caso di profili differenti espone la comparazione incrociata dei coefficienti omogenei. |
| `TwoEditSparsity` | Le quattro identità/divisibilità sono aritmetiche condizionali alle due equazioni affini. Nel segno negativo P indica il totale **nuovo** fino all'edit e B il totale vecchio dopo l'edit. La differenza di notazione dal rapporto T02 è dichiarata e coerente. Il quinto lemma prova il budget `2^A endpoint≤4^k source`. Evertse, nonnullità del residuo nell'applicazione e il limite asintotico non sono nuovi assiomi o conclusioni Lean. |
| `TraceDensityBridge` | Le quattro dichiarazioni sono algebra su reali, con identità della traccia, confronto dei pesi e Harnack come ipotesi esplicite. I costi `κ/(RPL)` e `c/(PL)` hanno l'orientamento corretto. La versione aggregata usa E(y)/y e mantiene la normalizzazione nell'ipotesi. Per applicarla ai bacini occorrono ancora le identità esterne nel dominio corretto, inclusa l'assenza del fattore ciclico. |
| `CycleMinimumProduct` | Il minimo M è un lower per **tutti** gli stati della parola prima dell'endpoint; nel caso chiuso l'endpoint coincide con il primo. La cancellazione richiede n>0 e il log richiede M>0. La parola vuota produce soltanto una disuguaglianza banale. Non sono importati Rhin, una verifica fino a 2^71, un limite sul numero di minimi locali o un'esclusione generale dei cicli. |

Una parola immagine positiva dispari nel senso fisico è un caso degli enunciati d'altezza, che ammettono anche un dominio S più ampio. Tali enunciati non certificano da soli che una sorgente arbitraria appartenga al bacino della mappa ordinaria; la parità e il ponte dinamico restano da fornire nell'applicazione. La documentazione esaminata non compie quel passaggio indebito.

## Verifica indipendente della costante

Ho ricalcolato con razionali esatti, senza eseguire il programma T01:

- ragione heavy `3125/3456`, somma dei cinque coefficienti `3271/576`;
- ragione light `27/32`, somma dei cinque coefficienti `51/16`;
- budget temporale al più 2 e correzione del livello zero pari a 1.

La costante conservativa è quindi

`1+(3271/576)/(1−3125/3456)+(51/16)/(1−27/32)=133547/1655≈80.69305136<81`.

Il fattore finale `exp(27)` è coerente con il prodotto di `1+1/(3x_i)` e la somma reciproca minore di 81. Il sibling canonico soddisfa `y≤16n+5≤21n` per n≥1, quindi il fattore `21 exp(27)` è uniforme. La grandezza della costante non è una stima di massa o di complessità computazionale.

## Documentazione, conteggi e dipendenze

Ho verificato tutte le **51** voci dell'indice del 15 novembre: nomi e numeri di riga puntano alle corrispondenti dichiarazioni nei sei sorgenti. Il conteggio per modulo è 19, 7, 13, 5, 4, 3. Gli hash coincidono con `verification/integration_receipt.json`, che registra build incrementale fissata e audit transitivo di 130 dichiarazioni, comprese 13 encoded-private.

README, STATUS e indice distinguono i risultati del 13 novembre da quelli del 15: la vecchia dipendenza dal bound di finestra resta nel solo `FiniteOrbitTransfer`, mentre il nuovo risultato globale usa `OrbitReciprocal`. La documentazione conserva Lean/Mathlib 4.29.1 e non presenta gli audit esterni Valbuena/Alick come replay locali. I teoremi su carta T02/T04 e T08 non vengono contati fra i 51 teoremi Lean.

Il budget e il prodotto riguardano traiettorie di interi positivi. Non sono un bound per traiettorie 3-adiche Haar generiche, né una stima dell'energia della legge stazionaria. Questa distinzione è stata comunicata a T09 e T10. Le conclusioni H, η e Collatz restano aperte.

La ricevuta della revisione è `research/research_sprint_2026-11-15/t11/semantic_review_receipt.json`. Essa conserva gli hash letti, il controllo delle 51 righe dell'indice e il calcolo razionale; non va confusa con una nuova compilazione delle prove.


## Appendice: controllo indipendente della fonte del 14 novembre

Dopo la revisione formale, il coordinatore ha assegnato un controllo distinto di Lyapunov Weaver, *Exact critical tail and linear collision energy for the ternary Syracuse law*, rStation collatz146/v1, manoscritto del **14 novembre 2026**. Il collegamento diretto della pagina e quello /v1 non erano leggibili con il browser testuale; le sezioni indicizzate erano accessibili. T10 ha poi recuperato l’intero Markdown mediante il collegamento pubblico versionato di download:

[Markdown primario, versione1](https://rstation.ai/api/v1/papers/collatz_146/versions/1/download), [pagina primaria](https://rstation.ai/problems/collatz/papers/146).

Ho letto il file completo `/tmp/collatz_t10_paper146.md`, SHA-256 `ff3c011022cd87f7f068c30759b732e7b92bb24f9269856dba4e851491c3e150`, 27.097 byte. Non ho eseguito il supplemento né ricompilato una formalizzazione esterna. La fonte dichiara CC BY4.0 per manoscritto e dati; la sua accettazione sul sito non viene assimilata a una revisione umana di rivista.

### Due cap differenti

Il cap B del manoscritto146 riguarda `sup_j A_j`, massimo del moltiplicatore reale `A_j=3^j2^{−D_j}` della parola casuale. Non è il cap M sugli esponenti individuali `e_i≤M` usato dal no-go T08. La regolarità L³ della densità a moltiplicatore limitato non contraddice la densità zero dei predecessori con valutazioni limitate. I due oggetti e le due misure vanno mantenuti distinti.

### Esito del nucleo weak-L²

**Non ho trovato un errore bloccante nella prova scritta delle sezioni2–6, entro il perimetro degli input citati.** Il lemma di supporto ritardato della sezione5 ha una prova effettiva; non è stato adottato dalla sola enunciazione o dai controlli finiti.

La ricostruzione indipendente ha controllato questi passaggi:

- La fase a cap fisso usa la spaziatura dei numeratori e l’input analitico di mixing di Tao per ottenere una densità troncata in L³. Ho letto l’enunciato primario di [Tao, Proposizione1.14](https://www.cambridge.org/core/journals/forum-of-mathematics-pi/article/almost-all-orbits-of-the-collatz-map-attain-almost-bounded-values/1008CC2DF91AF87F66D190C5E01C907F): l’esponente polinomiale arbitrario richiesto dall’interpolazione è presente. Non ho riprodotto tutta la prova di Tao.
- Il cambio di misura ai primi attraversamenti conserva i pesi corretti. L’overshoot è limitato dal massimo fattore3/2; il potenziale esponenziale del record dà un momento uniforme del rapporto reale offset/moltiplicatore. Il rapporto21/4 e l’intervallo t<4/7 sono coerenti con la trasformazione esponenziale del passo.
- Nel lemma ritardato un prefisso superstite ha un totale più alto di Δ≥1 rispetto al totale del precedente supporto fermato. La spaziatura consente O(2^ΔK) prefissi, mentre ciascuno paga4^−Δ sotto la legge inclinata. Rimane un peso sommabile2^−Δ. La stima Chernoff è uniforme nel livello residuo perché questo è r2^Δ con r in[2/3,1). Non viene assunta l’indipendenza dei supporti sovrapposti.
- La separazione dei piccoli e grandi valori del rapporto reale, seguita dalla partizione secondo il primo supporto, controlla la norma cubica dell’intera somma. L’Hölder pesato e il passaggio monotono da somme finite non scartano i termini incrociati fra lunghezze diverse.
- La stima della coda debole e l’upper lineare dell’energia seguono con layer cake e medie condizionate. La conclusione riguarda Haar e densità dei cilindri.

La fonte è pertanto un **input analitico esterno su carta, controllato nel suo nucleo**, non un nuovo risultato Lean del progetto. I suoi audit a profondità10 controllano interfacce finite e non costituiscono la prova del bound uniforme.

### Cosa non segue dall’energia lineare

La sezione8 usa la nonnegatività degli incrementi e Fatou per ottenere un’interazione limite finita attraverso un **liminf**. Questo non prova un upper uniforme degli incrementi finiti, la loro convergenza o un limite per l’energia divisa per la profondità. La formula di interazione con le iterazioni di4x+1 è già nella fonte: ricostruirla qui non ne fa una nuova scoperta bibliografica.

Ho controllato il perimetro e l’algebra della parte di rinnovo finale, compresa la scelta nonlattice e il passaggio dalla funzione smussata alla coda monotona. Non ho riletto integralmente il teorema di rinnovo esterno citato: la dichiarazione di una costante di coda esatta va quindi conservata come risultato della fonte, con quella dipendenza, e non come un teorema verificato autonomamente da questo audit.

### Impiego corretto nel progetto

La coda debole in L² fornisce una stima per la **media** di ogni cilindro di profonditàm, non per il valore della traccia intera. Se un nuovo lower locale mostrasse che questa media vede una quota θ della traccia g(n) entro `m≤2log₃n−h(n)+O(1)`, con h(n)→∞ e costanti uniformi, allora il rapporto g(n)/n tenderebbe a zero. Il lower locale e il controllo del suo tempo restano da dimostrare. Nessuna parte della fonte146 li fornisce, né costruisce η o H.

Questo distingue tre stati: nucleo analitico esterno letto e ricostruito; nuovi lemmi formali locali già verificati; rate locale ancora aperto.


## Seguito: settimo modulo `IntegerAtomTilt` e localizzazione del cutoff

Il seguito è stato richiesto dal coordinatore dopo la conclusione della revisione iniziale. **Il dato storico dei sei moduli, 51 teoremi pubblici e 130 dichiarazioni già verificati rimane invariato.** Qui si aggiunge una lettura semantica del nuovo modulo; compilazione e audit aggregati aggiornati sono responsabilità del coordinatore e non sono dichiarati completati da questa nota.

### Nucleo finito letto

`IntegerAtomTilt.lean` contiene tre teoremi pubblici. Il primo dà un budget≤2 per la somma dei reciproci quadrati di un finset di naturali. Il termine0 vale0 secondo la divisione di Lean; il teorema applicativo impone comunque sorgenti strettamente positive. Il secondo limita il peso omogeneo di una singola parola effettiva al suo target positivo. Il terzo prova

`Σ_(w∈W) ω(w)^2 ≤2n²`

per un catalogo **finito di parole effettive della stessa lunghezza**, tutte con endpoint n>0 e sorgenti positive.

La prova è coerente con il risultato dichiarato. Parole distinte della stessa lunghezza dalla stessa sorgente esatta sarebbero uguali per determinismo, quindi la funzione sorgente è iniettiva. Il potenziale di una singola parola fornisce `ω(w)≤n/source(w)` senza alcuna ipotesi di nonritorno. La somma dei quadrati si riduce pertanto al budget dei reciproci quadrati. Il catalogo è un finset di parole, non di etichette duplicate; non vi è moltiplicazione artificiale della massa.

La parola vuota è ammessa e dà al più un termine1; n≥1 rende il bound valido. Un target ciclico è ammesso: non si usa il budget81 o l’iniettività di un segmento di orbita. La sola iniettività necessaria è quella delle sorgenti a lunghezza fissata. **Non ho trovato un difetto di specifica nel nuovo enunciato.**

### Collegamento probabilistico, ancora su carta

Per un intero positivo **dispari** n, il dizionario affine identifica ciascun prefisso di codice che contribuisce al cilindro n modulo3^m con una sorgente intera positiva, invertendo l’ordine della parola. Ogni prefisso più corto ha la stessa proprietà. Dall’identità `n=B_i+A_iY_i` con Y_i≥1 segue A_i≤n. La parità del target non va omessa nell’identificazione con parole Syracuse esatte.

Sotto la legge inclinata `P_*(e=j)=3/4^j`, il contributo atomico di ciascuna parola al livello m, normalizzato con il fattore3^m, è proprio il quadrato del suo peso omogeneo. Il bound finito si estende alla somma numerabile per monotonia. Si ottiene la maggiorazione necessaria alla localizzazione con costante2n², uniformemente in m.

Se B>n, nessuno dei prefissi così identificati ha già attraversato il livello reale B. Il suffisso non usato è indipendente. Il prodotto futuro dei moltiplicatori, sotto la legge geometrica originaria, è una martingala nonnegativa di media1; la probabilità di un attraversamento futuro del livello B/A_m è al più A_m/B. Sommando sui prefissi, il nuovo bound quadratico paga il costo. Con C_m(n)=n+3^mZ₃, su carta risultano

`0≤ρ_m(n)−3^m σ_B(C_m(n))≤2n²/B`,

`σ_B(C_m(n))≥(1−n/B) μ(C_m(n))`.

Le due formule riguardano il cutoff **infinito** del moltiplicatore: non sostituiscono impropriamente il massimo sui primi m passi al massimo su tutti i passi. Il primo usa il tilt atomico; il secondo segue già dal bound A_m≤n.

Il modulo finito non importa questa legge casuale, Doob, il cutoff infinito, un limite di traccia o una stima weak-L². Il ponte probabilistico richiede ancora le identificazioni appena dichiarate e rimane una deduzione su carta. Le disuguaglianze sono uniformi nella profondità, ma **non danno un tempo al quale la media del cilindro approssimi la traccia g(n)**. Non chiudono H o il criterio di rilassamento.
