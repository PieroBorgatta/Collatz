# Certificare la discesa con un conteggio modulare

24 settembre 2026. Continuazione dello
[studio fra livelli](../post_v6_levels_2026-09-24/RESULTS_IT.md).

**Risultato:** un criterio sufficiente generale trasforma un conteggio di
parità modulo una potenza di 2 in un certificato di discesa sotto la sorgente.
Il programma ha certificato tutti i 17 livelli v=5,…,21, con controllo
aritmetico indipendente completo. I tre livelli v=19,20,21 estendono quelli
precedentemente verificati; non sono calcoli del tempo esatto di discesa.
Resta aperta la disuguaglianza sul conteggio per tutti i livelli.

In parallelo, un'applicazione del Teorema 2.1 di Chim (2025), con controlli
finiti per i livelli piccoli, mostra che il primo passo diverso fra due
livelli adiacenti rimane sopra la rispettiva sorgente. La dimostrazione è
nella [nota sulla separazione](CHIM_OBSTRUCTION_IT.md).

Entrambi sono risultati a livello di dimostrazione informale, con revisione
interna tramite agenti e controlli aritmetici. Non sono nuove dichiarazioni
Lean. Non è stabilita l'originalità nella letteratura e non è provata la
discesa della famiglia infinita.

## 1. Definizioni e obiettivo

Per v≥5 poniamo M=2^v e

\[
 Q_v=\frac{9^M-1}{2^{v+3}},\qquad
 N_v=\frac{2^{3M-5}-11}{3},\qquad
 t_v=\min\{k\ge0:S^k(Q_v)<N_v\}.
\]

Come prima, S(x)=(3x+1)/2^{ν₂(3x+1)} su dispari positivi, e il minimo
vale ∞ se non esiste. N_v è la sorgente n_q con q=2^{v−1}−1; il ponte
dal precedente endpoint z_q a Q_v ha tre passi. Il tempo t_v parte da
Q_v, non da N_v, e non misura il raggiungimento di 1.

Introduciamo la mappa abbreviata a una divisione per passo:

\[
 T(x)=\begin{cases}(3x+1)/2&x\text{ dispari},\\x/2&x\text{ pari}.
 \end{cases}
\]

Un passo Syracuse con esponente a corrisponde a un passo dispari di T
seguito da a−1 passi pari. Questa T differisce dalla mappa non abbreviata
che separa anche la moltiplicazione 3x+1 dalla sua prima divisione.

## 2. Criterio sufficiente con costanti razionali

Fissiamo un budget intero 1≤K≤M e

\[
 \boxed{H=\left\lceil\frac{485K+52M}{306}\right\rceil.}
\]

**Proposizione.** Se fra Q_v,T(Q_v),…,T^{H−1}(Q_v) ci sono J≤K valori
dispari, allora esiste i≤J tale che S^i(Q_v)<N_v. In particolare t_v≤J≤K.

Il conteggio J è determinato completamente da Q_v modulo 2^H.
Il criterio è sufficiente: J>K non implica t_v>K né assenza di discesa.
Non viene assunta alcuna distribuzione casuale delle parità.

**Prova.** I primi H passi di T consumano esattamente H divisioni per 2.
Avendo iniziato J passi Syracuse, i loro esponenti completi hanno somma
A_J≥H. L'ultima sequenza di divisioni può proseguire oltre il tratto
osservato: non occorre conoscerne l'esponente esatto.

Poniamo y_i=S^i(Q_v). Se una discesa è già avvenuta prima di J, la tesi
è soddisfatta. Altrimenti y_i≥N_v per i<J, e l'identità esatta

\[
 y_J=\frac{3^JQ_v}{2^{A_J}}
       \prod_{i<J}\left(1+\frac1{3y_i}\right)
\]

dà una maggiorazione del prodotto di 3/2. Infatti J≤K≤M≤N_v e

\[
 \prod_{i<J}\left(1+\frac1{3y_i}\right)
 \le (1+1/(3N_v))^J
 \le\frac1{1-J/(3N_v)}\le\frac32.
\]

La seconda disuguaglianza segue dal binomio e dalla serie geometrica.
La disuguaglianza M≤N_v è immediata da 2^{3M−5}≥3M+11 per M≥32.
Inoltre, posto B=2^{3M−5}, B≥44 implica N_v=(B−11)/3≥B/4. Ne segue

\[
 \frac{Q_v}{N_v}<4\,2^{2-v}(9/8)^M,
 \qquad
 \frac{y_J}{N_v}
 <\frac{24}{2^v}\frac{3^{K+2M}}{2^{H+3M}}.
\]

Il controllo intero 3^{306}<2^{485} e la definizione di H danno

\[
 306(H+3M)\ge485(K+2M)
 \quad\Longrightarrow\quad 3^{K+2M}<2^{H+3M}.
\]

Pertanto y_J/N_v<24/2^v≤3/4, il che prova la discesa se non era
già avvenuta. □

La conclusione è **«entro J»**. Dopo una discesa precedente l'orbita può
risalire: il criterio non garantisce che S^J(Q_v), né T^H(Q_v), sia sotto
N_v. Il fattore additivo non è stato ignorato. La soglia H è volutamente
sufficiente e non ottimizzata fino all'ultimo bit.

## 3. Perché basta un residuo e come lo verifichiamo

Il vettore di parità dei primi H passi di T dipende solo dall'ingresso
modulo 2^H. A ogni passo la precisione scende di un bit; il bit iniziale
successivo è noto fino all'ultimo dei passi richiesti. Questo è il
classico principio dei cilindri di parità, non un nuovo principio generale.

Il residuo iniziale si ottiene senza costruire Q_v:

\[
 Q_v\bmod2^H
 =\frac{(9^{2^v}\bmod2^{H+v+3})-1}{2^{v+3}}.
\]

La divisione a destra è esatta. Il produttore compone T a blocchi di
16 passi. Per ogni residuo r modulo 2^{16} precalcola

\[
 T^{16}(x)=\frac{3^{j_r}x+C_r}{2^{16}}
 \quad(x\equiv r\bmod2^{16}),
\]

e somma i conteggi j_r. L'ultimo blocco usa soltanto i bit rimasti.
Conserva SHA-256 del residuo e della sequenza di blocchi; gli hash sono
controlli di integrità, non sostituiscono la verifica aritmetica.

Il verificatore separato non importa il produttore o le sue tabelle:
ricostruisce il residuo con Q₁=5 e Q_{u+1}=Q_u+2^{u+2}Q_u²,
poi applica Syracuse modularmente un passo alla volta. L'ultimo esponente
è marcato esplicitamente come **almeno** la precisione residua.
I due programmi concordano su tutti i 20 tentativi archiviati.

Il bit necessario per sapere che un endpoint Syracuse è dispari non è
richiesto qui al termine della precisione: usiamo soltanto A_J≥H. Questo
non contraddice il modulo 2^{A+1} necessario per certificare una parola
Syracuse esatta di somma A.

## 4. Risultati finiti e tentativi inconcludenti

Per ogni v proviamo K=M/2. Soltanto se il certificato fallisce, riproviamo
con K=M. I fallimenti del primo tentativo restano nei dati.
Tutti i 17 livelli da 5 a 21 hanno almeno un certificato riuscito:

| v | Budget K riuscito | Precisione H | Limite certificato t_v≤J |
|---:|---:|---:|---:|
| 5 | 16 | 31 | 14 |
| 6 | 64 | 113 | 58 |
| 7 | 128 | 225 | 112 |
| 8 | 128 | 247 | 120 |
| 9 | 512 | 899 | 480 |
| 10 | 512 | 986 | 483 |
| 11 | 1024 | 1972 | 951 |
| 12 | 2048 | 3943 | 1955 |
| 13 | 4096 | 7885 | 4009 |
| 14 | 8192 | 15769 | 7854 |
| 15 | 16384 | 31537 | 15783 |
| 16 | 32768 | 63074 | 31613 |
| 17 | 65536 | 126147 | 62747 |
| 18 | 131072 | 252293 | 126369 |
| 19 | 262144 | 504585 | 251632 |
| 20 | 524288 | 1009169 | 504483 |
| 21 | 1048576 | 2018338 | 1008989 |

I 14 livelli v≤18 si sovrappongono alle orbite complete dello studio
precedente; i limiti certificati sono compatibili con tutti i tempi esatti
già registrati. Per v=19,20,21 non abbiamo calcolato il primo tempo esatto:
abbiamo questi nuovi limiti certificati per q=262143,524287,1048575.

Il primo budget fallisce a v=6,7,9, con rispettivamente 34>32, 66>64,
268>256 passi dispari. A v=6 il tempo esatto noto è invece 28<32:
è un esempio concreto del fatto che il fallimento è inconcludente.

Totali di lavoro: 4.037.892 passi binari modulari, contenenti 2.018.020
passi dispari, su 20 tentativi. I tentativi dello stesso livello condividono
parte del prefisso: questi totali non sono altrettanti eventi indipendenti.
Nessun intero Q_v completo è costruito dal produttore o dal verificatore.
I test su piccoli livelli costruiscono invece gli interi, appositamente,
per controllare il collegamento con le orbite naturali.

## 5. Il problema infinito ora ha una forma verificabile

Per K=2^{v−1}, la precisione scelta è

\[
 H_v=\left\lceil\frac{589\cdot2^v}{612}\right\rceil.
\]

Una sufficiente via alla discesa di tutti i livelli v≥10 sarebbe provare

\[
 \#\{0\le r<H_v:T^r(Q_v)\text{ dispari}\}\le2^{v-1}
 \quad\text{per ogni }v\ge10.
\]

È una **proposta ancora aperta**, suggerita dai casi verificati, non una
conseguenza dei calcoli. La frazione ammessa tende a 306/589≈0,5195;
non serve dimostrare una frequenza esattamente 1/2. Il fatto che la soglia
ammetta un margine non autorizza ad assumere indipendenza o casualità.
I risultati in densità naturale non coprono automaticamente questa
sottosequenza di densità zero.

Il nuovo criterio supera il limite operativo dei soli prefissi condivisi:
esamina abbastanza bit specifici del singolo livello da poter certificare
la discesa. Non risolve il problema di controllarli uniformemente.
La nota di Chim esclude inoltre il primo salto distinto come luogo della
discesa: il controllo deve proseguire oltre quel punto.

Un'alternativa al conteggio è cercare un'induzione quadratica fra endpoint.
Le identità esatte e il criterio di convessità sono riportati nella
[nota sulla separazione, sezione 4](CHIM_OBSTRUCTION_IT.md#4-una-possibile-induzione-ancora-da-chiudere).
Nessun invariante che chiuda tale induzione è stato trovato in questa fase.

## 6. Letteratura e riproduzione

La dipendenza delle parità dal residuo e la composizione affine sono
classiche: [Bernstein–Lagarias (1996)](https://doi.org/10.4153/CJM-1996-060-x).
Il prodotto usato per controllare il termine additivo compare anche in
[Rozier–Terracol, v5 del 17 maggio 2026, Teorema 4.2](https://arxiv.org/html/2502.00948v5).
La nostra soglia è una specializzazione sufficiente per Q_v/N_v; non
assume la congettura di uguaglianza fra stopping time e coefficient
stopping time. I risultati tipici di
[Inselmann, v3](https://arxiv.org/abs/2402.03276v3) non dimostrano il
conteggio richiesto su tutti questi livelli. La nuova applicazione del
risultato di Chim (2025) è esplicitata nella nota separata, senza attribuire
all'articolo originale conclusioni su questa famiglia.

Dalla radice del repository:

```sh
python3 notes/post_v6_certificates_2026-09-24/test_certificates.py
python3 notes/post_v6_certificates_2026-09-24/modular_certificate.py --max-v 21 --output-dir /tmp/tower-certificates
python3 notes/post_v6_certificates_2026-09-24/separation_probe.py --output /tmp/tower-certificates/separation_results.json
python3 notes/post_v6_certificates_2026-09-24/verify_certificates.py --max-v 21 --input /tmp/tower-certificates/certificate_results.json --output /tmp/tower-certificates/verification_results.json
```

Il verificatore, senza `--max-v 21`, si ferma per default al livello 18 e
marca esplicitamente quelli non ripercorsi. La corsa completa archiviata
non ne salta nessuno. I dieci test coprono composizione e cambi di blocco,
precisione troncata, dati alterati, esempi di discesa e i piccoli casi
della prima separazione.

Dati: [certificati](certificate_results.json),
[replay indipendente](verification_results.json),
[separazione finita](separation_results.json).
La v6 pubblicata e i moduli Lean esistenti rimangono invariati.
