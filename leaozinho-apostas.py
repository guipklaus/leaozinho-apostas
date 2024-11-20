from pynput import keyboard
import csv
import os
from time import sleep


class Player:
   Money = 12.0
   actions = {
      "Americanas": 0,
      "123Milhas": 0
   }


class B3:
   actions = {
      "Americanas": 0.001,
      "123Milhas": 0.2
   }


   def getActions():
      texts = []
      for key, value in Player.actions.items():
         texts.append(f"\t{key}: {value}")
      return texts


   def soldAction( name, quant: int = 1):
      if Player.actions[name] >= int(quant):
         Player.actions[name] -= int(quant)
         Player.Money += B3.actions[name] * int(quant)
         printDelayed(f"|Aprovado|\n   Saldo = |{Player.Money}|", [Colors.GREEN, Colors.BROWN])
      else:
         printDelayed(f"|Negado|\n  Você possui |{Player.actions[name]}|, e tentou vender |{int(quant)}|", [Colors.RED, Colors.BROWN, Colors.BROWN])


   def buyAction(name: str, quant: int = 1):
      totalValue = B3.actions[name] * int(quant)
      if Player.Money > totalValue:
         Player.Money -= float("%.4f" %totalValue)
         Player.actions[name] += int(quant)
         printDelayed(f"|Aprovado|\n   Saldo = |{Player.Money}|", [Colors.GREEN, Colors.BROWN])
      else:
         printDelayed(f"Você precisa de |R${totalValue}|, mas só tem |R${Player.Money}|", [Colors.LIGHT_GREEN, Colors.LIGHT_RED])


   def Open():
      game.b3Open = True
      printDelayed("|___________________________________|", Colors.BLUE, time=0.01)
      printDelayed("Mostrando ações da bolsa no momento", time=0.05)
      for key, value in B3.actions.items():
         last = 30 - (len(str(key)) + len(str(value)))
         underlines = "_" * last
         printDelayed(f"   |{key}|" + underlines + f"|R${value}|", [Colors.BROWN, Colors.GREEN], time=0.004)


   def Close():
      printDelayed("|___________________________________|\n", Colors.BLUE, time=0.01)
      game.b3Open = False


   def EditMode():
      game.isTyping = True
      playerInput = [i.strip() for i in input(">>>").split()]
      if playerInput[0].lower() == "exit":
         game.isTyping = False
         return

      if len(playerInput) == 3:
         buySold, actionName, quant = playerInput
         if buySold.lower() == "comprar":
            B3.buyAction(actionName, quant)
            B3.EditMode()
         elif buySold.lower() == "vender":
            B3.soldAction(actionName, quant)
            B3.EditMode()
         else:
            printDelayed("|Insira a sintaxe correta|", Colors.RED, 0.0001)
            B3.EditMode()
      else:
         printDelayed("|Insira a sintaxe correta|", Colors.RED, 0.0001)
         B3.EditMode()


   def Help():
      printDelayed("Para entrar no modo de trading, pressione '|t|'", Colors.BLUE)
      printDelayed("Para fazer transações de ações na bolsa, utilize a sintaxe a seguir:", time=0.05)
      printDelayed("\t       |Ação          Nome        Quantidade|", Colors.PURPLE, time=0.05)
      printDelayed("\t|(comprar ou vender)          (inteiro maior que 0)|\n", Colors.LIGHT_PURPLE, time=0.05)
      printDelayed("Para sair da bolsa, pressione '|esc|'", Colors.BLUE)


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
   printDelayed("|b|________________Mostrar bolsa", Colors.CYAN, time=0.01)
   printDelayed("|r|_________Mostrar estatísticas", Colors.CYAN, time=0.01)
   printDelayed("|s|__________________Salvar jogo", Colors.CYAN, time=0.01)
   printDelayed("|esc|__________Encerrar programa", Colors.CYAN, time=0.01)
   printDelayed("|______________________________|\n", Colors.BLUE, time=0.01)


def showRanking():
   printDelayed("|______________________________|", Colors.BLUE, time=0.01)
   printDelayed(f"Dinheiro: |\t{Player.Money}|", Colors.GREEN)
   printDelayed("Ações: ")
   for action in B3.getActions():
      printDelayed(f"|{action}|", Colors.BROWN)
   printDelayed("|______________________________|\n", Colors.BLUE, time=0.01)


def on_press(key):
   if not game.isTyping:
      if game.b3Open:
         if key == keyboard.KeyCode.from_char('m'):
            B3.Help()
         if key == keyboard.KeyCode.from_char('t'):
            B3.EditMode()
         if key == keyboard.Key.esc:
            B3.Close()
      else:
         if key == keyboard.KeyCode.from_char('b'):
            B3.Open()
         if key == keyboard.KeyCode.from_char('m'):
            showRules()
         if key == keyboard.KeyCode.from_char('r'):
            showRanking()
         if key == keyboard.KeyCode.from_char('s'):
            game.saveData()
         if key == keyboard.Key.esc:
            game.saveData()
            printDelayed("|█||█||█|Encerrando programa|█||█||█|", [Colors.GREEN, Colors.YELLOW, Colors.BLUE, Colors.BLUE, Colors.YELLOW, Colors.GREEN])
            game.playing = False


def on_release(key):
   pass


class Game():
   playing = False
   isTyping = False
   b3Open = False

   path = os.environ.get("LOCALAPPDATA")
   file = f"{path}\\system_data.csv"

   def start(self):
      self.openData()
      self.inicialPrints()
      self.playing = True


   def inicialPrints(self):
      printDelayed("Bem vindo ao Leãozinho, jogue para conseguir dinheiro!!!\n")
      printDelayed("Você poderá ver suas estatísticas digitando 'r'", time=0.05)
      printDelayed("Para ver o manual digite 'm'", time=0.05)
      printDelayed("Para ver o manual da B3 digite 'm' quando estiver na B3", time=0.05)
      printDelayed(f"Você iniciará com: |R${Player.Money}|", Colors.GREEN)


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
            printDelayed("|Opening saved game!!!|", Colors.GREEN, 0.01)
            data = data[0]
            actionList, money = data

            if money.split(",")[0] == "Dinheiro":
               Player.Money = float(money.split(",")[1])

            for actionText in actionList.split("|"):
               nome, quant = actionText.split(",")
               Player.actions[nome] = int(quant)
         else:
            self.saveData()


if __name__ == "__main__":
   game = Game()
   game.start()

   listener = keyboard.Listener(on_press=on_press, on_release=on_release)
   listener.start()

   while game.playing:
      pass
