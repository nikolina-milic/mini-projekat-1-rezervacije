"""Integracioni testovi konkretnih CSV i tekstualnih adaptera."""

from decimal import Decimal

from rezervacije.adapteri import CsvIzvorRezervacija, TekstualniIzvjestavac
from rezervacije.modeli import Izvjestaj, StavkaIzvjestaja


def test_csv_izvor_ucitava_rezervacije(tmp_path) -> None:
    csv_putanja = tmp_path / "rezervacije.csv"
    csv_putanja.write_text(
        "gost,noci,cijena_noci\nAna,2,100\nMarko,3,50.50\n",
        encoding="utf-8",
    )

    rezervacije = CsvIzvorRezervacija(csv_putanja).ucitaj()

    assert [rezervacija.gost for rezervacija in rezervacije] == ["Ana", "Marko"]
    assert rezervacije[1].iznos == Decimal("151.50")


def test_tekstualni_izvjestavac_upisuje_stavke_i_ukupan_iznos(tmp_path) -> None:
    putanja = tmp_path / "izvjestaj.txt"
    izvjestaj = Izvjestaj(
        stavke=(
            StavkaIzvjestaja("Ana", Decimal("200")),
            StavkaIzvjestaja("Marko", Decimal("151.50")),
        )
    )

    TekstualniIzvjestavac(putanja).objavi(izvjestaj)

    assert putanja.read_text(encoding="utf-8") == (
        "Ana: 200.00\nMarko: 151.50\nUKUPNO: 351.50\n"
    )
