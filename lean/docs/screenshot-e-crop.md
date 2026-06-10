# Screenshot e crop

## Stato

Non sono stati generati screenshot automatici perche il progetto non contiene
frontend, sito, dashboard, form, pannelli admin o server locale da aprire nel
browser.

Cartella predisposta:

```text
docs/assets/screenshots/
```

## Screenshot da acquisire manualmente

Quando serve popolare Wiki.js con immagini, acquisire questi screenshot senza
mostrare token, email, path sensibili non necessari o dati personali.

### 1. Build Lean riuscito

- Comando:

  ```bash
  cd /Volumes/AFUOCO/SVILUPPO/TEORIE/Collatz/lean
  /Volumes/AFUOCO/MAC/Applicazioni/elan/bin/lake build
  ```

- Salvare come:

  ```text
  docs/assets/screenshots/lake-build-success.png
  ```

- Crop consigliato: terminale con comando e righe finali dell'output.
- Didascalia: `Build completo Lake/Lean completato con successo.`

### 2. Controllo assenza placeholder

- Comando:

  ```bash
  rg -n "sorry|admit|^[[:space:]]*axiom" CollatzShadowing -g "*.lean"
  ```

- Salvare come:

  ```text
  docs/assets/screenshots/no-placeholders-check.png
  ```

- Crop consigliato: comando e assenza di output.
- Didascalia: `Controllo placeholder Lean senza occorrenze.`

### 3. Struttura progetto

- Schermata editor o terminale con:

  ```bash
  tree -L 2 CollatzShadowing docs
  ```

- Se `tree` non e installato:

  ```bash
  find CollatzShadowing docs -maxdepth 2 -type d -o -type f | sort | sed -n '1,120p'
  ```

- Salvare come:

  ```text
  docs/assets/screenshots/project-structure.png
  ```

- Didascalia: `Struttura principale del progetto Lean e della documentazione.`

### 4. Pagina Wiki.js sincronizzata

- Aprire Wiki.js all'indirizzo configurato.
- URL/IP Wiki.js: Da verificare.
- Salvare come:

  ```text
  docs/assets/screenshots/wikijs-page.png
  ```

- Didascalia: `Pagina principale Wiki.js generata da docs/wiki-source.md.`

## Sintassi Markdown per inserire immagini

```markdown
![Build completo Lake/Lean](assets/screenshots/lake-build-success.png)
```

Ogni immagine deve avere una didascalia testuale subito sotto o nella sezione
che la introduce.
