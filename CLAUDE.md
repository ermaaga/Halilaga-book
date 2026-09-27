# Il Mancino del Sultano

Romanzo storico sulla famiglia Halilaga. Si lavora in italiano.

Prima di fare qualsiasi cosa, leggi:
1. `CONTESTO_Il_Mancino_del_Sultano.md`: fonti, trama approvata, preferenze dell'autore. È il riferimento.
2. `NOTE-DI-LAVORO.md`: analisi del testo attuale, confronto con la trama approvata, domande aperte.

- `romanzo/NN.md`: **la nuova stesura** (dal 26/09/2026), un file per capitolo (`00-prologo.md` … `16-epilogo.md`), secondo la "Scaletta v2" in `NOTE-DI-LAVORO.md`. I capitoli non ancora scritti contengono solo il titolo e un commento `<!-- SCALETTA: ... -->`.
- `python3 crea_docx.py` unisce i capitoli già scritti in `Romanzo_Halil.docx` (`--bozze` include anche quelli vuoti). Richiede `pip install python-docx`. Rigenera il Word dopo ogni capitolo nuovo o modificato e fai commit anche del .docx.
- `romanzo-sq/NN.md`: **traduzione albanese** della nuova stesura, stessi nomi di file. `python3 crea_docx.py --sq` crea `Romanzo_Halil_sq.docx`. Quando si modifica un capitolo italiano, va aggiornata anche la traduzione.
- `manoscritto/cap-NNN.md`: la **vecchia versione** (estratta da `Il_Mancino_del_Sultano.docx`). Serve solo come materiale da cui attingere.
- `HalilagaBook.pdf`: libro fonte in albanese (foto). È già stato letto: non rileggerlo se non serve.
- Non riscrivere capitoli già approvati senza indicazione esplicita dell'autore.

## "Dove eravamo rimasti?"

Quando l'autore chiede "dove eravamo rimasti" (o simili):
1. Riassumi in 3–4 righe lo stato del lavoro, leggendo `NOTE-DI-LAVORO.md` e `git log`.
2. Fagli **una domanda alla volta** tra quelle aperte in fondo a `NOTE-DI-LAVORO.md`, partendo dalla più importante (il segreto della mano sinistra). L'autore scrive dal cellulare: domande brevi, con le opzioni numerate.
3. Registra ogni risposta nel file di note (sezione "Decisioni prese"), poi fai commit e push.
