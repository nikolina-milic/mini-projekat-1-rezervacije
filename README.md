# Mini projekat 1: refaktoring obrade rezervacija

Projekat refaktoriše monolitnu obradu rezervacija u male komponente sa jasno
odvojenim odgovornostima. Rješenje koristi Python 3.12, type hints, `Protocol`
i `pytest`.

## Polazni problem

Polazna klasa `legacy/monolit.py` istovremeno:

- učitava podatke iz datoteke;
- računa iznose;
- čuva izvještaj;
- simulira slanje obavještenja.

Zbog toga ima više razloga za promjenu i krši Single Responsibility princip.
Takođe direktno zavisi od datoteka i `print` funkcije, pa je teško testirati je
bez rada sa stvarnim ulazom i izlazom.

## Dizajn poslije refaktoringa

```text
CsvIzvorRezervacija ─┐
                     ├─> ObradaRezervacija ─> Izvjestavac
LazniIzvor (test) ───┘                         ├─ TekstualniIzvjestavac
                                               └─ PrateciIzvjestavac (test)
```

- `modeli.py` sadrži nepromjenjive domenske modele i računanje iznosa.
- `protokoli.py` definiše male ugovore `IzvorRezervacija` i `Izvjestavac`.
- `servis.py` samo koordinira učitavanje, obračun i izvještavanje.
- `adapteri.py` sadrži konkretan CSV ulaz i tekstualni izlaz.
- `tests/` koristi zamjenski izvor i izvještavač, bez stvarnih datoteka u
  testovima poslovne logike.

### Primijenjeni principi

**S — Single Responsibility:** model validira podatke i računa iznos, CSV
adapter čita CSV, izvještavač upisuje rezultat, a servis koordinira slučaj
upotrebe.

**D — Dependency Inversion:** `ObradaRezervacija` ne kreira CSV čitač niti
tekstualni izvještavač. Prima objekte koji zadovoljavaju male `Protocol`
ugovore kroz konstruktor. Zbog toga test može ubaciti zamjenske objekte.

Rješenje podržava i Open/Closed princip: novi izvor, na primjer baza podataka,
ili novi način izvještavanja mogu se dodati bez izmjene servisa.

## Struktura projekta

```text
mini_projekat_1_rezervacije/
├── data/rezervacije.csv
├── legacy/monolit.py
├── src/rezervacije/
│   ├── __init__.py
│   ├── __main__.py
│   ├── adapteri.py
│   ├── modeli.py
│   ├── protokoli.py
│   └── servis.py
├── tests/
│   ├── test_adapteri.py
│   └── test_servis.py
├── pyproject.toml
└── README.md
```

## Pokretanje

Potrebno je imati Python 3.12 ili noviji.

```bash
python -m venv .venv
```

Aktivacija na Windowsu:

```powershell
.venv\Scripts\Activate.ps1
```

Instalacija projekta i razvojnih alata:

```bash
python -m pip install -e ".[dev]"
```

Pokretanje testova i provjere stila:

```bash
pytest
ruff check .
ruff format --check .
```

Pokretanje primjera:

```bash
python -m rezervacije data/rezervacije.csv izvjestaj.txt
```

Očekivani ispis:

```text
Obradjeno rezervacija: 3
Ukupan iznos: 805.00
```

## Testovi

Poslovna logika ima više od tražena tri `pytest` testa sa zamjenskim izvorom:

1. obračun jedne rezervacije;
2. obračun više rezervacija i ukupnog iznosa;
3. obrada praznog izvora;
4. provjera da servis učitava jednom i objavljuje isti rezultat;
5. validacija neispravnih podataka.

Dodatna dva testa provjeravaju konkretne CSV i tekstualne adaptere.

## Rad sa AI asistentom

### Upit 1: analiza i refaktoring

```text
Uloga: iskusni Python softverski arhitekta.
Analiziraj priloženu monolitnu klasu za obradu rezervacija. Refaktoriši je za
Python 3.12 primjenom Single Responsibility i Dependency Inversion principa.
Definiši odvojene Protocol ugovore za izvor rezervacija i izvještavanje.
Koristi dataclass modele, type hints i dependency injection kroz konstruktor.
Ne uvodi apstrakcije koje zadatak ne zahtijeva. Prikaži strukturu datoteka i
objasni odgovornost svake komponente.
```

**Provjera i ispravke AI prijedloga:**

- Prvi nacrt je pravio `CsvIzvorRezervacija` direktno unutar servisa. To je
  ispravljeno ubrizgavanjem `IzvorRezervacija` protokola kroz konstruktor.
- Prvi nacrt je imao jedan veliki protokol za učitavanje i izvještavanje.
  Razdvojen je na dva mala ugovora da klijenti ne zavise od metoda koje ne
  koriste.
- Za novac je prvo korišćen `float`. Zamijenjen je sa `Decimal` da sabiranje
  cijena ne zavisi od binarne reprezentacije decimalnih brojeva.
- Dodata je validacija praznog gosta, broja noćenja i negativne cijene, jer je
  prvi nacrt prihvatao neispravno stanje modela.

### Upit 2: testovi i kritički pregled

```text
Napiši najmanje tri pytest testa za servis ObradaRezervacija. Testovi ne smiju
čitati CSV niti pisati izvještaj na disk. Napravi ručni zamjenski izvor podataka
i izvještavač koji pamti primljeni rezultat. Pokrij jednu rezervaciju, više
rezervacija, prazan izvor i provjeru saradnje sa zavisnostima. Zatim navedi
granične slučajeve koje testovi još ne pokrivaju.
```

**Provjera i ispravke AI prijedloga:**

- AI testovi su prvo provjeravali samo ukupan zbir. Dodate su provjere
  pojedinačnih stavki i identiteta objavljenog rezultata.
- Zamjenski izvor sada broji pozive, pa test potvrđuje da servis ne učitava
  podatke više puta.
- Dodati su parametrizovani testovi za prazno ime, nula noćenja i negativnu
  cijenu.
- Dodati su odvojeni integracioni testovi adaptera, dok testovi servisa ostaju
  brzi i nezavisni od datoteka.

## Kratko objašnjenje za odbranu

Servis zavisi od ponašanja, a ne od konkretnih klasa. Python `Protocol`
omogućava strukturno tipiziranje: objekat ne mora naslijediti protokol, dovoljno
je da ima odgovarajuću metodu. Zato `LazniIzvor` i `PrateciIzvjestavac` u
testovima mogu zamijeniti produkcijske adaptere. Ovakav dizajn smanjuje
povezanost, ubrzava testove i omogućava dodavanje novih izvora ili izvještaja
bez izmjene poslovne logike.
