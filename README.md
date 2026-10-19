# Pygame Pong

Kétjátékos Pong játék Python és Pygame használatával. A játék háromféle, futás közben előállított hanghatást tartalmaz; külön hangfájlok nem szükségesek.

## Futtatás

Python 3.10 vagy újabb ajánlott.

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python pong.py
```

A tesztek futtatásához:

```bash
python -m pip install -r requirements-dev.txt
pytest -q
```

## Irányítás

- Bal játékos: **W** és **S**
- Jobb játékos: **fel** és **le** nyílbillentyű
- **P**: szünet / folytatás
- **R**: új játék, pontszám nullázása
- **Esc**: kilépés

Az nyer, aki először eléri a 7 pontot.

## Hanghatások

- **Ütőtalálat:** rövid, magas hang
- **Falról visszapattanás:** rövidebb, mélyebb hang
- **Pontszerzés:** magasabb hang

A hangmintákat a program a `make_tone()` függvényben, matematikailag állítja elő. Így nincs szükség külső WAV- vagy MP3-fájlokra. A hangok frekvenciája és hossza a `create_sounds()` függvényben módosítható.

## Tanulási célok

- koordináták és sebesség;
- ciklusok és eseménykezelés;
- ütközésvizsgálat;
- függvények és osztályok;
- hanggenerálás és hanghatások;
- egységtesztelés `pytest` segítségével.

## Diákfeladatok

A részletes feladatokat a [tasks.md](tasks.md) fájl tartalmazza.
