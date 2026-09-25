# Nota critica per una revisione matematica specialistica

25 settembre 2026. Documento preparatorio interno; non inviato a terzi.

Il progetto studia una famiglia specifica associata al problema di Collatz.
Scriviamo T(n)=n/2 sui pari e T(n)=(3n+1)/2 sui dispari; S indica la mappa
Syracuse, che rimuove tutte le potenze di due dopo 3n+1. Per v≥5 poniamo

\[
M=2^v,\qquad Q_v=\frac{3^{2M}-1}{2^{v+3}},\qquad
N_v=\frac{2^{3M-5}-11}{3}.
\]

L'obiettivo è una visita dell'orbita di Q_v sotto N_v per ogni livello.
Questa discesa uniforme non è dimostrata. I risultati seguenti distinguono
implicazioni formalizzate, argomenti su carta e verifiche finite; non viene
rivendicata originalità matematica.

**Parte formalizzata.** Il modulo
[DescentCertificate.lean](../../lean/CollatzShadowing/DescentCertificate.lean)
dimostra che, per x,N,k naturali con x,N>0, k<3N e somma effettiva A_k
degli esponenti Syracuse,

\[
3^{k+1}x<2^{A_k}(3N-k)
\quad\Longrightarrow\quad
\exists i\le k:\ S^i(x)<N.
\]

La prova controlla anche il termine additivo della dinamica. Il modulo
[QuadraticTransfer.lean](../../lean/CollatzShadowing/QuadraticTransfer.lean)
formalizza un trasferimento condizionale: per X,N,c,ℓ naturali con
X≥N>0, c≥1, Y=X+cX², w razionale positivo con wX<N e ℓ≤N,
la condizione c·w_ℓ(Y)≤96w², dove
w_ℓ(Y)=3^ℓ/2^{A_ℓ(Y)}, implica una visita sotto
96N²+704N+1287 entro ℓ. Queste implicazioni sono verificate da Lean;
non forniscono automaticamente le stime dinamiche richieste nelle premesse.

**Evidenza finita.** I [certificati modulari](../post_v6_certificates_2026-09-24/RESULTS_IT.md)
e la [fase successiva](../post_v6_compensation_2026-09-25/RESULTS_IT.md)
coprono i livelli 5–24. Certificano visite sotto N_v a partire da Q_v,
non primi tempi esatti né tempi di raggiungimento di 1. Per i livelli
22–24 due implementazioni, Python e C/GMP, concordano su conteggi,
testimoni ed hash delle intere parole di parità: 28.256.725 passi binari
complessivi. Una candidata sulla massima perdita intermedia, fissata prima
di questi tre livelli, supera i controlli ma resta congetturale. La verifica
dei programmi non è una formalizzazione Lean dei calcoli.

Il criterio globale attuale usa

\[
H_v=\left\lceil\frac{589\,2^v}{612}\right\rceil,\qquad
j_v=J_{Q_v}(H_v),\qquad m_v=2^{v-1}-j_v,
\]

dove J conta i passi dispari di T. Il margine m_v≥0 è sufficiente per
la discesa; il suo fallimento è inconcludente. Ai livelli 6, 7 e 9 sono
stati necessari certificati con un budget diverso. Definendo
Δ_v=j_{v+1}−2j_v, valgono esattamente

\[
m_{v+1}=2m_v-\Delta_v,\qquad
2^{-n}m_{v+n}=m_v-\sum_{i=0}^{n-1}2^{-i-1}\Delta_{v+i}.
\]

La [nota sui margini](../post_v6_margin_2026-09-25/RESULTS_IT.md) ricava
su carta un obiettivo sufficiente aperto:

\[
\Delta_v\le2\cdot2^{\lceil v/2\rceil}\quad\text{per ogni }v\ge16.
\]

Alla base 16, m_16=1155 e la somma pesata della maggiorazione futura è
1024: rimarrebbero 131 unità di margine normalizzato. Il limite passa
sulle coppie già osservate, ma è stato scelto retrospettivamente. Non è
dedotto da una distribuzione casuale delle parità, né da un teorema valido
su un insieme di densità uno.

**Ostacolo ai vincoli misti.** La ricorrenza esatta è
Q_{v+1}=f_v(Q_v), con f_v(X)=X+2^{v+2}X². La fattorizzazione della
differenza mostra che f_v è un'isometria 2-adica. Una classe inferiore
modulo 2^{H_v} lascia quindi libere tutte le code superiori compatibili
fino a K=H_{v+1}. Si possono scegliere code interamente dispari che
violano il budget superiore.

Il nuovo argomento su carta aggiunge molta precisione ternaria. Ponendo
e=2M e s=M/2=e/4, il teorema cinese dei resti consente di imporre
simultaneamente una classe avversaria X≡r modulo 2^K e X≡Q_v modulo
3^s. Il periodo P=2^K3^s è inferiore alla larghezza Z della binade
[Z,2Z) contenente Q_v, per ogni v≥6. Esiste dunque un rappresentante
nella stessa fascia d'altezza.

La stima è elementare: 3^4<2^7 implica 3^s<2^{7M/8}; per v≥7,
K≤2M e M/8≥v+3 danno P<2^{3M-v-3}≤Z. Il caso v=6 si controlla
separatamente. Non occorre alcuna ipotesi di equidistribuzione.

Con R=⌈log₂P⌉ possiamo conservare **tutti i bit nelle posizioni ≥R**,
con |X−Q_v|<2^R. Non conserviamo generalmente quelli nelle posizioni
≥K: imporli insieme alla classe modulo 2^K determinerebbe già X.
Inoltre

\[
1+2^{v+4}f_v(X)=(1+2^{v+3}X)^2,
\]

perciò anche il valore superiore coincide con Q_{v+1} modulo 3^{2s}.
Questo raddoppio della precisione ternaria non esclude gli esempi avversari.

Il risultato uniforme usa la classe inferiore artificiale X≡1 modulo
2^{H_v}, che ha margine positivo. Negli esempi finiti v=10 e v=12 si
conserva invece l'intera parola inferiore effettiva di Q_v: rispettivamente
512 e 2048 cifre ternarie, oltre a 450 e 1838 bit alti, sono compatibili
con margini +29→−426 e +93→−1841. Non si estende questa seconda
affermazione a tutti i livelli. Gli interi costruiti non sono Q_v.
Questi nuovi esempi sono controllati attraverso l'iterazione elementare
degli interi completi; la verifica C/GMP delle vecchie parole non viene
presentata come una verifica indipendente dell'intero nuovo procedimento.

La precisione necessaria a isolare Q_v deve essere distinta da un controllo
dinamico. Nella cella X≡Q_v modulo 2^{H_v}3^s, entro [Z,2Z), l'unicità
equivale a

\[
2^{H_v}3^s\ge\max(Q_v-Z+1,\,2Z-Q_v).
\]

Le soglie sono s=1418 e s=5695 nei due esempi; la costruzione avversaria
è garantita rispettivamente fino a 795 e 3207. Fra queste soglie non
affermiamo né esistenza né assenza generale di esempi avversari.

**Richiesta al revisore.** Cerchiamo una proprietà del punto speciale
1+2^{v+3}Q_v=3^e, con e=2^{v+1}, che discrimini le code avversarie
senza limitarsi a identificare nuovamente l'intero esatto attraverso
precisione sufficiente. Potrebbe tale proprietà dare una stima puntuale
degli errori Δ_v, o delle loro somme pesate? Questo è il passaggio
mancante. Né i controlli finiti né le identità di trasferimento costituiscono
una nuova dimostrazione della discesa della famiglia.
