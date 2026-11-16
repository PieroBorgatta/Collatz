# Addendum U05 — Code generate da pochi pezzi periodici

Prova su carta candidata, successiva alla nota U05 principale e separata per non modificarne lo snapshot sottoposto a revisione. Nessun nuovo esperimento. Input profondo unico: Corollario 2 di Evertse1984, nella forma e con i limiti già dichiarati in T02/T04. Nessuna priorità bibliografica globale accertata.

## Enunciato

Fissare target positivi dispari distinti n,y, un intero s≥0 e un dizionario finito D di parole non vuote di esponenti positivi. Ogni coda strutturata è concatenazione di al più s pezzi, ciascuno dei quali è:

- una lettera arbitraria e≥1; oppure
- q^t, ripetizione t≥1 di una parola q∈D.

Considerare parole effettive w=pα:u→n, w'=pβ:v→y, con p identico e |α|=|β|=L, Σα=Σβ=B. Assumere che w sia di PRIMO ARRIVO a n; per w' non occorre questa ipotesi. La sorgente originale soddisfa u≤X, mentre v non ha cutoff.

**Candidato.** Il numero dei codici fisici (u,p,α,β,v) è X^o(1), con costanti dipendenti solo da n,y,D,s e dal parametro dell'esponente arbitrariamente piccolo. Un flusso con carico uscente≤1 per sorgente non può quindi ottenere una quota positiva di un bacino di densità inferiore positiva attraverso questa relazione.

Il numero di pezzi è fissato. La lunghezza delle potenze, gli esponenti delle lettere libere, la distanza fra gli edit e il totale delle parole possono crescere con X. Ciò non copre code con numero crescente di blocchi diversi o con dizionario che cambia con X.

## 1. Ogni potenza ha soltanto due termini affini

Per q∈D, scrivere ell=|q|, a=Σq, C=C(q), d=2^a−3^ell. Si ha d≠0, poiché a,ell>0 e una potenza di2 non può uguagliare una potenza di3. Inoltre d è coprimo con6. La concatenazione dà

C(q^t)=C(q)[2^(at)−3^(ell t)]/[2^a−3^ell].

Sia Δ il minimo comune multiplo dei |d| del dizionario, posto Δ=1 se D è vuoto. La costante affine di una concatenazione di≤s pezzi si ottiene sommando le costanti dei pezzi con fattori 2^(totale del prefisso) e3^(lunghezza del suffisso). Dopo moltiplicazione per Δ, è quindi una somma di≤2s termini

c·2^b3^j,

con c appartenente a un insieme FINITO fissato, 0≤b≤B, 0≤j≤L. Per una lettera libera C([e])=1 per qualsiasi e, quindi essa costa un solo termine; il suo esponente non introduce coefficienti nuovi. I coefficienti sono interi dopo la moltiplicazione per Δ e restano indipendenti da t,e,L,B.

## 2. Il residuo controlla la lunghezza non strutturata

Come in U05 principale, porre r=|p|, P=Σp, k=r+L, A=P+B. L'identità affine dà

3^k(v−u)=2^P R,
R=2^B(y−n)−[C(β)−C(α)].

Poiché n≠y e le lunghezze totali sono uguali, R≠0: altrimenti u=v e la determinazione dell'orbita darebbe lo stesso endpoint. Dunque ΔR è una somma non nulla di≤4s+1 S-unità, con S fissato dai coefficienti, 2,3 e y−n. Il minimo dei valori assoluti ternari è≥c·3^(−L), con c>0 fissato; l'altezza è≤C·2^B3^L≤C·6^B. Il prodotto su S di ciascuna coordinata è1.

Il Corollario 2 di Evertse ammette sottosomme nulle e dà, per ogni τ>0,

ν₃(R)≤L+τA+C_τ.

Da3^k|R segue r≤τA+C_τ. L'argomento non pretende di rendere sublogaritmica tutta la profondità: paga separatamente la parte strutturata.

## 3. Il primo arrivo impedisce potenze arbitrariamente lunghe a sorgente fissata

Sia x l'inizio di un pezzo q^t, e x_t il suo endpoint. L'esattezza fornisce

2^(at)[d x_t−C]=3^(ell t)[d x−C].

Se d x−C=0, la prima copia effettiva di q torna esattamente a x. Essa ripete uno stato all'interno della parola originale. Una parola di primo arrivo è iniettiva su tutti i suoi stati, incluso l'endpoint, quindi ciò è impossibile. Non si è assunto che non esistano altri cicli positivi.

Pertanto d x−C è un intero NON NULLO e

2^(at) | (d x−C),

sicché at≤log₂|d x−C|≤log₂(x+1)+O_q(1). La lunghezza di questo pezzo è dunque O_q(1+log(x+1)). Con la crescita di un passo S(z)+1≤(3/2)(z+1), tutte le sue altezze intermedie sono≤C_q(x+1)^(c_q), con costanti dipendenti solo da q.

Per una lettera libera vale sempre la stessa crescita di un passo, anche se il suo esponente è molto grande. Componendo al più s pezzi, da uno stato iniziale z si ottiene

L≤C_(D,s)[1+log₂(z+1)].

Prima della coda, z+1≤(3/2)^r(X+1), perciò L≤C_(D,s)[1+log₂(X+1)+r]. Questo clock è il punto che richiede primo arrivo; altrimenti un blocco che chiude un vero ciclo potrebbe essere ripetuto indefinitamente a sorgente fissata.

## 4. Assorbimento e conteggio

Il budget elementare della parola originale è A≤2k+log₂X. Inserendo il clock della coda e r≤τA+C_τ, si assorbe r per un τ abbastanza piccolo. Ne risultano k,A=O(logX). Reinserendo in r≤τA+C_τ per ogni τ>0 si ricava r=o(logX).

I prefissi si contano conΣ_(r≤o(logX))binom(O(logX),r)=X^o(1). La scelta dei tipi dei≤s pezzi ha un numero finito di possibilità. Ciascun parametro t o e è≤A=O(logX), perciò i due suffissi aggiungono soltanto fattori polilogaritmici. Le parole e i rispettivi target determinano al più una u e una v. Questo prova il candidato.

## Relazione con gli attacchi precedenti

Scegliendo D={[1]}, si escludono i corridoi tutti1 con poche lettere libere. Un dizionario con parole miste esclude anche un numero fissato di lunghi corridoi periodici che abbiano arbitrariamente molti cambi di esponente al loro interno. La prova non scambia questi corridoi per offset arbitrari: la formula geometrica è la ragione esatta della dimensione S-unità limitata.

La nota principale U05 rimane più forte, quanto alle ipotesi orbitali, nella sua sottoclasse con pochi non1: lì non richiede primo arrivo. Questa estensione richiede primo arrivo soltanto per il clock dei pezzi periodici.

Il caso generale di pochi edit in posizioni mobili, con blocchi inalterati non periodici di complessità crescente, resta aperto. Questa è una restrizione rigorosa di quali costruzioni fondate su phantom periodici potrebbero ancora produrre massa relativa, non una dimostrazione di H o Collatz.
