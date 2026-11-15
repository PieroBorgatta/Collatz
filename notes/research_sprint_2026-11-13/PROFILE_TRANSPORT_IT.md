# Confronto dei profili e passaggio ai predecessori ordinari

13 novembre 2026. Ricerca del coordinatore nel perimetro del [protocollo congelato](PROFILE_TRANSPORT_PROTOCOL_IT.md). Le costruzioni e i conteggi qui esposti sono finiti. Non è stata dimostrata una quota asintotica di massa.

## Perché cambiare l'intera parola

Le correzioni di due soli esponenti producono pochi successi nel censimento S06. Il nuovo dizionario permette una relazione più ampia: una parola da u a n e una parola da v a h(n) possono avere esponenti completamente diversi, conservando soltanto il profilo `(k,A)`, cioè lunghezza e totale delle valutazioni.

Per il dominio di H, il risultato su carta S10 dà

`v ≤ D₀u`, con `D₀=21 exp(B/3)` universale,

per ogni trasformazione reale che conservi `(k,A)`. La costante è enorme e non viene sostituita dai piccoli valori D dell'esperimento. L'interesse è teorico: per questi trasporti l'altezza non richiede una nuova stima separata per ogni parola.

La parte non dimostrata diventa il confronto delle capacità dei profili: quante sorgenti del bacino di base possono essere accoppiate a sorgenti effettive dell'altro bacino, senza riutilizzare le immagini? La distribuzione congiunta di residuo ternario e totale A è pertinente a questa domanda; due distribuzioni marginali non bastano.

## Accoppiamento finito con capacità uno

Per ciascun target e cutoff, il programma ricostruisce tutte le orbite finite usate, con cap esplicito. Per ogni sorgente considera la parola del primo arrivo e raggruppa le sorgenti per `(k,A)`. Un arco u→v richiede profili uguali e `v≤Du`.

All'interno di un profilo, le sorgenti u e le immagini v vengono ordinate. Il minimo v viene assegnato al primo u che lo ammette. Questa regola trova un matching di cardinalità massima per il grafo a soglia:

- Se il minimo v supera Du per il minimo u, quel u non ha alcun arco e può essere scartato.
- Altrimenti esiste un matching massimo contenente la coppia dei due minimi. Se erano accoppiati diversamente, scambiare i due archi conserva la validità, perché i successivi u sono maggiori e quindi ammettono ogni immagine già ammessa dal primo.
- Si rimuovono i due minimi e si ripete.

Le immagini sono interi distinti e ogni sorgente è usata una sola volta: il carico è uno per questa specifica selezione. Ciò non contraddice le collisioni S06, che riguardano una relazione diversa prima della selezione.

Il [replay indipendente S13](agents/S13_REPLAY_IT.md) usa cammini aumentanti, senza copiare il greedy, e certifica il massimo con un vertex cover della stessa cardinalità. Otto casi a X=256, D=16/64 coincidono esattamente.

## Risultati sul dominio congelato

Sono stati fissati prima del calcolo n in `{5,7,31,593}`, X in `{256,1024,4096}` e D in `{4,16,64}`. I 36 casi hanno completato il censimento. Il grafo contiene 208.223 nodi dispari effettivamente visitati; la massima profondità accelerata è 164. Si tratta di una verifica finita degli inizi usati, non di un'ipotesi di terminazione per altri inizi.

Per X=4096 e D=64:

| n | h(n) | Sorgenti dispari di base | Sorgenti dispari accoppiate | Sorgenti di base in profili senza immagini |
|---:|---:|---:|---:|---:|
| 5 | 85 | 1924 | 946 | 470 |
| 7 | 29 | 382 | 376 | 6 |
| 31 | 125 | 197 | 190 | 6 |
| 593 | 9493 | 689 | 2 | 687 |

Il cambiamento dell'intera parola produce accoppiamenti effettivi che la modifica di pochi esponenti non trovava. Il bersaglio 593/9493 rimane però fortemente sbilanciato: il risultato non giustifica una costante uniforme, né la promozione del rapporto finito a una densità.

La parte utile della diagnostica sono i profili mancanti e le capacità insufficienti. Essi indicano quale disuguaglianza dovrebbe fornire una teoria degli atomi congiunti, oppure dove occorrerebbe cambiare anche profilo o profondità.

## Preservare i fattori di due

Un matching iniettivo f fra parti dispari induce un matching fra sorgenti ordinarie:

`2^e u → 2^e f(u)`.

Ogni positivo ha una decomposizione unica in parte dispari e potenza di due, quindi il matching rimane iniettivo. L'altezza resta al più D. Le traiettorie Syracuse certificate danno traiettorie ordinarie mediante i passi pari e dispari usuali.

Al cutoff X, il peso di u è il numero di e con `2^e u≤X`, cioè `floor(log₂(X/u))+1`. Questi pesi devono essere contati: la percentuale non pesata di parti dispari non è la percentuale di sorgenti ordinarie.

Lo [script supplementare](experiments/root_profile_lifts.py) conserva esattamente i matching e i parametri precedenti, verifica la distinzione delle immagini e ricalcola i pesi. Un replay indipendente con la mappa ordinaria controlla tutti i 1024 inizi dei quattro target al cutoff minimo.

Per X=4096 e D=64, il matching induce:

| n | Sorgenti ordinarie di base | Sorgenti ordinarie accoppiate |
|---:|---:|---:|
| 5 | 3839 | 1842 |
| 7 | 731 | 702 |
| 31 | 373 | 341 |
| 593 | 1343 | 4 |

Le immagini stanno entro DX; questi rapporti non sono stime della densità del bacino superiore al cutoff X. La selezione può essere migliorata, ma il suo perfezionamento finito non dimostra una massa persistente nel limite.

## Un lemma sufficiente da cercare

Nel dominio senza ritorni, ogni sorgente fisica ha una sola parola di arrivo; anche le immagini del pool non ricorrente hanno una sola rappresentazione fisica. A profilo fissato, il dizionario ternario conta esattamente le parole ammissibili e le loro sorgenti.

Una possibile prosecuzione è minorare la somma delle capacità dei profili comuni rispetto alla massa effettiva di base, scartando soltanto una massa o_n(X), con cutoff e normalizzazione dichiarati. La stima deve riguardare gli stessi interi e gli stessi profili, non due lower bound separati. Se profili sfavorevoli concentrano una massa non trascurabile, occorrerà un trasporto fra profili o una comparazione aggregata fra blocchi di fratelli.

Per passare da una comparazione a tutti i cutoff dispari alla comparazione ordinaria si può anche sommare sui fattori di due. Si tronca a e<E, si applicano le stime ai finitissimi cutoff `X/2^e`, poi si passa a X→∞ e infine E→∞. La coda e≥E contiene al più X/2^E inizi, perché tutti sono divisibili per 2^E. Questo ordine dei limiti evita di scambiare una somma infinita con un liminf senza controllo.

**Criterio di arresto:** non continuare con soli cutoff maggiori se la costruzione non espone un lemma di comparazione relativa o un nuovo meccanismo fra profili. La coppia 593/9493 deve restare fra i controtest; non va eliminata per migliorare i rapporti osservati.

I due programmi del coordinatore danno output identici con e senza ottimizzazione Python. [Dati dei profili](verification/root_profile_transport.json), [dati ordinari](verification/root_profile_lifts.json) e [controllo indipendente del matching](verification/s13_profile_matching.json) conservano il dominio e i risultati esatti.
