# U04 — Forza e dominio degli input analitici

16 novembre 2026. Lettura mirata dei primari, senza usare i giudizi editoriali come prova. Nessuna compilazione esterna, riesecuzione di certificati o importazione Lean. URL, hash dei byte consultati e scope esatto sono nella ricevuta `u04/analytic_inputs_review_receipt.json`; i file scaricati restano temporanei.

**Esito:** i manoscritti enunciano e dimostrano gli input richiesti, con dipendenze analitiche esterne dichiarate; non li subordinano alla congettura di Collatz o alla nondivergenza. Resta essenziale una correzione di dominio: **l'upper lineare di g è disponibile sui target nonreturn; una costante lineare uniforme su tutti i cicli non è stata trovata né giustificata.** Tutto resta input esterno del progetto, non teorema Lean locale verificato da questo audit.

## 1. Traccia canonica, positività e armonicità

Nel primario [Valbuena, archivio23025885](https://doi.org/10.5281/zenodo.23025885), il file `paper/tao-basin-densities.tex` prova: limite critico finito e armonicità a due rami (Teorema8), decadimento su antenati di un root fissato (Proposizione9), identificazione Cesàro/Abel (Teorema14) e upgrade dei mezzi pesati a densità naturale (Teorema16). La prima parte usa la stabilizzazione di primo passaggio di Tao a due scale, con il controllo scritto del cambio di parametro; l'upgrade naturale aggiunge il trasporto di Mazur. La sezione finale distingue gli enunciati ancora aperti dalle conseguenze provate. Non ho ricompilato il bundle né verificato tutte le sue dipendenze formali.

Per passare ai genitori dispari, si itera l'equazione finita. Il resto è `2^(−m)H(2^m n)=n·H(2^m n)/(2^m n)`, che tende a zero perché 2^m n è un antenato del root n. Quindi la somma countable positiva soddisfa Lg=g, anche ai root periodici. È il passaggio esplicito della [fonte12, §9, Corollario7](https://rstation.ai/problems/collatz/papers/12).

## 2. Floor assoluto: non è una congettura lasciata come CE

[El Jaouhari,23377671](https://doi.org/10.5281/zenodo.23377671), Theorem A, afferma `ρ_k(r)≥α>0` a ogni profondità positiva e ogni residuo unità. Ho letto la catena scritta: iniettività degli offset a totale fissato; conteggio pesato delle fibre; blocchi selezionati con massa positiva e incrementi uniformi sommabili; verifica delle core estimates CE; cilindro positivo; passo inverso di esponente limitato che lo propaga a tutte le unità. CE viene verificata, non soltanto assunta. L'input analitico nominato è il mixing fine di Tao, Proposition1.14. La nota formale indica un tag pubblico e controlli delle dipendenze; qui non sono stati rieseguiti.

Prendendo i mezzi Cesàro della disuguaglianza a ogni livello, il limite canonico dà immediatamente `g(n)≥α` su ogni unità positiva dispari, compresi i cicli. Non viene applicato il floor ai multipli di tre, dove la traccia è zero.

## 3. Upper: lineare soltanto nel dominio corretto

Ponendo κ=log(4/3)/2, la formula canonica è `g(n)=κ n β_n/(1−λ_n)`, con 0≤β_n≤1 e λ_n=0 se n non è periodico. Pertanto il bound necessario sulle spine divergenti è già `g(n)≤κn`. Per un root ciclico rimane invece `g(n)≤κn/(1−λ_n)≤κn(3n+1)`.

La distinzione compare anche nella fonte12, Corollario5, equazioni18–19. Non si può cancellare il fattore di ciclo. U12/U07 operano già su root nonreturn; Green pesato, LF, cap e ladder che non usano l'upper restano validi sui cicli. Il cap lineare U15 usa l'upper soltanto sulle spine divergenti; l'uniformità heavy elimina prima le orbite eventualmente periodiche del pool finito. L'applicazione di quel corollario non richiede quindi un upper globale sui cicli.

## 4. Densità reciproca: prova nel manoscritto, dipendenze dichiarate

La [fonte12, Theorem1 e §2](https://rstation.ai/problems/collatz/papers/12) dimostra il coefficiente uniforme c/a con due catene alternative. Per i nostri usi basta atom floor + esistenza di densità naturale. [Leen, Brownian motion,23252395](https://doi.org/10.5281/zenodo.23252395), lemma Densities e teorema Invariant sets, prova quest'ultima dal passaggio relativo; non usa la positività dei bacini. Il [primario di passaggio23046896](https://doi.org/10.5281/zenodo.23046896), Theorem5.3, contiene una stima uniforme in tutti i test limitati, con errore relativo più resto assoluto. Gli input non sono il bottom-tail aperto menzionato altrove. Leen dichiara una parte dei riscontri formali non pubblica: qui la catena è stata letta come prova scritta, non ricertificata.

Ricostruzione del raccordo: a un root nonreturn, `Σ_(k≤K)ρ_k(a)≥αK` conta sorgenti odd distinte, ciascuna con gain≤a/x. L'esponenziale geometrico paga le sorgenti x>exp(8K). Segue densità logaritmica relativa odd≥α/(4a). Esistenza naturale e invarianza per raddoppio identificano questa con la densità ordinaria. Per un root periodico, fra tre genitori dispari diretti di altezza≤64a/3 ce ne sono due unità e al massimo uno periodico; scegliere l'altro trasferisce il lower. Questa prova non assume una classificazione dei cicli.

La [fonte9, §8.2, Theorem12](https://rstation.ai/problems/collatz/papers/9/v1) dà invece a^(−2−ε), usando il diverso input pesato di Mazur; da sola non giustifica c/a. Il manoscritto9 precisa che tale interfaccia di cammini non è stata ricompilata né certificata come dichiarazione formale separata. Non è necessaria per la via atom floor + densità appena descritta.

## 5. Minimo seed e tail: guardie indispensabili

Queste verifiche sono elementari e indipendenti dai tag delle fonti. Il minimo ordinario m_* di un bacino è dispari: se fosse pari, m_*/2 sarebbe un antenato minore. Se è già unità, m_U=m_*. Altrimenti, per un target unità, m_* non è il target; S(m_*) è una unità, raggiunge ancora il target ed è ≤(3m_*+1)/2≤2m_*. Quindi `m_U≤2m_*` anche ai target periodici. Il label è il minimo **antenato**, non il minimo futuro dell'orbita.

La fonte12, §12, equazione36, pone esplicitamente un root positivo dispari unità nonperiodico e controlla l'intera unione dei bacini dei genitori con m_*>M mediante una cella comune di landing. Il tail completo non va esteso al genitore ciclico. La successiva entropia ai periodici separa quel genitore.

Nel dominio nonreturn, g(n)≥εn implica β_n≥ε/κ. Scegliere M grande nel tail rende positiva la massa di qualche genitore con m_*≤M. Il passaggio precedente produce un seed unità≤2M; il primo arrivo dà F(n)≥n/(2MP₀). Questa direzione g-heavy⇒F-heavy usa il tail e il suo dominio. La direzione F-heavy⇒g-heavy usa soltanto armonicità e floor. Non è stata postulata un'equivalenza uniforme su tutti i cicli.

## Stato verificativo

Ho controllato enunciati, normalizzazioni, passaggi locali e dipendenze delle catene citate. Non è una nuova verifica integrale dei manoscritti o dei loro progetti formali. Gli input sono risultati provati nei testi letti, importati esternamente e con certificazioni non rieseguite; il lower critico di A e la nondivergenza restano aperti.
