# Audit mirato delle costanti di TwoSeedDensity

24 settembre 2026. Ispezione statica di `/tmp/TwoSeedDensity.lean`,
`/tmp/TwoSeedNonreturn.lean` e delle definizioni richiamate nel checkout
`/Volumes/AFUOCO/SVILUPPO/TEORIE/.codex-collatz-predecessor-adapter/2026-09-24`.
Non ho avviato compilazioni, estrazione di programmi o valutazioni numeriche.

**Esito:** nel flusso dei *valori numerici* esaminato non emerge una scelta
esistenziale nascosta. Le costanti sono formule uniformi nel bersaglio `a`,
indipendenti dal residuo buono e da quale dei due semi sia nonperiodico.
Anche il valore naturale `explicitSyracuseMixingCoefficient` si riconduce a
operazioni su naturali e iterazioni finite. Questo è un audit dei sorgenti,
non una certificazione separata dell'eseguibilità del programma Lean.

## Parametri della stima

Pongo `C = explicitSyracuseMixingCoefficient`, `G = ndGeneralTargetRoot` e
`F(b,n) = explicitSeedFloor b n`. Le definizioni ispezionate danno:

| Parametro | Corpo numerico |
|---|---|
| `b` | `2^80` |
| envelope `E₀` | `2^467 * b * 16^b * (C+1)` |
| `Nseed` | `20000 * (Nat.clog 2 E₀ + 64)` |
| `F` | `F(b,0)=b`; `F(b,n+1)=F(b,n)+F(b,n)/100` |
| `q` | `Q(b,F(b,Nseed)/4,Nseed)`, dove `Q(b,k,0)=k`, `Q(b,k,n+1)=b+3*b/5+Q(b+b/100,k,n)` |
| `Xseed` | `16^b` |
| `T` | `G(2*a,(Xseed+3)*3^q)` |
| `m` | `132*T*C+1` |
| `Nmark` | `Nseed+20000*(Nat.clog 2 (21*E₀)+96)` |
| `J` | `Nmark+2*m+20*10^9` |
| `H` | `2^((2*J+4)*b*2^J+J*(17*(J+1)+1))*T` |
| soglia pubblica | `32*(H+1)` |
| coefficiente pubblico | `3/(256*T*3^m)`, interpretato in `ℝ` |

Qui `/` nelle righe naturali è divisione intera. `G(r,k)=(3*r+1)*A(k)+r`,
con `A(0)=0`, `A(k+1)=4*A(k)+1`: nessuna scelta nel calcolo di `T`.
Il ramo di `seedBase` verifica solo `a % 3 = 1`, proposizione decidibile sui
naturali; inoltre `seedBase` non compare nel valore del maggiorante `T`.

Fonti numeriche: `ExplicitVariationBudgets.lean:8`,
`ExplicitLogarithmicVariationBudgets.lean:10`, `ExplicitFrozenCoreSeed.lean:9`,
`Geom2ShiftedWideSymmetricCoreBackwardMean.lean:286`,
`Geom2ShiftedWideSymmetricBalancedCrossingRate.lean:11`,
`ExplicitLogarithmicFrozenSeed.lean:12`, `PredecessorAnalyticSupport.lean:54`,
`A5HistoricalAdjacentCylinderPreviousPhysicalLowerShellNoGo.lean:9`.
Questi percorsi sono relativi a `Erdos1135/ND/PositiveDensity/` nel checkout.

## Il punto meno evidente: C

Ho seguito `ExplicitNumericalSyracuseMixing` →
`ExplicitNumericalPrimitiveDecay` → `ExplicitCanonicalMonotonicity` →
le soglie dei tre casi, incluse `ExplicitCanonicalCase2Moment`,
`ExplicitCanonicalCase3Scale` e `ExplicitCanonicalOuterBadJAbsorption`.
Le soglie sono somme, prodotti, potenze e massimi di naturali.

Il coefficiente primitivo usa `explicitRenewal_fixed hE`, con `E=2^170`.
Questa struttura contiene anche dati reali e prove analitiche, ma i campi
effettivamente proiettati nelle soglie (`Aweight=8192`, `Pmax`, `P=Pmax+1`)
sono assegnati direttamente. In particolare:

- `t=10*6409*2^(3*E)` e `r=2^E*(t+3*(8192+3)+1)+1`;
- `Pmax` è l'iterata `r-1` volte, a partire da `t`, della funzione naturale
  `x ↦ x+10*8^32768*(x+1)^3+1+t`;
- `C = 2*((32*6409*B)^6409*20^6409)+2+2^481`, dove `B` è il massimo
  delle tre soglie naturali suddette, con `L=2^80` e `S₀=2^34*(Pmax+1)`.

Ho verificato anche le definizioni dell'iterazione in
`Tao/Renewal/QEndpointFreshSurvival.lean:21` e `Prop78Case3Event.lean:144–228`,
e `Nat.clog` in Mathlib `Data/Nat/Log.lean:335`: i suoi rami confrontano
naturali. Non occorrono `Classical.choose`, test di periodicità, confronti
fra reali o arrotondamenti di quantità reali per determinare questi numeri.

## Limiti e formulazione da usare

`noncomputable section` compare in diversi file; da solo non dimostra che
i valori naturali qui estratti richiedano una scelta noncostruttiva. Viceversa,
la presente lettura non sostituisce una versione Nat/ℚ separata, compilata e
dimostrata uguale ai parametri originali. Il coefficiente è dichiarato in
`ℝ`; la sua formula è razionale, ma non ho formalizzato tale estrazione.
Le dimensioni sono enormi: formula finita non significa valutazione pratica.

Formulazione supportata: **«formule uniformi esplicite nel bersaglio, senza
dipendenza dal seme scelto né da un'altezza ignota dei cicli»**.
Non attribuire a questo audit un algoritmo già validato che scelga quale
seme è nonperiodico, una valutazione numerica effettuata, né un nuovo audit
dell'intera dimostrazione analitica della stima di mixing.
