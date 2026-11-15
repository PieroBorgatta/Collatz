# S01 Meccanismi web da integrare nel progetto

13 novembre 2026. Lettura mirata di fonti primarie e di sorgenti, senza compilare progetti esterni o eseguire codice scaricato. Tre meccanismi finiti sono adatti a un'integrazione locale indipendente: pool senza connessioni orbitali, allocazione a soglia e controllo di miscele con massa totale limitata. Nessuno fornisce il confronto relativo H o un nuovo input analitico.

## Provenienza e confine della verifica

Il repository [Shaik](https://github.com/shaikidris/CollatzConvergencePositiveDensity) è stato interrogato tramite API e sorgenti raw al commit **`f0fda887ee60dc8ac4ef0d864935148b03734726`**. Il timestamp del commit restituito dall'API è 22 settembre 2026; va distinto dalla segnalazione pubblica di ottobre e dalle date del manoscritto. Il progetto esterno è fissato a Lean/Mathlib **4.33.0**, mentre il progetto locale principale usa 4.29.1: copiare moduli con sintassi `module`/`public import` non è un'integrazione verificata.

Il codice è Apache-2.0; la licenza del manoscritto è separata. Una piccola selezione di moduli utili, la licenza e gli avvisi Mazur sono conservati in `research/research_sprint_2026-11-13/s01_sources/`, con URL immutabili, hash e dimensioni nel manifest. Non sono stati copiati manoscritti o librerie complete. La selezione serve alla lettura e all'attribuzione; non è una nuova dipendenza o un progetto eseguibile completo.

La pagina [ProofAtlas sui predecessori](https://www.proofatlas.ai/formalizations/positive-lower-density-collatz-predecessors/) documenta un controllo della chiusura locale più esteso rispetto alla fotografia di settembre. I coefficienti restano dipendenti dal target; non vi è un rapporto uniforme fra bacini, né un replay con kernel indipendente. Questo aggiornamento sostiene un successivo audit della catena esterna, non permette di assumerla nella libreria principale senza un collegamento esplicito.

## Lemma 1 Pool non ricorrenti e carico reciproco

Fonte precisa: `WordCertDensity/Roots/Antichain.lean:27,52,108` e `Roots/PoolCharge.lean:59,88,96`, al commit sopra. Il requisito è più forte del nonritorno separato di ogni radice: un pool P non contiene alcun positivo iterato di un suo membro, compreso il membro stesso.

Nel linguaggio locale, siano x>0 e W un insieme finito di parole distinte esatte da x, tutte con endpoint R_w appartenente a un tale pool per S. Allora

`Σ_(w∈W) ω(w)/R_w ≤ 1/x`.

La ragione è semplice e non richiede probabilità: due visite dalla stessa sorgente al pool devono avere lo stesso tempo; due parole esatte della stessa lunghezza coincidono. Nel catalogo può quindi comparire al più una parola realizzata. Il suo peso reciproco è il potenziale orbitale, già limitato da `1/x` mediante la dissipazione locale.

Per etichette duplicate basta aggregare il coefficiente totale di ogni parola e imporlo al più M; il limite diventa `M/x`. L'alternativa dissipativa `Σω/[R(3R+1)]≤1/x` resta necessaria per pool annidati o con ritorni. Gli endpoint dei blocchi crescenti `[1,2]` non sono un pool non ricorrente: non usare il limite più forte per essi.

**Confronto fra agenti:** ho inviato definizione, riferimenti e requisito sulle etichette a S02. Ho letto la sua implementazione indipendente `RootPoolBudget.lean`: la definizione, l'unicità dei tempi e la prova di unicità della parola corrispondono al meccanismo. Non ho trovato un'ipotesi mancante. La verifica di compilazione rimane registrata da S02 e dall'integrazione principale.

## Lemma 2 Allocazione finita a soglia

Fonti precise: `WordCertDensity/Counting/ProfileThreshold.lean:16,29,43`, `Counting/ProfileDuality.lean:12,35`; per il distinto problema di costo reciproco delle radici, `Roots/Allocation.lean:57,80,97`.

Il primo ponte utile può essere dimostrato direttamente nel nostro modello, senza importare gli ottimizzatori esterni. Per un insieme finito di celle r, assumere

`0≤c_r≤C`, `h_r≥0`, `p≤Σ c_r h_r`, `t>0`.

Allora

`max(p−C Σ max(h_r−t,0),0)/t ≤ Σ c_r`.

La prova locale usa solo `c_r h_r≤t c_r+C max(h_r−t,0)` e somma sulle celle. Un'allocazione che riempia al cap le celle con h maggiore della soglia, svuoti quelle sotto la soglia e usi eventualmente una cella parziale può saturare il limite. Si tratta di una certificazione finita di costo, non di un teorema statistico.

Per usarla nei conteggi occorrono le stesse celle fisiche: un cap C dimostrato per il loro carico, il loro valore effettivo h e una minorazione p della massa selezionata. Una distribuzione di riferimento con gli stessi valori marginali non sostituisce questi dati. Il risultato può migliorare una conversione che usa soltanto il massimo uniforme K; non crea la minorazione analitica p.

**Decisione:** ho proposto al coordinatore una formalizzazione breve di questo ponte, prima dell'eventuale algoritmo greedy. La formula di costo fra due target, da sola, non confronta le densità effettive dei rispettivi bacini.

## Lemma 3 Miscele finite senza indipendenza artificiale

La lettura del [paper rStation 10 v3](https://rstation.ai/problems/collatz/papers/10), Lemma 4.4, suggerisce di conservare insieme il residuo ternario e il totale degli esponenti. Il suo teorema globale dipende da una stima esterna di mixing congiunto che non è stata riprodotta qui.

Un'integrazione elementare distinta è possibile. Per vettori finiti v_σ e coefficienti nonnegativi p_(τ,σ), supporre `Σ_(τ∈W) p_(τ,σ)≤b` per ogni σ. Per qualunque seminorma N, omogenea e subadditiva,

`Σ_(τ∈W) N(Σ_σ p_(τ,σ) v_σ) ≤ b Σ_σ N(v_σ)`.

La prova è disuguaglianza triangolare, omogeneità, scambio di due somme finite e limite sulle masse di colonna. Applicando N alla differenza fra una distribuzione e la sua media sui cilindri, si ottiene un controllo dell'oscillazione delle miscele. Il requisito essenziale è che i coefficienti della miscela non dipendano anche dalla cella del vettore; altrimenti il passaggio non è giustificato.

Questo lemma è riutilizzabile senza probabilità o mixing asintotico. Per applicarlo alle vere parole serve poi un'identità di convoluzione della legge congiunta, provata sul modello effettivo. Non si può sostituire quest'ultima con due leggi marginali o con l'ipotesi che i residui osservati lungo una singola orbita siano indipendenti.

## Dizionario esatto e una correzione di dominio della fonte

Nel Lemma 3.1 di rStation il target a è stampato come intero positivo arbitrario. La formulazione con `Syr^k(x)=a` richiede però a dispari. Controesempio: a=2, k=1, totale A=1. Il residuo `2^(-1) mod3` è 2, quindi il conteggio di parole predice una sorgente; la sorgente inversa è x=1, ma `S(1)=1`, non 2. La prova della fonte riconosce che, per un target pari, si ottiene invece un segmento shortcut. Non è un'obiezione al successivo uso su target dispari.

La versione da integrare è quindi un dizionario finito **per target dispari positivi**. Per lunghezza k e somma A, le composizioni positive w che soddisfano

`2^A a ≡ C(w) (mod 3^k)`

devono essere identificate con le sorgenti intere positive dispari delle parole esatte che terminano in a. L'orientamento della legge X della fonte è l'inverso dell'ordine forward locale: il suo atomo usa `reverse(w)`. Positività, integrità intermedia e valutazioni esatte vanno provate, non soltanto l'identità affine finale.

Il controllo indipendente [s01_joint_count.py](../experiments/s01_joint_count.py) ha confrontato conteggio dei residui e iterazione effettiva su **480 casi**: k=1,…,4, A=k,…,k+5 e target dispari 1,…,39. Tutti coincidono. Il codice registra anche il controesempio pari. È una verifica finita; non è il dizionario generale formalizzato.

## Prosecuzione e criterio di arresto

La prima integrazione utile è il carico dei pool in S02, seguita dal ponte a soglia e da un dizionario finito delle parole. Sono componenti verificabili senza acquisire un risultato analitico esterno. Dopo questi passaggi, il tentativo di flusso relativo deve ancora dimostrare una quota di massa effettiva con altezza e molteplicità controllate.

Interrompere la pista se il nuovo punteggio è soltanto una minorazione assoluta non confrontabile con il bacino di base, se le etichette moltiplicano il carico o se il mixing congiunto è assunto al posto di essere provato. La nuova architettura è uno strumento per esporre il lemma mancante, non una ragione per dichiarare prossima una prova di Collatz.
