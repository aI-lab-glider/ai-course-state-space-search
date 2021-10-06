# Instrukcje do instrukcji

## Podstawowe informacje
1. Struktura
    1. Problemy przyjmują stan początkowy i końcowy zagadnienia.
    1. Definiuj osobno *Problem* i *Stan* dla danego zagadnienia.
    1. Metody klasy *Problem* i *Stan* przyjmują i zwracają typy argumentów jakie zostały zdefiniowane w _/base_.
    1. Nie musisz tworzyć żadnych nowych plików.

## N Puzzle 

1. Problem
    1. Napisz metodę *actions*. Metoda ma zwracać listę możliwych ruchów tj. [dół, góra, prawo, lewo] z aktualnego stanu. Stan jest podawany na wejściu.  
    np.
    ```
    2 8 3
    1 6 4
    0 7 5
    ```
    powinno zwrócić możliwy ruch w górę i prawo. Zakładając, że '0' jest elementem pustym.

    1. Napisz metodę *transition_model*. Metoda ma zwracać stan po wykonaniu pewnej akcji / ruchu. Na wejściu podawany jest stan oraz akcja.
    np.
    ```
    2 8 3                   2 8 3
    1 6 4   --prawo-->      1 6 4
    0 7 5                   7 0 5
    ```

    1. Napisz metodę *action_cost*. Jest ona opcjonalna. Możesz wymyślić swoją własną metodę obliczania kosztu. Na wejściu jest podawany **aktualny_stan**, **akcja** oraz **nowy_stan**. Zwracanym kosztem jest liczba całkowita.

    1. Napisz metodę *is_goal*. Podawany stan przyrównaj z oczekiwanym stanem końcowym. Funkcja powinna zwracać True lub False


## Route finding (Miasta)


## Problem 3