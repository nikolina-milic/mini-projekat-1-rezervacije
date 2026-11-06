"""Testovi servisa koriste zamjenski izvor i zamjenski izvjestavac."""

from collections.abc import Sequence
from decimal import Decimal

import pytest

from rezervacije.modeli import Izvjestaj, Rezervacija
from rezervacije.servis import ObradaRezervacija


class LazniIzvor:
    """Zamjenski izvor bez datoteka i baze podataka."""

    def __init__(self, rezervacije: Sequence[Rezervacija]) -> None:
        self._rezervacije = tuple(rezervacije)
        self.broj_poziva = 0

    def ucitaj(self) -> Sequence[Rezervacija]:
        self.broj_poziva += 1
        return self._rezervacije


class PrateciIzvjestavac:
    """Zamjenski izvjestavac koji pamti primljene izvjestaje."""

    def __init__(self) -> None:
        self.izvjestaji: list[Izvjestaj] = []

    def objavi(self, izvjestaj: Izvjestaj) -> None:
        self.izvjestaji.append(izvjestaj)


def napravi_rezervaciju(
    gost: str,
    noci: int,
    cijena_noci: str,
) -> Rezervacija:
    return Rezervacija(gost, noci, Decimal(cijena_noci))


def test_obrada_racuna_iznos_jedne_rezervacije() -> None:
    izvor = LazniIzvor([napravi_rezervaciju("Ana", 3, "80")])
    izvjestavac = PrateciIzvjestavac()

    rezultat = ObradaRezervacija(izvor, izvjestavac).obradi()

    assert rezultat.stavke[0].gost == "Ana"
    assert rezultat.stavke[0].iznos == Decimal("240")
    assert rezultat.ukupan_iznos == Decimal("240")


def test_obrada_racuna_ukupan_iznos_vise_rezervacija() -> None:
    izvor = LazniIzvor(
        [
            napravi_rezervaciju("Ana", 3, "80"),
            napravi_rezervaciju("Marko", 5, "65"),
            napravi_rezervaciju("Ivana", 2, "120"),
        ]
    )
    izvjestavac = PrateciIzvjestavac()

    rezultat = ObradaRezervacija(izvor, izvjestavac).obradi()

    assert [stavka.iznos for stavka in rezultat.stavke] == [
        Decimal("240"),
        Decimal("325"),
        Decimal("240"),
    ]
    assert rezultat.ukupan_iznos == Decimal("805")


def test_prazan_izvor_daje_prazan_izvjestaj() -> None:
    izvor = LazniIzvor([])
    izvjestavac = PrateciIzvjestavac()

    rezultat = ObradaRezervacija(izvor, izvjestavac).obradi()

    assert rezultat.stavke == ()
    assert rezultat.ukupan_iznos == Decimal("0")
    assert izvjestavac.izvjestaji == [rezultat]


def test_servis_ucitava_jednom_i_objavljuje_isti_rezultat() -> None:
    izvor = LazniIzvor([napravi_rezervaciju("Ana", 1, "99.99")])
    izvjestavac = PrateciIzvjestavac()

    rezultat = ObradaRezervacija(izvor, izvjestavac).obradi()

    assert izvor.broj_poziva == 1
    assert izvjestavac.izvjestaji == [rezultat]


@pytest.mark.parametrize(
    ("gost", "noci", "cijena", "poruka"),
    [
        ("", 1, "10", "Ime gosta"),
        ("Ana", 0, "10", "Broj nocenja"),
        ("Ana", 1, "-1", "Cijena nocenja"),
    ],
)
def test_rezervacija_odbija_neispravne_podatke(
    gost: str,
    noci: int,
    cijena: str,
    poruka: str,
) -> None:
    with pytest.raises(ValueError, match=poruka):
        napravi_rezervaciju(gost, noci, cijena)
