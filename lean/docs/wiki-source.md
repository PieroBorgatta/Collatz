# CollatzShadowing

## Stato attuale

`CollatzShadowing` e un progetto Lean 4/Lake nella directory:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

Stato confermato dalla ricognizione del 2026-06-10:

- progetto Lean 4 con Mathlib;
- target Lake principale: `CollatzShadowing`;
- toolchain Lean: `leanprover/lean4:v4.29.1`;
- Mathlib: `v4.29.1`;
- moduli manuali in `CollatzShadowing/`;
- certificati generati in `CollatzShadowing/Generated/`;
- nessun frontend, backend HTTP, Docker o database nella directory `lean/`.

Il progetto dichiara nel README che i sorgenti `CollatzShadowing` sono privi di
`sorry`, `admit` e `axiom`. Prima di ogni rilascio verificare con:

```bash
rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
```

## A cosa serve

Il progetto formalizza in Lean parti verificate del programma
`Phantom Orbit Shadowing` legato alla mappa Syracuse/Collatz:

- mappa Syracuse accelerata e valutazioni 2-adiche;
- parole fantasma e rappresentanti razionali/2-adici;
- lemma di shadowing congruenziale esatto;
- no-infinite-shadowing;
- esclusione di endpoint positivi in cicli espansivi;
- operatori finiti e certificati Collatz-Wielandt;
- bridge condizionali di discesa.

Importante: il progetto non prova la congettura di Collatz. Le ipotesi aperte
sono isolate come proposizioni nominate e vanno trattate come obblighi ancora
da chiudere.

## Stack tecnico

- Lean 4 `4.29.1`
- Mathlib `v4.29.1`
- Lake
- Git/GitHub
- Python nella root superiore per generazione certificati: Da verificare per
  singolo script

Non presenti:

- frontend web;
- API HTTP;
- database;
- Docker;
- file `.env` applicativi.

## Dove si trova

Percorso locale:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
```

Root git:

```text
/Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz
```

Remote:

```text
https://github.com/PieroBorgatta/Collatz
```

Branch osservato:

```text
phase10-wip
```

URL o IP Wiki.js: Da verificare.

## Come si avvia

Il progetto non si avvia come servizio. Si compila/verifica con Lake.

```bash
cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake exe cache get
/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
```

Se `lake` e nel `PATH`:

```bash
lake exe cache get
lake build
```

Build modulo singolo:

```bash
lake build CollatzShadowing.Shadowing
lake build CollatzShadowing.NoInfinite
lake build CollatzShadowing.Bound
```

## Servizi principali

Nessun servizio runtime.

| Servizio | Stato | Indirizzo |
|---|---|---|
| App web | Non presente | Non applicabile |
| API HTTP | Non presente | Non applicabile |
| Database | Non presente | Non applicabile |
| Docker | Non presente in `lean/` | Non applicabile |
| Wiki.js | Esterno al progetto | Da verificare |

Indirizzi locali utili solo per strumenti esterni:

- `127.0.0.1`: localhost IPv4, non usato dal progetto Lean.
- `::1`: localhost IPv6, non usato dal progetto Lean.

## Screenshot e flussi visivi

Non sono stati prodotti screenshot automatici perche non esiste una UI
applicativa.

Screenshot da acquisire manualmente:

1. `docs/assets/screenshots/lake-build-success.png`
   - Didascalia: `Build completo Lake/Lean completato con successo.`
2. `docs/assets/screenshots/no-placeholders-check.png`
   - Didascalia: `Controllo placeholder Lean senza occorrenze.`
3. `docs/assets/screenshots/project-structure.png`
   - Didascalia: `Struttura principale del progetto Lean e della documentazione.`
4. `docs/assets/screenshots/wikijs-page.png`
   - Didascalia: `Pagina principale Wiki.js generata da docs/wiki-source.md.`

Dettagli operativi in `docs/screenshot-e-crop.md`.

## Variabili ambiente

Nessuna variabile ambiente applicativa richiesta.

Variabile utile per usare `lake` senza percorso assoluto:

```bash
export PATH="/Volumes/AFUOCO/MAC/Applicazioni/elan/bin:$PATH"
```

Non salvare segreti, token, password, email o dati personali nei file di
documentazione.

## File importanti

| File | Scopo |
|---|---|
| `lakefile.toml` | Configurazione Lake, Mathlib e opzioni Lean |
| `lean-toolchain` | Versione Lean pinning |
| `CollatzShadowing.lean` | Target aggregatore della libreria |
| `CollatzShadowing/THEOREM_INDEX.md` | Indice dichiarazioni e teoremi |
| `CollatzShadowing/Basic.lean` | Mappa Syracuse e valutazioni |
| `CollatzShadowing/Shadowing.lean` | Lemma di shadowing |
| `CollatzShadowing/NoInfinite.lean` | No-infinite-shadowing |
| `CollatzShadowing/Bound.lean` | Certificati Collatz-Wielandt |
| `CollatzShadowing/Generated/` | Moduli generati verificati da Lean |
| `TODO.md` | Piano operativo e log storico |
| `PROJECT_CONTEXT.md` | Contesto sintetico per ripresa futura |

## API

Non esiste una API HTTP. L'API del progetto e costituita da dichiarazioni Lean.

Dichiarazioni principali:

- `S`: mappa Syracuse accelerata su naturali.
- `Syracuse2adic`: estensione 2-adica.
- `PhantomWord`: parole fantasma.
- `exact_shadowing`: lemma di shadowing congruenziale esatto.
- `no_infinite_period_congruence_expansive`: no-infinite-shadowing.
- `FiniteCWCertificate`: certificato Collatz-Wielandt finito.
- `spectralRadius_le_of_finiteCWCertificate`: bridge verso spectral radius.
- `classicalCollatz_of_uniformStrictDescent_provedBridge`: bridge
  condizionale verso Collatz.

Pagina dettagliata: `docs/api.md`.

## Database

Nessun database applicativo.

I dati verificati sono codificati come:

- sorgenti Lean;
- moduli generati Lean;
- eventuali file di input generatore nella root superiore: Da verificare.

Pagina dettagliata: `docs/database.md`.

## Problemi noti

- La pipeline esatta per rigenerare ogni file in `CollatzShadowing/Generated/`
  va verificata script per script.
- Alcuni risultati sono finiti o cap-specific, non teoremi infiniti.
- Le ipotesi globali di discesa restano obblighi aperti, non risultati provati.
- URL/IP Wiki.js non configurato nel repository: Da verificare.
- Build completo verificato il 2026-06-10 con
  `/Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build`:
  `Build completed successfully (3350 jobs).`

## Prossime attivita

- Eseguire `lake build` completo e salvare screenshot.
- Eseguire controllo placeholder e salvare screenshot.
- Documentare procedura precisa di rigenerazione certificati generati.
- Sincronizzare `docs/wiki-source.md` in Wiki.js.
- Inserire URL/IP reale della istanza Wiki.js.
- Aggiornare `TODO.md` dopo ogni sessione tecnica.

## Ultime modifiche

2026-06-10: Documentazione iniziale generata per Wiki.js, con pagine tecniche
su installazione, comandi, architettura, API Lean, database, decisioni tecniche
e screenshot da acquisire.
