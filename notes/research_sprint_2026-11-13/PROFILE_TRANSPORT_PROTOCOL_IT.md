# Protocollo del confronto finito fra profili congiunti

Fissato alle **16:16:45 UTC del 13 novembre 2026**, prima del calcolo.

L'esperimento esce dal modello di due soli esponenti: permette di cambiare l'intera parola, mantenendo esattamente lunghezza k e somma A. Le nuove stime su carta controllano l'altezza di qualunque trasporto reale con questi parametri. L'esperimento usa un costo d'altezza pratico D fissato, senza assumere che coincida con la costante universale teorica.

Parametri congelati: target n in `{5,7,31,593}`, fratello canonico h(n); cutoff dispari X in `{256,1024,4096}`; dilatazioni D in `{4,16,64}`; cap di 10.000 nuovi passi per completare ciascuna esplorazione. Nessun parametro viene adattato ai risultati.

Per ciascun target si ricostruiscono le parole del primo arrivo da sorgenti dispari entro il cutoff. Le sorgenti sono raggruppate per profilo `(k,A)`. Un arco u→v è ammesso se u raggiunge n, v raggiunge h(n), i profili coincidono e `v≤D*u`. Si cerca un accoppiamento iniettivo finito, con capacità uno su entrambe le parti. Ordinare ciascuna classe e accoppiare il minimo v al primo u che lo ammette produce un accoppiamento di cardinalità massima per questo grafo a soglia.

Registrare conteggi di base e immagini, profili mancanti, coppie distinte, rapporto finito η e costo D/η. Sono conteggi di parti dispari: non sono la comparazione ordinaria H. I fattori diadici e la massa asintotica richiedono un passaggio ulteriore.

Il censimento deve verificare tutte le orbite finite utilizzate; una ricerca incompleta è un errore, non un conteggio zero. I controlli delle coppie devono usare la stessa mappa ma una ricostruzione esplicita delle parole. Il massimo matching finito non dimostra che una quota sopravviva al limite. Se i profili mancanti restano il problema, il prossimo lemma riguarda comparazione degli atomi o trasporto fra profili diversi; aumentare soltanto X non lo risolve.
