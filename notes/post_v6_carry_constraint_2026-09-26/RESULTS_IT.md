# Il riporto futuro è un vincolo lineare, ma non controlla il peso delle parità

**26 settembre 2026. Esito:** il vincolo aritmetico è stato ricavato
esattamente, e il suo possibile uso come certificato di parità viene
respinto al livello 16. Il **281º candidato** nell'ordine congelato
conserva il prefisso inferiore completo, tutti i bit alti e il riporto
futuro della sorgente effettiva, ma ha **Delta=31.168**, contro il
bersaglio **512**. Il margine passa da **+1.155 a −28.858**.

La torre effettiva ha invece `Delta_16(Q_16)=−479` e margine superiore
`+2789`. Il controesempio riguarda una classe di completamenti, non
`Q_16` o Collatz. Non viene calcolato un nuovo livello della torre,
aggiunto un teorema Lean o rivendicata originalità matematica.

## 1. Il passaggio quantitativo ottenuto

La [fase precedente](../post_v6_binary_carries_2026-09-26/RESULTS_IT.md)
aveva mostrato selettività finita del riporto futuro. Ora quel vincolo
è scritto come una sola disuguaglianza lineare sui bit liberi.
Poniamo `r=v+3`, `H=H_v`, `K=H_(v+1)`, `N=r+K`, con `K<=2H`.
Fissato `u=Q_v mod2^H`, scriviamo

\[
X=u+2^Ht+2^Kh,\qquad P_0=1+2^ru,\qquad
t=\sum_{j<K-H}t_j2^j.
\]

Per la convoluzione troncata
`F_N(P)=sum_(i+j<N) bit_i(P)*bit_j(P)*2^(i+j)`, il riporto è
`C_N(P)=floor(F_N(P)/2^N)`. Due bit liberi hanno posizioni troppo
alte per contribuire sotto N; resta quindi esattamente

\[
F_N(1+2^rX)=F_N(P_0)+\sum_{j<K-H}t_jW_j,
\quad W_j=2^{r+H+j+1}(P_0\bmod2^{K-H-j}).
\]

Ne segue l'equivalenza

\[
\boxed{C_N(1+2^rX)=c\quad\Longleftrightarrow\quad
c2^N\le F_N(P_0)+\sum_jt_jW_j<(c+1)2^N.}
\]

I bit da K in su non intervengono. I pesi normalizzati sono
`W_j/2^N=2*(P_0 mod2^(K-H-j))/2^(K-H-j)`, tutti fra zero e due.
È una restrizione quantitativa sui bit della **sorgente**, ricavata
senza usare il conteggio shortcut da maggiorare. Quel conteggio è una
diversa funzione degli stessi bit: il passaggio dalla restrizione al
bersaglio di parità è precisamente ciò che il controesempio respinge.
Le [prove complete](PROOF_IT.md) includono anche la decomposizione
del riporto ancorato e gli algoritmi di inversione.

## 2. Protocollo e ricerca al livello 16

Il [protocollo](PROTOCOL_IT.md) e l'[elenco preliminare](presearch.json)
sono stati salvati prima di generare candidati al livello 16. La
famiglia deriva però da un sondaggio precedente ai livelli 5..12:
non si tratta di una preregistrazione cieca o pubblica. Il suo hash è
`9584df9345d36a838661fc1acfbfe5b238c58a86e1bd20a1488c1c4e2d7d5d9a`.

Si congela `v=16`, con

| Quantità | Valore |
|---|---:|
| `r` | 19 |
| Orizzonte inferiore `H` | 63.074 |
| Orizzonte superiore `K` | 126.147 |
| Frontiera del riporto `N` | 126.166 |
| Bit liberi `K-H` | 63.073 |
| Riporto effettivo richiesto | 31.655 |
| Bersaglio `g(16)` | 512 |
| Candidati distinti nell'elenco | 988 |

Si mantiene il prefisso superiore effettivo di lunghezza H. Il suffisso
viene posto tutto uno; seguono parole con uno zero in 512 posizioni
equispaziate e con due zeri speculari, eliminando i duplicati. Il
residuo superiore viene invertito attraverso `f_16`; si ripristinano
poi tutti i bit della sorgente da K in su. Positività, disparità,
binade e parola inferiore completa vengono conservate.

L'arresto era fissato al primo candidato con riporto corretto e
`Delta>512`, oppure all'esaurimento. È avvenuto al candidato di indice
280, dopo **281 verifiche su 988**. Non sono stati enumerati gli
altri candidati: un testimone basta per respingere l'implicazione.
L'ordine è deterministico e non dà una stima della frequenza dei fallimenti.

## 3. Testimone e confronto con la torre

Il suffisso superiore del testimone è tutto uno, salvo **uno zero alla
posizione assoluta 97.510**, indicizzata da zero. Il prefisso superiore
di lunghezza H contiene 31.322 uno; quindi il totale superiore è
`31322+(63073-1)=94394`.

| Dato | Sorgente alternativa | Torre effettiva |
|---|---:|---:|
| Passi dispari inferiori | 31.613 | 31.613 |
| Passi dispari superiori | 94.394 | 62.747 |
| Riporto futuro | **31.655** | **31.655** |
| Difetto `J_U-2J_L` | **31.168** | **−479** |
| Margine inferiore | +1.155 | +1.155 |
| Margine superiore | **−28.858** | **+2.789** |

La sorgente alternativa ha 207.726 bit, la stessa binade di `Q_16`,
lo stesso residuo modulo `2^63074` e gli stessi bit da 126.147 in su.
Gli interi esatti `X` e `Y=f_16(X)`, le parole complete e gli hash
sono nel [risultato archiviato](carry_constraint_results.json).
La parola inferiore ha hash
`86cb17b586a676c6c1529c082ca99d6d0bab52faaea7126fda430469e1870e03`,
quello della parola superiore alternativa è
`f2661d2418869d1b24a1479f17e28c221067543ba9d4e3daa6354f7211a7d8db`.

Il bilancio dei margini è esatto:
`2*1155-31168=−28858`. Il testimone respinge quindi anche il
trasferimento del solo segno del margine sulla stessa classe,
oltre al bersaglio più restrittivo `Delta<=512`.

La verifica non impone la cascata completa dal seme 3, antenati interi
o congruenze ternarie aggiuntive. Non si estende a un filtro che imponga
quelle altre condizioni. Il punto esatto della torre resta distinto.

## 4. Come il riporto e la costruzione sono verificati

Il programma certifica il riporto dalle ultime colonne usando il limite
universale `0<=C_n<=n-1`. Se un blocco di B colonne dà somma pesata S,
il riporto finale appartiene all'intervallo intero

\[
\left[\left\lfloor S/2^B\right\rfloor,
\left\lfloor(S+\max(N-B-1,0))/2^B\right\rfloor\right].
\]

Si accetta il valore soltanto quando i due estremi coincidono. Per il
testimone bastano **19 colonne**, per la sorgente effettiva 38; entrambi
gli intervalli si riducono a `{31655}`. Questo è un certificato esatto
del riporto, non un'approssimazione probabilistica. Il valore viene
ricontrollato con la disuguaglianza lineare su tutti i bit liberi e
con una convoluzione indipendente nei test.

I residui delle parole con pochi zeri hanno una formula chiusa. Se il
prefisso di lunghezza H ha dati affini `(a,A)`, il completamento tutto
uno richiede
`y_*=-(A+2^H)*3^(-a) mod2^K`. Con uno zero in posizione H+s,
il residuo è `y_*-2^(H+s)*3^(-a-s) mod2^K`. L'inverso quadratico
viene calcolato con Newton, insieme all'inverso della derivata. Queste
formule sono provate su carta e controllate contro tutti i residui
su piccoli domini. Le parità del testimone sono poi riprodotte anche
per iterazione diretta degli interi completi.

Le cinque piccole fibre della fase precedente, **33.046 completamenti**,
sono ricontrollate interamente: la formula lineare e il riporto rapido
coincidono con tutti i valori e le distribuzioni congelati. I tre
testimoni preliminari ai livelli 5..7 vengono documentati come
esplorativi, senza convertirli in validazione prospettica.

## 5. Decisione e confine rimasto

Il riporto futuro è una restrizione reale sui bit, ma **questa singola
restrizione, con prefisso completo e altezza corretta, non produce il
bilancio di parità cercato**, già al livello dove era ancorato il
bersaglio uniforme. Non si aumenta il numero dei riporti o si modifica
la soglia dopo il fallimento di questo test.

La forma lineare resta utile per descrivere esattamente ciò che il
filtro ammette. Per un tentativo positivo serve una proprietà della
generazione esatta che controlli la trasformazione da bit di sorgente
a parità, con un costo cumulativo indipendente. L'uguaglianza di un
altro dato selettivo non può essere assunta automaticamente sufficiente.
La disuguaglianza sui soli punti `Q_v` e la discesa uniforme rimangono
aperte. Questa fase non aggiunge un bilancio uniforme.

## Riproduzione

Dalla radice del repository:

```sh
python3 notes/post_v6_carry_constraint_2026-09-26/test_carry_constraint.py
python3 notes/post_v6_carry_constraint_2026-09-26/carry_constraint_probe.py --output /tmp/carry_constraint_results.json
cmp notes/post_v6_carry_constraint_2026-09-26/carry_constraint_results.json /tmp/carry_constraint_results.json
```

Il [manifesto](verification_manifest.json) registra hash, log e controlli
locali. La [revisione interna](REVIEW_IT.md) separa le prove aritmetiche,
la verifica del testimone e i quantificatori. I motori modulari e affini
sono riusati con sorgenti vincolate da hash; il replay dello stesso
codice non è un ulteriore metodo indipendente. Il workflow CI è
predisposto; non viene rivendicata una nuova CI riuscita, build Lean,
formalizzazione delle prove su carta o revisione umana esterna.

I **nove test passano localmente**, incluso il quadrato impacchettato
che normalizza tutte le 126.166 colonne per entrambe le sorgenti.
