# Collatz/Syracuse — Teoria del Debito Gravitazionale e delle Famiglie di Confluenza

## 1. Obiettivo

Lo scopo di questa ricerca non è dichiarare risolta la Congettura di Collatz, ma costruire un quadro strutturale più preciso per descrivere il comportamento delle orbite.

L'idea centrale è interpretare la dinamica della mappa accelerata di Syracuse come una competizione tra:

- espansione prodotta dal fattore \(3n+1\);
- dissipazione prodotta dalle divisioni per potenze di 2;
- confluenza delle orbite in tronchi comuni.

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

dove:

\[
\nu_2(m)
\]

è il massimo esponente \(a\) tale che \(2^a\mid m\).

Un passo Syracuse è quindi:

\[
n_{k+1}=S(n_k)
\]

con:

\[
a_k=\nu_2(3n_k+1)
\]

---

## 3. Soglia critica

Approssimativamente:

\[
S(n)\approx n\cdot \frac{3}{2^a}
\]

Quindi la variazione logaritmica è dominata da:

\[
\log 3-a\log 2
\]

La soglia critica è:

\[
a>\log_2(3)
\]

e:

\[
\log_2(3)\approx 1,5849625
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
- \(\max D(k)\): misura la resistenza dell'orbita alla caduta.

La formulazione fisica è:

\[
\text{debito}=\text{espansione attesa}-\text{divisioni per 2 accumulate}
\]

---

## 5. Primo caso estremo: \(n=3.041.127\)

Uno dei numeri più esplosivi trovati sotto 5 milioni è:

\[
n=3.041.127
\]

Risultati:

- picco massimo: \(207.572.633.873\)
- rapporto massimo rispetto allo start: circa \(68.255\)
- step del picco: 36
- primo rientro sotto lo start: 62
- salti Syracuse fino a 1: 132
- massima sequenza consecutiva di \(v2=1\): 17
- media finale \(v2\): 1,75

Poiché:

\[
1,75>\log_2(3)
\]

la traiettoria, pur essendo inizialmente esplosiva, è complessivamente dissipativa.

---

## 6. Corridoi 2-adici

Le sequenze di valori \(a_k=\nu_2(3n_k+1)\) non sono libere.

Una lunga sequenza di valori:

\[
1,1,1,\dots,1
\]

impone che il numero iniziale cada in classi residue 2-adiche sempre più strette.

Per esempio:

\[
v2(3n+1)=1
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
- media \(v2\) del tronco: 2,111111;
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
- \(v2\) totale: 133;
- media \(v2\): 2,111111;
- surplus finale: +33,147362;
- massimo debito del tronco: 0.

La caduta più violenta osservata nel tronco è:

\[
428.885\rightarrow 2.513
\]

con:

\[
v2=9
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

da cui:

\[
n=\frac{m2^a-1}{3}
\]

purché \(n\) sia intero, positivo e dispari.

Costruendo l'albero inverso del nodo \(8.216.025.965\), con ricerca fino al valore del root e target sotto 5 milioni, si ottiene:

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
| avg v2 medio | 1,433575 | 1,456776 |
| ratio \(v2=1\) medio | 0,688817 | 0,680587 |

I membri top-debito hanno:

- media \(v2\) più bassa;
- maggiore densità di \(v2=1\);
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
- media \(v2\) dei tronchi: 1,847881;
- media surplus finale: +24,010594.

La media dei tronchi è quindi superiore alla soglia critica:

\[
1,847881>1,5849625
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

- membri: 62
- nodi: 78
- max common: \(8.216.025.965\)
- media \(v2\): 2,111111
- dissipativo da subito: sì.

### Tipo B — Confluenze larghe ma corte

Molti membri, pochi nodi comuni, spesso miste.

Esempio:

- membri: 61
- nodi: 7
- media \(v2\): 1,793651
- dissipativo da subito: no.

### Tipo C — Tronchi alti

Valore massimo comune superiore a \(10^{10}\).

Molti sono dissipativi da subito.

### Tipo C2 — Tronchi estremi

Valore massimo comune superiore a \(10^{11}\).

Esempio:

\[
207.572.633.873
\]

- membri: 2
- nodi: 82
- media \(v2\): 1,979167
- dissipativo da subito: sì.

### Tipo D — Ultra dissipativi

Surplus per step molto alto.

Esempio:

- media \(v2\): 2,833333
- surplus per step: 1,248371.

### Tipo F — Misti

Non sono dissipativi da subito, ma hanno surplus finale positivo.

Sono il tipo più numeroso.

---

## 15. Interpretazione teorica

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

## 16. Cosa manca per una dimostrazione

Questi risultati sono computazionali e strutturali. Non dimostrano ancora la Congettura di Collatz.

Per trasformarli in una dimostrazione servirebbe provare almeno una di queste affermazioni generali.

### A. Ogni corridoio espansivo è finito

Una sequenza con alta densità di \(v2=1\) non può continuare indefinitamente senza incontrare valori \(v2\) più grandi.

### B. Il debito gravitazionale è limitato

Esiste un limite superiore effettivo per:

\[
D(k)=k\log_2(3)-\sum_{i=1}^{k}a_i
\]

lungo ogni orbita.

### C. Confluenza obbligata

Ogni ramo espansivo deve prima o poi entrare in una famiglia di confluenza.

### D. Dominanza dissipativa dei tronchi

Ogni famiglia sufficientemente profonda possiede un tronco con media \(v2\) superiore a:

\[
\log_2(3)
\]

### E. Funzione di Lyapunov 2-adica

La via più promettente sarebbe costruire:

\[
H(n)=\log n+R(n)
\]

dove \(R(n)\) misura la posizione 2-adica del numero rispetto ai corridoi espansivi.

Bisognerebbe dimostrare che per ogni \(n>1\) esiste \(k\) tale che:

\[
H(S^k(n))<H(n)
\]

---

## 17. Conclusione

La ricerca ha prodotto una formulazione più ordinata:

1. le salite sono prodotte da corridoi con alta densità di \(v2=1\);
2. questi corridoi sono 2-adicamente sottili;
3. le orbite ribelli accumulano debito gravitazionale;
4. i rami ribelli confluiscono in famiglie comuni;
5. molte famiglie hanno tronchi dissipativi;
6. le famiglie alte ed estreme sono quasi sempre dissipative da subito;
7. il comportamento suggerisce una rete gerarchica di attrazione verso 1.

La formulazione finale del programma di ricerca è:

\[
\boxed{
\text{Collatz come dinamica di corridoi 2-adici espansivi che confluiscono in tronchi dissipativi}
}
\]

Questa non è ancora una dimostrazione, ma è una struttura teorica coerente su cui provare a costruire una funzione di Lyapunov.


---

## 18. Funzione Quasi-Lyapunov empirica

Dopo l'analisi delle famiglie di confluenza, la ricerca è stata estesa alla costruzione di una funzione di energia empirica capace di distinguere tra:

- una semplice discesa locale sotto il valore iniziale;
- una vera uscita dal corridoio espansivo;
- una traiettoria che scende temporaneamente, ma rimane in una regione futura ad alto rischio.

La candidata principale è:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

dove i termini aggiuntivi sono calcolati su una finestra futura di 80 passi Syracuse.

### 18.1 Debito espansivo futuro

\[
D_{\max,80}(n)=\max_{1\leq k\leq80}\left(k\log_2(3)-\sum_{i=1}^{k}a_i\right)
\]

Misura il massimo debito espansivo visibile nei prossimi 80 passi.

### 18.2 Cascata dissipativa futura

\[
C_{\max,80}(n)=\max_{1\leq k\leq80}\left(\sum_{i=1}^{k}a_i-k\log_2(3)\right)
\]

Misura la massima cascata dissipativa futura.

### 18.3 Pressione del corridoio \(v2=1\)

\[
P_{\max,80}(n)=\max_{1\leq k\leq80}\left(\frac{\#\{i\leq k:a_i=1\}}{k}\right)
\]

Misura la massima densità iniziale di passi con \(v2=1\). È un indicatore di pressione espansiva 2-adica.

---

## 19. Interpretazione della funzione \(H\)

La funzione \(H\) non misura solo se un numero è diventato più piccolo.

Misura se la traiettoria è uscita dalla regione pericolosa.

In particolare:

- \(\log(n)\) misura la quota locale;
- \(D_{\max,80}\) penalizza il debito espansivo futuro;
- \(C_{\max,80}\) premia la presenza di una cascata dissipativa;
- \(P_{\max,80}\) penalizza i corridoi futuri con alta densità di \(v2=1\).

Quindi una discesa locale può non essere considerata una vera discesa energetica se il numero, subito dopo, entra in un corridoio espansivo.

Questa è la differenza centrale tra:

\[
\log(n)
\]

che vede solo la quota numerica, e:

\[
H(n)
\]

che vede anche la struttura 2-adica futura.

---

## 20. Validazione empirica fino a 20 milioni

Sul range:

\[
1<n\leq20.000.000
\]

considerando solo i dispari, sono stati analizzati:

\[
9.999.999
\]

valori.

La funzione \(H\) ha prodotto:

| Metrica | Valore |
|---|---:|
| Improved | 1.592.944 |
| Worsened | 408 |
| Same | 8.406.647 |
| Avg log step | 3,491526 |
| Avg H step | 3,141184 |
| Max log step | 181 |
| Max H step | 176 |
| Worst loss | 133 su \(n=12.826.025\) |
| Best gain | 80 su \(n=9.138.203\) |

Classificazione dei 408 peggioramenti:

| Classe | Conteggio |
|---|---:|
| VERO_RIBELLE | 297 |
| VERO_RIBELLE_ESTREMO | 64 |
| INTERMEDIO | 27 |
| FALSO_ALLARME | 20 |

Quindi 361 peggioramenti su 408 sono veri ribelli o ribelli estremi.

---

## 21. Validazione empirica fino a 100 milioni

Sul range:

\[
1<n\leq100.000.000
\]

considerando solo i dispari, sono stati analizzati:

\[
49.999.999
\]

valori.

La funzione \(H\) ha prodotto:

| Metrica | Valore |
|---|---:|
| Improved | 8.019.345 |
| Worsened | 2.839 |
| Same | 41.977.815 |
| Avg log step | 3,492657 |
| Avg H step | 3,131343 |
| Max log step | 237 |
| Max H step | 190 |
| Worst loss | 151 su \(n=52.369.065\) |
| Best gain | 124 su \(n=20.638.335\) |

Classificazione dei 2.839 peggioramenti:

| Classe | Conteggio |
|---|---:|
| VERO_RIBELLE | 2.066 |
| VERO_RIBELLE_ESTREMO | 399 |
| INTERMEDIO | 207 |
| FALSO_ALLARME | 167 |

Quindi 2.465 peggioramenti su 2.839 sono veri ribelli o estremi.

La funzione mantiene quindi una buona selettività anche a 100 milioni: peggiora pochissimi casi, e la maggioranza dei peggioramenti corrisponde a traiettorie realmente espansive.

---

## 22. Casi estremi osservati a 100 milioni

### 22.1 Peggior loss

Il peggior caso per differenza tra step logaritmico e step energetico è:

\[
n=52.369.065
\]

con:

- log step: 1;
- H step: 152 circa nella variante con micro-correzione, 152/151 nell'intorno sperimentale;
- loss: 151;
- max ratio: circa 1.949.604;
- ratio \(v2=1\): circa 0,671;
- \(P_{\max}\) al log-step: 1,000000.

Interpretazione:

Il numero scende subito sotto il valore iniziale, ma rimane in una regione futura estremamente espansiva. La funzione \(H\) fa bene a non considerare quella discesa come una vera uscita dal pericolo.

### 22.2 Massima espansione osservata

Uno dei casi più violenti per rapporto massimo è:

\[
n=31.033.519
\]

con:

- max ratio: circa 3.289.958;
- loss: circa 150;
- ratio \(v2=1\): circa 0,665;
- \(P_{\max}\) al log-step: 1,000000.

Anche questo caso conferma il ruolo dei corridoi ad alta pressione \(v2=1\).

---

## 23. Esperimento sulla micro-correzione \(T_{risk}\)

È stata testata una variante della funzione:

\[
H_{TR}(n)=H(n)+\eta T_{risk}(n)
\]

con:

\[
T_{risk}(n)=\max(0,T^*_{80}(n)-\alpha C_{\max,80}(n))
\]

Il test più stabile a 20 milioni ha suggerito:

\[
\alpha=1.00,
\qquad
\eta=0.0025
\]

A 20 milioni questa micro-correzione ha prodotto un miglioramento minimo della media, mantenendo basso il numero di falsi allarmi.

La validazione a 100 milioni ha dato:

| Metrica | Base \(H\) 100M | \(H_{TR}\) 100M |
|---|---:|---:|
| Avg step | 3,131343 | 3,130929 |
| Max step | 190 | 190 |
| Worsened | 2.839 | 2.845 |
| Falsi allarmi | 167 | 167 |

Conclusione:

\[
H_{TR}
\]

è stabile, ma il guadagno è troppo piccolo rispetto alla maggiore complessità teorica.

La micro-correzione \(T_{risk}\) viene quindi archiviata come nota sperimentale, non come nuova funzione finale.

La candidata principale resta:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

---

## 24. Analisi dei falsi allarmi a 100 milioni

Dopo la validazione della funzione base \(H\) a 100 milioni, sono stati analizzati separatamente i 167 casi classificati come falso allarme.

Lo scopo non era dimostrare la Congettura di Collatz, né costruire una nuova funzione ad hoc, ma capire se i falsi allarmi fossero dovuti a un difetto semplice della pressione \(P_{\max,80}\).

### 24.1 Risultato dello script 46

Lo script:

```text
46_analyze_false_alarms.py
```

ha analizzato i peggioramenti della funzione base \(H\), usando come input il CSV della validazione a 100 milioni.

Distribuzione confermata:

| Classe | Conteggio |
|---|---:|
| VERO_RIBELLE | 2.066 |
| VERO_RIBELLE_ESTREMO | 399 |
| INTERMEDIO | 207 |
| FALSO_ALLARME | 167 |

I falsi allarmi risultano quasi sempre micro-peggioramenti:

| Metrica | FALSO_ALLARME | VERO_RIBELLE* |
|---|---:|---:|
| loss mediana | 1 | 7 |
| loss media | 1,263473 | 24,723327 |
| max_ratio mediana | 1,000000 | 6,248946 |
| ratio_1_until_h mediana | 0,000000 | 0,575000 |
| h_delta_at_log_step mediana | circa 0,009769 | maggiore e più distribuito |

Quindi i falsi allarmi non sono traiettorie realmente esplosive: sono casi in cui \(H\) resta appena sopra il riferimento logaritmico per pochi passi, con margine molto piccolo.

### 24.2 Test della pressione robusta

È stata testata l'ipotesi che \(P_{\max,80}\) fosse troppo sensibile ai prefissi corti.

La variante descrittiva considerata è:

\[
P^{(m)}_{\max,80}(n)=
\max_{m\leq k\leq80}
\frac{\#\{i\leq k:a_i=1\}}{k}
\]

con:

\[
m=4,6,8,10,12
\]

Il risultato è stato negativo per una sostituzione secca: rimuovere i prefissi corti colpisce più spesso i veri ribelli che i falsi allarmi.

Per esempio, l'analisi dei drop:

\[
P_{\max,80}-P^{(m)}_{\max,80}
\]

mostra che molte orbite realmente ribelli hanno proprio una pressione iniziale breve ma significativa.

Quindi \(P_{\max,80}\) non va sostituito direttamente con una versione robusta.

---

## 25. Test della penalizzazione dei falsi deboli

È stato poi testato uno schema esplorativo:

\[
H_{47}(n)=H(n)-\gamma W(n)
\]

con:

\[
W(n)=
\max(0,P_{\max,80}(n)-P^{(m)}_{\max,80}(n))
\cdot
\max(0,\theta-r_{1,80}(n))
\]

L'idea era penalizzare solo la pressione breve non sostenuta da una densità globale elevata di \(a_i=1\) nei primi 80 passi.

Il miglior caso dello scan ha ottenuto:

| Parametri | Falsi corretti | Veri ribelli colpiti | Intermedi colpiti |
|---|---:|---:|---:|
| \(m=4,\theta=0,675,\gamma=5\) | 17 / 167 | 212 / 2.465 | 29 / 207 |

Il risultato è stato giudicato non selettivo.

Per correggere pochi falsi allarmi, la penalizzazione elimina troppi veri ribelli.

Quindi la variante:

\[
H_{47}
\]

non viene promossa.

---

## 26. Regole descrittive ex-post

Lo script:

```text
48_false_alarm_rules_fast.py
```

ha cercato regole descrittive ex-post del tipo:

\[
loss\leq L,
\qquad
max\_ratio\leq R,
\qquad
ratio\_1\_until\_h\leq Q,
\qquad
h\_delta\_at\_log\_step\leq E
\]

Queste regole non possono entrare direttamente in \(H(n)\), perché usano informazioni osservate dopo l'evoluzione dell'orbita. Servono solo per classificare la natura dei peggioramenti.

La migliore regola descrittiva trovata è:

\[
loss\leq3,
\qquad
max\_ratio\leq1,
\qquad
ratio\_1\_until\_h\leq0,25,
\qquad
h\_delta\_at\_log\_step\leq0,015
\]

Risultato:

| Metrica | Valore |
|---|---:|
| Casi selezionati | 142 |
| Falsi allarmi intercettati | 107 / 167 |
| Precisione sui falsi | 75,35% |
| Intermedi intercettati | 0 |
| Veri ribelli intercettati | 35 / 2.465 |
| Estremi intercettati | 0 |

La regola separa bene una famiglia di falsi allarmi deboli, ma non è perfetta: intercetta anche 35 veri ribelli non estremi.

Inoltre non è stata trovata alcuna regola pulita con:

- almeno 5 falsi allarmi intercettati;
- zero estremi;
- al massimo 10 veri ribelli intercettati.

Conclusione: i falsi allarmi sono parzialmente descrivibili, ma non separabili in modo pulito dai veri ribelli non estremi tramite soglie semplici.

---

## 27. Stato attuale della teoria

La forma più aggiornata del programma di ricerca è:

\[
\boxed{
\text{corridoi 2-adici espansivi}
\rightarrow
\text{debito}
\rightarrow
\text{confluenza}
\rightarrow
\text{tronchi dissipativi}
}
\]

con una funzione quasi-Lyapunov empirica:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

La funzione non dimostra la Congettura di Collatz, ma fornisce un criterio sperimentale più raffinato del semplice \(\log(n)\): non basta scendere localmente, bisogna anche uscire dalla regione futura di pressione espansiva.

Il prossimo obiettivo non è aggiungere nuovi termini alla cieca, ma consolidare la classificazione empirica dei peggioramenti e cercare una formulazione più dimostrabile del ruolo della pressione 2-adica.
