# U11 — Un suffisso a slope limitata non fornisce massa relativa

Prova su carta della sessione aggiuntiva del 15–16 novembre 2026, base `203cbb8`. Non è un nuovo teorema Lean. La finitezza dei cataloghi a slope limitata era già usata nel progetto senza ritorni; la sua estensione ai ritorni segue dal budget di occupazione già formalizzato in `WeightedWords`. La deduzione proposta qui è l'ostruzione polilogaritmica al recoding, senza un input S-unit. La priorità bibliografica globale non è stata accertata.

## Enunciato e quantificatori

Fissare due target positivi dispari distinti n,y e una costante reale R₀>0. Per una parola effettiva a di lunghezza L e totale B, porre

`ω(a)=3^L/2^B`, `ρ(a)=1/ω(a)=2^B/3^L`.

Considerare tutti i codici fisici

`w=pα:u→n`, `w'=pβ:v→y`,

con sorgenti u,v positive dispari, prefisso p IDENTICO come lista di esponenti, `|α|=|β|`, `Σα=Σβ`, `ρ(α)≤R₀` e `u≤X`. Le parole sono esatte per S; non sono richiesti primo arrivo, nonritorno o un cutoff su v. Non si assume alcun limite sul numero di esponenti o di pezzi nella coda.

**Proposizione candidata.** Esiste un intero K=K(n,y,R₀)≥0, indipendente da X, tale che ogni codice ammesso ha lunghezza totale `k=|pα|≤K`. Per X≥2, il numero dei codici ammessi è quindi

`O_(n,y,R₀)((1+log X)^K)`.

In particolare è X^o(1). Se un flusso con carico uscente≤1 per sorgente usa questa relazione, esso non trasferisce una quota positiva di un bacino con densità inferiore positiva. Questo non esclude trasporti con slope della coda crescente con X, prefissi differenti o profili totali diversi.

## 1. Il catalogo a slope limitata è finito anche con ritorni

Sia

`E(n,R₀)={a : esiste z>0 dispari con a:z→n esatta e ω(a)≥1/R₀}`.

La parola vuota è inclusa se R₀≥1. Il potenziale reciproco verificato nel progetto dà `ω(a)z≤n`, quindi ogni sorgente appartiene al finito insieme `1≤z≤R₀n`.

Fissare uno di tali z. Il teorema già verificato `WeightedVisits.sum_wordWeight_fiber_le` afferma, per ogni Finset W di parole distinte effettive da z a n,

`Σ_(a∈W)ω(a)≤n(3n+1)/z`.

Il teorema ammette ritorni e parole vuote. Per W⊂E(n,R₀) segue

`|W|/R₀≤Σ_(a∈W)ω(a)≤n(3n+1)/z`.

Una famiglia infinita conterrebbe Finset di cardinalità arbitrariamente grande, contraddicendo questa maggiorazione uniforme. Dunque il sottoinsieme a sorgente z è finito. L'unione sulle finitissime sorgenti è finita. Per una parola e un target la sorgente è inoltre unica, per l'identità affine, ma la finitezza non ha bisogno di contare tale unicità due volte.

Questo argomento fornisce un bound sulla CARDINALITÀ, non sulla lunghezza massima delle parole. La finitezza permette poi di prendere il massimo delle lunghezze e dei totali del catalogo; non produce un cutoff temporale esplicito o un algoritmo di terminazione per i piccoli antenati.

## 2. Anche il catalogo delle coppie di code è finito

Per ogni codice dell'enunciato, lo stato z raggiunto dal prefisso p è positivo dispari; α appartiene quindi a E(n,R₀). Esistono soltanto finitissime α, con lunghezza L e totale B in un insieme finito. Per ciascuna coppia (L,B), le liste β di L interi positivi e somma B sono finite. Pertanto l'insieme F delle coppie (α,β) che possono apparire è finito.

Non è stato imposto che β sia primo arrivo o che abbia sorgente limitata. La finitezza delle liste di lunghezza e somma fissate basta. Eventuali β non effettive non servono e si possono lasciare nel soprainsieme finito.

## 3. Il residuo forza una profondità totale limitata

Usare la costante affine C(a), definita da

`2^(Σa) endpoint =3^|a| source + C(a)`.

Con `r=|p|`, `P=Σp`, `L=|α|=|β|`, `B=Σα=Σβ` e `k=r+L`, la cancellazione del prefisso comune dà

`3^k(v−u)=2^P R(α,β)`,

`R(α,β)=2^B(y−n)−C(β)+C(α)`.

Il residuo è un intero. Non può essere zero in un codice effettivo: se R=0, allora v=u, e due parole esatte della stessa lunghezza dalla stessa sorgente coincidono; i loro endpoint sarebbero n=y, impossibile.

Sia F* il sottoinsieme di F con residuo non nullo. È finito, e per ogni codice ammesso

`3^k | R(α,β)`, quindi `k≤ν₃(|R(α,β)|)`.

Se F* è vuoto, non ci sono codici e si può porre K=0. Altrimenti prendere

`K=max_((α,β)∈F*)ν₃(|R(α,β)|)`.

Si ottiene k≤K. K è un massimo ESISTENZIALE di un insieme finito. Non si deduce un valore numerico di K dal solo bound di cardinalità del §1. Non si applica Evertse e non si scambia un bound sul numero di code con uno sulla loro profondità.

## 4. Conteggio delle parole e delle sorgenti

La parola originale ha sorgente u≤X, target n≥1 e totale A. Il budget elementare già verificato in `TwoEditSparsity.exact_word_exponent_budget` dà

`2^A n≤4^k u≤4^K X`.

Quindi `A≤2K+log₂X`. Il numero delle liste di esponenti positivi di lunghezza≤K e totale≤2K+floor(log₂X) è O_K((1+logX)^K): per lunghezza j si può usare il numero di composizioni `binom(H,j)`, H=2K+floor(log₂X). Il caso K=0 conta soltanto la parola vuota.

Ogni parola originale e il target n determinano al più una sorgente u. Vi sono al più K+1 tagli pα; a ciascuno corrispondono soltanto finitissime β dal §2. Una parola immagine e y determinano al più una sorgente v. La molteplicità aggiuntiva è dunque una costante dipendente da n,y,R₀. Questo prova il bound polilogaritmico sui codici fisici.

## 5. Raccordo con il manoscritto 148

Il [manoscritto 148 del 15 novembre](https://rstation.ai/problems/collatz/papers/148) costruisce una lingua con prefissi strettamente espansivi. Come intere parole di arrivo a n fissato, esse partono da u<n e coprono solo sorgenti finite. Come code, soddisfano ρ(α)<1 e rientrano nel caso R₀=1 della proposizione.

La crescita esponenziale del numero di parole astratte o l'ammissibilità di tutte le valutazioni non dà perciò una quota η del bacino fisico. Il manoscritto tratta minimi inversi e ostacoli al minimo controesempio; non propone quel trasferimento di massa. Il nostro corollario ne delimita l'uso nel programma presente.

## Stato

Prova candidata sottoposta a U05 per revisione indipendente. Nessun esperimento, GPU, esecuzione di codice esterno o modifica Lean. Il modulo di occupazione esistente è un input formale; la nuova deduzione di finitezza e di esclusione polilogaritmica è qui su carta.
