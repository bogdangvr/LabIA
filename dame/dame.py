import time

class Joc:
    """
    Clasa care defineste jocul. Se va schimba de la un joc la altul.
    """
    NR_LINII = 8
    NR_COLOANE = 8
    JMIN = None
    JMAX = None
    GOL = '#'

    def __init__(self, tabla=None):
        if tabla!=None:
            self.matr = tabla
        else:
            linia0 = ['a' if i%2==1 else '#' for i in range (self.NR_COLOANE)]
            linia1 = ['a' if i%2==0 else '#' for i in range (self.NR_COLOANE)]
            linia3 = ['#' for i in range (self.NR_COLOANE)]
            linia5 = ['n' if i % 2 == 0 else '#' for i in range(self.NR_COLOANE)]
            linia6 = ['n' if i % 2 == 1 else '#' for i in range(self.NR_COLOANE)]
            self.matr = []
            self.matr.append(linia0)
            self.matr.append(linia1)
            self.matr.append(linia0)
            self.matr.append(linia3)
            self.matr.append(linia3)
            self.matr.append(linia5)
            self.matr.append(linia6)
            self.matr.append(linia5)

    def final(self):
        countA=0
        countN=0
        for i in range (self.NR_LINII):
            for j in range (self.NR_COLOANE):
                if self.matr[i][j].lower()=='a':
                    countA+=1
                elif self.matr[i][j].lower=='n':
                    countN+=1

        if countA == 0:
            return 'n'
        elif countN == 0:
            return 'a'
        else:
            return False

    def mutari_joc(self, jucator):
        """
        Pentru configuratia curenta de joc "self.matr" (de tip lista, cu 9 elemente),
        trebuie sa returnati o lista "l_mutari" cu elemente de tip Joc,
        corespunzatoare tuturor configuratiilor-succesor posibile.

        "jucator" este simbolul jucatorului care face mutarea
        """
        l_mutari = []

        #mutare ((ic, jc),(if,jf))




        return l_mutari


    def fct_euristica(self):
        countA = 0
        countN = 0
        for i in range(self.NR_LINII):
            for j in range(self.NR_COLOANE):
                if self.matr[i][j].lower() == 'a':
                    countA += 1
                elif self.matr[i][j].lower == 'n':
                    countN += 1

        if self.JMAX == 'a':
            return countA-countN
        else:
            return countN - countA



    def estimeaza_scor(self, adancime):
        t_final = self.final()
        if t_final == Joc.JMAX :
            return (999+adancime)
        elif t_final == Joc.JMIN:
            return (-999-adancime)
        elif t_final == 'remiza':
            return 0
        else:
            return self.fct_euristica()

    def __str__(self):
        sir = (" ".join([str(x) for x in self.matr[0]]) + "\n" +
               " ".join([str(x) for x in self.matr[1]]) + "\n" +
               " ".join([str(x) for x in self.matr[2]]) + "\n" +
               " ".join([str(x) for x in self.matr[3]]) + "\n" +
               " ".join([str(x) for x in self.matr[4]]) + "\n" +
               " ".join([str(x) for x in self.matr[5]]) + "\n" +
               " ".join([str(x) for x in self.matr[6]]) + "\n" +
               " ".join([str(x) for x in self.matr[7]]) + "\n")

        return sir


class Stare:
    """
    Clasa folosita de algoritmii minimax si alpha-beta
    Are ca proprietate tabla de joc
    Functioneaza cu conditia ca in cadrul clasei Joc sa fie definiti JMIN si JMAX (cei doi jucatori posibili)
    De asemenea cere ca in clasa Joc sa fie definita si o metoda numita mutari_joc() care ofera lista cu
    configuratiile posibile in urma mutarii unui jucator
    """

    ADANCIME_MAX = None

    def __init__(self, tabla_joc, j_curent, adancime, parinte=None, scor=None):
        self.tabla_joc = tabla_joc  # un obiect de tip Joc => „tabla_joc.matr”
        self.j_curent = j_curent  # simbolul jucatorului curent

        # adancimea in arborele de stari
        #	(scade cu cate o unitate din „tata” in „fiu”)
        self.adancime = adancime

        # scorul starii (daca e finala, adica frunza a arborelui)
        # sau scorul celei mai bune stari-fiice (pentru jucatorul curent)
        self.scor = scor

        # lista de mutari posibile din starea curenta
        self.mutari_posibile = []  # lista va contine obiecte de tip Stare

        # cea mai buna mutare din lista de mutari posibile pentru jucatorul curent
        self.stare_aleasa = None

    def jucator_opus(self):
        if self.j_curent == Joc.JMIN:
            return Joc.JMAX
        else:
            return Joc.JMIN

    def mutari_stare(self):
        l_mutari = self.tabla_joc.mutari_joc(self.j_curent)
        juc_opus = self.jucator_opus()

        l_stari_mutari = [Stare(mutare, juc_opus, self.adancime - 1, parinte=self) for mutare in l_mutari]
        return l_stari_mutari

    def __str__(self):
        sir = str(self.tabla_joc) + "(Juc curent:" + self.j_curent + ")\n"
        return sir


""" Algoritmul MinMax """


def min_max(stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Altfel, calculez toate mutarile posibile din starea curenta
    stare.mutari_posibile = stare.mutari_stare()

    # aplic algoritmul minimax pe toate mutarile posibile (calculand astfel subarborii lor)
    mutari_scor = [min_max(mutare) for mutare in stare.mutari_posibile]

    if stare.j_curent == Joc.JMAX:
        # daca jucatorul e JMAX aleg starea-fiica cu scorul maxim
        stare.stare_aleasa = max(mutari_scor, key=lambda x: x.scor)
    else:
        # daca jucatorul e JMIN aleg starea-fiica cu scorul minim
        stare.stare_aleasa = min(mutari_scor, key=lambda x: x.scor)

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor
    return stare


def alpha_beta(alpha, beta, stare):
    # Daca am ajuns la o frunza a arborelui, adica:
    # - daca am expandat arborele pana la adancimea maxima permisa
    # - sau daca am ajuns intr-o configuratie finala de joc
    if stare.adancime == 0 or stare.tabla_joc.final():
        # calculam scorul frunzei apeland "estimeaza_scor"
        stare.scor = stare.tabla_joc.estimeaza_scor(stare.adancime)
        return stare

    # Conditia de retezare:
    if alpha >= beta:
        return stare  # este intr-un interval invalid, deci nu o mai procesez

    # Calculez toate mutarile posibile din starea curenta (toti „fiii”)
    stare.mutari_posibile = stare.mutari_stare()

    if stare.j_curent == Joc.JMAX:
        scor_curent = float('-inf')  # scorul „tatalui” de tip MAX

        # pentru fiecare „fiu” de tip MIN:
        for mutare in stare.mutari_posibile:
            # calculeaza scorul fiului curent
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (cresc) scorul si alfa
            # „tatalui” de tip MAX, folosind scorul fiului curent
            if scor_curent < stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if alpha < stare_noua.scor:
                alpha = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MIN


    elif stare.j_curent == Joc.JMIN:
        scor_curent = float('inf')  # scorul „tatalui” de tip MIN

        # pentru fiecare „fiu” de tip MAX:
        for mutare in stare.mutari_posibile:
            stare_noua = alpha_beta(alpha, beta, mutare)

            # incerc sa imbunatatesc (scad) scorul si beta
            # „tatalui” de tip MIN, folosind scorul fiului curent
            if scor_curent > stare_noua.scor:
                stare.stare_aleasa = stare_noua
                scor_curent = stare_noua.scor

            if beta > stare_noua.scor:
                beta = stare_noua.scor
                if alpha >= beta:  # verific conditia de retezare
                    break  # NU se mai extind ceilalti fii de tip MAX

    # actualizez scorul „tatalui” = scorul „fiului” ales
    stare.scor = stare.stare_aleasa.scor

    return stare


def afis_daca_final(stare_curenta):
    final = stare_curenta.tabla_joc.final()
    if (final):
        if (final == "remiza"):
            print("Remiza!")
        else:
            print("A castigat " + final)

        return True

    return False

def mutariPosibile(stare_curenta, i, j):
    pass


def main():
    # initializare algoritm
    raspuns_valid = False
    while not raspuns_valid:
        tip_algoritm = input("Algorimul folosit? (raspundeti cu 1 sau 2)\n 1.Minimax\n 2.Alpha-Beta\n ")
        if tip_algoritm in ['1', '2']:
            raspuns_valid = True
        else:
            print("Nu ati ales o varianta corecta.")

    # initializare ADANCIME_MAX
    raspuns_valid = False
    while not raspuns_valid:
        n = input("Adancime maxima a arborelui: ")
        if n.isdigit():
            Stare.ADANCIME_MAX = int(n)
            raspuns_valid = True
        else:
            print("Trebuie sa introduceti un numar natural nenul.")

    # initializare jucatori
    raspuns_valid = False
    while not raspuns_valid:
        Joc.JMIN = input("Doriti sa jucati cu a sau cu n? ").lower()
        if (Joc.JMIN in ['a', 'n']):
            raspuns_valid = True
        else:
            print("Raspunsul trebuie sa fie a sau n.")
    Joc.JMAX = 'a' if Joc.JMIN == 'n' else 'n'

    # initializare tabla
    tabla_curenta = Joc()
    print("Tabla initiala")
    print(str(tabla_curenta))

    # creare stare initiala
    stare_curenta = Stare(tabla_curenta, 'n', Stare.ADANCIME_MAX)

    while True:
        if (stare_curenta.j_curent == Joc.JMIN):
            # muta jucatorul
            raspuns_valid = False
            while not raspuns_valid:
                try:
                    liniec = int(input("linie piesei selectate="))
                    coloanac = int(input("coloana piesei selectate="))

                    if (liniec in range(0, 7) and coloanac in range(0, 7)):
                        if stare_curenta.tabla_joc.matr[liniec][coloanac] == Joc.JMIN:
                            raspuns_valid = True
                            mutariPosibile = mutariPosibile(stare_curenta, liniec, coloanac)
                            linied = int(input("linie piesei destinatie="))
                            coloanad = int(input("coloana piesei destinatie="))
                        else:
                            print("Nu ai selectat o piesa a ta.")
                    else:
                        print("Linie sau coloana invalida (trebuie sa fie intre 0 si 7.")

                except ValueError:
                    print("Linia si coloana trebuie sa fie numere intregi")

            # dupa iesirea din while sigur am valide atat linia cat si coloana
            # deci pot plasa simbolul pe "tabla de joc"
            stare_curenta.tabla_joc.matr[linie][coloana] = Joc.JMIN

            # afisarea starii jocului in urma mutarii utilizatorului
            print("\nTabla dupa mutarea jucatorului")
            print(str(stare_curenta))

            # testez daca jocul a ajuns intr-o stare finala
            # si afisez un mesaj corespunzator in caz ca da
            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()

        # --------------------------------
        else:  # jucatorul e JMAX (calculatorul)
            # Mutare calculator

            # preiau timpul in milisecunde de dinainte de mutare
            t_inainte = int(round(time.time() * 1000))
            if tip_algoritm == '1':
                stare_actualizata = min_max(stare_curenta)
            else:  # tip_algoritm==2
                stare_actualizata = alpha_beta(-500, 500, stare_curenta)
            stare_curenta.tabla_joc = stare_actualizata.stare_aleasa.tabla_joc
            print("Tabla dupa mutarea calculatorului")
            print(str(stare_curenta))

            # preiau timpul in milisecunde de dupa mutare
            t_dupa = int(round(time.time() * 1000))
            print("Calculatorul a \"gandit\" timp de " + str(t_dupa - t_inainte) + " milisecunde.")

            if (afis_daca_final(stare_curenta)):
                break

            # S-a realizat o mutare. Schimb jucatorul cu cel opus
            stare_curenta.j_curent = stare_curenta.jucator_opus()


if __name__ == "__main__":
    main()