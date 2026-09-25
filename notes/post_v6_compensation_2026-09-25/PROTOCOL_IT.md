# Protocollo congelato prima dei livelli 22–24

25 settembre 2026. Questa nota e `frozen_protocol.json` vengono committati
e pubblicati prima di calcolare i livelli di verifica 22, 23, 24. Non saranno
aggiornati alla luce dei loro risultati. Le conclusioni andranno in un
documento separato. È un protocollo interno versionato, non una registrazione
presso un registro esterno.

## Candidata

Con T(n)=n/2 per n pari e T(n)=(3n+1)/2 per n dispari, poniamo

\[
Q_v=(9^{2^v}-1)/2^{v+3},\quad
H_v=\lceil589\,2^v/612\rceil,\quad
J_v(r)=\#\{0\le i<r:T^i(Q_v)\text{ dispari}\}.
\]

Il bilancio del certificato precedente è B_v(r)=306r−589J_v(r).
La nuova passeggiata corretta è C_v(r)=B_v(r)−r=305r−589J_v(r).
Ogni passo pari guadagna 305 e ogni passo dispari perde 284.

**Ipotesi da mettere alla prova:** per ogni v≥15,

\[
\max_{0\le s\le t\le H_v}\bigl(C_v(s)-C_v(t)\bigr)\le128v^2.
\]

La massima caduta riguarda ogni coppia di prefissi, inclusi gli estremi.
I blocchi di 256 passi servono soltanto a descrivere i dati; non si escludono
le violazioni all'interno di un blocco. Non si richiede che ogni blocco
abbia bilancio positivo.

## Stato e significato della compensazione

Lo stato esatto al passo r contiene il residuo di T^r(Q_v) modulo
2^(H_v−r), la precisione residua H_v−r e un credito z_r. Fissato
D=128v², il credito parte da D e segue

\[
 z_0=D,\qquad z_{r+1}=\min(D,z_r+C_v(r+1)-C_v(r)).
\]

Non si tronca inferiormente a zero: un credito negativo è un fallimento.
Ponendo M_r=max_{s≤r}C_v(s), l'identità esatta è
z_r=D+C_v(r)−M_r. La candidata equivale quindi alla sopravvivenza del
credito per tutti i prefissi. La precisione diminuisce di un bit a ogni
passo; il solo residuo di un blocco non determina la sua continuazione.

Se il credito sopravvive, C_v(H_v)≥−D e B_v(H_v)≥H_v−D.
H_15=31537>28800=D(15), e H_v/v² cresce per v≥3: perciò la candidata
implicherebbe il certificato di discesa per tutti i v≥15. I livelli 5–14
dispongono già di certificati finiti separati.

## Scelta delle costanti e dati separati

La deriva 1 e la forma D(v)=a v² sono scelte esplorative. Il coefficiente
a è la più piccola potenza positiva di due che domina la massima caduta
divisa per v² nei livelli **10–21**. La calibrazione esatta dà a=128;
il massimo rapporto è 20576/169 al livello 13. La soglia v=15 è il
primo livello almeno 10 per cui H_v≥128v².

I livelli 22, 23, 24 sono esclusi dalla calibrazione e da qualsiasi scelta
successiva delle costanti. Una violazione resta una violazione anche se il
conteggio totale continua a certificare la discesa. Non si aumenta a dopo
aver osservato i nuovi dati all'interno di questo protocollo.

## Verifica e criteri di esito

Il produttore Python usa quadrature modulari e composizione affine
ricorsiva. Il verificatore C/GMP usa invece la ricorrenza quadratica di
Q_v e blocchi lineari fino a 32 passi. Si confrontano tutti i conteggi,
estremi, testimoni della massima caduta e hash delle parole di parità.

Per ciascun livello si conservano H, J, bilanci finali, massima caduta,
coppia testimone, credito minimo e primo istante di eventuale violazione.
I pareggi scelgono la coppia (s,t) lessicograficamente minima.

- Se un livello 22–24 viola il limite, la candidata congelata è confutata.
- Se tutti passano, si ottiene soltanto evidenza finita su casi non usati
  nella calibrazione. Non è una prova per tutti i livelli.
- Una prova uniforme deve mostrare la conservazione del credito sugli
  stati effettivamente raggiunti dalla famiglia, inclusi gli estremi.

Esiste già un ostacolo al tentativo generico: n=2^m−1 produce m passi
dispari consecutivi e una caduta 284m. Qualunque credito D fallisce per
m=floor(D/284)+1. Questi interi non sono identificati con stati della
famiglia Q_v; il controesempio esclude una prova basata su tutti i residui
indistintamente, non la candidata specifica qui proposta.

Non viene rivendicata originalità matematica per l'algebra del credito,
né una formalizzazione Lean della candidata.
