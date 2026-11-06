"""Domenski modeli za rezervacije i izvjestaj."""

from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True, slots=True)
class Rezervacija:
    """Jedna rezervacija gosta."""

    gost: str
    noci: int
    cijena_noci: Decimal

    def __post_init__(self) -> None:
        if not self.gost.strip():
            raise ValueError("Ime gosta ne smije biti prazno")
        if self.noci <= 0:
            raise ValueError("Broj nocenja mora biti pozitivan")
        if self.cijena_noci < Decimal("0"):
            raise ValueError("Cijena nocenja ne smije biti negativna")

    @property
    def iznos(self) -> Decimal:
        """Vrati ukupan iznos rezervacije."""
        return self.cijena_noci * self.noci


@dataclass(frozen=True, slots=True)
class StavkaIzvjestaja:
    """Iznos obracunat za jednog gosta."""

    gost: str
    iznos: Decimal


@dataclass(frozen=True, slots=True)
class Izvjestaj:
    """Nepromjenjiv rezultat obrade rezervacija."""

    stavke: tuple[StavkaIzvjestaja, ...]

    @property
    def ukupan_iznos(self) -> Decimal:
        """Vrati zbir svih stavki izvjestaja."""
        return sum((stavka.iznos for stavka in self.stavke), Decimal("0"))
