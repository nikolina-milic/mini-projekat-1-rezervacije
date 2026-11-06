"""Mali ugovori koje servis koristi kroz dependency inversion."""

from collections.abc import Sequence
from typing import Protocol

from rezervacije.modeli import Izvjestaj, Rezervacija


class IzvorRezervacija(Protocol):
    """Ugovor za bilo koji izvor rezervacija."""

    def ucitaj(self) -> Sequence[Rezervacija]:
        """Ucitaj i vrati rezervacije."""
        ...


class Izvjestavac(Protocol):
    """Ugovor za bilo koji nacin objavljivanja izvjestaja."""

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        """Objavi dobijeni izvjestaj."""
        ...
