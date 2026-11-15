# T06 Accoppiamenti inversi, debito di esponenti e massa fisica

15 novembre 2026. Attacco costruttivo all'intero albero inverso, con tre risultati: un criterio locale di ottimalità del matching ordinale, un avversario analitico che esclude un suo costo puntuale uniforme o logaritmico, e una diagnosi esatta del compromesso fra altezza e collisioni per un feedback greedy. **Nessuna quota relativa eta è stata dimostrata. Nessun nuovo modulo Lean è stato introdotto da T06.**

## La costruzione locale e cosa può ottimizzare

Per un target dispari t, non multiplo di3, i due primi esponenti inversi che producono figli ancora non multipli di3 sono:

| t mod9 | c0 | c1 |
|---:|---:|---:|
|1|2|4|
|2|1|3|
|4|2|6|
|5|3|5|
|7|4|6|
|8|1|5|

L'intero elenco ordinato è `a_(2r+s)=6r+c_s`. La verifica usa `I_a(t)=(2^a t−1)/3`; fra tre esponenti della parità ammissibile uno produce una foglia multipla di3. Il matching ordinale fra due nodi associa gli stessi indici. Lo shift locale è al più3 in valore assoluto; il debito totale `d=A'−A` può invece crescere con la profondità.

**Lemma di ottimalità locale.** Fra tutte le biiezioni di due elenchi crescenti di esponenti, il matching ordinale minimizza `sup_r |d+b_(pi(r))−a_r|`, per d fissato. Per due figli, i due shift diretti sono entrambi compresi fra gli estremi dello scambio: `d+b0−a1 ≤ d+b_s−a_s ≤ d+b1−a0`. Lo scambio non diminuisce quindi il massimo dei valori assoluti; non diminuisce neppure la somma dei due costi assoluti.

Per elenchi infiniti, se una biiezione ha costo al più C, i primi r+1 input devono avere r+1 immagini sotto `a_r+C−d`: dunque `b_r≤a_r+C−d`. Applicando lo stesso ragionamento all'inversa si ottiene `a_r≤b_r+C+d`. Quindi anche l'ordinale ha costo al più C.

Il lemma non esclude un controllo con anticipo: accettare un costo maggiore oggi potrebbe cambiare favorevolmente lo stato futuro. Esclude soltanto l'idea che una permutazione locale, scelta per minimizzare il peggior debito immediato, migliori l'ordinale. Nel test la policy `pair_minimax` coincide infatti byte per byte con `ordinal` a tutti i livelli.

## Un avversario analitico dell'ordinale

Costruzione proposta dal coordinatore e verificata indipendentemente da T06, compresi indici, segni e costanti. Il risultato è puntuale, non un no-go di massa.

Partiamo dal ramo inverso negativo minimo interno `z0=−11`:

`z_(i+1)=(2^(b_i) z_i−1)/3`,

dove b_i è il minimo esponente positivo che rende il figlio dispari e non multiplo di3. I suoi valori sono quelli della tabella precedente, anche per residui di interi negativi. Il ramo resta negativo e non raggiunge−1: l'unico predecessore negativo dispari di−1 è−1 stesso, con esponente1. Pertanto `|z_i|≥3`. Posto `B_t=Σ_(i<t)b_i`, la moltiplicazione delle identità dà

`3^t |z_t|=11·2^B_t · Π_(i<t)(1+1/(2^(b_i)|z_i|))`.

Ogni fattore è al più7/6, perciò

`2^(B_t−t) ≥ (3/11)(9/7)^t`.

Scegliamo ora target positivi

`n_t=18·3^t−1`, `y_t=16n_t+5=288·3^t−11`.

Il ramo ordinale minimo della base ha a_i=1 per tutti i primi t passi e termina nella sorgente `u_t=18·2^t−1`. L'immagine ordinale segue esattamente gli esponenti b_i del ramo negativo, perché dopo i passi i si ha

`v_i=288·2^B_i·3^(t−i)+z_i`,

quindi il residuo modulo9 è quello di z_i. La quantità positiva dominante assicura anche v_i>0. Al termine,

`v_t ≥277·2^B_t`,

quindi

**`v_t/u_t ≥(277/66)(9/7)^t`.**

Questo supera qualunque costo uniforme e qualunque multiplo di `1+log n_t`, poiché quest'ultimo cresce soltanto linearmente in t. La biiezione ordinale non può quindi fornire quel controllo puntuale per tutte le sorgenti e tutti i target.

Il fallimento non riguarda soltanto una sorgente piccola da correggere separatamente. A n_t fissato, aggiungiamo un ulteriore passo inverso di rango `2R`, R≥0. Poiché `u_t≡8 mod9`, gli esponenti associati sono `a=1+6R` e `b=b_min(z_t)+6R`, con b_min≥1. Le sorgenti

`U_R=(2^(1+6R)u_t−1)/3`

tendono all'infinito, mentre le immagini corrispondenti soddisfano `V_R/U_R>v_t/u_t`. Il costo fallisce dunque anche su input arbitrariamente grandi per ciascuno di questi target.

**Confine essenziale:** per n_t fissato questa famiglia ha soltanto O(log X) inizi entro X. Può essere scartata come o(X). Non confuta un accoppiamento che conservi una quota positiva dopo uno scarto trascurabile, non confuta H e non esclude un altro accoppiamento globale. Non è stata dimostrata l'assenza di ritorni dei target n_t per tutti i t; il no-go puntuale della costruzione non usa tale assenza.

Il replay congelato controlla t=0,...,64 e ranghi supplementari0,2,4,14,62. Tutte le identità e le disuguaglianze incrociate passano, con output normale e ottimizzato identici. Il replay è un controllo della prova, non la sua sostituzione.

## Feedback greedy e coda riflessa

Una policy diversa sceglie, per ogni esponente originale a, l'esponente interno b che minimizza `(|d+b−a|,b)`. Può usare tutti i ranghi nell'immagine. Le distanze fra esponenti interni consecutivi sono2 o4. Se il valore desiderato a−d supera il minimo b_min, il punto più vicino dista al più2. Altrimenti la policy è bloccata al primo esponente. Segue il vincolo deterministico

`−2≤d'≤max(2,d+b_min−a)`.

Il debito si comporta quindi come una coda riflessa: l'ostacolo è la frequenza e il costo delle visite alla barriera dei piccoli esponenti. Non basta dichiarare un drift medio favorevole sotto una distribuzione uniforme dei codici. Servirebbe dimostrarlo rispetto alla massa dei predecessori effettivi e contemporaneamente controllare le collisioni.

Un punto di misura preciso: i coefficienti geometrici `3·2^(−a)` sui soli figli interni **non formano un kernel di probabilità**. Il loro totale, nei residui1,2,4,5,7,8 modulo9, è rispettivamente

`20/21, 40/21, 17/21, 10/21, 5/21, 34/21`.

Per ottenere il kernel inverso reale occorrono i fattori della traccia g descritti da T03. Un kernel approssimato con le densità dei cilindri usa invece rho_(m−1) nei figli e rho_m nel genitore: perde un livello di precisione a ogni passo inverso. Una policy a memoria finita non può ignorare questa perdita trattando i nuovi digit ternari degli interi fissati come uniformi.

## Esperimenti congelati: altezza, collisioni, misura

Il primo protocollo fissa target `{5,7,31,593}`, siblings canonici, profondità massima18 e i primi due ranghi interni della base. È un sottoalbero binario di codici reali. Sono confrontate quattro policy: ordinale, scambio minimax, greedy e greedy con scarto locale di un input quando i due figli greedy coincidono. Ogni arco viene verificato con la mappa Syracuse in avanti. I target e le immagini sono certificati finitamente raggiungere1, escludendo ritorni alle radici usate. Non si assume la terminazione di altri inizi.

Alla profondità18, ciascun albero completo contiene262144 codici:

| n | Massimo debito ordinale | Massima dilatazione ordinale osservata | Massimo carico greedy | Codici conservati dal cap locale1 |
|---:|---:|---:|---:|---:|
|5|29|9.19·10^9|4112|4447|
|7|25|1.39·10^8|514|5044|
|31|26|2.71·10^8|5001|8960|
|593|32|6.88·10^10|20759|364|

Per593, il greedy associa la sorgente97 all'immagine220700680961, con profondità18, totale originale26 e totale immagine53. Entrambe le parole sono registrate nei dati e verificate direttamente. È un controesempio puntuale al piccolo controllo d'altezza per questa policy, non un controesempio a H.

Due protocolli successivi, dichiarati come follow-up dopo aver osservato i conteggi, mantengono lo stesso dominio e misurano prima `Σ3^k2^(−A)`, poi la somma armonica effettiva `Σ1/u`. Quest'ultima viene racchiusa in intervalli razionali mediante `floor(2^256/u)`: l'errore assoluto è al più `numero_codici·2^(−256)`. La selezione finale con capacità immagine1 conserva, per ogni immagine, la sorgente più piccola: massimizza esattamente la massa armonica selezionata per quella funzione.

Per n=593 e dilatazione64, il greedy ha **77.735% dei codici** entro l'altezza ammessa. Essi portano però solo **0.023005% della somma armonica delle sorgenti** del medesimo sottoalbero. Dopo il cap finale1 resta **0.004817%**. Il cap locale precoce conserva entro altezza64 circa **2.08·10^(−8)** della massa armonica dell'intero sottoalbero iniziale. I denominatori di questi confronti restano quelli dell'albero completo, non quelli del sottoalbero già potato.

Anche la somma armonica finita **non è eta in densità naturale**: può essere dominata da sorgenti piccole a una profondità fissata. Questi risultati servono a smascherare un proxy sbagliato e a stressare la costruzione; non autorizzano un'asintotica negativa o positiva per il greedy su tutti i predecessori.

Un ulteriore confine è stato isolato indipendentemente da T08: per un cap fisso M, i predecessori di un target il cui intero primo arrivo ha tutte le valutazioni≤M hanno densità naturale zero. Infatti chi arriva in meno di r passi con quel cap è un insieme finito, mentre chi arriva dopo ha un prefisso di r esponenti≤M, di densità relativa dispari `(1−2^(−M))^r`. Si passa prima al limite degli inizi e poi r→∞. Il nostro sottoalbero ha cap6: nessuna percentuale dei suoi codici può dimostrare eta su un bacino di densità positiva. Il suo scopo è soltanto trovare errori e avversari della policy. T08 ha inoltre ricavato la stima quantitativa `N_cap^odd(X)≤3X^alpha_M`, `alpha_M=log M/log(M/(1−2^(−M)))<1` per M≥2; il suo rapporto conserva la prova. Essa impone di non trattare nemmeno un cap che cresca molto più lentamente di log log X come sorgente di massa persistente.

## Prosecuzione concreta e criterio di arresto

Cambiare profondità è uno spazio di costruzioni ancora aperto. Il coordinatore ha isolato il costo corretto: basta controllare `rho'=2^A'/3^k'` rispetto a `rho=2^A/3^k`; con i prodotti di correzione limitati, ne segue il controllo d'altezza. Il criterio è equivalente, a costanti universali, al controllo dell'altezza effettiva. Non crea massa soltanto rinominando i profili.

Una prosecuzione sensata deve quindi lavorare con tutti i ranghi, un cap crescente e cataloghi fisici, consentendo una selezione globale dei cammini invece dello scarto precoce a ogni nodo. Gli obblighi sono: una comparazione relativa delle capacità su una stopping line, controllo della massa persa alla barriera del debito e carico finale degli interi. Il matching locale iniettivo, il debito medio sotto pesi geometrici e la quota uniforme dei codici non sostituiscono tali obblighi.

Fermare questa policy come candidata a prova di H finché non espone quella minorazione relativa. Sono giustificati il no-go puntuale dell'ordinale, le formule della coda e le diagnosi finite; non un no-go globale per accoppiamenti adattivi, profondità variabile o η.

## File e riproducibilità

Tutti i file T06 sono in `research/research_sprint_2026-11-15/t06/`. I quattro programmi sono indipendenti dai programmi T02/T03: `coupling_policies.py`, `coupling_pressure.py`, `coupling_harmonic.py`, `ordinal_adversary.py`. I rispettivi protocolli precedono le esecuzioni, compresi i follow-up esplicitamente dichiarati. Gli output normali e con Python -O sono confrontati byte per byte; i receipt registrano SHA-256. Le guardie usano eccezioni esplicite, non assert eliminabili dall'ottimizzazione.

Verifica finale T06 alle20:34:26 UTC: quattro coppie normale/-O identiche, manifest e guardie razionali in `verification_manifest.json`. Le quote armoniche593 citate soddisfano anche i controlli interi `quota_codici>77/100`, `quota_armonica_buona<231/10^6`, `quota_armonica_selezionata<49/10^6`. SHA-256 dei dati armonici: `2ecbc5f734f7310fbe812d54f895f8753194280957806dd6da7b0bda92c63f34`; dati avversario: `da0a62e097295642c8d5f4b31fac2c834643a7649ae61c5432a30e2e8bf55c2f`.
