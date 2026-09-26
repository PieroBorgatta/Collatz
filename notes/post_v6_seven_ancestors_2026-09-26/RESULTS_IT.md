# Il filtro dei sette antenati non trasferisce il margine

**Esito:** l'implicazione proposta è falsa già al livello 11. Il
sessantesimo candidato nell'ordine congelato conserva tutti i filtri e
porta il margine da **+34 a −18**. Questo controesempio chiude il test;
non serve enumerare i restanti candidati per respingere l'implicazione.

Il test riguarda una classe di interi che approssima la torre. Non è un
controesempio a Collatz né alla torre effettiva: per \(Q_{11},Q_{12}\)
i margini restano **+73 e +93**. Non certifica nuovi livelli, non aggiunge
teoremi Lean e non rivendica originalità scientifica.

## Criterio e ricerca

Il [protocollo](PROTOCOL_IT.md) è stato scritto prima della nuova ricerca
di parità, con intervallo e cardinalità salvati separatamente nel
[calcolo preliminare](presearch_interval.json). È un congelamento locale,
non una preregistrazione pubblica con data certificata. Il suo SHA-256 è
`86f7882d65d1cd478fcf2b2429ad50484451ff03ee2e63903f021514f7a3b46e`.

Si è mantenuta senza modifiche la formula proposta: sette antenati prima
del livello inferiore, stessa binade della torre al livello superiore,
radice dispari e congruente a quella effettiva modulo un quarto della
precisione ternaria. Per \(v=11,u=4\), si richiedono

\[
x>0,\quad x\text{ dispari},\quad x\equiv Q_4\pmod{3^8},
\quad X=G_{4,7}(x),\quad Y=G_{4,8}(x),
\]

\[
2^{12969}\le Y<2^{12970},\qquad
\mu_{11}(X)\ge0\ \Longrightarrow\ \mu_{12}(Y)\ge0.
\]

Le definizioni di \(Q,f,G,H,\mu\) sono nel protocollo. Qui la parola
completa di parità di \(Q_{11}\) **non** è un'ipotesi.

Il precedente caso esplorativo al livello 10 aveva soltanto dodici
radici ammesse, tutte con margine superiore positivo. Il nuovo
intervallo è molto più ampio:

| Quantità | Valore esatto |
|---|---:|
| \(Q_4\) | 14.476.720.225.405 |
| Estremo inferiore \(L\) | 14.476.218.277.651 |
| Estremo superiore \(U\) | 14.515.467.287.088 |
| Passo \(2\cdot3^8\) | 13.122 |
| Primo parametro \(t\) | −38.252 |
| Ultimo parametro \(t\) | 2.952.832 |
| Primo candidato | 14.476.218.282.661 |
| Ultimo candidato | 14.515.467.286.909 |
| Numero di candidati | **2.991.085** |

Si enumerano \(x=Q_4+13122t\) per \(t\) crescente, compresi i valori
negativi. L'arresto era fissato al primo controesempio, oppure a 100000
candidati, oppure all'esaurimento. La ricerca si è fermata al primo di
questi eventi dopo 60 candidati: non è stata un'enumerazione completa.
L'ordine non è casuale e non autorizza stime sulla frequenza dei fallimenti.

## Certificato compatto del controesempio

\[
t=-38193,\qquad x=14476219056859,
\qquad a=1+128x,
\]

\[
X=\frac{a^{128}-1}{2^{14}},\qquad
Y=\frac{a^{256}-1}{2^{15}}=X+2^{13}X^2.
\]

| Quantità | Livello 11 | Livello 12 |
|---|---:|---:|
| Orizzonte \(H\) | 1.972 | 3.943 |
| Passi dispari \(J\) | 990 | 2.066 |
| Soglia \(2^{w-1}\) | 1.024 | 2.048 |
| Margine | **34** | **−18** |
| Margine della torre effettiva | 73 | 93 |

Il difetto di raddoppio è \(2066-2\cdot990=86\): l'identità dei margini
restituisce esattamente \(2\cdot34-86=-18\).

Nei primi 59 candidati non si verifica la coppia di disuguaglianze
richiesta per un controesempio. Tra i 60 visitati, 56 hanno margine
inferiore non negativo; soltanto l'ultimo ha margine superiore negativo.
La parola inferiore del testimone differisce da quella effettiva già
alla seconda parità: il vincolo fissato era sul conteggio totale.

Gli interi completi, tutte le parità dei due orizzonti del testimone e
della torre effettiva, gli hash delle parole dei 60 candidati e i margini
sono nel [risultato riproducibile](seven_results.json).
Le parole sono impacchettate a partire dal bit meno significativo, con
zeri di riempimento nell'ultimo byte.

## Perché sono soddisfatti tutti i filtri

Per \(w=4,\ldots,12\), gli antenati sono esplicitamente

\[
x_w=\frac{(1+128x)^{2^{w-4}}-1}{2^{w+3}}.
\]

Sono interi positivi dispari perché si ottengono anche applicando
successivamente \(f_w\), che preserva positività e disparità. Vale

\[
1+2^{w+3}x_w=(1+128x)^{2^{w-4}}.
\]

In generale, se \(x\equiv Q_4\pmod{3^8}\), allora \(3^8\) divide
\(1+128x\), poiché \(1+128Q_4=3^{32}\). Elevando alla potenza
\(2^{w-4}\) e confrontando con \(1+2^{w+3}Q_w=3^{2^{w+1}}\), segue

\[
x_w\equiv Q_w\pmod{3^{8\cdot2^{w-4}}}.
\]

Questi filtri ai vari livelli seguono tutti dalla congruenza della
radice: non sono condizioni indipendenti aggiuntive. Nel testimone la
valutazione effettiva è persino maggiore di quella richiesta:

| Livello \(w\) | Bit dell'intero | Precisione ternaria richiesta | \(\nu_3(x_w-Q_w)\) |
|---|---:|---:|---:|
| 4 | 44 | 8 | 9 |
| 5 | 94 | 16 | 18 |
| 6 | 194 | 32 | 36 |
| 7 | 396 | 64 | 72 |
| 8 | 801 | 128 | 144 |
| 9 | 1.612 | 256 | 288 |
| 10 | 3.234 | 512 | 576 |
| 11 | 6.479 | 1.024 | 1.152 |
| 12 | 12.970 | 2.048 | 2.304 |

Le lunghezze in bit coincidono con quelle di \(Q_w\). Per interi positivi di binade
\(B\), la binade di \(f_w(x)\) è \(w+2+2B\) oppure \(w+3+2B\).
Il limite superiore usa \(x\le2^{B+1}-1\), non soltanto la disuguaglianza
reale stretta. Di conseguenza la binade successiva determina quella
precedente tramite \(B=\lfloor(B_{next}-w-2)/2\rfloor\).
La binade finale corretta forza quindi tutte le binadi intermedie.

La formula chiusa di \(G\) è strettamente crescente. Le quattro verifiche
esatte \(G(L-1)<2^{12969}\le G(L)\) e
\(G(U)<2^{12970}\le G(U+1)\) certificano le frontiere dell'intervallo.
Il numero delle radici congruenti segue poi da una progressione aritmetica.

## Verifica e limiti della conclusione

La ricerca riusa il motore modulare congelato. Un'implementazione
separata nei test ricostruisce gli interi dalla formula chiusa e itera
direttamente \(T\): controlla le parole complete dei 60 candidati, il
primo fallimento, gli estremi dell'intervallo, tutti i filtri e il caso
storico con dodici radici. La revisione matematica interna ricontrolla
separatamente anche tutti i 60 candidati e i quantificatori; non è una
revisione esterna. Gli **11 test** passano localmente e il JSON viene
riprodotto identico byte per byte.

La [CI del filtro](https://github.com/PieroBorgatta/Collatz/actions/runs/36234177020)
e la [build Lean con gli audit esistenti](https://github.com/PieroBorgatta/Collatz/actions/runs/36234177017)
sono passate sul commit `d4b35bc`. Gli 11 test passano anche in Linux e
il JSON scaricato coincide byte per byte con quello locale. La CI
riesegue il codice archiviato: non è un ulteriore metodo indipendente.
I nuovi argomenti su carta non sono formalizzati dalla build Lean.
Log e SHA-256 sono nel [manifesto](verification_manifest.json).
Verificati e invariati i 121 hash degli input delle nove fasi
precedenti, esclusi i loro README storici; invariati gli artifact v6.

La conclusione è circoscritta e definitiva: **questa formula universale
per il trasferimento del margine è falsa**. Non segue che ogni criterio
con sette antenati fallisca, né che fallisca il diverso bilancio pesato
proposto a partire dal livello 16. Il lemma precedente con due antenati,
altezza corretta e parola inferiore effettiva completa resta compatibile:
il testimone non soddisfa quest'ultima ipotesi.

Non propongo di aumentare subito la profondità o spostare la soglia dopo
questo fallimento. Il test ha mostrato che questi filtri ammettono una
sorgente con comportamento diverso da \(Q_v\). Per riaprire una via
positiva serve un argomento sul dato esatto
\(1+2^{v+3}Q_v=3^{2^{v+1}}\), o un'altra condizione motivata prima delle
nuove osservazioni che produca un bilancio uniforme dimostrabile.
Al momento quel bilancio resta aperto.
