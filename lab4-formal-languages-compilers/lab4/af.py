"""
clasa AF generica, valabila pentru orice automat finit (deteminist sau nedeterminist)
tranzitiile sunt stocate ca dict[(stare,simbol)]->set(stari), ceea ce permite reprezentarea unui AFN fara nicio schimbare de structura atunci cand automatul este de fapt determinist (caz in care fiecare multime din dictionar are cel mult un element)
formatul fisierului de intrare este descris in EBNF in grammar.md
"""

class AF:
    def __init__(self):
        self.stari=set()
        self.alfabet=set()
        self.tranzitii={} #(stare,simbol)->set(stari)
        self.initiala = None
        self.finale = set()

    #constructie
    def adauga_tranzitie(self, stare_sursa, simbol, stare_dest):
        cheie = (stare_sursa, simbol)
        self.tranzitii.setdefault(cheie, set()).add(stare_dest)

    #citire dintr-un fisier text (grammar.md pentru EBNF)
    @staticmethod
    def citeste_din_fisier(cale):
        af = AF()
        with open(cale, "r", encoding="utf-8") as f:
            linii = [l.strip() for l in f if l.strip() != ""]

        mod_tranzitii = False
        for linie in linii:
            linie_lower = linie.lower()
            if linie_lower.startswith("stari:"):
                af.stari = set(linie.split(":", 1)[1].split())
            elif linie_lower.startswith("alfabet:"):
                af.alfabet = set(linie.split(":", 1)[1].split())
            elif linie_lower.startswith("initiala:"):
                af.initiala = linie.split(":", 1)[1].strip()
            elif linie_lower.startswith("finale:"):
                af.finale = set(linie.split(":", 1)[1].split())
            elif linie_lower.startswith("tranzitii"):
                mod_tranzitii = True
            elif mod_tranzitii:
                sursa, simbol, dest = linie.split()
                af.adauga_tranzitie(sursa, simbol, dest)

        return af

    #citire interactiva, de la tastatura
    @staticmethod
    def citeste_de_la_tastatura():
        af = AF()

        print("Introduceti starile separate prin spatiu:")
        af.stari = set(input("> ").split())

        print("Introduceti alfabetul (simboluri separate prin spatiu):")
        af.alfabet = set(input("> ").split())

        print("Introduceti starea initiala:")
        af.initiala = input("> ").strip()

        print("Introduceti starile finale separate prin spatiu:")
        af.finale = set(input("> ").split())

        print("Introduceti tranzitiile, cate una pe linie, format: stare simbol stare_dest")
        print("(linie goala pentru a termina)")
        while True:
            linie = input("> ").strip()
            if linie == "":
                break
            sursa, simbol, dest = linie.split()
            af.adauga_tranzitie(sursa, simbol, dest)

        return af

    #afisare
    def afiseaza_stari(self):
        print("Multimea starilor Q:", " ".join(sorted(self.stari)))

    def afiseaza_alfabet(self):
        print("Alfabetul Sigma:", " ".join(sorted(self.alfabet)))

    def afiseaza_tranzitii(self):
        print("Functia de tranzitie delta:")
        for (sursa, simbol), destinatii in sorted(self.tranzitii.items()):
            for dest in sorted(destinatii):
                print(f"  delta({sursa}, {simbol}) = {dest}")

    def afiseaza_finale(self):
        print("Multimea starilor finale F:", " ".join(sorted(self.finale)))

    #verifică dacă automatul e AFD sau AFN, testând |δ(q,a)| <= 1 pentru orice stare/simbol (adică fiecare tranziție duce spre cel mult o stare, nu mai multe
    def este_determinist(self):
        """|delta(q,a)| <= 1 pentru orice (q,a)."""
        return all(len(destinatii) <= 1 for destinatii in self.tranzitii.values())

    def _delta1(self, stare, simbol):
        """Pentru AFD: starea unica in care se ajunge, sau None daca nu exista tranzitie."""
        destinatii = self.tranzitii.get((stare, simbol))
        if not destinatii:
            return None
        return next(iter(destinatii)) #sg element

    #acceptarea unei secvente (doar AFD)
    def accepta(self, secventa):
        stare_curenta = self.initiala
        for simbol in secventa:
            stare_curenta = self._delta1(stare_curenta, simbol)
            if stare_curenta is None:
                return False
        return stare_curenta in self.finale

    #cel mai lung prefix acceptat
    def cel_mai_lung_prefix_acceptat(self, secventa):
        """
        Returneaza cel mai lung prefix al secventei date care este el
        insusi o secventa acceptata de automat, sau None daca niciun
        prefix (incluzand cel vid) nu este acceptat.
        """
        stare_curenta = self.initiala
        cel_mai_lung = "" if stare_curenta in self.finale else None
        prefix_curent = ""

        for simbol in secventa:
            urmatoarea = self._delta1(stare_curenta, simbol)
            if urmatoarea is None:
                break
            prefix_curent += simbol
            stare_curenta = urmatoarea
            if stare_curenta in self.finale:
                cel_mai_lung = prefix_curent

        return cel_mai_lung