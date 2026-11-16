# H01 — Che cosa dà davvero la letteratura al programma

16 novembre 2026. Audit concettuale indipendente: fonti primarie, lettura di prove scritte e di alcune firme pubbliche; nessun esperimento, calcolo numerico, build o esecuzione di codice esterno. Non è una nuova ricertificazione dei pacchetti analitici. Versioni, URL e ambito sono in `sources/H01_sources.json`.

## 1. Un obbligo da togliere dalla lista: nonatomicità a root fisso

[Valbuena, Proposition9, archivio23025885](https://doi.org/10.5281/zenodo.23025885) dimostra già

`sup{g(v)/v : v≥V, v antenato di n} → 0`, per OGNI root positivo n fissato.

La prova del primario è uniforme fra quegli antenati, non soltanto lungo una traiettoria scelta. I target periodici richiedono il loro fattore di ciclo, ma fra gli antenati di un root fissato solo finitissimi target possono essere periodici. La [fonte12/v1](https://rstation.ai/problems/collatz/papers/12), introduzione e paragrafo dopo Theorem9, attribuisce già a questo risultato la nonatomicità della frontiera inversa e il decadimento della massima massa dei cilindri a profondità crescente.

Perciò, con `p_w=Ω_w g(u_w)/g(n)`,

`K₂^m(g²)(n)/g(n)² = Σ_(|w|=m) p_w² ≤ max_(|w|=m)p_w → 0`.

La rappresentazione di potenziale del deficit quadratico si chiude quindi puntualmente nel quadro di quelle fonti. Non occorre inventare un altro Green per provare soltanto questo limite. La cautela U07 resta corretta: il Green non pesato da SOLO non controlla il resto con terminale g². L'input aggiuntivo che lo controlla era però già disponibile.

Non segue un orizzonte uniforme dell'ordine di log n. Anche il coefficiente indipendente dal root per la frequenza superiore dei word in fonte12 non fornisce un tempo uniforme di inizio. Sono quantificatori diversi. Questa è un'integrazione utile della letteratura, non una nuova priorità.

## 2. Forza degli input e stato delle prove

- [Tao, Forum of Mathematics Pi10,2022](https://doi.org/10.1017/fmp.2022.8): il minimo scende sotto ogni funzione divergente per quasi ogni sorgente in densità logaritmica. Proposition1.14 dà mixing medio dei residui, uniformemente per 1≤m≤n. Ho confrontato questo preciso dominio con il manoscritto ElJaouhari: la citazione del mixing non è, da sola, un salto ingiustificato a un bound puntuale.
- [Krasikov–Lagarias, Acta Arithmetica109,2003](https://arxiv.org/abs/math/0205002): lower di crescita dei predecessori con esponente0,84; non è un lower di massa positiva in ciascun ramo fisico.
- [ElJaouhari,23377671](https://doi.org/10.5281/zenodo.23377671): il record consultato è un preprint. TheoremA afferma una floor uniforme su tutti gli atomi unità. La prova passa attraverso selezione, iniettività a totale fissato e un vero lemma aritmetico da norma media a norma uniforme. Nei passaggi letti non ho individuato una premessa Collatz nascosta o un errore locale da denunciare.
- [ConjectureA,23025918](https://doi.org/10.5281/zenodo.23025918): la [presentazione primaria](https://github.com/neljaouh/ConjectureA) dichiara l'input M2 vendorizzato e lo stato non refereed. Il coefficiente di densità è dipendente dal target: non sostituisce automaticamente il c/a uniforme della fonte12.
- I due [preprint Leen](https://doi.org/10.5281/zenodo.23046896), [23252395](https://doi.org/10.5281/zenodo.23252395) aggiungono trasporto naturale, densità e leggi del clock. La lettura non trova un teorema di ergodicità 0–1 dei bacini. Le loro leggi statistiche non determinano quale destino abbia un dato intero.

Le firme pubbliche ElJaouhari al commit17e43a3 usano la vera legge Syracuse ricorsiva a lettere geometriche; gli endpoint principali sono enunciati chiusi e il checker verifica la corrispondenza di tipo e gli assiomi. Questo è un riscontro statico, non una nostra build. Il README associa proprio l'hash del manoscritto letto. Il metadato Zenodo collega ancora il tagb, mentre manoscritto e README indicano il tagh: per un futuro replay va fissato il commit corretto. Lo stato di preprint non rende falsa una prova; neppure un'etichetta editoriale o l'affermazione di un audit sostituisce una verifica che non abbiamo eseguito.

## 3. Uno spunto concreto, con il suo ostacolo

Nel primario ElJaouhari il kernel finito dei prefissi selezionati soddisfa

`||K_(Γ,q) h||∞ ≤ L(B₀+3^q Ω)·mean_(G_q)|h|`, `G_q=Z/3^qZ`.

Qui L conta i totali, β_w≤B₀ e Ω_w≤Ω. È un bound ARITMETICO: non si ricava dal mixing medio astratto. Le famiglie selezionate hanno B₀ fisso e coefficienti molto piccoli. Le differenze globali uniformi sono sommabili: il loro limite S è quindi globalmente limitato. Ne consegue immediatamente

`S(n)/g(n) ≤ ||S||∞/(εn) → 0` sui root g(n)≥εn.

Il meccanismo fornisce un componente positivo utile a una floor assoluta, ma quel componente non conserva una quota fissa dei picchi lineari. Inoltre ogni word w mantenuto da un operatore positivo impone

`||K_(Γ,q)||_(L¹(HaarG_q)→L∞) ≥ 3^q Ω_w`.

Prova: scegliere h indicatore di un solo input z; la media è3^(−q) e all'output Φ_w(z) il contributo del word èΩ_w, senza cancellazione. Includere un witness Ω_w≥εn comporta dunque un costo almeno3^qεn. Il dominio è il QUOZIENTE FINITO a risoluzione q; non si afferma un bound per un operatore atomico su una L¹ senza risoluzione.

Questo ostacola il riuso dello STESSO bound positivo globale per ottenere massa relativa sui root difficili. Non esclude stime per errori centrati strutturati, cancellazioni firmate o una norma adattata alla genealogia. Il problema di ricerca utile è una stima aritmetica relativa che mantenga il colore del primo ramo e paghi i picchi, non un altro teorema generico di mixing. Il normale floor resta utile, ma non fa quel lavoro.

## 4. Riduzione del carico analitico e giudizio di utilità

Per il criterio diretto che confronta un cammino osservato e un witness laterale, bastano armonicità/upper nonperiodico canonici di Valbuena, floor di ElJaouhari e prodotto di primo arrivo del nucleo locale. Il telescopio dei contributi laterali non richiede in aggiunta densità naturale, CLT, Q, collisione o F. Queste restano interfacce possibili; non sono tutte prerequisiti della ricerca principale. La via alternativa che usa le densità dei bacini richiede invece proprio i suoi input uniformi.

Un bacino positivo di un seed divergente b è compatibile con Tao: ogni suo grande antenato passa già per b<f(N), mentre il futuro dopo b può ancora divergere. Anche un clock gaussiano indipendente dal destino può coesistere con un destino cattivo. In [Kontorovich–Lagarias](https://arxiv.org/abs/0910.1944) la distinzione fra modello stocastico e traiettorie aritmetiche è già centrale; non va persa importando risultati statistici nuovi.

Il lavoro non è completamente inutile: exact words, prodotto e no-go aritmetici permettono di formulare il costo dell'editor senza confondere codice e percorso. Ma una parte dell'apparato va declassata a infrastruttura o a descrizione: la nonatomicità a root fisso era già nota; le leggi del clock non separano il destino; il massimo aritmetico non porta da solo un rate. Il passo discriminante resta un nuovo controllo dell'offset e del colore con costo ammortizzato, oppure una vera stima relativa strutturata che lo sostituisca.

L'ulteriore [lemma di supporto sparso](H01_SPARSE_SUPPORT_IT.md) rende questa diagnosi più precisa: gli editor economici lungo una possibile divergenza stanno fuori dalla finestra centrale dei risultati di mixing condizionato. In quel regime un confronto Haar a profondità fine sublineare è impedito dal numero stesso delle parole. Resta aperto l'overlap dei supporti rari sui target già selezionati dall'orbita originale.

## 5. Un selettore positivo di tempi è già disponibile

Il prodotto convergente, già discusso nell'audit T01 con [fonte Curry](https://doi.org/10.5281/zenodo.22087163), dà sulla possibile spine divergente `n_j=b3^j2^(−A_j)P_j`, `P_j→P∞`. Pertanto

`{log₂n_j}={j log₂3+log₂(bP∞)+o(1)}`.

La rotazione irrazionale di Weyl implica che ogni intervallo di fase reale I viene visitato con frequenza |I|. È un corollario del prodotto e non si rivendica che la sua formulazione fosse assente dalla letteratura Benford. Non implica ritorni in ALTEZZA, né equidistribuzione congiunta con i residui n_j modulo3^r.

Vi è anche un controllo congiunto elementare senza indipendenza. Se e_i sono le valutazioni, `A_j≤j log₂3+O_b(1)` implica che la densità superiore degli e_i>M è al più `(log₂3−1)/M`, per M intero positivo. Per blocchi di lunghezza L fissata, l'unione dei tempi con una valutazione maggiore di M ha densità superiore al più L volte quel bound. Scegliendo M abbastanza grande, i tempi in I con TUTTO il blocco successivo in {1,…,M} conservano densità inferiore positiva. Esiste quindi una famiglia finita di pattern locali che copre una porzione abbondante dei tempi in I, senza postulare mixing dei residui.

Per il criterio di costo di root non serve un editor a ogni tempo. Una copertura con editor di debito al più `log₂j+log₂log j+O_b(1)` su quell'unione a densità INFERIORE positiva farebbe già divergere il budget. La sola densità SUPERIORE positiva di un singolo pattern non basta per il peso1/(j log j); basta invece per il peso1/j, oppure si usa direttamente la somma pesata divergente. Rimane da costruire l'editor con il vero carry e il colore laterale: la frequenza disponibile non paga quel costo. Questo è un template condizionale più circoscritto, non un editor già ottenuto.
