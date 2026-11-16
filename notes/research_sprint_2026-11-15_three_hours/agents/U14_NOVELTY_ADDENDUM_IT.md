# U14 — Addendum di novità: massimo inverso e soglia esatta del cap

Valutazione bibliografica mirata, 15 novembre 2026, successiva a `U14_V7_NOVELTY_IT.md`. Letti U12, U15_MAXPLUS, U15_FINITE_CAP e l'audit U04_MAXPLUS, che conclude PASS anche sulle due note U15. Nessuna modifica al manoscritto, PDF, pubblicazione, esperimento, Lean o Git. Questa nota aggiorna il giudizio editoriale; non è una rivendicazione di priorità globale.

## Esito

Il nuovo raccordo rafforza il motivo per **preparare una v7 tecnica**, ma non giustifica un deposito immediato o il linguaggio «nessuno l'ha mai tentato». Il nucleo più caratteristico è l'identificazione del massimo aritmetico con la soglia ESATTA della traccia intera capped. L'esistenza del massimo, il suo profilo unico e la terminazione della policy ottimale hanno spiegazioni brevi a partire da ingredienti noti: da soli sarebbero un titolo troppo ambizioso per il contenuto.

Nelle fonti primarie direttamente controllate non ho trovato l'enunciato preciso «la traccia capped a un intero è una funzione a gradini finita, con soglia minima F e ultimo salto esplicito». Ho trovato invece precedenti diretti per l'ottimizzazione a profondità fissata, il Green intero, la traccia Cesàro armonica e il taglio del massimo moltiplicatore. **Risultato nuovo per il progetto; priorità globale non accertata.** Il mancato risultato di una ricerca per parole chiave non prova novità.

## Il confronto che ridimensiona la novità della sola funzione F

La [fonte127, §12](https://rstation.ai/problems/collatz/papers/127) definisce già `C_k(n)`, minimo del totale degli esponenti sulle parole inverse legali di k passi dispari, con stati unità. Specializzando a un target intero positivo unità, ogni cammino legale resta positivo ed è un vero cammino intero. Con `C_0=0` segue esattamente

`F(n)=sup_(k≥0) 3^k 2^(−C_k(n))`.

L'ottimizzazione a profondità fissata è dunque un precedente diretto, non una semplice analogia. La fonte studia la crescita ottimale su finestre e rispetto a Haar, senza identificare questo inviluppo su tutte le profondità con una soglia di traccia puntuale.

La [fonte9/v1, §8.1, Proposizione11](https://rstation.ai/problems/collatz/papers/9/v1) dà già la sommabilità del Green intero `Σ_w Ω(w)²`, anche ai target periodici. Essa implica immediatamente che le parole con `Ω≥1` sono finite. In presenza della parola vuota ciò dà un massimo raggiunto F; l'unicità del profilo (K,E) segue dalla fattorizzazione di `3^K/2^E`. Questi sono corollari utili e localmente formalizzabili di un risultato noto. Il confronto con il minimo antenato e la calibrazione hanno inoltre la struttura consueta dell'ottimizzazione di cammini: servono il raccordo preciso e il dominio dichiarato, non una pretesa di avere inventato la programmazione dinamica.

## Dove resta una distinzione precisa nelle fonti controllate

La [fonte146/v1](https://rstation.ai/problems/collatz/papers/146) definisce già la misura `σ_B` restringendo la legge originale all'evento `H=sup_i A_i≤B`, e ne analizza primi attraversamenti e shell. Afferma espressamente che la regolarità così ottenuta non produce una traccia puntuale prescritta agli interi. La [fonte12, §§8–10](https://rstation.ai/problems/collatz/papers/12) fornisce la traccia intera Cesàro, l'armonicità e il kernel canonico, oltre alla comparazione uniforme. Non vi ho trovato la funzione F o la sua identificazione con la soglia del cap. La [fonte37/v3, §§2–6](https://rstation.ai/problems/collatz/papers/37/v3) usa cap sugli esponenti delle singole transizioni e parole selezionate: il suo operatore capped non è il taglio del massimo cumulativo H del nuovo enunciato.

U15_FINITE_CAP combina invece i due oggetti sul medesimo target intero fissato. Per ogni `B≥1`, il primo attraversamento `Ω>B` appartiene al catalogo finito. Il passaggio Cesàro richiede quindi soltanto una somma finita; il Green quadratico paga ancora il futuro della legge originale. È questa prova che rimuove la dominazione uniforme `ρ_r≤C_D g` e il floor dalla sola identificazione

`g_B(n)=g(n) Q_n(H≤B)`.

Da qui il supporto finito del cap sotto Q, `g_B(n)=g(n) ⇔ B≥F(n)`, e

`g(n)−g_(F(n)^−)(n)=F(n) Σ_(u∈Opt(n))g(u)`.

Non attribuire questo enunciato alla fonte146; non omettere però che σ_B e il primo-crossing sono suoi oggetti preesistenti. La novità candidata è la specifica conclusione puntuale e la prova con gli input ridotti, non il principio generale del taglio di un massimo.

Due dettagli di dominio sono essenziali. F usa solo seed unità, mentre il catalogo dei crossing comprende anche le foglie multiple di3: queste hanno traccia zero e non determinano la soglia che conserva g. Inoltre il salto a F=1 si interpreta con l'estensione `g_B=0` per B<1; U15 tratta già questo caso. La finitezza esistenziale non dà un algoritmo con un termine noto per scoprire tutti gli ottimi.

## Conseguenza editoriale e prossima ricerca

I tre contributi da rendere leggibili nella v7 sono: (1) cataloghi e budget verificati, presentati con l'attribuzione dei risultati globali già noti; (2) l'ostruzione al recoding con suffix di pendenza limitata, con il suo preciso dominio; (3) la soglia intera esatta del cap e il ponte al surplus dei rami. La parte max-plus spiega e collega questi risultati, senza dover essere un quarto programma autonomo.

Continuerei la ricerca sul lower del surplus `LF−F`, o su certificati di seed in rami finali distinti. Il lower costante e la stabilizzazione sulla spine non danno l'ordine `n/log n` ancora mancante. La soglia esatta non esclude una spine divergente: su di essa F è confrontabile con l'altezza, e aggiungendo il floor e l'upper lineare esterni il salto superiore mantiene massa relativa positiva. Nessun passo nuovo elimina l'obbligo separato dei cicli non banali.

Prima del rilascio servono un testo coerente con la prova a crossing finiti, l'attribuzione esplicita a 9/12/127/146 e una tabella dei claim distinguendo prova locale, input esterno, calcolo finito e ipotesi aperta. L'audit U04 PASS va mantenuto nel relativo snapshot. **Preparare v7 ora; decidere il deposito dopo questa integrazione e revisione.** Continuare per mesi senza consolidare perderebbe il vantaggio di avere ora un quadro più pulito; depositare prima della revisione farebbe apparire come nuove conseguenze già immediate della letteratura.

Due titoli difendibili, secondo l'enfasi scelta:

1. **Maximal inverse gain and exact cutoff thresholds for Syracuse integer traces.**
2. **Finite predecessor catalogues and bounded-tail recoding obstructions for the Syracuse map.**

Il primo descrive il raccordo recente senza promettere convergenza; il secondo mette al centro il nucleo aritmetico e la formalizzazione. Entrambi richiedono che il testo dichiari subito il contributo esatto rispetto ai precedenti.

## Perimetro della verifica bibliografica

Ricerca mirata su «Collatz max-plus», «maximal gain», «maximum word weight», «optimal gain», «capped integer trace» e varianti; controllo diretto dei testi primari 9/v1, 12/v1, 37/v3, 127/v1 e del testo146/v1 già acquisito nel repository. Lettura aggiuntiva della pagina primaria1/v3 per distinguere minimo antenato e guadagno omogeneo. I risultati riferiti alla formula di Collatz–Wielandt nella teoria max-plus sono falsi positivi rispetto alla congettura di Collatz e sono esclusi. Non è stata ripetuta una ricerca integrale della letteratura classica, né sono stati verificati tutti i supplementi, tutte le versioni o tutti i commenti. Le copie temporanee delle nuove fonti restano fuori dal repository; la ricevuta conserva URL e hash.
