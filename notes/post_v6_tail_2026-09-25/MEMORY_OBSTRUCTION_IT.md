# Memoria esatta della coda e limiti dei potenziali universali

**25 settembre 2026.** Studiamo il trasduttore della coda alimentato da
bit arbitrari. Dimostriamo una descrizione completa degli stati
raggiungibili a numero fissato di passi dispari e un limite inferiore
alla memoria necessaria per prevederne esattamente tutte le uscite.
La normalizzazione reale contrae le distanze, ma non rende stabile la
parità. I risultati sono prove su carta, non dichiarazioni Lean; non si
attribuisce originalità a queste conseguenze delle codifiche classiche.

Il dominio degli ingressi arbitrari è essenziale. Nessuno degli esempi
avversari viene identificato con un livello della torre `Q_v`; nessuna
delle ostruzioni esclude un certificato che usi proprietà specifiche
delle sue sorgenti.

## 1. Trasduttore e stati normalizzati

Per la mappa shortcut `T`, scriviamo

\[
 T^t(n)=3^{j_t}\lfloor n/2^t\rfloor+z_t,
 \qquad j_t=J_n(t),\quad 0\le z_t<3^{j_t}.
\]

La [decomposizione esatta](../post_v6_propagation_2026-09-25/PREFIX_PROPAGATION_IT.md)
assicura questa formula. All'inizio `(j,z)=(0,0)`. Dato il bit
d'ingresso `h∈{0,1}`, l'uscita e lo stato successivo sono

\[
 p=(h+z)\bmod2,
\]
\[
 (j',z')=
 \begin{cases}
 (j,(3^j h+z)/2),&p=0,\\
 (j+1,(3^{j+1}h+3z+1)/2),&p=1.
 \end{cases}                                                   \tag{1}
\]

Ogni parola finita di ingressi `h_0,…,h_(t−1)` è realizzata dai bit
inferiori dell'intero `a=Σ_(i<t)h_i2^i`. Non occorre assumere un intero
ordinario con una coda infinita di bit uguali a uno.

Ponendo `u=z/3^j`, la ricorrenza diventa

\[
             u'=\frac{h+u}{2}+\frac{p}{2\,3^{j+1}}.             \tag{2}
\]

Il termine aggiuntivo è nullo se `p=0`. La formula non rende la parità
una funzione continua di `u`: per determinarla serve la parità
dell'intero `z`, sulla griglia di passo `3^(−j)`.

## 2. Quali code sono raggiungibili a `j` fissato

**Proposizione.** Per ogni `j≥1`, gli stati raggiungibili con quel
valore di `j` hanno precisamente

\[
        z\in\{1\le z<3^j:3\nmid z\}.
                                                                  \tag{3}
\]

Sono `q_j=2·3^(j−1)` stati distinti. Inoltre tutti questi stati possono
essere raggiunti al medesimo tempo

\[
                         t_j=j+q_j-1.                            \tag{4}
\]

**Necessità.** Finché non compare il primo dispari, lo stato rimane
`(0,0)`. Il primo dispari crea `(1,2)`. Successivamente un passo con
`p=0` dà `z'≡2z mod3`, mentre un passo con `p=1` dà `z'≡2 mod3`.
Quindi il resto non diventa mai divisibile per tre.

**Un fatto elementare sulle unità.** Il numero `2` genera tutte le
unità modulo `3^j`. Per vederlo senza assumere una formula generale
sugli ordini, l'induzione binomiale dà

\[
                      v_3(4^{3^k}-1)=k+1.                        \tag{5}
\]

La base è `4−1=3`. Se `A=1+3^(k+1)c` con `3∤c`, allora

\[
 A^3-1=3^{k+2}c
       \left(1+3^{k+1}c+3^{2k+1}c^2\right),
\]

e la parentesi è congrua a uno modulo tre. Ne segue che l'ordine di
`4` modulo `3^j` è `3^(j−1)`: divide questa potenza e non una potenza
inferiore. L'ordine di `2` è pari, poiché `2≡−1 mod3`; pertanto è il
doppio dell'ordine di `4`, cioè `2·3^(j−1)`. Questo è il numero totale
delle unità.

**Sufficienza.** Leggendo `j` ingressi uguali a uno si ottiene

\[
                         (j,z)=(j,3^j-1),                        \tag{6}
\]

come mostra direttamente (1). Da questo stato si può imporre ogni
uscita successiva uguale a zero scegliendo `h=z mod2`. Il contatore
`j` resta fisso e la trasformazione del resto è

\[
                         z'\equiv2^{-1}z\pmod{3^j},              \tag{7}
\]

sempre con rappresentante in `[0,3^j)`. Per (5), l'orbita di
`3^j−1` mediante (7) visita tutte le unità. Ogni resto desiderato
si raggiunge dopo un numero `e` di questi passi con `0≤e<q_j`.

**Sincronizzazione.** Prima della costruzione appena descritta,
aggiungiamo `t_j−j−e` ingressi nulli. Lo stato iniziale resta `(0,0)`;
seguono i `j` ingressi uno e i `e` ingressi scelti per (7).
La lunghezza totale è sempre `t_j` e il contatore finale è sempre
`j`. Non stiamo dunque confrontando stati che si distinguerebbero
soltanto osservando il tempo o il numero di dispari già trascorsi.

## 3. Distinguibilità e limite inferiore alla memoria

**Lemma delle parole di parità.** La mappa che associa a un residuo
modulo `2^k` le sue prime `k` parità shortcut è una biezione con
`{0,1}^k`.

**Dimostrazione.** Due interi congrui modulo `2^k` hanno le stesse
prime `k` parità: dopo `s≤k` passi la loro differenza è
`3^(J(s))2^(k−s)c`, e prima del passo successivo è pari. Per
l'induzione sulla lunghezza, i due sollevamenti `a` e `a+2^k` di
un residuo modulo `2^k` hanno quindi la stessa parola iniziale;
dopo `k` passi differiscono di `3^(J(k))`, un numero dispari.
Le parità successive sono opposte. Ogni parola di lunghezza `k`
ammette dunque precisamente i due prolungamenti possibili. La base
`k=0` è immediata.

Ora fissiamo `j≥1` e due resti raggiungibili distinti `z,ż` in (3).
Forniamo a entrambi una continuazione di ingressi tutti nulli. Con
`h=0`, la componente intera della coda evolve esattamente mediante
`T(z)`, indipendentemente dal contatore `j`. Le uscite sono quindi
le parole di parità degli interi `z` e `ż`.

Per

\[
                       k_j=\lceil\log_2(3^j)\rceil,              \tag{8}
\]

i due interi sono distinti anche modulo `2^(k_j)`. Il lemma garantisce
che le due uscite divergono entro i primi `k_j` bit della continuazione.

**Conseguenza sulla memoria.** Un trasduttore deterministico che
preveda esattamente tutte le uscite per ogni ingresso finito deve
distinguere almeno `2·3^(j−1)` stati alla sezione sincronizzata (4).
Se ne identificasse due, la medesima continuazione nulla produrrebbe
la stessa uscita nell'astrazione e uscite diverse nel sistema esatto.
Servono quindi almeno

\[
                    \left\lceil\log_2(2\cdot3^{j-1})\right\rceil
                                                                  \tag{9}
\]

bit di stato. Il limite vale anche se `j` e il tempo sono forniti
separatamente, poiché sono uguali per tutti gli stati confrontati.
Si intende una macchina sequenziale senza accesso supplementare
all'intero ingresso già letto.

Il risultato esclude un numero finito uniforme di stati per la
previsione esatta su tutti gli ingressi. Non esclude un'astrazione
con uscite multiple, una stima aggregata, un errore controllato o
un dominio ristretto alla torre.

### Un quoziente esatto per un orizzonte finito

Il limite di memoria ammette anche una formulazione costruttiva.
Fissati `j` e un orizzonte futuro `k≥0`, due resti `z,ż` producono
le stesse prossime `k` uscite **per ogni medesima continuazione di
ingressi** se e soltanto se

\[
                              z\equiv\widetilde z\pmod{2^k}.
                                                                  \tag{10}
\]

Per la sufficienza, le prime uscite sono uguali perché le parità dei
resti coincidono. I contatori restano sincronizzati; dalla (1) la
differenza fra i nuovi resti è `3^p(z−ż)/2`. A ogni passo si perde
un bit di precisione binaria, e l'induzione copre i `k` passi.
Per la necessità basta scegliere tutti gli ingressi futuri nulli e
applicare il lemma delle parole di parità.

Il numero minimo di classi distinguibili a quell'orizzonte è dunque

\[
 N_{j,k}=\#\{z\bmod2^k:1\le z<3^j,\ 3\nmid z\}.
\]

Se `3^j≥2^(k+1)`, ogni residuo `r mod2^k` ha i rappresentanti
`r,r+2^k` nell'intervallo `[0,3^j)`. Non possono essere entrambi
divisibili per tre, dunque `N_(j,k)=2^k`. Se `2^k≥3^j`, nessuna
delle unità si identifica con un'altra e `N_(j,k)=2·3^(j−1)`.
Non occorre una formula per il regime intermedio per queste conclusioni.

Operativamente, conoscendo `j` e `a=z mod2^k`, si calcola
`p=(h+a) mod2` e si aggiorna

\[
 j'=j+p,\qquad
 a'=\frac{3^p(3^j h+a)+p}{2}\pmod{2^{k-1}}.
                                                                  \tag{11}
\]

La divisione è intera e la classe ottenuta non dipende dal
rappresentante scelto per `a`. Il budget di precisione scende da
`k` a `k−1`; per `k=0` non si richiedono uscite. Questo è un
trasduttore esatto a orizzonte finito, non una memoria di `k` bit
riutilizzabile indefinitamente senza informazione ulteriore.

## 4. Perdita immediata della parità nei troncamenti ternari

Supponiamo di conservare soltanto le prime `K` e le ultime `L` cifre
della coda scritta con esattamente `j` cifre, oltre a `j` e al bit
corrente `h`. Se `j≥K+L+1`, consideriamo

\[
                         z=1,\qquad\widetilde z=1+3^L.           \tag{12}
\]

Per `L=0` sono `1` e `2`; per `L≥1` entrambi sono congrui a uno
modulo tre. Sono dunque raggiungibili per la proposizione precedente.
Hanno le stesse ultime `L` cifre e le prime `K` cifre entrambe nulle,
perché `1+3^L<3^(j−K)`. Tuttavia la loro differenza è dispari:
con il medesimo ingresso `h` le prossime uscite sono opposte.

L'ostruzione riguarda precisamente questo troncamento, senza altri
riassunti della parte scartata. Un bit aggiuntivo con la parità totale
risolve la sola prossima uscita; non supera il limite (9) per tutte
le continuazioni.

## 5. Contrazione reale senza stabilità della parità

Consideriamo due corse con gli stessi successivi `k` ingressi e con
entrambi i contatori iniziali almeno `J`. I contatori non diminuiscono;
i due termini correttivi in (2) appartengono sempre all'intervallo
`[0,1/(2·3^(J+1))]`. Pertanto

\[
 |u_k-\widetilde u_k|
 \le2^{-k}|u_0-\widetilde u_0|
       +\frac{1-2^{-k}}{3^{J+1}}.                              \tag{13}
\]

La prova consiste nell'iterare
`|u'−ũ'|≤|u−ũ|/2+1/(2·3^(J+1))`.
Non è necessario che le uscite o i contatori delle due corse coincidano.

È una contrazione quantitativa nell'intervallo reale. Non autorizza
a cancellare la memoria delle uscite: gli stati raggiungibili `z=1`
e `z=2` allo stesso `j` distano soltanto `3^(−j)` dopo normalizzazione,
ma con `h=0` producono immediatamente parità opposte.

Una formula più precisa descrive l'approssimazione mediante i bit
d'ingresso. Partendo da `(0,0)`, siano `i_1<…<i_j` le posizioni,
numerate da zero, delle uscite dispari fra i primi `t` passi. Posto

\[
 a=\sum_{i=0}^{t-1}h_i2^i,\qquad d=\frac a{2^t},
\]

iterando (2) si ottiene

\[
 \delta:=u_t-d=\sum_{\ell=1}^j\frac{2^{i_\ell-t}}{3^\ell}.
                                                                  \tag{14}
\]

I vincoli `ℓ−1≤i_ℓ≤t−j+ℓ−1` danno gli estremi esatti

\[
 2^{-t}\bigl(1-(2/3)^j\bigr)
 \le\delta\le2^{-j}-3^{-j}.                                    \tag{15}
\]

Le due somme geometriche si raggiungono collocando i `j` dispari,
rispettivamente, all'inizio o alla fine della parola. Queste parole
sono realizzabili per il lemma di biezione. Per `j=0` tutti i termini
sono zero. Il numero `d` ha sviluppo binario finito
`0.h_(t−1)…h_0`: la coda normalizzata lo approssima con errore
minore di `2^(−j)`. Questa precisione resta più grossolana del passo
`3^(−j)` della griglia della coda; (15), da sola, non fissa la parità.
Per esempio, per `t=4`, `a=7`, `j=3`, il resto effettivo è `13`,
ma entrambi i candidati `z=13` e `z=14` soddisfano (15) e sono unità
modulo `27`. Per scegliere quello effettivo serve ulteriore informazione
sulla dinamica, già determinata dall'ingresso completo.

## 6. Potenziali universali: costo necessario lungo gli ingressi uno

Per i primi `t` ingressi tutti uguali a uno, la formula (6) vale
a ogni tempo:

\[
           p_s=1,\qquad j_s=s,\qquad z_s=3^s-1,
           \qquad u_s=1-3^{-s}.                               \tag{16}
\]

Ogni segmento finito è realizzato dall'intero positivo `2^t−1`.
Consideriamo un certificato universale della forma

\[
                 589p_s-306\le\Phi(S_s)-\Phi(S_{s+1}),           \tag{17}
\]

dove `S_s` è lo stato esatto normalizzato o una sua astrazione,
con stato iniziale comune. Sommando lungo (16), necessariamente

\[
                         \Phi(S_t)\le\Phi(S_0)-283t.            \tag{18}
\]

Non può quindi esistere un tale potenziale limitato inferiormente
sull'insieme degli stati raggiungibili; in particolare non può
esistere un potenziale reale su un insieme finito di stati.
Per un premio generale `p−ρ` lo stesso argomento esclude `ρ<1`.

Se il potenziale dipende soltanto da `u`, (18) impone lungo la
successione esplicita `u_t=1−3^(−t)`

\[
 \Phi(u_t)\le\Phi(0)+\frac{283}{\log3}\log(1-u_t).             \tag{19}
\]

Deve dunque divergere verso meno infinito almeno con questo costo
logaritmico alla frontiera `u=1`. Non si escludono potenziali
singolari, dipendenti da contatori illimitati o da un costo iniziale
che cresce con l'ingresso. In quei casi bisogna controllare i termini
di estremità senza riutilizzare il numero di dispari che si vuole
maggiorare; altrimenti il telescopio non dà un limite indipendente.

Per le astrazioni usuali il medesimo ostacolo è un ciclo esplicito.
Lungo (16), ogni prefisso e suffisso ternario di lunghezza fissata
diventa una parola di soli `2`, e ogni memoria finita degli ingressi
diventa una parola di soli `1`. Se si conserva anche `j mod b`, lo
stato ripete un ciclo di lunghezza `b`; senza tale residuo è fisso.
Il premio (17) è positivo a ogni arco. Sommare su questo ciclo
contraddice un certificato di potenziale su tale astrazione.

## 7. Che cosa resta utilizzabile per la torre

La descrizione (3) e la distinguibilità mostrano perché la previsione
esatta generica richiede memoria crescente. Le formule (13)–(15)
restano strumenti quantitativi: separano la parte reale contrattiva
dalla precisione aritmetica che determina le parità.

Una misura uniforme sui bit d'ingresso produce parole di parità
uniformi, per la biezione dimostrata sopra. Questo fatto probabilistico
non fornisce un controllo puntuale delle sorgenti deterministiche
`Q_v`. Analogamente, il ciclo (16) non è un controesempio alla torre.

Anche un telescopio esatto deve avere un costo residuo controllato.
La somma delle cifre della coda al tempo `t` è al più `2j_t≤2t`,
e i riporti nella coda sono al più `j_t≤t`. Sommare queste quantità
su un orizzonte `H` produce quindi limiti individuali `O(H²)`.
La grandezza quadratica non è soltanto un artefatto del maggiorante:
lungo gli ingressi uno, le code sono parole di soli `2`, le somme
delle cifre sono `2t` e i riporti della scansione sono `t`. Le due
somme quadratiche si cancellano esattamente nel telescopio mentre
la densità delle uscite è uno. Un'identità fra i telescopi degli
orizzonti disuguali non controlla, da sola, il segno o la grandezza
del resto `E`; occorre una disuguaglianza indipendente sulla loro
cancellazione.

Un progresso verso il margine del progetto deve quindi aggiungere
un vincolo verificabile sugli ingressi effettivi, oppure controllare
un costo aggregato delle code che sopravviva alla perdita di precisione.
Queste prove non forniscono ancora una maggiorazione uniforme di
`E(m,L)` o `Δ_v` né una nuova discesa.
