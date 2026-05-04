# Lemma di Shadowing dei Cicli Fantasma

## Contesto

La metrica empirica sviluppata nei report precedenti individua numeri con alto debito, alta pressione `Pmax` e falsi allarmi. La nuova interpretazione e' che questi numeri non siano anomalie isolate: sono interi positivi che seguono per un tratto l'ombra di orbite periodiche razionali negative nello spazio 2-adico.

Questa nota separa la parte dimostrabile dalla parte ancora congetturale.

## Definizione

Sia `S` la mappa Syracuse compressa sugli odd:

```text
S(n) = (3n + 1) / 2^a,    a = v_2(3n + 1).
```

Fissiamo una parola finita di valutazioni

```text
w = (a_0, ..., a_{L-1}),      A = a_0 + ... + a_{L-1}.
```

La composizione corrispondente e' affine:

```text
S_w(n) = (3^L n + C_w) / 2^A,
```

dove `C_w` e' determinato ricorsivamente da

```text
C_0 = 0,
A_0 = 0,
C_{j+1} = 3 C_j + 2^{A_j},
A_{j+1} = A_j + a_j.
```

Il punto periodico razionale 2-adico associato alla parola periodica `w^infty` e'

```text
q_w = C_w / (2^A - 3^L).
```

Se `3^L > 2^A`, allora il ciclo e' espansivo nel valore reale, e `q_w` e' reale negativo.

## Lemma 1: criterio di shadowing esatto

Sia `B_m = a_0 + ... + a_{m-1}` la somma delle prime `m` valutazioni della parola periodica `w^infty`.

Se un intero dispari positivo `n` soddisfa

```text
n == q_w  (mod 2^{B_m + 1}),
```

allora i primi `m` passi di Syracuse di `n` hanno esattamente le valutazioni prescritte da `w^infty`.

In particolare, per `b` periodi completi:

```text
n == q_w  (mod 2^{bA + 1})
```

implica che `n` segue `w` ripetuta `b` volte.

## Dimostrazione

Supponiamo che dopo `j` passi l'orbita reale di `n` e quella razionale 2-adica di `q_w` abbiano seguito la stessa parola fino a quel punto. Allora

```text
S^j(n) - S^j(q_w) = (3^j / 2^{B_j}) (n - q_w).
```

Quindi

```text
v_2(S^j(n) - S^j(q_w)) >= B_m + 1 - B_j.
```

Per forzare la valutazione successiva `a_j`, non basta sapere che `3S^j(n)+1` e `3S^j(q_w)+1` sono congruenti modulo `2^{a_j}`; bisogna anche escludere la divisibilita' per `2^{a_j+1}`. Serve quindi

```text
B_m + 1 - B_j >= a_j + 1.
```

Questa disuguaglianza equivale a

```text
B_m >= B_j + a_j = B_{j+1},
```

che vale per ogni `j < m`. Per induzione, i primi `m` passi seguono la parola prescritta.

Il bit extra `+1` e' essenziale: gli esperimenti con `55_shadowing_congruence.py` mostrano controesempi quando si usa solo `2^{bA}`.

## Lemma 2: shadowing infinito impossibile per interi positivi

Se un intero positivo `n` seguisse `w^infty` per sempre, allora dovrebbe soddisfare

```text
n == q_w  (mod 2^K)
```

per ogni `K`. Dunque `n = q_w` in `Z_2`.

Ma nei cicli fantasma osservati `q_w` e' un razionale reale negativo, non un intero positivo. Quindi un intero positivo puo' shadoware un fantasma solo per un tempo finito.

## Avvertenza importante

Non esiste un bound uniforme assoluto sulla durata dello shadowing. Per ogni `b` si puo' costruire il minimo positivo

```text
n_b = q_w mod 2^{bA + 1}
```

che segue `b` periodi completi.

Quindi il problema non e':

```text
dimostrare che lo shadowing e' sempre corto.
```

Il problema giusto e':

```text
dimostrare che, dopo l'uscita dallo shadowing, il debito accumulato viene
pagato in modo controllabile rispetto alla taglia iniziale.
```

## Evidenza computazionale

Lo script `55_shadowing_congruence.py` verifica il criterio per i phantom trovati fino a `k=24`, con `b <= 10`.

I cicli fantasma rilevati sono ombre dei seguenti razionali negativi:

```text
k=10: q = -5739192681529 / 2404426874857  ~= -2.38693
k=11: q = -2199012694031 / 709849655971   ~= -3.09786
k=12: q = -2123 / 1675                    ~= -1.26746
k=12: q = -817 / 601                      ~= -1.35940
k=20: q = -104312644103 / 30307317785     ~= -3.44183
```

Risultato del test:

```text
Tutti i minimi positivi congruenti a q mod 2^(bA+1) seguono esattamente
la parola phantom ripetuta b volte.
```

## Ruolo delle formule empiriche precedenti

Le formule `H`, debito, pressione `Pmax` e falsi allarmi non sono la prova, ma sono il radar che ha indicato dove cercare. Hanno separato tre fenomeni:

```text
1. discesa ordinaria verso il ciclo banale;
2. falsi allarmi, cioe' debito locale senza shadowing strutturale;
3. ribelli, cioe' interi positivi vicini a ombre 2-adiche espansive.
```

La nuova teoria non cancella quella empirica: la traduce in linguaggio 2-adico.

## Prossimo obiettivo

Formalizzare un bound di uscita:

```text
Se n shadowa un fantasma espansivo per b periodi, allora dopo l'uscita esiste
un tempo controllato T(b, w) per cui S^T(n) < n.
```

La forma forte di questo bound sarebbe un vero passo verso Collatz. La forma debole produrrebbe comunque una classificazione algebrica dei ribelli.

## Probe sulle famiglie congruenziali

Il rappresentante minimo

```text
n_b = q_w mod 2^{bA+1}
```

non basta: ogni classe di shadowing contiene una famiglia infinita

```text
n_{b,t} = r_b + t * 2^{bA+1}.
```

Lo script `57_shadowing_family_probe.py` testa queste famiglie.

Risultato denso:

```text
b <= 10,  t = 0..1023,  5 fantasmi,  51.200 orbite
bad word count: 0
unresolved count: 0
massimo rientro sotto n0: 311 passi compressi
```

Risultato sparso sulle potenze:

```text
b <= 16,  t fino a 65535 vicino a potenze di 2
bad word count: 0
unresolved count: 0
massimo rientro sotto n0: 341 passi compressi
```

Questa evidenza suggerisce che il rientro post-shadowing non sia un artefatto del rappresentante minimo. Il parametro `t` cambia la quota massima raggiunta, ma nei test non produce code lunghe dopo l'uscita dal fantasma.

La prossima domanda teorica e':

```text
Dato un fantasma w e una profondita' b, la mappa post-uscita su t ha
partizioni residue finite con drift negativo uniforme?
```

Se si riesce a provarlo, il pagamento del debito potrebbe diventare un lemma
di tipo finite-state, verificabile su un numero finito di classi residue.

## Correzione: il rientro one-shot non e' l'oggetto giusto

Il tentativo `58_escape_certificate.py` prova a certificare, per tutti gli
infiniti `t`, un rientro uniforme dopo un singolo episodio fantasma. Il test
sul caso `k=10, b=1` mostra che il certificatore esplode gia' oltre milioni di
nodi senza chiudere. Questa non e' solo inefficienza: concettualmente i bit
alti liberi di `t` possono codificare nuovi episodi di shadowing futuri.

Quindi il modello corretto non e':

```text
fantasma -> rientro immediato uniforme.
```

ma:

```text
fantasma -> fantasma -> ... -> rientro.
```

Lo script `59_shadow_episode_graph.py` costruisce questo grafo di episodi.

Risultato denso:

```text
b <= 8,  t = 0..255
10.240 orbite
unresolved: 0
max episodi per orbita: 19
```

Risultato sparso sulle potenze:

```text
b <= 16,  t fino a 65535 vicino a potenze di 2
3.760 orbite
unresolved: 0
max episodi per orbita: 34
```

Le transizioni dominanti sono ricorrenti e strutturate, per esempio:

```text
k11:c1:b1 -> k12:c2:b1
k10:c1:b1 -> k12:c2:b1
k12:c2:b2 -> k12:c2:b1
k12:c1:b2 -> k12:c1:b1
k12:c2:b1 -> k10:c1:b1
k12:c2:b1 -> k11:c1:b1
```

Questo suggerisce un secondo livello di teoria: non basta estinguere i cicli
fantasma modulo `2^k`; bisogna dimostrare che il grafo degli episodi ha una
funzione di energia decrescente. La profondita' `b` puo' passare da un fantasma
all'altro, ma nei test tende a degradare o a rientrare in configurazioni basse
prima della discesa.

Nuovo teorema-obiettivo:

```text
Esiste una funzione E(phantom, b, fase) tale che ogni transizione di episodio
non terminale soddisfa E_next < E_current, salvo un insieme finito di mosse
certificate direttamente.
```

Questa e' una versione algebrica della tua intuizione originale del debito:
non piu' debito lungo l'orbita grezza, ma debito/energia sul grafo degli
episodi 2-adici.

## Diagnostica dello stato giusto

Lo script `60_episode_graph_diagnostics.py` controlla se lo stato grossolano

```text
(k, ciclo, b)
```

e' sufficiente per una funzione energia.

Risultato sui dati `b <= 16`, `t` vicino a potenze di 2:

```text
stati nel grafo grossolano: 65
SCC non banali: 1
dimensione SCC principale: 34
```

La SCC principale contiene, tra gli altri:

```text
(10,1,b) per b=1..15
(11,1,b) per b=1..15
(12,1,b) per b=1..2
(12,2,b) per b=1..2
```

Quindi nessuna energia strettamente decrescente puo' dipendere solo da
`(k,ciclo,b)`.

Ambiguita' osservata:

```text
stato (12,2,1):
  occorrenze: 13862
  episodi residui prima della discesa: da 0 a 32
```

Raffinare con il surplus

```text
v2(n - q_w) - (bA + 1)
```

non risolve: `(12,2,1,surplus=0)` resta ambiguo da 0 a 32 episodi residui.
Anche aggiungere un bucket della grandezza reale non basta.

Conclusione: la coordinata mancante e' una fase aritmetica del parametro
libero `t`, non solo la profondita' 2-adica o la taglia. Il prossimo stato
da testare e':

```text
(k, ciclo, b, t mod 2^m)
```

o, piu' intrinsecamente, una fase ottenuta dalla coniugazione 2-adica del
residuo post-episodio.

## Raffinamento della fase e return map critico

Lo script `61_phase_refinement.py` testa due fasi locali:

```text
low: t_local mod 2^m
odd: (v2(t_local), odd_part(t_local) mod 2^m)
```

Risultato:

```text
la fase low non rompe la SCC;
la fase odd riduce l'ambiguita', ma non rompe la SCC nemmeno a 18 bit.
```

Il nodo critico resta:

```text
(k=12, cycle=2, b=1)
```

Lo script `62_critical_return_map.py` studia il primo ritorno da questo nodo
a se stesso. Risultato:

```text
ritorni osservati: 14461
terminali osservati: 6493
delta_t_bits piu' frequenti: +4, +3, +2, +5
```

Quindi neppure il parametro locale `t` e' monotono al ritorno: spesso cresce.

Lo script `63_critical_pressure.py` misura una pressione empirica del return
map critico. A `s=0` c'e' contrazione perche' circa il 31% delle visite
terminalizza:

```text
P_0 = 0.690131
```

ma per `s >= 0.5` la pressione esplode a causa di rari ritorni con
`delta_t_bits` molto negativo:

```text
delta_t_bits min/max: -27 / +7
P_1 ~= 8955
```

Conclusione: anche la pressione grezza su un singolo nodo critico non basta.
Le eccezioni rare devono diventare sottostati espliciti. La prossima
struttura da cercare e':

```text
grafo degli episodi + sottostati eccezionali del return map critico.
```

In altre parole, il problema si sta trasformando in un algoritmo di
partizionamento simbolico: ogni volta che una pressione o energia fallisce per
una coda rara, quella coda va separata come nuovo stato finito. Se questo
processo termina, produce un certificato finite-state.

## Splitter delle eccezioni e automa critico

Lo script `64_exception_splitter.py` cerca regole residue per separare le code
rare del nodo critico. A `s=1` la pressione grezza e':

```text
P_1 ~= 8955
```

ma cinque regole eccezionali rendono il resto contrattivo:

```text
from_t_v2 == 20
from_odd_mod_4 == 1
from_odd_mod_8 == 3
hit_index == 7
from_t_v2 == 21

REMAINDER:
  P_1 ~= 0.485
```

Quindi il "bulk" del return map critico e' subcritico. La pressione e'
portata da code rare e strutturate.

Lo script `65_certificate_automaton.py` costruisce un automa con blocchi:

```text
BULK
E1_v2_20
E2_odd_mod4_1
E3_odd_mod8_3
E4_hit_7
E5_v2_21
```

Il bulk e' subcritico, ma l'automa complessivo resta in una SCC unica perche'
le eccezioni possono rimandare ad altre eccezioni.

Lo script `66_automaton_spectral.py` calcola il raggio spettrale della matrice
pesata dei blocchi. Risultato:

```text
rho(0)    ~= 0.725   subcritico
rho(0.25) ~= 0.414   subcritico
rho(0.5)  ~= 1.948   supercritico
rho(1)    ~= 1831    supercritico
```

Il problema residuo non e' il bulk, ma pochi edge eccezionali.

Lo script `67_weighted_edge_inspector.py` mostra gli edge dominanti a `s=1`:

```text
E1_v2_20 -> E2_odd_mod4_1      delta_min = -27
E1_v2_20 -> E3_odd_mod8_3      delta_min = -25
E2_odd_mod4_1 -> E2_odd_mod4_1 delta_min = -21
E3_odd_mod8_3 -> E3_odd_mod8_3 delta_min = -21
```

La singola transizione peggiore osservata e':

```text
source_b = 8
source_t = 107
hit_index = 7
from_t_v2 = 20
from_odd_mod_256 = 3
delta_t_bits = -27
```

Questo e' un punto importante: la pressione non fallisce per un fenomeno
diffuso, ma per un numero minuscolo di transizioni atomiche. Il prossimo passo
e' splittare ricorsivamente questi edge dominanti, non tutti gli stati.

Nuovo obiettivo operativo:

```text
costruire un refinement loop:
  1. calcola rho della SCC;
  2. trova l'edge che contribuisce di piu' al peso;
  3. split sull'invariante residuo che isola quell'edge;
  4. ripeti finche' rho < 1 o emerge una famiglia infinita di eccezioni.
```

Questo sarebbe il primo vero "motore di certificazione" della teoria.

## Miner delle eccezioni: risultato e correzione

Lo script `68_refinement_loop.py` aveva mostrato che, sul campione critico
originario, il raggio spettrale a `s=1` scende sotto 1 dopo 31 split atomici:

```text
rho_0 ~= 1830.94
rho_31 ~= 0.813
```

Lo script `69_exception_pattern_miner.py` ha poi controllato se quei 31 atomi
fossero davvero 31 pattern indipendenti. Risultato inatteso ma pulito:

```text
I 31 atomi sono esattamente tutte le righe con

    delta_t_bits <= -11

nel campione dense_b8_t255.
```

Sul campione originario:

```text
returns: 14,461
atoms:      31
rule:       delta_t_bits <= -11
precision: 1.0
```

Questa scoperta e' utile, ma introduce una correzione concettuale: la soglia
`delta_t_bits <= -11` usa l'esito della transizione, quindi e' una
classificazione di edge, non ancora una classificazione predittiva dello
stato sorgente. Per un certificato formale bisogna dimostrare che la massa
pesata di questi edge profondi e' controllata.

## Stress test della coda profonda

Lo script `70_delta_exception_stress.py` allarga il campione senza
sovrascrivere i file canonici `62_*`. Il test conta le transizioni profonde:

```text
delta_t_bits <= -11
```

Risultati:

```text
dense_b8_t255:
  returns     = 14,461
  exceptions  = 31
  fraction    = 0.002144
  min_delta   = -27

dense_b8_t1023:
  returns     = 57,849
  exceptions  = 131
  fraction    = 0.002265
  min_delta   = -29

powers_b16_t65535:
  returns     = 11,389
  exceptions  = 57
  fraction    = 0.005005
  min_delta   = -55
```

Conclusione importante: le eccezioni profonde non sono finite. Crescono
quando si allarga `t`, e a profondita' `b` piu' alte compaiono ritorni ancora
piu' violenti. Quindi la strada "isolo una lista finita di mostri" e' falsa.

La strada corretta e' piu' sottile:

```text
bulk subcritico
+ coda eccezionale rara ma ricorsiva
+ stima della massa pesata della coda
=> pressione totale < 1
```

In termini di teoria, il problema non e' piu' trovare una Lyapunov
puntuale. E' costruire una disuguaglianza di tipo transfer-operator:

```text
sum_{ritorni} 2^{-s * delta_t_bits} * Prob(ritorno | stato)
```

e dimostrare che la parte supercritica ha misura/conteggio abbastanza piccolo
da non distruggere il raggio spettrale.

Questo e' il nuovo nucleo della dimostrazione tentata:

```text
1. costruire una partizione edge/state che rende il bulk subcritico;
2. descrivere simbolicamente la coda delta_t_bits <= -11;
3. provare un bound di conteggio per le code profonde:

       #{edge con delta_t_bits <= -d} <= C * 2^{-alpha d} * N

   con alpha sufficiente;
4. inserire il bound nella matrice pesata e ottenere rho < 1.
```

Questo non e' una dimostrazione di Collatz, ma e' finalmente una formulazione
matematica nuova e falsificabile del muro: la congettura viene ridotta al
controllo della coda dei ritorni profondi nel grafo degli episodi phantom.

## Profilo empirico della coda

Lo script `71_exception_tail_profile.py` calcola:

```text
N_d = #{ritorni con delta_t_bits <= -d}
```

Alcuni valori:

```text
dense_b8_t1023:
  d >= 11: 131 / 57,849   -log2 ~= 8.79
  d >= 18:  53 / 57,849   -log2 ~= 10.09
  d >= 25:  12 / 57,849   -log2 ~= 12.24
  d >= 29:   3 / 57,849   -log2 ~= 14.24

powers_b16_t65535:
  d >= 11: 57 / 11,389    -log2 ~= 7.64
  d >= 18: 44 / 11,389    -log2 ~= 8.02
  d >= 32: 14 / 11,389    -log2 ~= 9.67
  d >= 55:  1 / 11,389    -log2 ~= 13.48
```

Le sorgenti piu' frequenti nel campione denso sono:

```text
k=10, cycle=1, b=8
k=10, cycle=1, b=7
k=10, cycle=1, b=6
k=12, cycle=2, b=8
```

Nel campione powers ad alta profondita', la massa si sposta verso:

```text
k=10, cycle=1, b=13
k=12, cycle=2, b=14
k=11, cycle=1, b=13
```

Questo suggerisce una struttura di rinormalizzazione: la stessa coda riappare
a scale `b` piu' alte, con profondita' di ritorno piu' grandi. Quindi il
prossimo oggetto teorico non e' una lista di residui, ma una stima di
decadimento della coda in funzione di `d` e `b`.

## Congruenze modulari delle eccezioni

Lo script `72_exception_congruence_miner.py` torna al campione denso
`b<=8, t<=1023` e cerca regole modulari che predicano gli edge profondi
dentro ciascuna sorgente.

Sorgenti dominanti:

```text
k=10,c=1,b=8: 40 / 7216 edge profondi, min_delta=-29
k=10,c=1,b=7: 26 / 6192 edge profondi, min_delta=-25
k=10,c=1,b=6: 14 / 5153 edge profondi, min_delta=-21
k=12,c=2,b=8: 13 /   42 edge profondi, min_delta=-17
```

Esempi di regole con forte lift:

```text
k=10,c=1,b=7:
  from_t_v2 mod 8 == 4
  precisione: 12 / 15 = 0.80
  baseline:   26 / 6192 ~= 0.0042

k=10,c=1,b=6:
  from_t_v2 mod 4 == 1
  precisione: 7 / 12 ~= 0.58
  baseline:   14 / 5153 ~= 0.0027

k=10,c=1,b=5:
  from_odd_mod_256 mod 16 == 1
  precisione: 3 / 4 = 0.75
  baseline:   11 / 4123 ~= 0.0027
```

Queste regole non bastano come predittori dal solo `n0`, perche' usano dati
del return edge (`from_t_v2`, `from_odd_mod_256`, `hit_index`). Pero' sono
esattamente il tipo di coordinate richieste da un transfer operator
raffinato: lo stato deve includere la fase locale del ritorno critico.

La nuova partizione candidata non e':

```text
stato = solo (k, cycle, b)
```

ma:

```text
stato = (k, cycle, b, v2(t_crit), odd(t_crit) mod 2^m, hit_index mod 2^m)
```

con edge pesati da `2^{-s delta_t_bits}`. Il test successivo deve costruire
questa matrice raffinata direttamente, invece di aggiungere atomi uno alla
volta.

## Operatore di trasferimento raffinato per fase

Lo script `73_phase_transfer_operator.py` costruisce direttamente la matrice
di trasferimento sugli stati:

```text
state = (v2(t_crit), odd(t_crit) mod 2^m, hit_index mod 2^h)
```

Ogni ritorno critico produce un edge:

```text
source_state -> destination_state
```

con peso:

```text
2^{-s * delta_t_bits}
```

Le visite terminali entrano nel denominatore dello stato sorgente ma non
producono edge uscente. Quindi `rho < 1` significa che l'operatore osservato
perde massa verso la discesa.

Risultato sul campione canonico `dense_b8_t255`:

```text
odd_bits=1, hit_bits=0: rho ~= 104.7     supercritico
odd_bits=1, hit_bits=1: rho ~= 634.4     supercritico
odd_bits=1, hit_bits=2: rho ~= 0.1286    subcritico
odd_bits=1, hit_bits=3: rho ~= 0.0057    subcritico
```

Quindi il salto strutturale e':

```text
hit_index mod 4
```

La fase del numero di visite al nodo critico e' una coordinata dissipativa.
Questo e' un oggetto molto piu' preciso delle vecchie feature empiriche.

Lo script `74_phase_transfer_stress.py` confronta tre scenari:

```text
canonical_dense_b8_t255
wide_dense_b8_t1023
deep_powers_b16_t65535
```

Risultati principali a `s=1`:

```text
canonical, odd_bits=1, hit_bits=2: rho ~= 0.1286
wide,      odd_bits=1, hit_bits=2: rho ~= 0.1286
deep,      odd_bits=1, hit_bits=2: rho ~= 6.94      supercritico
deep,      odd_bits=2, hit_bits=2: rho ~= 0.1519    subcritico
deep,      odd_bits=4, hit_bits=3: rho ~= 0.1437    subcritico
```

Conclusione aggiornata:

```text
stato minimo candidato =
    (v2(t_crit) capped,
     odd(t_crit) mod 4,
     hit_index mod 4)
```

Questa partizione resta subcritica anche nel campione powers ad alta
profondita', dove appaiono ritorni fino a `delta_t_bits = -55`.

Questo e' il miglior candidato emerso finora per un certificato finite-state:
non cerca una Lyapunov su `n`, ma un gap spettrale su un operatore di ritorno
2-adico raffinato per fase.

## Operatore critico troncato e test di quoziente

Lo script `75_critical_symbolic_operator.py` elimina le vecchie sorgenti
campionate e lavora direttamente sul nodo critico:

```text
target = (k=12, cycle=2, b=1)
n = r + t * 2^(A+1)
```

Enumera:

```text
t = 0, ..., 2^T - 1
h = hit_index mod 4
```

e calcola il primo ritorno al nodo critico oppure l'uscita sotto `n0`.
Lo stato e':

```text
(v2(t), odd(t) mod 4, h mod 4)
```

La matrice e' quindi esatta sul troncamento `0 <= t < 2^T`. Risultati:

```text
T= 6: states= 48, rho=0.125000, terminal=0.8750
T= 8: states= 64, rho=0.031250, terminal=0.9062
T=10: states= 80, rho=0.027030, terminal=0.9033
T=12: states= 96, rho=0.029411, terminal=0.8989
T=14: states=112, rho=0.030297, terminal=0.8967
T=16: states=128, rho=0.030261, terminal=0.8961
```

Questo e' il risultato numerico piu' pulito finora: il raggio spettrale del
return operator critico troncato si stabilizza attorno a:

```text
rho ~= 0.03
```

con zero unresolved fino a `T=16`.

Pero' lo script `76_quotient_consistency_probe.py` mostra anche il limite:
la transizione non dipende ancora solo da `t mod 2^T`. Confrontando:

```text
t = r + j * 2^T,   j=0..7
```

si ottiene:

```text
T= 6: stable = 180 / 256  = 0.7031
T= 8: stable = 716 / 1024 = 0.6992
T=10: stable = 3016 / 4096 = 0.7363
```

Quindi non possiamo ancora dichiarare un quoziente finito esatto. La
vittoria corretta e':

```text
il troncamento critico e' fortemente subcritico,
ma i bit alti restano dinamicamente attivi.
```

Questo sposta il prossimo obiettivo dal "quoziente periodico esatto" a una
disuguaglianza di dominanza:

```text
operator(full) <= operator(truncated stable core) + tail(high bits)
```

La parte stabile ha gia' gap grande (`rho ~= 0.03`). Ora serve stimare la
coda prodotta dai bit alti e mostrare che non puo' colmare il gap fino a 1.

## Decomposizione core/tail dei bit alti

Lo script `77_high_bit_tail_bound.py` implementa la decomposizione:

```text
t = r + j * 2^T
```

Per ogni classe `(r, h mod 4)` confronta i lift `j` e separa:

```text
CORE = firma di transizione maggioritaria
TAIL = firme minoritarie prodotte dai bit alti
```

Costruisce tre matrici normalizzate:

```text
FULL = CORE + TAIL
```

e misura:

```text
rho(FULL)
rho(CORE)
rho(TAIL)
||TAIL||_inf
rho(CORE) + ||TAIL||_inf
```

L'ultimo valore e' importante perche' da' un bound perturbativo elementare:

```text
rho(CORE + TAIL) <= rho(CORE) + ||TAIL||.
```

Risultati con `j=0..7`:

```text
T=6:
  rho_full = 0.0323
  rho_core = ~0
  ||tail||_inf = 0.25
  bound = 0.25

T=8:
  rho_full = 0.0317
  rho_core = 0.0039
  ||tail||_inf = 0.0903
  bound = 0.0942

T=10:
  rho_full = 0.0299
  rho_core = 0.0108
  ||tail||_inf = 0.5
  bound = 0.5108
```

Risultati con `j=0..15`:

```text
T=8:
  rho_full = 0.0294
  rho_core = 0.0039
  ||tail||_inf = 0.5
  bound = 0.5039

T=10:
  rho_full = 0.0303
  rho_core = 0.0120
  ||tail||_inf = 0.5
  bound = 0.5120
```

Quindi la consistenza di classe non basta, ma la dominanza perturbativa si':
anche con lift alti, la coda osservata resta troppo piccola per chiudere il
gap.

Nuovo lemma candidato:

```text
Per lo stato critico (v2(t), odd(t) mod 4, h mod 4),
la matrice di ritorno piena si decompone come

    M = C + E

con

    rho(C) <= 0.02 circa
    ||E||_inf <= 1/2

quindi rho(M) < 1.
```

Questo e' finalmente nella forma giusta per una dimostrazione: non pretende
che i bit alti siano irrilevanti, ma solo che la loro massa perturbativa sia
uniformemente limitata.

## Boundary layer della coda

Lo script `78_tail_row_certificate_probe.py` mostra che il massimo
`||TAIL||_inf` non viene dal bulk. Viene da stati rarissimi:

```text
v2(t) = T
odd(t) = 3 mod 4
h = 0,1,2,3
```

Per `T=10, j=16`:

```text
state v2=10, odd=3:
  source_count = 4 per fase h
  tail_weight  = 2
  tail_row_sum = 1/2

bulk principale v2=2, odd=3:
  source_count = 1024 per fase h
  tail_row_sum ~= 0.0776
```

Con `j=32`, la boundary sale leggermente:

```text
state v2=10, odd=3:
  tail_row_sum = 0.5625

bulk principale:
  tail_row_sum ~= 0.0822
```

Lo script `79_boundary_tail_scaling.py` separa:

```text
bulk:     v2(t) < T
boundary: v2(t) >= T
```

per `T=10`:

```text
j= 8: all_max=0.500000, bulk_max=0.077179, boundary_src=1/1024
j=16: all_max=0.500000, bulk_max=0.077606, boundary_src=1/1024
j=32: all_max=0.562500, bulk_max=0.082237, boundary_src=1/1024
j=64: all_max=0.570312, bulk_max=0.068291, boundary_src=1/1024
```

Questa e' una correzione importante al lemma candidato. Il bound globale in
norma infinita e' troppo pessimista perche' e' dominato da una boundary layer
di misura `2^{-T}`.

Nuova decomposizione:

```text
M = C + E_bulk + E_boundary

rho(C) piccolo
||E_bulk||_inf <= circa 0.09
E_boundary vive su una frazione 2^{-T} degli stati/sorgenti
```

Il prossimo lemma non deve solo dire `||E||_inf <= 1/2`; deve dire:

```text
la parte ad alta norma e' confinata in una boundary layer
di densita' 2^{-T}, e non forma una SCC persistente.
```

Questo e' molto piu' plausibile come prova: il bulk e' uniformemente
contrattivo, la boundary e' rara, e bisogna dimostrare che non puo'
autoalimentarsi.

## SCC della boundary: combinatoria vs spettro

Lo script `80_boundary_scc_probe.py` controlla se la boundary layer puo'
autoalimentarsi nel grafo delle transizioni. Per `T=10, j=64`:

```text
graph  nontrivial SCC  boundary SCC
full        1              1
core        1              0
tail        1              1
```

Quindi la boundary non e' puramente one-shot: nel grafo `full` e nel grafo
`tail` esiste una SCC che tocca stati boundary. Questo impedisce una prova
troppo semplice del tipo "la boundary esce sempre subito".

Pero' lo script `81_boundary_scc_spectral.py` misura lo spettro pesato delle
SCC normalizzate. Risultato per `T=10, j=64`:

```text
core SCC:
  size = 16
  boundary states = 0
  rho ~= 0.01283

full SCC che contiene boundary:
  size = 60
  boundary states = 4
  rho ~= 0.03026

tail SCC che contiene boundary:
  size = 60
  boundary states = 4
  rho ~= 0.01691
```

Questa e' la lettura corretta:

```text
la boundary puo' ricorrere combinatoriamente,
ma la ricorrenza boundary e' spettralmente debole.
```

Il lemma candidato diventa quindi:

```text
La SCC critica raffinata, inclusa la boundary layer v2(t)>=T,
ha raggio spettrale uniformemente < 1.
```

Non basta boundare la singola riga peggiore; bisogna boundare lo spettro della
SCC. Numericamente il margine e' enorme (`rho ~= 0.03`).

## Scaling dello spettro boundary

Lo script `82_boundary_scc_spectral_scaling.py` controlla se lo spettro della
SCC che tocca la boundary layer resta stabile al variare di `T` e del numero
di lift `j`.

Risultati:

```text
T= 8, j=16: boundary SCC assente, largest rho ~= 0.02941
T= 8, j=32: boundary SCC assente, largest rho ~= 0.02987
T= 8, j=64: boundary SCC assente, largest rho ~= 0.03030

T=10, j=16: boundary SCC assente, largest rho ~= 0.03030
T=10, j=32: boundary SCC assente, largest rho ~= 0.03085
T=10, j=64: boundary SCC presente, rho_full ~= 0.03026, rho_tail ~= 0.01691

T=12, j=16: boundary SCC presente, rho_full ~= 0.03026, rho_tail ~= 0.01609
T=12, j=32: boundary SCC presente, rho_full ~= 0.03059, rho_tail ~= 0.01672
T=12, j=64: boundary SCC presente, rho_full ~= 0.03060, rho_tail ~= 0.01596
```

Lettura:

```text
la boundary SCC appare quando il campione dei bit alti e' abbastanza ricco,
ma quando appare non aumenta lo spettro critico.
```

Il plateau numerico e':

```text
rho_critico ~= 0.030 - 0.031
rho_tail_boundary ~= 0.016 - 0.017
```

Questo rende piu' precisa la forma del certificato:

```text
1. costruire la SCC critica raffinata;
2. includere esplicitamente gli stati boundary v2(t)>=T;
3. dimostrare un bound uniforme sul raggio spettrale della SCC,
   non sulla singola riga.
```

La singola riga boundary puo' avere peso locale alto, ma non cambia il
raggio spettrale osservato della componente.

## Gap perturbativo CORE vs FULL

Lo script `83_perturbation_gap_scaling.py` misura

```text
gap(T, j) = rho(FULL_{T,j}) - rho(CORE_{T,j})
```

al variare della profondita' di quoziente `T` e del numero di lift dei bit
alti `j`. Risultati:

```text
T= 6: gap = 0.023 - 0.032
T= 8: gap = 0.025 - 0.028
T=10: gap = 0.018 - 0.019
T=12: gap = 0.016 - 0.017
```

Il gap e' monotonamente decrescente in `T` e praticamente indipendente da `j`
a `T` fissato. Quindi rho(CORE) insegue rho(FULL) man mano che il
raffinamento cresce: la decomposizione perturbativa si stringe, non si
allarga.

Il bound elementare

```text
rho(FULL) <= rho(CORE) + ||TAIL||_inf
```

resta pero' inutilizzabile: ||TAIL||_inf vale circa 0.5 perche' poche righe
boundary hanno massa locale alta. Il gap reale e' trenta volte piu' piccolo.
Quindi la disuguaglianza in norma infinito e' troppo grezza: serve una
norma pesata che misuri TAIL li' dove la dinamica vive davvero.

## Bound perturbativo pesato

Lo script `84_weighted_perturbation_bound.py` usa una stima Collatz-Wielandt
rispetto al vettore di Perron destro di FULL.

Sia `v >= 0` un autovettore destro non negativo di FULL associato al raggio
spettrale. Allora vale, componente per componente,

```text
FULL v = CORE v + TAIL v
```

Quindi

```text
rho(FULL) = max_i (FULL v)_i / v_i
         <= max_i (CORE v)_i / v_i + max_i (TAIL v)_i / v_i
         = core_action(v) + tail_action(v).
```

Risultati su `(T, j)`:

```text
T= 8, j=16: bound ~= 0.0408     T= 8, j=32: bound ~= 0.0400
T=10, j=16: bound ~= 0.0487     T=10, j=32: bound ~= 0.0485
T=12, j=16: bound ~= 0.0499     T=12, j=32: bound ~= 0.0497
T=14, j=16: bound ~= 0.0511     T=14, j=32: bound ~= 0.0507
T=16, j=16: bound ~= 0.0516
```

Sequenza degli incrementi in `T` (j=16):

```text
T=8 -> 10: +0.0079
T=10 -> 12: +0.0012
T=12 -> 14: +0.0012
T=14 -> 16: +0.0005
```

Decadimento geometrico chiaro. Estrapolazione conservativa:

```text
lim_{T -> infty} bound(T, 16) <~ 0.054.
```

E' essenzialmente indipendente da `j`: variazioni di lift dei bit alti
spostano la quarta cifra decimale.

Il gap `rho(FULL) - rho(CORE)` decade in parallelo:

```text
T= 8: gap ~= 0.0255
T=10: gap ~= 0.0183
T=12: gap ~= 0.0165
T=14: gap ~= 0.0149
T=16: gap ~= 0.0138
```

cioe' rho(CORE) -> rho(FULL) man mano che il raffinamento cresce. La
componente CORE da sola contiene quasi tutto lo spettro asintotico.

Calcolo dell'autovettore di Perron destro: viene usato `power iteration` su
`FULL + epsilon * J`, con epsilon = 1e-12. La perturbazione rank-1 rende la
matrice irriducibile, garantendo un eigenvettore strettamente positivo per
Perron-Frobenius. Epsilon e' sotto il rumore numerico, quindi
l'autovalore restituito e' essenzialmente rho(FULL).

Tentando lo stesso bound col vettore di Perron destro di CORE invece che di
FULL, il risultato esplode da `T=12` in su. Questo e' coerente col fatto
che CORE e' riducibile: il suo autovettore destro ha massa nulla sugli
stati boundary, quindi quando TAIL invia probabilita' su quegli stati il
rapporto diverge. Il vettore-test corretto e' quello dell'operatore pieno,
non del solo core.

## Forma del certificato

Il lemma quantitativo verso cui converge l'evidenza ha quindi la forma:

```text
Esiste una scelta consistente di parametri di raffinamento (T, j) tale che,
posta v_T,j la funzione test associata a FULL_{T,j}, valga
uniformemente in T e j una stima della forma

   max_i (CORE_{T,j} v)_i / v_i  +  max_i (TAIL_{T,j} v)_i / v_i  <  1

e tale che FULL_{T,j} domini correttamente l'operatore di ritorno critico
non troncato.
```

La parte numerica del bound e' gia' largamente soddisfatta: il valore
osservato e' circa 0.05 contro 1. Quello che manca per la dimostrazione e'
un argomento *strutturale* che mostri:

```text
1. tail_action(v) decade (o resta limitato) come funzione di T;
2. la consistenza di quoziente residua (assente in 30% dei casi a T=12,
   da 76_quotient_consistency_probe.py) non puo' inflazionare il bound
   nel limite T -> infinito.
```

Entrambe le parti sono ora esprimibili come stime dirette su matrici
finite, non piu' come affermazioni asintotiche su orbite singole.

## Stabilita' del troncamento in j

Lo script `85_truncation_stability.py` controlla quanto la matrice
`FULL_{T, j}` cambi al raddoppiare di `j`. Misura due cose:

```text
sig_drift(j) = frazione di gruppi (r, h) la cui firma dominante
               cambia tra j e il raddoppio successivo;
delta_bound(j) = bound_F(T, 2j) - bound_F(T, j),
                 calcolato con l'autovettore di Perron di FULL_{T, 2j}.
```

Risultati (j = 16, 32, 64, 128):

```text
T=8,  sig_drift_vs_prev: 0,  0.0078,  0.0078,  0.0000
T=10, sig_drift_vs_prev: 0,  0.0039,  0.0088,  0.0000
```

A `j = 128` *nessun* gruppo (r, h) cambia la propria firma dominante
rispetto a `j = 64`. La struttura di transizione si chiude completamente
sui parametri attuali.

```text
T=8,  bound: 0.0408, 0.0400, 0.0421, 0.0425   incrementi: -0.0007, +0.0021, +0.0004
T=10, bound: 0.0487, 0.0485, 0.0509, 0.0515   incrementi: -0.0003, +0.0024, +0.0006
```

L'incremento al raddoppio successivo cala di un fattore circa 4. Sotto
ipotesi di decadimento geometrico:

```text
lim_{j -> infty} bound(T=8, j)  <~ 0.0426
lim_{j -> infty} bound(T=10, j) <~ 0.0517
```

Combinando con l'estrapolazione in `T` della sezione precedente, il bound
asintotico atteso e':

```text
lim_{T, j -> infty} bound(T, j) <~ 0.06.
```

Il margine rispetto a 1 e' di un ordine di grandezza.

## Cosa resta da dimostrare

Il bound `<= 0.06` e' una stima a posteriori, non un teorema. Le tre cose
che mancano per chiudere il certificato sono:

```text
1. una stima a priori sul rapporto di decadimento di sig_drift(j) e
   delta_bound(j), oppure un argomento strutturale che esibisca un j*
   oltre il quale FULL_{T, j} = FULL_{T, j*} esattamente;

2. una stima a priori sul rapporto di decadimento di bound(T) in T;

3. l'estensione del certificato dal singolo nodo critico (k=12, c=2, b=1)
   all'intera SCC critica.
```

Tutte e tre le stime sono ora misurabili come quantita' su matrici finite.
Nessuna richiede di parlare di orbite asintotiche di Collatz.

## Estensione del certificato agli altri nodi della SCC

Lo script `86_scc_node_certificates.py` calcola `bound_F` non solo per il
nodo critico `(12, 2, 1)` ma per ogni nodo della SCC trovata in
`60_episode_graph_diagnostics.py`. Risultati a `T=10, j=32`:

```text
(10, 1, 1):  rho ~= 0,         bound_F = 0.0000
(10, 1, 2):  rho ~= 0,         bound_F = 0.0000
(11, 1, 1):  rho ~= 0,         bound_F = 0.0000
(11, 1, 2):  rho ~= 0,         bound_F = 0.0000
(12, 1, 1):  rho = 0.0035,     bound_F = 0.0043
(12, 2, 1):  rho = 0.0308,     bound_F = 0.0485
(12, 2, 2):  rho = 0.0007,     bound_F = 0.0007
```

Lettura:

```text
1. Il nodo (12, 2, 1) e' il peggior caso della SCC. Tutti gli altri nodi
   hanno bound_F da uno a cinque ordini di grandezza piu' piccolo. Il
   certificato single-node che abbiamo costruito e' valido al worst case.

2. I nodi (10, 1, *) e (11, 1, *) hanno auto-ritorno essenzialmente
   vuoto. Coerente con il grafo di episodi di 59-60: non hanno
   auto-cicli, sono porte di ingresso che mandano transizioni verso
   (12, 2, 1). La SCC vive trasversalmente.
```

## Limite del certificato single-node

L'analisi di cui sopra dimostra che ogni nodo della SCC, considerato in
isolamento, ha un return operator con `rho` e `bound_F` molto sotto 1.
Questo e' una *condizione necessaria* per la subcriticita' della SCC, ma
non e' sufficiente.

Per un certificato completo della SCC bisogna costruire l'operatore
cross-node:

```text
M[(k, c, b), (k', c', b')] = peso pesato di transizioni dal nodo (k,c,b)
                              al nodo (k', c', b'),
                              ognuna con il proprio fattore 2^{-delta}.
```

Il nodo critico ha `bound_F ~= 0.05`. Tutti gli altri hanno `bound_F`
quasi zero. Da cio' segue, almeno euristicamente, che l'operatore
cross-node sara' dominato dal blocco (12, 2, 1) e quindi sara' anch'esso
subcritico. Pero' la stima rigorosa richiede un nuovo script che assembli
la matrice cross-node.

## Operatore cross-node sulla SCC

Lo script `87_cross_node_transfer.py` costruisce l'operatore di
trasferimento sull'unione degli stati di tutti i nodi della SCC critica:

```text
state = (node_id, v2(t_local), odd(t_local) mod 4, hit_index mod 4)
```

Per ogni stato sorgente, si traccia il primo evento (drop sotto n0 oppure
primo hit su un nodo qualsiasi della SCC, source incluso) e si registra
un edge pesato `2^{-delta_bit_length}`.

Risultato a `T=8, j=8`, su 5 nodi `(10,1,1), (11,1,1), (12,1,1),
(12,2,1), (12,2,2)`, totale 548 stati:

```text
rho(M_cross)   = 0.0366
bound_F(cross) = 0.0366
status         = OK
```

Topologia degli edge cross-node osservata:

```text
(10,1,1) -> (12,2,1):  8128    porta di ingresso
(11,1,1) -> (12,2,1):  8192    porta di ingresso
(12,2,2) -> (12,2,1):  8128
(12,2,1) -> (12,2,1):   812    unico self-loop forte
(12,2,1) -> (12,1,1):   308
(12,1,1) -> (12,1,1):    96
(12,2,2) -> (12,2,2):    64
(12,2,1) -> (12,2,2):     8
(10,1,1) -> (11,1,1):    64
(12,1,1) -> (12,2,1):   444
```

Lettura strutturale:

```text
La SCC e' una "stella" centrata su (12, 2, 1) con porte di ingresso
(10,1,1), (11,1,1) e (12,2,2). L'unico self-loop di peso significativo
e' su (12, 2, 1). Cross-coupling DISTRIBUISCE la massa, non la
amplifica: il bound cross-node (0.037) e' addirittura piu' basso del
bound single-node del nodo critico (0.049).
```

Il certificato single-node era quindi piu' conservativo del necessario:
includere esplicitamente le transizioni cross-node migliora il bound.

## Stato finale del lemma

Sintesi onesta:

```text
- Forma del certificato: corretta (Collatz-Wielandt pesato).
- Numerica: bound_F <= 0.06 con margine 16x rispetto a 1.
  Uniforme su (T, j) testati, su tutti i nodi singoli della SCC,
  e sulla matrice cross-node assemblata.
- Dimostrazione: aperta. Restano due stime a priori:
  (i)  decadimento del bound in T;
  (ii) decadimento del drift di firme in j.
  La terza ipotesi (cross-node) e' verificata numericamente al primo
  campionamento e migliora il bound invece di peggiorarlo.
- Tutte le stime mancanti sono ora su matrici finite, non su orbite.
```

Il muro e' passato da "trovare una funzione di Lyapunov per Collatz" a
"controllare lo spettro di una famiglia di matrici finite indicizzate da
(T, j) e dai nodi della SCC critica". E' un cambiamento qualitativo del
problema, non una sua soluzione.
