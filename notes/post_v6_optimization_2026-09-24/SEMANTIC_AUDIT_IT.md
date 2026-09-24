# Audit semantico del conduttore ottimizzato

**Aggiornamento successivo:** nuova via e confronti verificati nella
[CI 36009718722](https://github.com/PieroBorgatta/Collatz/actions/runs/36009718722).
Il testo sotto conserva il perimetro della lettura statica iniziale;
le evidenze del replay sono nel [resoconto finale](RESULTS_IT.md).

24 settembre 2026. Lettura dei sorgenti `OptimizedConductor.lean`,
`OptimizedDensity.lean` e delle API esterne immediatamente utilizzate.
**Stato al momento della lettura iniziale: nuova implementazione in attesa di CI.** Questa nota non
attesta compilazione o audit delle dipendenze della nuova via; non è un
nuovo controllo dell'intera dimostrazione analitica esterna.

**Esito della lettura:** non ho individuato circolarità, quantificatori
incompatibili o fattori mancanti nel passaggio alla sesta potenza.

## Perché D può dipendere da m

La definizione esterna `ndExplicitQuadraticMixingAt D m`
(`Geom2ShiftedWideSymmetricExplicitConductor.lean:7–11`) tiene **m fissato**
e richiede il bound L1 `D/m²` per ogni livello `k≥m`. Non richiede una sola
costante `D` valida simultaneamente per diversi valori di `m`.

La stima globale disponibile è invece
`syracFineScaleMixingAt 6 C`: per ogni `1≤m≤k`, oscillazione `≤C/m⁶`
(`Tao/Fourier/MixingStatement.lean:40–42`). L'identità
`unitReferenceDensity_fullL1_eq_twoThirds_oscillation` introduce esattamente
il fattore `2/3` (`Geom2ShiftedWideSymmetricReferenceDensityTransport.lean:24`).
Dunque, fissato `m≥1`,

\[
\mathrm{L1}(m,k)\le\frac{2C}{3m^6}
=\frac{D}{m^2},\qquad D=\frac{2C}{3m^4},\quad k\ge m.
\]

Questo è precisamente ciò che afferma `scaled_quadratic_mixing`
(`OptimizedConductor.lean:90–101`). Il codice non assume che `D` sia una nuova
costante globale per `syracFineScaleMixingAt 6`.

## Budget e massa: il coefficiente 88 è corretto

Il census esterno richiede
`88*P*Cmix ≤ α*m²` e ricava un errore `44*P*Cmix/m² ≤ α/2`
(`Geom2ShiftedWideSymmetricExplicitConductor.lean:13–19`;
`GeneralTargetTerminalCensus.lean:181–210`). Nel singleton `P=r≤T`,
la massa disponibile è `α=2/3` e `Cmix=D≥0`. Il budget scelto dà

\[
88TC\le m^6
\Longrightarrow
88rD\le\frac23m^2
\Longrightarrow
44r\frac{D}{m^2}\le\frac13.
\]

Il `2/3` della conversione L1 si cancella con il `2/3` della massa: non
occorre reintrodurre il precedente fattore 132. Con `p=3^m`, il census
restituisce `9α/(16p)=3/(8·3^m)`; dividendo ancora per `32T` si ottiene
esattamente `3/(256T·3^m)`. Le istanziazioni sono in
`OptimizedDensity.lean:198–209,212–238,243–250`.

## Ordine dei parametri e assenza di circolarità

L'ordine effettivo è

`C → b,Nseed,q → T → m → D,J,H,c,cutoff`.

- `b=2^80`, `Nseed` e `markedStart` conservano il **C globale**
  (`OptimizedDensity.lean:132–145`). Il lemma analitico della massa marcata
  riceve ancora `C` e `hmix` (`:85–128`), come richiede la sua API esterna.
- Il residuo buono viene scelto all'interno della prova, mentre `T` è il
  maggiorante compatto uniforme, dipendente solo da `a,b,q` (`:22–24,39–44`).
- `m` è il minimo naturale positivo con `88TC≤m⁶`. Il predicato è decidibile
  e ha il testimone finito `88TC+1` (`OptimizedConductor.lean:18–40`).
  `Nat.find` cerca fra naturali tramite un predicato decidibile; non sceglie
  il seme e non introduce una dipendenza dalla sua nonperiodicità.
- Soltanto dopo aver fissato `m` viene formato `D`. Esso compare nel census
  terminale (`OptimizedDensity.lean:200–209,231–235`), non nella definizione
  del seed generation, del residuo o di `T`.
- La condizione `m≤k` del census è fornita da `n≥J≥2m` e dal lemma sul quarto
  del floor (`:227–234`). Non è lasciata come ipotesi pubblica aggiuntiva.

L'enunciato finale (`:268–275`) continua a richiedere soltanto `a>0` e
`3∤a`; usa la stessa stima numerica esterna di mixing. La produzione della
generazione per ogni soglia `Y` resta affidata all'API di conteggio già
impiegata dalla via two-seed. Nessuna selezione algoritmica del candidato
nonperiodico né valutazione pratica delle enormi costanti è stata verificata
da questa lettura.

## Controllo complementare del confronto

In `OptimizedComparison.lean`, i due `rootBound` condividono esattamente
`b,Nseed(C),q`; cambia solo il maggiorante del seme. Analogamente, i due
`markedStart` coincidono. L'esponente della funzione `intervalHeight` è
monotono nel numero di generazioni, e il fattore esterno `T` è strettamente
crescente: la riduzione stretta del cutoff non richiede `C>0`.
Anche il coefficiente migliora strettamente quando l'arrotondamento lascia
`m` invariato, grazie a `T` strettamente minore. Nessun disallineamento
semantico individuato; l'elaborazione Lean di questi confronti era ancora da verificare in CI.
