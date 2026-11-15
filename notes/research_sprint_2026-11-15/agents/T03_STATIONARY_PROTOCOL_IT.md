# T03: diagnostica congelata della legge stazionaria

Protocollo fissato il 15 novembre 2026, prima dell'esecuzione. Scopo: controllare
come una famiglia di target che varia con k interagisce con una profondità
ternaria finita m. Non stimare una densità di bacino né dimostrare H.

- Profondità: m=1,...,12, senza estensione adattiva.
- Famiglia: n_k=2·3^k−1, k=1,...,10; target superiori h(n_k)=16n_k+5.
- Controtest fissi: i punti 3-adici −1, −5, −17 e −11.
- Legge: densità del cilindro rho_m(x)=3^m P(X≡x mod3^m), per
  X=sum_{j≥0}3^j 2^{−(a_1+...+a_{j+1})}, P(a_i=a)=2^{−a}.
- Calcolo: ricorrenza binaria ciclica sulle unità modulo3^m,
  rho_m(x)=rho_m(2x)/2+(3/2)1_{2x≡1 mod3}rho_{m−1}((2x−1)/3).
  Si parte da rho_0=1 e si risolve il ciclo delle potenze di2.
- Verifiche: rho_m=0 fuori dalle unità, positività sulle unità,
  massa totale sum_x rho_m(x)=3^m e residuo massimo dell'equazione
  inferiore a10^-9. A m≤4 si ricalcola tutto con Fraction, con uguaglianze
  esatte di massa e ricorrenza e confronto numerico ≤10^-12.
- Si registrano valori individuali e medie Cesàro sulle profondità1,...,m.
  L'assenza di un errore quantitativo per la convergenza della traccia è
  parte del risultato: questi valori non forniscono un upper bound per E.
- Per ogni n_k, la condizione di assenza di ritorni rimane non assunta e
  non verificata. Il test non viene presentato come controesempio a H.

Il limite della fonte esterna è m→∞ **a target intero fissato**. La diagonale
k≥m colloca n_k vicino a−1 e h(n_k) vicino a−11 nella topologia3-adica;
scambiare questi due ordini di limite non è autorizzato.
