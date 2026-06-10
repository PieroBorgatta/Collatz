# AGENTS.md

Guida rapida per agenti AI e sessioni future sul progetto Lean
`CollatzShadowing`.

## Contesto essenziale

- Directory progetto Lake: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean`
- Root git: `/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz`
- Branch corrente al momento della generazione documentazione:
  `phase10-wip`
- Remote git: `https://github.com/PieroBorgatta/Collatz`
- Toolchain: Lean `4.29.1`, Mathlib `v4.29.1`
- File toolchain: `lean-toolchain`
- Manifest Lake: `lakefile.toml`, `lake-manifest.json`

Il progetto formalizza in Lean 4 parti del programma
`Phantom Orbit Shadowing` collegato a Collatz/Syracuse. Non e una web app,
non espone API HTTP e non contiene un database applicativo.

## Prima di modificare codice

1. Leggere `PROJECT_CONTEXT.md`.
2. Leggere `README.md`.
3. Leggere `TODO.md`, soprattutto la sezione iniziale e il log piu recente.
4. Per dichiarazioni Lean gia presenti, consultare
   `CollatzShadowing/THEOREM_INDEX.md`.
5. Verificare lo stato git:

   ```bash
   cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
   git status --short --branch
   ```

Attenzione: il repository git include anche la directory superiore. Possono
esistere modifiche fuori da `lean/`; non revertirle e non includerle in commit
di documentazione Lean se non richiesto.

## Comandi principali

Usare il `lake` installato da elan:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake exe cache get
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Se `lake` e nel `PATH`, e equivalente:

```bash
lake exe cache get
lake build
```

Build di moduli singoli:

```bash
lake build CollatzShadowing.Shadowing
lake build CollatzShadowing.NoInfinite
lake build CollatzShadowing.Generated.A0ReturnBranches
```

Controllo placeholder:

```bash
rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
```

## Regole operative

- Non affermare che il progetto dimostra la congettura di Collatz.
- Distinguere sempre tra risultati provati in Lean, certificati finiti
  generati e ipotesi aperte isolate come `Prop`.
- Non modificare file generati in `CollatzShadowing/Generated/` a mano, salvo
  correzioni esplicitamente richieste e documentate.
- Se un fatto matematico, comando o percorso non e verificato localmente,
  scrivere `Da verificare`.
- Non salvare token, password, email o dati personali nei Markdown.
- Dopo modifiche Lean, eseguire almeno il build del modulo toccato. Per
  modifiche solo documentali, indicare che il build completo non e necessario.

## Screenshot

Non ci sono frontend, dashboard, form o pannelli admin in questa directory.
Gli screenshot utili per Wiki.js sono quindi solo screenshot manuali di:

- output terminale di `lake build`;
- struttura cartelle in editor/file manager;
- pagina Wiki.js dopo import/sincronizzazione.

La lista operativa e in `docs/screenshot-e-crop.md`.
