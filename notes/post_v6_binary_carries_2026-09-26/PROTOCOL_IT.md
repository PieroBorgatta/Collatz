# Esperimento circoscritto: riporti binari della torre

26 settembre 2026. Autori: Piero Borgatta e Codex, con revisione interna
di agenti. Questo piano fissa il dominio del programma archiviato prima
della sua esecuzione. La scelta del modello segue l'analisi delle fasi
precedenti e un piccolo sondaggio interno sui riporti futuri: non è una
preregistrazione cieca o pubblica.

## Stato esatto e compressione candidata

Si parte da `R_0=3` e si genera `R_(a+1)=R_a²` in colonne binarie.
Con `b_(a,n)=bit_n(R_a)`, la colonna del prodotto e il riporto sono

```
d_(a,n) = sum_{i=0}^n b_(a,i)*b_(a,n-i)
C_(a,0) = 0
b_(a+1,n) = (C_(a,n)+d_(a,n)) mod 2
C_(a,n+1) = floor((C_(a,n)+d_(a,n))/2).
```

Il generatore esatto conserva i prefissi delle righe; non si assume che
sia uno stato di dimensione uniforme. `Q_v=(R_(v+1)-1)/2^(v+3)`.
I bit così prodotti alimentano il trasduttore delle code shortcut,
con le due orbite confrontate agli orizzonti `H_v` e `H_(v+1)`, dove
`H_v=ceil(589*2^v/612)`.

La compressione da falsificare conserva, alla colonna `n`, livello,
posizione, riporto corrente, ancoraggio basso modulo `2^(r+1)`, ultime
`w` cifre d'ingresso e del quadrato. Si fornisce anche il bit corrente
d'ingresso. Il dominio di questo test di chiusura è quello degli input
`P=1+2^r*X`, `X` positivo dispari, non soltanto le potenze esatte di 3.
Una collisione esclude la previsione deterministica su questo dominio;
non esclude un'astrazione con più uscite o una stima sulla torre esatta.

## Tre controlli fissati

1. **Generazione esatta.** Per `v=5..9`, generare le due sorgenti per
   colonne dai quadrati successivi del seme 3. Confrontare tutti i bit
   delle righe con esponenziazione modulare separata, tutti i riporti con
   un prodotto a coefficienti impacchettati e le parole shortcut con
   iterazione intera diretta. Gli hash delle parole devono coincidere
   con `margin_results.json`. Non si estendono i livelli storici.
2. **Informazione e chiusura.** Riprendere gli otto testimoni di soglia
   `v=5..12` di `renewal_results.json` e quello dei sette antenati.
   Alla massima precisione condivisa fra `X` e `Q_v`, verificare
   l'uguaglianza di tutti i riporti esposti e il primo riporto diverso.
   Controllare esaustivamente gli input dispari ancorati per `r=3..6`,
   colonne `n=r+2..12` e finestre `w=1..min(4,n-r-1)`. Conservare la
   prima collisione nell'ordine crescente degli input per ogni tripla.
   Verificare inoltre una famiglia analitica di collisioni con stessa
   binade e stessi bit alti. Se la compressione non è chiusa, arrestare
   la ricerca di un potenziale deterministico per quello stato.
3. **Selettività di un riporto futuro.** Per `v=0..4`, enumerare tutti
   gli input che condividono con `Q_v` i primi `H_v` bit e quelli da
   `K=H_(v+1)` in su. Condizionare sul riporto del quadrato alla colonna
   `r+K`, uguale a quello della sorgente effettiva. Registrare il numero
   di candidati, la distribuzione completa dei difetti `Delta` e il
   massimo prima e dopo il filtro. Questi livelli piccoli sono
   diagnostici; non si impone una binade se i bit alti non la fissano.
   Il riporto futuro usa informazione oltre il prefisso: non è un
   rinnovo gratuito e non è già noto dall'orbita inferiore.

Si registrano anche le somme parziali firmate già determinabili dai
conteggi congelati `v=16..24`. È contabilità storica, non una stima
indipendente dei difetti futuri.

## Interpretazione e arresto

L'esito utile sarebbe un vincolo quantitativo ricavato dallo stato
aritmetico, con un costo cumulativo dimostrato indipendentemente dalle
parità da maggiorare. Un filtro che identifica il punto per definizione
o una riscrittura del telescopio non soddisfa questo criterio.

I riporti esposti possono risultare ridondanti; quelli futuri possono
avere selettività finita senza fornire un bilancio uniforme. Si riportano
anche questi esiti negativi. Nessun aumento dei livelli, delle finestre
o delle soglie viene deciso in base ai risultati. Nessuna nuova prova
di Collatz, discesa uniforme o originalità viene rivendicata. Non sono
previste nuove dichiarazioni Lean per questa fase sperimentale.
