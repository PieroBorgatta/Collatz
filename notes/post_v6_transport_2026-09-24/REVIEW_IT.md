# Controllo semantico della continuazione sulle torri

24 settembre 2026. Questa è una revisione interna degli enunciati e delle
formule, non una revisione umana indipendente. Gli esiti meccanici sono
registrati separatamente nel manifest finale.

## Domini e quantificatori

- `quotient_modEq_iff` usa v≥1, qualunque precisione b≥0 e parametri naturali
  q,r, incluso zero. Il caso di parametri uguali viene separato prima di
  usare la valutazione, evitando `ν₂(0)`.
- Il collegamento con la torre originale richiede q>0 e v≥1. Allora
  d=2^v q≥2 e l'indice 3d è pari e almeno 6: il reset originale è legittimo.
- La classificazione del suffisso impone primo esponente almeno 2 e gli
  altri strettamente positivi. Trova una classe dispari anche senza
  assumere in anticipo la disparità del parametro di cui si verifica il match.
- Ogni suffisso ammette parametri arbitrariamente grandi. Il parametro
  dipende dal suffisso; nessun passaggio scambia `∀ parola ∃ parametro`
  con `∃ parametro ∀ prefisso`.

## Fattori e tempi

- LTE fornisce `ν₂(9^(2^v d)−1)=v+3+ν₂(d)`.
- Il modulo del cilindro in z è `2^(A+1)`. La sostituzione
  `z=2·3^s Q−1` cancella un solo fattore 2: il modulo del parametro q
  è `2^A`, non `2^(A−1)`.
- Il primo esponente almeno 2 implica che P+C è divisibile per 4.
  Dopo il dimezzamento, l'addendo costante è pari e il bersaglio è
  dispari: la classe del parametro è quindi dispari.
- La fase C parte dall'indice originale k=3d. Il reset costa un passo,
  i d−1 blocchi costano 2(d−1), l'uscita `[1,4]` costa due, la raffica
  successiva costa v: il totale è `2d+1+v`.
- La fase B è collegata formalmente dalla sua uscita nota alla raffica;
  il teorema principale di libertà dalla sorgente originale usa la fase C.

## Cosa viene effettivamente escluso

Non può esistere una parola finita ammissibile vietata a tutta questa
famiglia con v fissato e q dispari libero. In particolare non si può
forzare un esponente maggiore di 1 entro un numero prefissato di passi
successivi al primo esponente 2. Si possono prescrivere tanti 1 consecutivi
quanto si vuole, scegliendo q opportunamente.

Questo non esclude un teorema su un sottoinsieme del parametro, un vincolo
che dipenda dalla sua grandezza, una discesa a un tempo dipendente da q,
o un rango diverso dal valore dell'orbita. Non conclude che tutte le
valutazioni di una singola orbita siano variabili aleatorie indipendenti.

`[2] ++ [1]^l` specifica un passo seguito da una raffica crescente. Il primo
passo può scendere sotto il valore all'uscita della raffica precedente.
Nessun teorema nuovo qui asserisce la mancata discesa dell'intero segmento
sotto la sorgente originale, né un ritorno effettivo alla sezione E.

## Criterio con limite sul parametro

Il rappresentante r è dispari, quindi positivo. Per ogni q che realizza
la parola, `q mod 2^A=r` implica r≤q. Viceversa r stesso realizza la parola.
Questo dimostra l'equivalenza `esiste 0<q≤B con il match ↔ r≤B`.
La trasformazione di un limite sulla sorgente in un limite su q sfrutta
la formula della sorgente e resta un'operazione ulteriore; nessuna stima
uniforme sulle parole che evitano la discesa è presupposta.

## Letteratura e perimetro della verifica

La suriettività dei prefissi nella codifica binaria è un fenomeno classico.
Il risultato locale riguarda il parametro esponenziale specifico delle
torri e la sua connessione al codice precedente. I test Python verificano
anche orbite di interi costruiti, oltre ai residui, ma restano finiti.
Il replay sullo stesso kernel e il controllo dei suoi assiomi non equivalgono
a un controllo tramite un'implementazione indipendente del kernel.
