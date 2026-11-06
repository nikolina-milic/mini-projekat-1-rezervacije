"""Komandni ulaz za pokretanje obrade rezervacija."""

import argparse
from pathlib import Path

from rezervacije.adapteri import CsvIzvorRezervacija, TekstualniIzvjestavac
from rezervacije.servis import ObradaRezervacija


def napravi_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Obrada rezervacija iz CSV datoteke")
    parser.add_argument("ulaz", type=Path, help="Putanja do ulazne CSV datoteke")
    parser.add_argument("izlaz", type=Path, help="Putanja za tekstualni izvjestaj")
    return parser


def main() -> None:
    argumenti = napravi_parser().parse_args()
    servis = ObradaRezervacija(
        izvor=CsvIzvorRezervacija(argumenti.ulaz),
        izvjestavac=TekstualniIzvjestavac(argumenti.izlaz),
    )
    izvjestaj = servis.obradi()
    print(f"Obradjeno rezervacija: {len(izvjestaj.stavke)}")
    print(f"Ukupan iznos: {izvjestaj.ukupan_iznos:.2f}")


if __name__ == "__main__":
    main()
