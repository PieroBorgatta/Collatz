# T01 — Audit e rafforzamento del controllo reciproco

15 novembre 2026. **Risultato formale verificato:** il nuovo modulo `CollatzShadowing/OrbitReciprocal.lean` dimostra integralmente il budget universale `133547/1655<81` per segmenti finiti positivi iniettivi della mappa shortcut. Contiene19 teoremi pubblici e non assume stime analitiche esterne. Nessuna pretesa di soluzione della congettura di Collatz.

## Audit della deduzione precedente

Ho recuperato nuovamente i metadati primari Zenodo del record 22087163 e il PDF di Michael John Curry, *An Explicit Windowed Sparsity Bound for Divergent 3x+1 Orbits, with Logarithmic-Floor Exclusion beyond the Harmonic Barrier*, 24 agosto 2026, DOI https://doi.org/10.5281/zenodo.22087163. Licenza dichiarata CC-BY-4.0. La lettura integrale conferma che il Teorema2.3 usa soltanto l'iniettività di `T^N` sull'insieme contato: nel caso leggero si fissa prima il numero m di passi dispari e la traslazione comune. La traduzione del vecchio sprint ai segmenti finiti è corretta: si tolgono gli ultimi N punti, non si asserisce l'iniettività dei loro futuri.

L'estensione a un segmento di primo arrivo è corretta, inclusa l'espansione Syracuse→shortcut. Il caso sorgente=bersaglio va interpretato come primo arrivo al tempo0, senza consentire una ripetizione del ciclo. Il controllo precedente `B<120000` non ha mostrato errori, ma si può migliorare in modo elementare evitando l'entropia e il fattore N+1.

## Attribuzione e confronto con la fonte Valbuena

T03 ha individuato anche Lucas Valbuena, *Collatz basin densities and canonical traces from first-passage stabilization*, sezione “Uniform control of finite distinct trajectories”, versione fissata al commit [a7275d5a73814d3d9a400c6fe6577de9542b03a3](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/tao-basin-densities.tex). Ho letto direttamente il sorgente della sezione: vi è già un packing uniforme per segmenti finiti distinti, la somma reciproca uniforme e il bound sul prodotto. La prova usa la ricorrenza `A(X)≤A(3X^c)+2X^b+floor(log₂X)` e induzione forte, con `b>H₂(log₃2)` e `c<1`; la stima del bordo è esplicita. La ricostruzione del principio di universalità quindi non è presentata come scoperta bibliografica nuova. Qui si aggiungono una prova differente via momento esatto, una costante razionale concreta e la verifica Lean dei passaggi finiti.

Precisazione sul dominio: un periodo di un ciclo percorso una sola volta è un segmento distinto e rientra nel bound. Non vi rientra la stessa orbita ciclica ripetuta con molteplicità. Anche la definizione di “collision-free” del Teorema2.3 di Curry ammette il valore insieme di un ciclo, perché T vi agisce come permutazione; la successiva frase della fonte che esclude i cicli da tutte le ipotesi è più ampia di quanto consenta la sua definizione. Questa osservazione non esclude alcun ciclo e non cambia la prova.

## Nuovo conteggio nelle bande diadiche

Sia `T(0)=0`, `T(n)=n/2` se n pari, `(3n+1)/2` se n dispari; sia `J(s,j)` il numero di dispari nei primi j stati. Le definizioni coincidono con `ShortcutCoverage.T` e `PrefixOptimality.J`.

Per n nella banda `[2^j,2^(j+1))`, scriviamo univocamente `n=s+2^j`, con `0≤s<2^j`. La traslazione è unica, include legittimamente s=0 e conserva l'intera parola di parità di lunghezza j. Vale

`T^j(n)=T^j(s)+3^{J(s,j)}`.

La stima affine elementare

`2^j T^j(s)<3^{J(s,j)}(s+2^j)`

vale anche a s=0,j=0; dunque, per s<2^j,

`T^j(s)<2·3^{J(s,j)}`.

Se `T^j` è iniettiva su A contenuto nella banda, le sorgenti con `J(s,j)=m` hanno immagini `T^j(s)` distinte in `[0,2·3^m)`. Ne segue

`card {n∈A:J(n−2^j,j)=m}≤2·3^m`.

Sommando le fibre leggere m<M:

`card_light≤Σ_(m<M)2·3^m=3^M−1<3^M`.

## Momento esatto della parità

Non serve un'approssimazione entropica. Per ogni semianello commutativo e q vale l'identità finita

`Σ_(0≤s<2^j)q^{J(s,j)}=(1+q)^j`.

Prova: accoppiare s e s+2^j nell'intervallo di lunghezza2^(j+1). I primi j bit sono uguali, mentre il bit al tempo j è complementato poiché l'offset al tempo j è la potenza dispari `3^{J(s,j)}`. Il contributo della coppia è `(1+q)q^{J(s,j)}`. L'induzione parte da j=0.

Con q=3/2, un conteggio pesante `J≥M` soddisfa

`card_heavy·(3/2)^M≤(5/2)^j`,

quindi, dividendo per2^j,

`card_heavy/2^j≤(5/4)^j(2/3)^M`.

Aggiungendo il pezzo leggero:

`card(A)/2^j≤(5/4)^j(2/3)^M+3^M/2^j`.

Questo passaggio non presuppone iniettività della mappa s→parità: il momento esatto è dimostrato direttamente tramite il lift. L'iniettività di `T^j` viene usata unicamente nel conteggio leggero.

## Somma universale razionale

Sia O il valore insieme di un segmento finito iniettivo di T. Per ogni banda si scartano al più j punti terminali, ottenendo

`card(O∩[2^j,2^(j+1)))/2^j ≤ j/2^j + H_j + L_j`,

con `M=floor(3j/5)`, `H_j=(5/4)^j(2/3)^M`, `L_j=3^M/2^j`.

Scrivendo `j=5r+s`, s=0,…,4, e `c_s=floor(3s/5)=(0,0,1,1,2)`,

`H_(5r+s) = h_s (3125/3456)^r`,
`L_(5r+s) = l_s (27/32)^r`,

con

`h=(1,5/4,25/24,125/96,625/576)`,
`l=(1,1/2,3/4,3/8,9/16)`.

Il punto1 contribuisce al più1; `Σ_(j≥1)j/2^j=2`; i termini j=0 di H e L valgono entrambi1. Quindi

`Σ_(x∈O)1/x ≤ 1+Σ_s h_s/(1−3125/3456)+Σ_s l_s/(1−27/32)`

`=133547/1655 <81`.

Tutte le costanti sono razionali e le due serie sono geometriche con ragioni strettamente minori di1. La costante è indipendente da sorgente, bersaglio, lunghezza e altezza. Non si conta un ciclo ripetuto con molteplicità.

Per un segmento Syracuse di primo arrivo, il prodotto affine soddisfa quindi

`Π_(i<k)(1+1/(3n_i))≤exp((133547/1655)/3)<exp(27)`.

Per una seconda parola reale con gli stessi k e A verso il fratello canonico y≤21n:

`v≤21 exp(27) u`.

Come nel vecchio sprint, l'esistenza di una parola trasformata e la quota relativa di sorgenti trasferibili rimangono aperte. Migliorare D non genera η.

## Stato formale e verifiche

`lake build CollatzShadowing.OrbitReciprocal`: **PASS**,3298 jobs,120s per il target, nessun errore o avviso. La [ricevuta](../../../research/research_sprint_2026-11-15/t01/build_receipt.json) registra hash del sorgente e dell’olean, toolchain e19 teoremi pubblici. Il controllo aggregato delle dipendenze/assiomi viene gestito dal coordinatore.

Il replay indipendente [verify_dyadic.py](../../../research/research_sprint_2026-11-15/t01/verify_dyadic.py) controlla131071 rappresentanti per j=0,…,16,131071 coppie di bit complementari,3850 segmenti di primo arrivo a5 da sorgenti dispari<8192 e49907 finestre di banda. Esiti normale e `-O` identici, entrambi **PASS**. I replay finiti non vengono usati per provare la costante universale: questa segue dalla prova Lean.

Il nuovo modulo resta distinto dall’adattatore `FiniteOrbitTransfer`, che assume il bound della finestra: qui il conteggio reale è dimostrato e la somma universale non è un input. Le dichiarazioni finali sono `finite_orbit_reciprocal_sum_le`, `finite_orbit_reciprocal_sum_lt_eighty_one` (scalari razionali) e `finite_orbit_reciprocal_sum_real_lt_eighty_one` (scalari reali).

Il coordinatore ha verificato indipendentemente l’algebra delle cinque classi e le ragioni geometriche; T03 ha ricontrollato traslazione, fibre leggere, momento pesante e bordo finito senza individuare errori. T01 ha inoltre letto integralmente e controllato matematicamente i moduli del coordinatore `WordProductEnvelope` e la parte strutturale di `FirstArrivalBudget`: identità del prodotto, clock crescente, parità degli stati interni e trasferimento del primo arrivo sono coerenti, inclusi i bordi di tempo0.

Nei moduli separati del coordinatore `WordProductEnvelope` e `FirstArrivalBudget`, l’estensione al prodotto, il budget Syracuse di primo arrivo e l’altezza canonica `21 exp(27) u` sono stati scritti e revisionati matematicamente da T01. Ho letto anche i tre corollari conclusivi: il budget Syracuse esclude il terminale ed è quindi dominato dal budget shortcut; i due bound di altezza mantengono correttamente l’esistenza della nuova parola come ipotesi. La compilazione di quei moduli e l’audit aggregato sono gestiti dal coordinatore. I confini della massa relativa η non cambiano.

Sorgente `OrbitReciprocal.lean` congelato dopo il build PASS: SHA-256 `750ee15525eea3dd9f7ea7cb1a90a9d07425680555949e322251a073c24875e0`. Nessun modulo preesistente modificato da T01, nessun commit o push.
