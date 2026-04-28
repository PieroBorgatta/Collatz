# Collatz/Syracuse

## Teoria del Debito Gravitazionale, Famiglie di Confluenza e Quasi-Lyapunov Collatziana

Questo repository raccoglie esperimenti computazionali e note teoriche sulla dinamica della mappa accelerata di Syracuse, collegata alla Congettura di Collatz.

L'obiettivo non e dichiarare risolta la congettura, ma proporre un quadro strutturale per descrivere perche alcune orbite sembrano crescere violentemente prima di rientrare verso 1.

La formulazione sintetica del programma e:

```text
Collatz come dinamica di corridoi 2-adici espansivi
che confluiscono in tronchi dissipativi.
```

## Idea Centrale

La dinamica viene interpretata come una competizione tra:

- espansione prodotta dal fattore `3n + 1`;
- dissipazione prodotta dalle divisioni per potenze di 2;
- corridoi 2-adici con alta densita di `v2 = 1`;
- confluenza delle orbite in tronchi comuni;
- scarico del debito tramite tronchi dissipativi;
- una funzione empirica quasi-Lyapunov capace di riconoscere discese locali ingannevoli.

La funzione candidata finale e:

```text
H(n) = log(n) + 0.28 D_max,80(n) - 0.03 C_max,80(n) + 0.30 P_max,80(n)
```

Dove:

- `D_max,80` misura il massimo debito espansivo futuro;
- `C_max,80` misura la massima cascata dissipativa futura;
- `P_max,80` misura la massima pressione futura del corridoio `v2 = 1`.

## Mappa Accelerata di Syracuse

La funzione Collatz classica e:

```text
C(n) = n / 2      se n e pari
C(n) = 3n + 1    se n e dispari
```

Per studiare solo i dispari si usa la mappa accelerata:

```text
S(n) = (3n + 1) / 2^v2(3n + 1)
```

Un passo Syracuse e quindi determinato dal valore:

```text
a_k = v2(3n_k + 1)
```

Il valore `a_k` misura quanta dissipazione viene prodotta nel passo.

## Soglia Critica

Approssimativamente:

```text
S(n) ~= n * 3 / 2^a
```

La variazione logaritmica e dominata da:

```text
log(3) - a log(2)
```

La soglia critica e:

```text
log2(3) ~= 1.5849625
```

Se la media degli `a_k` lungo un tratto orbitale e maggiore di questa soglia, il tratto e dissipativo. Se e minore, il tratto e espansivo.

## Debito Gravitazionale

Il debito gravitazionale dopo `k` passi Syracuse e definito come:

```text
D(k) = k log2(3) - sum(a_i, i = 1..k)
```

Interpretazione:

- `D(k) > 0`: l'orbita ha accumulato vantaggio espansivo;
- `D(k) < 0`: la dissipazione ha dominato;
- `max D(k)`: misura quanto l'orbita riesce a resistere alla caduta.

In forma fisica:

```text
debito = espansione attesa - divisioni per 2 accumulate
```

Il debito e la quantita che un tronco dissipativo dovra poi scaricare.

## Corridoi 2-Adici Espansivi

Le sequenze dei valori `a_k = v2(3n_k + 1)` non sono libere.

Una lunga sequenza di valori:

```text
1, 1, 1, ...
```

impone che il numero iniziale cada in classi residue 2-adiche sempre piu strette.

Per esempio:

```text
v2(3n + 1) = 1
```

equivale a:

```text
n == 3 mod 4
```

Per una sequenza lunga di soli `1`, i rappresentanti minimi seguono:

```text
3, 7, 15, 31, 63, 127, ...
```

cioe:

```text
2^(k + 1) - 1
```

Quindi i corridoi piu espansivi si avvicinano a `-1` in senso 2-adico.

## Caso Estremo: n = 3.041.127

Uno dei numeri piu esplosivi trovati sotto 5 milioni e:

```text
n = 3.041.127
```

Risultati principali:

- picco massimo: `207.572.633.873`;
- rapporto massimo rispetto allo start: circa `68.255`;
- step del picco: `36`;
- primo rientro sotto lo start: `62`;
- salti Syracuse fino a 1: `132`;
- massima sequenza consecutiva di `v2 = 1`: `17`;
- media finale `v2`: `1,75`.

Poiche:

```text
1,75 > log2(3)
```

la traiettoria, pur essendo inizialmente esplosiva, e complessivamente dissipativa.

La struttura tipica e:

```text
fase espansiva -> debito -> cascata dissipativa -> 1
```

## Autostrada Gravitazionale Comune

Tra i numeri con massimo debito sotto 5 milioni e emersa una famiglia principale di confluenza.

Il tronco comune massimo e:

```text
8.216.025.965
```

Questa famiglia contiene:

- 62 membri;
- 78 nodi comuni;
- minimo nodo comune del tronco: `428.885`;
- media `v2` del tronco: `2,111111`;
- surplus per step: `0,526149`;
- dissipativo da subito: si.

Il tronco da `8.216.025.965` a `1` ha:

- 63 salti Syracuse;
- `v2` totale: `133`;
- media `v2`: `2,111111`;
- surplus finale: `+33,147362`;
- massimo debito del tronco: `0`.

La caduta piu violenta osservata nel tronco e:

```text
428.885 -> 2.513
```

con:

```text
v2 = 9
```

Questo tronco non accumula debito: lo scarica.

## Albero Inverso del Tronco

La mappa inversa di Syracuse e:

```text
S(n) = m
(3n + 1) / 2^a = m
n = (m * 2^a - 1) / 3
```

purché `n` sia intero, positivo e dispari.

Costruendo l'albero inverso del nodo `8.216.025.965`, con ricerca fino al valore del root e target sotto 5 milioni, si ottiene:

- nodi totali generati: `116.129`;
- nodi sotto 5 milioni: `133`;
- membri top-debito attesi: `62`;
- membri trovati: `62`;
- membri mancanti: `0`;
- extra sotto 5 milioni: `71`.

Quindi i 62 numeri ribelli non sono casuali: sono un sottoinsieme dei predecessori sotto 5 milioni del tronco dissipativo.

## Famiglie di Confluenza

Dall'analisi delle confluenze alte sono stati ottenuti:

- 6.670 nodi di confluenza;
- 344 famiglie distinte.

Sulle 344 famiglie:

- famiglie dissipative da subito: `77`;
- percentuale dissipative da subito: `22,38%`;
- media membri: `6,979651`;
- media nodi comuni: `19,389535`;
- media `v2` dei tronchi: `1,847881`;
- media surplus finale: `+24,010594`.

Poiche:

```text
1,847881 > 1,5849625
```

le famiglie di confluenza sono mediamente dissipative.

## Tipi Strutturali

Le famiglie osservate sono state classificate in categorie:

- Tipo A: autostrade larghe, con molti membri e molti nodi comuni;
- Tipo B: confluenze larghe ma corte;
- Tipo C: tronchi alti, con massimo comune superiore a `10^10`;
- Tipo C2: tronchi estremi, con massimo comune superiore a `10^11`;
- Tipo D: ultra dissipativi, con surplus per step molto alto;
- Tipo F: misti, non dissipativi da subito ma con surplus finale positivo.

La struttura osservata e:

```text
corridoi 2-adici espansivi
-> accumulo di debito
-> confluenza
-> tronchi dissipativi
-> 1
```

## Quasi-Lyapunov Collatziana

La sola funzione:

```text
V(n) = log(n)
```

vede quando un'orbita scende localmente sotto il valore iniziale.

Ma questa discesa puo essere ingannevole: alcuni numeri scendono subito sotto lo start e poi entrano in un corridoio fortemente espansivo.

Per questo e stata introdotta la funzione corretta:

```text
H(n) = log(n) + lambda D_max,80(n) - mu C_max,80(n) + theta P_max,80(n)
```

La candidata empirica finale e:

```text
H(n) = log(n) + 0.28 D_max,80(n) - 0.03 C_max,80(n) + 0.30 P_max,80(n)
```

Interpretazione dei termini:

| Termine | Ruolo |
|---|---|
| `log(n)` | quota/potenziale locale |
| `D_max,80` | debito espansivo futuro |
| `C_max,80` | cascata dissipativa futura |
| `P_max,80` | pressione del corridoio `v2 = 1` |

Questa funzione non misura solo se un numero e sceso. Misura se e davvero uscito dalla zona espansiva.

## Validazione Empirica

Sul range dei dispari fino a 5.000.000:

- peggioramenti totali: `76`;
- veri ribelli: `59`;
- veri ribelli estremi: `14`;
- falsi allarmi: `3`.

Quindi 73 peggioramenti su 76 risultano strutturalmente significativi.

Sul range dei dispari fino a 20.000.000:

- dispari analizzati: `9.999.999`;
- improved: `1.592.944`;
- worsened: `408`;
- same: `8.406.647`;
- avg log step: `3,491526`;
- avg H step: `3,141184`;
- max log step: `181`;
- max H step: `176`;
- worst loss: `133` su `n = 12.826.025`;
- best gain: `80` su `n = 9.138.203`.

Classificazione dei 408 peggioramenti:

- vero ribelle: `297`;
- vero ribelle estremo: `64`;
- intermedio: `27`;
- falso allarme: `20`.

Quindi 361 peggioramenti su 408 sono veri ribelli o ribelli estremi.

## Casi Notevoli fino a 20 Milioni

Peggior loss osservato:

```text
n = 12.826.025
```

con:

- log_step = `1`;
- H_step = `134`;
- loss = `133`;
- max_ratio = `2345,210`;
- ratio `v2 = 1` = `0,679104`;
- `P_max` al log-step = `1,000000`.

Il log puro vede una discesa immediata, ma `H` riconosce che la traiettoria e ancora dentro un corridoio espansivo.

Massima espansione osservata tra i peggioramenti:

```text
n = 16.098.751
```

con:

- max_ratio = `197.430,845`;
- loss = `77`;
- ratio `v2 = 1` = `0,709677`;
- `P_max` al log-step = `1,000000`;
- `D_max` cresce di `+7,300750`.

## Perche Non e una Dimostrazione

Questa costruzione non dimostra la Congettura di Collatz.

I motivi principali sono:

- la funzione usa un lookahead finito di 80 passi;
- i coefficienti sono empirici;
- non e ancora dimostrato che ogni orbita abbia un blocco futuro in cui `H` decresce;
- non e esclusa formalmente l'esistenza di un'orbita infinita che mantenga alto `D_max` e `P_max` senza mai entrare in una cascata dissipativa sufficiente.

## Programma di Ricerca

Per trasformare questi risultati in una dimostrazione servirebbe provare almeno una delle seguenti affermazioni:

- ogni corridoio espansivo e finito;
- il debito gravitazionale e limitato;
- ogni ramo espansivo deve prima o poi entrare in una famiglia di confluenza;
- ogni famiglia sufficientemente profonda possiede un tronco con media `v2` superiore a `log2(3)`;
- esiste una funzione di Lyapunov 2-adica formale.

La domanda teorica centrale diventa:

```text
una pressione espansiva alta implica inevitabilmente
una futura cascata dissipativa sufficiente a compensare il debito?
```

## File nel Repository

- `01.py` - `37.py`: script sperimentali progressivi.
- `Spiegazione Attuale/`: report aggiornati da cui questo README e stato ricavato.
- `Spiegazione V1/`: versione precedente dei report.

I file CSV sono esclusi dal repository Git e restano solo locali, per evitare di pubblicare dataset pesanti o generati.

## Sintesi Finale

La ricerca suggerisce una struttura non casuale:

1. le salite sono prodotte da corridoi con alta densita di `v2 = 1`;
2. questi corridoi sono 2-adicamente sottili;
3. le orbite ribelli accumulano debito gravitazionale;
4. i rami ribelli confluiscono in famiglie comuni;
5. molte famiglie hanno tronchi dissipativi;
6. le famiglie alte ed estreme sono spesso dissipative da subito;
7. la funzione quasi-Lyapunov `H` riconosce molte discese locali ingannevoli;
8. i peggioramenti di `H` corrispondono quasi sempre a traiettorie realmente instabili;
9. il comportamento suggerisce una rete gerarchica di attrazione verso 1.

Questa non e ancora una dimostrazione, ma e una struttura teorica coerente su cui provare a costruire una funzione di Lyapunov formale.
