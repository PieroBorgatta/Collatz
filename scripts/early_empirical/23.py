from pathlib import Path


OUTPUT_FILE = "collatz_report_finale.md"


def main():
    report = r"""# Collatz/Syracuse — Teoria del Debito Gravitazionale e delle Famiglie di Confluenza

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
"""

    Path(OUTPUT_FILE).write_text(report, encoding="utf-8")

    print(f"Report finale generato: {OUTPUT_FILE}")
    print()
    print("Per aprirlo:")
    print(f"open '{OUTPUT_FILE}'")


if __name__ == "__main__":
    main()
