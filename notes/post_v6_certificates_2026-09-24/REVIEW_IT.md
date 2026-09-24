# Revisione interna: certificati e prima separazione

24 settembre 2026. Revisione tramite agenti separati nella stessa sessione;
non peer review esterna. Originalità non accertata, nessuna nuova prova Lean.

## Criterio di discesa e software

La revisione conferma che H passi binari di T contenenti J passi dispari
iniziano J passi Syracuse con somma completa A_J≥H. La divisione finale
può essere incompleta. Il criterio non richiede un endpoint dispari noto,
quindi H bit iniziali sono sufficienti.

Con H=ceil((485K+52M)/306), K≤M=2^v, la prova controlla il termine
additivo con il fattore 3/2, senza assumere una frequenza probabilistica
degli esponenti. La conclusione è una discesa **entro J**, non una proprietà
necessaria dell'endpoint dopo J passi se una discesa precedente è avvenuta.
Il produttore usa coerentemente `descent_time_upper_bound`.

L'implementazione a blocchi è stata confrontata con passi binari scalari
e con una seconda implementazione che non importa il produttore. Quest'ultima
ottiene il residuo tramite ricorrenza quadratica e conta i passi Syracuse
modularmente, con l'ultimo esponente marcato come limite inferiore.
Il replay completo fino a v=21 ha confermato tutti i 20 tentativi dei
17 livelli: 4.037.892 divisioni binarie, 2.018.020 passi dispari, nessun
livello saltato. Il SHA dell'input è incluso nel risultato archiviato.

Dieci test persistenti controllano composizione affine su residui e loro
traslazioni, cambi di blocco, precisione finale, formula del residuo,
discesa su piccoli interi, falsi negativi del criterio, rifiuto di record
alterati e confronto della prima separazione con orbite complete piccole.
Le quattro manomissioni riguardano conteggio, precisione, hash e decisione.

I fallimenti del primo budget a v=6,7,9 restano nei dati; sono inconcludenti.
Il caso v=6 ha discesa effettiva entro 28 passi pur fallendo il certificato
con budget 32. Il secondo tentativo certifica un limite sufficiente più largo.

## Applicazione di Chim

Il Teorema 2.1, pp. 298–299, è stato consultato nella fonte primaria.
La specializzazione con α₁=3, α₂=−c verifica che le basi sono unità e
che D=e=f=g=1. Il caso di dipendenza moltiplicativa c=3^b, incluso c=1,
è separato e trattato con valutazione ≤2. La costante 180000 e il cutoff
800 sono arrotondamenti conservativi, verificati con limiti razionali
su ln2 e ln3, non valori arrotondati in senso sfavorevole.

Sono stati ricontrollati c_j<12^{v+2}, E_j+1≤2^{v+3},
D_j=ν₂(3^{E_j}+c_j)−j−3 e il confronto quadratico/esponenziale a v=37.
L'induzione usa l'identità v²+803v+800>0. Per 5≤v≤36 il calcolo
modulare determina entrambi gli esponenti esattamente e verifica che
entrambi gli endpoint restano sopra le rispettive sorgenti.

La parte finita e gli arrotondamenti sono riproducibili in Python;
il teorema esterno e il ragionamento per tutti i v≥37 restano prove
informali. Il successo di una build Lean esistente non li formalizza.
Nessuna conclusione di discesa per tutti i livelli segue da questa nota.
