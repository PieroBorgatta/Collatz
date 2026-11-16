# U02 — Carry effettivi e costo di una ricodifica con colore diverso

Ultimo attacco del 16 novembre, prima della chiusura. Prove su carta: nessun calcolo, griglia, GPU o sorgente Lean modificato. Il controllo superiore del costo resta aperto. Il punto è conservare la vera costante affine della parola, non soltanto il gain di un modello ladder.

## 1. Identità esatta del controller

Sia a=(a₀,…,a_(k−1)) una parola effettiva x₀=u→…→x_k=n. Per un candidato b della stessa lunghezza, costruire inversamente v_k=n e v_i=(2^b_i v_(i+1)−1)/3. Porre

`D_i=Σ_(j≥i)(b_j−a_j)`, `D_k=0`, `c_k=0`,

**`c_i=[2^b_i c_(i+1)+2^D_i−1]/3`.**

L'induzione dà esattamente `v_i=2^D_i x_i+c_i`. Le potenze negative sono razionali diadiche. L'identità non garantisce che il candidato sia intero o positivo: questi requisiti, e l'essere unità, restano condizioni effettive da verificare.

La condizione di integrità è

`2^b_i[c_(i+1)+2^(D_(i+1)−a_i)]≡1 (mod3)`.

Il coefficiente tra parentesi è congruo a v_(i+1). Se è zero modulo3, nessun b_i funziona. Se è unità, la parità di b_i è forzata; fra le tre classi corrispondenti modulo6, due danno figli unità. Si controllano così i veri offset e il colore del primo genitore, ma non ancora il costo totale.

Cambiare soltanto l'ultimo esponente in a_(k−1)+2r produce esattamente il sibling H^r(x_(k−1)), H(x)=4x+1. Con r=1 oppure2 si sceglie il sibling unità canonico. La costante forward

`C(a)=Σ_(i<k)3^(k−1−i)2^(a₀+…+a_(i−1))`

non contiene l'ultimo esponente, quindi C(b)=C(a), e

`3^k(v₀−4^r u)=(4^r−1)C(a)`.

Poiché C(a) è unità modulo3 e ν₃(4^r−1)=1, per r=1,2 un candidato intero richiede k≤1. L'edit deve quindi propagarsi; applicarlo soltanto al genitore finale non costruisce il seed. Al bordo opposto, cambiare soltanto il PRIMO esponente in a₀+2r funziona sempre dal seed H^r(u), poiché S(H^r(u))=S(u); per k≥2 conserva però il genitore finale originale. La ricodifica economica al seed non cambia colore, quella che cambia colore al target non attraversa il prefisso senza altri edit.

## 2. Un vero diamond e il suo costo

Per ogni n positivo dispari con n≡26mod27, porre

`u=(256n−5)/9`, `v=u−14`.

Le parole effettive `[1,7]:u→n` e `[7,1]:v→n` hanno seed unità (u≡1, v≡2mod3) e genitori finali distinti, rispettivamente `(128n−1)/3` e `(2n−1)/3`. Positività e valutazioni sono esatte; il primo target dispari ammesso è53. Qui si conserva davvero l'offset, non solo il monomio3²/2⁸.

Il limite è preciso. Per due parole di lunghezza2 e stesso totale B, le costanti sono3+2^a e3+2^b. Un diamond non banale richiede9|(2^a−2^b), quindi a−b è un multiplo non nullo di6 e B≥8. Il gain è allora≤9/256<1: questi diamond brevi non realizzano un crossing ladder espansivo. Inserirli dopo un prefisso impone inoltre la nuova divisibilità ternaria attraverso quel prefisso; non possono essere concatenati ignorando il carry.

## 3. Dove il lifting modulo6 perde il budget

Se un figlio y è ottenuto con esponente b, sostituire b con b+6t dà

`y_t=64^t y+(64^t−1)/3`.

Si ha `ν₃(y_t−y_s)=1+ν₃(t−s)`: infatti64−1=63 ha valutazione ternaria2 e3y_s+1 è unità. Di conseguenza per q≥1, t=0,…,3^(q−1)−1 percorre esattamente la classe ymod3 dentro il modulo3^q.

Se y≡2mod3 e r≥1, per attraversare altri r passi inversi invariati di esponente1 occorre y_t+1≡0mod3^r, cioè

**`64^t(3y+1)≡−2 (mod3^(r+1))`.**

Esiste un unico t modulo3^(r−1). Questa congruenza garantisce l'integrità dei r passi e l'essere unità degli stati interni; l'unità dell'endpoint finale richiede una guardia su un'ulteriore cifra. Il lifting fornisce però soltanto una garanzia di costo aggiunto fino a6(3^(r−1)−1). Non offre un overhead logaritmico nella profondità. Non è dimostrato che il peggior costo si realizzi sulle particolari parole da seed piccoli: proprio quelle correlazioni aritmetiche andrebbero sfruttate. Distribuire correzioni su molte posizioni evita una sola correzione enorme, ma la somma dei costi non è controllata.

## 4. Obbligazione finita, con la guardia sul colore

Per una parola effettiva a:u→n, cercare b di stessa lunghezza k, con seed alternativo v positivo dispari UNITÀ e ultimo esponente diverso. Per un budget E fissato sono finitissime le composizioni con totale B≤Σa+E. Il controller sopra ne conserva tutti gli offset; un candidato reale è un certificato verificabile senza ipotesi sulla misura.

Perché il costo conta: su una spine divergente n_k=S^k(u), una tale parola soddisfa

`v_k≤n_k2^B_k/3^k≤P₀u2^(B_k−A_k)`.

I bacini dei seed alternativi sono laterali e disgiunti anche fra k diversi. Sotto il lower esterno di densità c/v per target unità, sarebbe quindi impossibile avere certificati su indici con `Σ_k2^−(B_k−A_k)=∞`. Per esempio basterebbe B_k−A_k≤log₂k+log₂logk+C_u per tutti i k grandi. Questa è soltanto una possibile condizione sul costo dell'editor; non è stata costruita, non è dichiarata più debole di H e non è una soluzione.

L'ostacolo emerso è concreto: il lifting risolve le congruenze, ma può consumare un budget esponenziale nella lunghezza del corridoio. Serve un ammortamento aritmetico del carry per le parole effettive da seed piccoli, con controllo del primo colore; i soli gain, la località e i cataloghi finiti non lo danno.

U04 ha verificato indipendentemente l'identità del controller, il diamond e la deduzione condizionale dei costi. U04 ha verificato anche il lifting modulo6, con le guardie q,r≥1 e la precisazione sull'unità dell'endpoint finale. Nessuna priorità bibliografica globale rivendicata.
