# Architettura

## Vista generale

`CollatzShadowing` e una libreria Lean 4. L'architettura e modulare:

1. definizioni base per valutazione 2-adica e mappa Syracuse;
2. parole fantasma e rappresentanti razionali/2-adici;
3. lemma di shadowing e conseguenze;
4. grafo episodi, operatori finiti e certificati;
5. bridge condizionali verso discesa/Collatz;
6. moduli generati con certificati finiti.

## Albero cartelle

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
      *.lean
  docs/
    wiki-source.md
    *.md
```

## Moduli principali

- `Basic.lean`: `ν₂`, `S`, numeratore ed esponente Syracuse.
- `Phantom.lean`: `PhantomWord`, coefficienti affini, `q_w`.
- `Syracuse2Adic.lean`: estensione 2-adica `Syracuse2adic`.
- `Auxiliary.lean`: lemmi tecnici per shadowing.
- `Shadowing.lean`: lemma di shadowing congruenziale esatto.
- `NoInfinite.lean`: no-infinite-shadowing e risultato su cicli espansivi.
- `EpisodeGraph.lean`: relazione diretta, reachability, SCC e certificati.
- `Operator.lean`: stati finiti, matrici di trasferimento, decomposizioni.
- `Bound.lean`: API certificati Collatz-Wielandt e spectral radius.
- `WeakBridge.lean`: bridge finiti A0 e label split.
- `CollatzBridge.lean`: bridge condizionali di discesa verso Collatz.
- `Generated/*.lean`: certificati finiti generati da script esterni.

## Flusso dei dati

```text
script Python esterni
        |
        v
CollatzShadowing/Generated/*.lean
        |
        v
moduli Lean generici: Operator, Bound, EpisodeGraph, WeakBridge
        |
        v
teoremi e certificati verificati da lake build
```

## Servizi

Non ci sono servizi runtime nel progetto Lean.

- Docker: non presente nella directory `lean/`.
- API HTTP: non presente.
- Database: non presente.
- Porta locale: nessuna.

## Confini importanti

Il progetto formalizza risultati e bridge verificabili, ma non afferma una
prova completa della congettura di Collatz. Le ipotesi aperte sono isolate in
dichiarazioni come `Prop` e vanno presentate come tali.
