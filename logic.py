"""Meursing-kategória meghatározó"""

# A tejtartalomra vonatkozó Meursing-összetevő felépítése:
# a kulcsok a tejzsír határok. A tejfehérje határok a tejzsír eredménytől
# függenek.
tej = {
    1.5: [2.5, 6, 18, 30, 60, 100],
    3: [2.5, 6, 18, 30, 60, 100],
    6: [2.5, 12, 100],
    9: [4, 15, 100],
    12: [6, 18, 100],
    18: [6, 18, 100],
    26: [6, 100],
    40: [6, 100],
    55: [100],
    70: [100],
    85: [100],
    100: [100],
}

# Szintúgy: a kem/glükóz maximumától függ a sz/inv/izog maximuma
cukor = {
    5: [5, 30, 50, 70, 100],
    25: [5, 30, 50, 70, 100],
    50: [5, 30, 50, 100],
    75: [5, 30, 100],
    100: [5, 100]
}


def beolvas():
    global hivatkozas
    res = ["tejzsír", "tejfehérje", "kem./gl.", "szach./inv./izogl."]
    eredmeny = []
    while len(eredmeny) != 4:
        for c in res:
            while 1:
                v = input("Add meg a " + c + " eredményt!\n> ")
                try:
                    v = float_(v)
                except ValueError:
                    print("Rosszul adtad meg a " + c + " eredmény!\n")
                else:
                    break
            eredmeny.append(v)

    v = input("Történt tejfehérje mérés?\nI/N > ")
    if v[0].lower() in ("i", "y"):
        hivatkozas = True
    else:
        hivatkozas = False
    v = input("Történt tejzsír mérés?\nI/N > ")
    if v[0].lower() in ("i", "y"):
        hivatkozas = True
    else:
        hivatkozas = False

    return eredmeny


def hatarok(eredmeny):
    #         tzs  tf   k/g  s/i/i
    # eredmeny:[...,....,....,....] ugyanúgy strukturált!
    maxi, mini = [None] * 4, [None] * 4
    n = 0
    for res in (tej, cukor):
        keylist = sorted(list(res.keys()))
        maxi[n] = keylist[len([i for i in keylist if i <= eredmeny[n]])]
        maxi[n + 1] = res[
            maxi[n]][len([i for i in res[maxi[n]] if i <= eredmeny[n + 1]])]
        mini[n] = keylist[len([i for i in keylist if i < eredmeny[n]]) - 1]
        mini[n + 1] = res[
            mini[n]][len([i for i in res[mini[n]] if i < eredmeny[n + 1]]) - 1]
        n += 2
    mini = [0 * i for i in mini if i == 100]
    print("MAXIMUMOK:", maxi, "\nMINIMUMOK:", mini)
    return maxi, mini


def kiiro(maximumok, minimumok, eredmeny):
    chain = ""
    komp = ["Tejzsír", "Tejfehérje", "Keményítő/glükóz",
            "Szacharóz/invertcukor/izoglükóz"]
    n = 0
    # print("MAXIMUMOK:", maximumok, "EREDMENY:", eredmeny)
    for res in (tej, cukor):
        # Az előbbi komponens meghatározása indul itt
        chain = chain + komp[n] + ": "
        keylist = sorted(list(res.keys()))

        # A minimum szám formázása
        chain += {
            True: "≥ 0", False: "≥ " + str_(keylist[keylist.index(maximumok[n]) - 1])
        }[keylist.index(maximumok[n]) - 1 < 0]

        # A maximum szám formázása
        chain += {
            True: "", False: " < " + str_(keylist[keylist.index(maximumok[n])])
        }[maximumok[n] == 100]

        # Az eredmény hozzáfűzése
        chain = chain + " (" + str_(eredmeny[n]) + ")\n"

        # Az utóbbi komponens meghatározása indul itt
        chain = chain + komp[n + 1] + ": "
        keylist = res[maximumok[n]]

        # A minimum szám formázása
        chain += {
            True: "≥ 0", False: "≥ " + str_(keylist[keylist.index(maximumok[n + 1]) - 1])
        }[keylist.index(maximumok[n + 1]) - 1 < 0]

        # A maximum szám formázása
        chain += {
            True: "", False: " < " + str_(keylist[keylist.index(maximumok[n + 1])])
        }[maximumok[n + 1] == 100]

        # Az eredmény hozzáfűzése
        chain = chain + " (" + str_(eredmeny[n + 1]) + ")"

        # Tejfehérjénél a hivatkozás hozzáfűzése, amennyiben szükséges
        if komp[n + 1] == "Tejfehérje":
            chain += {
                True: " (1101/2014/EU rendelet 1. mellékletének 1. pontja)",
                False: ""}[hivatkozas]
        chain += "\n"
        n += 2

        # Amennyiben valamelyik érték mérési hibahatáron van, azt megjegyzésben
        # közölni kell.
        # Megjegyzés-hozzáfűzést meg kellene csinálni!

    print(chain)


def float_(chain):
    return round(float(chain.replace(",", ".")), 1)


def str_(flt):
    return str(flt).replace(".", ",")


def main():
    eredmenyek = beolvas()
    (maxi, mini) = hatarok(eredmenyek)
    kiiro(maxi, mini, eredmenyek)


hivatkozas = False

if __name__ == '__main__':
    main()
