# Revisione interna dell'argomento aritmetico

25 settembre 2026. Due agenti hanno svolto separatamente la revisione
aritmetica e quella delle fonti; non si tratta di peer review umana esterna.

La revisione matematica ha controllato la conservazione del prefisso,
l'equivalenza fra integralità finale e cilindro completo, la composizione
della costante affine, entrambe le congruenze, il limite inferiore
dell'altezza e i quantificatori della proposizione della sezione 3.
Ha controllato inoltre l'inversione 2-adica, i cilindri periodici e la
costruzione di parole sbilanciate con complessità elevata.

La revisione delle fonti ha verificato le attribuzioni, l'assenza di una
deduzione puntuale dai risultati quasi ovunque e la distinzione fra
cifre dell'intero e parità dell'orbita. Ha richiesto una correzione nel
memo: la costruzione combinatoria prova che densità elevata non forza
bassa complessità della parola di parità stessa; non dimostra che ogni
ponte verso le cifre ordinarie sia impossibile. Il testo è stato ristretto
di conseguenza, anche nel README. Sono state aggiunte la condizione
M≥3 nell'esempio generico e una giustificazione esplicita dell'isometria.

I 10 test di `test_arithmetic.py` sono scritti separatamente dal produttore.
Controllano tutti i cilindri fino a 8 bit, l'iterazione elementare e gli
estremi della costante, attraversano la soglia della composizione ricorsiva,
includono prefissi deliberatamente falsi e verificano le due congruenze
contro piccoli interi completi della torre. Controllano anche altezze,
centratura, periodicità, parole codificate e potenze modulari. Tutti passano.

Il replay dei livelli 22–24 verifica nuove identità sugli stessi dati
precedenti: non estende il campione. La concordanza in CI è riproducibilità
dello stesso programma. L'indipendenza C/GMP riguarda le parole complete
già verificate nella fase precedente, non un secondo verificatore delle
nuove costanti affini.

La proposizione generale è una dimostrazione su carta; l'applicazione del
teorema esterno di Chim non è verificata dal codice. La compensazione
uniforme e la discesa uniforme della famiglia restano aperte. Nessuna nuova
dichiarazione Lean o priorità matematica è rivendicata.
