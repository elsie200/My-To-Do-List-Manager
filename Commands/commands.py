#this file will contain all the commands for the project
import bcrypt
import getpass
from datetime import datetime
import shlex
from globals import connected_user, built_in_categories


#connected_user=""
#built_in_categories = ["Work/Professional", "Personal", "Home", "Education/Learning", "Health/Fitness", "Social", "Travel", "Creativity/Projects", "Goals and Long-Term Plans"]

def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

#fonction d'enregistrement d'utilisateur ligne de commande
def register(username,dbname):
    global connected_user
    mail = input("Enter a valid mail adress:\n")
    #add a verification with regex
    password = getpass.getpass("Set a password. It has to be at least 7 characters long:\n") 
    while len(password) < 7:
       password = getpass.getpass("Not strong enough. Try again:\n")
       if len(password) >= 7:
         break
    hpwd = hash_password(password)

    #créer le dictionnaire qui va contenir les informations de l'utilisateur
    #new_user_infos is a dictionary containing all the information about the user that is trying to register
    new_user_infos = {"name":username, "mail":mail, "password":hpwd}

    users_collection = dbname["users"]
    if users_collection.insert_one(new_user_infos):
        print("Registration successful! Proceed.\n")
        connected_user = username
    return dbname

def login(username, dbname):
    global connected_user
    users_collection = dbname["users"]
    #l'utilisateur met son nom
    looging_user = users_collection.find_one({"name":username})
    #rechercher l'utilisateur
    if looging_user:
        #s'il existe,on lui demande son mot de passe,sinon, on lui dit qu'il n'existe pas
        #vérifier que le mot de passe est correct
        password = getpass.getpass("What's your password? ")
        pwd_check = bcrypt.checkpw(password.encode('utf-8'), looging_user["password"])
        while not pwd_check:
            password = getpass.getpass("Password incorrect:\n")
            pwd_check = bcrypt.checkpw(password.encode('utf-8'), looging_user["password"])
        print("Login successful!\n")
        connected_user = username
        return dbname
    return dbname

def add_task(task_name, dbname):
    global connected_user
    #l'utilisateur a tapé add_task <nom de la tâche>
    #je cherche le document qui lui correspond dans la collection users pour récupérer son id
    users_collection = dbname["users"]
    logging_user = users_collection.find_one({"name":connected_user})
    if logging_user:
        description = input("What is the task about? Please input description.\n")
        deadline = datetime.strptime(input("Enter a due-date under this format: YYYY-MM-DD HH:MM:SS\n"), '%Y-%m-%d %H:%M:%S')
        while deadline < datetime.now():
            deadline = datetime.strptime(input("Enter a valid due-date under this format: YYYY-MM-DD HH:MM:SS"), '%Y-%m-%d %H:%M:%S')
        #vérifier que la date est dans le bon format
        #après, je vais implémenter un calendrier dans l'interface graphique
        category = input("To what category does this task belong? Choose between these or create your own: Work/Professional, Personal, Home, Education/Learning, Health/Fitness, Social, Travel, Creativity/Projects, Goals/Long-Term Plans\n")
        if category not in built_in_categories:
            built_in_categories.append(category)
        priority = input("Task priority: low, medium, high?\n")
        while priority.lower() not in ["low","medium","high"]:
            priority = input("Task priority: low, medium, high?\n")
        status=input("Whats is the current status of the task: to-do, in progress, completed?\n")
        while status.lower() not in ["to-do","in progress","completed"]:
            status = input("Task status: to-do, in progress, completed?\n")
        save=input("Should we save this task? Write \"yes\" if you want to and \"no\" if not \n")
        if save.lower() =="yes":
            task_infos = {
                "creator_name":connected_user,
                "name":task_name,
                "description": description,
                "deadline":deadline,
                "priority":priority,
                "status":status,
                "category":category,
                "creation_date": datetime.now(),
                "edited":[]
            }
            tasks_collection = dbname["tasks"]
            if tasks_collection.insert_one(task_infos): print("Task saved!\n")
        else: print("Operation cancelled!\n")
    return dbname


def edit_task(task_name, dbname):
    #l'utilisateur a tapé edit_task <nom de la tâche>
    #on recherche maintenant la tâche en fonction de son nom et du nom du créateur de la tâche
    tasks_collection = dbname["tasks"]
    task_to_edit = tasks_collection.find_one({"name":task_name,"creator_name":connected_user})
    if task_to_edit:
        #récupérer les champs que l'utilisateur veut modifier
        cmd = input("To edit this task, enter the fields to edit like so:\nFor the fields name and descriprion, use this syntax <field>:\"new value\".\nFor deadline, enter a valid date like so deadline:\"YYYY-MM-DD HH:MM:SS\".\nFor priority, category and status: <field>:<value>.\nYou can edit multiple fields at the same time, just separate by a space.\n")
        #vérification des champs
        #Séparer chaque élément à éditer
        fields = shlex.split(cmd)
        # Séparer chaque élément en clé/valeur
        result = [item.split(':', 1) for item in fields]
        key_value = {key: value for key, value in result}
        #maitenant, je m'assure de ce que la personne a bien entré les valeurs, l'interface graphique aura un dropdown
        if "deadline" in key_value:
            while not datetime.strptime(key_value["deadline"], '%Y-%m-%d %H:%M:%S'):
                key_value["deadline"] = datetime.strptime(input("Enter a valid due-date under this format: YYYY-MM-DD HH:MM:SS"), '%Y-%m-%d %H:%M:%S')
        if "priority" in key_value:
            while key_value["priority"].lower() not in ["low","medium","high"]:
                key_value["priority"] = input("Task priority: low, medium, high?\n")
        if "status" in key_value:
            while key_value["status"].lower() not in ["to-do","in progress","completed"]:
                key_value["status"] = input("Task status: to-do, in progress, completed?\n")
        if "category" in key_value:
            print(key_value["category"])
            while key_value["category"] not in built_in_categories:
                key_value["category"] = input("Task status: to-do, in progress, completed?\n")
        save=input("Should we save this task? Write \"yes\" if you want to and \"no\" if not \n")
        if save.lower() =="yes":
            edition_list = task_to_edit.get("edited", [])
            if edition_list is None:
                edition_list = []
            edition_list.append(datetime.now())  # This updates the list in place
            key_value["edited"] = edition_list
            print(key_value)
            new_fields = {
                "$set": key_value
            }
            edited = tasks_collection.update_one({"_id": task_to_edit["_id"]}, new_fields)
            if edited.matched_count > 0:
                if edited.modified_count > 0:
                    print("Task updated.\n")
                else:
                    print("No changes were made to the task.\n")
                
        else: print("Operation cancelled.\n")
    return dbname

def delete_task(task_name, dbname):
    #l'utilisateur a tapé delete_task <nom de la tâche>
    tasks_collection = dbname["tasks"]
    if tasks_collection.find_one({"name":task_name,"creator_name":connected_user}):
        confirm = input("Are you sure about this action? Input yes or no.\n")
        if confirm.lower() == "yes":
            #on recherche maintenant la tâche en fonction de son nom et du nom du créateur de la tâche
            if tasks_collection.delete_one({"name":task_name,"creator_name":connected_user}):
                print("Task deleted\n")
        else: print("Operation cancelled.\n")
    return dbname

def ongoing_tasks(dbname):
    #l'utilisateur a tapé ongoing_tasks
    tasks_collection = dbname["tasks"]
    # if we don't want to print id then pass _id:0
    for x in tasks_collection.find({"creator_name": connected_user}, {"_id":0, "name": 1, "description": 1, "deadline":1, "priority":1, "status":1, "category":1, "creation_date": 1 }): 
        print(x)


def view_completed_tasks(dbname):
    #l'utilisateur a tapé view_completed_tasks
    tasks_collection = dbname["tasks"]
    # if we don't want to print id then pass _id:0
    for x in tasks_collection.find({"status":"completed"}): 
        print(x)

def view_task(task_name, dbname):
    #l'utilisateur a tapé view_task "<nom de la tâche>"
    tasks_collection = dbname["tasks"]
    task_to_edit = tasks_collection.find_one({"name":task_name,"creator_name":connected_user}, {"_id": 0})
    if task_to_edit:
        print(task_to_edit)

def search(key_word, dbname):
    #l'utilisateur a tapé search "<mots clés>"
    tasks_collection = dbname["tasks"]
    query = {
        "$or": [
            {"name": {"$regex": key_word, "$options": "i"}},  # Case-insensitive search in 'title'
            {"description": {"$regex": key_word, "$options": "i"}}  # Case-insensitive search in 'description'
        ]
    }
    # Execute the query
    documents = tasks_collection.find(query, {"_id": 0})
    if documents:
        for doc in documents:
            print(doc)
    return dbname

def filter(cmd, dbname):
    #l'utilisateur a tapé filter puis des tas de mots clés
    tasks_collection = dbname["tasks"]
    query_conditions = []
    #regarder les valeurs selon lesquelles l'utilisateur veut filtrer
    fields = shlex.split(cmd)
        # Séparer chaque élément en clé/valeur
    result = [item.split(':', 1) for item in fields]
    key_value = {key: value for key, value in result}

    #maitenant, je m'assure de ce que la personne a bien entré les valeurs et je filtre, l'interface graphique aura un dropdown
    if "name" in key_value:
        query_conditions.append({"name": {"$regex": key_value["name"], "$options": "i"}})
    if "description" in key_value:
        query_conditions.append({"description": {"$regex": key_value["description"], "$options": "i"}})
    if "deadline" in key_value:
        while not datetime.strptime(key_value["deadline"], '%Y-%m-%d %H:%M:%S'):
            key_value["deadline"] = datetime.strptime(input("Enter a valid due-date under this format: YYYY-MM-DD HH:MM:SS"), '%Y-%m-%d %H:%M:%S')
        query_conditions.append({"deadline": {"$regex": key_value["deadline"], "$options": "i"}})    
    if "priority" in key_value:
        while key_value["priority"].lower() not in ["low","medium","high"]:
            key_value["priority"] = input("Task priority: low, medium, high?\n")
        query_conditions.append({"priority": {"$regex": key_value["priority"], "$options": "i"}})
    if "status" in key_value:
        while key_value["status"].lower() not in ["to-do","in progress","completed"]:
            key_value["status"] = input("Task status: to-do, in progress, completed?\n")
        query_conditions.append({"status": {"$regex": key_value["status"], "$options": "i"}})
    #verify that the conditions are there
    if query_conditions:
        query = {"$or": query_conditions}
    else:
        query = {}
    # Execute the query
    documents = tasks_collection.find(query, {"_id": 0})
    if documents:
        for doc in documents:
            print(doc)
    return dbname