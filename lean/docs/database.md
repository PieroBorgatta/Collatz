# Database

## Stato

Il progetto `CollatzShadowing` non usa un database applicativo.

Non sono presenti nella directory `lean/`:

- migrazioni SQL;
- schema Prisma, Rails, Django o simili;
- file SQLite applicativi;
- connessioni Postgres/MySQL;
- servizi Docker per database;
- variabili ambiente database.

## Dati presenti

I dati strutturati del progetto sono rappresentati come:

- definizioni e teoremi Lean;
- moduli generati in `CollatzShadowing/Generated/`;
- file JSON/CSV sorgenti dei generatori: Da verificare nella root superiore.

## Backup

Per questa directory il backup operativo coincide con Git:

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
git status --short --branch
git push origin phase10-wip
```

Eventuali dataset intermedi fuori da Git: Da verificare.
