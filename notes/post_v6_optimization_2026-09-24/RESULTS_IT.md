# Semi compatti e decadimento di ordine sei

24 settembre 2026. **Risultato verificato:** la nuova via fornisce un
coefficiente di densità strettamente maggiore e un cutoff strettamente
minore rispetto alle formule uniformi della precedente via dei due semi.
La [CI 36009718722](https://github.com/PieroBorgatta/Collatz/actions/runs/36009718722),
sul commit `1847065cff482fd9a71c4b7b7c9850b47fe9e23c`, ha verificato
**399 moduli e tutti e tre gli audit finali**. I quattro nuovi moduli contengono
40 teoremi pubblici e due lemmi privati.

Il teorema di densità dei predecessori resta quello esterno di Lech Mazur.
Il risultato qui riguarda una costruzione quantitativa migliore delle nostre
precedenti formule, senza nuova ipotesi analitica. Non è una prova di Collatz,
una rivendicazione di priorità bibliografica assoluta o di ottimalità globale.
PDF e archivio della v6 pubblicata restano invariati.

## 1. Riduzione del limite del seme

Scriviamo `G(r,k)=ndGeneralTargetRoot r k` e `Q=3^q`. Il punto iniziale
`r=seedBase(a)` è positivo quando `a>0` e `3∤a`. La formula esatta dà
`G(r,k)≥4^k`. Per superare la soglia `16^b` basta dunque `k>2b`.

Sia p l'indice della classe utile, con `0≤p<Q`. Posto `B=2b`, scegliamo

\[
\ell=\lfloor B/Q\rfloor+\mathbf1_{p\le B\bmod Q},\qquad k=p+\ell Q.
\]

Allora `2b<k≤2b+Q` e `k+Q≤2b+2Q`. I due candidati `G(r,k)` e
`G(r,k+Q)` sono nella stessa classe ternaria richiesta e hanno lo stesso
successore Syracuse. Almeno uno non ha ritorni positivi, per l'iniettività
della mappa sui suoi punti periodici. Entrambi sono limitati da

\[
T_{\mathrm{new}}=G(2a,2b+2Q)
  <G(2a,(16^b+3)Q)=T_{\mathrm{old}}.
\]

La disuguaglianza è universale nei parametri naturali del lemma. La
costruzione non decide quale candidato sia nonperiodico. Il bound uniforme
è indipendente sia dal residuo utile sia da tale scelta.

File: [CompactSeedNonreturn.lean](../../research/weighted_predecessors_adapter/CompactSeedNonreturn.lean).

## 2. Conservazione del decadimento analitico

La stima disponibile dà un errore L1 `≤(2/3)C/m^6`. La precedente
conversione lo maggiorava mediante `C/m²`, scegliendo un conduttore lineare.
L'API del census permette invece di fissare

\[
D=\frac{2C}{3m^4},\qquad \frac D{m^2}=\frac{2C}{3m^6}.
\]

Il livello m è fissato prima della quantificazione sui livelli `k≥m`:
D può quindi dipendere da m. Il budget per la massa iniziale `2/3` diventa
esattamente `88TC≤m^6`. Definiamo

\[
m_{\mathrm{new}}=\min\{m\in\mathbb N:1\le m\ \text{e}\ 88T_{\mathrm{new}}C\le m^6\}.
\]

Il predicato è decidibile e ha un testimone finito `88TC+1`. Il codice usa
`Nat.find`; minimalità e budget sono dimostrati. Il valore è la radice sesta
intera arrotondata per eccesso, con minimo 1. Non si richiede una scelta
esistenziale del seme per determinarlo.

`Nseed` e `Nmark` continuano a usare la costante globale C. Soltanto il
conteggio terminale usa D. L'ordine è `C → b,Nseed,q → T → m → D,J,H`;
la [revisione semantica](SEMANTIC_AUDIT_IT.md) controlla questo punto e i
fattori numerici. Nessuna delle enormi costanti pubbliche è stata valutata.

File: [OptimizedConductor.lean](../../research/weighted_predecessors_adapter/OptimizedConductor.lean)
e [OptimizedDensity.lean](../../research/weighted_predecessors_adapter/OptimizedDensity.lean).

## 3. Confronto formale delle costanti pubbliche

I due percorsi condividono esattamente `b=2^80`, la costante globale C,
`Nseed`, q e `Nmark`. Cambiano il limite del seme e il conduttore.

| Quantità | Via precedente | Nuova via | Confronto Lean |
|---|---|---|---|
| Limite T | `G(2a,(16^b+3)Q)` | `G(2a,2b+2Q)` | nuovo strettamente minore |
| Conduttore m | `132*T_old*C+1` | minimo positivo con `88*T_new*C≤m^6` | nuovo non maggiore; strettamente minore se `C>0` |
| Coefficiente c | `3/(256*T_old*3^m_old)` | `3/(256*T_new*3^m_new)` | nuovo strettamente maggiore |
| Cutoff | `32*(H_old+1)` | `32*(H_new+1)` | nuovo strettamente minore |

Qui `J=Nmark+2m+20·10^9` e
`H=2^((2J+4)b·2^J+J(17(J+1)+1))*T`. Il miglioramento della soglia segue
alla monotonia dell'esponente in J e alla crescita stretta nel fattore T.
La stretta disuguaglianza per c e cutoff vale anche se C=0 e m resta uguale.

[OptimizedComparison.lean](../../research/weighted_predecessors_adapter/OptimizedComparison.lean)
dimostra questi confronti direttamente sulle formule del codice, per ogni
`a>0`, senza ipotesi di mixing o scelta di semi. Il teorema di densità richiede
inoltre `3∤a`. Specializzando C alla costante numerica esterna, il nuovo
enunciato pubblico dà `c_new>0` e, per ogni naturale `Y≥cutoff_new`, almeno
`c_new*Y` predecessori positivi distinti strettamente sotto Y.

Non è un confronto con il chooser esistenziale della via pesata: i due
termini confrontati sono le formule uniformi dei due percorsi dichiarati.
L'enunciato riassuntivo è
`OptimizedComparison.public_constants_strictly_improve`.

## 4. Evidenze e limiti della verifica

La CI finale ha ricontrollato e riusato **398** ricevute di moduli già compilati
e compilato l'ultimo: **399 moduli locali verificati**, con 388 moduli della
catena esterna e 11 dell'overlay. Non è un rebuild integrale da zero in una
sola esecuzione. Il riuso verifica sorgenti, dipendenze, configurazione e hash
degli oggetti; le librerie esterne provengono dalla cache fissata di Mathlib.
La toolchain è Lean 4.30.0-rc2, Mathlib
`5450b53e5ddc75d46418fabb605edbf36bd0beb6`.

L'audit della nuova radice ha percorso **43.285 dichiarazioni**, inclusi
5.037 privati, 41.329 corpi e 1.094.941 archi tipo/corpo, senza filtro di
modulo. Ha raggiunto il seme compatto, la conversione di ordine sei e il suo
budget. I vecchi selettori vietati e il fallback al precedente teorema di
densità non compaiono nella chiusura ispezionata. Gli audit dei due percorsi
precedenti sono passati nuovamente.

La radice e quattro enunciati di confronto/minimalità hanno soltanto
`propext`, `Classical.choice` e `Quot.sound`. Il controllo eseguibile del
conduttore dà `[1,1,3,5]` per `(T,C)=(0,7),(1,0),(1,1),(100,1)`.
La compilazione conserva un avviso protettivo: una potenza con esponente
`2^80` non viene valutata numericamente. Nessuna soglia è stata aumentata.

Evidenze permanenti:

- [ricevuta dei 399 moduli](modular_receipt.json) e [log del replay](modular_build.log);
- [audit ottimizzato e confronti](optimized_dependency_audit.log);
- [audit pesato](weighted_dependency_audit.log) e [audit precedente dei due semi](two_seed_dependency_audit.log);
- [artefatto CI completo, 414 file](ci_evidence_36009718722.tar.gz);
- [manifest degli hash e cronologia CI](verification_manifest.json).

Dopo il download sono stati verificati tutti i 399 hash dei log e gli 11 hash
dei sorgenti overlay. Il [controllo aritmetico riproducibile](exact_checks.py)
ha inoltre superato 42.471 casi dei semi e 31.031 del conduttore. Sono controlli
finiti, non sostituti delle prove generali né decisioni della nonperiodicità.
L'esempio numerico nel JSON usa piccoli parametri illustrativi e non quelli
pubblici del teorema analitico.

Le costanti restano enormi e la ricerca naturale minima non è proposta come
algoritmo pratico per calcolarle. Il replay usa la toolchain fissata; non è
un controllo con kernel indipendente né una revisione umana completa della
catena analitica. Il risultato riguarda le costanti dei predecessori: la
convergenza universale di Collatz resta aperta.
