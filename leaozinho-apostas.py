from pynput import keyboard
import csv
import os
from time import sleep


class Player:
   Money = 10
   Acoes = {
      "Americanas": 0,
      "123Milhas": 0
   }

class B3:
   Americanas = 0.001
   Milhas = 0.2

class Colors:
   BLACK = "\033[0;30m"
   RED = "\033[0;31m"
   GREEN = "\033[0;32m"
   BROWN = "\033[0;33m"
   BLUE = "\033[0;34m"
   PURPLE = "\033[0;35m"
   CYAN = "\033[0;36m"
   LIGHT_GRAY = "\033[0;37m"
   DARK_GRAY = "\033[1;30m"
   LIGHT_RED = "\033[1;31m"
   LIGHT_GREEN = "\033[1;32m"
   YELLOW = "\033[1;33m"
   LIGHT_BLUE = "\033[1;34m"
   LIGHT_PURPLE = "\033[1;35m"
   LIGHT_CYAN = "\033[1;36m"
   LIGHT_WHITE = "\033[1;37m"
   BOLD = "\033[1m"
   FAINT = "\033[2m"
   ITALIC = "\033[3m"
   UNDERLINE = "\033[4m"
   BLINK = "\033[5m"
   NEGATIVE = "\033[7m"
   CROSSED = "\033[9m"
   END = "\033[0m"


def printDelayed(texto, time=0.1):
   valor = ""
   for char in texto:
       valor += char
       print(valor, end="\r")
       sleep(time)
   print("")


def printDelayedColor(texto, cor, time=0.1):
   valor = ""
   for char in texto:
       valor += char
       print(cor + valor + Colors.END, end="\r")
       sleep(time)
   print("")


def saveData():
   path = os.environ.get("LOCALAPPDATA")
   print(path)
   file = f"{path}\\system_data.csv"
   print("Saving...", end="\r")
   with open(file, mode="w") as csvFileWrite:
      writer = csv.writer(csvFileWrite)
      text = [f"Americanas,{Player.Acoes["Americanas"]}|123Milhas,{Player.Acoes["123Milhas"]}"], f"Dinheiro,{Player.Money}"
      writer.writerow(text)
      csvFileWrite.close()


def openData():
   path = os.environ.get("LOCALAPPDATA")
   file = f"{path}\\system_data.csv"
   with open(file, mode='r') as csvFileRead:
      data = list(csv.reader(csvFileRead))
      if data:
         print("Opening saved game!!!")
         print("Data:", data)
      else:
         saveData()


def inicialPrints():
   printDelayed("Bem vindo ao tigrinho, jogue para conseguir dinheiro!!!\n")
   printDelayed("Você poderá ver suas estatísticas digitando 'r'")
   printDelayed("Para ver o manual digite 'm'")
   printDelayed("Você iniciará com: ")
   printDelayedColor("\tR$10", Colors.GREEN)


def showRules():
   printDelayedColor("______________________________", Colors.BLUE, 0.01)
   printDelayed("Tecla                     Ação", 0.01)
   printDelayed("a________________Mostrar bolsa", 0.01)
   printDelayed("r_________Mostrar estatísticas", 0.01)
   printDelayed("Ctrl+c_______Encerrar programa", 0.01)
   printDelayedColor("______________________________\n", Colors.BLUE, 0.01)


def getActions():
   texts = []
   for key, value in Player.Acoes.items():
      texts.append(f"\t{key}: {value}")
   return texts

def showRank():
   printDelayedColor("______________________________", Colors.BLUE, 0.01)
   printDelayed("Dinheiro: ")
   printDelayedColor(f"\t{Player.Money}", Colors.GREEN)
   printDelayed("Ações: ")
   for i in getActions():
      printDelayedColor(i, Colors.BROWN)
   printDelayedColor("______________________________\n", Colors.BLUE, 0.01)


def showB3():
   printDelayedColor("___________________________________", Colors.BLUE, 0.01)
   printDelayed("Mostrando ações da bolsa no momento", 0.05)
   printDelayed(f"Americanas__________________R${B3.Americanas}", 0.05)
   printDelayed(f"123Milhas__________________R${B3.Milhas}", 0.05)
   printDelayedColor("___________________________________\n", Colors.BLUE, 0.01)


def on_press(key):
   if key == keyboard.KeyCode.from_char('a'):
      showB3()
   if key == keyboard.KeyCode.from_char('m'):
      showRules()
   if key == keyboard.KeyCode.from_char('r'):
      showRank()
   if key == keyboard.KeyCode.from_char('s'):
      saveData()


def on_release(key):
   pass


def game():
   openData()
   inicialPrints()
   listener = keyboard.Listener(on_press=on_press, on_release=on_release)
   listener.start()


if __name__ == "__main__":
   game()

   while True:
      a = 1

