# Revisione interna dell'esperimento sui riporti binari

26 settembre 2026. Revisione matematica e dei controlli affidata a due
agenti, separata dall'implementazione principale. È una revisione interna
assistita, non peer review umana o un certificato Lean.

## Allineamenti e aritmetica

- Il seme è `R_0=3`, la sorgente inferiore usa la riga `v+1`, quella
  superiore la riga `v+2`. Le posizioni iniziali sono `v+3` e `v+4`.
  `K+v+4` colonne includono esattamente tutti i `K` bit superiori richiesti.
- Il prodotto a coefficienti impacchettati usa una radix strettamente
  maggiore del numero di colonne. Ogni coefficiente della convoluzione
  è al più quel numero: non possono verificarsi riporti fra slot.
  Il buffer del quadrato è sufficientemente lungo.
- La formula chiusa del riporto usa solo i coefficienti `i+j<N`.
  Sostituirla con il quoziente del quadrato dell'intero prefisso sarebbe
  errato, perché includerebbe anche coefficienti di colonne successive.
- Per i testimoni il prefisso massimo condiviso termina in `n=r+M`:
  si confrontano `C_0..C_n`, non si assume uguale `C_(n+1)`. Il primo
  riporto diverso differisce di uno e il primo bit del quadrato diverso
  è `n+1`. Sono stati verificati separatamente i numeri e gli shift.

Non sono stati individuati errori bloccanti in questi passaggi.

## Quantificatori della collisione

L'enumerazione piccola usa rappresentanti ancorati `P<2^n`, con bit
corrente zero. Per testare l'uscita immediata ciò non perde il caso con
bit corrente uno: sostituire `P` con `P+2^n` conserva stato precedente
e finestre, aggiunge due al coefficiente corrente e lascia invariata
l'uscita modulo due. I bit oltre `n` non intervengono.

I 13 casi con collisione bastano a falsificare lo stato deterministico
proposto sul dominio generale. I **67 casi senza collisione immediata
non provano la chiusura delle transizioni**, né l'uguaglianza delle
uscite a orizzonti maggiori. La famiglia analitica aggiunge stessa
binade e stessi bit alti, per ogni finestra finita.

Gli input alternativi non vengono identificati con potenze della
cascata esatta dal seme 3. La prova non esclude memoria particolare per
quella successione, ricalcolo modulare da livello e posizione, né
astrazioni con più uscite e costi cumulativi controllati.

## Selezione futura e bilancio

Le fibre enumerano tutti i `K-H` bit liberi, mantenendo i bit bassi e
quelli da `K` in su. La positività e la disparità seguono dal prefisso
di `Q_v`. Per i livelli diagnostici piccoli con parte alta nulla non
si aggiunge un vincolo di binade.

Il filtro futuro può escludere sorgenti: respinge tutti i nove vecchi
testimoni. Il massimo del difetto dopo il filtro resta però diverso
dal valore effettivo, ad esempio `6` contro `4` a `v=3`, e `0` contro
`−6` a `v=4`. Non ne deriva un vincolo uniforme per i livelli grandi.

Il dato futuro non è determinato dal solo prefisso esposto. Per usarlo
in un certificato occorrerebbe giustificare la sua condizione dalla
generazione esatta e ricavarne un costo indipendente delle parità. La
somma firmata storica non maggiora i termini non ancora osservati.

## Metodi di controllo e stato della verifica

I test ricostruiscono le colonne mediante prodotti scolastici annidati,
le uscite mediante quadrati interi e le parità mediante iterazione
shortcut diretta. Le piccole fibre e le prime collisioni sono
riesaminate esaustivamente con oracoli separati. Per i grandi riporti
archiviati è usata anche la formula triangolare dei coefficienti e
una diversa radix impacchettata; quest'ultima condivide il principio
di convoluzione con il programma principale.

Il test di alterazione controlla il rifiuto di un digest congelato
non valido senza modificare i file storici. Il replay del risultato
deve essere identico byte per byte. I log finali e gli hash sono nel
[manifesto](verification_manifest.json).

La verifica è locale. Il workflow predisposto è ripetizione del codice
archiviato; finché non viene eseguito non è evidenza di una CI riuscita.
Nessuna nuova dichiarazione Lean o build aggregata è necessaria per
queste note e non ne viene rivendicata una.
