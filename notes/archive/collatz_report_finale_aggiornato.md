# Collatz/Syracuse — Report finale aggiornato

## Teoria del Debito Gravitazionale, Famiglie di Confluenza e Quasi-Lyapunov Collatziana

## 1. Obiettivo

Lo scopo di questa ricerca non è dichiarare risolta la Congettura di Collatz, ma costruire un quadro strutturale più preciso per descrivere il comportamento delle orbite della mappa accelerata di Syracuse.

L'idea centrale è interpretare la dinamica come una competizione tra:

- espansione prodotta dal fattore \(3n+1\);
- dissipazione prodotta dalle divisioni per potenze di 2;
- corridoi 2-adici ad alta densità di \(v_2=1\);
- confluenza delle orbite in tronchi comuni;
- scarico del debito tramite tronchi dissipativi;
- funzione di energia empirica capace di riconoscere le discese locali ingannevoli.

La formulazione finale può essere sintetizzata così:

\[
\boxed{
\text{Collatz come dinamica di corridoi 2-adici espansivi che confluiscono in tronchi dissipativi}
}
\]

con una candidata quasi-Lyapunov:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

---

## 2. Mappa accelerata di Syracuse

La funzione Collatz classica è:

\[
C(n)=
\begin{cases}
n/2 & \text{se } n \text{ è pari}\\
3n+1 & \text{se } n \text{ è dispari}
\end{cases}
\]

Per studiare solo i dispari, usiamo la mappa accelerata:

\[
S(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}
\]

Dove:

\[
\nu_2(m)
\]

è il massimo esponente \(a\) tale che:

\[
2^a\mid m
\]

Un passo Syracuse è quindi:

\[
n_{k+1}=S(n_k)
\]

con:

\[
a_k=\nu_2(3n_k+1)
\]

Il valore \(a_k\) misura quanta dissipazione viene prodotta nel passo.

---

## 3. Soglia critica

Approssimativamente:

\[
S(n)\approx n\cdot\frac{3}{2^a}
\]

Quindi la variazione logaritmica è dominata da:

\[
\log 3-a\log 2
\]

La soglia critica è:

\[
a>\log_2(3)
\]

con:

\[
\log_2(3)\approx 1.5849625
\]

Se la media degli \(a_k\) lungo un tratto orbitale è maggiore di questa soglia, il tratto è dissipativo.

Se è minore, il tratto è espansivo.

---

## 4. Debito gravitazionale

Definiamo il debito gravitazionale dopo \(k\) passi:

\[
D(k)=k\log_2(3)-\sum_{i=1}^{k}a_i
\]

Interpretazione:

- \(D(k)>0\): l'orbita ha accumulato vantaggio espansivo;
- \(D(k)<0\): la dissipazione ha dominato;
- \(\max D(k)\): misura quanto l'orbita riesce a resistere alla caduta.

La formulazione fisica è:

\[
\text{debito}=\text{espansione attesa}-\text{divisioni per 2 accumulate}
\]

Il debito è la quantità che un tronco dissipativo dovrà poi scaricare.

---

## 5. Primo caso estremo: \(n=3.041.127\)

Uno dei numeri più esplosivi trovati sotto 5 milioni è:

\[
n=3.041.127
\]

Risultati:

- picco massimo: \(207.572.633.873\);
- rapporto massimo rispetto allo start: circa \(68.255\);
- step del picco: 36;
- primo rientro sotto lo start: 62;
- salti Syracuse fino a 1: 132;
- massima sequenza consecutiva di \(v_2=1\): 17;
- media finale \(v_2\): 1,75.

Poiché:

\[
1.75>\log_2(3)
\]

la traiettoria, pur essendo inizialmente esplosiva, è complessivamente dissipativa.

Questo caso mostra una struttura tipica:

\[
\text{fase espansiva}\rightarrow\text{debito}\rightarrow\text{cascata dissipativa}\rightarrow1
\]

---

## 6. Corridoi 2-adici

Le sequenze di valori:

\[
a_k=\nu_2(3n_k+1)
\]

non sono libere.

Una lunga sequenza di valori:

\[
1,1,1,\dots,1
\]

impone che il numero iniziale cada in classi residue 2-adiche sempre più strette.

Per esempio:

\[
\nu_2(3n+1)=1
\]

equivale a:

\[
n\equiv 3\pmod 4
\]

Per una sequenza lunga di soli \(1\), i rappresentanti minimi seguono:

\[
3,7,15,31,63,127,\dots
\]

cioè:

\[
2^{k+1}-1
\]

Quindi i corridoi più espansivi si avvicinano a \(-1\) in senso 2-adico.

Questi corridoi sono sottili, ma quando vengono attraversati generano forte crescita.

---

## 7. Autostrada principale

Tra i numeri con massimo debito sotto 5 milioni è emersa una famiglia principale di confluenza.

Il tronco comune massimo è:

\[
8.216.025.965
\]

Questa famiglia contiene:

- 62 membri;
- 78 nodi comuni;
- minimo nodo comune del tronco: 428.885;
- media \(v_2\) del tronco: 2,111111;
- surplus per step: 0,526149;
- dissipativo da subito: sì.

Quindi la famiglia principale è una vera autostrada dissipativa.

---

## 8. Tronco principale: scarico del debito

Il tronco da:

\[
8.216.025.965
\]

a:

\[
1
\]

ha:

- 63 salti Syracuse;
- \(v_2\) totale: 133;
- media \(v_2\): 2,111111;
- surplus finale: +33,147362;
- massimo debito del tronco: 0.

La caduta più violenta osservata nel tronco è:

\[
428.885\rightarrow 2.513
\]

con:

\[
v_2=9
\]

Questo tronco non accumula debito: lo scarica.

---

## 9. Albero inverso del tronco principale

La mappa inversa di Syracuse è:

\[
S(n)=m
\]

quindi:

\[
\frac{3n+1}{2^a}=m
\]

Da cui:

\[
n=\frac{m2^a-1}{3}
\]

purché \(n\) sia intero, positivo e dispari.

Costruendo l'albero inverso del nodo:

\[
8.216.025.965
\]

con ricerca fino al valore del root e target sotto 5 milioni, si ottiene:

- nodi totali generati: 116.129;
- nodi sotto 5 milioni: 133;
- membri top-debito attesi: 62;
- membri trovati: 62;
- membri mancanti: 0;
- extra sotto 5 milioni: 71.

Quindi i 62 numeri ribelli non sono casuali: sono un sottoinsieme dei predecessori sotto 5 milioni del tronco dissipativo.

---

## 10. Membri top-debito vs extra

Confrontando i 62 membri ribelli con i 71 extra dello stesso albero inverso:

| Misura | Membri top-debito | Extra |
|---|---:|---:|
| max debt medio | 12,786329 | 11,153815 |
| max ratio medio | 8444,966694 | 2327,773039 |
| entry step medio | 85,000000 | 87,929577 |
| avg \(v_2\) medio | 1,433575 | 1,456776 |
| ratio \(v_2=1\) medio | 0,688817 | 0,680587 |

I membri top-debito hanno:

- media \(v_2\) più bassa;
- maggiore densità di \(v_2=1\);
- debito massimo più alto;
- crescita massima molto superiore.

Quindi i rami più pericolosi sono quelli che restano più a lungo in regime espansivo prima di entrare nel tronco dissipativo.

---

## 11. Famiglie di confluenza

Dall'analisi delle confluenze alte sono stati ottenuti:

- 6.670 nodi di confluenza;
- 344 famiglie distinte.

Una famiglia è definita come:

\[
\text{insieme di nodi comuni condivisi dallo stesso insieme di membri}
\]

Quindi non si studiano più singoli nodi, ma catene comuni.

---

## 12. Metriche globali delle famiglie

Sulle 344 famiglie:

- famiglie dissipative da subito: 77;
- percentuale dissipative da subito: 22,38%;
- media membri: 6,979651;
- media nodi comuni: 19,389535;
- media \(v_2\) dei tronchi: 1,847881;
- media surplus finale: +24,010594.

La media dei tronchi è quindi superiore alla soglia critica:

\[
1.847881>1.5849625
\]

Questo indica che, mediamente, le famiglie di confluenza sono dissipative.

---

## 13. Classificazione delle famiglie

Le 344 famiglie sono state classificate in categorie.

Conteggi principali:

| Classe | Numero famiglie |
|---|---:|
| F_MISTO | 144 |
| F_MISTO + G_MICRO | 108 |
| C_TRONCO_ALTO + E_DISSIPATIVO_DA_SUBITO | 38 |
| E_DISSIPATIVO_DA_SUBITO | 20 |
| B_CONFLUENZA_LARGA_CORTA + F_MISTO | 15 |
| D_ULTRA_DISSIPATIVO + E_DISSIPATIVO_DA_SUBITO | 6 |
| C_TRONCO_ALTO + C2_TRONCO_ESTREMO + E_DISSIPATIVO_DA_SUBITO | 4 |
| A_AUTOSTRADA_LARGA + E_DISSIPATIVO_DA_SUBITO | 2 |
| A_AUTOSTRADA_LARGA + C_TRONCO_ALTO + E_DISSIPATIVO_DA_SUBITO | 2 |

---

## 14. Tipi strutturali

### Tipo A — Autostrade larghe

Molti membri e molti nodi comuni.

Esempio:

\[
\text{id}=5166a862c128
\]

- membri: 62;
- nodi: 78;
- max common: \(8.216.025.965\);
- media \(v_2\): 2,111111;
- dissipativo da subito: sì.

### Tipo B — Confluenze larghe ma corte

Molti membri, pochi nodi comuni, spesso miste.

Esempio:

- membri: 61;
- nodi: 7;
- media \(v_2\): 1,793651;
- dissipativo da subito: no.

### Tipo C — Tronchi alti

Valore massimo comune superiore a:

\[
10^{10}
\]

Molti sono dissipativi da subito.

### Tipo C2 — Tronchi estremi

Valore massimo comune superiore a:

\[
10^{11}
\]

Esempio:

\[
207.572.633.873
\]

- membri: 2;
- nodi: 82;
- media \(v_2\): 1,979167;
- dissipativo da subito: sì.

### Tipo D — Ultra dissipativi

Surplus per step molto alto.

Esempio:

- media \(v_2\): 2,833333;
- surplus per step: 1,248371.

### Tipo F — Misti

Non sono dissipativi da subito, ma hanno surplus finale positivo.

Sono il tipo più numeroso.

---

## 15. Interpretazione teorica delle famiglie

La struttura osservata è:

\[
\text{corridoi 2-adici espansivi}
\rightarrow
\text{accumulo di debito}
\rightarrow
\text{confluenza}
\rightarrow
\text{tronchi dissipativi}
\rightarrow
1
\]

Le orbite ribelli non sembrano essere traiettorie isolate. Sembrano rami di alberi inversi che convergono in famiglie comuni.

La metafora del buco nero va quindi raffinata:

> Non esiste un unico imbuto semplice. Esiste una rete di corridoi espansivi 2-adici che confluisce in famiglie di tronchi dissipativi.

---

## 16. Necessità di una funzione quasi-Lyapunov

La sola funzione:

\[
\log(n)
\]

vede quando un'orbita scende localmente sotto il valore iniziale.

Ma questa discesa può essere ingannevole: alcuni numeri scendono subito sotto lo start e poi entrano in un corridoio fortemente espansivo.

Serviva quindi una funzione capace di misurare non solo la quota locale, ma anche il rischio futuro.

Questa ha portato alla costruzione della funzione:

\[
H(n)=\log(n)+\lambda D_{\max,80}(n)-\mu C_{\max,80}(n)+\theta P_{\max,80}(n)
\]

---

## 17. Debito futuro \(D_{\max,80}\)

Per una finestra futura di \(K=80\) passi Syracuse, definiamo:

\[
D(k)=k\log_2(3)-\sum_{i=1}^{k}a_i
\]

Il massimo debito futuro è:

\[
D_{\max,80}(n)=\max_{1\leq k\leq80}\left(k\log_2(3)-\sum_{i=1}^{k}a_i\right)
\]

Interpretazione:

- \(D_{\max,80}\) alto significa che nei prossimi 80 passi esiste una fase in cui la moltiplicazione per 3 domina la dissipazione per potenze di 2.
- È una misura di rischio espansivo futuro.

---

## 18. Cascata dissipativa futura \(C_{\max,80}\)

Definiamo il surplus dissipativo:

\[
C(k)=\sum_{i=1}^{k}a_i-k\log_2(3)
\]

Il massimo surplus futuro è:

\[
C_{\max,80}(n)=\max_{1\leq k\leq80}\left(\sum_{i=1}^{k}a_i-k\log_2(3)\right)
\]

Interpretazione:

- \(C_{\max,80}\) alto indica la presenza futura di una cascata dissipativa.
- Una cascata dissipativa è una fase in cui le divisioni per potenze di 2 superano nettamente la spinta del fattore 3.

Nella funzione \(H\), questo termine entra con segno negativo:

\[
-\mu C_{\max,80}(n)
\]

perché la presenza di una cascata futura riduce il rischio.

---

## 19. Pressione del corridoio \(v_2=1\): \(P_{\max,80}\)

Il fenomeno più pericoloso osservato è la persistenza di passi con:

\[
a_i=1
\]

Infatti, se \(a_i=1\), allora localmente:

\[
n_{i+1}\approx \frac{3}{2}n_i
\]

cioè la traiettoria cresce.

Definiamo quindi la pressione espansiva massima:

\[
P_{\max,80}(n)=\max_{1\leq k\leq80}\left(\frac{\#\{i\leq k : a_i=1\}}{k}\right)
\]

Interpretazione:

- \(P_{\max,80}\) alto significa che esiste un prefisso futuro con alta densità di passi \(v_2=1\).
- Questo è un indicatore molto forte di corridoi espansivi.

Nella funzione \(H\), entra con segno positivo:

\[
+\theta P_{\max,80}(n)
\]

perché maggiore pressione \(v_2=1\) significa maggiore rischio.

---

## 20. Funzione finale candidata

Dopo diversi test empirici, la candidata finale è:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

Interpretazione dei termini:

| Termine | Significato | Segno |
|---|---:|---:|
| \(\log(n)\) | quota locale del numero | positivo |
| \(D_{\max,80}\) | debito espansivo futuro | positivo |
| \(C_{\max,80}\) | cascata dissipativa futura | negativo |
| \(P_{\max,80}\) | pressione del corridoio \(v_2=1\) | positivo |

La funzione non chiede solo se il numero sia sceso sotto il punto di partenza. Chiede se la traiettoria sia davvero uscita dalla zona pericolosa.

---

## 21. Risultati empirici fino a 5 milioni

Sul range dei dispari fino a 5.000.000, la funzione ha prodotto:

- peggioramenti totali: 76;
- veri ribelli: 59;
- veri ribelli estremi: 14;
- falsi allarmi: 3.

Quindi:

\[
73\text{ peggioramenti su }76
\]

risultano strutturalmente significativi.

Questo è un passaggio importante: la funzione non trattiene numeri casuali, ma quasi solo numeri con vera instabilità futura.

---

## 22. Validazione empirica fino a 20 milioni

Sul range dei dispari fino a 20.000.000:

- dispari analizzati: 9.999.999;
- improved: 1.592.944;
- worsened: 408;
- same: 8.406.647;
- avg log step: 3,491526;
- avg H step: 3,141184;
- max log step: 181;
- max H step: 176;
- worst loss: 133 su \(n=12.826.025\);
- best gain: 80 su \(n=9.138.203\).

Classificazione dei 408 peggioramenti:

- vero ribelle: 297;
- vero ribelle estremo: 64;
- intermedio: 27;
- falso allarme: 20.

Quindi:

\[
361\text{ peggioramenti su }408
\]

sono veri ribelli o ribelli estremi.

La percentuale di peggioramenti è:

\[
\frac{408}{9.999.999}\approx0.0000408
\]

cioè circa:

\[
0.00408\%
\]

---

## 23. Caso estremo principale fino a 20 milioni

Il peggior loss osservato fino a 20 milioni è:

\[
n=12.826.025
\]

con:

- log_step = 1;
- H_step = 134;
- loss = 133;
- max_ratio = 2345,210;
- ratio \(v_2=1\) = 0,679104;
- \(P_{\max}\) al log-step = 1,000000;
- \(D_{\max}\) cresce di +1;
- \(C_{\max}\) scende di -0,415037.

Interpretazione:

Il log puro vede una discesa immediata, ma la funzione \(H\) riconosce che la traiettoria entra in un corridoio ad alta pressione espansiva. La successiva esplosione conferma che il peggioramento non è un errore, ma un segnale corretto di rischio.

---

## 24. Caso con massima espansione osservata fino a 20 milioni

Il massimo rapporto osservato tra valore massimo e valore iniziale tra i peggioramenti è:

\[
n=16.098.751
\]

con:

- max_ratio = 197.430,845;
- loss = 77;
- ratio \(v_2=1\) = 0,709677;
- \(P_{\max}\) al log-step = 1,000000;
- \(D_{\max}\) cresce di +7,300750.

Questo è un esempio particolarmente forte di orbita con discesa locale ingannevole e successiva esplosione massiccia.

---

## 25. Interpretazione geometrica

La funzione \(H\) può essere letta come una quota geometrica in un campo discreto:

- \(\log(n)\) misura l'altitudine numerica;
- \(D_{\max}\) misura la curvatura espansiva futura;
- \(C_{\max}\) misura la presenza di una via dissipativa;
- \(P_{\max}\) misura la pressione del corridoio \(v_2=1\).

In questa interpretazione, una traiettoria non è considerata sicura quando scende localmente, ma quando esce dalla regione in cui il campo futuro resta espansivo.

La metafora del buco nero diventa quindi:

> I numeri possono essere temporaneamente espulsi lungo corridoi 2-adici sottili, ma la rete di confluenze e tronchi dissipativi tende a riportarli verso il bacino finale.

---

## 26. Perché non è una dimostrazione

Questa costruzione non dimostra la Congettura di Collatz.

I motivi sono:

1. La funzione usa un lookahead finito di 80 passi.
2. I coefficienti sono empirici.
3. Non è ancora dimostrato che ogni orbita abbia un blocco futuro in cui \(H\) decresce.
4. Non è esclusa formalmente l'esistenza di un'orbita infinita che mantenga alto \(D_{\max}\) e \(P_{\max}\) senza mai entrare in cascata dissipativa sufficiente.

Quindi il risultato va considerato una formulazione sperimentale forte, non una prova.

---

## 27. Cosa manca per una dimostrazione

Per trasformare questi risultati in una dimostrazione servirebbe provare almeno una delle seguenti affermazioni generali.

### A. Ogni corridoio espansivo è finito

Una sequenza con alta densità di \(v_2=1\) non può continuare indefinitamente senza incontrare valori \(v_2\) più grandi.

### B. Il debito gravitazionale è limitato

Esiste un limite superiore effettivo per:

\[
D(k)=k\log_2(3)-\sum_{i=1}^{k}a_i
\]

lungo ogni orbita.

### C. Confluenza obbligata

Ogni ramo espansivo deve prima o poi entrare in una famiglia di confluenza.

### D. Dominanza dissipativa dei tronchi

Ogni famiglia sufficientemente profonda possiede un tronco con media \(v_2\) superiore a:

\[
\log_2(3)
\]

### E. Funzione di Lyapunov 2-adica

La via più promettente sarebbe costruire:

\[
H(n)=\log n+R(n)
\]

Dove \(R(n)\) misura la posizione 2-adica del numero rispetto ai corridoi espansivi.

Bisognerebbe dimostrare che per ogni \(n>1\) esiste \(k\) tale che:

\[
H(S^k(n))<H(n)
\]

---

## 28. Prossimo obiettivo matematico

Per trasformare questa teoria in qualcosa di più vicino a una dimostrazione, occorre eliminare la dipendenza dal lookahead empirico.

La domanda teorica centrale diventa:

> Esiste una costante universale \(K\) tale che per ogni dispari \(n>1\), entro \(K\) passi Syracuse oppure \(H(n)\) scende, oppure la traiettoria entra in una classe strutturalmente dissipativa dimostrabile?

Oppure, in forma più forte:

> Si può dimostrare che corridoi con alta pressione \(P_{\max}\) generano inevitabilmente, dopo un tempo finito, una cascata \(C_{\max}\) sufficiente a compensare il debito \(D_{\max}\)?

Questa è la vera porta verso una dimostrazione.

---

## 29. Prossimi esperimenti consigliati

### 29.1 Validazione a 100 milioni

Testare la funzione finale fino a:

\[
100.000.000
\]

Obiettivo:

- controllare la crescita dei peggioramenti;
- verificare se i falsi allarmi restano bassi;
- osservare se emergono nuove classi di ribelli.

### 29.2 Studio dei falsi allarmi

I falsi allarmi rimasti sono pochi. Vanno studiati separatamente per capire se:

- sono rumore della funzione;
- dipendono da \(P_{\max}\) troppo sensibile;
- richiedono una pressione netta, per esempio:

\[
P_{net}=P_{\max}-\alpha C_{\max}
\]

### 29.3 Studio dei ribelli estremi

I ribelli estremi sembrano avere firma comune:

- \(P_{\max}=1\);
- \(D_{\max}\) crescente;
- \(C_{\max}\) decrescente;
- alta densità di \(v_2=1\);
- grande max_ratio.

La domanda successiva è se questa firma implichi necessariamente una successiva cascata dissipativa.

---

## 30. Sintesi finale

La ricerca ha prodotto una formulazione più ordinata:

1. le salite sono prodotte da corridoi con alta densità di \(v_2=1\);
2. questi corridoi sono 2-adicamente sottili;
3. le orbite ribelli accumulano debito gravitazionale;
4. i rami ribelli confluiscono in famiglie comuni;
5. molte famiglie hanno tronchi dissipativi;
6. le famiglie alte ed estreme sono quasi sempre dissipative da subito;
7. la funzione quasi-Lyapunov \(H\) riconosce molte discese locali ingannevoli;
8. i peggioramenti di \(H\) corrispondono quasi sempre a traiettorie realmente instabili;
9. il comportamento suggerisce una rete gerarchica di attrazione verso 1.

La formulazione finale del programma di ricerca è:

\[
\boxed{
\text{Collatz come dinamica di corridoi 2-adici espansivi che confluiscono in tronchi dissipativi, misurabile tramite una quasi-Lyapunov a debito, cascata e pressione.}
}
\]

Questa non è ancora una dimostrazione, ma è una struttura teorica coerente su cui provare a costruire una funzione di Lyapunov formale.
