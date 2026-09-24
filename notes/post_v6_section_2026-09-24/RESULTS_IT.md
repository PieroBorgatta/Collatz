# Continuazione dopo la v6: sezione marcata e torri parametriche

24 settembre 2026. Sviluppo successivo al deposito
[v6, DOI 10.5281/zenodo.22936057](https://doi.org/10.5281/zenodo.22936057).
Il PDF, lo ZIP e la copia del supplemento pubblicato sono conservati;
queste aggiunte appartengono al sorgente di lavoro.

**Verifica completata:** build integrale riuscita, 3365 job; audit di 13
teoremi principali con soli `propext`, `Classical.choice`, `Quot.sound`.
I cinque nuovi moduli non introducono `sorry`, `admit`, assiomi dichiarati
o `native_decide`. Dettagli in [lean_build.log](lean_build.log),
[axioms.log](axioms.log) e [verification_manifest.json](verification_manifest.json).

## Il risultato e il suo limite

La proposta della revisione è diventata un programma formale concreto:
un certificato aritmetico di copertura, una sezione di sei progressioni,
formule universali per torri di cancellazione e un'interfaccia precisa per
il problema dei ritorni. La congettura di Collatz rimane aperta: manca
un rango che controlli tutti i ritorni alla sezione.

La sufficienza della classe `20 mod 27` è un risultato classico di
[Monks et al., *Discrete Mathematics*, 2013, Teorema 6.4](https://doi.org/10.1016/j.disc.2012.11.019).
Non rivendichiamo di averla scoperta. Il contributo di questa continuazione
è un certificato esplicito con coefficienti piccoli, il collegamento esatto
agli episodi Syracuse e la loro integrazione con torri parametriche nella
biblioteca Lean. Non è stata stabilita una priorità bibliografica assoluta
per questa particolare formula del rango.

## 1. Un rango che garantisce l'arrivo, con un limite al tempo

Sia `T(n)=n/2` per n pari e `T(n)=(3n+1)/2` per n dispari. Fermiamo il
procedimento quando `n=1` oppure `n≡20 mod27`.

Per `r=n mod27`, poniamo

```
c(r) = 4   se r ∈ {8,17}
       7   se r ∈ {2,4,5,11,14,22,23}
      13   altrimenti.

R(n) = 1                 se r=13
       ν₂(n+1)+2         se r=26
       c(r)·n+3          altrimenti.
```

Se n e T(n) non sono terminali, `R(T(n))<R(n)`. Le transizioni regolari
sono controllate dai coefficienti 4, 7, 13. Il solo autoanello espansivo
nella classe 26 consuma esattamente un bit di `ν₂(n+1)` a ogni passo
dispari. Il passo pari da 26 porta a 13; da 13 si raggiunge 20 alla mossa
successiva, con entrambe le parità.

Ne segue un limite universale esplicito:

\[
\forall n>0\quad \exists k\le R(n)+1\le13n+4:
\quad T^k(n)=1\ \text{oppure}\ T^k(n)\equiv20\pmod{27}.
\]

Questo rango **non** deve diminuire oltre la condizione di arresto.
La sua esistenza non è una prova di terminazione a 1. È tuttavia un
prototipo completo del metodo proposto: controllo finito dei residui e
contatore non limitato per un episodio di crescita.

Fonte formale: `ShortcutCoverage.lean`, in particolare
`rank_decrease` e `exists_iterate_target_linear_bound`.
Il controllo indipendente `coverage_probe.py` verifica i 54 archi di
residuo/parità, un milione di sorgenti e contatori fino a 10.000 bit.
Lo script assegna rango zero ai terminali, variante equivalente del
certificato. Le verifiche finite sono controlli aggiuntivi, non la prova
dell'enunciato universale.

Lo stesso script ricostruisce i coefficienti, anziché limitarsi a
verificarli: risolve i vincoli interi `b(dest)≤b(source)+1` sugli archi
pari e `b(dest)≤b(source)−1` su quelli dispari. Un algoritmo di
Bellman–Ford sui 43 archi regolari produce livelli 0, 1, 2 e quindi
`c=3·2^b+1`. Le classi escluse 13, 20, 26 sono fornite dal progetto
matematico; il contatore non limitato per 26 è dimostrato separatamente.
È un piccolo prototipo riproducibile di sintesi, non un sintetizzatore
di ranghi globali per Collatz.

## 2. La sezione di sei progressioni e la sua ricorrenza

La sezione E è l'unione delle sei classi:

| Residuo | Modulo | Esponente rappresentante |
|---:|---:|---:|
| 13 | 18 | 1 |
| 53 | 72 | 3 |
| 853 | 1152 | 7 |
| 3413 | 4608 | 9 |
| 54613 | 73728 | 13 |
| 218453 | 294912 | 15 |

Per un dispari positivo u non divisibile per 3, `u∈E` equivale a dire
che l'episodio `(u,S(u)]`, **sorgente esclusa**, contiene un punto
`20 mod27`. La prova riduce qualsiasi esponente positivo modulo 18,
preservando la condizione di divisibilità; non impone un limite
alla valutazione vera `ν₂(3u+1)`.

La scomposizione esatta degli episodi trasferisce la copertura di T a S:
ogni orbita positiva dispari raggiunge 1 oppure E. Di conseguenza,
un'orbita che non raggiunge mai 1 incontra E a tempi accelerati
arbitrariamente grandi. Questa conclusione copre sia una divergenza sia
un eventuale ciclo non banale.

Fonti formali: `MarkedSection.section_iff_episodeHits20`,
`SectionCoverage.exists_accelerated_hit`,
`SectionReturn.recurrent_section_of_never_hits_one`.

## 3. Una famiglia di ritorni e un controesempio immediato

Per ogni intero `t≥0`,

\[
 S(661+1152t)=31+54t<661+1152t,
\]

con esponente esattamente 6 ed entrambi gli estremi nella prima classe
di E. È una famiglia infinita di ritorni decrescenti, verificata senza
enumerare un limite di t (`descending_return_family`).

Il primo ritorno non è sempre decrescente:

```
31 → 47 → 71 → 107 → 161 → 121.
 E                           E
```

I quattro valori intermedi non appartengono a E. Il teorema
`first_return_can_increase` esclude quindi il candidato più semplice:
il valore dell'intero come rango decrescente a ogni primo ritorno.

## 4. Torri universali: oltre le verifiche fino a k=2000

Per k pari almeno 4 si considera

\[
 n_k=(2^{k+1}-11)/3,\qquad S(n_k)=2^k-5.
\]

Posti `r=⌊(k−1)/3⌋` e `h=k−3r∈{1,2,3}`, seguono esattamente r blocchi
`[1,2]`, con estremo `2^h9^r−5`. Più generalmente, per `r≥1` e qualsiasi
cofattore pari `u≥2`, il blocco ripetuto porta `8^r u−5` a `9^r u−5`.

| h | Suffisso dopo i blocchi | Estremo dopo il suffisso |
|---:|---|---|
| 1 | `[3]` | `(3·9^r−7)/4` |
| 2 | `[1,1]` | `9^(r+1)−10` |
| 3 | `[1,4]` | `(9^(r+1)−5)/4` |

Per **ogni k pari almeno 30**, nessun passo dell'intera sequenza,
compreso il suffisso finale, scende sotto n_k. La lunghezza è `2r+2`
se h=1 e `2r+3` altrimenti. È un risultato universale sui parametri,
non l'estrapolazione dei 999 casi del precedente esperimento.

Il collegamento con E è esplicito:

\[
 n_{18t+10}\equiv13\pmod{18}.
\]

In particolare, per qualsiasi orizzonte B, la sorgente
`n_(18(B+2)+10)` appartiene a E e non scende nei primi B passi S.
`marked_sources_noDrop_for_any_horizon` rende questo ostacolo parte
della stessa sezione di cui è garantita la copertura.
L'estremo della sequenza descritta **non** è dichiarato un primo ritorno a E.
Non si rivendica un nuovo teorema generale sull'assenza di un limite
uniforme ai tempi di discesa, già illustrata dai lunghi prefissi di
esponenti 1. Il risultato specifico è il trattamento universale del
meccanismo di cancellazione della v6, con tutte le fasi e il suo
collegamento alla sezione coperta.

## 5. L'obbligo che rimane e la prossima ricerca

`SectionReturn.RankDescent R` richiede che, per ogni n in E, l'orbita
raggiunga 1 oppure esista un tempo realmente successivo k con

\[
 S^k(n)\in E,\qquad R(S^k(n))<R(n).
\]

Un tale rango a valori naturali implica Collatz, per induzione sul rango
e per la copertura appena ottenuta. La proprietà è ancora aperta: il
ponte esplicita l'obbligo, non ne diminuisce da solo la difficoltà.
Il teorema `exists_rankDescent_iff_acceleratedCollatz` dimostra anche
formalmente che l'esistenza di un rango con questa interfaccia equivale
alla congettura accelerata.
La discesa a un punto esterno a E non basta, perché il successivo
ingresso in E potrebbe essere più grande.

La ricerca ora può concentrarsi su un oggetto verificabile: famiglie di
transizioni fra i sei ingressi con parametri non limitati. Le torri vanno
compresse analiticamente; la fase h e le identità ternarie degli estremi
devono restare nello stato, invece di essere perse in un semplice conteggio
dei bit. Si può cercare un rango tramite vincoli aritmetici sulle famiglie
di transizioni, usando il piccolo certificato modulo 27 come prototipo
di sintesi riuscita. Il prototipo sui residui modulo 27 è realizzato;
la sua estensione alle famiglie di ritorni Syracuse resta da costruire.

I criteri minimi per accettare il prossimo risultato sono: dominio della
famiglia dimostrato, esponenti esatti, ritorno effettivo a E o raggiungimento
di 1, copertura dichiarata delle famiglie e discesa di un rango unico.
Una nuova tabella di esempi senza questi collegamenti non chiuderebbe
il problema emerso dalla v6.

## Riproduzione e affidabilità

I cinque nuovi moduli sono `ShortcutCoverage`, `MarkedSection`,
`SectionCoverage`, `CancellationTower`, `SectionReturn`. Build e audit
usano il pin esistente Lean/Mathlib 4.29.1. Il replay su una versione
corretta più recente, raccomandato nella revisione precedente, rimane
separato e non è stato eseguito qui.

Tutti e cinque sono importati dal target principale. La verifica finale
ha rielaborato i nuovi moduli e il target aggregato; le dipendenze
Mathlib provengono dalla cache della revisione fissata. Non è una
ricompilazione da zero dell'intera toolchain. Gli usi storici di
`native_decide` nella biblioteca precedente non vengono rimossi né
aggiunti da questa continuazione.

Il controllo offline dei sei PDF pubblicati è passato. Lo ZIP v6
conserva SHA-256
`20f9195443dd058aeae16b9316ed0f6beafb6d360182ba93b875107a0ee9da60`;
sono stati verificati anche manifesto e contenuti interni. Gli undici
artefatti della revisione precedente mantengono tutti i loro checksum.

```sh
cd lean
lake build
lake env lean ../notes/post_v6_section_2026-09-24/axioms.lean
python3 ../notes/post_v6_section_2026-09-24/coverage_probe.py
python3 ../scripts/check_published_pdfs.py
```

Sul Mac di questa sessione occorre anteporre
`DEVELOPER_DIR=/Library/Developer/CommandLineTools` ai comandi Lake:
altrimenti un errore di licenza Xcode in Git può indurre Lake a rimuovere
erroneamente la dipendenza mathlib prima del tentativo di riscaricarla.
