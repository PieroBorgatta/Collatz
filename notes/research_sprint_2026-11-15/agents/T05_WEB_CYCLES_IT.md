# T05 Fonti sui cicli e vincoli del minimo

15 novembre 2026. Primo lavoro alle **20:09:27 UTC**. Nuovo modulo locale congelato dopo la build delle tre dichiarazioni; nessuna dipendenza o versione degli strumenti modificata. Le fonti esterne sono state lette e fissate, non ricompilate localmente.

## Risultato integrabile subito

Il modulo [CycleMinimumProduct.lean](../../../lean/CollatzShadowing/CycleMinimumProduct.lean) completa il candidato già registrato nella revisione S09 del 13 novembre. Contiene tre teoremi, tutti compilati:

1. Una parola esatta w da n, i cui k stati prima dell'endpoint sono almeno M, soddisfa

   `2^A M^k eval(w,n) ≤ (3M+1)^k n`.

2. Se il percorso è chiuso e n>0, si cancella n e si ottiene

   `2^A M^k ≤ (3M+1)^k`.

3. Se anche M>0, passando ai logaritmi si ottiene il ponte nelle coordinate locali

   `A log 2 − k log 3 ≤ k/(3M)`.

Qui A è il totale delle valutazioni e k la lunghezza Syracuse. Il minimo M resta un'ipotesi esplicita su tutti gli stati. Non sono importati un cutoff computazionale, un teorema sui cicli fino a 101 minimi o la misura di Rhin. Questi sono vincoli classici, non nuove esclusioni di cicli.

La prova del primo enunciato moltiplica `2^a M S(x) ≤ (3M+1)x`, valida perché `M≤x`; i fattori intermedi si cancellano. Per il terzo, si prende il logaritmo del secondo e si usa `log(1+1/(3M))≤1/(3M)`. Il caso w vuoto è incluso e dà le identità 1≤1 e 0≤0.

La build finale `lake build CollatzShadowing.CycleMinimumProduct` è terminata con exit 0, 3297 job, 120 secondi per il nuovo target. La [ricevuta](../../../research/research_sprint_2026-11-15/t05/cycle_minimum_receipt.json) conserva hash del sorgente e i tentativi precedenti. L'audit integrato delle dipendenze è affidato al coordinatore; questa ricevuta non è un replay con kernel indipendente. A M=1 il primo vincolo coincide con il budget `2^A endpoint≤4^k source` usato da T02: non va contato come una scoperta analitica distinta.

## Fonte Alick: almeno 102 minimi, con due input dichiarati

Fonte primaria: [repository di Justin Alick](https://github.com/justinalick/collatz-m-cycles-101-lean), fissato al commit **d18959450f9acb5c0fa8c54310bc799a636d7db4**, datato **28 settembre 2026, 08:09:51 UTC**. È una novità per questa revisione del progetto, non un annuncio successivo al 13 novembre. Il repository dichiara di escludere i cicli con al più 101 minimi locali; non è ancora referato e il manoscritto descrittivo è in preparazione. Il codice usa Lean 4.35.0-rc3, diverso dal nostro 4.29.1.

Ho letto direttamente `MCycle101.lean`, le definizioni, l'audit, il controllo del teorema e parte dei moduli di finestre e catene. Il teorema finale ha esattamente due parametri matematici esterni:

- ogni positivo n≤2^71 raggiunge 1;
- `RhinBound`, una minorazione trascendente del gap logaritmico per i cicli non banali.

La conclusione riguarda la shortcut T e un tempo di ritorno p qualunque. Prendendo il periodo minimo si ottiene il numero di minimi del ciclo; ripetere il periodo moltiplica il conteggio. La definizione `numLocalMin` conta gli stati dispari il cui predecessore ciclico è pari.

Nelle nostre parole Syracuse, ogni esponente a≥2 introduce un segmento pari prima del successivo dispari. Il numero di minimi shortcut coincide quindi con il numero di entrate a≥2 del periodo Syracuse. Questa corrispondenza è ricostruita su carta qui, **non formalizzata nel nuovo modulo**. Il numero di minimi non coincide con k, benché sia al più k. Un candidato ripetuto deve essere ricondotto al periodo primitivo prima di interpretarne i conteggi; non si sostituisce questa operazione con `gcd(A,k)=1`.

Il meccanismo da studiare è distinto dai nostri sieve di rotazione: `TwoRiseCheck.lean` certifica vincoli su due run crescenti consecutive; `MCycleChain.lean` trasferisce quei vincoli lungo i minimi; `MCycleWalk.lean` enumera le forme rimaste sotto il tetto di Rhin con un cammino di Farey. Le prove di soundness collegano i controlli booleani alle vere traiettorie. Il workflow pubblicato prevede build, audit e verifica del teorema. **Non ho eseguito quel workflow, controllato tutti i certificati o ricostruito il progetto esterno**: l'integrazione locale non assume perciò la conclusione 102.

La selezione di 19 file è in `research/research_sprint_2026-11-15/t05/sources/alick/`, con licenza Apache-2.0, URL immutabili e SHA-256 nel manifest. L'audit esterno esamina le dichiarazioni pubbliche del namespace Collatz e le loro dipendenze; il nostro esame del testo dell'audit non ne sostituisce l'esecuzione.

## Controllo bibliografico di Hercher e Rhin

La pagina primaria del [Journal of Integer Sequences](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/hercher5.html) collega l'articolo di Hercher del 2023 e il [corrigendum del 14 giugno 2026](https://cs.uwaterloo.ca/journals/JIS/VOL26/Hercher/corrigendum.pdf). La correzione riguarda un passaggio della dimostrazione del Teorema 21, non la trasformazione dei minimi shortcut in numero di dispari. Nel codice Alick la parte di finestre documenta separatamente una versione senza argomento sui vertici e un bound a due elementi: non ho trattato il vecchio passaggio errato come un input valido.

Ho acquisito temporaneamente il [PDF primario di Simons–de Weger, Acta Arithmetica 117 (2005), 51–70](https://deweger.net/papers/%5B35%5DSidW-3n%2B1-ActaArith%5B2005%5D.pdf) e ispezionato visivamente la pagina stampata **61**. Il Lemma 12 contiene la stessa formula usata nel parametro `RhinBound`:

`Λ > exp(−13.3(0.46057+log K))`, con `Λ=(K+L)log 2−K log 3`.

Nel nostro linguaggio `K=k` e `K+L=A`. La corrispondenza della formula è verificata; il teorema trascendente non è stato formalizzato o aggiunto come assioma. Il PDF è rimasto in `/tmp`; la ricevuta conserva l'URL e SHA-256 `a088347a8344fb74512b7eb5e324a0bfa0f5cd71c04b26a7d6f344b720fc0248`.

## Bound per run: prova elementare su carta

Un ulteriore ponte utile alle tecniche di Hercher si ricostruisce senza input esterni. Per il blocco

`b=[1]^r ++ [a]`,

la costante affine non dipende dall'ultimo a e soddisfa esattamente

`C(b)+2^(r+1)=3^(r+1)`.

La prova è un'induzione: per r=0 la costante è 1. Anteponendo 1 si passa da C_r a `3^(r+1)+2C_r`; aggiungere `2^(r+2)` dà `3^(r+1)+2(C_r+2^(r+1))=3^(r+2)`. Non si assume che il blocco appartenga a un ciclo.

Se il blocco è effettivo da x>0 a z, la sua inflation è perciò

`2^(r+a) z/(3^(r+1)x) = 1+[1−(2/3)^(r+1)]/x < 1+1/x`.

Un ciclo positivo non vuoto ha almeno un esponente a≥2, perché una parola tutta di esponenti 1 non è contracting. Ruotandolo opportunamente, si decompone in m blocchi di questo tipo, ognuno terminante in a≥2. I loro inizi sono i minimi shortcut. Se sono tutti almeno M>0, moltiplicando e cancellando gli endpoint intermedi:

`2^A M^m ≤ 3^k(M+1)^m`,

quindi

`A log 2−k log 3 ≤ m/M`.

Questo bound è utile soprattutto per run lunghe; non domina sempre `k/(3M)` quando m è vicino a k. È la versione per blocchi del controllo classico delle somme reciproche delle run usato da Hercher e Simons–de Weger. La prova sopra è su carta; non è una quarta dichiarazione del modulo compilato e non esclude tutti i valori di m.

La prosecuzione sensata sul canale cicli è collegare rigorosamente il conteggio delle run alle coordinate del ciclo, poi selezionare un input trascendente e certificati con provenienza verificata. Aumentare soltanto il numero di rotazioni dello stesso sieve non aggiunge informazione.

## Due altre fonti e il loro confine rispetto a H

[Nashida, fixed-barrier r8](https://github.com/harappa/collatz-fixed-barrier-power-saving), commit **976fffb160744c56f1f26912f7bd23d195fe02d2** del **27 settembre 2026**, espone un teorema senza ulteriori parametri matematici: il numero di inizi≤X la cui intera orbita ordinaria resta strettamente sopra M è al più `K M^(−c') X`, uniformemente in X, con c' esplicito circa 3.5·10^−6 e K ineffettivo. Il tempo zero è incluso. Ho letto gli enunciati e parte dell'assemblaggio; nessun replay locale della chiusura esterna. La selezione di 12 file conserva licenza, avvisi e hash.

Questa uniformità nel cutoff è utile per errori assoluti e tightness, ma non confronta la quota reale di due bacini. Il bacino di un target può inoltre contenere sorgenti che passano prima sotto M: l'appartenenza al bacino non autorizza da sola a usare il bound delle orbite interamente sopra M. Non fornisce quindi η né una prova di H.

[Vasilyev, arXiv:2611.10311v1](https://arxiv.org/abs/2611.10311), presentato il **6 novembre 2026**, è più recente. La lettura qui è limitata all'abstract e alla disponibilità dei materiali. Studia varianti e famiglie con scelta della mappa; i drift iniziali del modello assumono indipendenza delle valutazioni. Non trasformiamo quel modello in una legge della singola orbita Collatz. Il lavoro suggerisce di verificare attentamente qualsiasi passaggio da mappe singole a switching arbitrario; nessun suo teorema è stato integrato localmente.

## Decisione di integrazione

Integrare i tre lemmi locali del minimo, con l'ambito dichiarato. Conservare le nuove fonti come materiale fissato per un audit successivo e il bound per run come prova su carta. Non dichiarare ottenuto il limite 102 nel progetto, né una nuova esclusione di cicli o un confronto relativo di densità. H e il problema dei cicli rimangono obblighi separati.
