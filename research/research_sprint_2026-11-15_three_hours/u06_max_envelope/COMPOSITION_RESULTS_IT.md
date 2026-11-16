# Prototipo standalone: composizione e calibrazione

Estensione in file separato; il CORE già verificato e congelato è copiato come prefisso identico. Nessun modulo integrato, entrypoint o statistica main è modificato. **PASS:** secondo controllo Lean standalone e audit transitivo dell’estensione (4 dichiarazioni, inclusa1 privata; tre enunciati pubblici). Il CORE ricopiato ha nuovamente superato il suo audit (18 dichiarazioni, incluse8 private). Soltanto `propext`, `Classical.choice`, `Quot.sound`. La lettura semantica indipendente U04 ha dato PASS e lega la stessa impronta del sorgente congelato.

Tre enunciati aggiuntivi:

1. **Composizione.** Se u è un seed positivo dispari unità e w:u→n è una parola effettiva, `Ω(w)F(u)≤F(n)`. Si prende un witness v che realizza F(u), lo si concatena a w nell’ordine forward v++w e si applica la dominazione di tutti i gain.
2. **Seed ottimale.** Se inoltre Ω(w)=F(n), allora F(u)=1. Si cancella il fattore F(n)>0 nella disuguaglianza di composizione e si usa F(u)≥1.
3. **Prefissi calibrati.** Se v:u→z e w:z→n sono effettive, u e z sono positivi dispari unità e Ω(v++w)=F(n), allora F(z)=Ω(v). La dominazione del prefisso dà un verso; la composizione sul suffisso e la cancellazione del suo gain positivo danno l’altro. L’ipotesi di unità sull’intermedio z è ESPLICITA: non viene aggiunto un lemma automatico sugli intermedi.

Sono inclusi prefissi e suffissi vuoti e target periodici. Non si richiedono g, Q, densità o ipotesi di massa. Non sono formalizzati i profili K/A, la policy ottimale completa o la sua velocità uniforme; la composizione non prova Collatz.

Il file `CompositionPrototype.lean` include i sei lemmi CORE per consentire un singolo controllo standalone senza modificare il file congelato o creare un modulo main. L’audit distingue le dichiarazioni CORE da quelle aggiuntive. I sei lemmi copiati non sono contati come ulteriori risultati indipendenti.

Il primo tentativo dell’estensione è conservato, compreso il sorgente corrispondente: la composizione aveva già superato Lean; due usi del nome generico della cancellazione moltiplicativa richiedevano l’API `mul_le_mul_iff_right₀`. La revisione non ha cambiato gli enunciati.

Il sorgente finale è congelato con SHA-256 `d199434cf12f96c042e133810d269437773cac1d65295f853f06d156b39faefa`; il CORE resta `c640f8cd46ee70772c5f0f3c0dc1795b912b05923bd9a3d6e92c7c8343562836`. Sorgenti e quattro moduli integrati rimasti invariati durante la verifica. I sei enunciati CORE e i tre aggiuntivi restano standalone: nessuna modifica alle statistiche dei moduli main è imputata a questi prototipi. La verifica riusa il toolchain e gli artefatti fissati; non è un replay indipendente o una ricompilazione a freddo.
