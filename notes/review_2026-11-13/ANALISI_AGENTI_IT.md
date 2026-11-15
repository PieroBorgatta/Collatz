# Dieci analisi del progetto Collatz

13 novembre 2026. Dieci agenti distinti sono stati avviati a gruppi, con un massimo di tre agenti operativi oltre al coordinatore. Gli incarichi coprono la libreria Lean, la storia del progetto, gli script e le note di ricerca, il pacchetto analitico separato, la letteratura e una revisione avversa della sintesi. Le letture sono mirate per ramo; non si rivendica una revisione matematica riga per riga di ogni sorgente o un controllo umano indipendente.

| Agente | Ambito | Contributo principale | Relazione |
|---|---|---|---|
| `01_web_frontiera` | Letteratura aggiornata | Fonti nuove da ottobre a novembre, verifica dei limiti e distinzione dello stato delle prove | [Analisi 1](AGENTE_01_IT.md), [fonti annotate](FONTI_WEB_IT.md) |
| `02_audit_formale` | Compilazione, assiomi e ipotesi aperte | Build integrata riuscita, 37 radici sottoposte ad audit stretto, confine della verifica esplicito | [Analisi 2](AGENTE_02_IT.md) |
| `03_storia_gap` | Storia scientifica e decisioni | Ricostruzione delle fasi e dei metodi chiusi; separazione globale, torre e densità | [Analisi 3](AGENTE_03_IT.md) |
| `04_spettrale` | Operatori e ponte infinito | Due inferenze da correggere nelle note storiche; percorso per kernel troncati | [Analisi 4](AGENTE_04_IT.md) |
| `05_ritorni_sezione` | Copertura, macro e primi ritorni | Arbitrariamente molti primi ritorni crescenti; certificati parametrici e interfacce d'uscita | [Analisi 5](AGENTE_05_IT.md) |
| `06_torre_aritmetica` | Torre, riporti e vincoli diofantei | Fattori coprimi, limiti dei filtri, controllo critico della pista S-unità | [Analisi 6](AGENTE_06_IT.md) |
| `07_densita_analitica` | Occupazione e predecessori | Budget normalizzato per target differenti e formulazione aggregata dei bacini | [Analisi 7](AGENTE_07_IT.md) |
| `08_trasporto_variabile` | Trasformazioni di parole inverse | Revisione H.2, ostacolo modulo 3 e costo combinato del flusso relativo | [Analisi 8](AGENTE_08_IT.md) |
| `09_cicli_diofanteo` | Cicli, minimi e letteratura specifica | Interfaccia Hercher, divisibilità invariante per rotazione e vincolo intero del prodotto | [Analisi 9](AGENTE_09_IT.md) |
| `10_revisione_avversa` | Quantificatori, circolarità e priorità | Controllo incrociato delle nuove deduzioni e dei criteri per proseguire | [Analisi 10](AGENTE_10_IT.md) |

Le prime tre relazioni sono sintesi dei contributi restituiti dagli agenti. Le relazioni 4–10 conservano il testo specialistico prodotto, con adattamenti ai collegamenti del dossier. La relazione 10 è deliberatamente una revisione dei risultati degli altri incarichi, non una seconda ricerca indipendente dell'intero progetto.

Il [rapporto principale](REPORT_IT.md) ordina conclusioni e priorità. I [log](verification/) distinguono le verifiche eseguite oggi dalle verifiche storiche o dichiarate dalle fonti esterne. Il [replay aritmetico](review_checks.py) conserva piccoli controlli riproducibili delle nuove osservazioni; nessuna di esse viene presentata come nuova dichiarazione Lean.
