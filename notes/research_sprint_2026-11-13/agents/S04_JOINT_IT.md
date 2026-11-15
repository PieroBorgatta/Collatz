# S04 Dizionario esatto per atomi congiunti e predecessori

13 novembre 2026. Integrazione indipendente di un meccanismo finito individuato nella nuova fonte [rStation paper 10 v3](https://rstation.ai/problems/collatz/papers/10), §3. Il codice esterno non è una dipendenza; non è stato importato alcun teorema di mixing.

## Risultato integrato

Il nuovo modulo `lean/CollatzShadowing/JointAtomDictionary.lean` separa tre informazioni che devono restare congiunte: parola esatta, somma degli esponenti e residuo ternario. Per una parola positiva non vuota w, un target dispari y e `A=sum(w), k=length(w), C=C(w)`, definisce

`inverseSource(w,y)=(2^A y−C)/3^k`

e la condizione `Admissible(w,y)` composta da `C<2^A y` e dalla divisibilità `3^k | 2^A y−C`. La sottrazione naturale non viene usata per nascondere l'eventuale mancata positività.

Dieci teoremi compilati provano:

- La divisibilità, sotto la condizione di altezza, equivale alla congruenza `C≡2^A y mod3^k`.
- La sorgente inversa soddisfa l'identità affine, è positiva e dispari e realizza esattamente tutte le valutazioni della parola, con endpoint y.
- Ogni predecessore effettivo positivo dà una parola ammissibile e coincide con la sorgente inversa.
- L'ammissibilità equivale all'esistenza di un predecessore positivo dispari esatto.
- Il cutoff è esattamente `inverseSource≤X ↔ 2^A y≤3^k X+C`, una disuguaglianza che mantiene l'offset affine.
- A lunghezza k fissata, parole ammissibili differenti hanno sorgenti differenti. Non serve fissare anche A: ciò rende possibile un profilo con pesi diversi al variare del totale, senza creare collisioni nello stesso livello.
- Per qualunque catalogo finito W di parole positive non vuote a stessa lunghezza, il numero di atomi ammissibili è uguale al numero delle sorgenti distinte dell'immagine.

Il catalogo W è un input finito: il modulo non afferma che un catalogo concreto enumeri tutte le composizioni senza una sua prova di completezza. La parte nuova dell'interfaccia rispetto al solo test di cilindro è il passaggio dai residui ternari ai **conteggi di sorgenti distinte con cutoff esatto**, necessario per collegare una legge congiunta ai conteggi.

## Positività automatica e confine della formalizzazione

Per parole positive e target intero positivo, la congruenza ternaria completa forza anche la positività della sorgente: risalendo dal target, ogni inversione integrale `(2^a y−1)/3` è positiva. La condizione di altezza è quindi un dato esplicito dell'API attuale, non un ulteriore ostacolo analitico. Il coordinatore ha avviato il modulo separato `AffinePositivity.lean` per dimostrare questa automaticità e consentire la successiva equivalenza senza l'ipotesi ridondante.

L'ipotesi **Odd y** rimane invece essenziale per l'esattezza delle valutazioni Syracuse. Nel caso `w=[1], y=2`, la formula affine dà sorgente 1, ma il vero passo è `S(1)=1`, con esponente 2. L'atomo affine non certifica un endpoint accelerato pari. Questo restringe correttamente il lemma stampato nella fonte, senza contestare il suo successivo uso su target dispari.

Il verso della parola è importante: il nostro C usa l'ordine forward della dinamica. La legge X della fonte usa l'ordine inverso; per collegare i suoi atomi occorre usare `reverse(w)`. Il modulo usa soltanto C locale, quindi non inserisce silenziosamente una legge nel verso errato.

## Confronto con gli altri agenti

- Con S01 sono state confrontate la restrizione dispari, la convenzione reverse e la positività automatica.
- A S02 è stata fornita la separazione fra iniettività a profondità fissa e controllo di carico cross-depth: sono obblighi diversi, coperti rispettivamente dal dizionario e dai budget dei pool.
- A S05 è stato indicato il cap naturale `C=1` per celle fisiche costituite da singole sorgenti/parole a stessa lunghezza. Il cap non vale automaticamente per una cella aggregata del solo residuo, che può contenere molte parole. A totale A fissato il peso è uniforme e l'ottimizzazione a soglia non offre un guadagno; un profilo cross-A conserva pesi variabili senza perdere l'iniettività nello stesso livello.
- Con S06 è stata condivisa l'interfaccia per il controllo delle immagini delle trasformazioni di parole: superare una congruenza inferiore non equivale a superare quella completa o il cutoff.

## Verifiche

`lake env lean CollatzShadowing/JointAtomDictionary.lean` termina con **exit 0**, senza output, errori o avvisi. Il log è `verification/s04_joint_atoms.log`. La prima elaborazione aveva un solo problema di tattica locale nella positività della sorgente; è stato corretto e il sorgente finale ricompilato. Nessun `sorry`, assioma dichiarato o `native_decide` è stato introdotto. La build integrata e l'audit delle radici restano al coordinatore.

Il replay indipendente `experiments/s04_joint_atoms.py` confronta costruzione affine forward e inversione backward: **800 profili**, **25.720 coppie parola/target**, **348 parole ammissibili** e **1.740 controlli del cutoff**, tutti superati. Dominio: k=1,…,5, A=k,…,k+7, target dispari 1,…,39. Controlla matching esatto, supporto dei residui, positività automatica nei casi ammessi e iniettività anche fra totali diversi a k fissato. Registra il controesempio pari. Gli output normale e con `python3 -O` sono identici byte per byte.

## Cosa resta aperto

Il dizionario non minorizza il numero degli atomi né li rende uniformi. Per usarlo nella comparazione dei bacini serve una stima quantitativa della **legge congiunta** sul supporto e nell'intervallo d'altezza pertinenti. Due stime marginali separate non la sostituiscono. Il suo risultato concreto è eliminare ambiguità di dominio, orientamento e molteplicità dal primo ponte finito.
