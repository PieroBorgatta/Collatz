# U04 — Audit del rinnovo finito per record

Revisione indipendente di `U15_LADDER_RENEWAL_IT.md`, snapshot `00fb7dc2753eb3529ba00b546f5d5738a6b88953f65c8a04e9951ec957572966`. Nessun esperimento, build o modifica agli originali. **PASS con gli input espliciti della precedente identificazione capped/Doob.** Non occorrono un floor uniforme o LF finito per il nuovo argomento di positività.

## 1. Partizione secondo l'ultimo massimo

I record sono sui prefissi inversi outermost-first. Per a>1, una parola record ha gain finale a e tutti i gain precedenti strettamente minori. Non è imposto che tali gain precedenti restino sotto1. È corretto applicare la finitezza del catalogo forward tramite reversione.

Tutte le parole di gain a hanno lo stesso profilo (k,E), per unicità della fattorizzazione. A un livello fissato i relativi cilindri sono quindi disgiunti e il livello non può essere raggiunto a due tempi diversi sullo stesso cammino. Il massimo H è effettivamente raggiunto e appartiene a un insieme finito di gain≥1.

Sull'evento H=a, il prefisso al tempo k appartiene a R_a. Dopo quel prefisso, il prodotto globale è a volte il prodotto normalizzato del futuro. La condizione residua è esattamente H_future≤1. Markov e il peso del prefisso danno

`g(n)Q_n(H=a)=aΣ_(w∈R_a)g(u_w)Q_(u_w)(H≤1)=aΣ_(w∈R_a)h(u_w)`.

Non serve F(u_w)=1: h è proprio il prezzo del futuro. Per a=1, l'unico profilo di gain1 è quello vuoto e la massa è h(n). Il caso F(n)=1 restituisce pertanto h(n)=g(n).

## 2. Rinnovo triangolare finito

Sommare la partizione atomica di H prova

`g_B(n)=h(n)+Σ_(record 1<Ω≤B)Ωh(u_w)` per B≥1,

e la formula completa di g quando B≥F(n). Per B<1 entrambi i membri capped valgono zero.

Ogni record non vuoto ha offset positivo: n=Ωu+B_w>Ωu>u. La somma è dunque triangolare nell'altezza intera e finita. Nei target periodici le eventuali parole differenti con lo stesso seed restano coefficienti distinti: non sono state identificate senza sommarle.

All'atomo superiore, i seed ottimali hanno F(u)=1, quindi h(u)=g(u); la formula recupera esattamente il salto massimo già verificato. Il rinnovo non costituisce un algoritmo indipendente per g o h, perché g rimane un input e la finitezza del catalogo non fornisce un cutoff effettivo di ricerca.

## 3. Positività puntuale del cap1

Per ogni genitore unità x, il massimo F(x) è realizzato. Se M_x=ωF(x)≥δ, concatenarne il witness con x→n produce una parola verso n di gain≥δ. Rami distinti producono parole distinte; il catalogo a soglia positiva ne contiene finitissime. Per una soglia reale si può prima scegliere una soglia razionale inferiore positiva.

I genitori unità sono infiniti: due classi di esponenti su sei rimangono lecite. In particolare esiste un ramo con M_x≤1. Il suo primo gain è≤1, e ogni ulteriore prefisso sotto Q ha prodotto globale al più ωF(x)≤1. L'intero cilindro di quel primo ramo appartiene a H≤1 e ha probabilità positiva ωg(x)/g(n). Quindi h(n)≥ωg(x)>0.

Questa prova vale anche con target periodici e non usa LF, g≥c₀F o un floor uniforme. Il ramo e la sua massa possono degenerare con n; non segue una quota relativa uniforme, un rate di clock o il lower del surplus A.

## Esito

La partizione usa soltanto gain fisici, profili univoci e la proprietà di Markov del vero kernel. Il nuovo rinnovo e la positività puntuale sono corretti. Rimangono necessari gli input precedenti per identificare la traccia capped della legge originale con la sopravvivenza Q; la prova non li sostituisce con un'assunzione indipendente sui cammini interi.
