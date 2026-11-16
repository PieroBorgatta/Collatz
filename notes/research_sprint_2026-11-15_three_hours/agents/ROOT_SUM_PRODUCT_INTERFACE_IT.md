# Interfaccia con il nuovo metodo sum-product

Lettura del 16 novembre 2026, senza eseguire codice esterno o modificare le prove Lean. La fonte è il manoscritto di Lyapunov Weaver del 14 novembre, [paper144/v1](https://rstation.ai/problems/collatz/papers/144). Il titolo nel testo scaricato è *Polynomial multiplicative expansion in Collatz orbit sets*. URL, versione e hash sono registrati in `research/research_sprint_2026-11-15_three_hours/root_late_web/source_metadata.json`; il testo completo resta temporaneo fuori dal repository, perché non è stata individuata una licenza nel manoscritto.

## Input esterni e ambito del controllo

La fonte dimostra un lower polinomiale sul numero di prodotti di un insieme finito di stati dispari che conserva molti archi effettivi. Per N stati consecutivi distinti il lower è N^(6/5)/64; per prefissi abbastanza lunghi rispetto al seed è N^(5/4)/64. Il meccanismo combina incidenze e separazione dei prodotti mediante la valutazione binaria. Le stime valgono anche per campioni densi. Il teorema12 ne deduce limiti superiori sull'energia moltiplicativa; il teorema14 dà unicità locale dei prodotti per finestre interamente molto alte. Queste sono condizioni necessarie su un possibile controesempio, non una conclusione di convergenza.

Il coordinatore ha letto la prova di separazione delle classi e la deduzione per traiettorie nelle sezioni2–4, e le interfacce delle sezioni5–7. Non è una verifica Lean, una revisione esterna indipendente o una replica dei controlli dell'autore; gli input combinatori classici non sono ricompilati qui.

## Decisione per il progetto

L'energia moltiplicativa riguarda uguaglianze fra prodotti degli stati di UNA traiettoria. Il surplus A=LF−F richiede invece percorsi reali che arrivino allo stesso target attraverso genitori fisici differenti, con un guadagno quantitativamente grande. Un prodotto di due stati non è automaticamente un antenato del target. La fonte non costruisce questa conversione e non è corretto usarne il lower di cardinalità come lower del surplus.

Il metodo può servire come vincolo aggiuntivo per una futura costruzione che produca già una relazione fra prodotti e percorsi rivali. In quel caso si dovranno verificare esistenza dei percorsi, etichetta del primo ramo e scala dei seed prima di applicare il bound di energia al controllo delle collisioni. Per ora la decisione è conservarlo come strumento esterno con questa interfaccia, senza aggiungere un'ipotesi analitica al nucleo formale o rivendicare un nuovo lower. Il problema attuale precede il conteggio delle collisioni: occorre costruire la massa del secondo insieme di cammini.
