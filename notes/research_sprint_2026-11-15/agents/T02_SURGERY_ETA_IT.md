# T02 La surgery di due esponenti a shift fissato è subpolinomiale

15 novembre 2026. Ricerca autonoma con controllo incrociato richiesto a T01 e al coordinatore. **Stato: prova matematica su carta; la verifica indipendente e la build dei lemmi finiti sono in corso.** Il risultato asintotico non è ancora una dichiarazione Lean.

## Risultato e dominio

Fissiamo target positivi dispari distinti n,y e un intero non nullo δ. Una surgery modifica un esponente interno a_i in a_i+δ e l'ultimo a_k in a_k−δ, lasciando positivi tutti gli esponenti. La lunghezza k e il totale A sono conservati. Si richiede che entrambe le parole siano **effettive**: la prima da u>0 dispari a n, la seconda da v>0 dispari a y.

Sia E_δ(X) l'insieme dei codici fisici `(u,w,i,v)` di queste trasformazioni con u≤X. Sono ammesse anche parole che non siano di primo arrivo. Una copia dovuta a metadati non è un nuovo codice fisico. Non imponiamo alcun cutoff su v.

**Teorema su carta.** Per ogni ε>0 esiste C_(ε,n,y,δ) tale che, per tutti gli X≥2,

`|E_δ(X)| ≤ C_(ε,n,y,δ) X^ε`.

In particolare sono X^o(1) sia le sorgenti coperte sia le immagini dispari distinte. La conclusione è più forte di o(X) entro una dilatazione fissata. Non usa la nuova sparsezza dei segmenti finiti, il limite B o il corollario d'altezza D₀. Usa invece una disuguaglianza classica sulle S-unità come teorema esterno dichiarato.

Questo non confuta H e non chiude i trasporti fra parole intere o a profondità variabile. Chiude il tentativo di produrre una quota positiva con un insieme finito di shift di questa specifica surgery.

## 1 Località terminale

Manteniamo la notazione S06: `q=k−i≥1`, P è il totale degli esponenti fino alla posizione i e B è il totale dopo i, dunque A=P+B. Sia T la costante affine della coda `(a_(i+1),…,a_k)`, lunga q.

Se δ=d>0, una condizione necessaria è

`3^q | y−2^d n`.

Se δ=−d<0, la condizione è

`3^q | 2^d y−n`.

I due interi sono dispari, dunque non nulli. Per δ fissato il valore q appartiene quindi all'insieme finito `1≤q≤Q_δ`, con

`Q_(+d)=ν₃(y−2^d n)`, `Q_(−d)=ν₃(2^d y−n)`.

Se Q_δ=0 non vi sono trasformazioni. Non si deduce un limite assoluto su k: il prefisso prima della surgery potrebbe ancora crescere.

## 2 Il residuo completo vede tutta la profondità

La costante affine non dipende dall'ultimo esponente. Per δ=d>0, la variazione della costante è `(2^d−1)2^P T`. Sottraendo le due identità affini:

`3^k(v−u)=2^P R_+`,

`R_+=2^B(y−n)−(2^d−1)T`.

Poiché 2 e 3 sono coprimi, **`3^k | R_+`**. Il residuo dipende soltanto dalla coda di lunghezza q, oltre ai parametri fissati: il prefisso non compare.

Per δ=−d<0, con P ancora il totale originale fino all'edit, la positività impone P≥d e dà

`3^k(v−u)=2^(P−d) R_-`,

`R_-=2^(B+d)(y−n)+(2^d−1)T`.

Anche qui **`3^k | R_-`**. Nel modulo Lean la stessa formula negativa usa P per il totale **nuovo** fino all'edit; la formula risulta senza sottrazione naturale.

T è dispari: nel suo sviluppo la prima potenza di 3 è dispari e tutti gli altri termini contengono una potenza positiva di 2. B≥q≥1 e d≥1. Pertanto entrambi i residui sono dispari e non nulli. Non occorre assumere a questo punto che i due bacini siano disgiunti.

Questo è un vincolo diverso da quello S06 sulla sola distanza q: l'intera potenza `3^k` divide una somma con un numero **limitato** di potenze di 2.

## 3 La disuguaglianza esterna usata esattamente

Fonte primaria: J.-H. Evertse, *On sums of S-units and linear recurrences*, Compositio Mathematica 53 (1984), 225–244, **Corollario 2, p.228, subito dopo il Teorema 2**. [Articolo e metadati](https://www.numdam.org/item/CM_1984__53_2_225_0/), [PDF](https://www.numdam.org/item/CM_1984__53_2_225_0.pdf).

Per K=Q, un insieme finito S di posti contenente quello infinito, T={3} e coordinate intere non nulle x_j con somma R≠0, quel corollario fornisce una minorazione di |R|₃ in termini del prodotto dei valori assoluti delle coordinate su S, del minimo dei loro valori assoluti in 3 e di una potenza arbitrariamente piccola della loro altezza. Quando tutte le coordinate sono S-unità, il prodotto vale uno. Il corollario richiede soltanto R≠0; non richiede l'assenza di sottosomme nulle.

Applichiamolo alle coordinate dello sviluppo

`T=Σ_(j=0)^(q−1) 3^(q−1−j) 2^σ_j`,

con `σ_0=0<σ_1<…<σ_(q−1)<B`.

In R_+ si aggiunge la coordinata `2^B(y−n)`; in R_- si aggiunge `2^(B+d)(y−n)`. Gli altri coefficienti sono rispettivamente `−(2^d−1)3^(q−1−j)` e `+(2^d−1)3^(q−1−j)`.

Per q,d,n,y fissati, scegliamo S contenente infinito, 2, 3 e tutti i primi dei coefficienti non nulli. Ogni coordinata è allora una S-unità. Il minimo dei valori assoluti in 3 è una costante positiva indipendente dagli esponenti σ_j e B; l'altezza è al più C₀ 2^(B+d). Dunque, per ogni τ>0,

`ν₃(R_±) ≤ τ B+C_(τ,q,n,y,d)`.

Le normalizzazioni dei logaritmi sono assorbite nella scelta libera del parametro di Evertse. Il termine τd è assorbito nella costante. Poiché q appartiene a un insieme finito, possiamo massimizzare le costanti su `1≤q≤Q_δ`. Otteniamo, uniformemente su tutti i trasporti con quello shift,

**`k ≤ τ A+C_τ`** per ogni τ>0.

Il teorema esterno è ineffettivo: qui non si ottiene una soglia numerica concreta oltre la quale k sia piccolo. Questo impedisce di promuovere l'osservazione precedente k≤7 a un limite generale.

## 4 Un budget elementare elimina il vincolo d'altezza

Siano x_0=u,…,x_k=n gli stati positivi della parola originale. Da

`2^(a_j) x_j = 3x_(j−1)+1 ≤4x_(j−1)`

segue, moltiplicando e cancellando gli stati intermedi,

**`2^A n ≤4^k u`**.

Per u≤X e n≥1:

`A≤2k+log₂X`.

Insieme alla stima precedente:

`k≤τ(2k+log₂X)+C_τ`.

Per 0<τ<1/2 si riordina:

`k≤[τ/(1−2τ)]log₂X+C_τ/(1−2τ)`.

La frazione tende a zero per τ→0. Pertanto **k=o(log X)** uniformemente sui codici di E_δ(X). Il medesimo budget dà **A≤log₂X+o(log X)**. Non è stato usato alcun vincolo su v, alcuna iniettività del segmento o ipotesi di nonritorno.

## 5 Conteggio dei codici

Una parola positiva di lunghezza k, totale al più L, ha esattamente `binom(L,k)` possibilità: si sommano le composizioni di tutti i totali fra k e L. Nel nostro dominio L=O(log X) e k=o(log X). La stima entropica delle somme binomiali dà

`Σ_(k≤o(log X)) binom(O(log X),k)=exp(o(log X))=X^o(1)`.

Per rendere il quantificatore esplicito: si fissa una piccola ρ>0; il §4 dà k≤ρlog₂X+O_ρ(1) e A≤(1+2ρ)log₂X+O_ρ(1). Il tasso entropico tende a zero quando ρ→0. Per ogni ε>0 si sceglie prima ρ e si assorbe il prefattore e l'intervallo iniziale nella costante C_ε.

Una parola e il target n determinano al più una sorgente u mediante l'identità affine. Per ogni parola, q ha al più Q_δ valori e fissa la posizione i=k−q. Quella posizione e δ fissano la parola modificata e al più una immagine v. Quindi anche i codici fisici sono X^o(1). Non si è supposta l'iniettività del trasporto e le collisioni possono soltanto diminuire il numero delle immagini distinte.

Consentire sorgenti ordinarie `2^e u≤X` aggiunge al più un fattore O(log X). Consentire qualsiasi lift d'uscita `2^f v≤DX`, con D fissato, aggiunge un altro O(log X). La conclusione X^o(1) rimane valida per entrambi questi conteggi finiti. La conclusione su tutte le immagini dispari senza cutoff non autorizza a contare infiniti lift d'uscita senza cutoff.

## 6 Chiusura della relazione pesata su tutti gli shift

Qui fissiamo la parola di **primo arrivo** di ogni sorgente: essa è unica anche se il target ha ritorni. Usiamo i pesi θ_δ=2^(−|δ|), con identificazione delle copie fisiche. Per ogni sorgente e shift δ vi sono al più Q_δ edit effettivi.

Posto N=max(n,y), l'argomento elementare precedente S06 dà

`Q_δ≤log₃N+|δ|log₃2`.

La massa totale uscente dai soli shift |δ|>R è quindi, **per ogni sorgente**, al più

`g_R=2^(1−R)[log₃N+(R+2)log₃2]`,

e g_R→0. Per |δ|≤R, il teorema appena dimostrato implica che la massa totale uscente da sorgenti ≤X sia X^o(1). La coda è al più Xg_R. Facendo prima X→∞ e poi R→∞:

**massa pesata totale uscente = o(X)**.

Lo stesso vale per sorgenti ordinarie con lift preservato `2^e u→2^e v`: ogni input ordinario conserva lo stesso limite g_R. Non si attribuisce un nuovo peso pieno a ogni possibile lift d'uscita indipendente.

Di conseguenza, se il bacino di base ha densità inferiore positiva, la relazione pesata proposta S06 non può fornire una quota relativa η>0, neppure prima di imporre l'altezza o pagare il carico incoming. Il limite del carico rimane corretto, ma non può trasformare o(X) massa uscente in una quantità lineare.

**Confine:** non abbiamo dimostrato o(X) per l'unione *non pesata* di tutti gli shift crescenti con X. L'ordine dei limiti e la sommabilità dei pesi sono essenziali per questa conclusione.

## Verifiche e integrazione finite

Il protocollo di controllo è stato congelato alle **19:56:38 UTC** prima dell'esecuzione: lunghezze 2…5, totale A≤12, target `{5,7,31,593}` e fratelli canonici, tutti gli shift non nulli che mantengono gli esponenti positivi. Non è una nuova scansione di cutoff asintotici.

Il controllo esaustivo ha verificato **1.573 parole**, **58.256 modifiche** e **81 trasporti esatti** (54 positivi, 27 negativi), ricostruendo le sorgenti mediante la somma affine e facendo un replay diretto indipendente di tutte le valutazioni. Identità firmate, residuo dispari, divisibilità per 3^k, località terminale e budget 2^A n≤4^k u sono passati. Gli output normale e Python -O sono identici, SHA-256 `494198cabf1e8632c064b0549c9985803eb70601fb07d52342517ae492ceb43d`.

Codice e dati: [controllo](../../../research/research_sprint_2026-11-15/t02/check_two_edit_residuals.py), [protocollo](../../../research/research_sprint_2026-11-15/t02/protocol.json), [risultati](../../../research/research_sprint_2026-11-15/t02/residual_check.json).

Il nuovo modulo [TwoEditSparsity.lean](../../../lean/CollatzShadowing/TwoEditSparsity.lean) contiene soltanto la parte finita dichiarata: identità e divisibilità del residuo per entrambi i segni, più il budget elementare per parole esatte. Non assume Evertse come nuovo assioma, non dimostra in Lean il limite asintotico e non modifica dipendenze o versioni del toolchain.

Il PDF primario è stato letto nella pagina stampata 228 tramite rendering locale. Provenienza: `https://www.numdam.org/item/CM_1984__53_2_225_0.pdf`, SHA-256 `5b02e0e31c546f7f8c6c34071b2caa4d7137be24f16d11d483cdcc65377b2f6d`; nessuna copia del PDF è stata aggiunta al repository.

## Decisione

Il nuovo passo giustificato è abbandonare la surgery di due esponenti con shift limitati e anche la sua versione pesata sommabile come candidata a η. I tentativi successivi devono cambiare un numero crescente di esponenti, l'intera parola, il profilo o la profondità, oppure comparare direttamente cataloghi fisici aggregati. Questa esclusione restringe la ricerca; non costituisce una prova di H o di Collatz.
