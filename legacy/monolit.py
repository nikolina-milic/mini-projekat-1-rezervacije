"""Polazni monolitni primjer prije refaktoringa.

Ovaj modul je sacuvan samo radi poredjenja i aplikacija ga ne koristi.
"""

from pathlib import Path


class UpravljanjeRezervacijama:
    """Klasa koja krsi SRP jer ucitava, racuna, cuva i obavjestava."""

    def __init__(self, putanja: Path) -> None:
        self.putanja = putanja

    def ucitaj(self) -> list[list[str]]:
        with self.putanja.open(encoding="utf-8") as datoteka:
            return [red.strip().split(",") for red in datoteka]

    def izracunaj_iznos(self, rezervacija: list[str]) -> float:
        return int(rezervacija[1]) * float(rezervacija[2])

    def sacuvaj_izvjestaj(self, iznosi: list[float]) -> None:
        Path("izvjestaj.txt").write_text(str(iznosi), encoding="utf-8")

    def posalji_mail(self, iznosi: list[float]) -> None:
        print("Poslato:", sum(iznosi))
