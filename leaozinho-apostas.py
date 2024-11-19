from pynput import keyboard
import csv
import os
from time import sleep


class Player:
   Money = 10
   actions = {
      "Americanas": 0,
      "123Milhas": 0
   }


class B3:
   actions = {
      "Americanas": 0.001,
      "123Milhas": 0.2
   }


class Colors():
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


def printDelayed(texto: str, color=Colors.END, time=0.1):
   colors = ([Colors.END] + color if type(color) == list else [Colors.END, color])
   colored = False
   times = 0
   for char in texto:
      if char == "|":
         if not colored:
            times += 1
         print(Colors.END if colored else colors[times], end="", flush=True)
         colored = not colored
      else:
         print(char, end="", flush=True)
         sleep(time)
   print("")

def showRules():
   printDelayed("|______________________________|", Colors.BLUE, time=0.01)
   printDelayed("Tecla                     Ação", Colors.CYAN, time=0.01)
   printDelayed("|a|________________Mostrar bolsa", Colors.CYAN, time=0.01)
   printDelayed("|r|_________Mostrar estatísticas", Colors.CYAN, time=0.01)
   printDelayed("|esc|__________Encerrar programa", Colors.CYAN, time=0.01)
   printDelayed("|______________________________|\n", Colors.BLUE, time=0.01)


def getActions():
   texts = []
   for key, value in Player.actions.items():
      texts.append(f"\t{key}: {value}")
   return texts


def showRanking():
   printDelayed("|______________________________|", Colors.BLUE, time=0.01)
   printDelayed(f"Dinheiro: |\t{Player.Money}|", Colors.GREEN)
   printDelayed("Ações: ")
   for action in getActions():
      printDelayed(f"|{action}|", Colors.BROWN)
   printDelayed("|______________________________|\n", Colors.BLUE, time=0.01)


def showB3():
   printDelayed("|___________________________________|", Colors.BLUE, time=0.01)
   printDelayed("Mostrando ações da bolsa no momento", time=0.05)
   for key, value in B3.actions.items():
      last = 33 - (len(str(key)) + len(str(value)))
      underlines = "_" * last
      printDelayed(f"   |{key}|" + underlines + f"|R${value}|", [Colors.BROWN, Colors.GREEN])
   printDelayed("|___________________________________|\n", Colors.BLUE, time=0.01)


def on_press(key):
   if key == keyboard.KeyCode.from_char('a'):
      showB3()
   if key == keyboard.KeyCode.from_char('m'):
      showRules()
   if key == keyboard.KeyCode.from_char('r'):
      showRanking()
   if key == keyboard.KeyCode.from_char('s'):
      game.saveData()
   if key == keyboard.Key.esc:
      printDelayed("|█||█||█|Encerrando programa|█||█||█|", [Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.GREEN, Colors.YELLOW, Colors.BLUE])
      game.playing = False


def on_release(key):
   pass


class Game():
   playing = False
   path = os.environ.get("LOCALAPPDATA")
   file = f"{path}\\system_data.csv"

   def start(self):
      self.openData()
      self.inicialPrints()
      self.playing = True


   def inicialPrints(self):
      printDelayed("Bem vindo ao Leãozinho, jogue para conseguir dinheiro!!!\n")
      printDelayed("Você poderá ver suas estatísticas digitando 'r'")
      printDelayed("Para ver o manual digite 'm'")
      printDelayed("Você iniciará com: |R$10|", Colors.GREEN)


   def saveData(self):
      print("Saving...", end="\r")
      with open(self.file, mode="w") as csvFileWrite:
         writer = csv.writer(csvFileWrite)
         text = ""

         for key, value in Player.actions.items():
            text += f"{key},{value}|"

         writer.writerow([text[0:-1], f"Dinheiro,{Player.Money}"])
         csvFileWrite.close()


   def openData(self):
      with open(self.file, mode='r') as csvFileRead:
         data = list(csv.reader(csvFileRead))
         if data:
            print("Opening saved game!!!")
            print("Data:", data)
         else:
            self.saveData()


if __name__ == "__main__":
   game = Game()
   game.start()

   listener = keyboard.Listener(on_press=on_press, on_release=on_release)
   listener.start()

   while game.playing:
      pass
