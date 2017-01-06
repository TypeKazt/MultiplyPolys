# Multiplying Polynomials

A trivial symbolic execution engine that allows the user to perform basic algebra on polynomials.

## Requirements

Python 2.7.12 
NumPy 1.11.0

```
sudo pip install numpy
```

## Usage

Currently the main script poly.py simply takes the contents of input.txt, so the script can be run without any args
Parser is not dependent on sysin, so it can be used anywhere.

```
python poly.py
```

## Authors
* **Alexander Kazantsev**

## Comments
* It is assumed that the users input is not flawed as this is an interview assignment.
* I strongly think that inheritance is not necessary between Polynomial, Term, and Variable.
* Interesting recursive problem could present itself where exponents can also be polynomials.
 * Would require a new input format.
