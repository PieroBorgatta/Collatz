# Seconda ora: una famiglia concreta e il problema delle uscite

16 novembre2026. Ricerca con tre agenti, lettura di fonti primarie e ragionamento su carta. Nessun esperimento numerico, compilazione, modifica di prove Lean o uso di GPU. Il lavoro precedente è rimasto al commit bfa35c3; questa cartella raccoglie soltanto la nuova fase. Il protocollo e la ricevuta finale separano il tempo di ricerca dalla consegna.

## Decisione

Il prossimo tentativo merita di concentrarsi sulle **coppie di percorsi e sulle uscite da un linguaggio esplicito**, prima di aggiungere altri oggetti F, tracce, cap o reset scelti liberamente. Abbiamo una piccola costruzione positiva, con cambiamento iniziale e stati interi controllati, che funziona su una classe propria di parole. Non abbiamo una copertura del futuro di un seme arbitrario, né un lower risolutivo o una prova di Collatz.

La v7 può servire a consolidare risultati e dipendenze, ma non è un passaggio obbligato per questa ricerca. Non pubblicherei una nuova versione scientifica solo per aggiungere questi raccordi. Prima chiederei un risultato sulla copertura delle uscite o sul bilancio dei costi per il percorso già dato.

## 1. Il risultato costruttivo da conservare

La traslazione `H(x)=x−2` intreccia due coppie di blocchi Syracuse:

`(1,2) → (2,1)` e `(2,1,2) → (1,1,3)`.

Le identità affini e i cilindri binari provano che ogni concatenazione dei blocchi a sinistra viene seguita dal compagno iniziale b−2 con i blocchi a destra, mantenendo differenza2 ai confini. Non sono semplicemente gain uguali o sorgenti razionali astratte: le valutazioni degli interi sono quelle prescritte. I blocchi non sono potenze dello stesso periodo. Il meccanismo generale delle parole accoppiate è classico; non rivendichiamo che sia stato tentato qui per la prima volta.

Un gate terminale della [fonte152/v1, §4](https://rstation.ai/problems/collatz/papers/152) consente la fusione finale con un ultimo genitore diverso da quello osservato. Sono state controllate le correzioni per ottenere seed unità; la parola alternativa può avere clock più corto. Una sottoclasse di due macroblocchi mantiene ogni prefisso osservato sopra il seed originale, pur ammettendo quel compagno più piccolo. Il riferimento completo, con parole e formule, è [H21, §8](agents/H21_EDITOR_IT.md).

La [fonte21/v3, Theorem3](https://rstation.ai/problems/collatz/papers/21) permetteva già di estendere ogni prefisso espansivo fissato a un cilindro con seme più piccolo. Il valore specifico del nostro raccordo è conservare **lo stesso** compagno b−2 attraverso una grammatica mista, con gate fisso e guardie esplicite; non è la prima costruzione di una riduzione di sorgente prima della discesa.

C'è anche una conseguenza senza il floor analitico esterno: un minimo seed divergente unità deve iniziare con gap1, perché un gap≥2 lo porterebbe subito a un'unità più piccola. Se rimanesse per sempre nel linguaggio `{12,212}^ω`, inizierebbe quindi con12. Il compagno b−2 divergerebbe insieme a lui ai confini dei blocchi: se fosse una foglia multipla di3, il suo primo gap2 darebbe l'unità `(3b−5)/4<b`, anch'essa divergente. Negli altri casi b−2 è già unità più piccola. Quindi quel minimo deve uscire dal linguaggio. Per questo argomento non occorre aspettare la fusione terminale. Non sono coperte tutte le uscite, né dimostrata la realizzazione positiva di una parola infinita arbitraria.

La prossima domanda è precisa: alla prima uscita, si può ottenere una fusione, passare a un'altra relazione tra i due percorsi con costo controllato, oppure certificare una discesa sotto b? La forma dei casi d'uscita è descrivibile, ma le valutazioni possono essere illimitate. Aggiungere altri esempi alla grammatica non dimostra una copertura.

Il controllo negativo è concreto: esistono prefissi `(12)^K13`, interamente espansivi e con gap osservati≤3, in cui il compagno b−2 arriva a1 mentre il percorso osservato arriva a un valore arbitrariamente grande. Quindi il solo buffer passato e un cap sui gap osservati non danno un carry uniformemente limitato. Questi esempi hanno però una successiva corsa forzata di gap2 che ripaga il dislivello e, per parametri abbastanza grandi, scende sotto b. Non confutano un controller che contabilizzi anche quelle discese future. Sotto l'ipotesi di minimo seed divergente, per le uscite13/213 e per il grande parametro dell'uscita11 è stato ricavato un costo esplicito in funzione del buffer di crescita; non è ancora un costo O(log j) né un ammortamento globale. Il target utile è proprio una simile alternativa con bilancio, non conservare sempre lo stesso compagno a ogni uscita.

## 2. Un criterio più adatto a futuri certificati finiti

[H23, §2](agents/H23_ADVERSARIAL_IT.md) estende il budget dell'ora precedente a un prefisso osservato semplice e a cataloghi finiti di veri primi arrivi off-spine, prefix-free nell'orientazione inversa. Non occorre decidere prima se il target sia globalmente nonperiodico:

`Σ Γ ≤ bP₀(8/α+1)`.

La prova separa l'unico possibile ingresso nel ciclo: bastano due antichain di seed nonperiodici, ciascuna pagata dal lower logaritmico già noto, e al più un seed periodico. Il floor α resta un input esterno non riprodotto; P₀ è il prodotto di primo arrivo già verificato nel progetto. Questa è una semplificazione dell'interfaccia del prossimo lemma, non la produzione della massa laterale richiesta.

Le nuove costruzioni di fusione non vengono automaticamente promosse a questi certificati: per usare il budget vanno mantenuti primi arrivi e prefix-free. Su una spine divergente il primo arrivo è automatico; per una generica identità finita va verificato o assunto.

## 3. Che cosa la letteratura ha fatto eliminare dal programma

Il reset lineare di una coppia con etichette scelte esiste già nella [fonte81/v2](https://rstation.ai/problems/collatz/papers/81). Anche il routing modulare dal root assegnato con totale lineare è già nella [fonte48/v2, Theorem8](https://rstation.ai/problems/collatz/papers/48). Non conviene riprovare quei due risultati come lacune nuove. Il primo sceglie un cilindro compatibile; il secondo non produce piccoli antenati. [H22](agents/H22_LITERATURE_IT.md) ne controlla gli input.

Un [conteggio elementare](ROOT_ROUTING_COST_IT.md) mostra perché il routing uniforme, seguito da k inverse di esponente1, non ripaga il guadagno desiderato: per coprire ogni root a lunghezza e totale fissati, il fattore reale finale è almeno `4·2^k`. La conclusione riguarda quell'architettura uniforme per root grandi; lascia aperti insiemi condizionati rari e costruzioni differenti.

Il [primario150/v2](https://rstation.ai/problems/collatz/papers/150) è il progresso recente più pertinente: ogni limite empirico ternario di una ipotetica spine divergente deve avere una massa singolare almeno circa8,85%. È una restrizione della possibile eccezione, non la sua esclusione. Né il floor, né il telescopio del progetto forniscono la regolarità opposta. Una legge media sotto Haar non può quindi essere sostituita gratuitamente alla legge del percorso eccezionale.

Sono stati letti anche gli aggiornamenti149,151,152,153,154. Il nuovo grande bound151 riguarda solo cicli con altezza canonica≤1;154 migliora una finestra per costruire famiglie terminanti lente.153 dà un limite alle riparazioni locali di assegnazioni parzialmente giunte, con ipotesi esplicite sulla parola fornita. Nessuno chiude il nostro obbligo di copertura; i grandi certificati esterni non sono stati rieseguiti. Si vedano [scope dei lavori151/153](ROOT_LATEST_SCOPE_IT.md) e le note degli agenti.

## 4. Valore del lavoro e condizioni per continuare

Il patrimonio utile del progetto è la legalità esatta dei percorsi, il controllo del prodotto di primo arrivo, i budget e gli ostacoli che eliminano costruzioni sbagliate. In questa ora quegli strumenti hanno permesso di valutare una famiglia positiva, anziché fermarsi a un'altra identità nominale.

Resta ridondante accumulare corollari qualitativi già disponibili, prove di reset con sorgenti scelte o upper usati dove serve un lower. Anche un linguaggio con molte parole può lasciare fuori il futuro decisivo di un solo intero. La letteratura classica di coppie mostra già quanto possano essere incomplete le classificazioni di gate proposte.

Continuerei con un tentativo circoscritto sulle uscite, cercando un'invariante dei due percorsi che conservi un partner più piccolo o un bilancio Γ utile. Se il tentativo produce soltanto una lista crescente di casi, senza controllo del carry e del costo, lo fermerei. La via entropica offre soglie necessarie per la possibile divergenza, ma non abbiamo un nuovo lower sui residui di un seme dato: non la presentiamo come una soluzione alternativa già pronta.

Tutte le deduzioni nuove sono state riviste su carta da altri agenti. Sono da distinguere dalle prove Lean preesistenti e dai teoremi dei manoscritti esterni. Nessuna priorità universale o soluzione della congettura è rivendicata.
