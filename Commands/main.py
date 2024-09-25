import mongo
#import argon2
import commands
import getpass
import read_commands
import graphic

  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = mongo.get_database()

   #code pour lancer le projet en interface graphique
   graphic.ToDoApp(dbname).run()

   #code pour lancement du programme en ligne de commande
   #cmd = input("Hello, welcome to my version of a smart To-Do List manager.To whom do I have the honour?\nPlease type \"register <name>\" to register and \"login <name>\" to login. You can type \"help\" to see the other commands.\n")
   #
   #while cmd.split(" ")[0] not in ["register","login","help"]:
   #   cmd = input("Please register or login before doing anything else. You can always use help to see the commands for further use.\n")
   #status = read_commands.read_cmd(cmd, dbname)
   #while(1):
   # cmd = input()
   # status = read_commands.read_cmd(cmd, dbname)
   # if status == 84: 
   #     break
    