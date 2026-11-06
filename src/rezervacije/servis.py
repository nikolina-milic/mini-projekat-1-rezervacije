"""Aplikacioni servis koji koordinira obradu rezervacija."""

from rezervacije.modeli import Izvjestaj, StavkaIzvjestaja
from rezervacije.protokoli import Izvjestavac, IzvorRezervacija


class ObradaRezervacija:
    """Ucitaj rezervacije, obracunaj iznose i objavi izvjestaj."""

    def __init__(
        self,
        izvor: IzvorRezervacija,
        izvjestavac: Izvjestavac,
    ) -> None:
        self._izvor = izvor
        self._izvjestavac = izvjestavac

    def obradi(self) -> Izvjestaj:
        """Izvrsi cijeli slucaj upotrebe i vrati isti objavljeni izvjestaj."""
        stavke = tuple(
            StavkaIzvjestaja(gost=rezervacija.gost, iznos=rezervacija.iznos)
            for rezervacija in self._izvor.ucitaj()
        )
        izvjestaj = Izvjestaj(stavke=stavke)
        self._izvjestavac.objavi(izvjestaj)
        return izvjestaj
