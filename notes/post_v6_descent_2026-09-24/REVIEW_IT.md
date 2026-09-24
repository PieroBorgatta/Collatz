# Revisione interna della tappa di discesa

24 settembre 2026. Revisione separata da agenti dello stesso sistema;
non costituisce peer review umana o un controllo formale indipendente.

- La metrica parte da z(q) e usa come soglia n(q). Per q=1 il tempo è zero;
  per q=3 c'è una discesa precedente al punto z, dichiarata nella nota.
- Confermata la prova q≤3(A−k) e quindi q<2^A, con A≥2 e k≥1.
  La conclusione q=r_w usa il teorema esistente della classe parametrica.
  Non garantisce discesa al minimo residuo e non produce una famiglia infinita.
- Confermati sia il certificato razionale di discesa entro k sia il controllo
  del tempo omogeneo tramite il minimo degli iterati precedenti.
- Corrette due anomalie latenti, non attivate dal campione interamente risolto:
  `None` nel CSV deve essere letto dal campo vuoto; un caso censurato può già
  confutare un limite se tutti gli iterati fino a `floor(bound*q)` sono stati
  osservati sopra soglia. Cinque test di regressione fissano questi casi.
- Separati replay completo con la stessa implementazione in CI e replay
  aritmetico con una seconda implementazione su 84 parametri. Il secondo
  controlla anche i certificati di quei parametri; non ricontrolla con quel
  metodo tutte le 4.130 traiettorie.
- La compressione del blocco [1,2] ha un precedente diretto nel lavoro di
  Andrei–Kudlek–Niculescu (2000); il prodotto per la correzione affine è già
  nel Teorema 4.2 di Rozier–Terracol. Le attribuzioni sono esplicite.
- Nessuna stima in densità è trasferita alla famiglia esponenziale; nessuna
  statistica dei residui è trasformata in indipendenza lungo una singola orbita.
- Nessuna dichiarazione Lean aggiunta e nessuna pretesa di novità assoluta.
  La v6 pubblicata e le vecchie evidenze rimangono snapshot immutati.
