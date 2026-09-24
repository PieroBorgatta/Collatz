# Revisione interna della continuazione fra livelli

24 settembre 2026. La revisione è stata svolta tramite agenti separati
all'interno della stessa sessione: non è peer review esterna e non verifica
la priorità matematica. Nessun nuovo enunciato è stato formalizzato in Lean.

## Matematica

Sono stati ricontrollati il ponte [2,2,v−4], la ricorrenza quadratica,
ν₂(Q_w−Q_v)=v+2 per ogni w>v, il criterio esatto A≤v+1 e la valutazione
minima al primo passo diverso. La non-discesa dei prefissi comuni è provata
per ogni v≥5: stima generale per v≥6, controllo separato del prefisso
[3,1,1] per v=5. La compressione rispetto a Q_v non raggiunge N_v.

La prova che t_v→∞ è stata controllata da due agenti. Usa la trascendenza
di L=log_{ℚ₂}(9)/8 come conseguenza del teorema classico di Mahler; non
assume la congettura di Collatz. Il limite reale Q_v/N_v→∞ e la
stabilizzazione di ogni prefisso finito sono usati con quantificatori
distinti: ∀K ∃V ∀v≥V. Nessuna monotonia o finitezza di ciascun t_v è dedotta.
Nel report «equivalentemente» è stato sostituito con «di conseguenza»:
il tempo definito dalla disuguaglianza stretta < non distingue da solo
un valore uguale alla sorgente, mentre la prova stabilisce effettivamente >.

Le fonti di Mahler sono state controllate attraverso la ristampa EMS e
la formulazione esplicita usata da Calegari–Dimitrov–Tang a p. 21.
Non si invoca una versione completa p-adica di Lindemann–Weierstrass.

## Software e dati

La revisione ha verificato il limite di precisione e la gestione
dell'esponente divergente maggiore come limite inferiore. Per v=6,
l'esponente reale 8 è soltanto ≥4 dai bit del confronto: c'è un test
esplicito contro l'errore di presentare 4 come valore esatto.

Due difetti di robustezza sono stati trovati e corretti, senza modificare
i risultati dell'esperimento predefinito:

- La CLI ammetteva 5 livelli ma selezionava comunque il livello 16 per
  il controllo diretto. Ora filtra gli indici e ha un test sulla
  configurazione minima valida.
- Il confronto con i dati precedenti presupponeva la discesa in entrambe
  le corse. Ora confronta tempi esatti oppure disuguaglianze compatibili
  con la censura, e confronta le somme soltanto a parità di endpoint
  temporale. I test includono cap 0, cap 4, discesa esattamente al cap 5,
  precedenti osservazioni censurate e una coppia di tempi incompatibili.

Tutti i sei test passano localmente. Le divisioni ripetute usate nei test
forniscono un controllo distinto dei prefissi su piccoli interi; il replay
completo in CI usa lo stesso programma Python, non un'implementazione
indipendente. I tre calcoli del limite concordano su 4.096 bit, ma non
sono una dimostrazione della sua trascendenza.

I tredici casi già presenti nel CSV precedente sono marcati come
sovrapposizione; l'unico nuovo parametro intero completo è q=131071.
I 512 confronti modulari non sono 512 verifiche complete di discesa.
Il cap operativo resta una censura: non raggiungerlo con successo non
sarebbe una dimostrazione di divergenza.

La riproduzione completa è passata nella
[CI 36023967396](https://github.com/PieroBorgatta/Collatz/actions/runs/36023967396),
al commit `c2a194962870b157bf6dc6f216baf49eb000f9f3`: entrambi i risultati
scaricati coincidono byte per byte. Sono passati anche build e audit Lean
esistenti nella [CI 36023967347](https://github.com/PieroBorgatta/Collatz/actions/runs/36023967347).
Il successo Lean riguarda il progetto già formalizzato, non le prove
informali di questa continuazione.
