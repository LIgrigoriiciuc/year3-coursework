from af import AF


def citeste_automat():
    print("Automatul se citeste:")
    print("  1. dintr-un fisier")
    print("  2. de la tastatura")
    optiune = input("Alegeti (1/2): ").strip()

    if optiune == "2":
        return AF.citeste_de_la_tastatura()
    cale = input("Introduceti calea fisierului: ").strip()
    return AF.citeste_din_fisier(cale)


def afiseaza_meniu():
    print()
    print("===== MENIU =====")
    print("1. Afiseaza multimea starilor")
    print("2. Afiseaza alfabetul")
    print("3. Afiseaza tranzitiile")
    print("4. Afiseaza multimea starilor finale")
    print("5. Verifica daca automatul este determinist (AFD)")
    print("6. Verifica daca o secventa este acceptata (doar AFD)")
    print("7. Determina cel mai lung prefix acceptat dintr-o secventa (doar AFD)")
    print("8. Reciteste automatul (fisier/tastatura)")
    print("0. Iesire")


def main():
    print("=== Program de lucru cu automate finite ===")
    af = citeste_automat()
    print("Automat citit cu succes.")

    while True:
        afiseaza_meniu()
        optiune = input("Alegere: ").strip()

        if optiune == "1":
            af.afiseaza_stari()

        elif optiune == "2":
            af.afiseaza_alfabet()

        elif optiune == "3":
            af.afiseaza_tranzitii()

        elif optiune == "4":
            af.afiseaza_finale()

        elif optiune == "5":
            determ = af.este_determinist()
            print("Automatul este", "DETERMINIST (AFD)." if determ else "NEDETERMINIST (AFN).")

        elif optiune == "6":
            if not af.este_determinist():
                print("Operatia este valabila doar pentru automate deterministe (AFD).")
            else:
                secventa = input("Introduceti secventa de verificat: ")
                rezultat = af.accepta(secventa)
                print("Secventa este", "ACCEPTATA." if rezultat else "RESPINSA.")

        elif optiune == "7":
            if not af.este_determinist():
                print("Operatia este valabila doar pentru automate deterministe (AFD).")
            else:
                secventa = input("Introduceti secventa: ")
                prefix = af.cel_mai_lung_prefix_acceptat(secventa)
                if prefix is None:
                    print("Niciun prefix (nici cel vid) nu este acceptat de automat.")
                else:
                    print(f"Cel mai lung prefix acceptat: '{prefix}' (lungime {len(prefix)})")

        elif optiune == "8":
            af = citeste_automat()
            print("Automat recitit cu succes.")

        elif optiune == "0":
            print("La revedere.")
            break

        else:
            print("Optiune invalida.")


if __name__ == "__main__":
    main()