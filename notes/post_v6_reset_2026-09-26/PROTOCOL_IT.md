# Protocollo della fase di consolidamento e nuova direzione

26 settembre 2026. Autore: Piero Borgatta con assistenza Codex.

La campagna di filtri su prefissi, antenati troncati e singolo riporto futuro
è chiusa. Non si aggiungono vincoli per salvare i test falliti. I risultati
pubblicati e gli archivi delle precedenti fasi rimangono riferimenti storici.

## Risultati richiesti

1. Formalizzazione aritmetica dell'ottimalità dei prefissi, con testimone
   positivo effettivo e audit degli assiomi.
2. Dossier per revisione umana esterna, preparato ma non inviato.
3. Ricognizione delle fonti primarie recenti, con enunciati e limiti.
4. Valutazione della proposta di amplificazione relativa dei bacini inversi.

## Diagnostica fissata prima del calcolo

Sia B(r;X) l'insieme degli inizi interi 1<=n<=X la cui orbita ordinaria
raggiunge il target dispari r. Per n dispari, n>1, 3 non divide n, scegliamo
y(n)=4n+1 se n=1 mod3 e y(n)=16n+5 se n=2 mod3. In entrambi i casi
S(y)=S(n), 3 non divide y e n<y<=16n+5.

Si calcolano esattamente i conteggi per i target dispari 5<=n<=1023,
3 non divide n, alle quattro soglie X=2^14,2^16,2^18,2^20. Si registrano
tutte le coppie e il rapporto diagnostico
(1+log(n))*card B(y;X)/card B(n;X), quando il denominatore è positivo.
I conteggi sono interi; il logaritmo è soltanto un dato floating point
di presentazione, non parte di un certificato matematico.

Il programma costruisce il grafo effettivo fino a 1 per tutti gli inizi
dispari <=X; le molteplicità delle parti dispari contano anche gli inizi
pari. Un limite di 10000 nuovi passi su una singola esplorazione provoca
errore, mai classificazione come convergente. Il limite non viene adattato.
Si verifica inoltre la disgiunzione dei bacini dei siblings lungo l'orbita
accelerata di 27 prima di 1, con somma dei conteggi <=X.

Non si sceglie una costante universale c dai risultati. I censimenti finiti
non provano né falsificano una disuguaglianza asintotica priva di un modulo
di convergenza. Un rapporto piccolo segnala un ostacolo quantitativo;
uno positivo non autorizza l'estrapolazione. Non si aumentano i cutoff
dopo aver visto i risultati di questo protocollo.

## Criterio per continuare

Il passo successivo deve costruire un confronto dimostrato fra famiglie
diverse di parole inverse per i due target vicini, con costo relativo
al più logaritmico. La positività separata dei due bacini non basta.
Se si ottengono solo costi polinomiali nell'altezza o una nuova ipotesi
sulla singola orbita, questa proposta resta una riduzione condizionale.
Prima di una nuova campagna occorre una stima concreta, non altri dati.
