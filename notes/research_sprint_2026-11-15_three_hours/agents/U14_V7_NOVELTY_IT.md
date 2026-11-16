# U14 — Valutazione critica della prossima versione

Valutazione indipendente preparata durante la sessione del 15–16 novembre 2026, base `203cbb8`. Non è un manoscritto, una revisione matematica completa o un’autorizzazione al deposito. Non sono stati creati PDF, modificati sorgenti Lean, avviati calcoli, contattati ricercatori o eseguite operazioni Git. I risultati eventualmente aggiunti dopo questa lettura richiederanno un aggiornamento circoscritto del giudizio.

## Decisione

**Preparerei ora una v7 tecnica breve; non la depositerei subito.** Il materiale post-v6 giustifica una versione coerente senza attendere una prova di Collatz. Prima del rilascio serve però trasformare gli appunti in un testo autonomo, correggere le attribuzioni alla luce dei precedenti appena trovati e fissare manoscritto e supplemento allo stesso commit verificato. Un’altra lunga sessione indiscriminata di ideazione prima di questa selezione rischia soprattutto nuove riscritture dell’obbligo aperto.

La ricerca dovrebbe poi continuare su un solo attacco misurabile: **nonconcentrazione fisica del kernel inverso a due copie**, eventualmente attraverso certificati di antenati che entrano da rami distinti. È la proposta più utile per organizzare il prossimo lavoro, non quella per cui sia dimostrata una maggiore probabilità di risolvere Collatz. Il lower richiesto rimane sostanziale; nel quadro con tightness dei root pesanti può essere equivalente alla mancanza di divergenza. Non siamo a un ultimo passaggio tecnico di una prova già acquisita.

## Tre nuclei sufficienti per una v7

| Nucleo | Valore concreto | Confine da scrivere nell’enunciato |
|---|---|---|
| Budget finiti e trasporto effettivo | Prova locale esplicita del budget reciproco, clock di primo arrivo, altezza, occupazione quadratica e finitezza dei cataloghi. La verifica Lean rende riutilizzabili questi ingredienti. | Segmenti positivi iniettivi o primi arrivi; gli altri domini vanno distinti. Il bound di cardinalità non è un cutoff effettivo sui tempi. Le formulazioni generali hanno precedenti. |
| Ostruzioni al recoding | Le code a slope limitata danno un bound polilogaritmico; le code con pochi non-1 o pochi pezzi di un dizionario periodico fissato danno X^o(1). Sono esclusioni di intere relazioni, più informative di un algoritmo che non ha trovato massa. | Target fissati, profilo uguale e prefisso comune. Nella seconda estensione serve il primo arrivo originale. Nessun no-go per ogni recoding, dizionari crescenti o prefissi differenti. |
| Ponte analitico e obbligo aperto | L’identità cap/Doob identifica esattamente quale massa il troncamento conserva; il difetto di collisione individua un lower fisico preciso. | Risultati su carta con input esterni dichiarati. Nessun lower provato, nessuna esclusione generale dei cicli e nessun teorema Collatz. Questa parte può stare in una breve sezione finale o appendice. |

Darei il maggior rilievo al secondo nucleo e userei il primo come infrastruttura verificata. Il corollario bounded-slope ha il vantaggio editoriale di non richiedere Evertse: la finitezza del catalogo e il residuo non nullo spiegano direttamente l’esclusione. Il suo K è esistenziale, non un numero ottenuto dal bound sulla cardinalità. Il risultato del dizionario periodico conserva invece l’input S-unit e i suoi limiti di effettività.

## Che cosa è nuovo, e in quale senso

La risposta difendibile a «nessuno l’ha mai tentato?» è **non lo sappiamo**. La ricerca ha già trovato precedenti per alcune conclusioni inizialmente candidate come nuove. Ciò è un risultato del controllo, non una ragione per rinominarle come innovazioni del progetto.

- Il budget uniforme e il prodotto affine erano già presenti nelle fonti segnalate da T01/T03. La costante esplicita e la prova indipendente nel toolchain locale sono contributi di formalizzazione, non un primato per la summabilità.
- Il [paper9/v1, §8.1, Proposizione11](https://rstation.ai/problems/collatz/papers/9/v1) contiene già il Green tilt intero e la finitezza con ritorni. Il bound locale 2n² non migliora la costante π²n²/8 della fonte. Anche il massimo dei profili e il clock critico hanno precedenti identificati nelle note U01/U02.
- I no-go di U05/U11 e l’identità capped/Doob sono corollari ricostruiti qui con revisione indipendente. La loro esatta formulazione non è stata localizzata nei materiali letti; **questo non certifica priorità globale**. Il primo-split, il kernel quadratico e la trasformazione di Doob sono strumenti standard.

La combinatoria degli alberi inversi è antica. La [pagina primaria di Wirsching1996](https://www.sciencedirect.com/science/article/pii/0012365X9400243C) descrive rappresentazioni dei predecessori con sequenze finite e l’uso di «small sequences»; la [bibliografia di Lagarias](https://arxiv.org/abs/math/0309224) è il riferimento di partenza per quel confronto. Qui sono stati controllati l’abstract ufficiale e i riferimenti bibliografici, non tutto il libro o il paper di Wirsching. Non bastano quindi per stabilire se uno specifico corollario di recoding fosse già implicito in quelle prove. Prima di una rivendicazione forte serve tale confronto, non un’altra ricerca per parole chiave.

## Che cosa escluderei dal corpo principale

Non presenterei il numero di agenti, moduli, enunciati o controlli come un numero di scoperte. Eviterei una cronaca di tutti gli esperimenti, un catalogo di nuove ipotesi sufficienti e l’importazione di tutte le analisi recenti sui momenti capped. Una tabella di casi avversi basta a mostrare la distinzione fra codici e sorgenti reali; i replay completi restano nel repository.

La nota sui ritorni parametrizzati e il singolo clock di un ramo possono essere appendici o restare nel repository: non sono necessari alla tesi sul recoding. Le leggi di Haar, il routing modulare e i dati finiti non vanno elevati a lower relativo sugli interi. Le percentuali nonsmooth di U10 non giustificano una strategia di successo, perché anche il controllo smooth escluso asintoticamente mostra trasferimenti finiti consistenti.

Il manoscritto148 pubblicato il15 novembre è un confronto utile sui minimi inversi. La lettura U11 non è un replay dei suoi certificati e il suo orizzonte r≤s non è quello di tutti i rivali. Non lo inserirei come risultato acquisito del progetto né come indizio di soluzione prossima.

## Prima di un deposito, in concreto

1. Scegliere due o tre enunciati centrali e scriverne prove autonome, con fonti accanto agli ingredienti. Le note degli agenti sono materiale preparatorio, non il manoscritto da pubblicare.
2. Aggiornare l’outline del13 novembre: la distinzione F/C/E/H va conservata, ma alcuni ingredienti allora su carta sono ora formalizzati; le nuove attribuzioni riducono il perimetro dei claim di novità.
3. Associare ogni enunciato del manoscritto a fonte, dominio, commit e verifica finale. Una build pinned incrementale e un audit transitivo sono prove del loro ambito, non una ricompilazione indipendente di tutti i pacchetti analitici esterni.
4. Fare un controllo finale tra testo e supplemento, inclusi gli errori storici corretti su campionamento Haar, Cauchy e valore della codifica accelerata. La v6 pubblicata rimane immutata.

Questi sono lavori editoriali e di verifica ordinari, non una richiesta di permesso aggiuntiva. L’utente ha autorizzato commit e push, non un deposito v7; qui non si esegue alcuna pubblicazione. La preparazione della v7 e un successivo attacco mirato al lower possono procedere come due attività distinte. Non serve comprare GPU per trasformare questi controlli finiti in una prova asintotica.

## Formula breve proposta per il riepilogo in chat

«Preparerei una v7 breve di consolidamento, ma non la pubblicherei oggi come svolta verso Collatz. Le esclusioni di alcune classi di trasporto sono solide; diversi budget avevano già precedenti. La pista da continuare è la nonconcentrazione di due processi inversi, cercando certificati aritmetici di rami distinti. Non posso affermare che nessuno l’abbia tentata, e il lower decisivo resta aperto.»
