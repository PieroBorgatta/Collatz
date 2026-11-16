# U05 — Revisione indipendente del no-go a slope terminale limitata

**PASS su carta nei quantificatori dichiarati**, con una sola precisazione documentale. Ho ricostruito la prova U11 dal potenziale reciproco e dal teorema `WeightedVisits.sum_wordWeight_fiber_le`, senza assumere primo arrivo o assenza di cicli.

Snapshot letta: `U11_BOUNDED_SLOPE_IT.md`, SHA-256 `166cf22f250fa548254ee8c07278c3f6b5c3422d0db907a4b261a2c01a777e9d`. Copia immutata e ricevuta sono in `research/research_sprint_2026-11-15_three_hours/u05/review_snapshot/` e `u05/bounded_slope_review_receipt.json`. Una successiva modifica documentale U11 non è silenziosamente inclusa in questo hash.

## Ricostruzione del passaggio centrale

Fissati n>0 dispari e R₀>0 reale, ogni parola effettiva a:z→n con `ρ(a)≤R₀` soddisfa `ω(a)≥1/R₀` e `ω(a)z≤n`. Quindi `1≤z≤R₀n`, un insieme finito, anche quando R₀ non è intero. Se R₀n<1 non ci sono parole.

Per ogni sorgente z e ogni insieme finito W di parole distinte di quel catalogo, il teorema già formalizzato ammette ripetizioni dell'orbita e dà

`|W|/R₀≤Σ_Wω≤n(3n+1)/z`.

Un insieme infinito fornirebbe sottoinsiemi finiti arbitrariamente grandi: il catalogo a z fissata è pertanto finito. L'unione sulle sorgenti limitate è finita. La parola vuota è inclusa precisamente quando R₀≥1; ha z=n, ω=ρ=1. I target periodici sono ammessi: il budget ponderato paga le ripetizioni, che non mantengono un peso minimo indefinitamente.

La finitezza del catalogo originale rende finiti L,B e tutte le nuove code β di identica lunghezza L e somma B. I β non effettivi possono rimanere nel soprainsieme; non aggiungono codici reali.

Per `w=pα:u→n`, `w'=pβ:v→y` con stessi k,A, l'eliminazione del prefisso identico dà

`3^k(v−u)=2^P R`, `R=2^B(y−n)−C(β)+C(α)`.

Per n≠y, un codice effettivo ha R≠0: altrimenti u=v, e la determinazione dell'orbita allo stesso tempo k darebbe n=y. La coprimalità di2 e3 impone `3^k|R`. Poiché i residui non nulli appartengono a un insieme finito, `k≤K=maxν₃|R|`; se nessun residuo non nullo esiste, non ci sono codici.

K è **esistenziale**, non una soglia temporale calcolata. Il bound sulla cardinalità delle code non limita la data della loro ultima comparsa lungo una sorgente: non è lecito ottenere un cutoff esplicito dal primo paragrafo. U11 conserva correttamente questa distinzione.

Infine `2^A n≤4^k u` e u≤X danno A≤2K+log₂X. Il conteggio delle composizioni positive di lunghezza j≤K e totale≤2K+floor(log₂X) è `binom(2K+floor(log₂X),j)`. Sommando in j si ottiene `O((1+logX)^K)`, incluso K=0. Ogni parola e il suo endpoint determinano al più una sorgente; i tagli e le β aggiungono soltanto un fattore fisso. Il count riguarda codici fisici, non copie illimitate di etichette.

## Qualificazione del raccordo con la fonte148

La frase «le parole prefix-expanding partono da u<n» va limitata alle parole **non vuote**. Il loro peso totale è ω>1, quindi ωu≤n implica u<n. La parola vuota ha invece u=n e ρ=1; resta comunque compresa nel caso R₀=1 del nuovo teorema. Questa precisazione non cambia la proposizione o la sua prova.

Non ho ri-auditato l'intero manoscritto148. Per il corollario qui basta la proprietà netta `ρ<1` attribuita alle sue parole non vuote; la prova astratta U11 non dipende da quella fonte.

## Confronto con le esclusioni U05

Il risultato U11 è complementare alle due note U05. Qui la complessità della coda è arbitraria, ma la sua slope resta limitata. Le note U05 ammettono slope che cresce senza limite, ma limitano il numero di non-1 oppure il numero di pezzi di un dizionario periodico fissato. Nel secondo caso occorre il primo arrivo originale per escludere blocchi periodici ripetibili senza limite.

Per ottenere una quota positiva attraverso prefissi identici e profili invariati occorre quindi sfuggire sia a ogni cap fisso sulla slope della coda sia alle classi strutturate escluse, nel rispettivo dominio. Non è stato dimostrato un no-go per pochi edit generici o per ogni trasporto possibile, e non è stato ottenuto H.

Nessun esperimento, modifica Lean o uso GPU è stato necessario per questa revisione.
