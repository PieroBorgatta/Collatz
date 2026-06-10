# CLAUDE.md

Istruzioni per Claude e altri assistenti che lavorano su
`CollatzShadowing`.

## Obiettivo del progetto

Formalizzare in Lean 4, con Mathlib, il nucleo verificabile del programma
`Phantom Orbit Shadowing` per Syracuse/Collatz:

- lemma di shadowing congruenziale esatto;
- corollario di no-infinite-shadowing;
- esclusione di cicli espansivi per endpoint positivi;
- certificati finiti di tipo Collatz-Wielandt;
- bridge condizionali di discesa verso Collatz.

Il progetto non contiene una prova completa della congettura di Collatz.

## File da leggere all'avvio

1. `PROJECT_CONTEXT.md`
2. `README.md`
3. `TODO.md`
4. `CollatzShadowing/THEOREM_INDEX.md`
5. File Lean direttamente coinvolti nella modifica richiesta.

## Convenzioni Lean

- Namespace principale: `CollatzShadowing`.
- Preferire import stretti rispetto a `import Mathlib`.
- Mantenere `relaxedAutoImplicit = false`.
- Ogni teorema collegato al paper deve avere commento che spiega il ruolo.
- Non introdurre `sorry`, `admit` o `axiom` in stato finale, salvo richiesta
  esplicita di bozza e con nota chiara in `TODO.md`.
- Per modifiche su certificati generati, preferire aggiornare lo script
  generatore nella root superiore e rigenerare il file Lean.

## Comandi

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Controllo placeholder:

```bash
rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
```

## Note di sicurezza

- Non inserire segreti o dati personali nei file.
- Non cancellare o revertire modifiche utente fuori dallo scope.
- Se un'informazione non e deducibile dal repository, scrivere
  `Da verificare`.
