# Audit del criterio e un budget per prefissi finiti

16 novembre 2026. H23. Ricerca e deduzioni su carta, senza esperimenti, compilazioni o nuove prove Lean. Le nuove deduzioni non sono presentate come risultati formalmente verificati o rivendicazioni di priorità. Il floor degli atomi rimane un input analitico esterno non ricompilato da noi.

## 1. Esito dell'audit del nucleo precedente

L'[ora precedente](../../research_ideas_2026-11-16_one_hour/ROOT_ATOM_FLOOR_CORE_IT.md) usa correttamente il lower logaritmico della [fonte12, §2](https://rstation.ai/problems/collatz/papers/12): per ogni unità positiva dispari nonperiodica v,

`liminf_(X→∞) (2/log X) Σ_(odd u≤X, u→v) 1/u ≥ α/(4v)`.

Non serve esistenza della densità naturale. Per ogni antichain FINITA di tali target, i bacini sono disgiunti; la somma armonica di tutti i dispari, normalizzata con `2/log X`, tende a1. Quindi `Σ1/v≤4/α`. Il passaggio usa additività finita e il verso corretto della disuguaglianza dei liminf. Non somma bacini annidati.

Anche la costruzione Abel opzionale passa l'audit locale. Su D, insieme numerabile delle unità positive dispari nonperiodiche, una sorgente compare a una sola profondità di hit. Questo giustifica il taglio armonico di `Σ_(k<K)L_D^k1`. Sulla coda, la somma di `sqrt(Ω)` sopra tutte le parole è una maggiorazione positiva, quindi non importa una falsa legalità dei codici. Il doppio fattore `(1−r)²` nell'identità delle somme parziali dà l'upper lineare dopo il limite. La diagonale numerabile esiste, e Fatou dà `L_Dh≤h` nel verso richiesto. Non serve uguaglianza armonica. Lo shift `ρ_(k+1)=L_D^kρ₁≤2L_D^k1` conserva il terminale completo; sostituirlo con uno shift zero sarebbe scorretto.

Queste verifiche confermano una riduzione delle dipendenze, non costruiscono una nuova massa laterale. La via breve della fonte12 rimane la scelta preferibile per il budget globale.

## 2. Proposizione: il budget si può formulare su dati finiti

Il requisito «il root è globalmente nonperiodico» è poco adatto a un futuro lemma su certificati finiti. Si può eliminarlo dal suo input aritmetico, pagando una costante più larga.

**Dati.** Sia `n₀=b,n₁,…,n_J` un vero prefisso Syracuse di unità positive dispari, con tutti gli stati distinti. Siano Ω_j i gain osservati da b a n_j. Per ogni `1≤j≤J`, sia W_j un catalogo FINITO di vere parole da seed unità v_w a n_j tale che:

1. Ogni parola raggiunge n_j per la prima volta al suo endpoint. Questo è verificabile dalla lista finita degli stati; in particolare il percorso è semplice.
2. L'ultimo genitore è diverso da `n_(j−1)`.
3. W_j è prefix-free nell'orientazione inversa, dal target al seed.

Non si richiede che il futuro del prefisso sia noto, che i seed convergano, o che tutti i root siano nonperiodici. Il clock delle parole alternative è libero. Porre `Γ_w=Ω(w)/Ω_j`.

**Input.** Assumere il lower logaritmico precedente per target nonperiodici, con α>0, e il bound uniforme del progetto `1≤P≤P₀` sui prodotti di veri primi arrivi. Il secondo input vale sui prefissi osservati distinti e su tutte le parole alternative ammesse dai dati.

**Conclusione.** Per ogni tale certificato finito,

**`Σ_(j,w∈W_j) Γ_w ≤ bP₀(8/α+1)`.**

Se nessuno degli n_j è periodico, basta il bound più forte `4bP₀/α`.

### Dimostrazione

Per ogni witness, le due identità di primo arrivo sono

`n_j=bΩ_jP_j=v_wΩ(w)P_w`.

Quindi `Γ_w=bP_j/(v_wP_w)≤bP₀/v_w`. Basta controllare il multinsieme dei reciproci dei seed, contando le eventuali ripetizioni tra cataloghi diversi.

Se tutti gli n_j sono nonperiodici, ogni seed lo è. Due seed dello stesso W_j che fossero comparabili forward darebbero parole inverse comparabili per prefisso, contro il terzo dato. Seed di due ingressi diversi non possono essere comparabili: dopo il primo ingresso nella spine, il cammino deterministico raggiunge il target successivo dal genitore osservato; non potrebbe entrarvi dal colore off-spine. Sono dunque una sola antichain e il bound è `4/α`.

Resta il caso in cui il segmento contiene punti periodici. Sia i il primo indice per cui n_i è periodico. Se i=0, tutti gli archi osservati sono sul ciclo, e ogni witness off-spine ha seed nonperiodico che entra nel ciclo per la prima volta nel proprio n_j. Gli ingressi sono distinti perché il segmento osservato è semplice. Si ottiene ancora una sola antichain.

Sia invece i≥1. Per j<i il root e i seed sono nonperiodici. Per j>i, il genitore osservato è l'unico genitore ciclico di n_j; un witness off-spine deve pertanto essere nonperiodico ed entrare nel ciclo per la prima volta proprio a n_j. I seed di TUTTI i W_j con j≠i formano una sola antichain: prima di i si distinguono per il primo ingresso nella spine; dopo i si distinguono per il primo ingresso nel ciclo. Un ingresso prima di i arriva al ciclo in n_i, quindi non può coincidere con un ingresso successivo, che vi arriva in un n_j diverso. Il loro budget è al più `4/α`.

Il catalogo W_i va separato: un suo cammino può percorrere parte del ciclo a ritroso e poi uscire verso un seed che riapparirà in un catalogo successivo. Non è lecito sommarlo gratuitamente alla precedente antichain. Al suo interno, i seed NONPERIODICI sono però ancora un'antichain. Infatti, se uno raggiungesse l'altro, lo farebbe prima del primo arrivo in n_i; le due parole inverse sarebbero comparabili per prefisso. Il loro budget è al più `4/α`.

Infine W_i contiene al più un seed PERIODICO. Ogni parola inversa verso un tale seed segue la stessa unica catena inversa ciclica fino alla prima visita del seed; tutte queste parole stanno su un solo ramo. La proprietà prefix-free ne ammette al più una. Il suo reciproco è al più1. Sommando i due budget e l'eventuale singolo termine si ottiene `Σ1/v_w≤8/α+1`, e quindi la conclusione.

La prova è stata letta e controllata separatamente da root, H21 e H22. Non è stata compilata in Lean. Nessun witness utile viene prodotto da questo upper.

## 3. Come usare il criterio senza un nuovo circolo logico

Il target precedente «ogni spine divergente produce una famiglia con somma Γ divergente» è sufficiente a escludere le spine, ma la sua formulazione universale diventa vacua se esse non esistono. Non dimostra, da sola, che abbiamo ridotto la difficoltà.

Il prossimo tentativo dovrebbe invece specificare un meccanismo su prefissi finiti: test d'ingresso, regole che conservano gli stati legali e il colore, dimensione dell'output, funzione del costo, condizioni d'uscita e lower cumulativo. La proposizione permette di usare come upper un dato finito senza certificare preventivamente la nonperiodicità globale. Un lower che crescesse senza limite sulla lunghezza dei prefissi distinti darebbe una vera contraddizione, ma tale lower resta da provare. Anche una costruzione limitata a una classe propria di prefissi sarebbe valutabile se la classe fosse esplicita; non va promossa a copertura di tutti gli interi.

Un automa che limitasse i seed a un insieme FINITO non potrebbe dare infiniti ingressi laterali distinti su una spine ipotetica. Un carry normalizzato o parametrico può essere diverso, ma deve contabilizzare la crescita dei seed. La sola complessità del linguaggio non garantisce la comparsa di un particolare reset dipendente dallo stato.

## 4. Confronto con il segno meno e con certificati di ritorno

Letto [Sultanow, Same Shadows, Different Forests](https://github.com/Sultanow/collatz/blob/cfdd47eee9cb307f4ab928aa4c99fad6d3e460b0/07%20Basins%20of%20Attraction/docs/main.tex), snapshot del16novembre10:55UTC, ampliato rispetto alla landing del [preprint v2](https://www.preprints.org/manuscript/202610.2552) del12novembre. La sezione locale riguarda densità di test su FINITAMENTE molte congruenze, mediante riflessione. La sezione sui ritorni separa certificato finito, bound uniforme della vera media d'ingresso e residuo di massa. Non prova convergenza.

Il seguente controllo di segno è una deduzione diretta. Per `S_±(x)=(3x±1)/2^e`, la riflessione `x↦−x` scambia i cataloghi completi di congruenze finite. Quindi un floor su TUTTI i residui unità della legge + si trasferisce alla legge − per la stessa riflessione. Non distingue da solo la struttura dei cicli.

Invece, su un ciclo, l'identità prodotto dà `Ω_ciclo<1` per il segno + e `Ω_ciclo>1` per il segno −. Una superfunzione finita positiva per L_- non può esistere su tutte le unità: già `S_-(1)=1`, con peso3/2, imporrebbe `h(1)≥(3/2)h(1)`. Il dominio D nonperiodico nella costruzione Abel è quindi sostanziale. Inoltre `P_+≥1` fornisce direttamente `Ωu≤n`; nel segno − serve un lower di `P_-`.

Il controllo statico del [packing del progetto](../../../lean/CollatzShadowing/OrbitReciprocal.lean) indica un trasferimento su carta, senza nuovo modulo: per il segno − restano i lift binari e i momenti Bernoulli esatti, mentre l'upper sugli endpoint dei rappresentanti migliora a `T_-^N(s)<3^J` per `s<2^N`. Tutte le maggiorazioni successive possono usare il precedente bound più debole `2·3^J`. La positività è conservata. Quindi il medesimo argomento dà `Σ1/x<81` sui segmenti iniettivi; `log(1−1/(3x))≥−1/(2x)` fornisce `P_-≥exp(−81/2)` sui primi arrivi. Questo ripara l'upper omogeneo, con una costante diversa. È un controllo di trasferibilità su carta, NON una verifica Lean del segno −, e non cambia il bersaglio di ricerca.

I cicli noti del segno − NON falsificano un criterio che mira soltanto alla divergenza nonperiodica. Il nostro programma separa già la questione dei cicli. Non abbiamo un'orbita positiva divergente di controllo per il segno − da usare come controesempio.

Controllo metodologico: `U≥1+PU`, `V≥1+2PU+PV` sono soddisfatti da `U=N`, `V=N²` sul grafo terminante. Il progresso richiede una formula con media d'ingresso uniformemente limitata e il controllo del residuo separato. L'arco nella stessa classe modulo fisso esclude un rank basato solo su quella classe SE appartiene al grafo considerato; la sua costruzione non certifica la terminazione successiva. Non esclude ogni possibile certificato.

## 5. Controlli incrociati e decisione

Le formule del controller affine di H21, il vincolo del prefisso condiviso e il counting dei seed distinti passano l'audit. Il primo disaccordo deve comparire presto, oppure la parola alternativa deve già finire presto: il clock libero non autorizza a ignorare questa seconda possibilità. I vincoli necessari non producono l'editor.

H22 ha derivato indipendentemente un reset lineare della chain contata, poi trovato che è già dimostrato nella [fonte81, v2](https://rstation.ai/problems/collatz/papers/81). L'audit delle transizioni conferma il meccanismo, ma la scoperta bibliografica impedisce di presentarlo come nuovo. La differenza ancora aperta è fra scegliere un cilindro/sorgente con un reset voluto e ottenere quel reset nel futuro già fissato di un singolo intero.

Il nuovo budget finito è un raccordo utile per rendere più preciso il prossimo tentativo. Il resto del valore dell'ora è soprattutto eliminare falsi sottoproblemi e certificati tautologici. Non è comparsa una nuova stima risolutiva. Non vedo ragione di accumulare altre riformulazioni di F o della traccia prima di un lemma che costruisca effettivamente percorsi alternativi, oppure di un bound uniforme sulla vera misura d'ingresso che affronti l'altro programma con le sue dipendenze esplicite.

## 6. Criteri per decidere se una prosecuzione vale il tempo impiegato

Il prossimo risultato dovrebbe cambiare almeno uno dei dati seguenti, con quantificatori espliciti:

- **Sorgente già data.** Deve funzionare per il futuro di un seed fissato, oppure per una classe propria chiaramente definita di tali futuri. «Per ogni lunghezza esiste una sorgente costruita» non sostituisce questo requisito.
- **Copertura del carry.** Deve aggiungere una transizione legale fra compagni che non commutano tutti con un'unica orbita razionale periodica, o una prova che la famiglia di transizioni copra i contesti richiesti. Una lista di identità affini senza copertura non basta.
- **Costo fisico.** Deve controllare il vero seed finale, il gain normalizzato o la massa prefix-free. La lunghezza corta di una descrizione o di un reset scelto non paga questi costi.
- **Frequenza utile.** Deve fornire un bilancio cumulativo divergente. Infinite occorrenze senza peso, o una densità superiore positiva applicata al peso1/(j log j), non sostituiscono quel bilancio.
- **Programma analitico alternativo.** Se si sceglie la via dei ritorni, deve limitare uniformemente la media sotto la vera legge d'ingresso e tenere separato il residuo di massa. Esistenza del certificato su ciascun grafo finito e secondo momento del modello non realizzano quel passaggio.

Fermare l'espansione di una pista se il suo output continua a essere soltanto una di queste cose: un reset già noto scelto tramite CRT; un upper su un oggetto che richiede invece un lower; un limite a root fisso usato per un root mobile; un elenco crescente di corollari della stessa traccia; un certificato che esiste prendendo come funzione proprio la quantità sconosciuta da stimare. Prima di trasformare un candidato in nuovo modulo, cercarne le formule esatte nelle fonti e scrivere l'ipotesi che manca.

Un consolidamento v7 può essere utile per correggere lo stato delle dipendenze e separare i lemmi verificati dalle ipotesi aperte. Non dovrebbe presentare queste semplificazioni come nuova evidenza di vicinanza alla congettura. La decisione di proseguire la ricerca sostanziale dovrebbe dipendere da uno dei cambiamenti sopra, non dal numero di note o agenti prodotti.

## 7. Un criterio entropico più debole dell'assoluta continuità

La nuova [fonte150, v2, Corollary4](https://rstation.ai/problems/collatz/papers/150) impone a ogni limite empirico ternario di una possibile orbita divergente una componente singolare su un insieme universale di Haar nullo. Riguarda i valori Syracuse reali nel tempo, non la legge inversa Q. Non la elimina. Il testo è stato letto tramite il download API di v2; nessun suo checker è stato eseguito.

Una deduzione elementare del coding dà una soglia diversa, utile per formulare cosa dovrebbe aggiungere una nuova idea. Non si rivendica priorità: è la disuguaglianza di massima entropia geometrica applicata alle parole del vero passato.

Sia `ell=log₂3` e porre `G(a)=a log a−(a−1)log(a−1)` per a>1. Se ν è QUALUNQUE limite debole delle leggi empiriche dei residui ternari di una possibile orbita nonperiodica, allora per ogni m≥1,

**`H(ν mod3^m)≤m G(ell)`.**

Qui H è l'entropia di Shannon con logaritmi naturali. La conclusione normalizzata è

`limsup_m H(ν mod3^m)/(m log3) ≤ θ`,

`θ=G(ell)/log3=H₂(log₃2)<1`.

H₂ nell'ultima espressione usa logaritmi in base2. Si tratta di dimensione informazionale tramite entropie finite, non di un'asserzione automatica sulle dimensioni locali di ogni punto.

**Prova.** Siano e_k i veri gap Syracuse. Il telescopio della ricorrenza e `n_k→∞` danno `limsup_N (Σ_(k≤N)e_k)/N≤ell`. Per k scelto uniformemente tra m e N, il blocco degli ultimi m gap ha costo medio al più `m ell+o_N(1)`: ogni gap compare in al più m blocchi. Il blocco determina esattamente `n_k mod3^m`, perché l'offset affine della parola soddisfa `2^A n_k≡C_word (mod3^m)`. Quindi l'entropia del residuo non supera quella del blocco.

Per un m-tuple di interi positivi con somma media al più ma, la disuguaglianza di Gibbs rispetto al prodotto delle geometriche di media a dà entropia al più `m G(a)`. Applicarla con a arbitrariamente vicino a ell sopra il costo medio. Fissato m, le distribuzioni empiriche dei residui convergono lungo la sottosuccessione a ν sulla partizione clopen finita; la loro entropia converge. Omettere i primi m indici cambia tale legge di o(1). Passando prima N→∞ e poi a→ell si ottiene il bound. Non si assume indipendenza dei gap dell'orbita.

H22 ha controllato indipendentemente questa deduzione. Non usa atom-floor, g, Q, una stima di mixing o la regolarità di una misura inversa. Non fornisce il lower entropico opposto.

Di conseguenza, per escludere una D basterebbe provare che almeno UNO dei suoi limiti empirici abbia entropia normalizzata superiore a θ. Come proprietà di una misura, è meno esigente dell'assoluta continuità: una miscela `λ·Haar+(1−λ)δ_x` con θ<λ<1 soddisfa il criterio ed è ancora singolare in parte. Non segue piena singolarità dal nostro upper; il lower di massa singolare del Corollary4 è più forte del semplice `1−θ` che si può ricavare da queste entropie.

Questo NON dimostra che il nuovo criterio sia più facile da ottenere. Un lower simile dovrebbe usare la nonperiodicità e una vera proprietà aritmetica del seed dato; un richiamo generico all'equidistribuzione riscrive soltanto il problema. Il bound ASINTOTICO normalizzato vale banalmente anche ai cicli, che hanno entropia normalizzata zero; non si sta applicando loro la stessa stima finita a ogni m, perché il loro costo medio può superare ell. Non viene autorizzato alcun lower per tutte le orbite positive.

Infine, i nostri input puntuali non producono quel lower. Se si usa la traccia canonica g con la sua legge Q, sulla possibile D `R_j=g(n_j)/Ω_j` è crescente e bounded. La massa Q del vero passato fino al seed fisso b è `Ω_jg(b)/g(n_j)=g(b)/R_j`, quindi rimane separata da zero mentre il root e la profondità crescono. Questo è compatibile con la nonatomia a root fisso e mostra la concentrazione persistente che il programma deve ancora rompere. I valori puntuali di g non identificano la densità rispetto a Haar del limite empirico ν.

## 8. La pista da mettere prima degli altri upper

Durante il controllo delle nuove fonti H21 ha costruito un piccolo menu effettivo di paired words. Le identità sono semplici e non vengono presentate come una nuova tecnica nella letteratura:

`W₁=12 → V₁=21`, `W₂=212 → V₂=113`.

Entrambe conservano lunghezza e totale, e soddisfano `T_V(x−2)=T_W(x)−2` sui rispettivi cilindri legali. I loro offset sono rispettivamente `(5,7)` su denominatore8 e `(29,19)` su denominatore32. Le guardie sono `11 mod16→9 mod16` e `57 mod64→55 mod64`. Ho ricontrollato identità, guardie e composizione. Il menu coniuga blocchi DIVERSI, senza richiedere che un compagno commuti con tutti i blocchi osservati.

Questo produce un'obbligazione precisa senza floor analitico. Se esiste D, scegliere il suo minimo seed b fra le unità positive dispari. Esso ha primo gap1: un gap≥2 darebbe `S(b)<b`, ancora unità e divergente. Se il suo itinerario restasse per sempre in `L={12,212}^ω`, inizierebbe quindi con12. Il compagno c=b−2 seguirebbe i blocchi concorrenti e avrebbe `S^(t_r)(c)=S^(t_r)(b)−2` a ogni confine t_r. Sarebbe perciò nonperiodico e divergente anch'esso.

Se b≡1 modulo3, c è unità positiva più piccola di b, contro la minimalità. Se b≡2 modulo3, c è una foglia, ma il suo primo gap è2; `S(c)=(3b−5)/4` è unità positiva, minore di b e ancora divergente. Anche questo contraddice la minimalità. Dunque il minimo UNIT-D deve uscire da L in tempo finito. Non si suppone che gli interi più piccoli raggiungano1: eventuali cicli ignoti restano ammessi e non modificano l'argomento di nondivergenza.

La fusione terminale con w₂₂ della fonte152 dà già una classe propria di uscite favorevoli, come dettagliato da [H21](H21_EDITOR_IT.md). Il menu generale non è tutto espansivo, perché212 ha gain27/32; la sottoclasse di H21 con macroblocchi `(12)^4` e `(12)^3(212)` ripristina tutti i gain di prefisso>1. Ho verificato anche questa guardia e la riparazione del seed unità. Non si deve dedurre assenza di ripetizioni dal solo fatto che gli stati restino sopra b.

Il passo successivo è classificare le prime uscite reali da L e provare che producano una fusione oppure una nuova relazione fra compagni con costo controllato. I punti d'uscita hanno una descrizione finita, ma gli esponenti e il carry risultante rimangono illimitati. Non è una copertura già ottenuta. Le formule delle prime uscite ricavate da H21 passano il controllo algebrico; una di esse porta alla parte dispari di `x−1`, altre a `2^r x−5` o `2^(r−3)x−1`. Questi stati non costituiscono ancora una famiglia chiusa con un bound utile.

Il controllo negativo di H21 mostra che un buffer espansivo con gap osservati≤3 può comunque produrre un carry arbitrariamente grande all'uscita13. Va inteso come limite a un bound LOCALE, non a ogni possibile controller: se lo stato primario è `z=2^t u+1`, i successivi `r=floor((t−1)/2)` gap sono esattamente2 e danno `S^r(z)=3^r2^(t−2r)u+1`. Un t grande rispetto alla crescita accumulata può quindi pagare una discesa successiva sotto il seed iniziale. Il target corretto può essere una dicotomia fra carry controllato rispetto al growth e discesa, non una promessa di carry assolutamente bounded. Non è stata ottenuta tale copertura generale o un costo O(log j).

Darei priorità a un tentativo circoscritto su queste uscite: c'è un partner legale del seed dato e una classe propria su cui ragionare, senza nuovi input analitici. Il criterio Γ resta utile quando il partner non è più piccolo e si vuole pagare una massa cumulativa. Se l'estensione del menu produce soltanto un carry incontrollato, aggiungere altre identità per enumerazione non basta a motivare altre ore sulla stessa pista.
