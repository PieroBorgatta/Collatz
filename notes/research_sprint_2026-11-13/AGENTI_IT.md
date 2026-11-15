# Quindici incarichi e confronto fra agenti

Sessione del 13 novembre 2026. Quindici agenti distinti hanno lavorato in gruppi compatibili con la capacità della piattaforma: al massimo tre operativi oltre al coordinatore. Non sono state avviate quindici istanze simultanee. Gli incarichi includevano scambi diretti di ipotesi, controesempi, risultati e controlli; i rapporti registrano i confronti pertinenti.

| Agente | Compito | Confronti principali | Relazione |
|---|---|---|---|
| S01 `s01_web_meccanismi` | Estrarre meccanismi finiti dalle nuove fonti | S02, S03, S04 | [S01](agents/S01_WEB_IT.md) |
| S02 `s02_budget_formale` | Budget condivisi e pool non ricorrenti | S01, S03, S04 | [S02](agents/S02_BUDGET_IT.md) |
| S03 `s03_blocchi_ritorno` | Formalizzare arbitrariamente molti primi ritorni crescenti | S01, S02, S05 | [S03](agents/S03_RETURN_IT.md) |
| S04 `s04_joint_atoms` | Dizionario esatto di atomi, parole e sorgenti | S01, S02, S05, S06 | [S04](agents/S04_JOINT_IT.md) |
| S05 `s05_fan_allocation` | Certificati finiti di allocazione a soglia | S04, S06 | [S05](agents/S05_CAPACITY_IT.md) |
| S06 `s06_word_surgery` | Trasformazioni di più esponenti e carico delle immagini | S04, S05, S07, S08 | [S06](agents/S06_SURGERY_IT.md) |
| S07 `s07_macro_exit` | Raccordi fra macro e code dei reset | S06, S08, S09, S10 | [S07](agents/S07_MACRO_IT.md) |
| S08 `s08_sibling_pool` | Collegare i pool non ricorrenti ai fratelli canonici | S06, S07 | [S08](agents/S08_POOL_IT.md) |
| S09 `s09_cycle_formal` | Rotazioni e invarianti dei vincoli ciclici | S07, S10, S11 | [S09](agents/S09_CYCLE_IT.md) |
| S10 `s10_sparse_potential` | Sparsezza finita e limite del prodotto affine | S07, S09, S11, S12 | [S10](agents/S10_SPARSE_IT.md) |
| S11 `s11_kernel_repair` | Correggere le note analitiche e provare un caso di convergenza del clock | S10, S12, S13 | [S11](agents/S11_KERNEL_IT.md) |
| S12 `s12_adversarial_sources` | Revisione avversa delle deduzioni e delle fonti | S10, S11, S13, S14 | [S12](agents/S12_ADVERSARIAL_IT.md) |
| S13 `s13_independent_checks` | Replay con algoritmi indipendenti e certificati di matching | S11, S12, S14, S15 | [S13](agents/S13_REPLAY_IT.md) |
| S14 `s14_formal_review` | Revisione semantica e audit di tutte le nuove radici | S12, S13, S15 | [S14](agents/S14_FORMAL_IT.md) |
| S15 `s15_v7_decision` | Valutare la v7 rispetto a risultati, attribuzioni e verifica | S13, S14 | [S15](agents/S15_V7_IT.md) |

Il coordinatore ha aggiunto i moduli `RelativeMassFlow`, `AffinePositivity` e `FiniteOrbitTransfer`, integrato le dieci nuove unità nella libreria, curato la compilazione e sviluppato il confronto dei profili con passaggio ai fattori di due. S13 ha controllato quest'ultimo con un algoritmo diverso e certificati duali.

Il lavoro degli agenti e i controlli incrociati sono verifiche interne assistite da AI. Non sono una revisione umana indipendente o una certificazione di priorità bibliografica.

Il [protocollo](PROTOCOL_IT.md) fissa l'inizio e la soglia minima di un'ora. Il [bilancio](REPORT_IT.md) distingue le dichiarazioni Lean, le deduzioni su carta, i dati finiti e gli obblighi aperti. I registri finali sono nel [manifest](verification_manifest.json).
