# U15 — Rinnovo finito tramite record del cap

Addendum su proposta del coordinatore, separato dagli snapshot U15 già revisionati. Si usano le ipotesi deboli della nota `U15_FINITE_CAP_IT.md`: cataloghi finiti a soglia positiva, dizionario intero, Cesàro di g, armonicità positiva sulle unità e Green quadratico per l'identità capped/Doob. Nessun floor assoluto di g è aggiunto. Prove su carta, nessuna priorità globale dichiarata.

## 1. Record outermost-first e massimo del futuro

I prefissi sono OUTERMOST-FIRST, cioè seguono il cammino inverso dal target n al seed u. Per applicare il catalogo Lean forward si inverte l'ordine della parola: il gain totale resta invariato, mentre la condizione di record resta esplicitamente sui prefissi inversi.

Sia h(n)=g_1(n)=g(n)Q_n(H≤1). Per a>1, sia R_a(n) l'insieme delle parole inverse effettive w, con sorgente unità, tali che

`Ω(w)=a`, `Ω(v)<a` per ogni prefisso proprio v di w, inclusa la parola vuota.

Sono record STRETTI al tempo finale, senza imporre che tutti i prefissi precedenti restino sotto 1. La famiglia R(n)=unione_(a>1)R_a(n) è finita: ogni suo elemento ha gain>1 e appartiene al catalogo finito. Per a=1 si ammette soltanto la parola vuota: nessuna parola nonvuota ha gain esattamente uno, per unicità della fattorizzazione in2 e3.

Tutte le parole di un gain fissato a=3^k/2^E hanno la stessa lunghezza k e totale E. Quindi su un cammino Q il livello a può essere visitato al più una volta. Poiché H è un massimo a supporto finito, per a>1 l'evento H=a è partizionato dai cilindri di R_a(n), seguiti dalla condizione che il futuro normalizzato non superi 1.

Dopo un prefisso w di gain a e sorgente u, il kernel del futuro è Q_u e i moltiplicatori futuri sono a volte quelli normalizzati da u. La proprietà di Markov e il peso del prefisso danno dunque

`g(n)Q_n(H=a)=a Σ_(w∈R_a(n)) h(u_w)`.

Non occorre assumere F(u_w)=1: h(u_w) è precisamente il costo del futuro che evita il cap1. Per a=1 la massa è h(n).

## 2. Rinnovo finito e triangolarità per altezza

Per B<1, g_B(n)=0. Per B≥1, sommando gli atomi del massimo si ottiene

**`g_B(n)=h(n)+Σ_(w∈R(n), Ω(w)≤B) Ω(w)h(u_w)`.**

Per B≥F(n) la somma contiene tutti i record e quindi

**`g(n)=h(n)+Σ_(w∈R(n)) Ω(w)h(u_w)`.**

Ogni record è nonvuoto e ha gain>1. L'identità affine positiva impone n>Ω(w)u_w, dunque u_w<n. La somma è perciò finita e TRIANGOLARE nell'altezza intera della sorgente. Più record possono avere lo stesso seed se il target è periodico; non vengono fusi senza sommare i loro coefficienti. Nel caso non ricorrente un seed ha al più una parola verso n.

Si tratta di una decomposizione di g tramite h, non di un algoritmo autonomo: g è ancora un input, il catalogo è finito esistenzialmente e non è stato certificato da un cutoff di lunghezza. La sottrazione h(n)=g(n)−Σ_R Ωh(u) non fornisce una stima inferiore uniforme, né un nuovo solver del problema.

L'atomo superiore a=F(n) recupera la formula della nota precedente. Ogni seed ottimale ha F(u)=1, quindi h(u)=g(u). Si ottiene g(n)−g_(F(n)^-)(n)=F(n)Σ_opt g(u). Se F(n)=1, la famiglia dei record è vuota e h(n)=g(n).

## 3. Positività punto per punto senza floor uniforme

**Corollario.** Sotto le stesse ipotesi, h(n)>0 per ogni target unità n. Non viene dedotto alcun lower uniforme, tasso o scelta efficace del ramo.

Per ogni genitore unità x di n, con gain ω=3/2^e, porre M_x=ωF(x). Il massimo F(x) è raggiunto. Se M_x≥δ>0, concatenare un witness ottimale verso x con l'ultimo passo x→n produce una parola verso n di gain almeno δ. Genitori distinti producono parole distinte. Il catalogo a soglia δ è finito, quindi per ogni δ ci sono soltanto finitissimi rami con M_x≥δ.

Ogni target unità n ha infiniti genitori unità: le congruenze di e che rendono (2^e n−1)/3 intero ed evitano la divisibilità per3 si ripetono periodicamente e lasciano infinite classi. Si può quindi scegliere un ramo con M_x≤1. Poiché F(x)≥1, anche ω≤1. Su tutto il cilindro Q di quel primo passo, ogni prodotto successivo è al più ωF(x)≤1, mentre A_0=1. Quel cilindro è dunque interamente contenuto nell'evento H≤1 e ha probabilità ωg(x)/g(n)>0. Pertanto

`h(n)≥ωg(x)>0`.

La prova non usa la sommabilità LF né g≥c₀F: il catalogo da solo dà che solo finitissimi rami sono pericolosi a una soglia fissata. Le costanti del ramo sicuro possono degenerare al crescere di n; la positività non conserva una quota relativa di g lungo una ipotetica spine divergente.

## Stato

La legge puntuale del cap ha una decomposizione finita per record e un rinnovo triangolare con sorgenti strettamente più piccole. La positività del cap1 è puntuale. Restano aperti tutti i lower uniformi necessari per il surplus o il clock.
