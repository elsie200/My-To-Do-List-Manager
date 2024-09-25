from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.core.window import Window
import gcommands
from functools import partial
from kivy.graphics import Color, Line, RoundedRectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput


class TaskEditionScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(TaskEditionScreen, self).__init__(**kwargs)
        main_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint=(1, 1))
        self.dbname = dbname
        # Left column (Project Name, Project Description, Status)
        left_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        left_layout.bind(minimum_height=left_layout.setter('height'))
        # Project Name
        left_layout.add_widget(Label(text="[b]Project Name[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_name_input = TextInput(size_hint=(1, None), height=50)
        left_layout.add_widget(self.project_name_input)
        # Project Description
        left_layout.add_widget(Label(text="[b]Project description[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_description_input = TextInput(size_hint=(1, None), height=100)
        left_layout.add_widget(self.project_description_input)
        # Status
        left_layout.add_widget(Label(text="[b]Status[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.status_input = TextInput(size_hint=(1, None), height=50)
        left_layout.add_widget(self.status_input)
        # Right column (Deadline, Category, Priority)
        right_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        right_layout.bind(minimum_height=right_layout.setter('height'))
        # Deadline
        right_layout.add_widget(Label(text="[b]Deadline[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.deadline_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.deadline_input)
        # Category
        right_layout.add_widget(Label(text="[b]Category[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.category_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.category_input)
        # Priority
        right_layout.add_widget(Label(text="[b]Priority[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.priority_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.priority_input)
        # Add left and right layouts to the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        # Buttons layout (Edit, Delete, Back)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=70, spacing=20)
        # Back Button (Placed on the left side, styled to match the others)
        back_button = Button(text="Back", background_color=(0, 0.5, 1, 1), size_hint=(0.4, 1))
        back_button.bind(on_press=self.go_back)  # Function to go back to the previous screen
        buttons_layout.add_widget(back_button)
        # Save Button
        save_button = Button(text="Save", background_color=(0, 0, 1, 1), size_hint=(0.4, 1))
        save_button.bind(on_press=self.save_task)
        buttons_layout.add_widget(save_button)
        # Add main and buttons layout to the screen
        final_layout = BoxLayout(orientation='vertical', spacing=10)
        # Add buttons layout at the top for easier navigation
        # Add the task details below
        final_layout.add_widget(main_layout)
        final_layout.add_widget(buttons_layout)

        self.add_widget(final_layout)

    def set_task_data(self, task):
        self.project_name_input.text = task['name']
        self.project_description_input.text = task['description']
        self.deadline_input.text = task['deadline'].strftime('%Y-%m-%d')
        self.category_input.text = task['category']
        self.priority_input.text = task['priority']
        self.status_input.text = task['status']
    
    def save_task(self, instance):
        # Logic to save the edited task back to the database
        # You will need to define how to update the task in your DB here
        updated_task = {
            'name': self.project_name_input.text,
            'description': self.project_description_input.text,
            'deadline': gcommands.datetime.strptime(self.deadline.text, '%Y-%m-%d'),
            'category': self.category_input.text,
            'priority': self.priority_input.text,
            'status': self.status_input.text
        }
        self.dbname = gcommands.task_edition(updated_task,self.dbname)
        # Call your database update function here
        # e.g., update_task_in_db(updated_task)
        self.go_back(instance)
    
    def go_back(self, instance):
        # Navigate back to the task list
        self.manager.current = 'task_details'


class TaskAddingScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(TaskAddingScreen, self).__init__(**kwargs)
        main_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint=(1, 1))
        self.dbname = dbname
        # Left column (Project Name, Project Description, Status)
        left_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        left_layout.bind(minimum_height=left_layout.setter('height'))
        # Project Name
        left_layout.add_widget(Label(text="[b]Project Name[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_name_input = TextInput(size_hint=(1, None), height=50)
        left_layout.add_widget(self.project_name_input)
        # Project Description
        left_layout.add_widget(Label(text="[b]Project description[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_description_input = TextInput(size_hint=(1, None), height=100)
        left_layout.add_widget(self.project_description_input)
        # Status
        left_layout.add_widget(Label(text="[b]Status[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.status_input = TextInput(size_hint=(1, None), height=50)
        left_layout.add_widget(self.status_input)
        # Right column (Deadline, Category, Priority)
        right_layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
        right_layout.bind(minimum_height=right_layout.setter('height'))
        # Deadline
        right_layout.add_widget(Label(text="[b]Deadline[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.deadline_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.deadline_input)
        # Category
        right_layout.add_widget(Label(text="[b]Category[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.category_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.category_input)
        # Priority
        right_layout.add_widget(Label(text="[b]Priority[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.priority_input = TextInput(size_hint=(1, None), height=50)
        right_layout.add_widget(self.priority_input)
        # Add left and right layouts to the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        # Buttons layout (Edit, Delete, Back)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=70, spacing=20)
        # Back Button (Placed on the left side, styled to match the others)
        back_button = Button(text="Back", background_color=(0, 0.5, 1, 1), size_hint=(0.4, 1))
        back_button.bind(on_press=self.go_back)  # Function to go back to the previous screen
        buttons_layout.add_widget(back_button)
        # Save Button
        save_button = Button(text="Save", background_color=(0, 0, 1, 1), size_hint=(0.4, 1))
        save_button.bind(on_press=self.save_task)
        buttons_layout.add_widget(save_button)
        # Add main and buttons layout to the screen
        final_layout = BoxLayout(orientation='vertical', spacing=10)
        # Add buttons layout at the top for easier navigation
        # Add the task details below
        final_layout.add_widget(main_layout)
        final_layout.add_widget(buttons_layout)

        self.add_widget(final_layout)
    
    def save_task(self, instance):
        # Logic to save the edited task back to the database
        # You will need to define how to update the task in your DB here
        updated_task = {
            
            'name': self.project_name_input.text,
            'description': self.project_description_input.text,
            'deadline': gcommands.datetime.strptime(self.deadline.text, '%Y-%m-%d'),
            'category': self.category_input.text,
            'priority': self.priority_input.text,
            'status': self.status_input.text,
        }
        self.dbname = gcommands.task_edition(updated_task,self.dbname)
        # Call your database update function here
        # e.g., update_task_in_db(updated_task)
        self.go_back(instance)
    
    def go_back(self, instance):
        # Navigate back to the task list
        self.manager.current = 'task_list'
