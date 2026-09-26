# Riporti binari della torre: generatore esatto e limiti dello stato breve

**26 settembre 2026. Esito:** il generatore per quadrati successivi dal
seme 3 riproduce esattamente le sorgenti e le parità controllate. I
riporti delle colonne già esposte sono però ridondanti rispetto al
prefisso completo. Conservare soltanto il riporto corrente e finestre
brevi non dà un trasduttore deterministico sugli input ancorati generali.
Un riporto futuro esercita una selezione reale nei test finiti, ma non
fornisce ancora una maggiorazione uniforme dei conteggi della torre.

Il [protocollo](PROTOCOL_IT.md) fissa un esperimento piccolo, senza
estendere i livelli storici. La scelta del candidato ha beneficiato di
analisi matematica e di un sondaggio interno preliminare: non si tratta
di una preregistrazione cieca o pubblica. Le [prove](PROOF_IT.md) sono
su carta; il programma Python e i suoi test non sono nuove prove Lean.

## 1. Uno stato che genera davvero la sorgente esatta

Poniamo `R_0=3`, `R_(a+1)=R_a²` e `b_(a,n)=bit_n(R_a)`. In ogni
colonna si calcolano

```
d_(a,n) = sum_{i=0}^n b_(a,i)*b_(a,n-i)
b_(a+1,n) = (C_(a,n)+d_(a,n)) mod 2
C_(a,n+1) = floor((C_(a,n)+d_(a,n))/2).
```

Il seme e questa ricorrenza producono `R_a=3^(2^a)`, quindi
`Q_v=(R_(v+1)-1)/2^(v+3)`. I bit della sorgente alimentano il
trasduttore delle code già studiato, agli orizzonti esatti `H_v` e
`H_(v+1)`. La scansione conserva i prefissi delle righe: non comprime
la storia in un numero fisso di bit e non produce un nuovo limite
sul peso delle parità.

Sono state controllate le **cinque coppie `v=5..9`**, corrispondenti
ai livelli storici `5..10`. Tutte le colonne di ogni riga coincidono
con l'esponenziazione modulare; tutti i coefficienti e i riporti sono
verificati anche con una moltiplicazione in radix impacchettato. Le
parità del trasduttore coincidono con l'iterazione diretta degli interi
e con gli hash congelati della fase dei margini. Nell'ultima coppia
sono generate 999 colonne e conservati 11.988 bit di righe, oltre ai
riporti e alle code. Questo conteggio descrive l'implementazione scelta,
non un limite inferiore per ogni algoritmo sulla torre.

## 2. I riporti esposti non escludono i vecchi completamenti

Per un input `P` con bit `b_i`, il riporto alla frontiera `N` è

\[
C_N(P)=\left\lfloor
2^{-N}\sum_{i+j<N}b_i b_j2^{i+j}
\right\rfloor.
\]

Dipende soltanto da `P mod2^N`. In particolare, se
`P=1+2^rX`, `P_actual=1+2^rQ_v` e `M=nu2(X-Q_v)`, sono uguali
tutti i riporti attraverso la frontiera `n=r+M`. Il primo riporto
diverso, `C_(n+1)`, differisce esattamente di uno. I quadrati hanno
la prima uscita diversa alla colonna `n+1`; lo shift nella definizione
della sorgente superiore riporta la differenza alla posizione `M`.

È quanto verificato per **tutti gli otto testimoni di soglia del rinnovo
e per quello dei sette antenati**. I riporti esposti non eliminano
nessuno di questi nove testimoni. Non si afferma che essi soddisfino
l'intera cascata dal seme esatto 3: sono completamenti alternativi del
prefisso, non punti della torre.

## 3. La compressione non è chiusa sul dominio generale

Lo stato candidato conserva colonna, livello, riporto corrente,
ancoraggio basso, ultime `w` cifre d'ingresso e d'uscita. Si fornisce
anche il bit corrente d'ingresso, per evitare che la collisione sia
soltanto effetto di un bit nuovo mancante.

L'enumerazione fissata controlla **80 casi** di livello, colonna e
finestra, con 952 righe d'ingresso e 3.720 proiezioni. In **13 casi**
trova due input con lo stesso stato e un'uscita successiva diversa.
Un esempio con quattro bit di finestra è:

| Dato alla colonna 12 | `P=105` | `P=153` |
|---|---:|---:|
| Radice dispari `X=(P-1)/8` | 13 | 19 |
| Ancoraggio `P mod16` | 9 | 9 |
| Riporto corrente | 1 | 1 |
| Ultimi quattro bit d'ingresso, impacchettati | 0 | 0 |
| Ultimi quattro bit del quadrato, impacchettati | 11 | 11 |
| Bit corrente d'ingresso | 0 | 0 |
| **Bit corrente del quadrato** | **0** | **1** |

La prova dà anche una collisione per **ogni** finestra finita `w`, con
input positivi dispari ancorati, stessa binade e stessi bit alti. La
ragione è che il coefficiente del quadrato modulo due contiene il bit
remoto `b_(n/2)` quando `n` è pari. Le finestre e il riporto corrente
non lo ricostruiscono in generale.

Questo arresta il tentativo di usare quello stato come trasduttore
deterministico su tutti gli input ancorati. Non esclude una previsione
specifica delle potenze esatte di 3, un'astrazione con più uscite o un
bilancio aggregato con costi d'errore. Non è un ciclo di Collatz.

## 4. Un riporto futuro seleziona, ma deve essere giustificato

Il controllo successivo usa un dato ulteriore: alla colonna
`r+K`, con `K=H_(v+1)`, richiede che il riporto del quadrato coincida
con quello della sorgente effettiva. Si enumerano tutti i completamenti
fra `H_v` e `K`, mantenendo i bit inferiori e quelli da `K` in su.
La distribuzione completa dei difetti è nel [JSON](binary_carry_results.json).

| Livello diagnostico | Candidati | Con riporto futuro uguale | Massimo `Delta` prima | Massimo dopo | `Delta` effettivo |
|---:|---:|---:|---:|---:|---:|
| 0 | 2 | 1 | 0 | −1 | −1 |
| 1 | 4 | 2 | 1 | 1 | 0 |
| 2 | 16 | 8 | 2 | 1 | −1 |
| 3 | 256 | 108 | 7 | 6 | 4 |
| 4 | 32.768 | 3.506 | 1 | 0 | −6 |

Sono **33.046 completamenti** enumerati esaustivamente. Questi livelli
sono inferiori al dominio `v≥5` dei certificati del progetto: servono
come diagnostica, non come prova della loro discesa. Dove i bit alti non
fissano una binade, non viene aggiunta un'ipotesi di altezza.

Il medesimo filtro respinge tutti e nove i controesempi archiviati nel
controllo aggiuntivo. È un risultato di selezione finito, distinto dalla
ridondanza dei riporti già esposti. Non significa che elimini ogni
completamento sfavorevole. Né il valore futuro del riporto né una stima
del suo costo vengono ricavati gratuitamente dal prefisso inferiore.

## 5. Bilancio e decisione

La contabilità firmata dei dati congelati parte da `m_16=1155`.
Fino alla coppia `23→24`, la perdita pesata cumulativa è
`−4339/64`: gli errori negativi forniscono un recupero netto. È una
verifica esatta del telescopio storico, non una maggiorazione dei
termini futuri. Dimostrare per tutte le lunghezze

\[
\sum_{i<N}\frac{\Delta_{16+i}}{2^{i+1}}\le1155
\]

resta equivalente alla nonnegatività dei margini successivi, finché
non si ricava un limite indipendente dall'aritmetica della sorgente.

**Decisione:** il modello breve di riporto e finestre viene chiuso sul
dominio generale. Il generatore esatto rimane uno strumento verificato
per formulare vincoli, ma il passo positivo non è stato ottenuto.
La selettività del riporto futuro offre un candidato più preciso per
un'eventuale ricerca successiva: occorrerebbe prima una disuguaglianza
sul peso delle parole nel suo insieme di completamenti, con un costo
giustificato dalla generazione esatta. La sola tabella qui ottenuta non
autorizza una legge uniforme o l'estensione al livello 25.

## Riproduzione e verifica

Dalla radice del repository:

```sh
python3 notes/post_v6_binary_carries_2026-09-26/test_binary_carries.py
python3 notes/post_v6_binary_carries_2026-09-26/binary_carry_probe.py --output /tmp/binary_carry_results.json
cmp notes/post_v6_binary_carries_2026-09-26/binary_carry_results.json /tmp/binary_carry_results.json
```

I test usano prodotti scolastici con cicli separati, moltiplicazioni
intere e iterazione diretta shortcut come controlli delle nuove formule.
I grandi coefficienti dei testimoni sono ricostruiti anche con un
secondo impacchettamento in radix: è la stessa idea matematica di
convoluzione, non un metodo indipendente per una stima analitica.
Il [manifesto](verification_manifest.json) registra input, hash e log
locali; la [revisione](REVIEW_IT.md) è interna agli agenti. Il workflow
CI è predisposto, ma questa fase non rivendica una nuova esecuzione CI,
una build Lean o una revisione umana esterna.
