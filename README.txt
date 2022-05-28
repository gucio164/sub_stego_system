Jest to implementacja metody steganografii lingwistycznej bazujacej na substytucji synonimow.
Algorytm odczytuje z pliku text w ktrym ma zostac ukryta wiadomosc.
Dokonuje jego tokenizacji przy pomocy metody word_tokenize (biblioteka nltk).
Dla kazdego ze slow odczytanych z pliku wykonuje operacje:
- Usuwania przyrostka wykorzystujac w tym celu SnowballStemmer (biblioteka nltk).
- Part-of-speech tagging korzystajac z metody .pos_ (biblioteka spacy z zaladowanym modelem en_core_web_md)
Jesli slowo jest conajmniej 3 literowym czasownikiem lub rzeczownikiem:
- Wyszukuje liste jego synonimow w slowniku wordnet (biblioteka nltk)(Ograniczona do 3 najlepszych synonimow dla poprawienia jakosci substytucji).
- Dla kazdego z nich dokonuje oceny podobienstwa za pomoca funkcji .similarity() (biblioteka spacy).
Jesli znalezione zostaly conajmniej dwa synonimy:
- Na podstawie ocen podobienstwa generowane jest drzewo huffmana dla synonimow danego slowa
- Drzewo sprawdzene jest pod katem pokrycia kolejnych bitow sekretu a nastepnie dokonywana jest substytucja slow.