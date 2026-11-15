# Analisi 2 Audit formale e verifica locale

Incarico svolto dall'agente `02_audit_formale`. La build incrementale integrata è riuscita: 3.380 passaggi, exit 0; unica segnalazione, ipotesi `hy` inutilizzata in `lean/CollatzShadowing/SignedTransport.lean:25`.

Quattro audit stretti sono stati elaborati nuovamente: 10 radici PrefixOptimality, 14 SiblingBasins, 7 LastExponentTransport e 6 SignedTransport. Tutte le 37 radici usano soltanto un sottoinsieme degli assiomi standard `propext`, `Classical.choice` e `Quot.sound`. Elaborazione fresca di ExactCylinders riuscita. I [log](verification/) e il [manifest](verification_manifest.json) sono conservati.

La scansione delle sorgenti non trova placeholder di prova o assiomi dichiarati. I nove `native_decide` sono tre piccoli controlli in `CollatzBridge.lean:669,693,714` e sei in `Generated/A0ReturnBranches.lean`, consentiti dalla CI. Non compaiono nelle dipendenze delle 37 radici controllate.

Riferimenti decisivi: shadowing `Shadowing.lean:86`; esclusione periodica espansiva `NoInfinite.lean:124`; congruenza esatta `ExactCylinders.lean:162`; tassa di precisione `PrecisionTax.lean:103`; ipotesi analitica esplicita `WeightedPredecessors.lean:172`; equivalenza del rango con Collatz `SectionReturn.lean:131`; budget di bacini `SiblingBasins.lean:77,113`.

La libreria principale è fissata a Lean 4.29.1; l'overlay analitico a 4.30.0-rc2. Il controllo storico dei suoi 399 moduli non è stato ripetuto. La verifica odierna riutilizza librerie compilate e non è un controllo tramite kernel indipendente.

Priorità proposte: certificati parametrici con copertura e rango verificati; formalizzazione del risultato asintotico H.2; replica isolata con toolchain aggiornato e audit ripetibili. La sostituzione dei controlli nativi può essere valutata in base al costo, senza confonderla con un avanzamento matematico sul problema aperto.
