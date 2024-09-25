import commands
#pour splitter en respectant les guillemets
import shlex

command_map = {
    "login": commands.login,
    "register": commands.register,
    "add_task": commands.add_task,
    "edit_task": commands.edit_task,
    "delete_task": commands.delete_task,
    "view_task": commands.view_task,
    "search": commands.search
}

single_arg_command_map = {
    #"ongoing_tasks": commands.ongoing_tasks,
    "ongoing_tasks": commands.ongoing_tasks,
    "view_completed_tasks": commands.view_completed_tasks
}

def read_cmd(user_input, dbname):
    split_cmd = shlex.split(user_input)
    #faire des switch case ou des ternaires pour appeler les fonctions au bon moment
    if len(split_cmd) == 1:
        if split_cmd[0] == "help":
            print("help")
        if split_cmd[0] == "exit":
            #84 is the exit code
            return(84)
    if len(split_cmd) == 1 and split_cmd[0] in single_arg_command_map:
        single_arg_command_map[split_cmd[0]](dbname)
    if len(split_cmd) == 2 and split_cmd[0] in command_map:
        dbname = command_map[split_cmd[0]](split_cmd[1], dbname)
    return 0