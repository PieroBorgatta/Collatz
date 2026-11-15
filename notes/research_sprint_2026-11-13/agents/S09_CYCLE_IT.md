# S09 Rotazioni e vincoli dei cicli

13 novembre 2026. Integrato il nuovo modulo `lean/CollatzShadowing/CycleRotation.lean`, con sei teoremi pubblici e una definizione. Il nucleo ha superato un'elaborazione dedicata con exit 0 senza messaggi. La ricevuta è `verification/s09_cycle_receipt.json`; il coordinatore riesegue la verifica integrata finale.

## Risultato formale

Per una parola `w=a::rest`, la rotazione è `rest++[a]`. Il denominatore firmato è `D=2^sum(w)−3^length(w)`. Si prova l'identità esatta

`2^a C(rot)=3 C(w)+D`.

Non richiede positività del denominatore, esattezza della parola o esistenza di un ciclo. Un divisore d di D divide C(w) se e solo se divide C(rot), sotto le due ipotesi esplicite `IsCoprime d 2` e `IsCoprime d 3`. Le ipotesi rendono visibili le cancellazioni: il modulo non le sostituisce con un'assunzione nascosta di esistenza di un ciclo. Si registra anche l'equazione ciclica locale e la conseguenza per il sieve ruotato.

L'uso operativo è evitare lavoro ridondante: il test di divisibilità per uno stesso divisore del denominatore non diventa più forte ripetendolo sulle rotazioni. Le rotazioni servono ancora a scegliere un minimo e a identificare rappresentazioni equivalenti. Il modulo non esclude tutti i cicli.

## Verifica finita indipendente

Il replay `experiments/s09_cycle_checks.py` usa la formula espansa della costante, invece della ricorrenza di testa usata in Lean. Controlla 5.460 parole, con lunghezza 1–6 ed esponenti 1–4: identità di rotazione, coprimalità del denominatore con 6 e invarianza del gcd. Le sole parole chiuse positive intere in questo dominio sono sei ripetizioni di `[2]`, tutte sulla sorgente 1; il programma controlla ogni valutazione e la chiusura. Output normale e con `-O` identici byte per byte. Non è un nuovo limite generale sui cicli.

## Confronto con gli altri agenti

S07 ha fornito un autoarco del proprio quoziente di clock, con r=9 e cofattore crescente. Non è un ciclo reale: ogni reiterazione esige nuove congruenze. L'identità di rotazione non fornisce tali congruenze e non autorizza a iterare un arco del quoziente. S11 ha confermato la stessa distinzione nel proprio controllo del campionamento e dei reset.

A S10 è stata trasmessa una verifica del controllo dei tempi per la nuova pista di sparsezza: su un segmento iniettivo `x_0,…,x_L`, la mappa `T^N` è iniettiva sugli indici `j≤L−N`. Il passaggio è corretto; rimane da verificare che il lemma di conteggio esterno richieda soltanto questa iniettività e non ipotesi ulteriori su traslazioni o tempi differenti. Questo scambio non è una verifica del teorema di sparsezza completo.

## Prodotto e priorità editoriale

Il vincolo classico del minimo ciclico `2^A M^L≤(3M+1)^L` ammette una prova puramente intera: per un segmento esatto sopra M si moltiplicano le disuguaglianze `2^a M S(n)≤(3M+1)n`, ottenendo `2^A M^L eval(w,n)≤(3M+1)^L n`; la chiusura permette di cancellare n>0. Un candidato di formalizzazione è conservato fuori dalla libreria in `research/research_sprint_2026-11-13/s09_product_candidate.lean.txt`, senza essere contato come verificato. L'elaborazione opzionale è stata annullata per liberare lo slot alla revisione della nuova pista di sparsezza.

Per una v7, il contributo è un'interfaccia aritmetica verificata e la rimozione di un sieve ridondante, non la scoperta di un nuovo vincolo diofanteo. Il collegamento a Hercher deve includere il corrigendum e distinguere i minimi della shortcut dai minimi della sequenza solo dispari. Nessuna verifica esterna esaustiva viene importata come teorema Lean.
