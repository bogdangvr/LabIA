class Nod:
    def __init__(self, info, h):
        self.info = info
        self.h = h

    def __str__(self):
        return "({}, h={})".format(self.info, self.h)

    def __repr__(self):
        return f"({self.info}, h={self.h})"


class Arc:
    def __init__(self, capat, varf, cost):
        self.capat = capat
        self.varf = varf
        self.cost = cost


class Problema:
    def __init__(self):
        self.noduri = [
            Nod('a', float('inf')), Nod('b', 10),
            Nod('c', 3), Nod('d', 7),
            Nod('e', 8), Nod('f', 0),
            Nod('g', 14), Nod('i', 3),
            Nod('j', 1), Nod('k', 2)
        ]
        self.arce = [
            Arc('a', 'b', 3),
            Arc('a', 'c', 9),
            Arc('a', 'd', 7),
            Arc('b', 'f', 100),
            Arc('b', 'e', 4),
            Arc('c', 'e', 10),
            Arc('c', 'g', 6),
            Arc('d', 'i', 4),
            Arc('e', 'f', 8),
            Arc('e', 'c', 1),
            Arc('g', 'e', 7),
            Arc('i', 'k', 1),
            Arc('i', 'j', 2)
        ]
        self.nod_start = self.noduri[0]  # de tip Nod
        self.nod_scop = 'f'  # doar info (fara h)

    def cauta_nod_nume(self, info):
        """Stiind doar informatia "info" a unui nod,
        trebuie sa returnati fie obiectul de tip Nod care are acea informatie,
        fie None, daca nu exista niciun nod cu acea informatie."""
        for nod in self.noduri:
            if info == nod.info:
                return nod
        return None





""" Sfarsit definire problema """

""" Clase folosite in algoritmul A* """


class NodParcurgere:
    """O clasa care cuprinde informatiile asociate unui nod din listele open/closed
        Cuprinde o referinta catre nodul in sine (din graf)
        dar are ca proprietati si valorile specifice algoritmului A* (f si g).
        Se presupune ca h este proprietate a nodului din graf

    """

    problema = None  # atribut al clasei

    def __init__(self, nod_graf, parinte=None, g=0, f=None):
        self.nod_graf = nod_graf  # obiect de tip Nod
        self.parinte = parinte  # obiect de tip Nod
        self.g = g  # costul drumului de la radacina pana la nodul curent
        if f is None:
            self.f = self.g + self.nod_graf.h
        else:
            self.f = f

    def drum_arbore(self):
        """
            Functie care calculeaza drumul asociat unui nod din arborele de cautare.
            Functia merge din parinte in parinte pana ajunge la radacina
        """
        nod_c = self
        drum = [nod_c]
        while nod_c.parinte is not None:
            drum = [nod_c.parinte] + drum
            nod_c = nod_c.parinte
        return drum

    def contine_in_drum(self, nod):
        """
            Functie care verifica daca nodul "nod" se afla in drumul dintre radacina si nodul curent (self).
            Verificarea se face mergand din parinte in parinte pana la radacina
            Se compara doar informatiile nodurilor (proprietatea info)
            Returnati True sau False.

            "nod" este obiect de tip Nod (are atributul "nod.info")
            "self" este obiect de tip NodParcurgere (are "self.nod_graf.info")
        """
        nod_c = self
        while nod_c.parinte is not None:
            if nod_c.nod_graf.info == nod.info:
                return True
            nod_c = nod_c.parinte
        return False

    # se modifica in functie de problema
    def expandeaza(self):
        """Pentru nodul curent (self) parinte, trebuie sa gasiti toti succesorii (fiii)
        si sa returnati o lista de tupluri (nod_fiu, cost_muchie_tata_fiu),
        sau lista vida, daca nu exista niciunul.
        (Fiecare tuplu contine un obiect de tip Nod si un numar.)
        """
        sol = []
        for arc in NodParcurgere.problema.arce:
            if self.nod_graf.info == arc.capat:
                nod = self.problema.cauta_nod_nume(arc.varf)
                cost = arc.cost
                sol.append((nod, cost))
        return sol


    # se modifica in functie de problema
    def test_scop(self):
        return self.nod_graf.info == self.problema.nod_scop

    def __str__(self):
        parinte = self.parinte if self.parinte is None else self.parinte.nod_graf.info
        return f"({self.nod_graf}, parinte={parinte}, f={self.f}, g={self.g})"


""" Algoritmul A* """


def str_info_noduri(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = "["
    for x in l:
        sir += str(x) + "  "
    sir += "]"
    return sir


def afis_succesori_cost(l):
    """
        o functie folosita strict in afisari - poate fi modificata in functie de problema
    """
    sir = ""
    for (x, cost) in l:
        sir += "\nnod: " + str(x) + ", cost arc:" + str(cost)

    return sir


def in_lista(l, nod):
    """
    lista "l" contine obiecte de tip NodParcurgere
    "nod" este de tip Nod
    """
    for i in range(len(l)):
        if l[i].nod_graf.info == nod.info:
            return l[i]
    return None


def a_star():
    rad_arbore = NodParcurgere(NodParcurgere.problema.nod_start)
    open = [rad_arbore]  # open va contine elemente de tip NodParcurgere
    closed = []  # closed va contine elemente de tip NodParcurgere

    while open:
        nod_curent = open.pop(0)
        closed.append(nod_curent)
        if nod_curent.test_scop():
            break
        for succesor, cost in nod_curent.expandeaza():
            nod_open = in_lista(open, succesor)
            nod_closed = in_lista(closed, succesor)
            g_nou = nod_curent.g + cost

            if nod_open:
                if g_nou < nod_open.g:
                    nod_open.g = g_nou
                    nod_open.f = g_nou + nod_open.nod_graf.h
            elif nod_closed:
                f_nou = g_nou + nod_closed.nod_graf.h

                if f_nou < nod_closed.f:
                    nod_closed.g = g_nou
                    nod_closed.f = f_nou + nod_closed.nod_graf.h

                    open.append(nod_closed)
            else:
                nod_nou = NodParcurgere(
                    nod_graf=succesor,
                    parinte=nod_curent,
                    g=g_nou
                )
                open.append(nod_nou)
        open.sort(key=lambda nod:nod.f)


    print("\n------------------ Concluzie -----------------------")
    if (len(open) == 0):
        print("Lista open e vida, nu avem drum de la nodul start la nodul scop")
    else:
        print("Drum de cost minim: " + str_info_noduri(nod_curent.drum_arbore()))


if __name__ == "__main__":
    problema = Problema()
    NodParcurgere.problema = problema
    a_star()
