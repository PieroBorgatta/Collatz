# Mappa critica dei risultati e degli ostacoli

26 settembre 2026. Audit interno documentale; nessuna rivendicazione di
originalità. Le nuove build e i replay del consolidamento sono documentati
separatamente nella [relazione](RESULTS_IT.md).

## 1. Tre domande distinte

| Obiettivo | Quanto è ottenuto | Passaggio mancante |
|---|---|---|
| Collatz per ogni positivo | Copertura universale da 1 o dalla sezione E; aritmetica esatta dei cilindri e di alcune famiglie di ritorni | Controllo ben fondato di tutte le successive escursioni da E, o altro principio universale |
| Discesa della torre speciale `Q_v` | Certificati finiti sino a v24, trasferimenti sufficienti, rappresentazioni esatte e ostacoli ai modelli semplificati | Maggiorazione indipendente delle parità per tutti i livelli; poi resterebbe comunque la copertura universale |
| Densità dei predecessori | Lemmi di occupazione, due semi espliciti e migliori costanti nella composizione con la catena esterna | Revisione specialistica e verifica attuale dell'intera catena; nessun passaggio automatico alla convergenza punto per punto |

`Q_v(q)` con q dispari libero non è il solo `Q_v=Q_v(1)`. «Ogni parola finita
è realizzata da qualche q» non significa «esiste un q naturale che realizza
un'intera parola infinita». Un controesempio in una classe di completamenti
non è un controesempio nella torre.

## 2. Registro epistemico

**F**: dichiarazioni Lean e verifiche storiche documentate; **C**: dimostrazione
su carta; **E**: calcolo esatto finito; **H**: ipotesi aperta. F non significa
che questo audit abbia rieseguito il controllo; E non prova un enunciato
uniforme. Le build della libreria preesistente non formalizzano le nuove note C.

| Ramo e fonti | Stato | Risultato da conservare | Inferenza da respingere |
|---|---|---|---|
| [V6](../../paper/collatz_spectral_reduction_v6.tex) | F/C | Cilindri esatti; tassa di precisione per parola espansiva fissata; trasporti compatibili; vincoli sui cicli; test di barriera | Repetizioni finite limitate non escludono cambi arbitrari di parola; matrice finita non dà gap infinito |
| [Sezione e torri](../post_v6_section_2026-09-24/RESULTS_IT.md) | F | Copertura da `20 mod27`; sei progressioni E; ricorrenza di E; formule universali di cancellazione; nessun orizzonte fisso di discesa per tutte le sorgenti marcate | Copertura della sezione non significa terminazione; endpoint di torre non significa primo ritorno |
| [Conteggio](../post_v6_counting_2026-09-24/RESULTS_IT.md), [adapter](../post_v6_adapter_2026-09-24/RESULTS_IT.md), [ottimizzazione](../post_v6_optimization_2026-09-24/RESULTS_IT.md) | F, con catena esterna distinta | Occupazione pesata senza iniettività; coppia limitata di semi; nonritorno; miglioramento formale di coefficiente e cutoff | Nonritorno non è divergenza; densità positiva non è convergenza universale; mixing probabilistico non è indipendenza lungo un'orbita |
| [Trasporto](../post_v6_transport_2026-09-24/RESULTS_IT.md) | F | `Q_v(q)` è isometrica e biiettiva sui residui; ogni suffisso ammissibile ha una classe di parametri; criterio esatto per parametro limitato | Nessuna proibizione finita uniforme sui q liberi; nessuna orbita divergente costruita |
| [Certificati](../post_v6_certificates_2026-09-24/RESULTS_IT.md), [induzione](../post_v6_induction_2026-09-25/RESULTS_IT.md) | C/E; criterio generale e trasferimento F | La somma di esponenti sufficiente dà una visita sotto soglia; nel trasferimento basta `c u≤96w²` | L'ipotesi superiore resta da provare; aspettare la discesa per scegliere il tempo non chiude l'induzione |
| [Compensazione](../post_v6_compensation_2026-09-25/RESULTS_IT.md) | C/E/H | Limite sufficiente sulla massima perdita; tre livelli 22–24 separati dalla calibrazione lo rispettano | Il limite `128v²` è empirico e resta H; milioni di passi non sono milioni di campioni indipendenti |
| [Aritmetica](../post_v6_arithmetic_2026-09-25/RESULTS_IT.md) | C/E | Divisibilità esatta della parola completa; limite quantitativo della specifica applicazione di Chim | Una riscrittura di congruenza non controlla le parità; densità di dispari non implica bassa complessità digitale |
| [Margine](../post_v6_margin_2026-09-25/RESULTS_IT.md) | C/E/H | Telescopio esatto; costi sufficienti espliciti; controesempi alla sola ricorrenza più prefisso e altezza | Stimare il coefficiente quadratico senza vincolo indipendente rinomina Δ; stima cumulativa equivalente al margine non è un progresso |
| [Ancestry](../post_v6_ancestry_2026-09-25/RESULTS_IT.md) | C/E | Due antenati, binade e parola inferiore completa isolano `Q_v`; conteggi esatti dell'intervallo radice | Rigidità del punto non è controllo del suo peso di parità; pochi candidati non implica candidati favorevoli |
| [Ternario](../post_v6_ternary_2026-09-25/RESULTS_IT.md) | C/E | Bound uniforme della prima giunzione `O(sqrt(m) log²m)`; controesempio ai sei pesi additivi locali | Sommare il bound su stati trasformati senza ipotesi valide; chiamare i bilanci identici una nuova stima |
| [Propagazione](../post_v6_propagation_2026-09-25/RESULTS_IT.md) | C/E | Quoziente originario esatto a ogni tempo; raccordo dei riporti originali | Il bound modulare perde efficacia prima del clock utile; tempi uguali e tempi raddoppiati sono problemi diversi |
| [Tail](../post_v6_tail_2026-09-25/RESULTS_IT.md) | C/E | Trasduttore e bilancio completi; precisione necessaria e sufficiente per blocchi; ostacoli di memoria sul dominio generico | Cancellazioni numeriche grandi non danno bound uniforme; rinnovo tramite stato esatto non è rinnovo a memoria limitata |
| [Renewal](../post_v6_renewal_2026-09-26/PROOF_IT.md) | C/E | `Δ_max(M)=K−2j_L−Z_U(M)`; arresto ottimale nel modello dei prefissi; ciclo a premio positivo nella proiezione dei residui | Nessun limite universale alla complessità di ogni prova; nessun ciclo Collatz infinito costruito |
| [Sette antenati](../post_v6_seven_ancestors_2026-09-26/RESULTS_IT.md) | C/E | Testimone al livello 11: margine `34→−18` con tutti i filtri fissati | Non confutarvi la rigidità con parola completa, che il testimone non conserva |
| [Riporti binari](../post_v6_binary_carries_2026-09-26/RESULTS_IT.md) | C/E | Generatore esatto dal seme 3; ridondanza dei riporti esposti; collisioni per ogni finestra finita sul dominio generale | Nessuna impossibilità di memoria per la sola torre; selettività futura non significa sufficienza |
| [Vincolo di riporto](../post_v6_carry_constraint_2026-09-26/RESULTS_IT.md) | C/E | Fascia lineare esatta; testimone v16 con riporto 31655 e `Δ=31168` | La fascia non produce il budget; non estendere il risultato negativo ai soli punti esatti `Q_v` |

## 3. Equivalenze, sufficienze e circolarità

- `UniformStrictDescentHypothesis` è equivalente alla convergenza universale
  dei dispari: discesa e induzione forte in un verso, visita a 1 nell'altro.
- L'esistenza di `SectionReturn.RankDescent` è formalmente equivalente alla
  congettura accelerata. La copertura permette di formularla sulla sezione,
  ma non la dimostra.
- Escludere tutte le codifiche non eventualmente periodiche dai positivi
  equivale all'assenza di orbite illimitate, non esclude da solo cicli non banali.
- Il bound uniforme su Δ è una condizione sufficiente per la torre; non si
  afferma un'equivalenza con Collatz o con la discesa effettiva della torre.
- La positività di tutti i margini equivale alle corrispondenti disuguaglianze
  sulle somme parziali pesate di Δ. Ricavare tali somme dagli stessi conteggi
  non è una prova indipendente.
- I criteri «parola contrattiva e sorgente sopra la barriera» sono utili se
  parola e dominio sono certificati indipendentemente. Valutare la barriera
  dopo aver selezionato un endpoint già minore riformula il risultato osservato.

## 4. Strumento alternativo: domini esatti di ritorni composti

La copertura di E offre un oggetto globale effettivo. La proposta è studiare
macro composte da ritorni a E, conservando parametri interi, domini esatti e
disuguaglianze affini. Un tale programma non beneficia automaticamente della
libertà dei suffissi né della statistica sulla torre q=1. Per coprire le torri
note dovrà ammettere durate non limitate e comprimerle con formule provate.

### Primo lemma pilota, derivato su carta

Per ogni `t≥0`, sia `n=205087+1179648t`. La sua traiettoria iniziale è:

| Tempo S | Valore esatto | Esponente per il passo seguente |
|---:|---|---:|
| 0 | `205087+1179648t` | 1 |
| 1 | `307631+1769472t` | 1 |
| 2 | `461447+2654208t` | 1 |
| 3 | `692171+3981312t` | 1 |
| 4 | `1038257+5971968t` | 2 |
| 5 | `778693+4478976t` | 4 |
| 6 | `146005+839808t` | — |

Ogni riga successiva è dispari e `3x+1` è la potenza di due dichiarata
moltiplicata per essa: ciò certifica gli esponenti esatti, per tutti i t.
Le righe 0 e 5 sono `13 mod18`; la riga 6 è `853 mod1152`. Le righe 1–4
hanno rispettivamente residui `47,71,35,17 mod72`, incompatibili con tutti
i sei porti di E. Quindi i tempi 5 e 6 sono i primi due ritorni consecutivi.

Le differenze sono

\[
S^5(n)-n=573606+3299328t>0,\qquad
n-S^6(n)=59082+339840t>0.
\]

Anche le righe 1–4 superano n. La discesa avviene quindi dopo una vera
escursione crescente, non è un ritorno successivo a una discesa già avvenuta.

**Derivazione del dominio.** La famiglia `31+1152a` ha parola
`[1,1,1,1,2]` e primo ritorno `121+4374a`. Imporre esponente 4 al passo
seguente equivale a `a=2+16u`. Si ottiene il secondo endpoint
`1663+13122u`. Imporne l'appartenenza al porto `853 mod1152` equivale a
`u=11+64t`, da cui la famiglia sopra. Il secondo endpoint appartiene a quel
porto per costruzione, non perché una semplice discesa garantisca un ritorno.

**Valore e limite.** Il lemma esemplifica un certificato di due ritorni con
crescita intermedia e dominio universale parametrico. È aritmetica classica
dei cilindri; non se ne rivendica la novità. La parola totale è già contrattiva,
con pendenza `729/1024`, quindi la sua discesa ricade nel criterio di barriera
esistente. Senza confronto con le famiglie già coperte non va presentata
neppure come incremento netto di copertura. Il lemma è C in questa nota:
un'eventuale dichiarazione Lean e relativo audit devono essere documentati
separatamente.

### Arresto ed esito che giustificherebbe continuare

La fase pilota termina con la verifica simbolica/formale del lemma, il suo
dominio e il confronto di copertura. Si registra il complemento di E che non
è trattato; non si inferisce nulla su di esso. Non si avvia un'esplorazione
illimitata di moduli e parole. Per continuare servirebbe una famiglia a durata
non limitata con una transizione parametrica che diminuisca un rango e una
prova che gestisce una parte precedentemente non coperta, oppure un lemma
strutturale indipendente che organizzi tali domini. «Esiste una macro
discendente per ogni punto di E» sarebbe ancora l'obiettivo, non il lemma.

La famiglia alternativa `661+73728t → 31+3456t → 121+13122t` è invece un
esempio da non contare come progresso: ha già discesa al primo passo, nella
famiglia formalizzata `descending_return_family`. Comporre dopo una crescita
non aggiunge copertura né supera un ostacolo precedente.

## 5. Riuso dei due semi e decisione pratica

Il riuso difendibile dei due semi è nel problema dei predecessori: selezione
quantitativa di semi, unicità delle visite al seme nonperiodico, controllo
delle costanti e delle dipendenze analitiche. Entrambi i candidati hanno lo
stesso futuro dopo un passo; l'esistenza di uno senza ritorni non forza quel
futuro a raggiungere 1. Usarlo come principio di fuga dai cicli o di discesa
globale aggiungerebbe una conclusione assente dal lemma.

Una proposta ulteriore può però usare il ramo dei predecessori senza
confonderlo con una conclusione di convergenza già ottenuta: cercare una
comparabilità **relativa** di bacini distinti che si uniscono al passo
successivo. Di seguito sono separati riduzione condizionale e nuovo ostacolo.

### Amplificazione lungo un'ipotetica orbita illimitata

Sia `B(n)={m>0 : un iterato ordinario di m è n}`, incluso n stesso, e sia
`d_*(B(n))=liminf_N #(B(n)∩[1,N))/N`. Per n dispari positivo con `3∤n`,
poniamo

\[
y(n)=\begin{cases}4n+1& n\equiv1\pmod3,\\
16n+5& n\equiv2\pmod3.\end{cases}
\]

Questi interi sono dispari, non divisibili per 3, soddisfano `y(n)>n`,
`y(n)≤16n+5` e `S(y(n))=S(n)`. L'idea richiede la seguente stima nuova:

\[
\tag{H}
\exists c>0\ \forall n:\quad
d_*(B(y(n)))\ge\frac{c}{1+\log n}\,d_*(B(n)),
\]

con ipotesi esplicite `n>0`, n dispari, `3∤n`, e assenza di ritorni positivi
sia per n sia per y(n). Non si presume di poter decidere tali ipotesi.
**(H) non è provata, né supportata da un bound relativo già presente.**

La sua sufficienza per escludere orbite illimitate si dimostra così:

1. Un'orbita Syracuse illimitata `x_0,x_1,…` non ripete alcun punto.
   Si può iniziare dopo il primo passo per avere `3∤x_0` e quindi `3∤x_i`.
2. Nessun `y(x_i)` appartiene alla spina `x_j`: dopo un passo avrebbe
   successore `x_(i+1)`, contraddicendo l'iniettività della spina. Tutti
   i fratelli sono nonperiodici, perché si immettono in quella spina.
3. I bacini dei fratelli sono disgiunti. Se una sorgente raggiungesse due
   fratelli, quello visitato per primo dovrebbe poi raggiungere il secondo;
   dopo il primo passo si trova invece sempre sulla spina.
4. `B(x_0)⊆B(x_i)`; la densità inferiore del primo è `δ>0` mediante la
   catena analitica esterna. Poiché `S(n)≤2n`,
   `1+log x_i≤1+log x_0+i log2`.
5. (H) darebbe, per ogni M,

   \[
   1\ge\sum_{i<M}d_*(B(y(x_i)))
     \ge c\delta\sum_{i<M}\frac1{1+\log x_0+i\log2}.
   \]

   La prima disuguaglianza usa disgiunzione e superadditività del liminf
   per una somma **finita**. L'ultima somma diverge, contraddizione.

Non serve che i cutoff delle densità siano uniformi lungo la spina. La
dimostrazione è condizionale: non trasferisce la positività assoluta in
comparabilità relativa. Non elimina i cicli non banali, sui quali la spina
si ripete e la disgiunzione viene meno. Non è stata provata un'equivalenza
fra (H) e Collatz; (H) è un enunciato nuovo e forte del programma, non una
conclusione dei teoremi già disponibili.

### Due ostacoli da conservare nel protocollo

**Restrizione ai fratelli vicini.** Se si quantificasse su tutti gli y
nonperiodici con `S(y)=S(n)`, mantenendo il denominatore dipendente soltanto
da n, il lemma sarebbe falso. Fissato un n nonperiodico, fra gli infiniti
`L^k(n)` con `L(n)=4n+1` al più uno può essere periodico: la funzione è
iniettiva sui suoi punti periodici. Infiniti altri non sono divisibili per 3
e hanno bacini disgiunti. Un identico lower bound positivo violerebbe il
vincolo di densità. La formula y(n), o un vincolo comparabile d'altezza,
è quindi essenziale, non un dettaglio tecnico.

**Le parole inverse identiche non si trasportano.** Per una parola di k≥1
passi, se `2^A n=3^k x+C`, la sorgente corrispondente alla stessa parola e
all'endpoint y sarebbe

\[
x'=x+\frac{2^A(y-n)}{3^k}.
\]

Qui `y−n=3n+1` oppure `5(3n+1)`, entrambi primi con 3; x' non è intero.
Una comparazione dei bacini richiede quindi di cambiare le parole e
controllarne massa, altezza e molteplicità. Applicare L alle sorgenti
conserva il loro successore e non devia il futuro verso il fratello del
bersaglio. Un semplice argomento di iniezione con lo stesso itinerario
non può provare (H).

**Primo compito e arresto.** Prima di censimenti più grandi, formulare e
dimostrare una comparazione di famiglie inverse diverse con perdita relativa
esplicita, sotto un cutoff e una profondità dichiarati. Verificare poi che
i costi restino compatibili con (H) nel limite. Fermarsi se il confronto usa
già (H), la convergenza, o soltanto i lower bound assoluti esistenti. Un
rapporto finito piccolo è diagnostico; senza un bound sull'errore e sulle
soglie non confuta (H). Il censimento non deve essere presentato come stima
del limite né usato per modificare retrospettivamente il denominatore.

Il collegamento con letteratura e precedenti resta da accertare: questa
nota identifica una direzione nuova **nel programma locale**, non una
novità scientifica. Un revisore dovrebbe valutare soprattutto la plausibilità
del confronto relativo, non la sola correttezza dell'argomento armonico.

Priorità proposta: congelare le famiglie di filtri confutate; consolidare
l'evidenza formale; far valutare esternamente la parte analitica e i pochi
risultati autonomi su carta. Il pilota dei ritorni è un modo limitato di
valutare un'interfaccia diversa, non una nuova campagna autorizzata dalla sola
assenza di controesempi. Nuovi livelli della torre o nuovi filtri, senza una
stima indipendente già formulata, non sono il prossimo investimento consigliato.
