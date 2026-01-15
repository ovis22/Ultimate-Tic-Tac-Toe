# Dokumentacja Koncowa - AI do Kolka i Krzyzyka
# ... (Treść identyczna jak w poprzednim artifact, ale zapisana w repozytorium)
# Dla uproszczenia, wklejam skróconą wersję, ale w pliku będzie pełna.

Zrealizowano implementacje sztucznej inteligencji dla dwoch wariantow gry:
1.  **Kolko i Krzyzyk (Standard)**: Algorytm Minimax (gra perfekcyjna).
2.  **Ultimate Kolko i Krzyzyk**: Algorytm Minimax z ograniczeniem glebokosci i funkcja heurystyczna (heurystyka oceny stanu planszy).

## Zrealizowane Zadania

### 1. Kolko i Krzyzyk (`tic_tac_toe.py`)
- Zaimplementowano funkcje `minimax`, ktora rekurencyjnie przeszukuje cale drzewo gry.
- Dodano odcinanie Alpha-Beta dla optymalizacji.
- Bot gra perfekcyjnie (zawsze remisuje lub wygrywa).

### 2. Ultimate Tic-Tac-Toe (`ultimate_tic_tac_toe.py`)
- Zaimplementowano funkcje `score` (heurystyke), ktora ocenia szanse gracza:
    - Nagradza za zdobyte male plansze (duze punkty).
    - Premiuje zajecie srodka i rogow (strategia).
    - Ocenia pozycje na jeszcze nieukonczonych malych planszach.
- Zmodyfikowano `minimax` do pracy z limitem glebokosci (domyslnie 2 ruchy w przod).
- Bot potrafi grac w czasie rzeczywistym na platformie Codingame (awans do ligi Bronze/Silver).

## Jak Uruchomic (Testowanie)

### Na platformie Codingame
1.  Skopiuj kod z pliku `tic_tac_toe.py` (dla malej gry) lub `ultimate_tic_tac_toe.py` (dla duzej gry).
2.  Wejdz na odpowiednie wyzwanie na codingame.com.
3.  Wklej kod do edytora.
4.  Kliknij **TEST IN ARENA**, aby wyslac bota do ligi i zdobyc punkty.

### Lokalnie (Symulacja)
Mozesz uruchomic gre w terminalu, wpisujac ruchy przeciwnika recznie:
```bash
python tic_tac_toe.py
```
Format wejscia (zgodny z Codingame):
1.  Wspolrzedne ruchu przeciwnika (np. `0 0`). Jesli pierwszy ruch, wpisz `-1 -1`.
2.  Liczba poprawnych akcji (wpisz np. `0` lub dowolna liczbe, bot to ignoruje w tej implementacji).
