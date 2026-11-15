# T04 Revisione indipendente e blocchi terminali di profondità limitata

15 novembre 2026. **Esito della revisione T02: nessun errore trovato nella prova su carta**, nei quantificatori dichiarati. La parte asintotica dipende dal Corollario 2 di Evertse; non è stata formalizzata in Lean. Ho ricostruito la prova senza eseguire o importare il programma T02 e ho aggiunto due replay indipendenti. Ne ricavo anche un'estensione: la scarsità non riguarda soltanto due esponenti, ma qualunque sostituzione di un blocco terminale di lunghezza fissata, anche con cambiamento limitato di profondità e totale.

## Revisione della prova T02

La scrittura della costante per concatenazione è

`C(p ++ t)=3^|t| C(p)+2^Σp C(t)`.

La modifica dell'ultimo esponente non cambia la costante. Con un aumento d>0 in posizione i e diminuzione d dell'ultimo, la differenza delle costanti è `(2^d−1)2^P T`, dove P è il totale originale fino a i e T la costante della coda lunga q=k−i. Sottraendo le identità affini si ottengono esattamente i residui T02. Nel segno negativo il fattore è `2^(P−d)`; il P del modulo Lean è invece il totale nuovo. Non è una discrepanza matematica.

La coda soddisfa `T≡2^B n mod3^q`, quindi i due residui danno rispettivamente `3^q | y−2^d n` e `3^q | 2^d y−n`. Per target dispari questi interi sono dispari e non nulli. Il limite q≤Q_δ è pertanto uniforme per lo shift fissato, mentre k non è ancora limitato. La costante T è dispari e B≥q≥1: entrambi i residui completi R sono dispari, quindi non nulli. L'identità `3^k(v−u)=2^P R` implica `3^k|R` per coprimalità.

Ho letto visivamente la pagina stampata 228 di [Evertse, *On sums of S-units and linear recurrences*, Compositio 53 (1984)](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf). Il Corollario 2 ammette sottosomme nulle; richiede coordinate non nulle e somma totale non nulla. Per coordinate S-unità, il prodotto dei valori assoluti su S è uno. Il minimo dei valori assoluti in 3 è costante positiva quando i coefficienti sono fissati e variano soltanto potenze di 2. È proprio questa versione, con minimo e non massimo, a sostenere l'applicazione.

Nel residuo T02 il numero delle coordinate è q+1, i coefficienti sono fissati per q,n,y,d, le potenze di 2 non superano B+d e q appartiene a un insieme finito. Si ottiene `k≤τA+C_τ` per ogni τ>0. Il budget elementare `2^A n≤4^k u` è valido anche con ritorni e dà `A≤2k+log₂X`. Assorbendo 2τk si ricava k=o(log X), poi A≤log₂X+o(log X).

La somma delle composizioni positive di lunghezza k e totale ≤L è `binom(L,k)`. Per k=o(log X) e L=O(log X), la somma sul piccolo intervallo di lunghezze è X^o(1). Una parola determina al più una sorgente; δ e q determinano la parola nuova e al più un'immagine. Non si sta contando con molteplicità illimitata una stessa etichetta. La conclusione riguarda dunque anche i codici fisici, non soltanto le sorgenti.

Infine, per la relazione di primo arrivo, la coda pesata degli shift soddisfa il limite uniforme per sorgente g_R dichiarato da T02. Si fa prima X→∞ con R fissato e poi R→∞. L'assenza di un cutoff su v è compatibile con tutta la prova. Sono invece essenziali il primo arrivo o un'altra unicità della parola per la conclusione sulla miscela pesata, e il controllo uniforme della coda. Non ho trovato una giustificazione per l'unione **non pesata** di tutti gli shift con distanza terminale crescente: T02 non la rivendica.

## Estensione 1: riscrivere una coda intera di lunghezza fissata

Fissiamo n≠y positivi dispari e L≥1. Consideriamo parole reali

`w=p ++ α : u→n`, `w'=p ++ β : v→y`,

con `|α|=|β|=L` e `Σα=Σβ=B`. Gli esponenti di α e β possono cambiare **arbitrariamente**; nessun limite individuale agli shift è necessario. Il prefisso p è identico. Posti P=Σp e k=|p|+L, l'eliminazione del prefisso dà

`3^k(v−u)=2^P R`,

`R=2^B(y−n)−(C(β)−C(α))`.

Dunque `3^k|R`. Se R=0, allora u=v; ma due parole esatte della stessa lunghezza dalla stessa sorgente coincidono, quindi n=y. Pertanto R≠0.

Sviluppando le due costanti, R è una somma di **2L+1** coordinate non nulle del tipo

`(y−n)2^B`, `+3^j 2^σ`, `−3^j 2^σ'`, con 0≤j<L e 0≤σ,σ'<B.

Le cancellazioni tra coordinate possono essere lasciate nella somma: il Corollario 2 le permette. Con S formato da infinito, 2, 3 e i primi di y−n, ogni coordinata è una S-unità. Il minimo dei valori assoluti in 3 è almeno `3^(-max(L−1,ν₃(y−n)))`. La grandezza ordinaria delle coordinate è ≤C_(n,y,L)2^B. Evertse dà `k≤τB+C_τ`, quindi il medesimo assorbimento T02 dà k=o(log X), A=O(log X), e X^o(1) parole originali.

Per una parola originale, le nuove code possibili sono `binom(B−1,L−1)≤(A+1)^(L−1)`: un fattore polilogaritmico. **Il numero dei codici reali con u≤X è X^o(1), senza alcun cutoff su v, anche per l'unione non pesata di tutte le riscritture di quella coda fissata.** I casi k<L coinvolgono solo lunghezze limitate e si contano direttamente con lo stesso ordine subpolinomiale.

Questa deduzione non è una rivendicazione di priorità: è un'estensione locale, ricostruita qui dal medesimo strumento classico e dalla struttura affine. L'ostruzione storica H.2 già trattava il caso speciale della sola ultima valutazione; vanno mantenuti distinti dominio, numero di passi e totale preservato.

## Estensione 2: cambiare anche la lunghezza e il totale del blocco

Fissiamo L,M≥0 e D∈ℤ. Ora α ha lunghezza L, β lunghezza M e `Σβ=Σα+D=B+D`. Siano p il prefisso comune di lunghezza r e totale P, u e v le sorgenti. La lunghezza complessiva cambia di M−L. Poniamo

`F=2^max(D,0)`, `G=2^max(−D,0)`.

Eliminando il punto finale del prefisso nelle due identità affini si ottiene

`G 3^(r+L+M)(v−u)=2^P R`,

`R=2^B(3^L F y−3^M G n)+3^M G C(α)−3^L G C(β)`.

Le potenze di 2 sono coprime con 3, perciò `3^(r+L+M)|R`. **R=0 equivale a u=v**. A differenza del caso L=M, una sorgente diagonale può effettivamente raggiungere n e y a tempi diversi; questa eccezione non può essere omessa.

Limitandosi ai trasporti **u≠v**, R è non nullo. Dopo eventuale omissione della coordinata iniziale con coefficiente zero, è somma di al più L+M+1 S-unità. Tutti i coefficienti dipendono soltanto da n,y,L,M,D; le potenze variabili di 2 sono al più B+max(D,0), a una costante fissa dall'altezza precedente. Il medesimo Corollario 2 dà

`r+L+M≤τB+C_τ`.

Il budget della parola originale usa k=r+L e resta `A≤2k+log₂X`. Di nuovo k=o(log X), A=O(log X). Per ogni parola originale il numero delle code β è al più `(A+|D|+1)^max(M−1,0)`, salvo il caso M=0, che ha al più una coda. Quindi:

**Per L,M,D fissati, il numero dei trasporti reali fuori diagonale con u≤X è X^o(1), senza limite su v.**

Nel dominio di H, i due bacini dei sibling sono disgiunti, quindi u=v è impossibile. Il risultato si applica dunque all'intera relazione. Per target collegati orbitalmente la diagonale può avere massa positiva: ad esempio `3→5` con parola [1] e `3→1` con parola [1,4], L=0, M=1, D=4. Qui R=0. È una controprova necessaria contro l'estensione scorretta senza esclusione diagonale.

## Conseguenza per la strategia

Non basta consentire un numero arbitrario di modifiche all'interno di una finestra terminale fissa. Non basta nemmeno un cambiamento fisso di profondità e totale dentro quella finestra. Qualunque unione **finita** di tali meccanismi ha ancora soltanto X^o(1) codici fuori diagonale.

Per una miscela numerabile si può concludere o(X) solo se si dimostra inoltre una coda uscente uniformemente piccola per sorgente, come nella pesatura T02. La mera sommabilità di pesi sui parametri L,M,D non controlla automaticamente la molteplicità delle nuove code. In particolare non si è chiusa una scelta adattiva che sposti massa verso blocchi terminali sempre più lunghi o verso D crescente con X.

Un trasferimento relativo positivo deve quindi sfuggire a ogni insieme finito di questi parametri, oppure rinunciare al prefisso comune, oppure usare un altro confronto di massa. Il trasporto di intere parole e la comparazione del kernel/trace restano strade aperte. Non ho dimostrato un'ostruzione per un numero fissato di modifiche **sparse su una finestra crescente**: la dimensione e i coefficienti del problema S-unità non rimangono uniformi con l'argomento appena dato.

## Replay indipendenti

I protocolli sono stati fissati prima dell'esecuzione in `research/research_sprint_2026-11-15/t04/`. I programmi generano le parole tramite inversione esatta passo per passo; l'ammissibilità non viene dedotta dalla sola somma affine e non viene riutilizzato il programma T02. Le traiettorie nuove sono controllate nuovamente con le valutazioni della mappa in avanti. Le guardie sono esplicite e restano attive con Python -O.

1. **Due edit:** 1.138 parole effettive, 15.213 modifiche, 603 trasporti, 346 positivi e 257 negativi. Sono inclusi target periodici, target non sibling e target divisibili per 3. Le identità, la divisibilità completa e terminale, la parità di R e il budget passano. Normale e -O identici; SHA-256 `04d1184dce0749bfb5bf2b1f07705ce10c301af5ac11daa4b290236983e1b7c6`.
2. **Sostituzione terminale:** 273 parole originali, 27.916 sostituzioni candidate, 2.586 trasporti reali: 2.429 fuori diagonale e 157 diagonali. Per tutti passano identità generale, divisibilità completa e equivalenza R=0↔u=v. Nei quattro casi sibling nessuna diagonale; nei casi collegati sono presenti e conservate. Normale e -O identici; SHA-256 `97dc4e89c107829099640215b1f8abf6e518cfae902a3cc4bce7fbfb36fa53ac`.

Le verifiche finite cercano errori nelle formule e nei confini; non provano le stime asintotiche. Nessun nuovo modulo, assioma, versione di strumento o dipendenza è stato introdotto da T04.
