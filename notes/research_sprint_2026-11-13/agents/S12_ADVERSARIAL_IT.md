# S12 Revisione avversa delle integrazioni e dei nuovi ponti

13 novembre 2026. Revisione in sola lettura dei sorgenti Lean e delle note storiche. Ho letto integralmente il PDF primario di Curry e verificato visivamente la pagina 2, riletto le deduzioni S10 e S11 e controllato il dominio del dizionario esatto rStation. Nessuna compilazione esterna, nuovo assioma o modifica ai moduli formali.

**Esito:** nessun errore matematico materiale individuato nei due nuovi ponti su carta. La sparsezza dei segmenti finiti e la convergenza del clock hanno domini sufficientemente precisi e prove controllabili. Il primo limita l'altezza del trasporto a totale invariato; il secondo è un autentico esempio circoscritto di convergenza con errore sommabile. La quota relativa di massa rimane aperta, così come il ponte al kernel globale e il problema dei cicli.

## Sparsezza dei segmenti finiti

Fonte primaria: [Curry, An Explicit Windowed Sparsity Bound, DOI 10.5281/zenodo.22087163](https://doi.org/10.5281/zenodo.22087163), Teorema 2.3. Il PDF originale temporaneo è `/tmp/collatz_s10_curry.pdf`; hash e provenienza sono nella ricevuta S10. Il teorema pubblicizzato riguarda insiemi collision-free, ma la dimostrazione usa unicamente l'iniettività di T^N sui punti della finestra considerata, con `N=floor(log₂X)`. Il resto è conteggio delle classi di parità e confronto delle immagini.

Ho controllato il punto delicato della traslazione. La prova sceglie uno stesso spostamento `z·2^N` per almeno metà dei punti della finestra e poi fissa il numero m di passi dispari. Per quei punti, una collisione fra le immagini dei rappresentanti traslati diventa una collisione fra le immagini T^N dei punti originali, poiché lo spostamento dell'immagine è il medesimo `z·3^m`. Non serve iniettività a tempi ulteriori. L'uso della contrazione nella classe leggera e del conteggio entropico nella classe pesante è quindi compatibile con l'ipotesi finita.

Sia `z_j=T^j(u)` per `0≤j≤L`, con valori distinti. Se L≥N, il prefisso con indici `0≤j≤L−N` ha T^N iniettiva: entrambe le immagini sono ancora nel segmento originario. Si scartano esattamente N punti terminali. Se L<N, il segmento ha L+1≤N punti e la stima è immediata. Questo dettaglio evita di attribuire erroneamente l'assenza di collisioni all'intero futuro di un segmento convergente.

Per ogni finestra `[a,a+X)`, a≥1 e X intero almeno 2, la deduzione finita dà dunque

`count ≤ N+6(N+1)(X^H(γ)+X^(γ log₂3))`.

Con `γ=3/5`, `β=49/50` e `q=2^(−1/50)`, la somma sulle bande `[2^j,2^(j+1))`, j≥1, è

`Σ_(x nel segmento) 1/x ≤ 1+Σ_(j≥1)j/2^j+12Σ_(j≥1)(j+1)q^j`

`=12/(1−q)^2−9=:B<120000`.

Ho ricontrollato l'algebra della serie e i tre confronti interi usati da S10 per gli esponenti e il limite grossolano. La costante è indipendente da lunghezza, sorgente e altezza. Il possibile punto 1 è contato una sola volta. Il risultato non si applica a un ciclo ripetuto con molteplicità.

Un segmento di primo arrivo a un bersaglio è iniettivo: una ripetizione prima del primo arrivo imporrebbe che il bersaglio fosse già stato visitato entro il primo giro del ciclo. Se il bersaglio coincide con la sorgente, il primo arrivo consentito è al tempo zero; un ritorno positivo non va chiamato primo arrivo. Nel dominio di H il bersaglio non ha ritorni, quindi questo problema non sorge. Lo stesso argomento vale per l'espansione shortcut di un segmento Syracuse.

## Conseguenza sull'altezza del trasporto

Il prodotto dei passi Syracuse soddisfa esattamente

`P=Π_(j<k)(1+1/(3n_j))=2^A n/(3^k u)`.

Gli n_j sono un sottoinsieme del segmento shortcut. Da `log(1+t)≤t` segue `P≤exp(B/3)`. Per un'altra parola reale con la stessa lunghezza k e la stessa somma A, sorgente v e bersaglio y, la nonnegatività di C' dà

`v/u≤(y/n)P`.

Per il fratello canonico `y≤16n+5≤21n`, segue il bound universale `v≤21exp(B/3)·u`. La costante è enorme e non viene proposta come stima numerica pratica. Non contraddice H.2: quest'ultima cambia il totale A mediante il solo ultimo esponente.

Questo risultato rimane una deduzione su carta dipendente dalla prova di conteggio primaria letta. Il modulo `FiniteOrbitTransfer` del coordinatore verifica un adattatore astratto; non va presentato come formalizzazione dell'intero conteggio entropico, della serie o dell'esponenziale.

## Carico della surgery a shift finiti

Ho controllato anche il bound su carta di S06. Un'immagine dispari v e un bersaglio superiore y senza ritorni fissano la parola modificata w' e la sua lunghezza k. Fissati uno shift δ e una distanza terminale `1≤q≤Q_δ`, si ricostruiscono l'indice i=k−q, la parola originale e al più una sorgente originale u. Pertanto il numero di sorgenti distinte che producono v è al più `Σ_δ Q_δ`. Le collisioni osservate dimostrano perché non si può sostituire questo limite con 1.

Per i lift ordinari, conservare l'esponente diadico e dell'input nell'output mantiene il carico: un'immagine `2^e v`, v dispari, determina e e v. Non segue però una quota ordinaria dal solo rapporto dei conteggi dispari; servono le stesse allocazioni e i pesi corretti delle parti dispari.

Il nuovo bound dell'altezza e il carico logarithmico lasciano ancora la quota relativa η da minorare. La finitezza di D e M non crea un flusso con massa positiva. I pochi successi del censimento finito non dimostrano una quota asintotica, né la sua assenza.

## Convergenza del clock su un ramo

Le ipotesi corrette sono `q_j=q0+bj`, q0,b interi positivi, b dispari, U≥1, R≥0, `P=8^R` e `|F(k)|≤M`, M≥0. Positività esclude il punto zero e la sua valutazione infinita. Il clock troncato `min(floor(ν₂(q_j)/3),R)` dipende solo da q_j modulo P. Poiché b è una unità, un periodo di P parametri visita tutte le classi.

Le frequenze esatte sono `(7/8)8^(−k)` per k<R e `1/P` per il valore troncato R. Ho ricontrollato separatamente i tre errori rispetto alla serie geometrica H:

- Sostituzione empirica con il clock troncato: al più `2M(1/P+1/U)`.
- Media su U punti rispetto a un periodo completo: al più `2MP/U`.
- Sostituzione nel modello geometrico: al più `2M/P`.

La somma è `4M/P+2M(P+1)/U`. Scegliendo P tra `sqrt(U)/8` e `sqrt(U)` si ottiene `36M/sqrt(U)`, sommabile sulle scale diadiche. I bordi R=0 e U=1 rispettano i medesimi limiti. Il modello vale anche per righe in uno spazio normato finito, con norma limitata da M.

La legge è rispetto al parametro libero consecutivo di questo ramo. Non vale automaticamente per tutte le righe del kernel, per i parametri visitati da un'orbita o per osservabili dipendenti anche da cofattore, destinazione e discesa. Questa è esattamente la distinzione necessaria per riparare il precedente salto verso Haar.

## Dizionario esatto e fonte rStation

Ho letto il Lemma 3.1 e la prova della [fonte primaria rStation](https://rstation.ai/problems/collatz/papers/10). La restrizione a target dispari è necessaria per la conclusione Syracuse. Con target 2, k=1 e totale 1, la parola inversa dà sorgente 1, mentre S(1)=1. La prova della fonte riconosce il diverso significato shortcut per target pari e usa poi target dispari.

Per un target positivo dispari, la congruenza completa rende integrali tutti gli inversi; questi sono positivi e dispari. La positività non è un nuovo input analitico. L'orientamento della parola forward locale è il reverse della parola letta outward nella fonte. A lunghezza fissata, la determinazione della parola da parte della sorgente giustifica l'iniettività usata dal dizionario locale.

Il mixing congiunto J e il passaggio agli atomi uniformi rimangono input e risultati della fonte non riprodotti in questa revisione. Non sono stati introdotti come premesse nascoste dei moduli finiti.

## Confronto fra agenti e conseguenze editoriali

Ho scambiato con S10 i controlli sul bordo temporale e sul prodotto. S11 ha recepito i residui editoriali nei paragrafi 8.4 e 8.5 della nota storica Gate10B, rendendo esplicito anche lì che il sampling è ancora aperto. S13 ha ricevuto i bordi N=L, N>L, target=sorgente, R=0 e U=1 per i replay indipendenti.

I risultati su carta sono sufficientemente precisi da entrare in una proposta di v7 tecnica con i loro confini espliciti. Non giustificano una dichiarazione di avanzamento globale verso la soluzione. Prima di presentarli come formalizzati occorre completare il conteggio della finestra e le sue conseguenze in Lean, oppure conservarne chiaramente lo stato di dimostrazioni matematiche separate. Nessuna revisione fra agenti sostituisce la revisione specialistica indipendente.
