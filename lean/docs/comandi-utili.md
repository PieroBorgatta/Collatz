# Comandi utili

Eseguire i comandi da:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

## Build

Build completo:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Scaricare cache Mathlib:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake exe cache get
```

Build modulo singolo:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build CollatzShadowing.Shadowing
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build CollatzShadowing.NoInfinite
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build CollatzShadowing.Bound
```

## Controlli qualita

Controllo placeholder Lean:

```bash
rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
```

Elenco file principali:

```bash
rg --files CollatzShadowing
```

Indice dichiarazioni:

```bash
sed -n '1,220p' CollatzShadowing/THEOREM_INDEX.md
```

## Git

Stato repository:

```bash
git status --short --branch
```

Vedere solo modifiche nella directory Lean:

```bash
git status --short -- lean
```

Commit documentazione:

```bash
git add lean/AGENTS.md lean/CLAUDE.md lean/PROJECT_CONTEXT.md lean/README.md lean/CHANGELOG.md lean/TODO.md lean/docs
git commit -m "docs: add Wiki.js technical documentation"
git push origin phase10-wip
```

## Rigenerazione certificati

Gli script generatori citati dal progetto sono nella root superiore:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
ls scripts/phantom_taxonomy
ls scripts/spectral_program
```

La procedura precisa per rigenerare ogni certificato e Da verificare per ogni
script prima di sovrascrivere file in `CollatzShadowing/Generated/`.
