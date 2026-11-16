# H01 — Per gli editor a basso debito serve overlap, non mixing Haar

16 novembre 2026. Deduzione su carta, senza esperimenti o compilazioni. H03 ha controllato indipendentemente il conteggio e il passaggio a variazione totale. Non è un no-go per tutti gli editor, né una rivendicazione di priorità per il bound entropico.

## Regime corretto delle parole candidate

Sia `n_k=S^k(b)` una ipotetica spine divergente da un seed positivo dispari unità fissato. Con A_k totale degli esponenti e prodotto correttivo P_k≤P₀,

`n_k=b·3^k·2^(−A_k)P_k`, quindi `A_k≤k log₂3+log₂(bP₀)`.

Il controllo P₀ usa l'iniettività; non si estende arbitrariamente alle ripetizioni di un ciclo. Gli editor di STESSA lunghezza k con debito B−A_k≤C_b log k hanno dunque, per k abbastanza grande,

`B≤(8/5)k`, poiché `log₂3<8/5`.

Sono molto lontani dalla finestra centrale B=2k+O(√(k log k)) del mixing condizionato nel primario Leen. Il problema non è solo che un teorema noto non copre quei parametri: la seguente ostruzione impedisce quella particolare estensione.

## Bound di supporto, con prova elementare

Le parole di k esponenti positivi e totale al più B sono esattamente `binom(B,k)`. Per ogni t>0,

`binom(B,k)≤(1+t)^B/t^k`.

Prendendo t=5/3 e B≤8k/5 si ottiene `binom(B,k)≤Λ^k`, dove

`Λ=[8^8/(3^3·5^5)]^(1/5)<3`.

L'ultima disuguaglianza equivale a `8^8<3^8·5^5`. Non viene usata un'approssimazione numerica o una scansione di parole. Ogni parola determina una sola classe target, il residuo affine `2^(−B)C(w) modulo3^k`; quindi qualunque legge sui candidati, anche con pesi disuguali, ha supporto di cardinalità al più Λ^k. Vincoli ulteriori di positività, unità e colore possono soltanto ridurlo.

Sia ν una tale legge su Z/3^kZ e sia ν̃_ℓ il lift uniforme della sua proiezione a profondità ℓ. Ogni suo atomo fine pesa al più3^(ℓ−k). Sul supporto di ν la massa di ν̃_ℓ è perciò al più `Λ^k3^(ℓ−k)`. Con la convenzione TV come sup sugli eventi,

**`TV(ν,ν̃_ℓ)≥1−Λ^k3^(ℓ−k)→1` se ℓ=o(k).**

La stessa prova vale se al posto della proiezione di ν si lifta qualsiasi altra legge a profondità ℓ: il bound per atomo resta3^(ℓ−k).

## Che cosa impedisce, e che cosa lascia aperto

L'appendice sul mixing condizionato di [Leen,23046896](https://doi.org/10.5281/zenodo.23046896) impone esplicitamente il totale centrale. Non può essere estesa, con la stessa conclusione per profondità coarsening sublineare, al regime a basso debito sopra. Analogamente, la floor degli atomi NON condizionata di ElJaouhari usa parole di tutti i totali e non dà una floor per questa famiglia sparsa. Non è stata trovata una contraddizione nei loro enunciati: sono domini diversi.

Questo NON dimostra che un editor economico non esista. Il target n_k non è un residuo Haar generico: è già selezionato da una parola effettiva proveniente dal seed b. Il bersaglio utile diventa l'**overlap fra due supporti sparsi con colori fisici diversi, condizionato alla parola originale e alla vera costante affine**. Una equidistribuzione su tutti i residui è più forte del necessario e qui impossibile; una correlazione aritmetica sui target selezionati rimane aperta.

Il lemma riguarda una lunghezza fissata e il lift al modulo completo corrispondente. Non esclude un routing con lunghezze variabili, un diverso spazio di stati o una norma che trattenga la genealogia. Una proposta di quel tipo deve però spiegare esplicitamente quale supporto condizionato confronta: non basta invocare il mixing medio delle parole tipiche.

Precisazione H02 sul clock variabile: ponendo il debito pesato `E_j=B_j−A_j−(d_j−j)log₂3`, il bound E_j=O(log j) implica `B_j≤d_j log₂3+O_b(log j)`. Se d_j/log j→∞, la medesima ostruzione vale al MODULO PROPRIO3^d_j. Cambiare clock non esce quindi automaticamente dal regime sparso; un clock O(log j) può sfuggire a questa sola deduzione, senza che sia provata l'esistenza del percorso. Non si stanno confrontando automaticamente moduli diversi o loro proiezioni a un modulo comune.

Cambiare i pesi tramite un tilt non aumenta il supporto della famiglia troncata. Anche per un tilt i.i.d. non troncato a media finita strettamente minore di8/5 per lettera, la legge dei grandi numeri concentra quasi tutta la massa su questa famiglia; la stessa ostruzione TV sopravvive, con un errore di massa tendente a zero. Questo lascia aperta una misura di riferimento diversa, ma non autorizza a trasferire al nuovo regime il mixing Haar già disponibile per parole centrali.
