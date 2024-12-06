import bcrypt
import getpass
from datetime import datetime
import shlex
from globals import connected_user, built_in_categories
from datetime import datetime, timedelta

def hash_password(plain_password):
    # Generate a salt and hash the password
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(plain_password.encode('utf-8'), salt)
    return hashed_password

#fonction d'enregistrement d'utilisateur interface graphique
def register_user(username, mail, password, dbname):
    global connected_user
    #on s'assure que l'utilisateur n'existe pas déjà
    if dbname["users"].find_one({"name":username}):
        return None, "User already exists"
    if len(password) < 7:
       #password = getpass.getpass("Not strong enough. Try again:\n")
       return None, "Not strong enough. Try again:"
    if len(password) >= 7:
        hpwd = hash_password(password)
        #créer le dictionnaire qui va contenir les informations de l'utilisateur
        #new_user_infos is a dictionary containing all the information about the user that is trying to register
        new_user_infos = {"name":username, "mail":mail, "password":hpwd}

        users_collection = dbname["users"]
        if users_collection.insert_one(new_user_infos):
            #print("Registration successful! Proceed.\n")
            connected_user = username
            return dbname, "Registration succesful!"
    return None, ""

#fonction de connexion de l'interface graphique
def login_user(username, password, dbname):
    global connected_user
    users_collection = dbname["users"]
    #l'utilisateur met son nom
    looging_user = users_collection.find_one({"name":username})
    #rechercher l'utilisateur
    if looging_user:
        #s'il existe,on lui demande son mot de passe,sinon, on lui dit qu'il n'existe pas
        #vérifier que le mot de passe est correct
        pwd_check = bcrypt.checkpw(password.encode('utf-8'), looging_user["password"])
        if not pwd_check:
            return None, "Incorrect password"
            #password = getpass.getpass("Password incorrect:\n")
            #pwd_check = bcrypt.checkpw(password.encode('utf-8'), looging_user["password"])
        else:
            #print("Login successful!\n")
            connected_user = username
            return dbname, "Login successful!"
    return None, ""

#fonction pour récupérer toutes les tâches
def tasks(dbname):
    #utilisé dans l'interface graphique pour voir les tâches
    tasks_collection = dbname["tasks"]
    
    print('None' if connected_user == None else connected_user)
    # Find tasks where the creator_name matches the connected user
    user_tasks = list(tasks_collection.find({"creator_name": connected_user}, {"_id":0, "creator_name":1, "name": 1, "description": 1, "deadline":1, "priority":1, "status":1, "category":1, "creation_date": 1, "edited": 1}))
    for tasks in user_tasks:
        print(tasks)
    # Convert the cursor to a list and return the tasks
    return user_tasks

#fonction pour récupérer les tâches à compléter (to do et in progress)
def pending(dbname):
    #utilisé dans l'interface graphique pour voir les tâches
    tasks_collection = dbname["tasks"]
    
    print('None' if connected_user == None else connected_user)
    # Find tasks where the creator_name matches the connected user
    user_tasks = list(tasks_collection.find({"creator_name": connected_user, "status": {"$in": ["in progress", "to-do"]}}, {"_id":0, "creator_name":1, "name": 1, "description": 1, "deadline":1, "priority":1, "status":1, "category":1, "creation_date": 1,"edited": 1}))
    for tasks in user_tasks:
        print(tasks)
    # Convert the cursor to a list and return the tasks
    return user_tasks

#fonction pour récupérer les tâches complétées
def completed_tasks(dbname):
    #utilisé dans l'interface graphique pour voir les tâches
    tasks_collection = dbname["tasks"]
    
    print('None' if connected_user == None else connected_user)
    # Find tasks where the creator_name matches the connected user
    user_tasks = list(tasks_collection.find({"creator_name": connected_user, "status": "completed"}, {"_id":0, "creator_name":1, "name": 1, "description": 1, "deadline":1, "priority":1, "status":1, "category":1, "creation_date": 1,"edited": 1}))
    for tasks in user_tasks:
        print(tasks)
    # Convert the cursor to a list and return the tasks
    return user_tasks

#function to edit a task
def task_edition(updated_task, dbname):
    tasks_collection = dbname["tasks"]
    task_to_edit = tasks_collection.find_one({"name":updated_task["initial_task"],"creator_name":connected_user})
    edition_list = task_to_edit.get("edited", [])
    if edition_list is None:
        edition_list = []
    edition_list.append(datetime.now())  # This updates the list in place
    updated_task["edited"] = edition_list
    del updated_task["initial_task"]
    print(updated_task)
    new_fields = {
        "$set": updated_task
    }
    edited = tasks_collection.update_one({"_id": task_to_edit["_id"]}, new_fields)
    if edited.matched_count > 0:
        if edited.modified_count > 0:
            print("Task updated.\n")
        else:
            print("No changes were made to the task.\n")
    return dbname

#function to create tasks
def task_creation(task, dbname):
    task_infos = {
                "creator_name": connected_user,
                "name": task["name"],
                "description": task["description"],
                "deadline": task["deadline"],
                "priority": task["priority"],
                "status": task["status"],
                "category": task["category"],
                "creation_date": datetime.now(),
                "edited":[]
            }
    tasks_collection = dbname["tasks"]
    if tasks_collection.insert_one(task_infos): print("Task saved!\n")
    else: print("Operation cancelled!\n")
    return dbname

def task_deletion(task_name, dbname):
        #l'utilisateur a tapé delete_task <nom de la tâche>
    tasks_collection = dbname["tasks"]
    if tasks_collection.find_one({"name":task_name,"creator_name":connected_user}):
        #on recherche maintenant la tâche en fonction de son nom et du nom du créateur de la tâche
        if tasks_collection.delete_one({"name":task_name,"creator_name":connected_user}):
            print("Task deleted\n")
        else: print("Operation cancelled.\n")
    return dbname

def search_func(key_word, dbname):
    #l'utilisateur a tapé search "<mots clés>"
    tasks_collection = dbname["tasks"]
    query = {
        "$or": [
            {"name": {"$regex": key_word, "$options": "i"}},  # Case-insensitive search in 'title'
            {"description": {"$regex": key_word, "$options": "i"}}  # Case-insensitive search in 'description'
        ]
    }
    # Execute the query
    documents = list(tasks_collection.find(query, {"_id": 0}))
    return documents

def filter_func(selected_date, selected_status, selected_category, selected_priority, dbname):
    #l'utilisateur a tapé filter puis des tas de mots clés
    tasks_collection = dbname["tasks"]
    query_conditions = dict()
    query_conditions["creator_name"] = connected_user
    if selected_date != None:
        query_conditions["deadline"] = {
                "$gte": selected_date,
                "$lt": selected_date + timedelta(days=1) - timedelta(microseconds=1)
            }
    if selected_status.lower() != "all":
        print(f"status:{selected_status}")
        query_conditions["status"] = selected_status
    if selected_priority.lower() != "all":
        print(f"priority:{selected_priority}")
        query_conditions["priority"] = selected_priority
    if selected_category.lower() != "all":
        print(f"category:{selected_category}")
        query_conditions["category"] = selected_category
    #verify that the conditions are there
    if query_conditions:
    # Execute the query
        documents = list(tasks_collection.find(query_conditions, {"_id": 0}))
        #print(documents)
    return documents