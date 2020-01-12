import math
# klasa przechowujaca nam informacje zapisywane w liscie otwartej i zamkniete
# jednoczesnie jako obiekt wpis jest na liscie jest referencyjny
class AGwiazdkaListaWpis:
     def __init__(self,wspolrzedne,rodzic = None):
        self.wspolrzedne = wspolrzedne
        self.rodzic = rodzic
     
        self.kosztG = 0
        self.kosztH = None
        self.kosztF = None  
# mechanizm algorytmu A*
class AGwiazdka:
     # inicjalizujemy i okreslamy wstepne wartosci algorytmu
     def __init__(self,plansza):
        self.listaOtwarta = []
        self.listaZamknieta = []
        # zalozenie okreslajace nam kierunek rozpatrywania sasiednich kratek
        self.kroki = [{"x": 0, "y": 1},{"x": -1, "y": 0},{"x": 0, "y": -1},{"x": 1, "y": 0}]
        self.plansza = []
        self.plansza = plansza
        self.rozmiar = len(plansza)
        self.startKratka = {"x": 0, "y": 0}
        self.celKratka = {"x": self.rozmiar-1, "y": self.rozmiar-1}
        
        # na podstawione zaznaczonych pozycji na planszy zaczytujemy pozycje start/stop
        for y, wiersz in enumerate(plansza):
            for x, kratka in enumerate(wiersz):
                if kratka == 1:
                    self.startKratka = {"x": x, "y": y}

                if kratka == 9:
                    self.celKratka = {"x": x, "y": y}

     # rozpoczyna dzialanie algorytmu
     def szukajDrogi(self):
          # poszukujemy celu indeksujac kolejne kratki zgodnie z algorytmem
          cel = self._szukajCelu(AGwiazdkaListaWpis(self.startKratka))

          if not cel:
               print('nie znaleziono drogi do celu')
               return
          
          # gdy okreslimy cel, wracamy po rodzicach do pozycji start
          self._wyznaczDroge(cel)

     # zaznaczamy droge na planszy
     def _wyznaczDroge(self,kratka):
          # zabezpieczenie rekurencji
          if not kratka.rodzic or kratka.rodzic.wspolrzedne == self.startKratka:
              return
          
          # na podstawie wspolrzednej rodzica okreslamy droge liczba 3
          self.plansza[kratka.rodzic.wspolrzedne['y']][kratka.rodzic.wspolrzedne['x']] = 3

          # wywolujemy rekurencyjnie az do pozycji start
          self._wyznaczDroge(kratka.rodzic)
     
     # dodawanie wpisow do listy otwartej
     def _dodajDoListyOtwartej(self,kratka):

         # szukamy duplikatu na liscie i jesli istnieje nic nie robimy
         for dodanaKratka in self.listaOtwarta:
              if dodanaKratka.wspolrzedne == kratka.wspolrzedne:
                 return

         # dodajemy kratke na liste 
         self.listaOtwarta.append(kratka);
         
     # dodawanie wpisow do listy zamknietej
     def _dodajDoListyZamknietej(self,kratka):

          # przy przenoszeniu do listy zamknietej usuwamy kratke z listy otwartej
          if kratka in self.listaOtwarta:
               self.listaOtwarta.remove(kratka)

          # szukamy duplikatu na liscie
          for dodanaKratka in self.listaZamknieta:
               if dodanaKratka.wspolrzedne == kratka.wspolrzedne:
                    # gdy kosztF z rodzica do tej kratki jest mniejszy, aktualizujemy rodzica kratce, i konczymy wykonywanie
                    if dodanaKratka.kosztF > kratka.kosztF:
                         dodanaKratka.rodzic = kratka.rodzic

                    return

          # dodajemy do listy zamknietej
          self.listaZamknieta.append(kratka);
         
     # indeksujemy sasiadujace kratki
     def _szukajCelu(self,kratka):
          # zgodnie z algorytmem, dodajemy analizowana kratke na liste zamknieta
          self._dodajDoListyZamknietej(kratka)

          # iterujemy po mozliwych do zindekstowania kratkach
          for nastepnaKratka in self._przejscia(kratka):
               # dodajemy do listy otwartej
               self._dodajDoListyOtwartej(nastepnaKratka)
               # i wyliczamy heurystyke
               self._wyliczHeurystyke(nastepnaKratka)

          # okreslamy nastepna kratke
          nastepnaKratka = self._wybierzPrzejscie()

          # gdy nie mozemy okreslic nastepnej kratki, algorytm musi zakonczyc poszukanie celu, poniewaz zadna droga do celu nie istnieje
          if not nastepnaKratka:
               return None;

          # sprawdzamy czy nastepna kratka jest celem, i konczymy indeksowanie
          if nastepnaKratka.wspolrzedne == self.celKratka:
               return nastepnaKratka     

          # rekurencyjnie przechodzimy dalej i indeksujemy kolejne kratki
          return self._szukajCelu(nastepnaKratka)             

     # wybieramy kartke po ktorej przejdziemy dalej
     def _wybierzPrzejscie(self):
          nastepnaKratka = None;

          # sprawdzamy wszystkie kratki na liscie otwartej i szukamy kratki o najnizszym koszcie F
          # konflikt (takie same F) rozwiazywany jest ze zwracana jest kratka dalsza na liscie (odkryta pozniej)
          for kratka in self.listaOtwarta:
               if nastepnaKratka is None or nastepnaKratka.kosztF >= kratka.kosztF:
                    nastepnaKratka = kratka
                    continue      

          return nastepnaKratka;
           
     # zwracamy liste kratek mozliwych do odwiedzenia z konkretnej kratki
     def _przejscia(self,kratka):
    
        def wyznaczprzejscia(przesuniecie):
            # wyliczamy wspolrzedne dla kolejnego przesucia      
            wspolrzedne = {"x": kratka.wspolrzedne["x"] + przesuniecie["x"], "y": kratka.wspolrzedne["y"] + przesuniecie["y"]}

            # wyjątki
            # kratki wychodzące poza zakres są odrzucane 
            if wspolrzedne["x"] < 0 or wspolrzedne["y"] < 0 or wspolrzedne["x"] >= self.rozmiar or  wspolrzedne["y"] >= self.rozmiar:
                 return None
               
            # sprawdzamy czy kratka ta nie jest przeszkodą na planszy 
            if self.plansza[wspolrzedne["y"]][wspolrzedne["x"]] not in [0,9]:
               return None

            # sprawdzamy czy kratek tych nie odwiedzilismy juz wczesniej (znajduja sie one na liscie zamkniete)
            for odwiedzoneKratki in self.listaZamknieta:
               if odwiedzoneKratki.wspolrzedne == wspolrzedne:
                    return None

            # jesli tworzymy wpis dla kratki o danej wspolrzednej i dopisujemy jej odwiedzana kratke jako rodzica 
            return AGwiazdkaListaWpis(wspolrzedne,kratka)

        # mapujemy przejscia na kolejne kratki i filtrujemy przejscia do kolejnych kratek
        return [sasiad for sasiad in map(wyznaczprzejscia, self.kroki) if sasiad is not None];


     # wyliczamy heurystyke 
     def _wyliczHeurystyke(self,kratka):
          # zwiekszamy koszt przebytej kratki od startu
          kratka.kosztG = kratka.rodzic.kosztG+1
          # wyliczamy heurystyke do celu bazujac heurystyce Euklidesowa (gdzie liczona jest odleglosc w kratkach do celu)
          kratka.kosztH = math.sqrt( math.pow(kratka.wspolrzedne["x"] - self.celKratka["x"],2) + math.pow(kratka.wspolrzedne["y"] - self.celKratka["y"],2))
          # wyznaczony ogolnie koszt od startu do konkretnej kratki i do celu
          kratka.kosztF = kratka.kosztG + kratka.kosztH
     
        

# plansze wczytujemy z pliku
def wczytajPlansze(mapa):
    plansza=[]
    plik = open(mapa);
    for wiersz in plik:
        plansza.append([int(x) for x in wiersz.strip().split(' ')]);

    print(plansza)
    return plansza       

# zamiana cyfr na symbole dla przejrzystosci
def symbol(x):
    s = {0: ' ', 1: 'S', 3: '.', 5: '*', 9: 'M'}
    return s[x]


# wyswietlamy plansze z wyszczegolnionymi wspolrzednymi
def wyswietl(plansza):

    linia = ' ';

    naglowek1 = linia + '\ ' + linia
    naglowek2 = linia + ' \\' + linia
    
    for x in range(len(plansza[1])):
        naglowek1 += str(int(x / 10)) + linia
        naglowek2 += str(x % 10) + linia

    print(naglowek1)
    print(naglowek2)
    
    for y, wiersz in enumerate(plansza):
        print( linia + '{:02d}'.format(y) + linia + linia.join(map(symbol, wiersz)) + linia)

    return;    
        
# ladujemy i inicjujemy algorytm A*
aGwiazdka = AGwiazdka(wczytajPlansze('grid.txt'))
# rozwiązujemy drogę
aGwiazdka.szukajDrogi()
# wyswietlamy plansze
wyswietl(aGwiazdka.plansza)
