# Audit semantico mirato: mixing Syracuse esplicita

Data: 2026-09-24. Sorgenti: `/tmp/collatz-predecessor-audit/assembled`.
Audit in sola lettura: nessuna build nuova, nessuna modifica ai sorgenti esterni.

## Conclusione

`explicitSyracuseMixing_six` è un enunciato chiuso di mixing a scala fine per una **legge probabilistica su residui ternari**, con coefficiente naturale esplicito. Nei wrapper e nelle definizioni esaminate non ho trovato un'ipotesi di terminazione Collatz, di assenza di cicli, di indipendenza statistica lungo una singola orbita reale, o una circolarità manifesta.

Questo non equivale a un audit dell'intera catena analitica, né a una nuova verifica del kernel. Il fatto che i wrapper chiamino teoremi senza ipotesi aperte è verificato nel testo; la validità delle dipendenze analitiche profonde rimane esterna a questo audit circoscritto. La compilazione e `#print axioms` devono completare separatamente la verifica formale.

## Enunciato effettivo

Da `Tao/Fourier/MixingStatement.lean`, con `p_n(y)=(syracPMF n y).toReal`, si definisce

\[
\operatorname{Osc}(m,n)=\sum_{y\bmod 3^n}\left|p_n(y)-3^{m-n}
\sum_{y'\equiv y\pmod{3^m}}p_n(y')\right|.
\]

`Tao.syracFineScaleMixingAt A C` significa esattamente

\[
\forall n,m\in\mathbb N,\quad 1\le m\le n\Longrightarrow
\operatorname{Osc}(m,n)\le C/m^A.
\]

Quindi:

- è una distanza L1 dalla legge resa uniforme **all'interno delle fibre modulo `3^m`**;
- non afferma uniformità globale su tutti i residui modulo `3^n`;
- non afferma una frequenza temporale per una singola orbita Syracuse;
- non contiene uno stopping time Collatz;
- conserva il marginale grossolano modulo `3^m`, compreso il supporto non nullo modulo 3;
- per `m=n` l'oscillazione è identicamente zero, coerentemente con la definizione.

Il teorema finale è `syracFineScaleMixingAt 6 (explicitSyracuseMixingCoefficient : ℝ)`.

## La legge probabilistica è concreta

Da `Tao/Syracuse/Syrac.lean`:

- `syracPMF 0 = PMF.pure 0`;
- al passo `n+1`, la distribuzione precedente viene combinata con `geom2PNat` mediante `PMF.bind`;
- `syracStep n y a = 2^{-a}(3 y.val+1)` in `ZMod(3^(n+1))`;
- `geom2PNat` è la geometrica di parametro `1/2` spostata sugli interi positivi; `geom2PNat_apply_toReal` dà esattamente `P(a)=2^{-a}`.

Questa indipendenza è parte della **definizione del modello aleatorio**. Non viene dedotta o postulata per le valutazioni di un dato intero. Il successivo collegamento a predecessori interi richiede pertanto i lemmi di residuo/affinità e il conteggio delle fibre: proprio il punto su cui interviene l'adapter di occupazione.

È anche esplicito il controllo al primo livello: le masse modulo 3 sono `0`, `1/3`, `2/3`, rispettivamente nei residui `0`, `1`, `2`. Una lettura come “distribuzione uniforme dei valori Syracuse” sarebbe dunque sbagliata già al livello 1.

## Catena principale verificata nel testo

1. `ExplicitNumericalSyracuseMixing.lean`
   - `explicitSyracuseMixing_six` applica `explicitSection6_mixing_nat` a `explicitRenewal_numericalPrimitiveDecay`.
   - Nessuna ipotesi aperta nel teorema finale.
   - Il coefficiente è `2*(C*20^6409)+2+2^481`, con `C=explicitRenewalPrimitiveCoefficient`.
   - `@[irreducible] def` protegge l'elaborazione dei grandi numeri; è una definizione, non un assioma.

2. `ExplicitNumericalPrimitiveDecay.lean`
   - La versione parametrica espone `hmass` (massa localizzata almeno 1/2) e `hcollar` (separazione geometrica).
   - La versione numerica le scarica chiamando `explicitRenewal_numericalLocalizedMass` e `explicitRenewal_numericalCollar`.
   - Usa `E=2^170`, `L=2^80`, esponente di decadimento 6409; coefficiente `(32*6409*Cthreshold)^6409`.
   - Non si tratta di dati numerici floating point importati: nei file letti le disuguaglianze numeriche sono provate con tattiche aritmetiche standard.

3. `ExplicitCanonicalPrimitiveCoefficient.lean`
   - La monotonia dell'effettiva quantità `SourceActualQmAtCutoff` produce un decadimento puntuale di `SourceActualQ`.
   - Il collegamento alla trasformata di Fourier passa per `TaoSection7CharacterBridgeStatement.source_law`, il bound dell'aspettativa e un momento geometrico.
   - Le ipotesi di monotonia sono esplicite nella versione intermedia e scaricate dalla catena numerica.
   - Le prove profonde dell'aspettativa, del momento e delle tre regioni non sono state riesaminate integralmente qui.

4. `ExplicitCanonicalMonotonicity.lean`
   - La soglia è il massimo delle soglie dei casi 1, 2, 3.
   - Costruisce i tre campi `cutoffWhite`, `nearTop`, `farBelow` e applica il lemma di monotonia relativo alla copertura attiva.
   - Le sole ipotesi sostanziali mostrate sono dati geometrici/renewal (`fixed`, `hEStar`, `hmass`, `hcollar`), non la convergenza di orbite Collatz.

5. `ExplicitSection6FixedSlice.lean`
   - Converte il decadimento primitivo di ordine 6409 nel bound di ordine 9 per una slice, assorbendo il fattore entropico di ordine al massimo 6400.
   - La stima L2 e i lemmi del gate restano dipendenze esterne al presente audit.

6. `ExplicitSection6Mixing.lean`
   - Somma le slice (`n` per `2n`) ottenendo ordine 7.
   - Aggiunge il costo della massa rifiutata, controllata da `1/n^7`.
   - Passa dalle scale adiacenti all'ordine 6 tramite telescoping.
   - Copre il regime `m>=2^80`.

7. `Tao/Section6/Prop114Assembly.lean`
   - Estende la stima alle piccole scale mediante il bound universale L1 `<=2`.
   - Da qui nasce il termine `2*(2^80)^6=2^481`.
   - Nessuna ipotesi di terminazione compare nell'assemblaggio.

Le definizioni di Fourier in `DecayStatement.lean` limitano il decadimento alle frequenze primitive (`xi` non multiplo di 3), come previsto dalla struttura ternaria. Il lemma `Section7SourceLaw.source_law` è un teorema dimostrato per induzione sulla PMF e identità di trasformata; non è soltanto un campo assunto di una struttura.

## Il “primo passaggio” renewal non è un arresto di Collatz

Sono stati controllati i punti definitori necessari, senza espandere tutte le prove di coda:

- `CanonicalFirstPassageEndpoint.lean`: la PMF degli endpoint è una `PMF.map` della PMF dei prefissi.
- `HoldFirstPassagePMF.lean:270`: la PMF del prefisso nasce da `taoSection7HoldSourcePrefixListPMF (gap+1)`, quindi da un numero finito prefissato di incrementi.
- `lemma79VerticalFirstPassageCut` cerca il primo attraversamento del livello verticale `start.l+gap`; restituisce 0 fuori dai casi in cui esiste.
- Questo valore di fallback non viene usato per “inventare” arresti sul supporto: `lemma79VerticalFirstPassageCut_decode_pos_le_gap_add_one` prova positività e limite `<=gap+1` per i campioni decodificati, usando incrementi verticali almeno 1.
- `CanonicalFirstPassageLocalizedMass.lean` definisce un evento di deviazione orizzontale e overshoot verticale. Il lemma generale di massa almeno 1/2 è una stima sul complemento di due eventi di massa al massimo 1/4.
- `ExplicitCanonicalCollar.lean` fornisce i valori numerici senza una premessa di terminazione Collatz; `ExplicitCanonicalFirstPassageTails.explicitRenewal_localized_mass` scarica la massa mediante le due stime di coda.

## Limiti e punti da tenere espliciti

1. **Audit formale ancora distinto dall'audit semantico.** Qui non ho ricompilato e non ho interrogato il kernel su `explicitSyracuseMixing_six`. La chiusura sintattica del wrapper non sostituisce l'audit degli assiomi transitivi.
2. **Nessuna circolarità riscontrata nel perimetro letto.** Non è una garanzia sull'intera libreria di centinaia di file. Le dipendenze profonde sono teoremi esterni invocati, non nuovamente verificati da questa lettura.
3. **Il costo numerico è enorme.** Il coefficiente è esplicito ma le soglie sono astronomiche. “Esplicito” non significa utile per esperimenti a scala ordinaria.
4. **Il trasferimento probabilità→predecessori non è automatico.** Occorrono esattezza dei percorsi, confronto dei pesi, ipotesi sulle scale e controllo della molteplicità. L'occupazione universale elimina la necessità di assenza di ritorni nel passaggio di conteggio; non sostituisce gli input analitici.
5. **Il target deve rispettare il supporto aritmetico.** La positività di densità di predecessori non può estendersi ai target positivi divisibili per 3: Syracuse non raggiunge mai un multiplo di 3 dopo un passo. Per la mappa ordinaria i predecessori di un tale target sono soltanto la catena di raddoppi, di densità zero. Il bound universale di occupazione resta valido, ma un input analitico che imponesse massa positiva sufficiente per questi target sarebbe falso.
6. **L'indipendenza lungo un'orbita non è disponibile.** Non riutilizzare `syracPMF` per giustificare frequenze temporali deterministiche senza un teorema separato.

## Perimetro

Lettura completa dei wrapper indicati e dei principali statement (circa dieci file brevi della catena); lettura mirata delle definizioni `syracPMF`, `geom2PNat`, dei prefissi/endpoint di primo passaggio e delle righe che scaricano la massa numerica. Ricerca lessicale dei wrapper letti: nessun `sorry`, `admit`, nuova dichiarazione `axiom`, `native_decide` o premessa `hitsOne`/Collatz. Le definizioni accessorie sono state seguite solo quanto necessario a distinguere il processo renewal dalle orbite aritmetiche; nessun audit globale è rivendicato.
