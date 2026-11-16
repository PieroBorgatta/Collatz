# U08 — Coalescenza e ostruzioni ai trasporti affini

Sessione del 15–16 novembre 2026, base `203cbb8`. Dimostrazioni su carta che usano risultati primari esterni dichiarati. Nessun esperimento, sorgente Lean, GPU, servizio a pagamento o modifica a file preesistenti. Gli enunciati qui non costituiscono una prova di H o Collatz.

## 1. Risultato e ambito

Per ogni target positivo fissato a, sia `I_a(u)` l'indicatore che l'orbita Collatz ordinaria di u raggiunge a, incluso il tempo zero. La coalescenza quantitativa implica:

1. Per ogni c intero fissato, `#{u≤X: u+c>0, I_a(u+c)≠I_a(u)}=O_(a,c)(X/sqrt(log X))`.
2. Per ogni menu FINITO fissato di mappe `f(u)=(Mu+B)/D`, con M,D positivi composti soltanto da fattori 2 e 3 e B intero fissato, ogni selezione dipendente dalla sorgente fra i candidati interi positivi conserva I_a fuori da o(X) sorgenti. La costante può dipendere dal menu e dal target.
3. Un risultato più uniforme vale per finestre additive crescenti: per ogni 0≤r<1 fissato, il vettore di TUTTI gli indicatori `I_a`, a≤X^r, è localmente costante su ogni finestra `|v−u|≤G_X`, fuori da o(X) sorgenti, se `log(G_X+2)=o((log X)^(1/8))`.

Pertanto questi schemi non possono trasferire una quota positiva di sorgenti fra due bacini disgiunti di target fissati. La terza conclusione permette anche una scelta adattiva del candidato e dei target nel dominio dichiarato. Per target crescenti l'errore è assoluto o(X), non relativo alla massa di un bacino che può essere raro.

Questi sono consumer della coalescenza e del safe-prefix transfer già pubblicati. Non è stata accertata una priorità globale delle formulazioni di ostruzione qui riportate.

## 2. Fonti primarie e verifica effettuata

- Said Duran, *Consecutive integers coalesce with density one under the Collatz map*, 27 settembre 2026, [record Zenodo](https://doi.org/10.5281/zenodo.23003524). Acquisita la scheda ufficiale; non letto o ricompilato il suo archivio Lean.
- David Leen, *Exact rates in Collatz synchronization*, 9 ottobre 2026, [record e sorgente](https://doi.org/10.5281/zenodo.23268751). Letti gli enunciati di assorbimento uniforme e il trasferimento esatto alle popolazioni di interi, in particolare `pop:discrepancy`.
- David Leen, *Quantitative synchronization of Collatz trajectories*, 9 ottobre 2026, [record e sorgente](https://doi.org/10.5281/zenodo.23268755). Letti `thm:pair`, `cor:deadline`, `lem:cylinders`, `lem:clock`, i passaggi sui mark stabili e il cociclo di dilatazione 2^a3^b. Il cociclo corrispondente era già esplicito nella fonte.
- lyapunov_weaver, *Synchronization of growing Collatz blocks and selected references*, 9 novembre 2026, [paper124/v1](https://rstation.ai/problems/collatz/papers/124/v1). Il Teorema 1 e l'equazione (18) sono l'input per le finestre crescenti. Il safe-prefix transfer è già usato nel suo Corollario 6. Revisione pubblica sul sito, distinta da una verifica formale.

Le due sorgenti TeX ufficiali di Leen sono conservate con record, licenza CC BY 4.0 e hash nel [manifest delle fonti](../../../research/research_sprint_2026-11-15_three_hours/u08/sources/manifest.json). È stata eseguita una lettura mirata delle interfacce utilizzate, non una ricostruzione di tutte le prove esterne. Nessun codice o TeX esterno è stato eseguito.

## 3. Input di coalescenza e bordo dei target

Sia C la mappa ordinaria e T la shortcut. Nei modelli delle fonti, l'assorbimento bilanciato di una coppia adiacente entro t passi shortcut è un evento periodico nella sorgente modulo 2^t, di massa complementare `q_t≤A/sqrt(t+1)`. Su un intervallo di X interi il numero dei fallimenti è al più

`X q_t+2^t`.

Un successo produce uno stesso stato allo stesso tempo ordinario non superiore a 2t: i conteggi dispari uguali permettono di scegliere un comune tempo ordinario. Queste sono le interfacce pubblicate, non un'ipotesi di indipendenza fra due orbite intere.

Deterministicamente `C^j(u)≥u/2^j`. Se u,v>R·2^N e due traiettorie si incontrano a tempi individuali al più N, nessuna ha raggiunto un target≤R prima dell'incontro. Da quel punto hanno la stessa coda, quindi

`I_a(u)=I_a(v)` per ogni a≤R.

Non si deduce questa uguaglianza dalla sola coalescenza eventuale: se si incontrassero dopo avere attraversato i target, i due bacini potrebbero essere disgiunti. Il bordo R·2^N paga esattamente quel caso.

## 4. Offset fissato e piccolo menu

Per c≥1, se tutte le c coppie adiacenti da u a u+c sono assorbite entro t, l'intero blocco ha una coda comune entro 2t passi ordinari. Il conteggio dei fallimenti, senza indipendenza, è al più

`cXq_t+c2^t+O(c^2)`.

Scartare inoltre `u≤a·2^(2t)` e scegliere `t=floor(log₂X/4)`. Questo prova la prima conclusione; c<0 si tratta reindicizzando e c=0 è immediato. Non è richiesta l'esistenza della densità del bacino.

Un menu finito di offset ha un'unione di eccezioni ancora di misura o(X). L'offset può essere scelto dopo avere osservato tutta la sorgente. Usando soltanto l'unione dei lati adiacenti si ottiene già la variante uniforme `G_X=o(sqrt(log X))`; la sezione 6 la migliora grazie al teorema di famiglia.

## 5. Dilatazioni 2,3 e affini razionali smooth

La stabilità sotto il fattore 2 è esatta fuori da un bordo finito: 2u raggiunge u in un passo ordinario. Per u dispari, C(u)=3u+1; coalescenza rapida fra 3u e 3u+1 implica quindi uguaglianza degli indicatori al target fra u e 3u, purché non sia stato attraversato il target prima del merger.

Ecco anche un conteggio uniforme dei casi pari. Scrivere u=2^v m, m dispari, e troncare v≤t. Le coppie 3m,3m+1 considerate per ogni v hanno al più

`(X/2^v)q_t+2^t`

fallimenti: per un upper si possono contare tutti gli m, non solo i dispari; moltiplicare per 3 permuta le classi binarie. Sommando v≤t si ottiene `2Xq_t+(t+1)2^t`. Le sorgenti con v>t sono al più X/2^t.

I due cammini originali u,3u si incontrano entro al più v+1+2t≤3t+1 passi individuali, quindi il bordo dei target è al più `a·2^(3t+1)`. Con `t=floor(log₂X/8)` tutti i termini di errore diversi da Xq_t sono o(X/sqrt(log X)). Ne segue

`#{u≤X:I_a(3u)≠I_a(u)}=O_a(X/sqrt(log X))`.

Iterare un numero fissato di volte i fattori 2 e 3 e usare gli offset fissati. Le preimmagini di un insieme di o(X) eccezioni sotto una mappa affine propria fissata sono ancora o(X), perché la mappa è iniettiva e la sua immagine è contenuta in [1,O(X)]. Si ottiene così stabilità per u→Mu+B quando M è smooth 2,3. Per f(u)=(Mu+B)/D intero positivo, l'ultimo confronto è con il fattore D: `I_a(Dv)=I_a(v)` fuori da o(X) valori v; l'applicazione u→v è ancora iniettiva sul dominio intero. Questo prova la seconda conclusione, compresa la scelta da un menu finito.

Il caso a=1 e altri target ciclici è ammesso nella stabilità degli indicatori. Per dedurre impossibilità di trasporto serve però davvero la disgiunzione dei due bacini. Per esempio il bacino di un antenato della ciclo banale può essere contenuto nel bacino di 1; la conclusione di ostruzione non si applica a una coppia annidata.

## 6. Finestre crescenti e vettore dei target piccoli

L'input supplementare di paper124/v1 è: per D starts consecutivi e qualunque intervallo positivo I di X sorgenti,

`#{b∈I:T_D(b)>t}≤C X(1+log D)^4/sqrt(t+1)+2^t`.

Sul successo T_D≤t tutti i D cammini condividono il futuro entro 2t passi ordinari. Non compare un fattore D nell'errore di conteggio delle classi.

Per interi X≥1, G≥0, R≥1, considerare la finestra `[u−G,u+G]` e scartare `u≤G+R·2^(2t)`. La base u−G è allora positiva e ogni prefisso prima del merger è sopra R. Applicando l'input con D=2G+1 e traslando l'intervallo delle sorgenti si ottiene

`#{u≤X:∃v>0, |v−u|≤G, ∃a≤R, I_a(v)≠I_a(u)}`

`≤G+R·2^(2t)+C X(1+log(2G+1))^4/sqrt(t+1)+2^t`.

Per G=0 il lato sinistro è zero; non occorre applicare il teorema di famiglia a D=1.

Fissare 0≤r<1, R=floor(X^r) e `t=floor((1−r)log₂X/4)`. Il bordo è `R·2^(2t)≤X^((1+r)/2)`. Se `log(G_X+2)=o((log X)^(1/8))`, tutti i termini sono o(X). Questa è la terza conclusione. Il vettore dei target è simultaneo perché tutta la parte pre-merger resta sopra R: non si è sommato un errore per ciascun target.

## 7. Conseguenza per il programma di trasporto

Se due target a,b hanno bacini disgiunti, u che raggiunge a e v che raggiunge b hanno `I_a(u)=1`, `I_a(v)=0`. Ogni trasporto appartenente alle classi sopra deve quindi usare una sorgente eccezionale. Per target fissati il numero di tali sorgenti è o(X); un menu fisso di affini smooth o una scelta nella finestra crescente non può produrre η>0.

L'ostruzione riguarda le mappe sulle SORGENTI, non le sole parole di esponenti. Non richiede conservare (k,A), né un bound incoming, poiché limita già la massa uscente fisica. Le mappe di slope non appartenente al gruppo generato da 2 e 3, le deformazioni sorgente-dipendenti fuori dalla finestra e i cataloghi generici di editing non sono coperti. La loro esclusione non è stata dimostrata.

La via complementare degli agenti U10 riguarda proprio multipliers 5,7,11,13: per loro non è disponibile il meccanismo di coalescenza a tempo fissato usato qui. Questo è un motivo di indagine, non un lower di massa né una prova che quelle mappe risolvano H.

## Esito

La coalescenza fornisce nuove ostruzioni controllabili per il progetto; le fonti già contengono gli strumenti di stabilità e i cocicli principali. Non è stato costruito un trasporto positivo o dimostrato un nuovo lower. Tutti gli input esterni restano separati dalla libreria Lean locale.
