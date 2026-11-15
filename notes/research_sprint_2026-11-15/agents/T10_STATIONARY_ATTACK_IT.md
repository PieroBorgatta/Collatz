# T10 — Nuova regolarità critica e un ponte aritmetico al cap del moltiplicatore

15 novembre 2026. Ricerca iniziata alle 20:47 UTC. **Stato:** deduzioni su carta, controlli razionali indipendenti e audit di una nuova fonte primaria. Nessun teorema esterno è stato importato nella libreria Lean, nessun codice del supplemento esterno è stato eseguito. Non si è ottenuto un rate uniforme di rilassamento, una quota η o una soluzione di Collatz.

## 1. Aggiornamento web del 14 novembre

La fonte [rStation 146/v1, *Exact critical tail and linear collision energy for the ternary Syracuse law*](https://rstation.ai/problems/collatz/papers/146), pubblicata il **14 novembre 2026 alle 16:51 UTC**, tratta la stessa legge geometrica originale e Haar di probabilità sull'intero Z₃. Dichiara una coda esatta κt⁻², weak L², energia dei cilindri comparabile alla profondità e finitezza dell'interazione fra branche. Non dichiara incrementi energetici uniformemente limitati, convergenza dell'energia divisa per la profondità o controllo degli interi.

Il testo completo versionato è stato letto, compreso il §5. Ho ricostruito: normalizzazioni del tilt, momento al record, conteggio dei prefissi con divisioni aggiuntive, costo probabilistico, somma sui ritardi e partizione per il primo supporto. Non ho trovato un errore nel nucleo esaminato. T11 esegue una seconda lettura indipendente. Questo è un audit matematico, **non** una formalizzazione o una certificazione definitiva.

Il manoscritto dichiara CC BY 4.0 ed è archiviato senza modifiche in `research/research_sprint_2026-11-15/t10/sources/`, con NOTICE e manifest. URL originale versionato: `https://rstation.ai/api/v1/papers/collatz_146/versions/1/download`; SHA-256 `ff3c011022cd87f7f068c30759b732e7b92bb24f9269856dba4e851491c3e150`.

## 2. Risolvente dell'odometro e collocazione bibliografica

Poniamo H(y)=4y+1, f=ρ_k e g(y)=ρ_(k+1)(3y+1). Due applicazioni della ricorrenza binaria effettiva danno esattamente

`g(y)=(1/4)g(Hy)+(3/4)f(Hy)`.

Poiché f e g hanno periodo 3^k e H è un ciclo unico su Z/3^kZ, con q=3^k si ottiene

`g(y)=3/(4^q−1) Σ_(j=1)^q 4^(q−j) f(H^j y)`.

Equivalentemente, a k fissato,

`g(y)=3 Σ_(j≥1)4^(−j) f(H^j y)`.

Definiti C_k(j)=∫ρ_k(y)ρ_k(H^j y)dλ(y) e H_k=∫gρ_k dλ, segue

`H_k=3 Σ_(j≥1)4^(−j) C_k(j)`,
`N_(k+1)−N_k=(2/3)H_k=2 Σ_(j≥1)4^(−j)C_k(j)`.

**Non si rivendica novità bibliografica:** l'ultima interazione è già esplicita nella formula (22) del nuovo paper e nelle fonti che esso cita. Il terminal fan Ψ_j=H^j è inoltre già usato nella fonte Valbuena per un'altra legge di riferimento ϱ_m. Quella legge ha media 2/3, mentre la ρ_m stazionaria ha media 1: il suo fan piatto di media 8/9 non è un bound per il nostro correlatore pesato con ρ_k.

Un bound C_k(j)≤K(j), uniforme in k e con Σ4⁻ʲK(j)<∞, sarebbe sufficiente a limitare ogni incremento energetico. Il nuovo paper dà invece il risultato più debole, ma sufficiente al proprio scopo, N_k=O(k) e finitezza dell'interazione limite. Non è stato dimostrato qui il bound uniforme degli incrementi.

### Contro-modello alla sola struttura di odometro

Il modello T07 può essere accoppiato lungo H. Per j≥1 porre

`a_j=(3^j−1)/2`, `A_j=a_j+3^(2j)Z₃`,
`b_j=2·3^j−1`, `B_j=b_j+3^(2j)Z₃=H(A_j)`.

Le due famiglie sono disgiunte: A_j appartiene alla classe 1, B_j alla classe 2 modulo 3; dentro ciascuna famiglia la differenza dei centri ha valutazione min(j,l). Definire

`F=(3/4)1_U+(1/2)Σ_(j≥1)3^j(1_(A_j)+1_(B_j))`.

La massa è uno. F è semicontinua inferiormente, massima fra i rappresentanti lsc della propria densità, finita e localmente costante a ogni positivo intero; è in L^p esattamente per 1≤p<2, ha energia dei cilindri O(m) e mixing L¹ esponenziale come T07. Tuttavia, su A_j, entrambi F(y) e F(Hy) sono almeno 3^j/2. Ogni j contribuisce almeno 1/4 all'integrale; dunque

`∫F(y)F(Hy)dλ=∞`.

Per le medie finite f_m, la correlazione è almeno floor(m/2)/4. F(Hy)=F(y) sulla classe 1; infatti, per m≥1, l'energia totale finita è il doppio di tale correlazione. Al livello m=0 si ha invece f₀=1 e N₀=C₀(1)=1. Questo **non** è un controesempio alla vera legge: F non soddisfa la sua ricorrenza binaria o la risolvente fra livelli. Mostra perché supporto, odometro e norme globali, da soli, non forniscono il bound mancante.

## 3. Positività intera: il moltiplicatore è automaticamente limitato

Questo ponte è stato individuato con il coordinatore e ricostruito indipendentemente. Si riferisce a un cap del **massimo moltiplicatore reale**, non al cap degli esponenti trattato da T08.

Sia n un positivo dispari. Per una parola outermost-first w=(e₁,…,e_m), scrivere

`A_i=3^i 2^(−D_i)`, `B_i=(1/3)Σ_(j≤i)A_j`, `D_i=Σ_(j≤i)e_j`.

Se il suo cilindro 3-adico contiene n, ogni prefisso i≤m ha una sorgente intera positiva Y_i con

`n=B_i+A_iY_i`.

Si usa il dizionario affine del progetto invertendo l'ordine della parola. L'integralità discende dalla congruenza ternaria completa; la positività intera è proprio il contenuto aritmetico verificato in `AffinePositivity`. Pertanto **A_i≤n per ogni i≤m**. Nessun codice che contribuisce all'atomo intero n può avere già superato n come moltiplicatore.

Ne segue ρ_m(n)=f_(m,B)(n) per ogni B≥n, dove f_(m,B) impone soltanto il cap fino al tempo m. Questo non identifica automaticamente la misura con cap infinito σ_B.

## 4. L'errore del cap infinito è uniforme nella profondità

Sotto il codice geometrico originale P(e)=2⁻ᵉ, A_i è una martingala nonnegativa, perché E(3·2⁻ᵉ)=1. Da un prefisso w, la probabilità di superare in futuro B>n è quindi al più A_m/B. Il futuro è indipendente dal prefisso e l'appartenenza al cilindro C_m(n) dipende soltanto dal prefisso. Sommando:

`0≤ρ_m(n)−3^m σ_B(C_m(n))≤ρ*_m(n)/B`,

dove P*(e)=3·4⁻ᵉ e ρ*_m è la densità del suo atomo modulo 3^m. Infatti P*(w)=A_wP(w).

Esiste un upper aritmetico semplice e uniforme:

**`ρ*_m(n)≤2n²` per ogni m.**

A lunghezza m e totale D fissati, A=3^m2⁻ᴰ è costante. Le parole ammissibili hanno sorgenti intere **distinte** Y, per l'iniettività del dizionario, e 1≤Y≤n/A. Il loro numero c_D è quindi ≤n/A. Poiché 3^mP*(w)=A²,

`ρ*_m(n)=Σ_D A²c_D≤n Σ_(D:A≤n)A≤2n²`.

L'ultima somma è geometrica: aumentando D di uno, A si dimezza, e il massimo ammesso è al più n. Tutti i termini sono nonnegativi, quindi il passaggio alla somma infinita è legittimo. Il caso m=0 è immediato.

Una prova più diretta, usata dal coordinatore nel nucleo Lean `IntegerAtomTilt`, sfrutta che a lunghezza fissata tutte le sorgenti sono distinte anche quando il totale varia: `Σ_w A_w²≤n²Σ_u u⁻²≤2n²`. Il modulo formalizza cataloghi finiti e il loro budget; il passaggio alla legge infinita, il cap e la traccia restano applicazioni analitiche su carta.

Abbiamo così una stima **uniforme nella profondità**:

`0≤ρ_m(n)−3^m σ_B(C_m(n))≤2n²/B`, `B>n`.

In forma relativa si ha anche

`σ_B(C_m(n))≥(1−n/B) μ(C_m(n))`.

Questa deduzione usa davvero positività e conteggio degli interi; non è un'inferenza dalla sola integrabilità Haar.

### Il termine di errore è sommabile: un Green bound aritmetico

Se n è senza ritorni, tutte le parole ammissibili, anche su profondità diverse, hanno sorgenti fisiche distinte. Una sorgente u può raggiungere n a un unico tempo: due arrivi darebbero un ritorno positivo di n. Inoltre A_w≤n/u. Sommando sulle sorgenti, con Tonelli,

`Σ_(m≥0)ρ*_m(n)=Σ_(u∈B_n^odd) A(u→n)²≤n²Σ_(u≥1)u⁻²≤2n²`.

L'ultima costante ammette il bound elementare della serie dei reciproci quadrati. Il cap infinito è quindi pagato anche dopo la somma su tutte le profondità:

`Σ_(m≥0)[ρ_m(n)−3^mσ_B(C_m(n))]≤2n²/B`.

Per ogni K≥1, l'errore fra i due Cesàro fino a K è al più **2n²/(BK)**. Con B=2n e g(n)≥cε·n, il relativo errore dei Cesàro è Oε(1/K), uniforme nei target di questa classe. Resta da controllare il rilassamento della stessa misura capped; non è stato ottenuto qui.

Un'estensione include i target periodici. Il budget `WeightedVisits` del progetto dà, per ogni sorgente u, Σ_(w:u→n)A_w≤n(3n+1)/u, anche contando i ritorni. Moltiplicando per A_w≤n/u e sommando su u si ottiene

`Σ_(m≥0)ρ*_m(n)≤2n²(3n+1)`.

Pertanto la differenza delle densità di cilindro tende ordinariamente a zero a ogni target positivo dispari, anche periodico. La traccia Cesàro g(n) è la stessa della misura σ_B per ogni B>n. Non si identifica con questo un rappresentante puntuale arbitrario della densità σ_B.

In forma alternativa, per n senza ritorni A_max(m,n)→0: A≥a>0 limita u≤n/a e vi sono solo finitissime sorgenti, ciascuna con un solo tempo d'arrivo. Questo isola nuovamente l'ostacolo a un rate uniforme: quantificare i tempi d'arrivo dalle sorgenti piccole.

### Il seed unità si confronta col livello successivo

La prima densità stazionaria è `ρ₁=1_(x≡1 mod3)+2·1_(x≡2 mod3)`. Quindi `1_U≤ρ₁≤2·1_U`. La positività dell'operatore accelerato S₁ e l'identità ρ_(m+1)=S₁^mρ₁ danno

`ρ_m^U≤ρ_(m+1)≤2ρ_m^U`.

Il reciproco della traccia sotto Doob rimane esattamente ρ_m^U(n)/g(n), ma un lower sul livello pieno successivo implica un lower Doob con perdita due. Non si devono aggiungere indebitamente le foglie a traccia zero.

## 5. Cosa cambia nel criterio locale di T07

Se il nuovo input weak L² della fonte 146 viene accettato, layer cake dà, per ogni insieme misurabile C,

`∫_C E dλ≤2√(K λ(C))`,

per una costante K della coda. In particolare

`ρ_m(n)≤2√K·3^(m/2)`.

Quindi la condizione locale non dimostrata

`ρ_(m(n))(n)≥θg(n)`, `m(n)≤2log₃n−h(n)+O(1)`, `h(n)→∞`,

è sufficiente a g(n)=o(n). Rispetto al solo bound energetico lineare, si elimina la perdita aggiuntiva in log m. Alla scala esattamente 2log₃n+O(1), senza margine divergente, i contro-modelli critici restano compatibili con g(n) lineare.

Il cap aritmetico del §4 offre una seconda forma della stessa scala. Per B>n, la comparazione relativa e il bound L³ della fonte danno

`ρ_m(n)≤(1−n/B)⁻¹ ||σ_B||₃·3^(m/3)`.

Scegliendo B=2n e usando ||σ_B||₃³≤CB si ottiene `ρ_m(n)≤C′n^(1/3)3^(m/3)`. Anche qui la soglia resta 2log₃n; la stabilizzazione locale non è stata provata.

Il criterio Doob a blocchi di T07/T09 può usare una scala più ampia, prossima a log_(3/2)n. La weak L² non sostituisce la sua ipotesi di rilassamento.

## 6. Perché un nuovo teorema di ergodicità debole non dà il lower Doob

La fonte [rStation 127](https://rstation.ai/problems/collatz/papers/127), del 9 novembre, dichiara Cesàro uniforme nel root per osservabili continui di un kernel inverso con cap fisso sei, e risultati per regole determinate da finitissimi digit. Quel kernel è diverso dal Doob reale e i suoi alberi hanno densità zero nel problema T08.

Esiste anche un ostacolo alla mera approssimazione dell'osservabile. La vera traccia g è illimitata in ogni classe ternaria di unità. Se una funzione continua nonnegativa f su U soddisfa f(n)≤1/g(n) per tutti i positivi unità, allora **f è identicamente zero**: un punto con f>0 avrebbe un cilindro con f≥c>0, ma lì esistono interi con g arbitrariamente grande.

Non esiste quindi un minorante continuo positivo di 1/g. La convergenza debole sui continui non fornisce il lower richiesto per questo osservabile; l'estensione 1/E è semicontinua superiormente e Portmanteau dà il verso superiore. Non si può usare il nuovo risultato sul kernel capped come rate per il kernel Doob.

## 7. Controlli e stato della verifica

Il programma indipendente `t10/check_resolvent.py` costruisce le leggi stazionarie con un risolutore razionale in avanti sul ciclo di raddoppio, senza importare i programmi T03/T07. Il protocollo è fissato prima del calcolo: livelli k=0,…,5. **PASS**: 364 identità puntuali della risolvente, normalizzazioni, correlazione ed energia; otto coppie di spike. Normale e Python -O sono identici, SHA-256 `16a31bdd22ae5ef3c67d4a027729c1b9c09f191e4a07cb0b96b76b9de41bd442`.

Il controllo indipendente `t10/check_delayed_support.py` enumera tutte le composizioni al totale ammissibile, senza cap dell'alfabeto, fino a lunghezza otto. **PASS**: 192 versioni esatte della (14), 293 prefissi fisici e 290 fibre complete; massimo rapporto fra i due lati 1/8. Output normale e ottimizzato identici, SHA-256 `16c27fc3d80dbb55b674adb83631cf6b69c4b0f076dc75f1150f0e54fa304875`. Non certifica l'upper esponenziale uniforme.

Il controllo del nuovo ponte aritmetico è registrato separatamente in `t10/positive_atom_protocol.json`, con profondità del tilt ≤6, target dispari 1,…,129 e parole finite di lunghezza ≤5, totale ≤12. PASS: 455 atomi esatti del tilt, 5.422 prefissi positivi, 3.250 fibre a totale fissato e 325 confronti con la somma troncata. Output normale e ottimizzato identici; SHA-256 `0dabdce06efb77d25acd21ff37994431c9bfe68b189c588b6b57c8926ecf95f4`. Il controllo non sostituisce le prove uniformi dei §§3–4.

**Decisione:** il nuovo input analitico utile è la regolarizzazione per massimo moltiplicatore, ora collegata a un controllo di errore aritmetico uniforme nella profondità. Restano da controllare il tempo di stabilizzazione ai target crescenti e la vera massa relativa. Nessuna prova di convergenza è stata ottenuta.
