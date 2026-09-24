# Valutazione della v6 e proposta di continuazione

24 settembre 2026. Ricognizione delle fonti primarie, audit del progetto e deduzioni sviluppate in questa sessione. **Non è una dimostrazione di Collatz né una certificazione di originalità bibliografica assoluta.**

## 1. Il mio giudizio

Il progetto merita di continuare, ma con un obiettivo più selettivo. La sua parte più solida è una biblioteca di aritmetica esatta, con enunciati formalizzati e controesempi che delimitano i tentativi di costruire un rango globale. Non vedo nella v6 un nuovo meccanismo capace di imporre la discesa a ogni orbita; vedo strumenti riutilizzabili per costruire e verificare un tale meccanismo, qualora si riesca a trovarlo.

La distinzione è sostanziale. La proprietà `UniformStrictDescentHypothesis` è essenzialmente equivalente alla congettura: raggiungere 1 implica scendere sotto ogni sorgente dispari maggiore di 1; viceversa, la discesa universale implica Collatz per induzione forte. Dare un nome all'ipotesi e formalizzare il ponte è buona architettura, ma non ne riduce automaticamente la difficoltà matematica.

La v6 è più credibile perché corregge esplicitamente l'errore di continuità della v4, distingue prove Lean, deduzioni su carta e obiettivi aperti, e presenta ostacoli concreti alle proprie strategie. Queste sono qualità scientifiche reali. L'originalità più difendibile riguarda la combinazione specifica di formalizzazione, certificati e ostruzioni; molte identità affini e osservazioni sui cilindri appartengono alla tradizione classica del problema.

**La continuazione che raccomando è un sistema di ritorni su una sezione aritmetica con copertura dimostrata, usando blocchi parametrizzati per rappresentare le torri di shadowing.** Il risultato utile da cercare per primo è un teorema su una famiglia infinita con tutti i parametri trattati, oppure un nuovo teorema d'impossibilità per una classe precisa di certificati. Non raccomando un'altra escalation della dimensione delle matrici o della profondità del trie.

## 2. Cosa ho effettivamente verificato

Il record [Zenodo v6](https://zenodo.org/records/22936057) è pubblico: versione 6.0.0, data 24 settembre 2026. Il DOI inizialmente restituiva 404, mentre la successiva lettura dell'API Zenodo ha confermato il deposito. PDF e ZIP locali corrispondono ai checksum MD5 pubblicati. Il verificatore del progetto ha inoltre controllato il manifesto SHA-256, il PDF e tutte le 65 voci del pacchetto. I dettagli sono in `publication_check.json`.

L'audit Lean ha ottenuto:

- build completa dei target, incrementale, riuscita: **3360 jobs**, Lean/Mathlib 4.29.1;
- rielaborazione diretta del sorgente `ExactCylinders.lean` riuscita;
- audit fresco di dodici enunciati principali: soltanto `propext`, `Classical.choice`, `Quot.sound`;
- assenza di `sorry`, `admit` e assiomi dichiarati dal progetto nei sorgenti esaminati; nove usi di `native_decide` nella biblioteca;
- un tredicesimo enunciato campione, di verifica finita, con la dipendenza nativa attesa.

Non ho ricompilato da zero tutte le dipendenze, eseguito un checker indipendente o migrato il progetto. L'assenza di assiomi aggiuntivi non rimuove le ipotesi esplicite presenti nel tipo di un teorema. La build iniziale ha incontrato il blocco Git/Xcode e Lake ha rimosso automaticamente la dipendenza mathlib; è stata ripristinata la revisione esatta con CommandLineTools e cache locale, senza modificare i sorgenti. Il resoconto completo, con riferimenti alle righe, è in `lean_audit.md`.

Il pin 4.29.1 precede le correzioni di soundness documentate nelle release [4.32.2](https://lean-lang.org/doc/reference/latest/releases/v4.32.2/) e [4.34.0](https://lean-lang.org/doc/reference/latest/releases/v4.34.0/). Non ho trovato evidenza che il progetto eserciti quei difetti. Un replay su una versione corretta resta una tappa di qualità della verifica, distinta dal progresso matematico.

## 3. Dove sta il contributo e dove sta il vuoto

| Componente | Cosa stabilisce | Cosa manca |
|---|---|---|
| `ExactCylinders` | Il match di una parola positiva equivale a una congruenza modulo `2^(A+1)`. Il bit finale impone l'esattezza dell'ultima valutazione. | Un teorema che escluda ogni cammino infinito eccezionale. |
| `PrecisionTax` | Ogni ripetizione della stessa parola espansiva consuma esattamente A bit di precisione. | Un bilancio valido sotto cambi arbitrari di parola e cancellazioni. |
| `SwitchingPrecision` | Trasporto esatto quando due equazioni sui coefficienti sono soddisfatte. | Controllo dei cambi incompatibili, che possono ricaricare il contatore. |
| `ThreeTraceObstruction` | La traiettoria concreta 743→1115→1673→1255 smentisce un rango strettamente decrescente basato soltanto su tre contatori. | Una risorsa aggiuntiva che funzioni per tutte le successioni di cambi. |
| Certificati CW | Limiti spettrali per matrici finite esplicitamente definite. | Trasporto puntuale a tutte le orbite intere; eventuale limite di operatore infinito. |
| `CycleConstraints` | Equazione e necessaria contrattività di un ciclo positivo. | Esclusione dei cicli contrattivi non banali. |
| `FirstBarrier` | Criterio esatto di discesa su un cilindro e identità con lo spostamento. | Un limite indipendente sul residuo o sulla correzione affine. |
| A0 | Discesa su due sottofamiglie infinite e ponti condizionali. | Le due ipotesi first-barrier e una copertura globale. |

Quando w coincide con i primi ℓ esponenti dell'orbita di n, l'identità

\[
 (2^A-3^\ell)n-C_w=2^A(n-S^\ell(n))
\]

spiega il rischio di circolarità: verificare il lato sinistro sulla sorgente effettiva è verificare la discesa stessa. Il criterio acquista forza solo quando si ottiene un limite per un'intera famiglia da informazioni indipendenti.

Anche un albero finito senza cicli con profondità massima fissata è insufficiente: gli interi `2^(m+1)-1` realizzano prefissi `[1]^m` di crescita arbitrariamente lunghi. Un certificato finito deve descrivere comportamenti di lunghezza non limitata tramite parametri, induzione o un'altra struttura ben fondata.

Una piccola precisazione editoriale: nel contesto di sorgenti positive, `P>Q` e `C_w>0` implicano davvero `(Pn+C_w)/Q>n`. La frase della v6 che distingue espansività della pendenza dalla crescita dell'endpoint potrebbe essere resa più netta per questo dominio. Non compromette i risultati.

## 4. Letteratura: ciò che cambia la scelta del prossimo obiettivo

La ricognizione estesa, con versioni e limiti, è in `literature.md`. Ho privilegiato fonti degli autori, arXiv, editori e sorgenti dei progetti. Le formalizzazioni esterne non sono state ricompilate in questa sessione.

| Fonte | Stato e contenuto pertinente | Conseguenza per il progetto |
|---|---|---|
| [Terras, 1976](https://www.impan.pl/en/publishing-house/journals-and-series/acta-arithmetica/all/30/3/101028/a-stopping-time-problem-on-the-positive-integers); [Bernstein–Lagarias, 1996](https://websites.umich.edu/~lagarias/doc/bernstein.pdf) | Fondamenti della codifica di parità e della dinamica 2-adica della mappa abbreviata. | I cilindri finiti hanno antenati classici. La coniugazione globale della mappa abbreviata non implica quella della mappa accelerata singolare. |
| [Tao, 2022; arXiv v7 luglio 2026](https://arxiv.org/abs/1909.03562) | Quasi tutti gli inizi in densità logaritmica raggiungono ogni soglia prescritta che tenda a infinito. | È molto più di un drift medio, ma non dà convergenza a 1 o una conclusione per ogni inizio. |
| [Inselmann, v3 agosto 2024](https://arxiv.org/abs/2402.03276v3) | Discesa sotto `n^ε` per quasi tutti gli inizi in densità naturale, su scala temporale logaritmica. Preprint nella fonte consultata. | Densità e soglia sono coordinate diverse: non presentarlo semplicemente come lo stesso teorema di Tao migliorato. |
| [Rozier–Terracol, v5 maggio 2026](https://arxiv.org/abs/2502.00948v5) | Pubblicato in *Discrete Mathematics* 349, 115167. Segmenti con pendenza contrattiva ma endpoint non inferiore alla sorgente. | La correzione affine è centrale. L'osservazione locale del progetto sui primi prefissi contrattivi va confrontata con la congettura classica CST di Terras. |
| [Hercher, 2023](https://arxiv.org/abs/2201.00406v3) | Esclusione dei cicli non banali con al più 91 minimi locali. | Non sono 91 passi o 91 elementi dispari; l'esclusione dei soli cicli espansivi non compete con questo risultato. |
| [Knight, 2026](https://doi.org/10.1016/j.disc.2025.114812); [Fernández–Ibáñez, luglio 2026](https://arxiv.org/abs/2607.24844) | Il primo esclude una classe tecnica di cicli razionali; il secondo studia estremali di Christoffel. | Un progetto sui cicli deve distinguere classi estremali e cicli generali, e confrontarsi con questi enunciati precisi. |
| [Barina, pagina del progetto](https://pcbarina.fit.vut.cz/); [Angeltveit, febbraio 2026](https://arxiv.org/abs/2602.10466) | Verifica esaustiva dichiarata sotto `2075·2^60` al controllo odierno; nuovo algoritmo per estendere verifiche finite. | Utili per basi finite e potature certificate. Non forniscono la chiusura infinita. |
| [Kramer, luglio 2026](https://arxiv.org/abs/2607.10041) | Preprint con diagnostica congiunta di drift reale, residui iniziali 2-adici ed endpoint 3-adici, e ricerca evolutiva. | La semplice proposta «unire 2, 3 e infinito» ha già prior art diretta. Il criterio esatto `2^(A+1)` della v6 è più informativo del solo vincolo d'integralità usato lì. |
| [Sharpe, repository corrente](https://github.com/msharpe248/collatz) | Dichiara risultati Lean su ostacoli ai potenziali, itinerari, ripetizioni, trasporto dei cilindri e intervalli di quozienti. | Neppure «aggiungere il quoziente intero» basta come novità. Servono un teorema ulteriore o certificati nuovi con quantificatori universali. |
| [Ross, Zenodo v3](https://doi.org/10.5281/zenodo.22181823) | Enuncia esplicitamente una classe dispari modulo `2^(1+Σa)` per ogni parola finita positiva. | La v6 fa bene a rivendicare l'integrazione Lean locale, non la priorità matematica del cilindro unico. |
| [Chang, aprile 2026](https://arxiv.org/abs/2603.11066v6) | Ampio preprint assistito da LLM; non rivendica una soluzione. | «Formal results» nell'abstract non equivale a prova Lean. Un catalogo di ostacoli non esaurisce logicamente tutte le strategie future. |
| [Mazur/ProofAtlas, settembre 2026](https://www.proofatlas.ai/formalizations/positive-density-log-time-collatz/) | Rivendica una frazione positiva esplicita di inizi che raggiunge 1 entro `10,46 log n` passi ordinari, con build registrata e revisione pendente. | Potenzialmente importante; non è convergenza in densità uno, né universale. Distinguere controllo del codice, allineamento dell'enunciato e revisione matematica. |
| [Shaik](https://shaikidris.github.io/) e [Allikvere](https://doi.org/10.5281/zenodo.21499244) | Rivendicazioni recenti su soglie polilogaritmiche o quasi limitate in densità naturale; diversi livelli di evidenza meccanica. | Sono oggetti da sottoporre ad audit, non premesse automaticamente acquisite. Anche se confermati, non chiudono il quantificatore «ogni». |
| [Monks et al., 2013](https://doi.org/10.1016/j.disc.2012.11.019) | Il Teorema 6.4 garantisce che ogni orbita divergente e ciclo non banale della mappa abbreviata incontri `20 mod27`. | È il risultato che offre il collegamento più concreto per una nuova continuazione locale: una sezione con copertura già dimostrata. |

Due controlli di versione mostrano perché una ricerca aggiornata non può basarsi sugli snippet: [Liu v2](https://arxiv.org/abs/2512.13760v2) riporta esponente `0,3227`, mentre risultati di ricerca mostrano ancora `0,946` della v1; [Niu v2](https://arxiv.org/abs/2605.13886v2) è stato ritirato. Non ho trovato nelle fonti esaminate una dimostrazione consolidata della congettura.

## 5. Una sezione concreta con copertura ricorrente

Scriviamo `T(n)=n/2` per n pari e `T(n)=(3n+1)/2` per n dispari. È la mappa abbreviata usata da Monks et al.; `S` è invece la mappa dispari-dispari del progetto.

**Deduzione su carta sviluppata in questa analisi, non ancora formalizzata in Lean.** Sia u positivo, dispari e non divisibile per 3, e sia `a=ν₂(3u+1)`. L'episodio **(u,S(u)]**, sorgente esclusa ed endpoint incluso, visita

\[
 T^j(u)=\frac{3u+1}{2^j},\qquad 1\le j\le a.
\]

Un suo punto è `20 mod27` esattamente quando

\[
 3u+1\equiv20\,2^j\pmod{27}.
\]

Poiché 2 ha ordine 18 modulo 27, possiamo ridurre j a `j₀∈{1,…,18}`, con `j₀≤j`. La congruenza forza j₀ dispari. Escludendo i tre valori che richiedono `3|u`, rimangono sei casi:

| j₀ | u modulo 9 | Condizione | Progressione equivalente |
|---:|---:|---|---|
| 1 | 4 | a≥1 | **u≡13 mod18** |
| 3 | 8 | a≥3 | **u≡53 mod72** |
| 7 | 7 | a≥7 | **u≡853 mod1152** |
| 9 | 2 | a≥9 | **u≡3413 mod4608** |
| 13 | 1 | a≥13 | **u≡54613 mod73728** |
| 15 | 5 | a≥15 | **u≡218453 mod294912** |

Chiamiamo **E** l'unione di queste progressioni. La tabella segue dal teorema cinese del resto applicato a `u mod9` e `3u+1≡0 mod2^j₀`. Le classi sono disgiunte. La densità fra tutti gli interi positivi è `6935/98304`, circa 7,05%; fra i dispari è circa 14,11%. **La copertura delle orbite eccezionali non segue da questa densità.**

La copertura segue così. Un'orbita positiva che non raggiunge 1 o entra in un ciclo non banale, oppure tende a infinito: un'orbita illimitata che rivisitasse indefinitamente un insieme finito ripeterebbe uno stato e diventerebbe periodica. Applicando il teorema di Monks a ogni coda dell'orbita T si ottengono visite arbitrariamente tarde a `20 mod27`. Dopo il primo passo S nessuno stato è multiplo di 3. Ogni episodio dispari-dispari è finito; infinite visite marcate richiedono quindi infiniti episodi marcati. Per l'equivalenza della tabella, le loro sorgenti appartengono a E.

**Conclusione: ogni eventuale orbita eccezionale di S visita E a tempi arbitrariamente grandi.** Nei cicli non sono necessariamente punti distinti. Il risultato trasferisce un teorema noto a una sezione adatta ai cilindri del progetto; non ne rivendico la priorità assoluta.

Questo è un miglioramento dell'impostazione: la scelta della regione di lavoro non ha più una copertura globale meramente ipotizzata, come avverrebbe scegliendo una famiglia A0 arbitraria. Rimane interamente aperta la discesa tra i ritorni.

Abbiamo controllato l'equivalenza dell'episodio su **333.333 sorgenti dispari ammissibili sotto un milione**, senza discrepanze. Il controllo finito verifica le trascrizioni; la prova generale è l'argomento modulare appena dato. La derivazione è stata riesaminata separatamente dagli agenti di questa sessione; non è una peer review esterna.

Tre dettagli impediscono false semplificazioni:

- La sorgente va esclusa dall'episodio: `47≡20 mod27`, ma 47 non appartiene a E e il suo episodio successivo non incontra la classe.
- Il ritorno a E è parziale sulle orbite generiche: `13∈E`, ma `13→5→1` non ritorna.
- Il primo ritorno non riduce sempre n: `31→47→71→107→161→121`, e 31 e 121 appartengono a E mentre gli stati intermedi no. Questo smentisce il rango n al primo ritorno su tutto E; non una proposizione ristretta alle ipotetiche orbite non convergenti.

## 6. Un nuovo controllo severo della famiglia di cancellazione

La v6 contiene già, per k pari almeno 4,

\[
 n_k=\frac{2^{k+1}-11}{3},\qquad S(n_k)=m_k=2^k-5.
\]

Ho esteso l'analisi all'uscita completa dal fantasma `[1,2]`. Questo sviluppo è una deduzione algebrica su carta accompagnata da un esperimento esatto, non una nuova dichiarazione Lean.

Poniamo

\[
 r=\left\lfloor\frac{k-1}{3}\right\rfloor,\qquad h=k-3r\in\{1,2,3\}.
\]

Poiché il blocco `[1,2]` agisce come `x↦(9x+5)/8`, da mₖ si eseguono esattamente r copie complete e si arriva a

\[
 x_r=2^h9^r-5.
\]

Il primo tratto che abbandona quella ripetizione ha una delle tre forme:

| h | Esponenti terminali | Endpoint y | Informazione 3-adica esatta |
|---:|---|---|---|
| 1 | `[3]` | `(3·9^r−7)/4` | `4y+7=3^(2r+1)` |
| 2 | `[1,1]` | `9^(r+1)−10` | `y+10=3^(2r+2)` |
| 3 | `[1,4]` | `(9^(r+1)−5)/4` | `4y+5=3^(2r+2)` |

Le valutazioni terminali si ottengono usando `9^r≡1 mod8`. Il segmento completo dalla sorgente è `[1]`, seguito da `[1,2]^r`, seguito dalla parola terminale.

Il rapporto `y/n_k` cresce asintoticamente come

\[
 c_h(9/8)^r,
 \qquad c_1=9/16,\quad c_2=27/8,\quad c_3=27/64.
\]

Non c'è quindi una compensazione automatica della crescita all'uscita del fantasma. Più precisamente, per **ogni k pari almeno 30**, nessuno stato di questo segmento è inferiore a nₖ e l'endpoint y è strettamente maggiore. Una dimostrazione elementare usa:

\[
\begin{array}{ll}
h=1:&12(y-n_k)=9^{r+1}-16\,8^r+23,\\
h=2:&3(y-n_k)=27\,9^r-8\,8^r-19,\\
h=3:&12(y-n_k)=27\,9^r-64\,8^r+29.
\end{array}
\]

Per le fasi compatibili con k pari, le ultime espressioni sono positive rispettivamente da r=5, r=2 e r=9. La dominanza resta vera aumentando r perché 9 cresce più rapidamente di 8. Gli endpoint dei blocchi `[1,2]` e i passi di esponente 1 sono crescenti, quindi resta da controllare soltanto l'eventuale ultimo passo contrattivo. La soglia comune k≥30 è sufficiente.

Ho verificato tutte le parole e identità con interi a precisione arbitraria per **999 valori pari, 4≤k≤2000**. Tutti hanno poi mostrato una prima discesa nel test finito; questo non prova la discesa per tutti i k.

| k | Passi S fino all'uscita descritta | log₂(y/nₖ), solo diagnostico | Prima discesa osservata |
|---:|---:|---:|---:|
| 30 | 21 | 0,28421 | 23 |
| 100 | 68 | 4,77745 | 70 |
| 200 | 135 | 12,96994 | 169 |
| 500 | 335 | 29,96244 | 435 |
| 1000 | 668 | 55,75495 | 832 |
| 2000 | 1335 | 114,92494 | 1612 |

Le disuguaglianze e le identità sono controllate esattamente; i logaritmi servono solo alla visualizzazione numerica. Il massimo tempo di prima discesa osservato nei 999 casi è 1649 passi, a k=1988.

La famiglia colpisce anche la sezione proposta: per k pari,

\[
 n_k\in E\quad\Longleftrightarrow\quad k\equiv10\pmod{18}.
\]

Infatti il primo esponente è 1, quindi può valere solo la prima riga della tabella; la condizione si riduce a una potenza di 2 modulo 27. Per questi k il primo endpoint `2^k−5` è già `20 mod27`. Il banco di prova non elimina artificialmente le difficoltà scegliendo una regione favorevole. L'uscita del fantasma non va però identificata con il primo ritorno a E: possono esserci visite intermedie.

## 7. La nuova via: conservare la struttura durante interi ritorni

Per una parola espansiva w, scriviamo `P=3^ℓ`, `Q=2^A`, `D=P−Q`, `H(n)=Dn+C`. Il risultato del progetto dà, su j copie effettivamente seguite,

\[
 H(n_j)=\frac{P^j}{Q^j}H(n_0).
\]

Se `H(n₀)=2^(jA+h)u`, con u dispari, allora

\[
 H(n_j)=2^h3^{\ell j}u.
\]

La compressione esatta deve conservare j e il cofattore u. Registrare soltanto la precisione 2-adica scarta la divisibilità 3-adica accumulata. Tuttavia questa identità da sola non è un rango: `log₂H−ν₂(H)` **aumenta** di `jℓ log₂3`. Anche il principio di trasferimento 2-adico/3-adico ha precedenti espliciti, inclusi programmi contemporanei ([esempio di note di lavoro](https://github.com/macindoe/collatz/blob/main/reverse.md)); non lo presento come scoperta.

Propongo di costruire oggetti che rappresentino famiglie di interi mediante una fase di ingresso in E, vincoli esatti sui residui, un contatore di ripetizione non limitato, cofatori e un confronto con la sorgente del ritorno. La ricerca può suggerire transizioni; un checker deve verificare identità, esattezza degli esponenti e copertura di tutti i casi. Le radici residue non trattate devono restare esplicitamente aperte.

La differenza operativa rispetto alle strade già tentate è precisa:

1. **La sezione E ha copertura dimostrata per ogni ipotetica orbita eccezionale.** Non viene scelta soltanto perché i dati sono favorevoli.
2. **Le torri si rappresentano con parametri.** Un ciclo `[1,2]^r` è una famiglia intera, non r righe aggiuntive di una matrice.
3. **Si certifica un esito puntuale del ritorno.** L'esito deve essere raggiungere 1, raggiungere una sorgente di sezione con rango inferiore, oppure lasciare una precisa obbligazione non risolta.

Un possibile teorema finale del checker sarebbe: esiste una funzione di stato R a valori in un ordine ben fondato tale che, per ogni n∈E, o un iterato raggiunge 1, oppure esiste un tempo positivo k con `S^k(n)∈E` e `R(S^k(n))<R(n)`. Con la copertura di E questo implicherebbe Collatz. **Questo enunciato rimane aperto ed è ancora sostanzialmente un bersaglio equivalente alla congettura**, non una scorciatoia già risolta. Il vantaggio cercato è nella rappresentazione delle obbligazioni e nella possibilità di chiuderne famiglie infinite, non nella loro scomparsa.

Come caso minimo concreto, per ogni intero t≥0 vale

\[
 S(661+1152t)=31+54t<661+1152t,
\]

ed entrambi i membri appartengono alla prima classe di E. Infatti `3(661+1152t)+1=64(31+54t)` e il quoziente è dispari: l'esponente è esattamente 6. È una famiglia infinita di ritorni discendenti con prova algebrica immediata. La propongo come test di correttezza del checker, non come risultato profondo o rivendicazione di priorità.

La prima vera sfida è certificare una famiglia con numero di ripetizioni non limitato, oltre una semplice foglia affine. La torre precedente impedisce di accettare il criterio falso «l'uscita da una cancellazione compensa la crescita».

## 8. Programma di lavoro e criteri per fermare una strada improduttiva

| Ordine | Consegna verificabile | Cosa non conterebbe come successo |
|---|---|---|
| 1 | Formalizzare la traduzione dell'episodio e le sei classi; poi la copertura usando una prova del caso Monks pertinente. | Assumere la ricorrenza di E come nuovo assioma. |
| 2 | Formalizzare la formula generale dei blocchi ripetuti e le tre uscite della torre, inclusa la crescita per k≥30. | Testare molti k e promuovere il risultato a universale. |
| 3 | Definire un formato di certificato e un checker Lean; validare il ritorno `661+1152t` e rifiutare il falso rango del primo ritorno da 31. | Un parser che verifica soltanto un'identità affine ma non gli esponenti o il dominio. |
| 4 | Chiudere una famiglia infinita con parametro di ripetizione realmente non limitato; pubblicare tutti i rami residui. | Coprire una frazione quasi totale dei campioni o del peso di una matrice. |
| 5 | Cercare composizione dei certificati e un rango ben fondato su più ritorni. | Nascondere la conclusione desiderata nella definizione del rango. |

Sconsiglio di fissare ora una promessa temporale per il quinto punto. I primi tre sono obiettivi delimitati; il quarto è ricerca matematica autentica; il quinto contiene ancora l'ostacolo globale.

Se la normalizzazione continua a produrre nuove radici e cofatori non correlati e non si trova un invariante capace di trattarli uniformemente, quella classe di stati va considerata insufficiente. La risposta utile è un teorema o controesempio che lo documenti, non aumentare indefinitamente il cutoff.

La via alternativa più prudente è una nota specialistica di verifica formale: copertura della sezione, lemma delle torri e ostruzioni ai ranghi finiti. Sarebbe un prodotto scientifico valutabile anche se non porta alla congettura. La promessa di innovazione va legata a questi enunciati concreti e confrontata con i repository correnti, non a un'etichetta come «approccio adelico».

## 9. Indicazioni per la prossima versione e riproduzione

Il README principale e alcuni documenti chiamano ancora v6 «local draft» e v5 «latest published»: sono da aggiornare ora che il deposito è confermato. Non li ho modificati durante questa analisi. Conservare i pacchetti pubblicati e indicare chiaramente quali nuovi teoremi appartengono alla futura versione.

Per una prossima pubblicazione, darei priorità a: confronto esplicito con Terras e Bernstein–Lagarias; confronto concreto con Kramer e Sharpe; enunciati formali della nuova sezione e della torre; replay del toolchain aggiornato; un audit di assiomi ripetibile. Il numero di linee di Lean o di casi calcolati non dovrebbe essere l'argomento principale di novità.

I nuovi risultati algebrici di questa nota sono **su carta**, con verifiche Python esatte; non sono stati inseriti nel nucleo Lean. Gli script sono eseguibili con Python 3 senza librerie esterne, dalla cartella di questa nota:

```bash
python3 section_probe.py --limit 1000000
python3 tower_probe.py --max-k 2000
```

`section_results.json` e `tower_results.json` conservano gli esiti, incluso il carattere finito dei test. `section_derivation.md`, `tower_derivation.md` e `section_independent_review.md` contengono derivazioni e controlli ulteriori; `literature.md` è la ricognizione bibliografica estesa; `lean_audit.md` registra la verifica del progetto.

La raccomandazione è investire il prossimo ciclo di lavoro nella **formalizzazione della copertura e nella compressione parametrica delle torri**, misurando il progresso in famiglie infinite effettivamente risolte. È la continuazione più concreta che ho identificato rispetto al nucleo della v6, con ostacoli espliciti e un primo programma falsificabile.
