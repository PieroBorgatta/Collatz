# Revisione indipendente degli audit delle dipendenze

24 settembre 2026. Revisione in sola lettura dei due script e delle API Lean chiamate. **Gli audit delle radici non sono stati eseguiti in questa revisione: qui non si attesta alcun PASS.** Nessuna modifica ai sorgenti Lean, nessuna compilazione.

Il controllo del codice non ha individuato una lacuna concreta che permetta a un corpo `opaque` o a un helper privato raggiunto di nascondere assiomi negli ambiti dichiarati. I due script hanno però perimetri diversi, da conservare nelle descrizioni dei risultati.

## WeightedDependencyAudit

- Parte dal nome pubblico unico con suffisso `weighted_predecessors_positive_lower_density`.
- Controlla presenza nell'ambiente verificato del kernel e proprietà del modulo delle tre dichiarazioni iniziali.
- Espande transitivamente tipo e corpo delle dichiarazioni appartenenti ai moduli `Erdos1135`, `Erdos1135.*`, `Weighted*`, `CollatzPredecessorDensity`. La selezione usa il modulo proprietario: i nomi privati non sono esclusi.
- Richiede che la traversata raggiunga `WeightedPathOccupation.sum_weight_visits_le` e il lemma con suffisso `weighted_exists_large_predecessor_in_residue`.
- Controlla i nomi vietati prima dell'eventuale arresto alla frontiera.
- `Lean.collectAxioms root` controlla separatamente che gli assiomi transitivi della radice appartengano a `{propext, Classical.choice, Quot.sound}`.

**Limite concreto:** la traversata dei corpi termina quando il modulo non soddisfa il filtro. `FormalConjectures.*`, `Mathlib.*`, `Lean.*` e un eventuale modulo `TwoSeed*` sono fuori da quel filtro. Una dipendenza vietata nascosta nel corpo di una dichiarazione di frontiera non sarebbe cercata dalla traversata nominale. Il controllo transitivo degli assiomi resta operativo tramite `collectAxioms`, ma non sostituisce il controllo dei nomi vietati oltre la frontiera. L'affermazione corretta è quindi “dipendenze vietate assenti dalla chiusura locale ispezionata”, non “assenza dimostrata in tutti i corpi importati”. Non ho trovato un simile percorso nascosto nei file della radice letti: questo è un limite dello schema, non un bypass riscontrato.

Lo script è progettato per importare la radice come modulo. Se fosse eseguito nello stesso modulo aggregato della radice, il controllo iniziale del proprietario fallirebbe: non produrrebbe silenziosamente un conteggio locale vuoto.

## TwoSeedDependencyAudit

- Usa il nome completo `Erdos1135.ND.PositiveDensity.TwoSeedDensity.generalTarget_predecessors_explicit_lower_bound`.
- Richiede la connessione effettiva ai due nuovi lemmi `exists_bounded_nonreturning_predecessor_in_residue` e `noReturn_or_noReturn_of_same_image`.
- Attraversa tutti i nomi raggiunti senza filtri di modulo o di prefisso, inclusi helper privati e dipendenze di terzi.
- Fallisce se una dichiarazione raggiunta non è disponibile tramite `Environment.find?`.
- Respinge direttamente ogni `.axiomInfo` diverso dai tre assiomi ammessi e ripete il controllo con `Lean.collectAxioms`.
- Vieta i vecchi selettori `exists_bound_predecessor_no_return` e `exists_large_nonreturning_predecessor_in_residue`. Il riuso del precedente censimento basato sul non ritorno è esplicitamente consentito.

Questo perimetro è più forte per il controllo dei nomi vietati. Gli eventuali export di teoremi presentati soltanto come `.axiomInfo` farebbero fallire il controllo diretto se non standard; non darebbero un falso PASS. Lo script usa `env.setExporting false` per accedere alla vista privata disponibile.

Il controllo diretto usa `env.find?`, mentre `collectAxioms` consulta l'ambiente verificato e i riepiloghi degli assiomi delle importazioni. Nel contesto previsto — radice importata da un modulo già compilato — non ho individuato un problema concreto dovuto a questa differenza. Il codice non va descritto come un verificatore indipendente del kernel.

## API Lean effettivamente controllate

Runtime interrogato: **Lean 4.30.0-rc2**, commit
`3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc`.

- [`ConstantInfo.getUsedConstantsAsSet`](https://github.com/leanprover/lean4/blob/3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc/src/Lean/Util/FoldConsts.lean#L66) unisce i nomi nel tipo e nel valore, chiamando `value? (allowOpaque := true)`. Sono dunque inclusi i corpi di definizioni, teoremi e dichiarazioni opache. Per gli induttivi visita i costruttori; per i ricursori segue `val.all` oltre al tipo. Non è una scansione testuale di ogni campo: non attraversa direttamente i `RecursorRule.rhs`; usa i collegamenti strutturali forniti da Lean.
- [`ConstantInfo.value?`](https://github.com/leanprover/lean4/blob/3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc/src/Lean/Declaration.lean#L482) restituisce realmente il valore di `.thmInfo` e `.opaqueInfo` quando `allowOpaque` è vero.
- [`Lean.collectAxioms`](https://github.com/leanprover/lean4/blob/3dc1a088b6d2d8eafe25a7cd7ec7b58d731bd7cc/src/Lean/Util/CollectAxioms.lean#L149), in questa versione, usa riepiloghi precalcolati all'esportazione per le dichiarazioni importate. La ricorsione locale legge tipi e corpi nell'ambiente verificato. Il risultato è transitivo sugli assiomi, ma una chiamata runtime non rilegge necessariamente i corpi di tutti i moduli importati.
- `Environment.allImportedModuleNames` corrisponde a `env.header.moduleNames`: l'indicizzazione usata dal primo audit è coerente con `getModuleIdxFor?`.

## Limiti comuni

1. Gli script controllano nomi e connessioni del grafo; non congelano il tipo esatto atteso delle radici con un `example` esplicito. Ho letto gli enunciati correnti: corrispondono rispettivamente alla densità positiva esistenziale e al limite quantitativo con coefficiente/cutoff pubblici. Un futuro cambio di enunciato va controllato separatamente.
2. Una dipendenza raggiunta non è necessariamente indispensabile alla prova. La documentazione di entrambi gli script lo riconosce correttamente.
3. I nomi vietati identificano le dichiarazioni elencate, anche attraverso alias e helper intermedi raggiunti; non riconoscono automaticamente una copia matematicamente equivalente rinominata.
4. Il corpo di un `opaque` non viene saltato. Il flag `isUnsafe` non è invece controllato esplicitamente dai due script: nessuna attestazione autonoma sui flag di sicurezza o sulla correttezza del runtime deve essere dedotta dal solo elenco degli assiomi. La validazione dei termini rimane quella del compilatore/kernel e degli artefatti importati.
5. La correttezza semantica della modellizzazione e la revisione delle argomentazioni analitiche restano distinte dall'audit delle dipendenze.

## Impronte dei file letti

SHA-256:

| File | SHA-256 |
|---|---|
| `WeightedDependencyAudit.lean` | `d990af92dab669b9f07d7727fddd3dad1496f8a31e8f248d6af3d13603040437` |
| `TwoSeedDependencyAudit.lean` | `5c6e1523a78ad82ba8c0e6f45d31fde56d54dea5d1d06c29ed3903704449d990` |
| Lean `Util/FoldConsts.lean` | `8d0129eab48b7abe62ea62cbaa6e04f3076f797ffd6bf4f089621de853af72be` |
| Lean `Util/CollectAxioms.lean` | `64f340d42f18c51ee83527f03fa69cc26415dd71dcf7fe71031b7760be90007d` |
| Lean `Declaration.lean` | `ca8ef13f4bb13725ebf7bc23c7de72ff1e0af75580a7007f5d3a7c69cc4004de` |
| Lean `Environment.lean` | `54f6ca1b7a49a52ff2d9fadb4ef544745584961d5e091ce6dd998228dbd2b253` |

Script esaminati nella directory `research/weighted_predecessors_adapter/`; sorgenti runtime letti da `/tmp/collatz-lean-4.30.0-rc2/src/lean/Lean/`.
