# Teoria del Debito Gravitazionale nella Mappa di Collatz/Syracuse

## 1. Premessa

La Congettura di Collatz afferma che, partendo da qualsiasi intero positivo \(n\), iterando la funzione:

\[
C(n)=
\begin{cases}
n/2 & \text{se } n \text{ è pari}\\
3n+1 & \text{se } n \text{ è dispari}
\end{cases}
\]

si raggiunge sempre il ciclo finale:

\[
1 \rightarrow 4 \rightarrow 2 \rightarrow 1
\]

Per eliminare i passi pari intermedi, si lavora sulla mappa accelerata di Syracuse, definita sui dispari:

\[
S(n)=\frac{3n+1}{2^{\nu_2(3n+1)}}
\]

dove:

\[
\nu_2(m)
\]

è il massimo esponente \(a\) tale che \(2^a\) divide \(m\).

---

## 2. Potenziale logaritmico

A ogni numero dispari \(n\) associamo un potenziale:

\[
V(n)=\log n
\]

Un passo Syracuse produce approssimativamente:

\[
S(n)\approx n\cdot\frac{3}{2^a}
\]

dove:

\[
a=\nu_2(3n+1)
\]

La variazione logaritmica approssimata è:

\[
\Delta V \approx \log 3-a\log 2
\]

La soglia critica è quindi:

\[
a > \log_2(3)
\]

Poiché:

\[
\log_2(3)\approx 1,5849625
\]

un tratto orbitale è mediamente dissipativo quando:

\[
\overline{a}>1,5849625
\]

ed è mediamente espansivo quando:

\[
\overline{a}<1,5849625
\]

---

## 3. Debito gravitazionale

Definiamo il debito gravitazionale dopo \(k\) passi Syracuse come:

\[
D(k)=k\log_2(3)-\sum_{i=1}^{k}a_i
\]

dove:

\[
a_i=\nu_2(3n_i+1)
\]

Interpretazione:

- se \(D(k)>0\), l'orbita ha accumulato vantaggio espansivo;
- se \(D(k)<0\), la contrazione ha dominato;
- il massimo di \(D(k)\) misura quanto un'orbita riesce a “resistere alla gravità”.

---

## 4. Primo caso estremo: \(n=3.041.127\)

Uno dei numeri più esplosivi trovati sotto 5 milioni è:

\[
n=3.041.127
\]

Risultati:

- massimo valore raggiunto: \(207.572.633.873\)
- rapporto massimo rispetto allo start: circa \(68.255\)
- step del picco: 36
- primo rientro sotto lo start: 62
- salti Syracuse totali fino a 1: 132
- massima sequenza consecutiva di \(v2=1\): 17
- media finale \(v2\): 1,75

Poiché:

\[
1,75 > \log_2(3)
\]

la traiettoria, pur avendo una fase esplosiva, è complessivamente dissipativa.

---

## 5. Autostrada gravitazionale comune

Analizzando i numeri con massimo debito sotto 5 milioni, è emerso un tronco comune:

\[
8.216.025.965
\]

Questo tronco è condiviso da 62 numeri ribelli distinti.

Caratteristiche del tronco:

- valore iniziale: \(8.216.025.965\)
- valore finale: 1
- salti Syracuse: 63
- \(v2\) totale: 133
- media \(v2\): 2,111111
- surplus finale: +33,147362
- massimo debito: 0

Il tronco è quindi fortemente dissipativo.

La caduta più violenta del tronco è:

\[
428.885 \rightarrow 2.513
\]

con:

\[
v2=9
\]

e rapporto:

\[
0,005859379554
\]

---

## 6. Struttura a due fasi

I 62 numeri ribelli seguono una dinamica in due fasi.

### Fase 1 — Pre-ingresso

Prima di entrare nel tronco comune, i numeri hanno media \(v2\) inferiore alla soglia critica.

Valori tipici:

\[
\overline{v2}\approx 1,40 - 1,46
\]

Poiché:

\[
1,40 - 1,46 < \log_2(3)
\]

questa fase è espansiva.

In questa fase i numeri accumulano debito gravitazionale.

### Fase 2 — Tronco comune

Dopo l'ingresso nel tronco:

\[
8.216.025.965
\]

la media diventa:

\[
\overline{v2}=2,111111
\]

quindi:

\[
2,111111 > \log_2(3)
\]

Il tronco scarica il debito accumulato e porta l'orbita fino a 1.

---

## 7. Albero inverso del tronco

La mappa inversa di Syracuse è data da:

\[
S(n)=m
\]

cioè:

\[
\frac{3n+1}{2^a}=m
\]

da cui:

\[
n=\frac{m2^a-1}{3}
\]

purché \(n\) sia intero, dispari e positivo.

Costruendo l'albero inverso del nodo:

\[
8.216.025.965
\]

con limite di ricerca pari al valore del root e target sotto 5 milioni, si ottiene:

- nodi totali generati: 116.129
- nodi sotto 5 milioni: 133
- membri top-debito attesi: 62
- membri trovati: 62
- membri mancanti: 0
- extra sotto 5 milioni: 71

Quindi i 62 numeri ribelli sono esattamente un sottoinsieme dei predecessori sotto 5 milioni del tronco comune.

---

## 8. Membri top-debito vs extra

Confrontando i 62 membri top-debito con i 71 extra dello stesso albero inverso:

| Misura | Membri top-debito | Extra |
|---|---:|---:|
| max debt medio | 12,786329 | 11,153815 |
| max ratio medio | 8444,966694 | 2327,773039 |
| entry step medio | 85,000000 | 87,929577 |
| avg v2 medio | 1,433575 | 1,456776 |
| ratio v2=1 medio | 0,688817 | 0,680587 |

Interpretazione:

I membri top-debito hanno:

- maggiore densità di \(v2=1\);
- media \(v2\) più bassa;
- debito massimo più alto;
- crescita massima molto superiore.

Quindi i rami più pericolosi dell'albero inverso sono quelli che mantengono più a lungo una dinamica espansiva.

---

## 9. Teoria risultante

La teoria può essere formulata così:

> Le orbite di Collatz/Syracuse possono salire solo entrando in corridoi 2-adici sottili caratterizzati da alta densità di valori \(v2=1\). Questi corridoi accumulano debito gravitazionale, ma tendono a confluire in tronchi comuni dissipativi, dove blocchi con valori \(v2\) elevati scaricano il debito e portano l'orbita verso 1.

In forma sintetica:

\[
\text{corridoio espansivo} \rightarrow \text{debito} \rightarrow \text{confluenza} \rightarrow \text{tronco dissipativo}
\]

---

## 10. Cosa manca per una dimostrazione

Questi risultati non costituiscono ancora una dimostrazione della Congettura di Collatz.

Per arrivare a una dimostrazione servirebbe provare almeno una delle seguenti affermazioni generali:

### A. Debito limitato

Esiste una funzione \(B(n)\) tale che per ogni orbita:

\[
D(k) \leq B(n)
\]

e il debito non può crescere indefinitamente.

### B. Confluenza obbligata

Ogni corridoio espansivo deve prima o poi confluire in un tronco dissipativo.

### C. Dominanza dei tronchi dissipativi

Ogni tronco sufficientemente profondo dell'albero inverso possiede una media \(v2\) superiore a:

\[
\log_2(3)
\]

### D. Funzione di Lyapunov corretta

Esiste una funzione:

\[
H(n)=\log n+R(n)
\]

dove \(R(n)\) è un termine aritmetico 2-adico, tale che per ogni \(n>1\) esiste \(k\) con:

\[
H(S^k(n))<H(n)
\]

Questa sarebbe la via più promettente verso una dimostrazione.

---

## 11. Conclusione

Il lavoro computazionale suggerisce una struttura non casuale:

1. le fasi espansive sono legate a sequenze con alta densità di \(v2=1\);
2. tali sequenze corrispondono a corridoi 2-adici rari;
3. i corridoi espansivi non restano isolati;
4. confluiscono in tronchi comuni;
5. i tronchi comuni osservati sono fortemente dissipativi;
6. il collasso avviene quando il surplus \(v2\) supera definitivamente il debito accumulato.

La metafora fisica corretta non è semplicemente “buco nero”, ma:

> una rete di corridoi espansivi sottili che confluisce in canali dissipativi ad alta densità di divisioni per 2.

Questa formulazione è più rigorosa e può essere usata come programma di ricerca.


---

## 12. Estensione: funzione Quasi-Lyapunov empirica

La teoria del debito gravitazionale suggerisce naturalmente la ricerca di una funzione di energia che non misuri solo la quota locale \(\log(n)\), ma anche il rischio futuro associato ai corridoi 2-adici.

La candidata empirica principale è:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

Questa funzione va letta come una quota gravitazionale corretta.

- \(\log(n)\): quota numerica locale;
- \(D_{\max,80}\): debito gravitazionale futuro;
- \(C_{\max,80}\): cascata dissipativa futura;
- \(P_{\max,80}\): pressione del corridoio \(v2=1\).

---

## 13. Definizioni operative

Per una finestra futura di 80 passi Syracuse, definiamo:

\[
D_{\max,80}(n)=\max_{1\leq k\leq80}\left(k\log_2(3)-\sum_{i=1}^{k}a_i\right)
\]

\[
C_{\max,80}(n)=\max_{1\leq k\leq80}\left(\sum_{i=1}^{k}a_i-k\log_2(3)\right)
\]

\[
P_{\max,80}(n)=\max_{1\leq k\leq80}\left(\frac{\#\{i\leq k:a_i=1\}}{k}\right)
\]

Interpretazione:

- \(D_{\max,80}\) misura quanto il numero può ancora salire;
- \(C_{\max,80}\) misura se esiste una cascata che può scaricare il debito;
- \(P_{\max,80}\) misura la pressione espansiva data dai passi con \(v2=1\).

---

## 14. Significato fisico della funzione

La funzione \(H\) considera un numero davvero in caduta solo quando la sua quota corretta scende.

Una traiettoria può avere:

\[
S^k(n)<n
\]

ma ancora:

\[
H(S^k(n))\geq H(n)
\]

Questo significa che la discesa numerica è solo apparente: il numero si trova ancora in una regione futura ad alto debito o ad alta pressione \(v2=1\).

La metafora gravitazionale diventa quindi:

> non basta cadere di quota; bisogna uscire dal corridoio espansivo.

---

## 15. Validazione fino a 20 milioni

Sul range dei dispari fino a 20 milioni:

- dispari analizzati: 9.999.999;
- improved: 1.592.944;
- worsened: 408;
- same: 8.406.647;
- avg log step: 3,491526;
- avg H step: 3,141184;
- max log step: 181;
- max H step: 176.

Classificazione dei 408 peggioramenti:

| Classe | Conteggio |
|---|---:|
| VERO_RIBELLE | 297 |
| VERO_RIBELLE_ESTREMO | 64 |
| INTERMEDIO | 27 |
| FALSO_ALLARME | 20 |

Quindi la funzione trattiene quasi sempre numeri effettivamente pericolosi.

---

## 16. Validazione fino a 100 milioni

Sul range dei dispari fino a 100 milioni:

- dispari analizzati: 49.999.999;
- improved: 8.019.345;
- worsened: 2.839;
- same: 41.977.815;
- avg log step: 3,492657;
- avg H step: 3,131343;
- max log step: 237;
- max H step: 190;
- worst loss: 151 su \(n=52.369.065\);
- best gain: 124 su \(n=20.638.335\).

Classificazione dei peggioramenti:

| Classe | Conteggio |
|---|---:|
| VERO_RIBELLE | 2.066 |
| VERO_RIBELLE_ESTREMO | 399 |
| INTERMEDIO | 207 |
| FALSO_ALLARME | 167 |

La maggioranza dei peggioramenti resta quindi strutturalmente significativa.

---

## 17. Esperimento \(T_{risk}\)

È stata testata una micro-correzione:

\[
H_{TR}(n)=H(n)+\eta T_{risk}(n)
\]

con:

\[
T_{risk}(n)=\max(0,T^*_{80}(n)-\alpha C_{\max,80}(n))
\]

Il candidato più pulito a 20 milioni è stato:

\[
\alpha=1.00,
\qquad
\eta=0.0025
\]

A 100 milioni:

| Metrica | Base \(H\) | \(H_{TR}\) |
|---|---:|---:|
| Avg step | 3,131343 | 3,130929 |
| Max step | 190 | 190 |
| Worsened | 2.839 | 2.845 |
| Falsi allarmi | 167 | 167 |

Il guadagno è troppo piccolo per giustificare la maggiore complessità.

Quindi \(T_{risk}\) resta una nota sperimentale, non la nuova formula finale.

---

## 18. Formula attuale consigliata

La forma attuale più equilibrata è:

\[
\boxed{
H(n)=\log(n)+0.28D_{\max,80}(n)-0.03C_{\max,80}(n)+0.30P_{\max,80}(n)
}
\]

Il suo significato gravitazionale è:

\[
\text{quota corretta}
=
\text{quota locale}
+
\text{debito futuro}
-
\text{cascata futura}
+
\text{pressione espansiva}
\]

Questa è la migliore formulazione empirica attuale della teoria del debito gravitazionale.

---

## 19. Prossimo problema teorico

Il punto debole osservato a 100 milioni sono i falsi allarmi.

Il prossimo passo non è aggiungere nuovi termini, ma capire quando \(P_{\max,80}\) sovrastima il rischio.

Una possibile variante futura è ignorare prefissi troppo corti:

\[
P^{(m)}_{\max,80}(n)=
\max_{m\leq k\leq80}
\frac{\#\{i\leq k:a_i=1\}}{k}
\]

Questo eviterebbe che una pressione iniziale breve ma innocua venga interpretata come vero corridoio espansivo.

---

## 20. Conclusione aggiornata

La teoria aggiornata può essere riassunta così:

> Le orbite salgono quando entrano in corridoi 2-adici ad alta densità di \(v2=1\). Questi corridoi accumulano debito gravitazionale. La caduta avviene quando l'orbita confluisce in tronchi dissipativi o incontra cascate sufficienti a scaricare il debito.

La funzione \(H\) rende questa idea misurabile.

Non è una dimostrazione, ma è una candidata quasi-Lyapunov empirica coerente con la struttura osservata.
