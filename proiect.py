import os
def listare_director(directory):
    try:
        contents = os.listdir(directory)
        print(f"Conținutul directorului '{directory}':")
        for item in contents:
            print(item)
    except FileNotFoundError:
        print(f"Eroare: Directorul '{directory}' nu există.")
    except PermissionError:
        print(f"Eroare: Nu aveți permisiunea să accesați directorul '{directory}'.")
    except Exception as e:
        print(f"Eroare neașteptată: {e}")

def copiere_fisier(source, destination):
    try:
        with open(source, 'r') as fsrc:
            with open(destination, 'w') as fdst:
                fdst.write(fsrc.read())
        print(f"Fișierul '{source}' a fost copiat în '{destination}'.")
    except FileNotFoundError:
        print(f"Eroare: Fișierul '{source}' nu a fost găsit.")
    except PermissionError:
        print(f"Eroare: Nu aveți permisiunea de a citi sau scrie fișierul '{source}'.")
    except Exception as e:
        print(f"Eroare neașteptată: {e}")


def copiere_director(source, destination):
    try:
        if not os.path.exists(destination):
            os.makedirs(destination)

        for item in os.listdir(source):
            source_item = os.path.join(source, item)
            destination_item = os.path.join(destination, item)

            if os.path.isdir(source_item):
                copiere_director(source_item, destination_item) 
            else:
                copiere_fisier(source_item, destination_item) 
        print(f"Directorul '{source}' a fost copiat în '{destination}'.")
    except FileNotFoundError:
        print(f"Eroare: Directorul '{source}' nu a fost găsit.")
    except PermissionError:
        print(f"Eroare: Nu aveți permisiunea de a citi sau scrie în directorul '{source}'.")
    except Exception as e:
        print(f"Eroare neașteptată: {e}")

    
def print_help():
    print("Comenzi disponibile:")
    print("  dir <director> - Afiseaza fisierele/directoarele dintr-un director")
    print("  copy <source> <destination> - Copie un fisier")
    print("  xcopy <source> <destination> - Copie un director recursiv")
    print("  help - Display this help message")
    

def main():
    while True:
        try:
            command = input("> ").strip()
            argument = command.split()

            if not argument:
                continue

            if argument[0] == "copy":
                if len(argument) == 3:
                    copiere_fisier(argument[1], argument[2])               
                else:
                    print("cp: missing file operand.\n Try 'help' for more information")
            
            elif argument[0]=="xcopy":
                 if len(argument) == 3:
                    copiere_fisier(argument[1], argument[2])               
                 else:
                    print("cp: missing file operand.\n Try 'help' for more information") 

            elif argument[0] == "help":
                print_help()
            elif argument[0] == "quit":
                break
            else:
                print(f"syntax error near unexpected token '{argument[0]}'")


        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
