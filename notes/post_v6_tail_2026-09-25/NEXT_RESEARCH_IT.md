# Cercare un bilancio congiunto con precisione controllata

Questa fase ha distinto tre problemi: la propagazione delle cifre
originarie è esatta; il bilancio delle code agli orizzonti diversi è
esatto; la stima uniforme della loro cancellazione è ancora aperta.
Il passo utile successivo deve aggiungere una disuguaglianza selettiva
per gli input della torre.

## Una formulazione concreta del certificato

Consideriamo gli input `Q_v` e `U_v=2Q_(v+1)` e suddividiamo il tempo
inferiore `H_v` in blocchi di lunghezze `b_0,…,b_(N−1)`, con somma
`H_v`. Il blocco superiore corrispondente ha lunghezza `2b_i`.
Se `t_i=Σ_(a<i)b_a`, definiamo il premio congiunto

\[
 w_i=J_{U_v}(2t_i+2b_i)-J_{U_v}(2t_i)
       -2\bigl[J_{Q_v}(t_i+b_i)-J_{Q_v}(t_i)\bigr].
\]

Allora `Σw_i=J_(U_v)(2H_v)−2J_(Q_v)(H_v)`. Gli ulteriori `r=v+3`
passi superiori necessari per `E_v` costano al massimo `r`, e
`Δ_v≤E_v`. Un certificato sufficiente avrebbe forma

\[
 w_i\le\Phi(X_i)-\Phi(X_{i+1})+c_i,
 \qquad
 \Phi(X_0)-\Phi(X_N)+\sum_i c_i+r\le g(v).          \tag{1}
\]

Qui `X_i` deve essere uno stato aritmetico specificato e `c_i` un costo
maggiorato senza conoscere già `Δ_v`. Le due disuguaglianze insieme
implicherebbero `Δ_v≤g(v)`; per ora **nessun** `Φ,c_i` con queste
proprietà è stato costruito. Non si presenta (1) come una soluzione.

Il [criterio pesato della fase dei margini](../post_v6_margin_2026-09-25/RESULTS_IT.md)
indica già un obiettivo sufficiente: ad esempio
`g(v)=2·2^ceil(v/2)` uniformemente da `v=16`. Il costo degli `r` passi
deve rientrare nello stesso budget, non essere dimenticato.

## Quale informazione includere

Il quoziente di precisione dimostrato in
[MEMORY_OBSTRUCTION_IT.md](MEMORY_OBSTRUCTION_IT.md) predice un blocco
di `b` passi da `z mod2^b`, dal contatore iniziale e dai prossimi bit
d'ingresso. Per il blocco superiore occorrono `2b` bit. Al termine,
questa precisione è consumata: per concatenare i blocchi serve un lemma
di rinnovo oppure una descrizione con più stati possibili e un costo
d'errore controllato.

Un'ipotesi di lavoro è costruire `X_i` come coppia di residui delle code,
insieme alla posizione nei due input e ai riporti che ne certificano
la generazione aritmetica. Gli input devono derivare esattamente da

\[
 Q_v=(3^{2^{v+1}}-1)/2^{v+3},\qquad
 Q_{v+1}=Q_v+2^{v+2}Q_v^2.
\]

La sola seconda relazione non basta: le
[ostruzioni aritmetiche precedenti](../post_v6_margin_2026-09-25/RESULTS_IT.md)
costruiscono altre coppie di interi che la soddisfano ma hanno un forte
eccesso di dispari. Anche una lista fissa di congruenze o di antenati
non identifica automaticamente la sorgente. Occorre dimostrare quali
stati incompatibili vengono esclusi dalla generazione esatta della torre.

## Un esperimento con condizioni di arresto chiare

Prima di ampliare le simulazioni:

1. Specificare lo stato `X`, il rinnovo della precisione e l'insieme di
   transizioni ammesse. Verificare l'inclusione di ogni transizione della
   torre: una tabella osservata su pochi livelli non è una prova.
2. Cercare una disuguaglianza della forma (1), con costo cumulativo
   esplicito. Se l'astrazione ammette cicli a premio positivo, esibire il
   ciclo e verificare se la sorgente esatta lo esclude; senza questa
   esclusione non dichiarare valido il certificato.
3. Controllare i termini iniziali e finali del potenziale indipendentemente
   dal peso di parità da maggiorare. Un potenziale proporzionale a `j`
   può soltanto spostare il problema nel termine finale.

È una proposta di ricerca, non la promessa di una compressione generica
possibile: il limite di memoria dimostrato esclude la previsione esatta
con un numero fisso di stati su tutti gli ingressi. Restano possibili
stime aggregate, memoria crescente o vincoli specifici della torre.
Una cancellazione uniforme dimostrata in (1), e non una nuova tabella di
parità o un'altra riscrittura del telescopio, sarebbe il progresso utile.
