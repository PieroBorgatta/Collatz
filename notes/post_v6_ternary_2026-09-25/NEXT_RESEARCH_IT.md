# Il prossimo problema: propagare il controllo oltre la prima divisione

Il primo difetto di riporto è ora limitato uniformemente dalla prova in
[FIRST_SEAM_BOUND_IT.md](FIRST_SEAM_BOUND_IT.md). Il problema aperto è la
stabilità di questa cancellazione quando le due traiettorie aggiungono
cifre `1` in tempi diversi. La stima attuale riguarda una sola scansione
interna della parola concatenata superiore, non il difetto fra le due
traiettorie su tutta la finestra.

Il prossimo esperimento utile deve conservare la **parola intera** e la
posizione delle aggiunte. La lunghezza e i sei conteggi locali non
contengono informazione sufficiente per il bilancio universale esaminato.
Le obiezioni dimostrate non escludono stime specifiche della torre né
potenziali con memoria più ricca.

## Obiettivo circoscritto

Derivare una formula esatta per le somme di riporti dopo una sequenza
prescritta di divisioni e aggiunte, separando la dipendenza dai prefissi
ternari originali da quella delle aggiunte. Per una parola di parità
fissata si conosce la forma affine dell'iterato; il lavoro necessario è
tradurre quella forma nei riporti e verificare se le somme risultanti
restano trattabili con un completamento di Fourier.

Si parte da due, quattro e otto passi oltre la prima giunzione, con
confronto contro il simulatore e contro l'iterazione intera nei casi
piccoli. Si deve rendere esplicito quanto cresce la complessità della
formula con il numero di aggiunte; una crescita esponenziale nel numero
di passi non produce da sola una stima utile sull'intera finestra.

Il risultato ricercato è una disuguaglianza con un costo delle aggiunte
controllato indipendentemente dal numero di dispari che si vuole stimare.
Se il costo richiede già la conoscenza di `J`, `E` o `Δ_v`, si è soltanto
riformulato il problema. Anche una stima per ogni finestra di lunghezza
fissa non autorizza il passaggio alla finestra `L_v`, che cresce col livello.

## Criterio di avanzamento

Un avanzamento verso la discesa richiede un ponte dimostrato fra i riporti
controllati e `E(m,L_v)`, oppure direttamente un maggiorante `g(v)` di
`Δ_v` con costo pesato sommabile e coperto da un margine iniziale verificato.
La fase [dei margini](../post_v6_margin_2026-09-25/RESULTS_IT.md) specifica
quest'ultimo criterio. Il nuovo limite sul primo difetto, pur essendo
sublineare in `m`, non soddisfa da solo questo requisito.

La prima attività dovrebbe quindi essere la derivazione e il controllo
della formula per pochi passi. Estendere la tabella numerica delle orbite
o accumulare nuovi nomi di lemmi non risolve questo passaggio.
