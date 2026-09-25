# Trasduttore delle code: bilancio esatto e precisione necessaria

**25 settembre 2026.** Il confronto fra le due orbite è ora verificato
agli orizzonti completi richiesti, mediante le sole code ternarie.
Abbiamo anche caratterizzato esattamente la precisione necessaria per
prevedere un blocco di parità. La cancellazione cumulativa cercata resta
da maggiorare: l'identità che la esprime non è ancora una stima.
Le dimostrazioni sono su carta, con verifiche finite indipendenti;
non aggiungono teoremi Lean e non stabiliscono originalità in letteratura.

## Il bilancio agli orizzonti giusti

Scriviamo `T^t(n)=3^(j_t)floor(n/2^t)+z_t`, con `0≤z_t<3^(j_t)`.
La coda ha `j_t` cifre ternarie, compresi gli zeri iniziali.
Il trasduttore riceve `h_t=bit_t(n)` e produce
`p_t=(h_t+z_t) mod2`. Se `S_t` è la somma delle cifre della coda e
`A_t` il numero dei suoi riporti uscenti uguali a uno, allora

\[
 2S_{t+1}=S_t+p_t+3h_t+2A_t,
 \qquad
 J_n(T)=2S_T+\sum_{t=1}^{T-1}S_t-3\sum_{t<T}h_t-2\sum_{t<T}A_t.
\]

La [nota delle identità](TAIL_IDENTITIES_IT.md) dimostra queste formule,
il telescopio pesato e gli estremi ottimali della coda normalizzata.
Il termine `3h_t` è indispensabile: la coda riceve un riporto dal
prefisso originario, anche quando quel prefisso è già stato eliminato
dalla rappresentazione operativa.

Per `r=v+3`, `m=2^(v+1)` e `H_v=ceil(589·2^v/612)`, gli input sono
`Q_v` e `WW=2Q_(v+1)`. I tempi effettivi sono rispettivamente
`H_v` e `2H_v+r`. Il difetto così calcolato soddisfa

\[
 E_v=\Delta_v+K_v,\qquad 0\le K_v\le v+2+\varepsilon_v,
 \quad\varepsilon_v=2H_v-H_{v+1}\in\{0,1\}.
\]

`K_v` conta i dispari realmente incontrati nel tratto superiore
aggiuntivo. La tabella riporta un replay di livelli già studiati.

| `v` | Tempo inferiore | Tempo superiore | `Δ_v` | `K_v` | `E_v` |
|---:|---:|---:|---:|---:|---:|
| 5 | 31 | 70 | 6 | 3 | 9 |
| 6 | 62 | 133 | −2 | 5 | 3 |
| 7 | 124 | 258 | −12 | 4 | −8 |
| 8 | 247 | 505 | 28 | 5 | 33 |
| 9 | 493 | 998 | −53 | 7 | −46 |
| 10 | 986 | 1985 | −15 | 8 | −7 |
| 11 | 1972 | 3958 | 53 | 5 | 58 |
| 12 | 3943 | 7901 | 99 | 11 | 110 |

Per `v=12`, il bilancio separa quattro termini esatti:

\[
 \underbrace{128}_{\text{masse finali}}
 +\underbrace{8231992}_{\text{masse interne}}
 \underbrace{-354}_{\text{bit degli input}}
 \underbrace{-8231656}_{\text{riporti}}=110.
\]

La somma dei valori assoluti è `16.464.130`. Una maggiorazione separata
dei termini perderebbe la cancellazione. Neppure la cancellazione
osservata basta a provare un limite uniforme: l'input generico di soli
uno presenta una cancellazione quadratica esatta e produce soltanto
parità dispari. Serve una disuguaglianza specifica per la torre.

## Un criterio esatto per la memoria

La [nota sulla memoria](MEMORY_OBSTRUCTION_IT.md) dimostra due risultati
complementari.

1. A contatore `j≥1` fissato, le code raggiungibili sono precisamente
   le `2·3^(j−1)` unità modulo `3^j`. Si possono raggiungere tutte allo
   stesso tempo. Una continuazione comune di soli zeri le distingue:
   un trasduttore generico esatto non può comprimerle in un numero
   uniforme finito di stati.
2. Per un orizzonte finito `k` e contatore iniziale `j` noto, due code
   hanno le stesse prossime `k` parità per **ogni** continuazione comune
   se e solo se sono congruenti modulo `2^k`. Questa è anche una
   costruzione utilizzabile: bastano quel residuo e i prossimi `k` bit
   d'ingresso. La precisione residua scende da `k` a `k−1` a ogni passo.

Il [codice](tail_probe.py) implementa questa previsione a blocchi e la
confronta con l'evoluzione completa. All'inizio di ciascun blocco il
residuo viene letto dallo stato esatto: il programma **non** risolve
il problema del rinnovo della precisione con memoria limitata.

Anche la contrazione reale della coda normalizzata è dimostrata, ma
code distanti solo `3^(−j)` possono avere la prossima parità opposta.
Inoltre un potenziale universale limitato inferiormente non può
certificare densità di dispari minore di uno: l'input di soli uno
lo costringerebbe a perdere un importo lineare senza limite.
Queste ostruzioni valgono per ingressi generici, non escludono un
controllo aggregato né una proprietà selettiva della torre.

## Rapporto con la letteratura

La lettura mediante trasduttori e conversioni fra basi ha un precedente
diretto in [Stérin–Woods, versione del 27 febbraio 2022](https://arxiv.org/html/2007.06979v4):
il loro automa contiene la divisione ternaria e dimostra una conversione
di base, insieme a limiti di complessità per specifici problemi di
previsione. Le nostre code usano cifre ternarie ordinarie e un diverso
modello di memoria; il limite sugli stati qui dimostrato non va
identificato con il loro risultato `NC¹`/`AC⁰`. La biezione fra residui
binari e parole di parità appartiene alla codifica classica del processo.
Non presentiamo quindi il trasduttore o i lemmi elementari come una
nuova scoperta di priorità accertata.

La [ricerca sulle somme modulari della fase precedente](../post_v6_propagation_2026-09-25/LITERATURE_IT.md)
resta pertinente ai prefissi originali. Non fornisce automaticamente
un controllo sulle code adattive o sul rinnovo di precisione.

## Verifica riproducibile

Il [probe](tail_probe.py) esegue **23.666 passi** sulle otto coppie,
scansiona **25.980.961 cifre di coda** e verifica **1.487 blocchi**
di al massimo 16 passi. A ogni passo confronta le parità prodotte
dalla coda intera, dalla scansione ternaria e dall'orbita intera diretta;
verifica inoltre il bilancio locale e la decomposizione del quoziente.
Il valore intero delle cifre di coda viene confrontato al termine di
ciascuna corsa. La previsione modulare a blocchi è un controllo ulteriore,
alimentato dallo stato esatto ai confini dei blocchi.

Tutti i conteggi e gli hash delle parole complete di parità agli
orizzonti `H_v` e `H_(v+1)` coincidono con il risultato congelato della
fase dei margini. Gli hash delle code e dei ledger sono inclusi nel
[JSON deterministico](tail_results.json); il ledger è una sequenza di
righe JSON compatte `[h,p,j_prima,S_prima,A,S_dopo]`, ciascuna con newline.
I valori `Δ_v,E_v,K_v` e le durate aggiuntive coincidono anche con la
precedente produzione C sulle parole ternarie complete.

I [14 test](test_tail.py) comprendono 1.649 replay con un oracolo intero,
tutte le parole ternarie fino a sei cifre, estremi affini fino a nove
passi, costruzioni sincronizzate delle code raggiungibili, distinguibilità
e 1.701 casi di previsione a precisione finita. Gli esempi nel JSON
controllano separatamente tutte le unità fino a `j=7`.

Dalla radice del repository:

```sh
python3 notes/post_v6_tail_2026-09-25/test_tail.py
python3 notes/post_v6_tail_2026-09-25/tail_probe.py --output /tmp/tail_results.json
cmp notes/post_v6_tail_2026-09-25/tail_results.json /tmp/tail_results.json
```

Il [workflow dedicato](../../.github/workflows/tower-tail.yml) ripete
test e generazione del JSON. L'evidenza della CI verrà archiviata dopo
il push del codice. La build Lean esistente riguarda i moduli già
formalizzati, non queste prove su carta.

## Conseguenza per il progetto

Il raccordo dei tempi e la descrizione delle code sono esatti. È aperta
la maggiorazione del difetto cumulativo `Δ_v`, e quindi la discesa
uniforme della famiglia. Non sono stati aggiunti nuovi livelli della
torre né nuove dichiarazioni Lean. La [direzione successiva](NEXT_RESEARCH_IT.md)
è un certificato con precisione controllata e cancellazione fra le
due code, con una condizione esplicita per evitare ragionamenti circolari.
