# U14 — Costante1 e minimo antenato: corollario utile, con precedente esplicito

16 novembre 2026, controllo bibliografico finale mirato. Letti U15_MINIMUM_SEED_ASYMPTOTIC, relativo U04 PASS, U09 e i passi primari indicati sotto. Nessuna modifica ai testi congelati, nuova ricerca globale, scansione, Lean o pubblicazione.

**Giudizio editoriale:** l'asintotica a costante1 merita un corollario nella v7, non una headline di priorità. Il raccordo con F e con i minimi dei rami è nuovo per il progetto, ma il meccanismo quantitativo `P→1` su segmenti alti è già scritto esplicitamente da Valbuena. Non va presentato come una nuova conseguenza scoperta della sola sommabilità globale.

## Il precedente è più forte del solo P≤P₀

Nel [testo primario di Valbuena, snapshot a7275d5a, sezione «Uniform control of finite distinct trajectories»](https://github.com/x1xhlol/collatz-two-coordinate-obstruction/blob/a7275d5a73814d3d9a400c6fe6577de9542b03a3/paper/tao-basin-densities.tex), il lemma `ct-packing` e l'equazione `ct-prefix-product` affermano già: posto `β=H₂(log₃2)<1`, per ogni `b∈(β,1)` esiste `R_b<∞` tale che ogni segmento shortcut finito di stati positivi DISTINTI soddisfa

`Σ_(x_i≥M)1/x_i≤R_b M^(b−1)`, M≥1.

Se gli stati dispari che compaiono nei fattori del prodotto sono tutti almeno M, segue esplicitamente

`1≤P≤exp[(R_b/3)M^(b−1)]→1`,

uniformemente nella lunghezza e negli endpoint. Il prodotto esclude lo stato terminale. Valbuena usa inoltre questo errore tendente a zero nel trasporto dei pesi di primo passaggio. È quindi un precedente diretto per la normalizzazione a costante1, non soltanto per un bound uniforme P₀.

## Input esterno alternativo, utilizzabile senza g

Nel corollario U15 si può sostituire l'errore locale U09 con

`E_ext(m)=R_b m^(b−1)`.

Il primo arrivo dal minimo seed unità m è iniettivo e tutti i suoi stati dispari sono≥m; perciò

`exp[−E_ext(m)/3] n/m≤F(n)≤n/m`.

La deduzione non usa g, il floor o una legge casuale. La coda locale `82q^floor(log₃₂m)` ha un prefattore numerico disponibile; il bound esterno può dare un esponente migliore, senza un R_b valutato qui. Infatti `β≈0,949956`: ad esempio b=0,96 è ammesso e dà potenza `m^(−0,04)`, contro l'esponente locale circa0,029049. Questi decimali servono soltanto a confrontare gli ordini, non sono certificati numerici delle costanti esterne.

La stessa sostituzione vale nella sandwich dei rami laterali. La costante asintotica1 di `A(n_j)/n_j ~ Σ_laterali 1/m_U(x)` segue poi dalla crescita uniforme dei minimi laterali e dalla stabilizzazione già verificate. Non dà un rate di tali minimi rispetto a j o n_j, né il lower reciproco ancora mancante.

## Perimetro della novità

Non ho trovato le due formule esatte con F e minimi unità nelle sezioni controllate di9/12/146 o nel Curry, §§3–4. Curry tratta già reciprocità sommabile e prodotto convergente su orbite divergenti; Valbuena contiene il precedente uniforme decisivo sopra. Non è stato ripetuto un confronto completo di tutti i testi di Leen o delle altre versioni. Nessuna conclusione di priorità globale segue da questo controllo.

La presentazione difendibile è: **«Dal packing alto noto ricaviamo il confronto asintotico del nostro massimo inverso con il minimo seed unità; forniamo inoltre una costante locale esplicita tramite U09».** La direzione utile importata dalla letteratura è il tail a potenza più forte; il risultato resta un corollario breve del quadro già costruito, non un nuovo lower del surplus.
