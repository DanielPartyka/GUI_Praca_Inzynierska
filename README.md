## GUI_Praca_Inzynierska

### Aplikacja została stworzona w pythonie wersja 3.8.3

#### Uruchamianie Aplikacji

Do uruchomienia aplikacji w systemie Windows i Linux użyte zostanie narzędzie
pip oraz virtualenv. Do uruchomienia aplikacji potrzebny jest język python w wersji 3.6+

### Windows

Przechodzimy do katalogu projektu
```
    cd GUI_Praca_Inzynierska
```
Update'ujemy pip
```
    python -m pip install --upgrade pip
```
Instalujemy wirtualne środowisko dla systemu Windows
```
    python -m pip install virtualenvwrapper-win
```
Tworzymy wirtualne środowisko
```
    python -m virtualenv <nazwa_wirtualnego_srodowiska>
```
Aktywujemy wirtualne środowisko
```
    .\<nazwa_wirtualnego_srodowiska>\Scripts\activate
```
Instalujemy pakiety dla aplikacji
```
    python -m pip install -r requirements/requirements_windows.txt
```
Instalujemy bibliotekę uamf
* Wypakowujemy plik uamf-0.5.0
* Uruchamiamy polecenia
```
    cd uamf-0.5.0
    python setup.py instal
    cd ..
```
 
Uruchamiamy Aplikację
```
    python3 praca_inzynierska.py
```
### Linux
Przechodzimy do katalogu projektu
```
    $ cd GUI_Praca_Inzynierska
```
Instalujemy środowisko wirtualne virtualenv
```
    $ sudo apt-get install virtualenv
```
Tworzymy wirtualne środowisko
```
    $ virtualenv <nazwa_wirtualnego_srodowiska>
```
Aktywujemy wirtualne środowisko
```
    $ source <nazwa_wirtualnego_srodowiska>/bin/activate
```
Instalujemy pakiety dla aplikacji
```
    $ pip3 install -r requirements/requirements_linux.txt
```
Instalujemy osobno dodatkowy pakiet do aplikacji (występowały problemy z importem)
```
    $ pip3 install --upgrade pyqt5==5.14.0
```
Instalujemy bibliotekę uamf
```
    $ tar -xf uamf-0.5.0.tar.gz
    $ cd uamf-0.5.0
    $ touch .version
    $ python3 setup.py install
```
Uruchamiamy Aplikację
```
    $ python3 praca_inzynierska.py
```

