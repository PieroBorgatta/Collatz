# Il routing uniforme consuma il guadagno della salita

16 novembre 2026. Deduzione elementare su carta, da sottoporre a revisione incrociata. Nessuna nuova prova Lean o sperimentazione. Il risultato riguarda un'architettura precisa: un blocco inverso a lunghezza e totale fissati, che instradi **ogni** root in un residuo prescritto, seguito da un corridoio di esponenti1. Non vieta gli editor globali condizionati a una spine.

## 1. Il risultato esterno da usare, senza riprovarlo

Il [primario48/v2, Theorem8, §9](https://rstation.ai/problems/collatz/papers/48), datato28 ottobre2026, dà routing inverso legale da ogni unità dispari positiva a ogni classe unità modulo3^r, con totale O(r), cap individuale logaritmico e un clock comune b a totale esattamente2b. Supera il budget quasi lineare del precedente37. Le costanti sono non calcolate. Si tratta di un manoscritto; non ne abbiamo riprodotto le verifiche né importato i teoremi in Lean.

Questo risolve la raggiungibilità modulare con costo controllato. Occorre ancora confrontare quel costo con il guadagno reale richiesto a un piccolo nuovo seed.

## 2. Conteggio con qualunque totale fissato

Fissare b≥1, E≥b, r≥1 e un residuo a unità modulo3^r. Una parola di b esponenti positivi, totale E, ha la forma inversa

`I_w(x)=(2^E x−C_w)/3^b`.

La condizione `I_w(x)≡a mod3^r` impone **un solo** residuo del root x modulo3^(b+r):

`x≡2^(−E)(C_w+3^b a) mod3^(b+r)`.

Ulteriori guardie di legalità possono soltanto ridurre la copertura. I root unità hanno `2·3^(b+r−1)` residui a questa precisione. Per coprirli tutti occorre perciò

`binom(E−1,b−1)≥2·3^(b+r−1)`.

Poiché il numero delle composizioni di E in b parti è al più `2^(E−1)`, il fattore reale inverso deve soddisfare

**`R=2^E/3^b≥4·3^(r−1)`.**

È un vincolo necessario all'intera famiglia di routing, non una stima del suo tempo di ricerca. La prova usa solo congruenze e counting; non usa floor, densità o nonperiodicità.

## 3. Appendere una salita non ripaga quel routing

Per poter appendere k inverse di esponente1, mantenendo l'unità anche alla fine, è sufficiente instradare in `−1 mod3^(k+1)`. Infatti

`I_1^k(y)+1=(2/3)^k(y+1)`.

Applicando il conteggio con r=k+1, il fattore reale del percorso composto è almeno

**`R_final=R(2/3)^k≥4·2^k`.**

Per b,E,k fissati, il menu di parole è finito. Gli offset affini possono favorire alcuni root piccoli, ma per root arbitrariamente grandi il rapporto nuovo seed/root tende a R_final, uniformemente sul menu. Questa architettura uniforme non può quindi dare discesa per tutti i root grandi, neppure migliorando la costante nascosta di un routing centrale già lineare.

Non segue che ogni singolo root abbia seed grande: la conclusione è uniforme e asintotica per quella famiglia a parametri fissati. Se lunghezza o totale dipendono dal root, o se si copre soltanto una classe rara, va rifatto il conteggio con i quantificatori corretti.

## 4. Quale condizionamento potrebbe ancora servire

Se il blocco deve coprire soltanto una frazione δ dei residui unità a precisione3^(b+r), il medesimo argomento dà `R≥4δ·3^(r−1)`, quindi `R_final≥4δ·2^k` per r=k+1. Evitare questa specifica espansione richiede almeno una classe molto rara, dell'ordine di2^(−k), oppure una costruzione differente.

Una parola osservata da un seed fissato fornisce proprio informazione rara sul root. Questo lascia aperta una direzione concreta: sfruttare quella informazione **per costruire un altro ramo**, conservando la relazione tra le due parole e gli offset veri. Il solo routing a tutte le classi cancella il vantaggio. Il bound è una diagnosi del costo, non il lemma di sovrapposizione condizionata che ancora manca.

Per un solo witness per indice, anche un gain grezzo uniformemente limitato non basta: `Γ_j≤C/Ω_j≤CbP₀/n_j`, e la somma reciproca sulla spine iniettiva è già finita nel progetto. Occorre un guadagno comparabile a n_j rispetto al nuovo seed, oppure una massa di witness sufficientemente grande. Un ulteriore floor assoluto sui percorsi non fornisce da solo tale confronto.
