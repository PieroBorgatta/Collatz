# S11 Correzione del ponte analitico e convergenza del clock su un ramo

13 novembre 2026. Le modifiche riguardano due note storiche, senza modificare sorgenti Lean, dipendenze o PDF pubblicati. La convergenza del clock qui sotto è una deduzione su carta, non una nuova dichiarazione Lean.

## Correzioni apportate

La [nota A0WeakApproximation](../../phase10_A0_weak_approximation_theorem_2026-05-25.md) conserva la disuguaglianza finita di errore dell'azione, ma ritira la conclusione Cauchy dai soli drift successivi tendenti a zero. Il controesempio positivo substocastico a uno stato `K_(2^m)=(1+sin(log(m+1)))/2` soddisfa quel drift senza convergere. La nuova A0W7 richiede uno spazio comune, compatibilità di proiezioni/inclusioni e una maggiorazione sommabile degli incrementi completi, oppure una vera stima Cauchy fra scale arbitrarie. La completezza va dichiarata nella norma usata; identificare il limite con un operatore prescritto è un ulteriore obbligo.

La [nota Gate10B](../../phase10_gate10B_conditional_closure.md) distingue ora i pesi uniformi delle classi residue dall'integrazione di una funzione. Per una funzione cilindrica il valore sul rappresentante dà la media corretta. Per una funzione soltanto misurabile ciò è falso: `1_(Z₂\N)` ha media Haar 1 e tutti i campioni naturali zero. Se le righe fossero veri integrali condizionali, la proprietà della torre darebbe già la media sul cilindro padre a ogni profondità. Per campioni puntuali serve invece una ricostruzione cilindrica `g_m` con errore `||g_m−g||_1→0`, o un'altra stima di quadratura. Il teorema martingala per integrali veri non dimostra questo errore.

Sono state rettificate l'apertura, le ipotesi H3/B, i punti P3/P5/P6, il verdetto di chiusura e la distinzione dalla provenienza finita dei generatori. Il gate rimane aperto. I conteggi di bordo già validi sono conservati.

## Un caso positivo dal nuovo ramo macro

Nel ramo [S07](S07_MACRO_IT.md), r è fissato e t varia nella progressione che soddisfa `9^r t≡9 mod64`. Il nuovo parametro ha forma

`q_j=q_0+bj`, con `q_0>0`, `b=27·9^r>0` dispari, `j≥0`.

Definiamo `c_j=floor(ν₂(q_j)/3)`. Per ogni intero `R≥0`, poniamo `P=8^R`. La condizione `c_j≥R` equivale a `P|q_j`. Poiché b è invertibile modulo P, seleziona una sola classe di j modulo P. Su U≥1 indici consecutivi il numero è fra `floor(U/P)` e `ceil(U/P)`.

Più precisamente, il clock troncato `min(c_j,R)` è P-periodico: aggiungere bP conserva la valutazione sotto 3R e conserva la divisibilità per P sopra quella soglia. Su un periodo completo, le frequenze sono

`Pr(min(c,R)=k)=(7/8)8^(−k)` per `0≤k<R`,

`Pr(min(c,R)=R)=8^(−R)`.

Per k<R, si sottraggono le frequenze di divisibilità per `8^k` e `8^(k+1)`. Il troncamento R=0 è costante e soddisfa la stessa convenzione. q_j è sempre positivo, quindi non compare la valutazione infinita di zero.

## Lemma di convergenza con errore sommabile

Sia F una funzione dei clock naturali con `|F(k)|≤M`, M≥0. La serie

`H(F)=Σ_(k≥0) (7/8)8^(−k)F(k)`

converge assolutamente. Per ogni U≥1, R≥0 e P=8^R,

`|U^(−1) Σ_(0≤j<U) F(c_j) − H(F)| ≤ 4M/P + 2M(P+1)/U`.       (1)

La prova separa tre termini, senza indipendenza statistica.

1. **Coda empirica.** Sostituire F(c_j) con `F_R(c_j)=F(min(c_j,R))` cambia al più 2M su ciascun indice con `c_j≥R`. La differenza media è quindi al più `2M(1/P+1/U)`.
2. **Media del periodo.** Scrivere `U=aP+d`, `0≤d<P`. I periodi completi hanno la media esatta H_R; il residuo di d termini cambia la media al più `2Md/U≤2MP/U`, perché entrambi i valori e la media hanno modulo al più M.
3. **Coda del modello.** La massa geometrica dei clock almeno R è `1/P`. Sostituire F con F_R nella serie cambia al più `2M/P`.

La somma è (1). Scegliere R con `8^R≤sqrt(U)<8^(R+1)` dà

`errore ≤ 36M/sqrt(U)`.

Infatti `1/P<8/sqrt(U)`, `P/U≤1/sqrt(U)` e `1/U≤1/sqrt(U)`. Su `U=2^m` il bound è `36M·2^(−m/2)`, quindi è sommabile. In particolare le medie del solo clock convergono, e i loro incrementi diadici sono sommabili usando la distanza di ciascuna media dal medesimo limite.

La stessa dimostrazione vale per righe vettoriali F(k) in uno spazio normato reale di dimensione finita con norma al più M, usando la disuguaglianza triangolare. Il limite è la miscela geometrica delle righe prescritte.

## Portata e obbligo residuo

Il lemma riguarda tutti i parametri consecutivi di **questo ramo** e osservabili che dipendono soltanto dal clock. Il ramo non copre tutte le uscite della macro. Una riga di ritorno che dipenda anche da cofattore, destinazione, bit length o discesa rispetto alla sorgente non è automaticamente F(c_j): tale riduzione va provata, oppure i suoi errori vanno stimati a parte.

Per una famiglia troncata di rami finiti, un obiettivo corretto è provare su ogni ramo la propria periodicità o discrepanza con misura dichiarata, sommare gli errori con i pesi effettivi e aggiungere separatamente la massa delle sorgenti non assegnate e dei reset sopra soglia. Un tasso sommabile per il clock di un ramo non fornisce il bad-tail globale, un operatore infinito identificato o un gap spettrale.

Questa è una frequenza rispetto a un parametro libero, non una legge dei parametri visitati da una singola orbita. Non autorizza concatenazioni indipendenti o esclusione di cicli del quoziente.

## Confronto e verifica

S09 ha confermato la distinzione fra autoarco del clock e ciclo realizzabile; il suo sieve di rotazioni non aggiunge un vincolo indipendente. S10 ha ricontrollato periodicità, tre errori, serie geometrica e costante 36 con i domini qui esplicitati. Il coordinatore ha ricontrollato separatamente la decomposizione di (1). S12 ha confermato il lemma, inclusi R=0 e U=1, e ha individuato tre residui editoriali nei §§8.4–8.5 che sono stati corretti prima della consegna. S13 esegue il replay indipendente dei piccoli domini.

La verifica di questa fase riguarda algebra su carta e coerenza delle modifiche Markdown. Non è stato annunciato un nuovo build Lean o un nuovo teorema globale.
