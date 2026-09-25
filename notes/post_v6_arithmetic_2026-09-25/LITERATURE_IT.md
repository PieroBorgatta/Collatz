# Parole di parità della torre: letteratura mirata

Ricerca e verifica delle fonti primarie: **25 settembre 2026**.
Questa selezione riguarda l'ostacolo specifico dei blocchi di parità di
`Q_v=(9^(2^v)−1)/2^(v+3)`, non una rassegna generale di Collatz.
Le fonti sotto non dimostrano la candidata
`589j−305b≤128v²` per ogni blocco effettivamente raggiunto entro l'orizzonte
prescritto. La ricerca non stabilisce l'assenza assoluta di altri risultati
pertinenti e non accerta alcuna priorità matematica del presente studio.

## 1. La novità più pertinente: Bugeaud, agosto 2026

Y. Bugeaud, *On the binary representation of powers of 3*,
[arXiv:2608.23017v1](https://arxiv.org/html/2608.23017v1), 24 agosto 2026,
Teoremi 1.2 e 1.6. Preprint; non presentato qui come articolo già sottoposto
a peer review.

Il Teorema 1.2 considera rappresentazioni in base `b` che sono prefissi di
parole infinite con complessità dei fattori `p(ℓ)≤Cℓ`, per `C` fissato,
escludendo la divisibilità per `b^floor(n/(C+2))`. Gli interi abbastanza
grandi così rappresentati hanno un divisore primo fuori da ogni insieme
finito fissato `S`. La soglia ottenuta mediante il teorema del sottospazio
non è effettiva. Il Teorema 1.6 limita invece effettivamente l'esponente
`t` delle rappresentazioni `W^t` delle `S`-unità intere.

Con `b=2` e `S={3}` si ottiene una restrizione specifica delle potenze di 3.
Riguarda però le cifre binarie, non le parità Collatz. Il solo sbilanciamento
di un blocco non implica ripetizioni o bassa complessità: manca un lemma
che colleghi i due oggetti.

## 2. Dalla parola al residuo: Bernstein–Lagarias

D. J. Bernstein e J. C. Lagarias, *The 3x+1 Conjugacy Map*, Canadian
Journal of Mathematics 48 (1996), 1154–1169,
[DOI](https://doi.org/10.4153/CJM-1996-060-x), §1, formule (1.5)–(1.6).

La codifica delle parità coniuga la mappa Collatz a una traslazione delle
cifre sui numeri 2-adici e induce una permutazione modulo `2^L`.
La formula inversa esprime il punto iniziale mediante una somma di termini
`−2^d_i/3^(i+1)`. Ogni parola finita corrisponde quindi a una classe residua
esatta: è il fondamento della traduzione aritmetica usata qui.

La conservazione della misura e la proprietà di Bernoulli riguardano la
misura di Haar. Non stabiliscono che la particolare successione sparsa
`Q_v` abbia parità tipiche. Contare classi residue favorevoli non dimostra
che la torre appartenga a esse.

## 3. Valutazioni e altezza della costante: Chim

K. C. Chim, *Lower bounds for linear forms in two p-adic logarithms*,
Journal of Number Theory 266 (2025), 295–349,
[DOI](https://doi.org/10.1016/j.jnt.2024.07.012),
[testo primario](https://tugraz.elsevierpure.com/ws/portalfiles/portal/92346766/1-s2.0-S0022314X24001793-main.pdf),
Teorema 2.1, pp. 298–299; pubblicazione online 21 agosto 2024.

Il teorema richiede basi moltiplicativamente indipendenti e fornisce una
stima esplicita della valutazione di una differenza di potenze.
La dipendenza dal parametro logaritmico degli esponenti è lineare;
resta il prodotto delle altezze delle basi. Specializzando a `3^E+c`,
la stima conserva dunque un fattore dell'ordine di `log c`.

Nel precedente argomento sul primo passo divergente la costante aveva
altezza controllata in funzione di `v`. Per un prefisso lungo, la costante
affine dipende anche dal prefisso: quel controllo non si trasferisce
automaticamente. Migliorare le costanti numeriche del teorema, da solo,
non elimina questa dipendenza. L'applicazione precedente e le sue
ipotesi sono documentate nella
[nota dedicata](../post_v6_certificates_2026-09-24/CHIM_OBSTRUCTION_IT.md).

## 4. Un vincolo sulle cifre iniziali: Stewart

C. L. Stewart, *On the representation of an integer in two different
bases*, Journal für die reine und angewandte Mathematik 319 (1980),
63–72, [testo dell'autore](https://uwaterloo.ca/pure-mathematics/sites/default/files/uploads/documents/j-reine-ange-math-1980.pdf),
Teorema 2, p. 64.

Per una ricorrenza con radice dominante moltiplicativamente indipendente
dalla base, il teorema limita inferiormente il numero di cifre diverse
da una cifra fissata. Applicato a `3^m` in base 2 dà, con costante
effettivamente calcolabile, `s₂(3^m) ≫ log m/log log m`.

L'identità della nostra famiglia
`3^(2^(v+1))=1+2^(v+3)Q_v` implica esattamente
`s₂(Q_v)=s₂(3^(2^(v+1)))−1`. Si ricava quindi un limite dell'ordine
`v/log v` sul numero di bit 1 di `Q_v`. È una restrizione aritmetica
autentica, ma non controlla la loro collocazione e non riguarda il numero
di passi dispari dell'orbita.

## 5. Distribuzione delle parità per quasi tutti gli interi: Inselmann

M. Inselmann, *An approximation of the Collatz map and a lower bound for
the average total stopping time*,
[arXiv:2402.03276v3](https://arxiv.org/html/2402.03276v3), 13 agosto 2024,
Teorema 1.6.

Per ogni `ε>0`, su un insieme di densità naturale 1, lo scarto fra il
numero di dispari e `k/2` è al massimo `ε log₂ n`, simultaneamente per
`0≤k≤log₂ n/(1−log₂√3)`. Il risultato controlla direttamente parità lungo
orbite, con un orizzonte proporzionale all'altezza binaria del dato iniziale.

Non identifica tuttavia i singoli interi eccezionali. Un insieme di
densità zero può contenere tutti i `Q_v`; serve un argomento ulteriore
per escluderlo. Inoltre `log Q_v` è dell'ordine di `2^v`: la scala di
errore del teorema, per `ε` fissato, non coincide con il limite `128v²`
della candidata.

## 6. Il resto affine dipende dall'ordine dei bit: Rozier–Terracol

O. Rozier e C. Terracol, *Paradoxical behavior in Collatz sequences*,
[arXiv:2502.00948v5](https://arxiv.org/html/2502.00948v5), 17 maggio 2026,
§2, Lemma 2.3 e Teorema 2.4.

Per una parola di `b` passi con `j` dispari, il resto nella formula
`T^b(n)=3^j n/2^b+E` soddisfa
`(3^j−2^j)/2^b≤E≤(3^j−2^j)/2^j`. Il testo caratterizza le parole che
raggiungono gli estremi e introduce un ordine parziale che controlla
l'effetto di spostare i bit 1.

Questi risultati consentono di stimare le costanti affini e dimostrano
perché il solo conteggio dei dispari perde informazione. Non forniscono
una legge uniforme sulla frequenza o sulla compensazione dei blocchi
raggiunti dalla torre.

## Il passaggio ancora necessario

La via suggerita da Bugeaud richiederebbe un risultato aggiuntivo:
dedurre, da un blocco di parità che viola il limite e dalla sua
raggiungibilità attraverso il prefisso effettivo, una ripetizione digitale
o una relazione aritmetica di complessità abbastanza limitata.
Una disuguaglianza sul numero di bit 1 non offre da sola tale deduzione.

In particolare, non è giustificato sostituire una somma affine con un
numero crescente di addendi con un'applicazione del teorema del
sottospazio a dimensione fissata. Né la trascendenza di un limite 2-adico,
né una legge di distribuzione valida quasi ovunque, forniscono da sole
la stima puntuale richiesta. Questa è una valutazione della pertinenza
delle fonti lette, non un teorema di impossibilità per altri approcci.
