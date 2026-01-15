# Raport Projektowy: Algorytmy Przeszukiwania (Minimax)

**Autor:** Dominik Łakomy  
**Nr albumu:** 29163  
**Przedmiot:**  Sztuczna Inteligencja (Laboratoria)  
**Technologia:** Python 3.9+ (Standard Library)

Zrealizowano implementację sztucznej inteligencji dla dwóch wariantów gry:
1.  **Kółko i Krzyżyk (Standard)**: Algorytm Minimax (gra perfekcyjna).
2.  **Ultimate Kółko i Krzyżyk**: Algorytm Minimax z ograniczeniem głębokości i funkcją heurystyczną (heurystyka oceny stanu planszy).

## Zrealizowane Zadania

### 1. Kółko i Krzyżyk (`tic_tac_toe.py`)
- Zaimplementowano funkcję `minimax`, która rekurencyjnie przeszukuje całe drzewo gry.
- Dodano odcinanie Alpha-Beta dla optymalizacji.
- Bot gra perfekcyjnie (zawsze remisuje lub wygrywa).

### 2. Ultimate Tic-Tac-Toe (`ultimate_tic_tac_toe.py`)
- Zaimplementowano funkcję `score` (heurystykę), która ocenia szanse gracza:
    - Nagradza za zdobyte małe plansze (duże punkty).
    - Premiuje zajęcie środka i rogów (strategia).
    - Ocenia pozycję na jeszcze nieukończonych małych planszach.
- Zmodyfikowano `minimax` do pracy z **pogłębianiem iteracyjnym** (bot stara się obliczyć jak najwięcej ruchów w przód w dostępnym czasie).
- Bot potrafi grać w czasie rzeczywistym na platformie Codingame.
- **Wynik weryfikacji:** Bot zakwalifikował się do **Złotej Ligi (Gold League)** (awans potwierdzony w systemie).

## Strategia i Algorytmika

### 1. Strategia Wagowa (Heurystyka)
Bot preferuje pola strategiczne (środek i rogi). Wagi przypisane do pól na dużej planszy:

| 1.2 (Róg) | 1.0       | 1.2 (Róg) |
|-----------|-----------|-----------|
| **1.0** | **2.0 (Środek)** | **1.0** |
| **1.2 (Róg)** | **1.0** | **1.2 (Róg)** |

### 2. Optymalizacja Czasowa (Real-Time)
Bot działa w rygorystycznym reżimie czasu rzeczywistego (wymóg Codingame: < 100ms na ruch). 
Zaimplementowano mechanizm **Iterative Deepening** (Pogłębianie Iteracyjne), który:
- Rozpoczyna szukanie od głębokości 1.
- Zwiększa głębokość w każdej iteracji (aż do limitu 10).
- Przerywa przeszukiwanie drzewa Minimax, gdy czas wykonania zbliża się do limitu (95ms), zwracając najlepszy dotychczas znaleziony wynik.

### 3. Schemat Punktacji (Heurystyka)
W funkcji `score` w `ultimate_tic_tac_toe.py` zaimplementowano zaawansowaną logikę oceny:
- **Globalna Wygrana**: +/- 10000 pkt
- **Zdobycie Małej Planszy**: +/- 100 pkt * waga planszy
- **"Prawie Wygrana" (2 znaki w linii)**: +/- 5 pkt * waga planszy (kluczowe dla Ligi Złotej)
- **Kontrola Środka**: +/- 2 pkt * waga planszy

## Struktura Projektu

- **`tic_tac_toe.py`** – Implementacja dla klasycznej planszy 3x3 (rozwiązanie kompletne, zawsze remisuje lub wygrywa).
- **`ultimate_tic_tac_toe.py`** – Implementacja dla wariantu Ultimate (9 plansz 3x3) z limitem głębokości (depth=10) i zaawansowaną heurystyką oceny pozycji.

## Wymagania Techniczne

- **Python 3.9+** (projekt wykorzystuje `dataclasses` oraz `type hinting` dla list `list[list[CellState]]`).
- **Standard Library Only**: Projekt nie wymaga żadnych zewnętrznych bibliotek (czysty Python).

## Zrzuty Ekranu: Postęp w Ligach

## Zrzuty Ekranu: Postęp w Ligach
<br>

![Liga Drewniana](welna.png)
*Rys 1. Początek w Lidze Drewnianej (Wood League)*
<br>

![Liga Brązowa](braz.png)
*Rys 2. Awans do Ligi Brązowej (Bronze League)*
<br>

![Liga Srebrna](srebro.png)
*Rys 3. Walka w Lidze Srebrnej (Silver League)*
<br>

![Liga Złota](zloto.png)
*Rys 4. Wejście do Ligi Złotej (Gold League)*
<br>

![Ranking](zloto1.png)
*Rys 5. Potwierdzenie pozycji w rankingu Złotej Ligi*
<br>

## Jak Uruchomić (Testowanie)

### Na platformie Codingame
1.  Skopiuj kod z pliku `tic_tac_toe.py` (dla małej gry) lub `ultimate_tic_tac_toe.py` (dla dużej gry).
2.  Wejdź na odpowiednie wyzwanie na codingame.com.
3.  Wklej kod do edytora.
4.  Kliknij **TEST IN ARENA**, aby wysłać bota do ligi i zdobyć punkty.

### Lokalnie (Symulacja)
Możesz uruchomić grę w terminalu, wpisując ruchy przeciwnika ręcznie:
```bash
python tic_tac_toe.py
```
Format wejścia (zgodny z Codingame):
1.  Współrzędne ruchu przeciwnika (np. `0 0`). Jeśli pierwszy ruch, wpisz `-1 -1`.
2.  Liczba poprawnych akcji (wpisz np. `0` lub dowolną liczbę, bot to ignoruje w tej implementacji).
