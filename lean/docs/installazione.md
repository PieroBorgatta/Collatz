# Installazione

## Prerequisiti

- macOS o Linux con shell POSIX.
- Git.
- Elan/Lean installato.
- Spazio disco sufficiente per la cache Mathlib. La cache puo occupare diversi
  GB.

Nel computer osservato il comando Lake e disponibile qui:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake
```

Se `lake` non e nel `PATH`, usare sempre il percorso assoluto sopra.

## Percorso progetto

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

Root git:

```bash
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
```

Remote GitHub:

```text
https://github.com/PieroBorgatta/Collatz
```

## Installazione dipendenze Lean

Scaricare la cache Mathlib precompilata:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake exe cache get
```

Build completo:

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

## Verifica installazione

```bash
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake --version
```

Versione osservata:

```text
Lake version 5.0.0-src+f72c35b (Lean version 4.29.1)
```

## Indirizzi IP e rete

Il progetto Lean non avvia servizi di rete e non espone porte.

- `127.0.0.1`: usare solo per eventuali servizi locali esterni, ad esempio
  una preview Markdown o una istanza Wiki.js locale. Non e usato dal progetto.
- `::1`: equivalente IPv6 di localhost. Non e usato dal progetto.
- URL Wiki.js di produzione o staging: Da verificare.

## Variabili ambiente

Nessuna variabile ambiente applicativa e richiesta dal progetto Lean.

Variabili utili ma non obbligatorie:

```bash
export PATH="/Volumes/AFUOCO/MAC/Applicazioni/elan/bin:$PATH"
```

Non salvare token GitHub, password o credenziali in `.env` o Markdown.
