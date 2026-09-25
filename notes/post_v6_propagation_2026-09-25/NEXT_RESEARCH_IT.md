# Studiare la coda, alimentata dai bit iniziali

La fase attuale ha risolto l'identificazione delle colonne originarie:
il loro comportamento è una successione di semplici divisioni per due.
Il passo successivo deve riguardare le colonne aggiunte, che contengono
la dipendenza dalle parità, e il confronto di orizzonti diversi.

## Ricorrenza esatta della coda

Scriviamo

\[
 T^t(n)=3^{j_t}P_t+z_t,\qquad
 P_t=\lfloor n/2^t\rfloor,\qquad 0\le z_t<3^{j_t}.
\]

All'inizio `j_0=0,z_0=0`. Il bit d'ingresso è
`h_t=P_t mod2=bit_t(n)`. La parità effettiva è

\[
 p_t=(h_t+z_t)\bmod2.
\]

Poiché `P_t=2P_(t+1)+h_t`, sostituendo nei due rami di `T` si ottiene

\[
 (j_{t+1},z_{t+1})=
 \begin{cases}
 (j_t,(3^{j_t}h_t+z_t)/2),&p_t=0,\\
 (j_t+1,(3^{j_t+1}h_t+3z_t+1)/2),&p_t=1.
 \end{cases}
\]

I numeratori sono pari per definizione di `p_t`; il lemma del quoziente
assicura il limite sul nuovo resto. È una riscrittura esatta, non ancora
un criterio di diminuzione. Il numero degli stati possibili cresce con
la lunghezza `j_t` della coda.

## Esperimento che distinguerebbe un progresso da una riscrittura

Implementare il trasduttore della coda con una contabilità esatta dei
riporti e delle cancellazioni fra le due orbite. Verificare prima pochi
passi contro le parole complete. Usare i bit effettivi delle sorgenti;
un risultato medio su ingressi arbitrari non dà un limite puntuale
sulla torre.

Cercare quindi un'identità telescopica o un potenziale che controlli
la somma dei difetti delle code e il passaggio dai tempi uguali ai tempi
`L` e `2L`. Un costo `O(t)` per scansione diventa `O(L²)` sommato
su `L` passi: è insufficiente. Una normalizzazione che richieda già
conoscere o limitare `j_t` non chiude il problema.

Prima di estendere gli esperimenti, la formula candidata deve indicare
un maggiorante indipendente per il costo cumulativo e come questo
implichi il criterio pesato della [fase dei margini](../post_v6_margin_2026-09-25/RESULTS_IT.md).
La sola piccolezza della giunzione originaria non autorizza quel passaggio.
