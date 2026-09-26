# Vincolo del riporto futuro: test fissato al livello 16

26 settembre 2026. Piero Borgatta e Codex. Piano fissato prima della
generazione dei nuovi candidati al livello 16. La famiglia di parole
è scelta dopo un sondaggio esplorativo ai livelli 5..12: non è una
preregistrazione cieca o pubblica. Quel sondaggio non ha esaminato
candidati al livello 16.

## Obbligo e implicazione da sottoporre a prova

Si usano `Q_v=(3^(2^(v+1))-1)/2^(v+3)`,
`f_v(x)=x+2^(v+2)x²`, `H_v=ceil(589*2^v/612)` e
`Delta_v(X)=J_(f_v(X))(H_(v+1))-2J_X(H_v)` per la mappa shortcut.
Il bersaglio proposto sulla torre esatta è `Delta_v(Q_v)<=g(v)`,
`g(v)=2*2^ceil(v/2)`, per tutti i livelli da 16. Non è dimostrato.

Il test riguarda invece la possibile estensione a una classe selezionata.
Si congela soltanto `v=16`, `r=19`, `H=63074`, `K=126147`,
`N=r+K=126166`. Si controlla l'implicazione candidata:

```
X>0 dispari; X mod2^H = Q_16 mod2^H;
floor(X/2^K) = floor(Q_16/2^K);
C_N(1+2^r*X) = C_N(1+2^r*Q_16)
    => Delta_16(X) <= 512.
```

`C_N` è il riporto scolastico binario del quadrato alla frontiera N,
non il quoziente del quadrato dell'intero prefisso. I bit alti fissati
conservano la binade della sorgente. L'intera parola inferiore è quella
effettiva perché coincide il residuo modulo `2^H`.

Si registra separatamente se un controesempio trasferisce anche il
margine da `m_16=1155` a un valore negativo: ciò avviene quando
`Delta_16(X)>2310`. Non è la condizione d'arresto principale.

## Famiglia e ordine congelati

Sia `F=K-H`. Si mantiene la parola superiore effettiva di lunghezza H.
Il suo suffisso di lunghezza F viene posto tutto uno e poi modificato
con le seguenti maschere di zeri:

1. Nessuno zero.
2. Uno zero nelle posizioni assolute
   `j_i=H+floor(i*(F-1)/511)`, per `i=0..511`, in ordine crescente.
3. Due zeri nelle posizioni `{j_i,H+K-1-j_i}`, nello stesso ordine.

Le maschere duplicate sono eliminate conservando la prima occorrenza.
L'elenco ha al massimo 1025 voci prima di eliminare i duplicati. Non
si cambiano la griglia, la famiglia o il livello dopo i risultati.

Per ogni parola si ricava il residuo superiore modulo `2^K`, si inverte
`f_16` modulo `2^K` e si ripristinano i bit della sorgente da K in su.
Tutti i candidati devono conservare il prefisso richiesto per costruzione.
Si controllano prima positività, disparità, altezza e peso previsto;
poi il riporto futuro. Arresto al primo candidato con riporto corretto
e `Delta>512`, oppure all'esaurimento dell'elenco.

Non si calcola un nuovo livello della torre. Le parole effettive ai
livelli 16 e 17 vengono riprodotte e confrontate con gli hash congelati.
La scelta dei completamenti non aspetta una discesa superiore.

## Verifiche e interpretazione

Prima della ricerca si salvano hash del protocollo, costanti ed elenco
delle maschere. Il generatore usa formule chiuse per i suffissi con pochi
zeri, un'inversione quadratica a precisione crescente e un riporto
certificato dai coefficienti finali. Questi algoritmi devono essere
controllati separatamente su piccoli domini esaustivi.

Per il primo testimone si archiviano gli interi esatti, le parole
complete e gli hash. Si riproducono le parità anche con l'iterazione
diretta degli interi. Il riporto deve essere controllato mediante
almeno due formule esatte, inclusa la forma lineare sui bit liberi.

Si dimostra su carta il vincolo lineare del riporto e si confrontano
tutte le piccole fibre `v=0..4` con le enumerazioni archiviate nella
fase precedente. I tre testimoni esplorativi `v=5..7` sono riportati
come tali e verificati, senza convertirli in conferme indipendenti.

Un controesempio respinge soltanto l'implicazione sulla classe di
completamenti, non il bersaglio sui soli `Q_v`, Collatz o ogni possibile
vincolo aritmetico della torre. Esaurire l'elenco senza controesempi
verifica soltanto questa famiglia finita. Il filtro non viene rinforzato
in questo stesso esperimento dopo un eventuale fallimento. Non sono
previsti nuovi teoremi Lean o rivendicazioni di originalità.
