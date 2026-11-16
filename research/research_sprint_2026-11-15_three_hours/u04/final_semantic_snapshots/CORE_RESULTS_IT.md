# Prototipo standalone del massimo aritmetico

**PASS** locale: sei enunciati pubblici, controllo Lean standalone e audit transitivo di tutte le18 dichiarazioni matematiche compilate, incluse8 private codificate. Sono ammessi soltanto `propext`, `Classical.choice`, `Quot.sound`. Il prototipo non è importato dalla libreria principale e non modifica le statistiche dei quattro moduli integrati.

Il dominio usa seed naturali positivi, dispari e non divisibili per3. Una parola ammissibile è effettiva e termina al target; non si assume nonritorno. La definizione totale F usa baseline1 anche fuori dal dominio valido; le conclusioni di massimo raggiunto e F≤n richiedono un target positivo dispari unità.

La finitezza di `BoundedSlopeCatalogue(n,1)` consente di prendere il massimo dei pesi≥1 dei seed unità. La parola vuota fornisce il peso1 per ogni target valido. Le parole di peso<1 sono dominate automaticamente.

Gli enunciati verificati sono:

- `one_le_envelope`: F(n)≥1.
- `wordWeight_le_envelope`: ogni parola ammissibile ha Ω≤F(n), anche se Ω<1.
- `exists_maximizing_word`: un’autentica parola da seed unità realizza il massimo.
- `envelope_le_target`: F(n)≤n per target valido.
- `optimal_source_bound`: il seed positivo di una parola ottimale soddisfa u≤n/F(n).
- `envelope_le_of_word_majorant`: F è il minimo maggiorante numerico dei gain di tutte le parole ammissibili. Quest’ultimo non è ancora un teorema di supersoluzione edge-by-edge.

La funzione F è noncomputabile: la finitezza del catalogo non certifica i tempi di arrivo di piccoli seed e non rende decidibili mediante timeout gli arrivi mancanti. Non sono introdotti g, Q, densità, profili ottimali, lower del surplus o conclusioni Collatz. Nessun esperimento o GPU utilizzato. Il sorgente del prototipo è ora congelato; eventuali estensioni vivranno in un altro file.
