# Analisi 9 Cicli e vincoli diofantei

13 novembre 2026. Revisione in sola lettura del progetto al commit `5428e89`. Nessuna build, modifica del repository o scansione estesa. Fonti primarie consultate direttamente: Hercher articolo e corrigendum, Fernández–Ibáñez v1, anteprima editoriale di Knight e repository della formalizzazione Knight2026.

## Confine dei risultati locali

`lean/CollatzShadowing/CycleConstraints.lean:30` prova l'equazione `(2^A−3^L)n=C_w` per una parola esatta chiusa. `:54` prova la contrattività `3^L<2^A`; `:92` il sieve di divisibilità; `:139` il vincolo affine per ogni prefisso basato a un minimo; `:201` il limite `3n≤j3^j` al primo prefisso contrattivo. Sono condizioni necessarie, non un'esclusione di tutti i cicli.

`NoInfinite.lean:124,145` esclude congruenze a precisione arbitraria verso il punto fisso negativo di una parola espansiva. Un ciclo positivo è invece necessariamente contrattivo; la distinzione è già esplicita nel codice. `FirstBarrier.lean:144` identifica quando un endpoint finito scende sotto la sorgente; al minimo di un ciclo ogni prefisso resta sopra il minimo e soddisfa la disuguaglianza opposta. `Phantom.lean:180` offre già la rotazione ciclica delle parole.

Nessun risultato sui soli cicli elimina una traiettoria iniettiva divergente. Reciprocamente H, anche insieme alla positività dei bacini, escluderebbe le orbite non eventualmente periodiche, lasciando separato il ramo dei cicli.

## Fonti esterne e mappa dei quantificatori

[Hercher, JIS 26, 23.3.5](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html) esclude cicli non banali con al più 91 minimi locali. Il [corrigendum del 14 giugno 2026](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf) ripara un passaggio della prova del Teorema 21. La citazione deve includere entrambi. La lunghezza totale, il numero di membri dispari e il numero di minimi sono quantità diverse.

Il collegamento concreto al linguaggio locale è il seguente. Espandere ogni esponente Syracuse a nella parola shortcut `1 0^(a−1)` produce una parola binaria di lunghezza A con L simboli 1. In un periodo primitivo, il numero dei minimi locali della mappa shortcut è il numero degli esponenti `a_i≥2`, cioè il numero dei passaggi ciclici `0→1`. **Non** è il numero dei minimi della sequenza solo dispari: questi richiederebbero anche un successivo esponente 1. Le ripetizioni della stessa parola moltiplicano i conteggi, perciò il ponte deve dichiarare il periodo primitivo oppure contare esplicitamente con molteplicità.

[Fernández–Ibáñez](https://arxiv.org/html/2607.24844v1) studiano il massimo del minimo ciclico del numeratore affine a lunghezza e numero di simboli dispari fissati. Il preprint dà anche vincoli sul minimo di un ciclo. L'estremalità non implica che ogni candidato sia una parola di Christoffel; occorre evitare quel salto.

L'[anteprima editoriale primaria di Knight](https://www.sciencedirect.com/science/article/pii/S0012365X25004200) descrive l'esclusione dei soli high cycles. La lettura integrale tramite questo URL è bloccata da 403. La classe impone condizioni di coprimalità e positività e non comprende tutti i cicli. Il [repository Knight2026_lean](https://github.com/tcosmo/Knight2026_lean/blob/main/SUMMARY.md) espone `no_integer_high_cycles` con le ipotesi `1<x<k`, `gcd(k,x)=1`, `3^x<2^k` e integrità del valore associato alla parola high e al suo reverse. Non è stato compilato qui. Inoltre un periodo primitivo non implica automaticamente `gcd(A,L)=1`: tale restrizione non può essere aggiunta al problema globale senza prova. Il SUMMARY contiene metadati bibliografici discordanti dall'editore; usare l'editore per il riferimento 114812.

## Due deduzioni aritmetiche utili

Per `w=(a,rest)`, `rot=rest++[a]` e `D=2^A−3^L>0`, dalle definizioni delle costanti segue

`2^a C_rot = 3 C_w + D`.

Poiché D è coprimo con 6, per ogni divisore d di D si ha `d|C_w ↔ d|C_rot`. Quindi ripetere il sieve di divisibilità su tutte le rotazioni non aggiunge vincoli indipendenti. La rotazione serve invece a scegliere il minimo e rimuovere duplicazioni nella ricerca. È una deduzione su carta, non una nuova dichiarazione Lean.

Inoltre, per i membri dispari positivi `n_i` di un ciclo,

`2^A = ∏_(i<L) (3 + 1/n_i)`.

Se ogni `n_i≥M>0`, segue il vincolo intero esatto

`2^A M^L ≤ (3M+1)^L`.

Per un ciclo non costante la disuguaglianza è stretta se M è il minimo. In forma logaritmica, per il minimo m,

`0 < A/L−log₂3 ≤ log₂(1+1/(3m)) < 1/(3m log 2)`.

Questi sono vincoli classici e non una rivendicazione di novità. La forma intera evita approssimazioni numeriche e può essere formalizzata prima di aggiungere analisi trascendente. Qualsiasi soglia M tratta da una verifica esaustiva esterna deve restare un'ipotesi esplicita finché non è certificata nell'ambiente Lean; il limite pubblico Barina non è automaticamente un teorema importato.

## Tre programmi con primo lemma e arresto

1. **Interfaccia cicli normalizzati e minimi locali.** Primo lemma: una parola esatta primitiva chiusa si espande nella parola shortcut di lunghezza A, con L termini dispari e `#{i:a_i≥2}` minimi locali. Aggiungere la rotazione al minimo e l'identità delle costanti sopra. Primo test: ricostruire la parola di `[2]` e sue ripetizioni, distinguendo periodo e molteplicità; usare parole positive razionali per testare conteggi non banali. Arresto se una definizione confonde i minimi shortcut con quelli odd→odd o deduce coprimalità dalla sola primitività. Questo è il ponte necessario prima di invocare il limite di Hercher.

2. **Sieve esatto del gap e certificati di approssimanti.** Formalizzare il prodotto e il vincolo intero per un minimo M; derivare intervalli razionali certificati contenenti `log₂3` e una disuguaglianza per le coppie `(A,L)` ammissibili. Primo test su lunghezze piccole e soglia M dichiarata: ogni eliminazione deve avere una disuguaglianza di interi verificabile, senza floating point. Il controllo tramite frazioni continue deve comprendere tutte le frazioni nell'intervallo, non soltanto i convergenti senza un'ipotesi che giustifichi quella riduzione. Arresto se si ottengono soltanto lower bound crescenti di L senza una nuova upper bound o un'esclusione di una classe non già trattata. È utile come libreria di certificati e collegamento bibliografico, non come soluzione universale.

3. **Classi estremali e stabilità rispetto a Christoffel.** Prima tradurre la costante affine locale in quella della parola binaria e verificare ipotesi primitive, rotazioni, integrità e reverse dell'interfaccia Knight. Un lemma successivo realmente nuovo per questo programma dovrebbe dire che un valore di `min_rot C_w` vicino al massimo costringe la parola in una famiglia strutturalmente controllata; poi escludere aritmeticamente quella famiglia. Primo test: enumerazione indipendente di tutte le parole binarie fino a lunghezza 12, fissando il numero di 1, per controllare orientamento delle rotazioni, soglie ed eventuali casi degeneri. Arresto se si usa l'integrità del solo massimizzatore per escludere anche i non estremali, oppure si ridimostra una minorazione già ottenuta dal prodotto senza guadagno strutturale. Il ruolo del ramo è coprire classi specifiche di cicli; l'esaustività infinita rimane da dimostrare.

## Controllo finito eseguito

Esaminate esattamente **5.460 parole** con lunghezza 1–6 ed esponenti 1–4. Identità di rotazione e invarianti di divisibilità superati. Le sei parole chiuse intere nel dominio sono le ripetizioni di `[2]`; una sola è primitiva. Per esse sono stati controllati matching di ogni valutazione, chiusura e vincolo sul minimo. È un test dell'algebra e dell'implementazione sul dominio dichiarato, non un nuovo limite generale sui cicli. Nessuna nuova dichiarazione Lean.
