# Test congelato: sette antenati e congruenza ternaria

Protocollo scritto il 26 settembre 2026 prima della ricerca dei nuovi
valori di parità. È una registrazione locale del piano, non una
preregistrazione pubblica con marcatura temporale esterna.

## Formula candidata

Si usano

\[
Q_w=(3^{2^{w+1}}-1)/2^{w+3},\qquad
f_w(z)=z+2^{w+2}z^2,\qquad
G_{u,d}=f_{u+d-1}\circ\cdots\circ f_u,
\]

\[
H_w=\lceil589\,2^w/612\rceil,\qquad
\mu_w(z)=2^{w-1}-J_z(H_w),
\]

dove \(J_z(h)\) conta le parità dispari nei primi \(h\) passi della mappa
\(T(z)=z/2\) se pari e \((3z+1)/2\) se dispari.

Per ogni \(v\ge10\), posto \(u=v-7\), la formula candidata è:

* \(x\) è un intero positivo dispari;
* \(x\equiv Q_u\pmod{3^{2^{u-1}}}\);
* \(Y=G_{u,8}(x)\) appartiene allo stesso intervallo
  \([2^B,2^{B+1})\) di \(Q_{v+1}\);
* \(X=G_{u,7}(x)\) soddisfa \(\mu_v(X)\ge0\);

allora \(\mu_{v+1}(Y)\ge0\).

La formula proviene dal successo esplorativo dei dodici candidati al
livello 10 nella fase `post_v6_ancestry_2026-09-25`. Non è una legge già
validata. Non si richiede la parola di parità completa di \(Q_v\).

## Ricerca fissata prima dei risultati

1. Testare soltanto il nuovo caso \(v=11\), \(u=4\).
2. Calcolare con interi l'intervallo inclusivo \([L,U]\) delle radici
   ammesso dall'altezza di \(Q_{12}\), prima di calcolare le parità.
3. Calcolare i limiti interi di \(t\), il primo e ultimo candidato e la
   cardinalità esatta, usando \(x=Q_4+2\cdot3^8t\).
4. Enumerare i candidati in ordine strettamente crescente di \(t\),
   includendo i valori negativi ammessi dall'intervallo.
5. Arrestarsi al primo candidato con \(\mu_{11}(X)\ge0\) e
   \(\mu_{12}(Y)<0\), oppure dopo 100000 candidati, oppure
   all'esaurimento dell'intervallo: vale il primo evento raggiunto.
6. Verificare il testimone mediante iterazione diretta su interi e
   costruzione separata degli antenati con la formula chiusa di \(G\).
   Registrare parità complete, hash, conteggi, congruenze e altezze.
7. Non cambiare profondità, precisione ternaria, altezza, margini o
   ordine di ricerca dopo aver visto i risultati.

## Interpretazione prestabilita

Un solo controesempio respinge l'implicazione universale indicata. Non
respinge Collatz né un enunciato limitato ai soli \(Q_v\). Nessun
controesempio entro una ricerca incompleta significa solo ricerca
parziale; l'esaurimento senza controesempi verifica soltanto questo caso
finito. Non vengono rivendicati nuovi livelli della torre, nuovi teoremi
Lean o originalità scientifica.
