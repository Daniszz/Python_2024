import os
import shutil
import winreg


def listare_director(directory):
    try:
        contents = os.listdir(directory)
        print(f"Continutul directorului '{directory}':")
        for item in contents:
            print(item)
    except FileNotFoundError:
        print(f"Eroare: Directorul '{directory}' nu exista.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea sa accesati directorul '{directory}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def copiere_fisier(source, destination):
    try:
        if os.path.isdir(destination):
            destination = os.path.join(destination, os.path.basename(source))
        shutil.copy(source, destination)
        print(f"Fisierul '{source}' a fost copiat in '{destination}'.")
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{source}' nu a fost gasit.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a citi sau scrie fisierul '{source}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")


def copiere_director(source, destination):
    try:
        if not os.path.exists(source):
            print(f"Eroare: Directorul sursa '{source}' nu a fost gasit.")
            return
        destination_path = os.path.join(destination, os.path.basename(source))
        shutil.copytree(source, destination_path)
        print(f"Directorul '{source}' a fost copiat in '{destination_path}'.")
    except FileExistsError:
        print(f"Eroare: Directorul de destinatie '{destination_path}' deja exista.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a citi sau scrie in directorul '{source}' sau '{destination}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")


def sterge_fisier(filepath):
    try:
        os.remove(filepath)
        print(f"Fisierul '{filepath}' a fost sters.")
    except FileNotFoundError:
        print(f"Eroare: Fisierul '{filepath}' nu a fost gasit.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a sterge fisierul '{filepath}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")


def sterge_director(directory, silent=False, recursive=False):
    try:
        if not os.path.exists(directory):
            print(f"Eroare: Directorul '{directory}' nu a fost gasit.")
            return

        if not recursive:
            if os.listdir(directory):  
                print(f"Eroare: Directorul '{directory}' nu este gol. Folositi optiunea '/s' pentru stergere recursiva.")
                return
            os.rmdir(directory) 
            print(f"Directorul gol '{directory}' a fost sters.")
            return

        
        if not silent:
            confirm = input(f"Sigur doriti sa stergeti directorul '{directory}' si tot continutul sau? (y/n): ")
            if confirm.lower() != 'y':
                print("Operatiune anulata.")
                return
        shutil.rmtree(directory)
        print(f"Directorul '{directory}' si tot continutul sau au fost sterse.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a sterge directorul '{directory}'.")
    except OSError as e:
        print(f"Eroare: {e}. Asigurati-va ca directorul este gol sau folositi optiunea '/s'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def mutare(source, destination):
    try:
        if not os.path.exists(source):
            print(f"Eroare: Sursa '{source}' nu a fost gasita.")
            return
        
        if os.path.isfile(source):
            copiere_fisier(source, destination)
            sterge_fisier(source)
        elif os.path.isdir(source):
            copiere_director(source, destination)
            sterge_director(source,silent=1,recursive=1)
        else:
            print(f"Eroare: '{source}' nu este nici fisier, nici director.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a muta '{source}' in '{destination}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")


def listare_key(input_key):
    try:
        predef, subkey = input_key.split('\\', 1) if '\\' in input_key else (input_key, "")
        hkey = getattr(winreg, predef.upper(), None)
        
        if not hkey:
            print(f"Eroare: Cheia predefinita '{predef}' este invalida.")
            return
        
        with winreg.OpenKey(hkey, subkey) as key:
            i = 0
            print(f"Continutul cheii '{input_key}':")
            while True:
                try:
                    subkey_name = winreg.EnumKey(key, i)
                    print(f"{input_key}\\{subkey_name}")
                    i += 1
                except OSError:
                    break
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def creare_key(input_key):
    try:
        predef, subkey = input_key.split('\\', 1) if '\\' in input_key else (input_key, "")
        hkey = getattr(winreg, predef.upper(), None)
        
        if not hkey:
            print(f"Eroare: Cheia predefinita '{predef}' este invalida.")
            return
        
        with winreg.CreateKey(hkey, subkey) as key:
            print(f"Cheia '{input_key}' a fost creata cu succes.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def modificare_key(input_key, value_name, data):
    try:
        predef, subkey = input_key.split('\\', 1) if '\\' in input_key else (input_key, "")
        hkey = getattr(winreg, predef.upper(), None)
        
        if not hkey:
            print(f"Eroare: Cheia predefinita '{predef}' este invalida.")
            return
        
        with winreg.CreateKey(hkey, subkey) as key:
            winreg.SetValueEx(key, value_name, 0, winreg.REG_SZ, data)
            print(f"Valoarea '{value_name}' a fost adaugata cu succes in '{input_key}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def sterge_key(input_key: str):
    try:
        predef, subkey = input_key.split('\\', 1) if '\\' in input_key else (input_key, "")
        hkey = getattr(winreg, predef.upper(), None)
        
        if not hkey:
            print(f"Eroare: Cheia predefinita '{predef}' este invalida.")
            return
        
        winreg.DeleteKey(hkey, subkey)
        print(f"Cheia '{input_key}' a fost stearsa cu succes.")
    except FileNotFoundError:
        print(f"Eroare: Cheia '{input_key}' nu a fost gasita.")
    except PermissionError:
        print(f"Eroare: Nu aveti permisiunea de a sterge cheia '{input_key}'.")
    except Exception as e:
        print(f"Eroare neasteptata: {e}")

def print_help():
    print("Comenzi disponibile:")
    print("  dir <director> - Afiseaza fisierele/directoarele dintr-un director")
    print("  del <pattern> - Sterge fisiere")
    print("  copy <sursa> <destinatie> - Copie un fisier (poate redenumi fisierul la destinatie)")
    print("  xcopy <sursa> <destinatie> - Copie un director recursiv")
    print("  rmdir <director> [/s] [/q] - Sterge recursiv un director. /s pentru stergere recursiva, /q pentru mod silentios")
    print("  move <sursa> <destinatie> - Muta un fisier sau un director") 
    print("  reg query <cheie> - Afiseaza lista cheilor de registru.")
    print("  reg add <cheie> - Adauga o noua cheie de registru.")
    print("  reg add <cheie> /v <valoare> /d <data> - Modifica o cheie de registru")
    print("  reg delete <cheie> /v <valoare> /d <data> - Modifica o cheie de registru")

    print("  help - Afiseaza acest mesaj de ajutor")
    print("  quit - Inchide programul")


def main():
    while True:
        try:
            command = input("> ").strip()
            argument = command.split()

            if not argument:
                continue

            if argument[0] == "dir":
                if len(argument) == 2:
                    listare_director(argument[1])
                else:
                    print("Argumente insuficiente. Utilizeaza help pentru ajutor.")

            elif argument[0] == "del":
                if len(argument) == 2:
                    sterge_fisier(argument[1])
                else:
                    print("Argumente insuficiente. Utilizeaza help pentru ajutor.")

            elif argument[0] == "copy":
                if len(argument) == 3:
                    copiere_fisier(argument[1], argument[2])
                else:
                    print("Argumente insuficiente. Utilizeaza help pentru ajutor.")

            elif argument[0] == "xcopy":
                if len(argument) == 3:
                    copiere_director(argument[1], argument[2])
                else:
                    print("Argumente insuficiente. Utilizeaza help pentru ajutor.")

            elif argument[0] == "rmdir":
                if len(argument) < 2:
                     print("Argumente insuficiente. Utilizeaza help pentru ajutor.")
                else:
                     recursive = '/s' in argument  
                     silent = '/q' in argument  
                     target_directory = [arg for arg in argument[1:] if not arg.startswith('/')]

                     if len(target_directory) == 1: 
                        sterge_director(target_directory[0], silent=silent, recursive=recursive)
                     else:
                        print("Argumente insuficiente sau nevalide. Utilizeaza help pentru ajutor.")

            elif argument[0] == "move":
                   if len(argument) == 3:
                        mutare(argument[1],argument[2])
                   else: 
                        print("Argumente insuficiente. Utilizeaza help pentru ajutor.")

            elif argument[0] == "reg":
                if len(argument) == 3:
                    if argument[1] == "query":
                        listare_key(argument[2])
                    elif argument[1] == "add":
                        creare_key(argument[2])
                    elif argument[1] == "delete": 
                        sterge_key(argument[2])   
                    else:
                        print("Argumente insuficiente. Utilizeaza 'help' pentru ajutor.")
                elif len(argument) == 7 and argument[1] == "add" and argument[3] == "/v" and argument[5] == "/d":
                    modificare_key(argument[2], argument[4], argument[6])
                else:
                    print("Argumente insuficiente sau incorecte. Utilizeaza 'help' pentru ajutor.") 

            

            elif argument[0] == "help":
                print_help()

            elif argument[0] == "quit":
                break

            else:
                print(f"Comanda necunoscuta: '{argument[0]}'. Utilizeaza 'help' pentru a vedea comenzile disponibile.")

        except Exception as e:
            print(f"Eroare neasteptata: {e}")


if __name__ == "__main__":
    main()
