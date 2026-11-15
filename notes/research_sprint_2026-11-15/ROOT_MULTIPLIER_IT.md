# Dal budget degli atomi al cutoff infinito

Nota di integrazione del coordinatore, 15 novembre 2026. Il collegamento è stato ricostruito con T10 e rivisto da T11. Il nucleo finito è verificato in `IntegerAtomTilt.lean`; i passaggi probabilistici e di limite descritti qui restano prove su carta. Nessuna legge analitica esterna è stata aggiunta come assioma Lean.

## Nucleo finito effettivo

Per una parola Syracuse esatta w da un positivo u al target n>0, il peso omogeneo è ω(w)=3^k/2^A. Il potenziale già verificato dà ω(w)≤n/u. A lunghezza fissata, due parole dalla stessa sorgente coincidono. Pertanto un catalogo finito W ha sorgenti fisiche distinte e

`Σ_(w∈W)ω(w)²≤n²Σ_(u∈source(W))u⁻²≤2n²`.

L'ultimo bound è elementare: per j≥1, `j⁻²≤2/[j(j+1)]`, e la somma telescopica è al più2. La divisione per zero della formalizzazione vale zero, ma le sorgenti del catalogo sono esplicitamente positive.

Il modulo prova cinque enunciati pubblici: il budget dei reciproci quadrati, il peso di una parola limitato dal target, il budget per sorgenti iniettive, il caso a lunghezza fissata e il budget condiviso fra tutte le profondità quando il target non ha ritorni. In quest'ultimo caso l'unicità della sorgente segue dal pool non ricorrente già formalizzato: due tempi di arrivo produrrebbero un ritorno positivo del target.

Il bound riguarda parole effettive e non copie di etichette. Nel caso ciclico il budget a profondità fissata resta valido; la versione condivisa con la stessa costante2n² richiede invece il nonritorno.

## Dizionario con la legge casuale

La fonte del 14 novembre [146/v1](https://rstation.ai/problems/collatz/papers/146) usa parole outermost-first. Per confrontarle con quelle forward del progetto si inverte l'ordine della lista; lunghezza, totale e peso restano identici.

Sotto gli esponenti geometrici originali P(e=j)=2⁻ʲ, un prefisso ha moltiplicatore A_i=3^i2⁻ᴰⁱ e offset reale B_i. Se il cilindro ternario della parola contiene il positivo dispari n, ogni prefisso soddisfa

`n=B_i+A_iY_i`, con Y_i intero positivo.

L'integralità è il dizionario ternario completo; la positività è già provata in `AffinePositivity`. Ne segue A_i≤n. Un prefisso che contribuisce all'atomo intero non può quindi aver superato n come moltiplicatore. Questo cap reale non è un limite sugli esponenti e_i.

La legge tilt P*(e=j)=3·4⁻ʲ è una probabilità. A profondità m, la densità normalizzata del suo atomo n è la somma dei pesi A_w² delle parole ammissibili. Il bound finito, applicato a cataloghi crescenti e poi passato al limite per monotonia, dà

`ρ*_m(n)≤2n²`.

Se n è senza ritorni, l'iniettività fisica vale contemporaneamente su tutte le profondità. Lo stesso argomento dà il risultato più forte

`Σ_(m≥0)ρ*_m(n)≤2n²`.

## Il futuro del prefisso viene pagato

Sia H=sup_i A_i e sia σ_B la misura originale ristretta a H≤B, con B>n. Il processo A_i è una martingala nonnegativa sotto la legge geometrica originale. Dopo un prefisso, la probabilità di superare in futuro B è al più A_m/B. Il prefisso stesso non ha attraversamenti, perché tutti i suoi moltiplicatori sono≤n<B.

L'appartenenza al cilindro C_m(n)=n+3^mZ₃ dipende soltanto dal prefisso. L'indipendenza del futuro e il cambio di peso danno allora

`0≤ρ_m(n)−3^mσ_B(C_m(n))≤ρ*_m(n)/B≤2n²/B`.

Questa stima distingue correttamente il cap fino al tempo m da quello infinito. Per un target senza ritorni si può anche sommare su tutte le profondità:

`Σ_(m≥0)[ρ_m(n)−3^mσ_B(C_m(n))]≤2n²/B`.

L'errore tra i Cesàro di K termini è quindi al più **2n²/(BK)**. In particolare le due medie hanno lo stesso limite a target fissato. Se B=2n e la vera traccia soddisfa g(n)≥cεn, il relativo errore delle medie è≤1/(cεK), uniforme in quella classe di target.

## Che cosa resta da dimostrare

Il nuovo articolo offre una regolarizzazione globale della misura σ_B; la sua prova analitica è stata letta indipendentemente, senza replay formale esterno. Il ponte sopra rende quantitativo l'errore del cutoff sugli atomi interi. Non dà però un lower delle medie capped entro un tempo dipendente dall'altezza del target.

L'obbligo successivo è controllare quel tempo uniformemente sui target rilevanti. Il criterio Doob revisionato in T09 consente tempi sotto `log_(3/2)n` con un deficit additivo divergente; il criterio basato sulla nuova weak L² usa la scala `2log₃n` con deficit divergente. Nessuno dei due lower di rilassamento è stato ottenuto. La sola proprietà σ_B∈L³ non sostituisce un controllo locale della sua traccia.
