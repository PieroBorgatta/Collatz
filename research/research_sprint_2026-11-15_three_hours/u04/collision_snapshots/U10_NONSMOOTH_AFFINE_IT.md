# U10 — Moltiplicatori esterni al gruppo generato da 2 e 3

Sessione del 15–16 novembre 2026, base `203cbb8`. Questa nota distingue una prova elementare dalla verifica finita di trasporti reali. Nessun nuovo enunciato Lean, nessuna GPU, nessuna estensione automatica della griglia.

## 1. Una dicotomia utile, senza rivendicazione di priorità

Il controllo U08 ricava dalle fonti Duran/Leen la stabilità asintotica dei bacini sotto mappe affini con coefficiente in `2^ℤ3^ℤ`, nei domini interi. Quella stabilità usa coalescenza a tempi finiti nella legge limite della sorgente. Non può essere estesa automaticamente a un coefficiente con un altro primo.

Il seguente lemma è una conseguenza diretta della classica formula affine delle iterate. La fonte primaria di riferimento è [Terras, *A stopping time problem on the positive integers*, 1976](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers). Non è stata trovata nelle fonti lette questa esatta formulazione quantitativa; ciò non ne stabilisce la novità bibliografica.

### Lemma: nessuna coalescenza a tempo stretto per coefficienti esterni

Siano `a=P/Q>0` in termini ridotti, `a∉2^ℤ3^ℤ`, e `b=B/Q`, con P,Q positivi e B intero. Si considerino soltanto u positivi per cui `v=(Pu+B)/Q` è un intero positivo. Se le orbite **ordinarie** coalescono con tempi r,s entrambi al più N, allora

`u≤(|B|+Q)6^N`.                                                (1)

Per la shortcut si ha analogamente il bound, volutamente non ottimizzato,

`u≤(|B|+2Q)6^N`.                                               (2)

Non è richiesto r=s. Una futura coalescenza, o la convergenza di entrambe le orbite a1, non è esclusa. Il lemma dice che il suo orizzonte deve crescere almeno logaritmicamente con u: per esempio dalla (1), `max(r,s)≥log₆(u/(|B|+Q))`.

**Prova ordinaria.** Un prefisso con o passi dispari e e dimezzamenti, o+e≤N, ha formula

`C^r(u)=(3^o u+R)/2^e`,

con R intero nonnegativo. Ogni aggiunta di1 contribuisce `2^(e_prima)3^(o_dopo)` al numeratore, quindi

`0≤R≤2^e(3^o−1)/2`.

Scrivere il secondo prefisso con o',e',R'. L'uguaglianza dei due endpoint implica

`[Q2^e'3^o−P2^e3^o']u=2^e3^o'B+Q2^eR'−Q2^e'R`.                 (3)

Il coefficiente a sinistra è un intero nonzero: la sua cancellazione imporrebbe `P/Q=2^(e'−e)3^(o−o')`, contrario all'ipotesi. Il suo valore assoluto è quindi almeno1. Inoltre

`2^e3^o'≤6^N`,
`2^(e+e')3^o≤6^N`, `2^(e+e')3^o'≤6^N`.

Infatti e+o≤N ed e'+o'≤N, e `2^e'3^o'≤3^N`. Il valore assoluto del membro destro di (3) è pertanto al più `(|B|+Q)6^N`, provando (1).

**Prova shortcut.** Per un prefisso di t passi con J passi dispari,

`T^t(u)=(3^J u+R_t)/2^t`, `0≤R_t≤3^t−2^t`.

Quest'ultimo bound segue per induzione dalle due ricorrenze dei numeratori. La stessa cancellazione dei coefficienti sarebbe impossibile. Ciascuno dei due termini di offset dopo moltiplicazione incrociata è al più6^N; il termine in B è al più |B|6^N. Segue (2).

Per ogni N fissato, le sorgenti che coalescono entro quell'orizzonte sono quindi finite e hanno densità zero. Il punto che differenzia p=5 dai controlli p=2,3 è questo; **non** una prova di trasferimento positivo fra bacini.

## 2. Un unico replay preregistrato di trasporti fisici

[Protocollo](../../../research/research_sprint_2026-11-15_three_hours/u10/protocol.json), [programma](../../../research/research_sprint_2026-11-15_three_hours/u10/affine_transport.py), [risultato](../../../research/research_sprint_2026-11-15_three_hours/u10/result.json), [ricevuta](../../../research/research_sprint_2026-11-15_three_hours/u10/receipt.json).

Griglia fissata prima dell'esecuzione: tutte le sorgenti dispari `u≤2^18`, target n=5,7,31,593 e sibling canonici, mappe `v=pu` per p=2,3,5,7,11,13, e cutoff2^10,2^12,2^14,2^16,2^18. Le immagini sono ammesse fino a pX, non soltanto fino a X. Ogni mappa è iniettiva e ha altezza esattamente p.

Sono state certificate fino a1 **582.034 sorgenti dispari distinte**, contando insieme originali e parti dispari delle immagini. Le membership ottenute mediante memoizzazione coincidono con una traversata diretta indipendente di ciascuna sorgente: **27.788.001 passi** per esecuzione. Zero casi irrisolti; lunghezza massima207, stato massimo36 bit. Tutti i totali originali e i lift coincidono con U03. Un timeout o un ciclo prima di1 avrebbe vietato la classificazione completa: non si è verificato.

Normale e `python -O` danno gli stessi byte, SHA-256 `3f2bf580e609c03cd724fdb095c62cb7c907bdc8fe3be8174a2d9e186b085907`. Tutte le guardie sono attive anche in modalità ottimizzata.

Al cutoff massimo, i conteggi di trasferimento dispari sono:

| n→y | Sorgenti nel bacino n | p=3 | p=5 | p=7 | p=11 | p=13 |
|---|---:|---:|---:|---:|---:|---:|
|5→85|122.825|1.964|2.893|2.801|3.053|2.936|
|7→29|25.111|3.976|6.080|5.044|7.212|6.492|
|31→125|12.256|676|935|809|1.245|972|
|593→9493|43.194|8|11|10|1|1|

Il controllo p=2 dà zero trasferimenti in ogni riga: rimuovere il primo fattore2 restituisce la stessa orbita dispari. Il controllo p=3 **non** deve dare zero a cutoff finito. La sua quota per7→29 è ancora15,83%, contro24,21% per p=5, benché la stabilità asintotica smooth di U08 escluda una quota limite positiva per p=3.

Questa osservazione impedisce di promuovere le percentuali p=5 a una evidenza di η asintotica. La griglia non è stata aumentata. Il caso avverso593 rimane particolarmente sfavorevole: p=5 trasferisce11/43.194 sorgenti dispari; `p/η/(1+log593)≈2658,51`. Anche questa cifra è soltanto finita. I conteggi ordinari, ottenuti con i lift esatti, e i confronti con il prodotto delle marginali sono nell'output; tale prodotto non è assunto come legge.

## 3. Perché la sola indipendenza non risolverebbe H

Siano d_n e d_y le densità dei due bacini, qualora le leggi congiunte necessarie esistano. Un'ipotetica indipendenza perfetta fra il label di u e quello di pu darebbe una quota condizionale `η_p≈d_y`, non la quota ideale `d_y/d_n` offerta dal confronto di capacità.

Se per esempio d_n e d_y fossero entrambi dell'ordine1/n, tale scelta perderebbe un fattore n rispetto a un trasporto ottimale. Un menu di K moltiplicatori con massimo D almeno K non recupera automaticamente il costo: sotto lo stesso modello indipendente `η≤Kd_y`, quindi `D/η≥1/d_y` finché quel bound è rilevante. Non è una confutazione di una costruzione aritmeticamente correlata; mostra che invocare il solo mixing generico non paga il costo richiesto.

Una continuazione avrebbe bisogno di **correlazione costruita** fra il bacino originale e quello di immagine, con costi uniformi. Una possibile domanda successiva, non eseguita perché esterna al protocollo, è usare rapporti dipendenti dai due target, ad esempio `v=floor((y/n)u)` con regole per le residue. Essa conserva altezza≤21 ma non fornisce da sola la massa. Non se ne dichiara né novità globale né riuscita.

## Esito

Il lemma separa rigorosamente una classe di coefficienti dai no-go da coalescenza a tempo stretto. Il replay trova trasferimenti fisici veri e rende esplicito quanto poco essi distinguano l'asintotica. Nessun lower uniforme, nessuna soluzione di H o Collatz. Le GPU non erano necessarie: il problema rimasto è la prova della correlazione aritmetica, non il numero di sorgenti campionate.
