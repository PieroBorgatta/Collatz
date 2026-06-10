# CollatzShadowing

Documentazione tecnica per il progetto Lean 4/Lake
`CollatzShadowing`, parte del repository `Collatz`.

`CollatzShadowing` formalizza in Lean 4 il nucleo verificabile del programma
`Phantom Orbit Shadowing` applicato alla mappa Syracuse/Collatz: shadowing
congruenziale, risultati di no-infinite-shadowing, operatori finiti e
certificati Collatz-Wielandt.

Importante: questa libreria non prova la congettura di Collatz. Formalizza
risultati verificati e bridge condizionali; gli obblighi aperti sono isolati
come proposizioni nominate.

## Stato attuale

- Stack: Lean 4, Mathlib, Lake.
- Toolchain: Lean `4.29.1`.
- Mathlib: `v4.29.1`.
- Target Lake: `CollatzShadowing`.
- Directory locale:
  `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean`
- Root git:
  `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz`
- Remote:
  `https://github.com/PieroBorgatta/Collatz`
- Branch osservato durante la generazione documentale: `phase10-wip`.

La documentazione Wiki.js e pronta in:

```text
docs/wiki-source.md
```

URL/IP Wiki.js: Da verificare.

## Avvio e build

Entrare nella directory del progetto:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

Scaricare cache Mathlib:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake exe cache get
```

Build completo:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Se `lake` e nel `PATH`, si puo usare:

```bash
lake exe cache get
lake build
```

Build di moduli singoli:

```bash
lake build CollatzShadowing.Shadowing
lake build CollatzShadowing.NoInfinite
lake build CollatzShadowing.Bound
```

Controllo assenza placeholder:

```bash
rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
```

## Struttura

```text
lean/
  lakefile.toml
  lean-toolchain
  CollatzShadowing.lean
  CollatzShadowing/
    Basic.lean
    Phantom.lean
    Syracuse2Adic.lean
    Auxiliary.lean
    Shadowing.lean
    NoInfinite.lean
    CollatzBridge.lean
    EpisodeGraph.lean
    Operator.lean
    WeakBridge.lean
    Bound.lean
    Generated/
  docs/
```

## Moduli principali

- `Basic`: valutazione 2-adica e mappa Syracuse accelerata `S`.
- `Phantom`: parole fantasma, coefficienti affini e rappresentante `q_w`.
- `Syracuse2Adic`: estensione 2-adica della mappa Syracuse.
- `Shadowing`: lemma di shadowing congruenziale esatto.
- `NoInfinite`: no-infinite-shadowing e cicli espansivi.
- `EpisodeGraph`: relazioni dirette, reachability, SCC.
- `Operator`: stati finiti e matrici di trasferimento.
- `Bound`: certificati Collatz-Wielandt e spectral radius.
- `WeakBridge`: bridge finiti A0 e label split.
- `CollatzBridge`: bridge condizionali di discesa.
- `Generated`: certificati finiti generati e verificati da Lean.

Indice completo:

```text
CollatzShadowing/THEOREM_INDEX.md
```

## Servizi, API e database

Questa directory non contiene servizi runtime.

- Frontend web: non presente.
- API HTTP: non presente.
- Database: non presente.
- Docker: non presente in `lean/`.
- File `.env`: non presente in `lean/`.
- Porte/IP applicativi: non applicabile.

La “API” del progetto e l'insieme delle dichiarazioni Lean documentate in
`docs/api.md`.

## Documentazione

- `AGENTS.md`: guida per agenti AI.
- `CLAUDE.md`: istruzioni specifiche per Claude/assistenti.
- `PROJECT_CONTEXT.md`: contesto sintetico per ripresa futura.
- `CHANGELOG.md`: storico modifiche documentali.
- `TODO.md`: piano operativo e log storico.
- `docs/wiki-source.md`: pagina principale pronta per Wiki.js.
- `docs/installazione.md`: installazione e rete.
- `docs/comandi-utili.md`: comandi ricorrenti.
- `docs/architettura.md`: struttura tecnica.
- `docs/api.md`: API Lean.
- `docs/database.md`: stato database.
- `docs/errori-risolti.md`: problemi tecnici documentati.
- `docs/decisioni-tecniche.md`: decisioni architetturali.
- `docs/screenshot-e-crop.md`: screenshot da acquisire manualmente.

## Screenshot

Non sono stati generati screenshot automatici perche il progetto non ha UI.
La cartella e pronta:

```text
docs/assets/screenshots/
```

Screenshot consigliati per Wiki.js:

- output finale di `lake build`;
- controllo assenza `sorry/admit/axiom`;
- struttura cartelle;
- pagina Wiki.js sincronizzata.

## Licenza

Licenza dichiarata in `lakefile.toml`: `CC-BY-4.0`.
