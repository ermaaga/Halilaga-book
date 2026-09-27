#!/usr/bin/env python3
"""Trasforma i capitoli di romanzo/ (o romanzo-sq/) in un audiolibro MP3.

Usa le voci neurali gratuite di Microsoft Edge tramite edge-tts, che parlano
sia italiano sia albanese. Serve una connessione a internet.

Installazione (una volta sola):
    pip install edge-tts

Uso:
    python3 crea_audiolibro.py                  # italiano, tutti i capitoli
    python3 crea_audiolibro.py --sq             # albanese
    python3 crea_audiolibro.py --capitoli 0 1   # solo prologo e capitolo 1
    python3 crea_audiolibro.py --voce it-IT-ElsaNeural
    python3 crea_audiolibro.py --velocita -10%  # più lento (anche +10%)
    python3 crea_audiolibro.py --unico          # crea anche un file unico con tutto il libro
    python3 crea_audiolibro.py --prova          # mostra il testo che verrebbe letto, senza internet

Voci consigliate:
    italiano: it-IT-DiegoNeural (uomo), it-IT-GiuseppeNeural (uomo),
              it-IT-ElsaNeural (donna), it-IT-IsabellaNeural (donna)
    albanese: sq-AL-IlirNeural (uomo), sq-AL-AnilaNeural (donna)
Per l'elenco completo: edge-tts --list-voices

I file finiscono in audiolibro/it/ (o audiolibro/sq/), un MP3 per capitolo.
Non vengono salvati su git (sono pesanti): vedi .gitignore.
"""
import argparse
import asyncio
import re
import sys
from pathlib import Path

RADICE = Path(__file__).parent

LINGUE = {
    "it": {
        "cartella": "romanzo",
        "voce": "it-IT-DiegoNeural",
        "titolo": "Il Mancino del Sultano. La leggenda di Halil Halilaga. Di Ermal Halilaga.",
        "capitolo": "Capitolo {n}.",
        "parti": {
            1: "Parte prima. Leshtej, 1787.",
            3: "Parte seconda. La guerra, 1787-1792.",
            7: "Parte terza. Il ritorno, 1792-1799.",
        },
    },
    "sq": {
        "cartella": "romanzo-sq",
        "voce": "sq-AL-IlirNeural",
        "titolo": "Mëngjarashi i Sulltanit. Legjenda e Halil Halilagës. Nga Ermal Halilaga.",
        "capitolo": "Kapitulli {n}.",
        "parti": {
            1: "Pjesa e parë. Leshtej, 1787.",
            3: "Pjesa e dytë. Lufta, 1787-1792.",
            7: "Pjesa e tretë. Kthimi, 1792-1799.",
        },
    },
}


def testo_capitolo(path, L):
    """Restituisce (numero, testo da leggere ad alta voce) per un file .md."""
    grezzo = re.sub(r"<!--.*?-->", "", path.read_text(encoding="utf-8"), flags=re.S)
    righe = grezzo.strip().splitlines()
    titolo = righe[0].lstrip("#").strip() if righe and righe[0].startswith("#") else ""
    corpo = "\n".join(righe[1:]).strip()
    if not corpo:
        return None
    n = int(path.stem[:2])

    pezzi = []
    if n == 0:
        pezzi.append(L["titolo"])
    if n in L["parti"]:
        pezzi.append(L["parti"][n])
    if n == 0 or "epilogo" in path.stem:
        pezzi.append(titolo + ".")
    else:
        pezzi.append(L["capitolo"].format(n=n) + " " + titolo + ".")

    for blocco in re.split(r"\n\s*\n", corpo):
        blocco = " ".join(blocco.split())
        if not blocco:
            continue
        if blocco == "***":
            pezzi.append("…")  # cambio di scena: una pausa
            continue
        blocco = re.sub(r"\*\*?([^*]+)\*\*?", r"\1", blocco)  # via corsivo e grassetto
        pezzi.append(blocco)
    # Le righe vuote tra i paragrafi fanno fare una pausa alla voce
    return n, "\n\n".join(pezzi)


async def sintetizza(testo, voce, velocita, uscita, tentativi=3):
    import edge_tts

    for i in range(1, tentativi + 1):
        try:
            await edge_tts.Communicate(testo, voce, rate=velocita).save(str(uscita))
            return
        except Exception as e:  # rete instabile: riprova
            if i == tentativi:
                raise
            print(f"   errore ({e.__class__.__name__}), riprovo…")
            await asyncio.sleep(3 * i)


def main():
    ap = argparse.ArgumentParser(description="Crea l'audiolibro dai capitoli del romanzo.")
    ap.add_argument("--sq", action="store_true", help="versione albanese")
    ap.add_argument("--voce", help="voce edge-tts (default: una per lingua)")
    ap.add_argument("--velocita", default="+0%", help="es. -10%% o +5%%")
    ap.add_argument("--capitoli", nargs="*", type=int, help="numeri dei capitoli (0 = prologo, 16 = epilogo)")
    ap.add_argument("--unico", action="store_true", help="unisce tutto in un solo MP3")
    ap.add_argument("--prova", action="store_true", help="stampa il testo senza generare l'audio")
    args = ap.parse_args()

    lingua = "sq" if args.sq else "it"
    L = LINGUE[lingua]
    voce = args.voce or L["voce"]
    cartella_out = RADICE / "audiolibro" / lingua

    capitoli = []
    for path in sorted((RADICE / L["cartella"]).glob("*.md")):
        risultato = testo_capitolo(path, L)
        if risultato and (args.capitoli is None or risultato[0] in args.capitoli):
            capitoli.append((path, *risultato))
    if not capitoli:
        sys.exit("Nessun capitolo scritto da leggere.")

    if args.prova:
        for path, n, testo in capitoli:
            print(f"===== {path.name}: {len(testo.split())} parole =====")
            print(testo[:600] + ("…" if len(testo) > 600 else ""))
            print()
        return

    try:
        import edge_tts  # noqa: F401
    except ImportError:
        sys.exit("Manca edge-tts. Installalo con:  pip install edge-tts")

    cartella_out.mkdir(parents=True, exist_ok=True)
    creati = []
    for path, n, testo in capitoli:
        uscita = cartella_out / f"{path.stem}.mp3"
        print(f"→ {path.name} ({len(testo.split())} parole) → {uscita.relative_to(RADICE)}")
        asyncio.run(sintetizza(testo, voce, args.velocita, uscita))
        creati.append(uscita)

    if args.unico and creati:
        # Gli MP3 di edge-tts hanno lo stesso formato: si possono accodare
        unico = cartella_out / f"Romanzo_Halil_{lingua}.mp3"
        with open(unico, "wb") as f:
            for c in creati:
                f.write(c.read_bytes())
        print(f"File unico: {unico.relative_to(RADICE)}")

    print(f"Fatto: {len(creati)} capitoli, voce {voce}.")


if __name__ == "__main__":
    main()
