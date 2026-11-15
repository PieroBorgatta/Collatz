# S10 Sparsezza dei segmenti finiti e controllo uniforme del prodotto affine

13 novembre 2026. Stato **C/E**: deduzione su carta con lettura della prova primaria e piccoli replay esatti. Nessuna nuova dichiarazione Lean è stata scritta da S10. La deduzione deve ricevere la revisione avversa prevista dallo sprint; non si rivendica priorità bibliografica.

## Risultato della ricerca

La sparsezza quantitativa usata per orbite infinite collision-free ammette una versione per **qualsiasi segmento finito iniettivo** della mappa shortcut T. Il costo del bordo temporale è al più `floor(log₂X)` punti per una finestra di lunghezza X. Sommando sulle bande diadiche si ottiene un limite universale della somma dei reciproci, quindi del prodotto affine lungo segmenti Syracuse che si espandono in un segmento shortcut iniettivo.

Questo controlla l'altezza di una trasformazione che conservi lunghezza k e totale A degli esponenti. Non produce una quota di sorgenti trasformabili e quindi non dimostra H.

## Fonte primaria e controllo effettuato

[Michael John Curry, agosto 2026, DOI 10.5281/zenodo.22087163](https://doi.org/10.5281/zenodo.22087163), Teorema 2.3 e Proposizione 3.1. L'accesso web ordinario non funzionava; sono stati letti i metadati dall'API Zenodo e il PDF primario di cinque pagine dall'endpoint dei file. La pagina 2 è stata anche renderizzata per controllare la parentesi nella stima affine del Lemma 2.2. Il file originale resta soltanto in `/tmp/collatz_s10_curry.pdf`; non è stato aggiunto al repository. Hash e provenienza sono nella [ricevuta](../verification/s10_receipt.json).

Il punto riusabile della prova è più debole dell'ipotesi globale dichiarata: per una finestra di lunghezza X serve soltanto l'iniettività di **T^N** sui suoi punti, con `N=floor(log₂X)`. La prova raggruppa per numero m di dispari, trasla di multipli di `2^N` e usa l'identità `T^N(s+z2^N)=T^N(s)+z3^m`. Una collisione delle immagini traslate fra punti con lo stesso m diventa dunque una collisione al medesimo tempo N fra i punti originali. Non vengono richiesti tempi ulteriori o collisioni fra tempi diversi.

Il riferimento storico Garcia–Tal è accreditato dalla fonte per il meccanismo; il suo PDF non è stato recuperato direttamente in questa analisi. La verifica matematica qui usa la prova autosufficiente di Curry.

## Lemma finito e prova del bordo temporale

Sia `z_j=T^j(u)` per `0≤j≤L`, con tutti gli z_j distinti, e sia O il loro insieme. Per `X≥2`, poniamo `N=floor(log₂X)`.

Se `L≥N`, il prefisso `O_N={z_j:0≤j≤L−N}` ha T^N iniettiva: un'uguaglianza `T^N(z_i)=T^N(z_j)` è `z_(i+N)=z_(j+N)`, fra due indici ancora nell'intervallo 0,…,L; l'iniettività del segmento dà i=j. Il complemento ha esattamente N punti. Se `L<N`, l'intero segmento ha al più N punti e il prefisso può essere vuoto.

Applicando la prova della finestra a O_N, per ogni `a≥1` e `1/2<γ<1/log₂3`, segue

`|O∩[a,a+X)| ≤ N + 6(N+1)(X^H(γ)+X^(γ log₂3))`.

Il termine N è necessario. Il segmento iniettivo shortcut `7→11→17→26→13→20→10→5` termina in 5, che non ha ritorni positivi; tuttavia `T^5(20)=T^5(5)=2`. Dunque non si può chiamare collision-free l'intero segmento senza trattare il futuro. Nel prefisso troncato la collisione non compare.

Questo passaggio non scambia una media con una proprietà puntuale: la finestra riguarda l'insieme dei valori di un singolo segmento, e il bordo è contato deterministicamente.

## Un limite universale esplicito

Prendiamo `γ=3/5`, `β=49/50`. Le due disuguaglianze che garantiscono `H(γ)<β` e `γ log₂3<β` si riducono ai confronti interi

`5^50 < 2^69·3^30`, `3^30 < 2^49`.

Per la banda `[2^j,2^(j+1))`, j≥1, il lemma dà quindi

`|O∩[2^j,2^(j+1))| ≤ j+12(j+1)2^(49j/50)`.

Ogni reciproco nella banda è al più `2^(−j)`. Il possibile punto 1 contribuisce al più 1. Con `q=2^(−1/50)`,

`Σ_(x∈O)1/x ≤ 1+Σ_(j≥1)j/2^j+12Σ_(j≥1)(j+1)q^j`

`= 12/(1−q)^2−9 =: B`.

È una costante **indipendente da sorgente, bersaglio, lunghezza e altezza del segmento**. Un limite razionale molto grossolano è `B<120000`: basta `q<99/100`, equivalente all'esatto confronto `2·99^50>100^50`. Questi tre confronti interi sono stati verificati nel replay. La stima è volutamente enorme; non si suggerisce utilità numerica del suo valore.

Per un segmento Syracuse `n_0=u,…,n_k=n` che si espande in un segmento shortcut iniettivo, il prodotto esatto è

`P=Π_(j<k)(1+1/(3n_j))=2^A n/(3^k u)`.

Gli n_j sono un sottoinsieme dei punti shortcut. Usando `log(1+t)≤t` si ottiene `P≤exp(B/3)`.

Un bersaglio senza ritorni positivi garantisce l'iniettività di qualunque segmento che vi arrivi. È sufficiente anche richiedere **primo arrivo** al bersaglio: una ripetizione precedente costringerebbe il primo arrivo ad avvenire già entro il primo giro del ciclo, contraddicendo il tempo dichiarato. Il limite non vale per un'orbita ripetuta più volte sul ciclo.

## Conseguenza per il trasporto a totale invariato

Sia una parola originale di lunghezza k e totale A da u a n, e sia una parola modificata con gli stessi k,A da v a y. Dalle identità affini e dalla nonnegatività della nuova costante C',

`v ≤ 2^A y/3^k = (y/n)P u`.

Se y è il fratello canonico e `y≤16n+5`, allora `y/n≤21` e quindi

`v ≤ D₀ u`, con `D₀=21 exp(B/3)` universale.

L'ipotesi decisiva è l'iniettività del segmento originale; nel dominio di H è soddisfatta. La conclusione copre più della surgery di due esponenti: vale per qualsiasi trasformazione reale che conservi k,A. Non entra in conflitto con H.2, che cambia il totale A attraverso l'ultimo esponente.

Per un insieme finito di shift, S06 ha un candidato separato di carico `M_odd≤ΣQ_δ=O(log n)` nel dominio senza ritorni del target superiore. Combinando i due risultati su carta, altezza e carico hanno un costo compatibile con la forma logaritmica, **se** si riuscisse a trasferire una frazione relativa η uniformemente positiva. Quest'ultima minorazione non è stata ottenuta. Nei dati congelati di S06 i successi sono pochi e poco profondi; non vi è evidenza di una tale η. Preservare il fattore diadico conserva D e M, ma la massa ordinaria deve ancora usare i corretti pesi delle parti dispari.

## Replay finito e confronto fra agenti

Il [programma S10](../experiments/s10_sparse.py) esamina i 1.924 segmenti con sorgente dispari u≤4095 che raggiungono il bersaglio noto 5. Controlla **30.784** troncamenti per `N=1,…,16`, assenza di collisioni nel prefisso, numero di eccezioni terminali e identità esatta del prodotto affine. Tutti superati; risultati normale e `-O` identici.

I massimi osservati sono circa 1,0611 per la somma dei reciproci shortcut e 1,1749 per il prodotto affine. Sono diagnostiche finite, non stime del supremo universale. È stato preservato anche il controesempio all'iniettività di T^N senza troncamento.

S09 ha verificato il controllo degli indici e chiesto di controllare l'uso esatto dell'iniettività nella prova primaria; ciò è stato fatto sopra. S07 non rileva ostacoli dalle macro lunghe note e fornisce per esse una somma geometrica indipendente. S11 ha richiamato la distinzione fra parametro libero e tempo di una stessa orbita: il lemma usa solo il secondo e un errore terminale esplicito.

Primo compito successivo: formalizzare il lemma finito `T^N`-iniettivo sul prefisso troncato e il conteggio della finestra; poi derivare il bound del prodotto. Prima di usare D₀ nel programma H serve una revisione indipendente di questa derivazione, richiesta al coordinatore. Il programma si arresta sul punto η se il nuovo trasporto non produce una minorazione relativa dimostrata: il controllo di altezza, da solo, non è una soluzione.
