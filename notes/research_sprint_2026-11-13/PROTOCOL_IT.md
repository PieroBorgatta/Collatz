# Sessione di ricerca e integrazione Collatz

Richiesta di Piero Borgatta del 13 novembre 2026: usare i nuovi risultati web, integrarli dove utile, coinvolgere quindici agenti in confronto reciproco e lavorare per almeno un'ora prima del bilancio.

L'obiettivo aggiornato include una decisione motivata sulla possibilità di una v7 del paper: confronto con il contenuto della v6, risultati aggiunti, priorità bibliografica, verifica e obblighi ancora aperti. Valutare la pubblicabilità non autorizza un deposito o una pubblicazione.

Inizio misurato: **2026-11-13 15:32:23 UTC**, cioè **16:32:23 Europe/Rome**. Il bilancio finale non inizia prima delle **16:32:23 UTC**, cioè **17:32:23 Europe/Rome**. Dopo tale soglia si fermano le nuove esplorazioni e si consolidano le verifiche.

**Chiusura effettiva della ricerca:** 2026-11-13 **16:32:38 UTC**, cioè **17:32:38 Europe/Rome**, dopo **3615 secondi**. Tutti i quindici incarichi e i confronti supplementari erano conclusi. Le attività successive riguardano soltanto sintesi, documentazione e controllo degli artefatti.

Base: commit `5428e89`, ramo `phase10-wip`. Il dossier `notes/review_2026-11-13/` appartiene alla precedente richiesta ed è conservato. Nessuna pubblicazione o contatto esterno è autorizzato da questa sessione.

## Regole di lavoro

- Quindici agenti distinti, in gruppi compatibili con il limite operativo di tre agenti oltre al coordinatore. Ciascun agente riceve un ambito e file propri; scambia risultati e obiezioni con gli altri agenti tramite messaggi.
- Priorità a lemmi finiti o parametrici effettivamente verificabili e a un ponte preciso con le fonti nuove. Lettura delle fonti primarie e distinzione tra risultato pubblicato, preprint, codice dichiarato verificato e verifica locale.
- Nessun `sorry`, `admit` o nuovo assioma di progetto. Una proposizione condizionale esplicita non è una prova della sua ipotesi. I risultati su carta e i test finiti restano distinti dai teoremi Lean compilati.
- Non riaprire i trasporti del solo ultimo esponente o i filtri finiti già confutati senza una modifica matematica che esca dal loro dominio.
- Le modifiche ai moduli principali vengono integrate e sottoposte a build solo dopo controlli mirati. Le dipendenze e gli snapshot pubblicati restano fissati.
- Gli esperimenti registrano domini, criteri di arresto e risultati negativi. I conteggi di parole non diventano conteggi di interi senza controllo della molteplicità.

## Domande principali

1. Quali meccanismi dei nuovi pool di radici e del mixing congiunto producono un lemma finito riutilizzabile senza importare l'intera catena esterna?
2. Un budget condiviso per target differenti permette un controllo di carico più efficace?
3. Una trasformazione di più esponenti o di profondità variabile mantiene massa relativa con costo totale compatibile con H o con una sua variante aggregata?
4. Si possono certificare primi ritorni, blocchi crescenti di durata arbitraria e una vera interfaccia d'uscita?
5. Quali vincoli esatti sui cicli o sui fattori primi aggiungono informazione indipendente?

Un risultato negativo o un obbligo rimasto aperto è un esito valido della sessione. L'obiettivo è una prosecuzione giustificata dai risultati, senza promettere la soluzione della congettura.
