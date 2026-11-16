# U09 — Revisione semantica finale dei quattro moduli

Lettura indipendente dei sorgenti, senza nuove compilazioni o audit assiomatici ridondanti. `FiniteHorizonBudget` e `QuadraticOccupation` coincidono con le copie già riviste; questa nota verifica in dettaglio i due moduli aggiunti successivamente. I quattro sorgenti sono congelati con hash nella [ricevuta finale](../../../research/research_sprint_2026-11-15_three_hours/u09/final_semantics_receipt.json).

## 1. SpineDispersion: sette enunciati pubblici, PASS

La parte superiore del budget è algebra finita. Il ramo selezionato deve appartenere al catalogo e avere massa esattamente `R_i/R_(i+1)`. Il floor positivo di R e la monotonia locale rendono il rapporto ben definito e compreso fra0 e1. Non sono importate la traccia Syracuse, la sua armonicità o una legge aleatoria infinita.

Il lemma finale non assume che p sia una probabilità: il fatto che i quadrati di tutti gli altri rami siano nonnegativi basta al suo **upper bound**. Perciò i suoi summandi non sono automaticamente nonnegativi. Il lemma separato `collision_defect_nonneg` paga questa conclusione richiedendo p≥0 e massa totale≤1.

Per un catalogo fisico troncato P, con i veri pesi dei rami,

`D_P=1−Σ_(j∈P)p_j² ≥ D_full`.

Il catalogo troncato è dunque un **upper** del difetto completo. Il solo valore numerico D_P≥a non dà un lower su D_full: per esempio un catalogo vuoto ha D_P=1 anche quando la legge completa è concentrata su un solo ramo e ha D_full=0. L'applicazione del budget superiore a D_full è invece corretta: `D_full≤D_P≤budget` quando il catalogo contiene il ramo selezionato.

### Certificati inferiori

Il certificato a due rami è corretto. Due rami distinti con massa almeno a implicano che ogni singola massa sia≤1−a; nonnegatività e massa totale≤1 danno quindi `D_P≥a`. Se a≤0 la conclusione è valida ma non informativa. Se a>1/2 le premesse non possono essere soddisfatte.

Il nuovo certificato di allocazione inferiore è anch'esso corretto, nella forma più generale dichiarata. Con `L=Σ lower_i`, `lower_i≤p_i`, `lower_i≤M` e M≥0, per ogni ramo vale

`p_i≤1−L+M`.

Il fattore a destra è nonnegativo perché L≤Σp≤1. Ne segue

`Σp_i²≤(1−L+M)Σp_i≤1−L+M`, dunque `D_P≥L−M`.

Le lower allocation possono essere negative: la prova usa soltanto `p_i−lower_i≥0`. Per ottenere un lower positivo utile occorre separatamente L>M. La generalità signed non produce massa positiva gratuitamente.

Questi due certificati inferiori si trasferiscono alla legge completa attraverso un argomento diverso dal solo D_P. La stessa disuguaglianza resta valida su **ogni estensione finita** del catalogo dei testimoni. Nel certificato di allocazione si estende lower con0 sui nuovi rami; p≥0 e M≥0 mantengono tutte le ipotesi. Passando al limite diretto delle estensioni finite si ottiene il medesimo lower su D_full. I testimoni devono rappresentare rami fisici distinti, oppure avere allocazioni già aggregate per ramo. Duplicare etichette non è un certificato di nuova massa.

### Budget e bordo

Il telescopio del budget vale anche per N=0. Per N>0 usa soltanto floor e monotonia fino all'indice N; non assume una monotonia globale non dichiarata. La conclusione è finita e dipende da `R_N−R_0`. Una sommabilità infinita uniforme richiede inoltre che R_N abbia un upper indipendente da N. Tale input non è dimostrato dal modulo e, nell'applicazione Syracuse, appartiene alle identità analitiche esterne.

Non vi è un lower globale, né viene asserita l'esistenza dei due rami o delle allocazioni utili. Il certificato a due rami e quello di allocazione sono interfacce condizionali verificabili.

## 2. BoundedSlopeCatalogue: cinque enunciati pubblici, PASS

`catalogue n R` è un **insieme di liste**, non un conteggio di rappresentazioni o una famiglia indicizzata con etichette duplicate. Richiede una sorgente positiva, un match effettivo, endpoint n e `wordWeight≥1/R`. R è razionale e strettamente positivo negli enunciati di finitezza. Questa ipotesi è sostanziale: per R≤0 il confronto con1/R non sarebbe un cutoff positivo del peso.

La sorgente scelta non computabilmente per ciascuna lista soddisfa tutte le proprietà del catalogo. Il budget quadratico ammette sorgenti ripetute, perciò la scelta non nasconde un'ipotesi di iniettività. Ogni parola del sottocatalogo spende almeno1/R² e la somma quadratica dà l'upper esplicito

`|W|≤2·visitConstant(n)·R²`.

La dimostrazione di `catalogue_finite` usa questa maggiorazione su **tutti i sottocataloghi finiti** e contraddice un sottoinsieme di cardinalità `ceil(B)+1`. Solo **dopo** avere provato la finitezza viene usato `Set.ncard` per il catalogo completo. È così evitato il falso argomento che tratterebbe `ncard` di un insieme infinito, uguale a0, come un suo conteggio effettivo.

### Domini e casi limite

- Le sorgenti pari positive sono ammesse. Possono avere esponente iniziale0; dopo un passo S produce un dispari. Il modulo non afferma che tutti gli esponenti siano positivi nel suo dominio più ampio.
- Un target n=0 non può essere raggiunto da una sorgente positiva, dunque il catalogo è vuoto. `visitConstant(0)=0` rende coerente il bound numerico.
- Per un target pari positivo, l'unica eventuale parola è quella vuota: ogni iterazione nonvuota di S è dispari. Il risultato rimane valido.
- La parola vuota è inclusa precisamente quando il suo peso1 soddisfa il cutoff; per n>0 ciò avviene se R≥1.
- Cicli e ripetizioni sono ammessi. Al punto1, per esempio, i pesi delle parole `[2,…,2]` sono `(3/4)^k`; un cutoff positivo ne conserva soltanto finitissime. Non occorre conoscere o assumere il periodo dei target ipoteticamente ciclici.

### Ciò che è numerico e ciò che è solo esistenziale

Il bound di cardinalità del catalogo e il bound sulla sorgente `u≤R·n` sono espliciti. La finitezza fornisce inoltre **l'esistenza** di massimi della lunghezza e della somma degli esponenti. Non si ricava il valore numerico di quei massimi dal numero delle parole: una piccola famiglia finita può contenere parole molto lunghe.

Il modulo non produce quindi un cutoff temporale effettivo, una procedura che certifichi completata un'enumerazione, o il no-go polilogaritmico completo di U11. La [prova su carta U11](U11_BOUNDED_SLOPE_IT.md) usa correttamente la finitezza per costruire un massimo esistenziale delle valutazioni dei residui di finitissime coppie di code; quel passaggio e il conteggio asintotico rimangono separati dal modulo. Il suo dominio dispari a esponenti positivi è una sottoclasse di quello formale.

## 3. Esito e provenienza

Esito semantico: **PASS** sui due nuovi moduli, per12 enunciati pubblici. I due moduli precedenti, con16 enunciati, coincidono con la revisione iniziale:28 enunciati pubblici complessivi nei quattro moduli dello sprint.

La finitezza del Green tilt e la sua estensione ciclica erano già pubbliche nel paper9/v1, Proposizione11; i moduli non ne rivendicano la priorità. I meccanismi di collisione e primo split sono classici. Le prove formali locali, i certificati finiti e i corollari analitici devono restare distinti. Questa lettura non sostituisce la compilazione e l'audit integrato che svolge il coordinatore; nessun Lean è stato modificato e non è stato eseguito un altro audit o esperimento.
