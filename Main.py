import csv
import datetime
import os.path
import re

# Initialisation de la variable BDD qui contient toute la base de donnée
BDD = []


# Gestion des entrées de l'utilisateur pour le chemin du document csv
def grab_path_input():

    n = False
    while not n:
        document_csv = input("Entrez le chemin d'accès du document csv: ")

        if os.path.isfile(document_csv) and str(document_csv)[-4:] == '.csv':
            n = True
            return str(document_csv)

        else:
            print("Le chemin d'accès est invalide!")


def grab_date_input():

    n = False
    while not n:
        date_recherche = input("Entrez la date de de recherche (JJ-MM-AAAA): ")

        try:
            date = datetime.datetime.strptime(date_recherche, '%d-%m-%Y')
            return date

        except ValueError:
            print("La date entrée est invalide!")


def transform_address(address):
    address = address[15:]

    if address[-6] == 'G' or address[-6] == 'J' or address[-6] == 'H':
        address = re.sub('Aucune province', 'Québec', address)
    elif address[-6] == 'K' or address[-6] == 'L' or address[-6] == 'M' or address[-6] == 'N' or address[-6] == 'O':
        address = re.sub('Aucune province', 'Ontario', address)
    elif address[-6] == 'V':
        address = re.sub('Aucune province', 'Colombie Britanique', address)
    elif address[-6] == 'S':
        address = re.sub('Aucune province', 'Saskatchewan', address)
    elif address[-6] == 'T':
        address = re.sub('Aucune province', 'Alberta', address)
    elif address[-6] == 'A':
        address = re.sub('Aucune province', 'Terre-Neuve-et-Labrador', address)
    elif address[-6] == 'B':
        address = re.sub('Aucune province', 'Nouvelle Écosse', address)
    elif address[-6] == 'C':
        address = re.sub('Aucune province', 'Île-du-Prince-Édouard', address)
    elif address[-6] == 'E':
        address = re.sub('Aucune province', 'Nouveau-Brunswick', address)
    elif address[-6] == 'R':
        address = re.sub('Aucune province', 'Manitoba', address)
    elif address[-6] == 'Y':
        address = re.sub('Aucune province', 'Yukon', address)

    address = address.split("\n")

    address[1] = str(address[1][:-7]) + ' ' + str(address[1][-7:-3]) + ' ' + str(address[1][-3:])
    return address


def transform_nom(nom):
    actual_name = ''
    x = nom.split(",")

    for i in reversed(x):
        new_name = i.strip(' ')
        new_name = new_name.title()
        actual_name += new_name + ' '

    return actual_name.strip(' ')


# Lecture du fichier csv et écriture de chaque ligne dans la variable BDD
with open(grab_path_input(), "r") as fich:
    base_de_données = csv.reader(fich)
    for ligne in base_de_données:
        BDD.append(ligne)

DATE = grab_date_input()

NOM_FICHIER = input('Entrez le nom du fichier csv qui sera crée (sans le .csv): ')

BD_filtrée = []

# Isoler les clients qui sont venus en consultation et qui n'ont pas acheté depuis la date fixée.
for i in range(len(BDD)):
    if BDD[i][-3] != '' and BDD[i][-3] != "Groupe\n\n" and BDD[i][-3][:6] == "Groupe":

        n = False
        iterator = 1
        nouvelle_date = datetime.datetime.strptime(BDD[i + iterator][1], '%Y-%m-%d')

        while not n:
            iterator += 1
            if BDD[i + iterator][1] != '':
                temp_date = datetime.datetime.strptime(BDD[i + iterator][1], '%Y-%m-%d')
                if temp_date > nouvelle_date:
                    nouvelle_date = temp_date

            else:
                n = True

        if nouvelle_date < DATE:
            BD_filtrée.append([transform_nom(BDD[i - 1][0]), transform_address(BDD[i][3])[0], transform_address(BDD[i][3])[1]])

print(str(len(BD_filtrée)) + ' clients trouvés')

BD_filtrée = sorted(BD_filtrée)


with open(NOM_FICHIER + '.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile, dialect='excel')
    writer.writerow(['Nom', 'Adresse'])
    for ligne in BD_filtrée:
        writer.writerow(ligne)

print('Le fichier ' + NOM_FICHIER + '.csv a été crée avec succès dans le dossier principal!')
