# Analisi 8 Trasporto di parole e profondità variabile

13 novembre 2026. Revisione in sola lettura del commit 5428e89; nessuna modifica al repository o nuova build. Ho verificato la prova H.2 e derivato condizioni aggiuntive per una trasformazione di più esponenti. Nessuna costruzione di massa relativa è stata ottenuta.

## Audit della prova H.2

La conclusione di `notes/post_v6_signed_mass_2026-09-26/PROOF_IT.md:34` è correttamente quantificata: n e y sono dispari positivi distinti e fissati, D>0 è fissato, si contano tutte le immagini distinte entro DX da sorgenti dispari entro X e parole di primo arrivo. Le correzioni dell'ultimo esponente sono tutte quelle intere ammissibili, e il fattore diadico dell'immagine è libero. Non si assume densità positiva per il risultato o(X).

I passaggi essenziali sono solidi a questa lettura:

- La costante affine C è invariata e positiva: da qui l'espansione per correzioni positive e la compressione per quelle negative (`:46–68`).
- Per ogni bound M, le correzioni |delta|≤M sono escluse alle profondità sufficientemente grandi dalla congruenza modulo 3^k fra interi non nulli (`:70–94`).
- Le profondità limitate contribuiscono soltanto un polinomio in log X, anche contando i sollevamenti diadici (`:98–110`).
- La coda positiva è una doppia serie geometrica sui parametri delta e f: l'unicità della parola di primo arrivo è usata per contare sorgenti per ogni coppia (`:118–135`).
- Per la coda negativa, gli output con f≤F stanno nella dilatazione di un insieme di O(2^-M X) interi; quelli con f>F sono divisibili per 2^(F+1), indipendentemente dalle collisioni (`:137–151`).
- L'ordine dei limiti X→∞, poi M→∞, poi F→∞ è esplicito e valido (`:154–167`).

I sei lemmi di `lean/CollatzShadowing/SignedTransport.lean:15–85` supportano l'aritmetica; non formalizzano l'asintotica intera. La conseguenza per H richiede la positività del bacino, ma il teorema di immagini sparse no.

L'ostruzione a profondità uguale di `local_coupling_IT.md:164–206` non va sovraestesa: esclude dilatazione universale su ogni sorgente, mentre una comparazione di densità può scartare o_n(X) sorgenti. Sul sottodominio certificato senza ritorno, il costo mostrato cresce come una potenza di log n con esponente minore di 1; non esclude una dilatazione O(log n). L'ostruzione agli stati affini finiti (`:208–237`) riguarda quel modello preciso, non ogni algoritmo.

## Un vincolo nuovo per la surgery bilanciata

Sia w=(a_1,...,a_k), A_r=a_1+...+a_r e

C(w)=sum_(r=0)^(k-1) 3^(k-1-r) 2^A_r.

Aumentiamo a_i di delta≥1 e diminuiamo a_j di delta, con i<j e a_j>delta, preservando la somma A_k. Allora

C(w')−C(w)=(2^delta−1) sum_(r=i)^(j-1) 3^(k-1-r) 2^A_r.

Questa identità cambia effettivamente C. Tuttavia, se j<k, ogni termine a destra è divisibile per 3. Per i fratelli canonici del progetto, y=h(n) soddisfa y≡−n mod3 e 3 non divide n. L'integralità della nuova sorgente richiederebbe

C(w')−C(w) ≡ 2^A_k(y−n) mod3,

impossibile perché il membro destro è non nullo. Quindi una modifica bilanciata che lasci invariato l'ultimo esponente non può funzionare neppure al primo livello ternario.

Più in generale, per qualunque parola esatta che termini in n con ultimo esponente a_k, la condizione finale implica 2^a_k n≡1 mod3. Per terminare in h(n), la parità dell'ultimo esponente deve cambiare. Una trasformazione utile deve dunque modificare l'ultimo esponente e anche altri esponenti o la profondità, così da uscire davvero dal dominio H.2.

Stato C/E: identità algebrica su carta, non nuova dichiarazione Lean. Un test esatto su parole di lunghezza 2–5 con esponenti iniziali 1–4 ha controllato 8.988 identità per delta=1: 5.232 modifiche che evitano l'ultimo esponente sono tutte escluse modulo 3; 3.756 che lo toccano superano soltanto il test modulo 3. Questo non certifica la congruenza modulo 3^k, un controllo d'altezza o un confronto di massa. [Dati conservati](verification/transport_probe.json).

## Tre obiettivi concreti e relativi arresti

### 1 Trasformazione bilanciata con modifica terminale

Primo candidato: a_i→a_i+delta, a_k→a_k−delta, con delta dispari, seguita eventualmente da una variazione di profondità. La formula sopra rende esplicita la nuova costante affine e il primo ostacolo ternario. Per una parola di lunghezza k e somma A invariata, definire v=(2^A y−C')/3^k. Il lemma finito da cercare deve provare insieme divisibilità per 3^k, positività e disparità di v, esattezza della parola e v≤D_n u su un insieme di sorgenti quantificato.

Test iniziale: fissare un target n prima del calcolo; enumerare parole effettive provenienti dalle sue sorgenti entro piccoli cutoff, senza variare n con la parola, e cercare gli aggiornamenti ammissibili. Registrare distintamente immagini distinte, sorgenti coperte, carico e massimo costo d'altezza. Fermarsi se il successo è solo modulo 3 o se funziona soltanto su profondità limitate: tali sorgenti hanno densità nulla. Anche una buona frequenza finita non prova la minorazione asintotica.

### 2 Problema di realizzazione a profondità variabile

Per una nuova parola di lunghezza ell, somma B e costante C', la sorgente è v=(2^B y−C')/3^ell. L'intervallo esatto per 0<v≤D_n u è

2^B y−3^ell D_n u ≤ C' < 2^B y.

Non basta scegliere C' in questa finestra: C' e B devono appartenere alla stessa parola positiva, soddisfare la congruenza e produrre l'endpoint dispari y. Il primo risultato utile sarebbe un lemma di realizzazione per una famiglia definita indipendentemente di coppie (B,C'), con ell variabile e costo esplicito. La finestra generalizza la condizione necessaria a profondità fissa di H.2:194–214.

Test iniziale: un enumeratore esatto di parole corte deve confrontare il supporto reale delle coppie (B,C') con la finestra, includendo i buchi ternari. Fermarsi se viene usata una distribuzione uniforme di C' a B fissato senza prova, o se i parametri vengono scelti dopo aver visto una sorgente favorevole. Nessuna densità segue dalla semplice non-vacuità della finestra.

### 3 Lemma di flusso relativo su sorgenti distinte

Siano U_X=B(n)∩[1,X] e V_X=B(h(n))∩[1,D_n X], con le sorgenti ordinarie, inclusi i fattori diadici. Cercare un flusso nonnegativo q_(u,v), sostenuto soltanto su trasformazioni esatte del punto 1 o 2, tale che

sum_(u,v) q_(u,v) ≥ eta_n |U_X| − E_n(X),

sum_u q_(u,v) ≤ M_n per ogni v,

E_n(X)=o_n(X), e D_n M_n/eta_n ≤ C(1+log n), con C universale.

Per doppio conteggio, |V_X|≥(eta_n/M_n)|U_X|−E_n(X)/M_n; dividendo per D_n X e passando al liminf si ottiene esattamente il tipo di H richiesto. D_n e M_n possono anche dipendere dal target: è il loro costo combinato con eta_n che deve restare logaritmico. Questo schema evita di richiedere un'accoppiamento puntuale di ogni sorgente e chiarisce il ruolo delle collisioni.

Il doppio conteggio è elementare; la costruzione del flusso e la sua massa relativa sono il lemma aperto. Primo test avversario: immagini sovrapposte, target 593/9493 del censimento locale, profondità alte e sorgenti che escono dal cutoff prima di tornare. Fermarsi se il flusso è normalizzato assumendo già la massa richiesta, oppure se si confrontano soltanto due lower bound assoluti di densità. Anche questo programma, se riuscisse, tratterebbe le orbite divergenti; i cicli resterebbero separati.

## Decisione

H.2 non lascia un miglioramento residuo del metodo dell'ultimo esponente. La formula della surgery bilanciata e il lemma astratto di flusso sono primi oggetti finiti verificabili; il vero ostacolo rimane una realizzazione quantitativa su una quota relativa di un bacino fissato, con costo totale logaritmico. Non è stata trovata una tale realizzazione e non è giustificato sostituirla con un censimento più grande.
