# U14 — Fonte147: input importabile e limiti per U05 e certificati adattivi

16 novembre 2026. Lettura mirata del testo primario147/v1 fornito dal coordinatore, in particolare §§2,4,7. Nessuna copia integrale aggiunta al repository, esperimento, supplemento eseguito, Lean o GPU. I risultati citati sono esterni; non sono rivendicati come scoperte del progetto.

## 1. Che cosa importare

La [fonte147/v1, *Time, Depth, and Description Complexity of Precise Collatz Returns*](https://rstation.ai/problems/collatz/papers/147) usa un bound quantitativo di durata per segmenti dispari con un dizionario finito fissato W, attribuito esplicitamente alla fonte15/v2 e al suo input Evertse–Ferretti. Le corse di esponente1 sono gratuite; ogni fattore periodico del dizionario o lettera singola di esponente almeno2 costa un pezzo. Per t passi dispari, sorgente a e costo k, l'equazione(7) è

`t+1≤exp(C_W(k+1)/log(k+2))·log(a+G_W)`.

La guardia arresta il segmento prima di un passo da1 o da un ciclo intero rappresentato dai template. Le costanti sono effettive nel risultato importato, ma non vengono valutate numericamente nella147. Il Teorema2 combina tale durata e un recupero dopo una discesa per imporre costo `≥c log(N+2)loglog(N+3)` a un ritorno effettivo power-precise in tempo fisico N, senza orizzonte superiore. Non fornisce un upper di complessità.

## 2. Incidenza precisa su U05 e sui cicli

Il Teorema2 non si applica automaticamente a una coppia di recoding: parole verso target distinti con lo stesso profilo non costituiscono un ritorno effettivo vicino al proprio punto iniziale. U05 ha già `k,A=O(log X)` per numero di pezzi fissato, e usa un altro passaggio S-unit per ottenere `r=o(log X)` sul prefisso comune. La durata quantitativa può rendere esplicita la dipendenza dalla complessità nel primo bound; non uniformizza l'altro passaggio quando il numero dei pezzi cresce, perché cresce anche la dimensione dell'equazione S-unit. Non dichiarerei quindi un'estensione di U05 al caso di complessità crescente.

I ritorni esatti sono compresi, ma il dizionario deve essere fissato prima dei parametri e l'onset dipende da esso. Scegliere per ogni ciclo il suo periodo come nuovo dizionario non conserva un onset uniforme. La147 ricorda inoltre che la fonte15 trattava già complessità dei cicli esatti. Non emerge una nuova esclusione generale dei cicli.

## 3. Un vincolo concreto per la frontiera adattiva

Il seguente è soltanto un corollario dell'equazione(7). Se i witness hanno seed `a≤U` e lunghezza t, e rispettano la guardia, porre

`R=(t+1)/log(U+G_W)`.

Quando R tende a infinito, l'inversione di(7) dà

`k+1≥c_W log R·loglog R`.

Si ottiene prima `k+1≥c log R`, poi si reinserisce il conseguente lower di log(k+2). Per target n senza ritorni la guardia è automatica: un cammino effettivo verso n non può aver già visitato1 o un qualsiasi ciclo positivo.

Questo suggerisce una variante PRECISA della procedura adattiva U14, conservandone integralmente la completezza:

`U_t=(n+1)2^t`, `K_t=(K₀(n)+t)^2`.

Ogni fase esegue ancora un numero finito di passi; entrambi i cutoff divergono. Tutte le parole finite restano prima o poi enumerate, perciò il certificatore corretto per soglie strette resta completo. I bit degli stati sono ora `O((log(n+1)+t)^2)`; è un aumento dichiarato del costo, non una promessa di accelerazione.

Per n fissato e per eventuali witness nella frontiera `K_t/2≤|w|≤K_t`, il rapporto R è almeno dell'ordine di t, poiché `log U_t=O(log(n+1)+t)`. Di conseguenza quei witness, se esistono e n non è periodico, richiedono costo almeno `c_W log t·loglog t` rispetto a QUALSIASI dizionario finito W fissato. Una ricerca confinata per sempre a un numero fisso di pezzi non rappresenterebbe questa frontiera. La generazione per vere orbite, senza restrizione di lingua, la comprende invece automaticamente.

La distinzione è essenziale: questa è una stima necessaria di complessità per i witness profondi, non una prova che essi esistano, abbiano grande gain, entrino in rami diversi o paghino A. La variante evita in modo concreto orizzonti e lingue fissati, ma resta da ottenere un tasso di crescita del totale privato del ramo massimo. Non viene proposta l'esecuzione di un nuovo scan prima di avere una domanda quantitativa che quel costo aggiuntivo possa discriminare.
