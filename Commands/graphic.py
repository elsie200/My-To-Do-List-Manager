from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
import manage_tasks
import actions_pages
from kivymd.app import MDApp
from kivy.uix.image import Image


#client = MongoClient('mongodb://localhost:27017/')
#db = client['my_todo_app']
#users_collection = db['users']


# First screen to choose between Login and Register
class WelcomeScreen(Screen):
    def __init__(self, **kwargs):
        super(WelcomeScreen, self).__init__(**kwargs)
        #layout = BoxLayout(orientation='vertical')

        #définition de la disposition de la fenêtre
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.4, 0.7)
        self.window.pos_hint =  {"center_x":0.5, "center_y":0.5}
        # Add padding and spacing to the GridLayout
        self.window.padding = [20, 20, 20, 20]  # Padding around the grid
        self.window.spacing = [10, 10]  # Spacing between widgets

        logo_image = Image(source='mylogo.png', size_hint=(0.4, None), size=(500, 500), allow_stretch=True)
        logo_image.pos_hint = {"center_x": 0.5}  # Center the image horizontally
        self.window.add_widget(logo_image)
        #création et ajouts des widgets/éléments dans la fenêtre
        welcome_label = Label(text="Welcome to your Smart To-Do Manager", color=(0, 0, 0, 1), halign="center",valign="middle")
        self.window.add_widget(welcome_label)

        login_button = Button(text="Login", size_hint=(0.5, 0.4), bold=True, background_color="#1E88E5")
        self.window.add_widget(login_button)

        register_button = Button(text="Register", size_hint=(0.5, 0.4), bold=True, background_color="#1E88E5")
        self.window.add_widget(register_button)

        login_button.bind(on_press=self.go_to_login)
        register_button.bind(on_press=self.go_to_register)

        # Add the layout to the screen
        self.add_widget(self.window)

    def go_to_login(self, instance):
        # Navigate to the login screen
        self.manager.current = 'login'

    def go_to_register(self, instance):
        # Navigate to the registration screen
        self.manager.current = 'register'


# Login Screen (as before)
class LoginScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)

        Window.clearcolor = (1, 1, 1, 1)  # White background

        #layout = BoxLayout(orientation='vertical')
        #defining window distribution
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.4, 0.8)
        self.window.pos_hint =  {"center_x":0.5, "center_y":0.5}

        # Add padding and spacing to the GridLayout
        self.window.padding = [15,15,15,15]  # Padding around the grid
        self.window.spacing = [10, 10]  # Spacing between widgets

        logo_image = Image(source='mylogo.png', size_hint=(0.4, None), size=(500, 500), allow_stretch=True)
        logo_image.pos_hint = {"center_x": 0.5}  # Center the image horizontally
        self.window.add_widget(logo_image)
        #defining elements/widgets to add
        self.label = Label(text="[b]Login[/b]", font_size=40, color=(0, 0, 0, 1), halign="center",valign="middle",markup=True)
        self.window.add_widget(self.label)

        self.username = TextInput(hint_text='Username', multiline=False, hint_text_color="#000000", background_color=(1, 1, 1, 1))
        self.password = TextInput(hint_text='Password', multiline=False, hint_text_color="#000000", background_color=(1, 1, 1, 1), password=True, password_mask='*')
        self.dbname = dbname
        login_button = Button(text='Login', size_hint=(1, 0.6), bold=True, background_color="#004aad")
        back_button = Button(text='Back', size_hint=(1, 0.6), bold=True, background_color="#004aad")
        self.error_message = Label(text="", color=(1, 0, 0, 1))  # Empty error message, red color
        
        #defining some actions
        login_button.bind(on_press=self.login_action)  # Bind to verify function
        back_button.bind(on_press=self.go_to_welcome)
        
        #adding elements to the layout
        self.window.add_widget(self.username)
        self.window.add_widget(self.password)
        self.window.add_widget(login_button)
        self.window.add_widget(back_button)
        self.window.add_widget(self.error_message)

        self.add_widget(self.window)

    #function to login that uses the login_user function
    def login_action(self, instance):
        username = self.username.text
        password = self.password.text
        dbname = self.dbname

        data, msg = manage_tasks.gcommands.login_user(username, password, dbname)
        if data != None and msg == "Login successful!":
            self.error_message.text = "Login successful!"
            #afficher sur la fenêtre
            self.error_message.color = (0, 1, 0, 1)  # Green color for success
            self.go_to_manager(None)
        else:
            self.error_message.text = "Invalid username or password!"
            self.error_message.color = (1, 0, 0, 1)  # Red color for error
            # Optionally, clear the fields or leave them for correction
            self.username.text = ""
            self.password.text = ""
        
    def go_to_welcome(self, instance):
        # Navigate to the login screen
        self.manager.current = 'welcome'
    
    def go_to_manager(self, instance):
        # Navigate to the login screen
        self.manager.current = 'task_list'



# Registration Screen (as before)
class RegisterScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(RegisterScreen, self).__init__(**kwargs)
        #layout = BoxLayout(orientation='vertical')
        
        Window.clearcolor = (1, 1, 1, 1)

        #defining window distribution
        self.window = GridLayout()
        self.window.cols = 1
        self.window.size_hint = (0.4, 0.8)
        self.window.pos_hint =  {"center_x":0.5, "center_y":0.5}

        # Add padding and spacing to the GridLayout
        self.window.padding = [15,15,15,15]  # Padding around the grid
        self.window.spacing = [10, 10]  # Spacing between widgets

        logo_image = Image(source='mylogo.png', size_hint=(0.4, None), size=(500, 500), allow_stretch=True)
        logo_image.pos_hint = {"center_x": 0.5}  # Center the image horizontally
        self.window.add_widget(logo_image)
        #defining elements or widgets
        self.label = Label(text="[b]Register[/b]", font_size=40, color=(0, 0, 0, 1), halign="center",valign="middle", markup=True)
        self.mail = TextInput(hint_text='Mail address', multiline=False, hint_text_color=(0, 0, 0, 1))
        self.username = TextInput(hint_text='Username', multiline=False, hint_text_color=(0, 0, 0, 1))
        self.password = TextInput(hint_text='Input a strong password: at least seven characters', multiline=False, password=True, password_mask='*', hint_text_color=(0, 0, 0, 1))
        self.dbname = dbname
        register_button = Button(text='Register', size_hint=(1, 0.6), bold=True,  background_color="#004aad")
        back_button = Button(text='Back', size_hint=(1, 0.6), bold=True, background_color="#004aad")
        self.error_message = Label(text="", color=(1, 0, 0, 1))  # Empty error message, red color
        #defining some actions and binding
        register_button.bind(on_press=self.create_user)  # Bind to registration function
        back_button.bind(on_press=self.go_to_welcome) #goes back to the welcome page

        #adding elements/widgets to the window
        self.window.add_widget(self.label)
        self.window.add_widget(self.mail)
        self.window.add_widget(self.username)
        self.window.add_widget(self.password)
        self.window.add_widget(Label(text="Already have an account? Go back", font_size=18))
        self.window.add_widget(register_button)
        self.window.add_widget(back_button)
        self.window.add_widget(self.error_message)

        self.add_widget(self.window)

    #function used by the class to create/register a user
    def create_user(self, instance):
        username = self.username.text
        password = self.password.text
        mail = self.mail.text
        dbname = self.dbname

        data, msg = manage_tasks.gcommands.register_user(username, mail, password, dbname)
        if data != None and msg == "Registration succesful":
            self.error_message.text = "Registration succesful!"
            self.error_message.color = (0, 1, 0, 1)  # Green color for success
            self.go_to_manager(None)
        if data == None and msg == "User already exists":
            self.error_message.text = "User already exists"
            self.error_message.color = (1, 0, 0, 1)  # Red color for error
            # Optionally, clear the fields or leave them for correction
            self.username.text = ""
            self.password.text = ""
        if data == None and msg=="Not strong enough. Try again:":
            self.error_message.text = "Not strong enough. Try again:"
            self.error_message.color = (1, 0, 0, 1)
            self.username.text = ""
            self.password.text = ""
        else:
            self.error_message.text = "Something went wrong"
            self.error_message.color = (1, 0, 0, 1)
            self.username.text = ""
            self.password.text = ""

    def go_to_welcome(self, instance):
        # Navigate to the login screen
        self.manager.current = 'welcome'
    
    def go_to_manager(self, instance):
        # Navigate to the login screen
        self.manager.current = 'task_list'


# Managing the different screens
class ToDoApp(MDApp):
    def __init__(self, dbname, **kwargs):
        super(ToDoApp, self).__init__(**kwargs)
        self.dbname = dbname
    
    def build(self):
        sm = ScreenManager()

        # Add WelcomeScreen, LoginScreen, and RegisterScreen to ScreenManager
        sm.add_widget(WelcomeScreen(name='welcome'))
        sm.add_widget(LoginScreen(self.dbname, name='login'))
        sm.add_widget(RegisterScreen(self.dbname, name='register'))
        sm.add_widget(manage_tasks.TaskListScreen(self.dbname,name='task_list'))
        sm.add_widget(manage_tasks.TaskDetailScreen(self.dbname, name='task_details'))
        sm.add_widget(actions_pages.TaskEditionScreen(self.dbname, name='edit_task'))
        sm.add_widget(actions_pages.TaskAddingScreen(self.dbname, name='add_task'))
        #sm.add_widget(ManageTasks(self.dbname, name='manager'))

        return sm