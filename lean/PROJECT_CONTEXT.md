# PROJECT_CONTEXT.md

## Stato attuale

`CollatzShadowing` e un progetto Lean 4/Lake autonomo nella sottodirectory
`lean/` del repository `Collatz`.

La libreria dichiara e verifica moduli matematici relativi a mappe
Syracuse/Collatz, shadowing 2-adico, grafi di episodi, operatori finiti e
certificati Collatz-Wielandt. Il codice sorgente principale e in
`CollatzShadowing/`; i certificati importati da generatori esterni sono in
`CollatzShadowing/Generated/`.

## Cosa e confermato dal repository

- Stack: Lean 4, Mathlib, Lake.
- Toolchain: `leanprover/lean4:v4.29.1`.
- Mathlib: `v4.29.1`.
- Target Lake: `CollatzShadowing`.
- Licenza dichiarata in `lakefile.toml`: `CC-BY-4.0`.
- Numero righe Lean osservato: circa `51295` righe tra moduli manuali e
  generati.
- La README esistente dichiara che il progetto e `sorry`-, `admit`- e
  `axiom`-free. Da verificare sempre con `rg` prima di una release.

## Cosa non e presente

- Nessun frontend web.
- Nessuna dashboard o pannello admin.
- Nessun server HTTP applicativo.
- Nessun database applicativo.
- Nessun Dockerfile o `docker-compose.yml` nella directory `lean/`.
- Nessun file `.env` nella directory `lean/`.

## Percorsi importanti

- Progetto Lean: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean`
- Root git: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz`
- Moduli Lean: `CollatzShadowing/*.lean`
- Moduli generati: `CollatzShadowing/Generated/*.lean`
- Script generatori citati dal repository:
  `../scripts/phantom_taxonomy/` e `../scripts/spectral_program/`
- Documentazione Wiki.js: `docs/wiki-source.md`

## Rischi e attenzioni

- I file generati sono grandi e vanno trattati come output di pipeline.
- Il paper e i file nella root superiore possono avere modifiche indipendenti.
- Non confondere certificati finiti o bridge condizionali con una prova
  completa della congettura di Collatz.
- Alcune parti del programma sono dichiaratamente aperte o condizionali:
  usare `Da verificare` o indicare chiaramente `ipotesi aperta`.

## Stato Wiki.js

Il repository ora contiene una pagina principale pronta per import manuale o
sincronizzazione in Wiki.js:

- `docs/wiki-source.md`

Indirizzo IP o URL della istanza Wiki.js: Da verificare.
