# InfoVis
## Installation
`sudo apt-get install python3-setuptools python3-dev build-essential`
`sudo easy_install3 pip`
`sudo pip install -U nltk`
`python3` >>> `import nltk` >>> `nltk.download()` >>> `all`

`python analyzer.py source.txt`


## Vorgehen
- html lowercase einlesen
- fette woerter und ueberschriften finden
- tags rauswerfen -> text
- text tokenisieren
- lemma finden ("better" -> "good")
- hochfrequente lemmta finden -> anzeigen
  - und die gemeinsamen vorkommen finden.
