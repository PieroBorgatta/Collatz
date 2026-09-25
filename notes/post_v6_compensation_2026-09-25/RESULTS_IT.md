# Una candidata di compensazione e tre livelli tenuti separati

25 settembre 2026. Continuazione del
[trasferimento condizionale](../post_v6_induction_2026-09-25/RESULTS_IT.md).

**Risultato:** una condizione sulla massima perdita intermedia, scelta
usando soltanto i livelli 10–21, supera i nuovi livelli 22, 23, 24.
Due implementazioni indipendenti concordano su ogni parola di parità
tramite hash, oltre che su conteggi, estremi e testimoni. La proprietà
uniforme resta congetturale. Un argomento esatto delimita inoltre il
tentativo di provarla usando soltanto residui e altezza.

Il [protocollo](PROTOCOL_IT.md) e i relativi
[hash](frozen_protocol.json) sono stati pubblicati nel commit
[`24e3569`](https://github.com/PieroBorgatta/Collatz/commit/24e35698a6cc104ac686b84a3f791e1f0341c617)
prima di calcolare i livelli 22–24. Formula, coefficiente, dominio e
verificatore sono rimasti invariati.

La [CI sperimentale 36122256203](https://github.com/PieroBorgatta/Collatz/actions/runs/36122256203)
ha superato tutti i quindici test e riprodotto calibrazione, nuovi livelli
e replay indipendenti. I quattro JSON scaricati coincidono byte per byte
con quelli locali. Sono passati anche build e audit Lean esistenti nella
[CI 36122256120](https://github.com/PieroBorgatta/Collatz/actions/runs/36122256120).
Entrambe riguardano il commit di codice
`df44e7f4daf79af2d56c3d8a35be2a3d3d8384fe`.
Il [manifest](verification_manifest.json) e i log archiviati conservano
l'evidenza. Le modifiche successive riguardano soltanto documentazione
ed evidenza, e il controllo Lean esistente non dimostra la nuova candidata.

## 1. La condizione messa alla prova

Siano T la mappa Collatz con una divisione per passo,
Q_v=(9^(2^v)−1)/2^(v+3),
H_v=ceil(589·2^v/612), e J_v(r) il numero di passi dispari fra i primi r.
La soglia originale è N_v=(2^(3·2^v−5)−11)/3; la mappa Syracuse sui
dispari è S(n)=(3n+1)/2^ν₂(3n+1).
Il bilancio del certificato diretto è B_v(r)=306r−589J_v(r).
Definiamo la passeggiata corretta

\[
 C_v(r)=B_v(r)-r=305r-589J_v(r).
\]

La candidata congelata è

\[
 \boxed{\quad
 \max_{0\le s\le t\le H_v}(C_v(s)-C_v(t))\le128v^2
 \quad\text{per ogni }v\ge15.\quad}
\]

Controlla tutte le perdite da un massimo precedente a un prefisso successivo,
non solo il bilancio finale. Il coefficiente 128 è la minima potenza di due
che supera tutti i rapporti osservati nei livelli 10–21; il massimo della
calibrazione è 20576/169 al livello 13. Questa scelta è empirica.

## 2. Perché basterebbe, e cosa ancora manca

Con D=128v², il credito saturo z_0=D,
z_(r+1)=min(D,z_r+C_v(r+1)−C_v(r)) soddisfa esattamente

\[
 z_r=D+C_v(r)-\max_{s\le r}C_v(s).
\]

La candidata equivale alla non negatività del credito a ogni passo.
Se vale, B_v(H_v)≥H_v−D. Abbiamo H_15=31537>D(15)=28800;
H_v/v² è crescente per v≥3, quindi H_v≥D per ogni v≥15.

Per completezza, H_(v+1)≥2H_v−1. Il rapporto cresce se
H_v(v²−2v−1)>v²; per v≥3 questo segue da H_v≥8 e
v²−2v−1≥2v²/9. Qui la formula di H si estende aritmeticamente a v≥3.

L'arrotondamento non lascia ambiguità: posto K=2^(v−1),
0≤306H_v−589K<306<589. Perciò B_v(H_v)≥0 equivale esattamente
a J_v(H_v)≤K, la premessa del precedente certificato modulare.
I livelli 5–14 hanno già certificati finiti separati.

Questa è la dimostrazione dell'**implicazione sufficiente**, non della
candidata. Manca una proprietà aritmetica che preservi il credito sugli
stati effettivamente raggiunti da tutti i Q_v. Lo stato modulare esatto
deve conservare anche la precisione residua: un bit viene consumato a ogni
passo. Una sequenza osservata di crediti positivi non dimostra questa
conservazione per livelli arbitrari.

## 3. Risultati sui livelli non usati nella calibrazione

| v | H_v | Passi dispari J | Massima perdita C | Limite 128v² | Credito minimo |
|---:|---:|---:|---:|---:|---:|
| 22 | 4.036.675 | 2.019.635 | 51.047 | 61.952 | 10.905 |
| 23 | 8.073.350 | 4.037.425 | 46.949 | 67.712 | 20.763 |
| 24 | 16.146.700 | 8.075.572 | 51.647 | 73.728 | 22.081 |

Sono **28.256.725 passi binari** nei tre livelli, ciascuno ripercorso dal
verificatore. Questo numero non rappresenta prove statisticamente
indipendenti. Tutti e tre i limiti congelati sono rispettati, senza
modificare la candidata dopo aver osservato i risultati.

Le perdite massime sono raggiunte negli intervalli:

- v22: 2.354.901 → 2.362.773;
- v23: 7.081.505 → 7.084.887;
- v24: 9.716.549 → 9.721.503.

I blocchi sfavorevoli sono numerosi. Fra i blocchi diagnostici di 256 passi,
quelli con incremento C negativo sono rispettivamente 4.592 su 15.769,
9.081 su 31.537 e 18.184 su 63.074. Gli ultimi blocchi hanno 67, 134 e
12 passi. Il test include ogni prefisso interno: non certifica solo i bordi
dei blocchi e non presuppone positività di ciascun blocco.

I conteggi J forniscono nuovi limiti superiori di discesa Syracuse sotto
N_v nei livelli 22–24: rispettivamente 2.019.635, 4.037.425, 8.075.572
passi da Q_v. Non sono primi tempi esatti né tempi di raggiungimento di 1.
Insieme ai certificati precedenti estendono la verifica finita fino a v24.

## 4. Il tentativo di prova e il suo limite concreto

Abbiamo tentato di chiudere la conservazione su una descrizione dello stato
formata da credito, residuo e fascia d'altezza. La
[nota sull'ostacolo](RESIDUE_OBSTRUCTION_IT.md) dimostra che una descrizione
che dimentica l'appartenenza specifica alla torre ammette necessariamente
continuazioni che esauriscono il credito.

In particolare, qualsiasi prefisso di L parità può essere seguito da m
passi dispari scegliendo opportunamente un lift. Con
m=floor(D/284)+1, questi passi esauriscono qualunque credito al massimo D.
La fascia d'altezza binaria contenente Q_v è abbastanza larga da contenere
tali interi compatibili, se L+m≤H_v.

Una prova valida per tutta questa cella di residuo e altezza richiederebbe
dunque L≥H_v−floor(128v²/284). Al livello 24 dovrebbe mantenere almeno
16.146.441 dei 16.146.700 bit. Questo è un limite di quella precisa
astrazione; non è un controesempio Q_v, né un'impossibilità generale di
dimostrare la candidata. Una prova simbolica potrebbe usare la struttura
aritmetica esatta della torre senza elencare i bit.

Il vincolo ulteriore necessario resta da trovare: la candidata rimane
esplicitamente una congettura di lavoro. Questa fase non formalizza in
Lean una conservazione uniforme del credito. Nessuna nuova priorità
matematica è stabilita.

## 5. Verifica e riproduzione

Il produttore usa quadrature modulari per il residuo iniziale e una
composizione affine ricorsiva per ricostruire le parità. Il verificatore
C/GMP usa la ricorrenza Q_(v+1)=Q_v+2^(v+2)Q_v² e un replay lineare in
blocchi fino a 32 passi, senza le tabelle del produttore. La concordanza
riguarda l'hash SHA-256 dell'intera parola di parità, tutti i conteggi,
minimi, massimi e testimoni; è stata verificata anche sull'intera calibrazione.

I quindici test includono confronto con T elementare, estremi e testimoni
esaustivi su parole corte, identità del credito, blocchi finali incompleti,
diverse larghezze del verificatore e rifiuto di tracce o risultati alterati.
Il motore calcola residui alla precisione H_v e non costruisce Q_v completo.

Dalla radice del repository, su Linux con `libgmp-dev`:

```sh
cc -O3 -std=c11 -Wall -Wextra -Werror notes/post_v6_compensation_2026-09-25/verify_blocks.c -lgmp -o /tmp/verify_blocks
python3 notes/post_v6_compensation_2026-09-25/test_compensation.py
python3 notes/post_v6_compensation_2026-09-25/test_verifier.py /tmp/verify_blocks
python3 notes/post_v6_compensation_2026-09-25/compensation_probe.py calibration --output /tmp/calibration_results.json
python3 notes/post_v6_compensation_2026-09-25/compensation_probe.py holdout --output /tmp/holdout_results.json
python3 notes/post_v6_compensation_2026-09-25/verify_holdout.py --input /tmp/holdout_results.json --verifier /tmp/verify_blocks --output /tmp/verification_results.json
```

Su macOS con Homebrew GMP, aggiungere `-I/opt/homebrew/include` e
`-L/opt/homebrew/lib` alla compilazione; nell'ambiente di sviluppo usato
serve inoltre `DEVELOPER_DIR=/Library/Developer/CommandLineTools`.

Dati: [calibrazione](calibration_results.json),
[nuovi livelli](holdout_results.json),
[replay indipendente](verification_results.json),
[replay della calibrazione](calibration_verification_results.json).
Questa fase non aggiunge prove Lean e non modifica gli artefatti pubblicati v6.
