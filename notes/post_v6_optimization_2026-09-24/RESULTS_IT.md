# Semi compatti e decadimento di ordine sei

24 settembre 2026. Continuazione della via dei due semi già verificata nel
commit `171150e`. I sorgenti nuovi sono separati dai sette moduli precedenti.
**Stato: nuove prove in attesa di compilazione e audit CI.**

## Due perdite evitabili

Scriviamo `G(r,k)=ndGeneralTargetRoot r k` e `Q=3^q`. Il vecchio limite era
`T_old=G(2a,(16^b+3)Q)`. Per superare `16^b` è sufficiente un esponente
`k>2b`, perché `G(r,k)≥4^k` quando `r≥1`. Il primo esponente congruo al
residuo prescritto sopra `2b` soddisfa `2b<k≤2b+Q`; il successivo è al più
`2b+2Q`. La stessa coppia garantisce un seme senza ritorni sotto

`T_new=G(2a,2b+2Q) < T_old`.

La seconda perdita è nella conversione del mixing. La stima originale dà
`(2/3)C/m^6`. Manteniamo quel valore attraverso l'API quadratica scegliendo
`D=(2/3)C/m^4`, con m fissato. Il budget terminale diventa

`88*T_new*C ≤ m^6`.

`OptimizedConductor.conductor T C` è il minimo naturale positivo che soddisfa
questo vincolo, trovato mediante un predicato decidibile. L'esistenza ha il
maggiorante finito `88TC+1`. Non si valuta alcuna delle enormi costanti pubbliche.

## Collegamento e confronto

`OptimizedDensity.lean` mantiene il coefficiente globale C nella selezione e
persistenza del seme. Usa D soltanto nel conteggio terminale. Il coefficiente
finale conserva la forma `3/(256*T*3^m)` e il cutoff `32*(H+1)`, con T e m
nuovi. L'input analitico esterno e le condizioni `a>0`, `3∤a` sono invariati.

`OptimizedComparison.lean` confronta direttamente le formule nuove e precedenti,
senza identificare chooser esistenziali. Gli enunciati candidati affermano,
per ogni `a>0`, un coefficiente strettamente maggiore e un cutoff strettamente
minore. Richiedono la compilazione prima di essere presentati come risultati
formalmente verificati. Non si confronta la formula con tutte le scelte
possibili di parametri, né si rivendica ottimalità globale.

## Limiti

La densità dei predecessori non risolve Collatz. Le costanti restano enormi;
la ricerca naturale minima non è proposta come algoritmo pratico per calcolare
il coefficiente pubblico. La revisione completa dell'argomento analitico resta
distinta dalla compilazione del codice e dagli audit delle dipendenze.
