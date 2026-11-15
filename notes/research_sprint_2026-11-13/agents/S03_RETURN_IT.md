# S03 Primi ritorni crescenti di lunghezza arbitraria

13 novembre 2026. Integrazione nel modulo `lean/CollatzShadowing/ReturnBlocks.lean`, senza modificare gli import principali o altri sorgenti Lean. Il risultato esplicita una proprietà dei primi ritorni che non era dichiarata nei precedenti teoremi di assenza di discesa a orizzonte fissato.

## Risultato formalizzato

Per ogni t positivo, r naturale e `0≤j≤r`, sia

`x_j=18·t·8^(r−j)·9^j−5`.

Per `j<r`, sia `y_j=216·t·8^(r−j−1)·9^j−7`. Il modulo prova:

- `S(x_j)=y_j`, con esponente esattamente 1;
- `S(y_j)=x_(j+1)`, con esponente esattamente 2;
- entrambi gli endpoint appartengono alla sezione E, mentre y_j non vi appartiene;
- `x_(j+1)=x_j+18·t·8^(r−j−1)·9^j`, dunque il ritorno è strettamente crescente;
- `S^[2j](x_0)=x_j`, per `j≤r`.

Il punto intermedio è escluso da tutti i sei porti: il suo residuo è `65 mod72` quando il coefficiente è positivo; il caso degenere è 0 ed è anch'esso esterno alla sezione. Il lemma `first_return` certifica esplicitamente che nessun tempo positivo strettamente inferiore a 2 incontra E.

Il teorema `arbitrarily_many_increasing_first_returns` conclude

`∀r ∃n>0`, con n nella sezione, tale che i primi r ritorni consecutivi avvengano ai tempi `2,4,…,2r` e siano tutti crescenti.

L'ordine dei quantificatori è essenziale: **non** viene costruito un singolo n con infiniti ritorni crescenti. Non è dimostrata la discesa dopo l'ultimo ritorno né l'assenza di orbite divergenti.

## Relazione con il codice preesistente

L'aritmetica del passo è riusata da `cancellationTower_block`: per un cofattore pari v, `8v−5 → 12v−7 → 9v−5`. Il nuovo lavoro certifica appartenenza, esclusione intermedia e concatenazione dei **primi** ritorni. È un corollario delle torri già note al progetto, senza rivendicazione di priorità bibliografica.

Riferimenti nel nuovo file: definizioni alle righe 15 e 18; passi esatti alla riga 63; incremento alla riga 76; primo ritorno alla riga 89; identificazione con gli iterati alla riga 105; teorema parametrico finale alla riga 118.

## Conseguenza per la prosecuzione

Un certificatore che cerchi la discesa entro un numero fissato di ritorni non può coprire questa famiglia. Serve comprimere un numero arbitrario di blocchi e dimostrare una vera interfaccia d'uscita. Un clock decrescente dentro il blocco non basta se il suo reset dopo l'uscita rimane senza controllo.

Il terminale è `18t·9^r−5`. Per t=1 questo è `2·9^(r+1)−5`: il passo successivo è già descritto da `cancellationTower_exit_one (r+1)`, con esponente 3 e uscita `(3·9^(r+1)−7)/4`. Non va presentato come nuova interfaccia. Per t dispari generale il successivo esponente è `1+ν₂(27t·9^r−7)`, che può essere elevato.

## Confronto con gli altri agenti

S01 e S02 sono stati avvisati che gli endpoint x_j sono annidati lungo una stessa orbita e non formano un pool nonricorrente. Il limite forte `Σω/R≤1/x` richiede una vera linea d'arresto/antichain; non può essere applicato sommando questi endpoint. Resta disponibile il budget dissipativo generale `Σω/[R(3R+1)]≤1/x`. Entrambi gli agenti hanno confermato questa distinzione nei messaggi reciproci.

## Verifica

**PASS:** elaborazione dedicata con Lean 4.29.1 e le dipendenze fissate del progetto, exit 0 e nessun messaggio. Comando: `DEVELOPER_DIR=/Library/Developer/CommandLineTools lake env lean CollatzShadowing/ReturnBlocks.lean`. Il log finale è `notes/research_sprint_2026-11-13/verification/s03_returns.log` (vuoto perché senza errori o avvisi); la ricevuta `s03_returns.json` registra comando, hash ed esito. Nessun nuovo assioma, `sorry`, `admit` o `native_decide` introdotto. Build integrata e audit delle dipendenze saranno eseguiti dal coordinatore o dagli incarichi di revisione.
