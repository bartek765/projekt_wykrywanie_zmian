# System Wykrywania Zmian w Plikach (Projekt 1)

## Opis projektu
Aplikacja konsolowa służąca do monitorowania integralności plików. Program weryfikuje, czy zawartość wskazanego pliku uległa zmianie od czasu ostatniego uruchomienia, wykorzystując bezwzględne ścieżki i algorytm bezpiecznego hashowania SHA-256 (bez analizowania struktury wewnętrznej tekstu).

## Lokalizacja rozwiązania
Główna logika aplikacji oraz punkt wejściowy znajdują się w pliku: `file_monitor.py`.

## Wymagania
- Python 3.x

## Instrukcja uruchomienia
Aby sprawdzić plik, należy wywołać program w terminalu, podając ścieżkę do pliku jako argument:
```bash
python file_monitor.py <ścieżka_do_pliku>