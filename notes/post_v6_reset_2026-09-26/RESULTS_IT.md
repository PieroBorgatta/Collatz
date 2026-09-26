# Consolidamento, revisione critica e proposta sui bacini inversi

26 settembre 2026. Piero Borgatta con assistenza Codex.

**Esito scientifico:** la campagna di filtri sulla torre viene chiusa.
Il risultato di ottimalità dei prefissi è stato tradotto in una prova
aritmetica Lean. La nuova candidata è un confronto relativo fra bacini
inversi di target vicini con lo stesso successore. Il suo lemma centrale
è aperto: non abbiamo ottenuto una dimostrazione di Collatz né evidenza
che la soluzione sia prossima.

## Cosa leggere

- [Nota per un revisore umano](EXTERNAL_REVIEW_BRIEF_IT.md): breve quadro
  dei risultati, delle ipotesi e dei quesiti. Preparata, non inviata.
- [Mappa critica](CRITICAL_MAP_IT.md): bilancio dei principali rami del
  progetto e distinzione fra copertura universale, torre speciale e densità.
- [Letteratura aggiornata](LITERATURE_IT.md): fonti primarie, versioni e
  limiti, inclusi lavori del 2026 e formalizzazioni in valutazione.
- [Nuova direzione](NEW_DIRECTION_IT.md): enunciato aperto, prova della sua
  conseguenza condizionale, ostacoli e risultato dell'esperimento fissato.

## Consolidamento matematico

`PrefixOptimality.lean` usa la vera mappa shortcut T e il polinomio
f_v(x)=x+2^(v+2)x². Per Q>0, H≤M≤K, dimostra che il massimo di
`J_(f_v(x))(K)−2J_x(H)` fra gli x>0 congrui a Q modulo 2^M è

\[
J_{f_v(Q)}(M)+(K-M)-2J_Q(H)=K-2J_Q(H)-Z_{f_v(Q)}(M).
\]

Un sollevamento aritmetico costruisce un vero intero positivo che raggiunge
il massimo. Ne segue il criterio necessario e sufficiente sugli zeri già
osservati e un controtestimone per ogni soglia insufficiente. Non sono
formalizzati qui molteplicità binomiali, posizione dell'R-esimo zero,
conservazione dei bit alti o vincoli aggiuntivi sugli antenati.

`SiblingBasins.lean` sviluppa un risultato distinto per una funzione
deterministica arbitraria: su una spina orbitale iniettiva, i predecessori
dei rami laterali selezionati hanno bacini disgiunti. Su qualunque insieme
finito di sorgenti, la somma dei loro pesi naturali non supera il peso
totale delle sorgenti. L'appartenenza a un bacino ammette tempi di visita
illimitati ed è definita in modo non computabile: il teorema non fornisce
un algoritmo generale per decidere tali appartenenze. Il modulo costruisce poi il fratello Syracuse
canonico, maggiore di n ma non oltre 16n+5 e non divisibile per 3 quando
n non lo è. Non formalizza la densità asintotica, l'input analitico esterno
o l'intera conversione al conteggio ordinario: quei passaggi sono distinti
nella nota teorica.

## Cosa cambia nella ricerca

L'idea è chiedere un confronto relativo

\[
d_*(B(h(n)))\ge\frac{c}{1+\log n}\,d_*(B(n)),\qquad c>0,
\]

per il fratello specificato e quando entrambi i target non ritornano a sé
stessi. Questa disuguaglianza **non è dimostrata**. Se valesse, insieme alla
positività del bacino iniziale, un'orbita illimitata obbligherebbe infiniti
bacini disgiunti ad avere massa totale divergente. Il budget la escluderebbe.
La prova condizionale è stata controllata da un secondo agente; non è
peer review umana e non elimina i cicli positivi non banali.

Il censimento previsto dal [protocollo](PROTOCOL_IT.md) esamina 340 coppie
di target a quattro soglie, fino a 1.048.576 inizi. Mostra asimmetrie forti:
per n=593 e h(n)=9493, all'ultima soglia i conteggi sono 345889 e 90.
Nessuna costante universale è stata scelta dai dati. I numeri non provano
né falsificano direttamente il confronto di densità asintotiche.

La rassegna non ha identificato una prova verificata di Collatz. Distingue
risultati pubblicati, preprint, prove dichiarate e formalizzazioni con
ipotesi aperte. Comprende anche un'obiezione esplicita alla conclusione di
unicità della misura non atomica in Chang C.48, preservando l'ipotesi di
gap dell'enunciato originale. È una critica di quel passaggio, non un
giudizio globale su tutti i risultati dell'autore.

## Verifica e riproduzione

La build integrata è riuscita: **3378 job, exit 0**, senza errori o avvisi
nel log. I due audit rigorosi sono passati su **10 + 14 dichiarazioni
principali**, con sole dipendenze da `propext`, `Classical.choice` e
`Quot.sound`. I sette test Python passano anche con `-O`; il replay completo
del censimento, eseguito con `-O`, riproduce tutti i conteggi interi salvati.
Sono passati anche i controlli aritmetici finiti delle note e i checksum
dei sei PDF pubblicati.

Le verifiche finali e gli hash sono registrati in `verification_manifest.json`.
I log separano build dei moduli, build integrata e audit delle dipendenze.
Il toolchain rimane Lean 4.29.1 / Mathlib 4.29.1. Un ripristino locale della
dipendenza Mathlib ha riutilizzato la cache compilata della revisione
`5e932f97dd25535344f80f9dd8da3aab83df0fe6`; non è un rebuild freddo di Mathlib
né una verifica con kernel indipendente. La portabilità a un toolchain
recente resta una verifica distinta, già segnalata in `lean/STATUS.md`.

Dalla directory `lean`:

```sh
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake build
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_reset_2026-09-26/PrefixDependencyAudit.lean
DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean ../notes/post_v6_reset_2026-09-26/SiblingDependencyAudit.lean
python3 ../notes/post_v6_reset_2026-09-26/paper_checks.py
python3 ../notes/post_v6_reset_2026-09-26/test_basin_probe.py
python3 ../notes/post_v6_reset_2026-09-26/basin_probe.py --output /tmp/basin-results.json
python3 ../notes/post_v6_reset_2026-09-26/verify_basin_results.py ../notes/post_v6_reset_2026-09-26/basin_results.json /tmp/basin-results.json
```

La variabile DEVELOPER_DIR serve a questa macchina macOS per usare Git
dei Command Line Tools; non è richiesta in generale, né in CI Linux.
I sette test includono un replay indipendente della mappa ordinaria, la
contabilità degli inizi pari, la disgiunzione sorgente per sorgente e il
rifiuto di esplorazioni incomplete e di dati alterati anche con Python
ottimizzato (`-O`). Il comparatore richiede uguaglianza
esatta degli interi e ammette soltanto arrotondamenti dei logaritmi di
presentazione. Il workflow Lean è stato esteso ai due audit e al replay;
questa fase non rivendica un nuovo run CI remoto.

I PDF pubblicati v1–v6 hanno superato il controllo dei checksum. Nessun
nuovo livello della torre è stato calcolato; gli archivi precedenti non
sono stati sovrascritti. Le revisioni fra agenti sono controlli interni,
non sostituiscono la revisione specialistica richiesta.

## Prossimo passo giustificato dai risultati

La domanda utile è ora se si possa trasferire una frazione controllata
della massa fra **parole inverse diverse**, mantenendo integrità, altezza
e molteplicità. Il trasferimento della stessa parola è impossibile già
modulo 3. Un altro censimento più grande non risolverebbe questo problema.
Prima di investire nella nuova pista serve un lemma quantitativo su quel
trasferimento o un'obiezione che lo escluda. La nota è pronta per questa
valutazione esterna; nessun contatto è stato effettuato.
