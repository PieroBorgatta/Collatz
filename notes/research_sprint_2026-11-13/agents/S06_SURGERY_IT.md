# S06 Trasformazioni bilanciate di due esponenti

13 novembre 2026. Ricerca su parole effettive che raggiungono target fissati, con confronto diretto con S04 sul dizionario di realizzabilità, S05 sul carico fisico, S07 sulle uscite e S08 sui pool. La trasformazione esce dal dominio H.2 perché cambia anche la costante affine; non è stata ottenuta una minorazione di massa relativa.

## Nuovo vincolo di località terminale

Sia `w=(a_1,…,a_k)` una parola esatta da u al target n e scegliamo `1≤i<k`. La surgery cambia `a_i` in `a_i+δ` e `a_k` in `a_k−δ`, lasciando positivi tutti gli esponenti e preservando la somma A. Poniamo `P=A_i`, `B=A−P`, `q=k−i`, `T=C(a_(i+1),…,a_k)` e `m=S^i(u)`.

Per δ=d>0 l'identità delle costanti è

`C(w')−C(w)=(2^d−1)2^P T`.

Se la parola modificata termina in y da una sorgente intera v, le identità affini danno

`2^A(y−2^d n)=3^k(v−u)−(2^d−1)2^P3^q m`.

Poiché q≤k e 2 è coprimo con 3, segue la condizione necessaria

`3^q | y−2^d n`.

Per δ=−d<0 la forma scalata è

`2^A(2^d y−n)=2^d3^k(v−u)+(2^d−1)2^P3^q m`,

quindi `3^q | 2^d y−n`. I numeratori non sono nulli per target positivi dispari distinti. Per ogni shift fissato la distanza q dall'ultimo esponente è pertanto limitata esplicitamente dalla valutazione ternaria del numeratore. Per editare una posizione lontana bisogna far crescere lo shift: `3^q≤max(y,2^d n)` nella prima forma, con l'analogo nella seconda.

Questo vincolo è più preciso del solo ostacolo modulo 3 della precedente revisione. Non esclude shift crescenti, molte posizioni modificate o profondità variabile e non prova sparsezza asintotica dell'intera relazione.

## Formalizzazione locale

Il nuovo [WordSurgery.lean](../../../lean/CollatzShadowing/WordSurgery.lean) contiene quattro lemmi: scomposizione di C su concatenazioni, identità della modifica interna, congruenza terminale derivata dalle identità affini e budget di profondità per target dispari distinti. La congruenza è formulata sull'algebra delle identità fornite; la prova completa che ogni surgery rappresentata da un codice soddisfi tali identità resta un adattatore applicativo. Non contiene una stima di densità o un teorema H.

L'elaborazione dedicata è riuscita con **exit 0**; il [log](../verification/s06_surgery_lean.log) contiene soltanto un suggerimento non bloccante `simp` al posto di `simpa`. Nessun placeholder, nuovo assioma o `native_decide` è stato introdotto. Nessun import principale è stato modificato da S06.

## Protocollo numerico congelato

Prima del calcolo sono stati fissati: target n in `{5,7,31,593}`, fratello canonico y, cutoff `{1024,4096,16384,65536}`, shift `δ∈{−5,−3,−1,1,3,5}`, fattori d'altezza `{1,4,16,64}` e cap di 2048 passi per il primo arrivo. Il dominio contiene solo sorgenti **dispari**; i sollevamenti diadici ordinari non vengono contati.

Ogni sorgente u è seguita fino al primo arrivo a n oppure a 1. Ogni parola modificata ammessa deve soddisfare integralità completa modulo `3^k`, positività e disparità; un replay indipendente di tutti i suoi passi controlla le valutazioni esatte e l'arrivo a y. Il codice controlla anche l'identità di ΔC. I conteggi distinguono codici, coppie fisiche `(u,v)`, immagini e sorgenti coperte.

Il [programma](../experiments/s06_surgery.py) e il [risultato JSON](../verification/s06_surgery.json) sono riproducibili. I replay normale e con `-O` coincidono byte per byte: SHA-256 del JSON `9f172a1e976cda65e47419332debaf382b1ced1e6bd055ea5c6c8fcaffd64aeb`.

## Risultati esatti

Nell'unione dei quattro censimenti sono state esaminate **50.694 incidenze sorgente/target**, non altrettante sorgenti distinte tra target diversi. Sono **3.137.835** le modifiche con esponenti positivi; **128.271** superano il vincolo terminale necessario; soltanto **368** producono trasporti effettivi. Tutti i successi osservati hanno lunghezza k≤7. Nessun successo osservato ha v≤u.

Al cutoff 65.536:

| n | y | Sorgenti dispari di base | Codici accettati | Sorgenti coperte con v≤64u | Immagini distinte | Massimo carico da sorgenti distinte |
|---:|---:|---:|---:|---:|---:|---:|
| 5 | 85 | 30.678 | 74 | 61 | 64 | 2 |
| 7 | 29 | 6.356 | 149 | 125 | 142 | 2 |
| 31 | 125 | 3.036 | 137 | 128 | 132 | 2 |
| 593 | 9493 | 10.624 | 8 | 8 | 7 | 2 |

Per n=5 e 593 nessuna immagine soddisfa v≤16u; per n=7 e 31 nessuna soddisfa v≤4u. Queste soglie sono finite e prespecificate: non sono limiti universali d'altezza.

Il costo delle collisioni è reale. Per n=593, le sorgenti 16853 e 16867 hanno parole `[7,1]` e `[1,7]`. Con shift rispettivamente −3 e +3 entrambe producono la parola `[4,4]` dalla stessa immagine v=270021 al target 9493. Dunque due sorgenti fisicamente diverse collidono già a k=2 e somma A=8 fissati. Il cap 1 non può essere dedotto dalla sola unicità di una parola a sorgente fissata.

Le valutazioni terminali massime Q_δ sono `{1,3,1,1,2,1}` per n=5, `{1,2,1,1,3,1}` per n=7 e `{4,1,1,2,1,1}` per n=31 e 593, nell'ordine δ del protocollo. Gli edit che superano il primo test sono quindi sempre nelle ultime quattro posizioni. La grande maggioranza fallisce comunque la congruenza completa.

## Un limite di carico su carta

Se y non ha ritorni positivi e l'insieme degli shift è finito, ogni immagine dispari v determina un'unica parola modificata e la sua lunghezza k. Per ogni δ e distanza terminale `1≤q≤Q_δ`, la trasformazione inversa degli esponenti determina al più una parola originale, quindi al più una sorgente u. Ne segue il limite di carico incoming

`M_odd ≤ Σ_(δ) Q_δ`,

indipendente da k e X. Nel protocollo la somma è 9 per n=5,7 e 10 per n=31,593. Questa deduzione non è stata formalizzata in Lean. L'ipotesi di nonritorno di y è essenziale per l'unicità della lunghezza; per target con ritorni serve un diverso budget pesato.

Per shift limitati Q_δ è al più di ordine log n, quindi il solo costo di collisione può essere compatibile con il budget logaritmico desiderato. Rimangono **altezza e quota di massa relativa**. Inoltre il limite riguarda parti dispari: consentire liberamente fattori diadici alle sorgenti ordinarie aggiunge rappresentazioni e richiede una regola di lift o un'allocazione esplicita.

Precisazione dal confronto con il coordinatore: preservare il fattore diadico, `2^e u→2^e v`, mantiene sia il fattore d'altezza sia il carico incoming, poiché un'immagine ordinaria determina univocamente e e la parte dispari v. Il confronto relativo delle masse ordinarie deve però usare il peso effettivo `floor(log₂(X/u))+1` delle sorgenti dispari; le quote non pesate del censimento non possono sostituirlo.

## Decisione

La piccola famiglia di shift fissati non mostra una quota stabile di massa profonda; scalare il cutoff non è giustificato come prossimo passo principale. L'integrazione utile è il vincolo di località terminale e il conteggio del carico dopo identificazione delle immagini. Il tentativo successivo deve dimostrare una minorazione indipendente della quota trasferita o usare una diversa realizzazione a profondità variabile. Se si conserva la stessa famiglia, il primo obbligo è capire perché i successi del censimento restano così poco profondi, senza trasformare l'osservazione k≤7 in un teorema generale.

## Appendice delle 16 29 UTC Carico pesato su tutti gli shift

Proposta del coordinatore, controllata su carta da S06 prima della chiusura dell'esplorazione. Non è una nuova formalizzazione Lean né un risultato globale o una rivendicazione di priorità.

Fissiamo n,y positivi dispari distinti e y senza ritorni positivi. Consideriamo qualunque catalogo finito di surgery effettive, con shift intero non nullo δ, esponenti positivi e totale A invariato. Ogni codice fisico riceve peso `θ_δ=2^(−|δ|)`. Le eventuali copie dovute a metadati devono essere identificate, oppure i loro coefficienti aggregati per codice fisico non devono superare θ_δ.

Una immagine dispari v determina un'unica parola modificata `w'=(b_1,…,b_k)` che termina in y. Per k<2 non esistono edit di questo tipo. Per k≥2, δ e la distanza q dall'ultimo esponente determinano la posizione i=k−q, la parola originale e quindi al più una sorgente u. Le condizioni di positività della parola originale impongono

`1−b_k≤δ≤max_(i<k)b_i−1`.

Gli shift ammissibili sono quindi finiti per ciascuna immagine, anche se il catalogo consente tutti gli interi non nulli. La congruenza necessaria precedente impone inoltre `1≤q≤Q_δ`, dove

`Q_(+d)=ν₃(y−2^d n)`, `Q_(−d)=ν₃(2^d y−n)` per d≥1.

Scrivendo `N=max(n,y)`, i numeratori sono non nulli e hanno modulo al più `2^d N`; dunque

`Q_δ≤log₃N+|δ|log₃2`.

Il carico pesato totale entrante in ogni immagine è al più

`Σ_(δ≠0)2^(−|δ|)Q_δ ≤ 2log₃N+4log₃2`,

perché `Σ_(d≥1)2^(−d)=1` e `Σ_(d≥1)d2^(−d)=2`, contando entrambi i segni. La somma su tutti gli shift è soltanto una maggiorazione di una somma fisica finita; non si assume uno scambio di limiti o di densità. Sul fratello canonico y≤16n+5≤21n, questo dà un costo O(1+log n).

La regola di lift `2^e u→2^e v` conserva il limite di carico: un'immagine ordinaria fissa sia e sia la sua parte dispari. Conserva anche il rapporto d'altezza. L'altezza universale D₀ proposta da S10, se mantenuta con il suo preciso dominio di primo arrivo/iniettività, è quindi compatibile con questa allocazione a totale invariato. La combinazione lascia ancora da dimostrare una minorazione uniforme **della massa relativa con questi pesi**, usando per le parti dispari i corretti pesi degli input ordinari.

### Perché la pesatura non risolve la quota relativa

Nel dominio H anche n non ha ritorni, quindi ogni sorgente u determina un'unica parola originale. Per ogni δ,q vi è al più una nuova immagine. La coda uscente con `|δ|>R` è pertanto uniformemente limitata, per ogni sorgente fisica, da

`2^(1−R) [log₃N+(R+2)log₃2]`,

che tende a zero per R→∞. Ne segue che una minorazione relativa positiva della massa pesata totale deve già essere sostenuta in parte da un insieme finito di shift moderati. La nuova pesatura non aggirerebbe un'eventuale futura prova di sparsezza per ogni shift fissato. Il censimento con |δ|≤5 non dimostra questa sparsezza generale, ma resta un test avversario pertinente.

Il risultato circoscrive meglio il problema del carico; non produce η e non fornisce evidenza che η sia uniformemente positiva.
