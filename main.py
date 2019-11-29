import sys
import globals
import drivefuncs as func
def input_choice():
    while True:
        try:
            choice = int(input())
        except ValueError:
            print("Ivestas pasirinkimas nera sveikas skaicius - bandykite dar karta")
            continue
        else:
            return choice
            break


def switch_def(argument):
    switcher = {
        1: func.find_transaction_fee,
        2: func.check_block,
        3: func.end_execution
    }
    function = switcher.get(argument, lambda: "Invalid choice")
    function()


def main():
    choices = [1, 2, 3]

    while globals.control == 0:
        print('Pasirinkite ka norite daryti:')
        print('1. Apskaiciuoti transakcijos kaina')
        print('2. Patikrinti ar bloko hashas yra teisingas')
        print('3. Baigti programa')
        globals.control = input_choice()
        if globals.control not in choices:
            while True:
                print('Ivestas netinkamas pasirinkimas - bandykite dar karta')
                globals.control = input_choice()
                if globals.control in choices:
                    break
        switch_def(globals.control)


if __name__ == "__main__":
    main()
