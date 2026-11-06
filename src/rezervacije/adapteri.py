"""Konkretni adapteri za CSV ulaz i tekstualni izvjestaj."""

import csv
from decimal import Decimal, InvalidOperation
from pathlib import Path

from rezervacije.modeli import Izvjestaj, Rezervacija


class CsvIzvorRezervacija:
    """Ucitaj rezervacije iz CSV datoteke."""

    _obavezne_kolone = {"gost", "noci", "cijena_noci"}

    def __init__(self, putanja: Path) -> None:
        self._putanja = putanja

    def ucitaj(self) -> list[Rezervacija]:
        rezervacije: list[Rezervacija] = []

        with self._putanja.open(newline="", encoding="utf-8") as datoteka:
            citac = csv.DictReader(datoteka)
            kolone = set(citac.fieldnames or [])
            nedostaju = self._obavezne_kolone - kolone
            if nedostaju:
                spisak = ", ".join(sorted(nedostaju))
                raise ValueError(f"Nedostaju CSV kolone: {spisak}")

            for broj_reda, red in enumerate(citac, start=2):
                try:
                    rezervacija = Rezervacija(
                        gost=(red["gost"] or "").strip(),
                        noci=int(red["noci"]),
                        cijena_noci=Decimal(red["cijena_noci"]),
                    )
                except (InvalidOperation, TypeError, ValueError) as greska:
                    raise ValueError(
                        f"Neispravni podaci u CSV redu {broj_reda}: {red}"
                    ) from greska
                rezervacije.append(rezervacija)

        return rezervacije


class TekstualniIzvjestavac:
    """Sacuvaj citljiv izvjestaj u tekstualnu datoteku."""

    def __init__(self, putanja: Path) -> None:
        self._putanja = putanja

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        redovi = [f"{stavka.gost}: {stavka.iznos:.2f}" for stavka in izvjestaj.stavke]
        redovi.append(f"UKUPNO: {izvjestaj.ukupan_iznos:.2f}")
        self._putanja.write_text("\n".join(redovi) + "\n", encoding="utf-8")
