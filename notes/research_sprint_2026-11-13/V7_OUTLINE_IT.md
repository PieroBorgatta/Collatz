# Proposta di ambito per la versione 7

13 novembre 2026. Proposta editoriale per Piero Borgatta. Non è un manoscritto completo né un deposito autorizzato. La decisione motivata è nella [relazione S15](agents/S15_V7_IT.md).

## Titolo proposto

**Finite Orbit Budgets and Predecessor Transport in Syracuse Dynamics**

Il sottotitolo può specificare “Version 7 of the CollatzShadowing research programme”. Il titolo descrive il contenuto positivo e i limiti del programma senza suggerire una soluzione globale.

## Abstract inglese proposto

We develop finite and parametric tools for predecessor transport in accelerated Syracuse dynamics. Exact valuation words are related to ternary affine residues and distinct positive sources. A telescoping occupation identity yields a shared dissipative budget for arbitrary endpoint families, while nonrecurrent root pools admit a stronger reciprocal charge bound. We combine these bounds with finite capacity certificates and an explicit relative-mass transport interface. A finite-segment form of a classical parity-packing argument gives a universal reciprocal-sum bound and controls the height of transports preserving word length and total valuation. We also prove obstructions to final-exponent-only transport and exhibit arbitrarily many consecutive increasing first returns to an arithmetic section. On one explicit return branch, the reset clock has a geometric parameter distribution with a summable approximation error. Lean-checked statements, separate mathematical proofs and finite computations are identified individually. A uniform relative-mass lower bound remains open; neither divergent orbits nor all nontrivial cycles are excluded.

## Tesi centrale

Il programma di trasporto si può scomporre in **altezza, carico e massa relativa**. Per trasformazioni a k,A invariati, l'altezza riceve un limite uniforme dalla sparsezza dei segmenti finiti; per shift finiti il carico ha un limite logaritmico nel target. Il risultato non risolto è una quota relativa η con il costo richiesto. Le interfacce formali rendono verificabile questa separazione e impediscono che un conteggio di rappresentazioni venga scambiato per un conteggio di interi.

## Matrice degli enunciati

**F** indica dichiarazioni Lean dello snapshot verificato, **C** prove matematiche separate, **E** controlli finiti esatti, **H** ipotesi aperte. Le etichette non sono intercambiabili; la build e gli audit finali devono riferirsi allo stesso snapshot del supplemento.

| Gruppo | Stato | Enunciato pubblicabile entro il suo dominio | Limite da conservare |
|---|---|---|---|
| Risultati della v6 | F/C | Cilindri, precisione, switching e singolarità già pubblicati, richiamati come base | Non rinumerarli come nuove scoperte |
| Sezione marcata e macro | F | Copertura da 1 o E, formule di cancellazione e arbitrariamente molti primi ritorni crescenti | Nessun rango globale; sezione sufficiente classica attribuita |
| Occupazione e pool | F | Budget dissipativo per target diversi; carico reciproco per pool non ricorrenti, compresi fratelli laterali | Un pool non ricorrente è più forte di radici separatamente senza ritorno |
| Dizionario ternario | F | Congruenza completa, positività automatica, endpoint dispari e conteggio iniettivo a lunghezza fissata | Target pari non ammesso nella conclusione Syracuse; catalogo completo da dichiarare |
| Capacità e flussi finiti | F | Allocazione a soglia e conversione di massa/carico in interi distinti | La minorazione della massa resta premessa |
| Trasporto del solo ultimo esponente | C/F/E | o(X) immagini a dilatazione fissa, con lemmi aritmetici Lean | L'asintotica completa non è formalizzata |
| Surgery bilanciata | F/C/E | Congruenza di località terminale; carico ≤ΣQδ per shift finiti e target senza ritorni | Il limite di carico completo e i lift sono su carta; η non ottenuta |
| Sparsezza finita e altezza | C/F/E | Bordo temporale N, B universale, prodotto affine limitato e D₀ universale a k,A invariati | Solo l'adattatore finito astratto è F; non l'intera stima entropica e le sue conseguenze |
| Raccordo e clock di un ramo | C/E | Primo ritorno esplicito, reset arbitrario e media del clock con errore ≤36M/√U | Frequenza su parametri liberi di un ramo, non lungo ogni orbita o sul kernel intero |
| H o confronto aggregato | H | Obiettivo quantitativo e conseguenza condizionale esplicita | Anche risolverlo lascerebbe il ramo dei cicli non banali |

## Indice ragionato

1. **Scope, maps and verification conventions.** Distinguere Col, shortcut T e Syracuse S; definire parole, sorgenti e target. Richiamare solo i risultati v6 necessari.
2. **Exact predecessor atoms.** Dizionario ternario, positività, disparità e conteggio delle sorgenti; orientamento delle parole rispetto alle fonti.
3. **Weighted occupation and nonrecurrent root pools.** Identità telescopica, normalizzazione, etichette duplicate e applicazione ai fratelli.
4. **Capacity certificates and relative transport.** Allocazione a soglia, collisioni e costo combinato D·M/η. Esporre l'obbligo nuovo senza assumerlo.
5. **Finite orbit sparsity and affine height.** Prova completa dell'adattamento finito del conteggio per finestre, somma sulle bande e conseguenza D₀. Attribuire il metodo di packing e delimitare la formalizzazione.
6. **Transport obstructions and balanced modifications.** Teorema H.2, vincolo terminale, limite di carico e collisione concreta. Nessuna estrapolazione asintotica dai successi numerici.
7. **Parametric returns and a controlled reset branch.** Ritorni crescenti, raccordo `[3,1,2]`, coda e convergenza del solo clock. Può diventare appendice se il nucleo sul trasporto risulta troppo ampio.
8. **Verification and open obligations.** Tabella dichiarazione→file→audit, prove C, esperimenti E, H aperta e problema dei cicli separato.

Le rotazioni dei cicli e i dettagli di riporto della torre possono stare in appendici o restare nel repository se non servono alla tesi centrale. Una v7 leggibile non deve contenere l'intera cronaca dei quindici incarichi.

## Primo passo indispensabile prima di un deposito

**Trasformare il nucleo S10 e il risultato H.2 in sezioni matematiche complete della v7, con una tabella precisa F/C/E/H e fonti accanto agli enunciati.** Contestualmente, associare il manoscritto a un commit/snapshot e al fascicolo finale di build, audit e hash. Si può mantenere la stima B e D₀ come prova su carta: non occorre attenderne la formalizzazione integrale per preparare un paper, ma non la si deve presentare come Lean-checked.

Dopo la stesura servono compilazione del nuovo PDF, verifica delle formule e dei rinvii, bibliografia aggiornata, supplemento riproducibile e confronto degli enunciati del PDF con i sorgenti. Queste attività precedono un eventuale deposito e non equivalgono a un'autorizzazione a pubblicare. La v6 pubblicata rimane immutata.
