# Limite di una prova basata soltanto su residuo e altezza

25 settembre 2026. Dimostrazione su carta con revisione interna; non una
nuova dichiarazione Lean, né una rivendicazione di priorità matematica.

La candidata sulla massima caduta è sopravvissuta ai test, ma non siamo
riusciti a provarne la conservazione sui livelli arbitrari. Il tentativo di
chiuderla su uno stato descritto soltanto da alcuni bit e da una fascia
d'altezza incontra il seguente ostacolo esatto.

## 1. Un prefisso lascia libere le continuazioni fra i suoi lift

Siano L≥0, 0≤a<2^L e m≥1. Sia j il numero di passi dispari nei primi
L passi di T da a. Per ogni intero t≥0,

\[
 T^L(a+2^L t)=T^L(a)+3^j t.
\]

La formula segue componendo le L mappe affini: tutti i lift condividono
le prime L parità, e la pendenza complessiva è 3^j/2^L. Poiché 3^j è
invertibile modulo 2^m, esiste un unico t modulo 2^m tale che

\[
 T^L(a)+3^j t\equiv-1\pmod{2^m}.
\]

Equivalentemente, esiste un'unica classe b modulo 2^(L+m), contenuta nel
cilindro a modulo 2^L, che produce m passi dispari consecutivi nelle
posizioni L,…,L+m−1. Per verificarlo basta osservare che, se
y=2^m u−1, allora

\[
 T^i(y)=3^i2^{m-i}u-1\quad(0\le i\le m).
\]

I valori prima del passo m sono dispari. Viceversa, componendo m rami
dispari, l'integralità impone y≡−1 modulo 2^m.

## 2. Una fascia d'altezza ampia non elimina il controesempio

Ogni intervallo intero [X,2X), con X≥2^(L+m), contiene un rappresentante
positivo di ciascuna classe modulo 2^(L+m). Basta prendere il primo
rappresentante almeno X: dista da X meno del modulo.

Per il credito saturo con incrementi +305 e −284, scegliamo

\[
 m=\lfloor D/284\rfloor+1.
\]

Un rappresentante della classe appena costruita fallisce entro L+m:
o il credito era già negativo nel prefisso, oppure al tempo L vale al
massimo D e i successivi m passi sottraggono 284m>D.

Pertanto, se H≥L+m e X≥2^(L+m), la cella

\[
 \{n>0:n\equiv a\pmod{2^L},\ X\le n<2X\}
\]

contiene un intero che esaurisce il credito entro H. Non si può certificare
la sopravvivenza di **tutta la cella**.

## 3. Conseguenza per questa particolare astrazione della torre

Posti M=2^v e v≥5, H_v≤M e

\[
 Q_v=\frac{9^M-1}{2^{v+3}}
 \ge2^{3M-v-3}\ge2^M.
\]

La prima disuguaglianza usa 9^M−1≥8^M; la seconda usa 2M≥v+3.
Se X è la potenza di due con X≤Q_v<2X, allora X≥2^M≥2^H_v.
Quindi l'ipotesi d'altezza della sezione 2 è automatica quando L+m≤H_v.

Una certificazione valida per tutti i lift positivi che conservano soltanto
i primi L bit di Q_v e questa fascia d'altezza richiederebbe dunque

\[
 L\ge H_v-\left\lfloor\frac{128v^2}{284}\right\rfloor.
\]

Al livello 24 significa almeno **16.146.441 dei 16.146.700 bit**:
questa astrazione può dimenticare al massimo 259 bit. È una condizione
necessaria per quel tipo di certificazione, non una condizione sufficiente.

## 4. Cosa questo risultato non dice

Gli interi costruiti non sono identificati con Q_v, né con stati di una
sua orbita. Non confutano la candidata sulla torre. Il risultato non è
un limite alla complessità di qualsiasi dimostrazione, e non esclude una
prova simbolica che sfrutti la formula esatta di Q_v.

Mostra che una futura prova deve conservare vincoli aritmetici più forti
dell'appartenenza a un cilindro e a una fascia d'altezza. Inoltre escludere
le sole sequenze interamente dispari non basterebbe: la candidata richiede
di escludere ogni intervallo con

\[
 589\,\#\mathrm{dispari}-305\,\mathrm{lunghezza}>128v^2.
\]

Non abbiamo trovato una proprietà della torre che escluda uniformemente
tutti questi intervalli. Questo è il punto in cui il tentativo di prova
si arresta; i test positivi non colmano il passaggio mancante.
