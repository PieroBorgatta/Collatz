# Dopo le torri: libertà dei suffissi finiti e limite della strategia locale

24 settembre 2026. Continuazione del risultato sui predecessori, commit
`f198185`. **Risultato verificato:** 19 nuovi teoremi pubblici e tre lemmi
privati; build aggregata riuscita (3.374 job) e audit delle undici radici
superato nella [CI 36015103652](https://github.com/PieroBorgatta/Collatz/actions/runs/36015103652),
commit `e713dfdf64403a15e451ec11d3cf642ef2b11615`.

La ricerca richiesta era un vincolo tra episodi consecutivi che obbligasse
una compensazione della crescita. Il trasporto esatto del parametro produce
un risultato diverso: fissata la fase e la valutazione v, **ogni parola finita
ammissibile dopo la raffica si realizza per infiniti parametri positivi**.
Non si può dunque escludere una continuazione finita soltanto perché segue
una torre della v6. Questo precisa il limite della strategia proposta;
non esclude vincoli che usino anche l'altezza reale o ulteriori restrizioni
sul parametro.

## 1. Il parametro conserva esattamente la precisione binaria

Per v≥1 e q naturale definiamo

\[
 Q_v(q)=\frac{9^{2^v q}-1}{2^{v+3}}.
\]

La divisione è esatta, anche per q=0. Per r<q, LTE e la fattorizzazione

\[
 9^{2^v q}-9^{2^v r}
 =9^{2^v r}\bigl(9^{2^v(q-r)}-1\bigr)
\]

danno

\[
 \nu_2\bigl(Q_v(q)-Q_v(r)\bigr)=\nu_2(q-r).
\]

Ne segue, per ogni b≥0,

\[
 Q_v(q)\equiv Q_v(r)\pmod{2^b}
 \quad\Longleftrightarrow\quad q\equiv r\pmod{2^b}.
\]

Sui residui finiti questo è un'iniezione di un insieme finito in sé, quindi
una biiezione. Inoltre `Q_v(q) mod 2 = q mod 2`. La dimostrazione non assume
una distribuzione casuale degli iterati.

Modulo Lean: [TowerParameter.lean](../../lean/CollatzShadowing/TowerParameter.lean).

## 2. Trasporto fino alle orbite effettive

Nella fase C poniamo d=2^v q e

\[
 n=\frac{2^{3d+1}-11}{3},\qquad y=\frac{9^d-5}{4}.
\]

Il reset, i d−1 blocchi `[1,2]` e l'uscita `[1,4]` già descritti nella v6
danno `S^(2d+1)(n)=y`. I successivi v passi di esponente 1 portano a

\[
 S^{2d+1+v}(n)=z=2\,3^v Q_v(q)-1.
\]

Nella fase B, l'uscita `9^(d+1)−10` percorre v+2 passi di esponente 1 e
arriva a `2·3^(v+4)Q_v(q)−1`. Le formule valgono per tutti i parametri positivi
nei domini indicati. Per q dispari le raffiche indicate sono massimali:
l'esponente seguente è almeno 2. La formalizzazione del teorema sui suffissi
certifica direttamente gli esponenti prescritti, senza assumere tale
massimalità come ipotesi.

Il modulo [TowerSuffix.lean](../../lean/CollatzShadowing/TowerSuffix.lean)
collega il trasporto di fase C alla sorgente originale tramite
`CancellationTower`; per B formalizza il tratto dall'uscita alla raffica.

## 3. Ogni parola finita ammissibile ha una sola classe del parametro

Sia w una parola finita non vuota, con primo esponente almeno 2 e tutti gli
altri positivi. Poniamo A=Σw, L=|w|, P=3^L e C=C_w, dove
`(Pz+C)/2^A` è l'estremo affine del suffisso. Scriviamo
`z=2·3^s Q_v(q)−1`, con s=v nella fase C e s=v+4 nella B.

Il teorema dei cilindri esatti già presente nel progetto dà

\[
 w\text{ è realizzata da }z
 \quad\Longleftrightarrow\quad
 Pz+C\equiv2^A\pmod{2^{A+1}}.
\]

Poiché P+C è divisibile per 4, la sostituzione di z e la cancellazione di
un fattore 2 danno precisamente

\[
 3^{L+s}Q_v(q)+\frac{C+P}{2}
 \equiv 2^{A-1}+P\pmod{2^A}.
\]

Il moltiplicatore è dispari e Q_v permuta i residui: esiste quindi una sola
classe `r mod 2^A`. La classe è dispari perché il termine a destra è dispari
e `(C+P)/2` è pari. Il risultato completo è

\[
 \exists r\in\{1,3,\ldots,2^A-1\}\quad
 \forall q>0:\quad
 \operatorname{Matches}(w,z(q))\iff q\equiv r\pmod{2^A}.
\]

Ogni rappresentante positivo `q=r+j·2^A` realizza la parola. Collegando questa
identità alla sorgente della fase C si ottiene il teorema sull'orbita concreta,
con parametri arbitrariamente grandi. In particolare si può prescrivere
`[2] ++ [1]^l` per qualsiasi l finito: dopo il passo di esponente 2 segue una
nuova raffica di crescita lunga quanto richiesto.

Questo enunciato specifica gli esponenti. **Non afferma che tutto il segmento
resti sopra il valore iniziale**, né dà un ritorno discendente alla sezione E.
L'esponente 2 può comportare una discesa locale; il confronto con l'origine
è un obbligo distinto.

## 4. Il ruolo dell'altezza e il criterio operativo

La stessa classe r fornisce un criterio esatto per un parametro limitato:

\[
 \exists\,0<q\le B:\ \operatorname{Matches}(w,z(q))
 \quad\Longleftrightarrow\quad r\le B.
\]

È il punto utile per una continuazione: trasportare insieme **residuo minimo,
modulo e limite del parametro**. Limitare solo il numero di parole o trattare
le valutazioni successive come indipendenti perde questa informazione.
Una ricerca successiva potrebbe verificare se le parole che evitano una
precisa discesa richiedano residui minimi superiori al limite consentito dalla
sorgente. Oggi non abbiamo un limite uniforme su tutte queste parole.

La libertà dei prefissi finiti non permette di scambiare i quantificatori:

\[
 \forall w\text{ finita}\ \exists q\in\mathbb N_{>0}
 \qquad\not\Rightarrow\qquad
 \exists q\in\mathbb N_{>0}\ \forall\text{ prefissi di una parola infinita}.
\]

Una successione compatibile di classi può convergere a un parametro 2-adico
che non è un naturale. Non abbiamo costruito orbite divergenti. Le frequenze
nei residui di q non sono densità naturali delle sorgenti n, che crescono
esponenzialmente in q.

## 5. Controlli, attribuzione e riproduzione

[transport_probe.py](transport_probe.py) usa soltanto interi esatti:

- tutte le 255 parole con primo esponente almeno 2 e somma al più 9;
- sei valori di v e entrambe le fasi: 3.060 classi uniche verificate;
- 533.460 controlli di appartenenza, inclusi rappresentanti oltre il primo periodo;
- 384 orbite di interi effettivamente costruiti, con quattro esponenti dopo la raffica;
- testimoni modulari per `[2] ++ [1]^l` fino a l=64.

L'algoritmo inverte Q_v bit per bit, usando potenze modulari: non costruisce
le sorgenti astronomiche degli ultimi testimoni. La prova Lean e i test finiti
hanno ruoli distinti. L’implementazione Python non è estratta da Lean e
non è oggetto di una prova universale di correttezza del programma. I risultati riproducibili sono in
[transport_results.json](transport_results.json).

La libertà generale dei prefissi e la codifica 2-adica sono classiche:
[Bernstein–Lagarias, 1996](https://doi.org/10.4153/CJM-1996-060-x) studiano la
coniugazione della mappa abbreviata, che induce permutazioni a ogni livello
finito; [Laarhoven–de Weger](https://arxiv.org/abs/1209.3495) collegano i grafi
modulari ai grafi di De Bruijn. Non rivendichiamo come nuova questa struttura,
né una coniugazione globale per Syracuse alla sua singolarità. Il contributo
locale è il suo trasporto dimostrato nella specifica famiglia esponenziale
delle torri della v6, con la congruenza esatta sul parametro originario.

```sh
cd lean
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_transport_2026-09-24/DependencyAudit.lean
python3 ../notes/post_v6_transport_2026-09-24/transport_probe.py
```

Il pin resta Lean 4.29.1, Mathlib
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`. La CI ha compilato i due nuovi
moduli e l'entrypoint aggregato, riusando le dipendenze fissate e la cache
Mathlib; 3.374 è il numero di job della build, non di nuovi moduli o teoremi.
La verifica finale non produce avvisi Lean nei nuovi moduli.

[DependencyAudit.lean](DependencyAudit.lean) ha controllato undici radici e
percorso l'intera unione delle loro dipendenze nominate, senza filtro:
**13.782 dichiarazioni**, 1.671 privati, 12.718 corpi e 229.886 archi tipo/corpo.
Sono raggiunti il lemma LTE, il cilindro esatto e l'iterazione della torre.
Gli unici assiomi sono `propext`, `Classical.choice`, `Quot.sound`.
Anche l'audit generale della biblioteca è passato con la sua allowlist
storica: i nuovi teoremi non dipendono dagli assiomi di `native_decide`
consentiti per alcune vecchie certificazioni finite.

Evidenze: [audit integrale](dependency_audit.log),
[log CI completo compresso](ci_36015103652.log.gz),
[prima CI riuscita](ci_36014535726.log.gz) e
[manifest degli hash](verification_manifest.json).
Il JSON prodotto in CI coincide byte per byte con quello archiviato.
La [revisione semantica interna](REVIEW_IT.md) distingue i quantificatori e
l'effettivo limite della strategia. Il
[protocollo di riproduzione](REPLAY_PROTOCOL.md) separa replay su nuova macchina,
controllo del kernel indipendente e revisione umana: questi ultimi due non
sono stati effettuati.

È stata inoltre preparata una
[nota matematica breve sui predecessori](../compact_seeds_sixth_power_note_2026-09-24.md),
che isola il precedente contributo quantitativo e l'input analitico esterno.
La v6 pubblicata e le sue evidenze rimangono immutate; questa è una nuova
continuazione del working tree. La congettura di Collatz resta aperta.
