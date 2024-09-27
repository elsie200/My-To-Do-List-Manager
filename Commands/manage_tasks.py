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
from kivy.graphics import Color, Line, RoundedRectangle, Rectangle
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.spinner import Spinner
from kivymd.uix.pickers import MDDatePicker
from kivy.uix.image import Image


def get_day_with_suffix(day):
    if 4 <= day <= 20 or 24 <= day <= 30:
        suffix = "th"
    else:
        suffix = ["st", "nd", "rd"][day % 10 - 1]
    return f"{day}{suffix}"

#popup pour les filtres
class FilterPopup(Popup):
    def __init__(self, task_list_screen, **kwargs):
        super(FilterPopup, self).__init__(**kwargs)
        self.task_list_screen = task_list_screen
        self.title = 'Filter Tasks'
        self.size_hint = (0.8, 0.8)
        # Create the form layout
        form_layout = GridLayout(cols=2, padding=10, spacing=10)
        # Date Filter
        date_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        # Add a label for the date on the left
        self.date_label = Label(text="Select Date:", size_hint=(0.4, None), height=50)  # Adjust size_hint if needed
        date_layout.add_widget(self.date_label)
        date_picker_btn = Button(text="Open Calendar", size_hint=(0.6, None), height=50)
        date_picker_btn.bind(on_release=self.open_calendar)
        date_layout.add_widget(date_picker_btn)
        form_layout.add_widget(date_layout)
        # Status Filter
        status_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        status_layout.add_widget(Label(text="Status:",size_hint=(0.4, None), height=50))
        #form_layout.add_widget(Label(text="Status:",size_hint_x=0.3))
        self.status_spinner = Spinner(
            text="All",
            values=("all", "to-do", "in progress", "completed"),
            size_hint=(0.6, None),
            height=50
        )
        status_layout.add_widget(self.status_spinner)
        form_layout.add_widget(status_layout)
        #form_layout.add_widget(self.status_spinner)

        # Category Filter
        category_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        category_layout.add_widget(Label(text="Category:",size_hint=(0.4, None), height=50))
        #form_layout.add_widget(Label(text="Category:",size_hint_x=0.3))
        self.category_spinner = Spinner(
            text="All",
            values=("All", "Work/Professional", "Personal", "Home", "Education/Learning", "Health/Fitness", "Social", "Travel", "Creativity/Projects", "Goals and Long-Term Plans"),
            size_hint=(0.6, None),
            height=50,
        )
        category_layout.add_widget(self.category_spinner)
        #form_layout.add_widget(self.category_spinner)
        form_layout.add_widget(category_layout)

        # Priority Filter
        priority_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        priority_layout.add_widget(Label(text="Priority:",size_hint=(0.4, None), height=50))
        #form_layout.add_widget(Label(text="Priority:",size_hint_x=0.3))
        self.priority_spinner = Spinner(
            text="All",
            values=("All", "high", "medium", "low"),
            size_hint=(0.6, None),
            height=50
        )
        priority_layout.add_widget(self.priority_spinner)
        #form_layout.add_widget(self.priority_spinner)
        form_layout.add_widget(priority_layout)
        # Add Filter Button
        filter_btn = Button(text="Apply Filter", size_hint=(1, None), background_color=(0, 0, 1, 1), height=50)
        filter_btn.bind(on_press=self.apply_filter)
        # Add form layout to the popup
        box = BoxLayout(orientation='vertical', padding=10, spacing=10)
        box.add_widget(form_layout)
        box.add_widget(filter_btn)
        self.content = box

    def open_calendar(self, instance):
        #date_dialog = MDDatePicker(callback=self.set_date)  # Create the date picker
        #date_dialog.open()
        date_dialog = MDDatePicker()  # Create the date picker
        date_dialog.bind(on_save=self.set_date)  # Bind the on_save event to set_date
        date_dialog.open()  # Open the date picker

    #function to set the date_label value using the value from the date picker
    def set_date(self, instance, value, *args):
        self.date_label.text = f"{value.strftime('%Y-%m-%d')}"

    #avec cette fonction, je récupère toutes les valeurs séclectionnées par l'utilisateur dans le filtre et j'appelle la fonction d'affichage des valeurs filtrées
    def apply_filter(self, instance):
        # Retrieve the values from the form
        try:
            selected_date = gcommands.datetime.strptime(self.date_label.text, '%Y-%m-%d')
        except:
            selected_date =  None
        selected_status = self.status_spinner.text
        selected_category = self.category_spinner.text
        selected_priority = self.priority_spinner.text
        # Trigger the callback with the selected filter values
        self.task_list_screen.display_filtered_data(selected_date, selected_status, selected_category, selected_priority)
        # Dismiss the popup
        self.dismiss()

#classe pour créer le bloc d'une tâche
class TaskFrame(BoxLayout):
    def __init__(self, task, task_list_screen, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.size_hint_y = None
        self.height = 100
        self.padding = 10
        self.spacing = 10
        self.task_list_screen = task_list_screen

        # Create a frame with rounded borders
        with self.canvas.before:
            Color(1, 1, 1, 1)  # Background color (light gray)
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
            Color(0, 0, 0, 1)  # Border color (black)
            self.border = Line(rounded_rectangle=[self.x, self.y, self.width, self.height, 15], width=2)
        # Bind to update the position and size of the rounded border and background
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        # Task name in bold above the deadline and status
        task_name = Label(text=f"[b]Name: {task['name']}[/b]", markup=True, size_hint_y=None, height=30, color=(0, 0, 0, 1))
        self.add_widget(task_name)
        # Layout for deadline and status in a row (Grid Layout or BoxLayout)
        task_details_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=40, spacing=10)
        if task['deadline'] < gcommands.datetime.today() and task["status"].lower() != 'completed':
            task_deadline = Label(text="Deadline: " + task['deadline'].strftime('%Y-%m-%d'), size_hint_x=0.4, color=(1, 0, 0, 1))
        else:
            task_deadline = Label(text="Deadline: " + task['deadline'].strftime('%Y-%m-%d'), size_hint_x=0.4, color=(0, 0, 0, 1))
        task_status = Label(text="Status: " + task['status'], size_hint_x=0.4, color=(0, 0, 0, 1))
        # Button to view task details
        view_button = Button(text="View", size_hint_x=0.2)
        view_button.bind(on_press=partial(self.task_list_screen.open_task_details, task))
        # Add deadline, status, and button to the task details layout
        task_details_layout.add_widget(task_deadline)
        task_details_layout.add_widget(task_status)
        task_details_layout.add_widget(view_button)
        # Add the task details layout to the main task frame
        self.add_widget(task_details_layout)

    def update_graphics(self, *args):
        # Update the position and size of the border and background to match the box layout's size
        self.bg.pos = self.pos
        self.bg.size = self.size
        self.border.rounded_rectangle = [self.x, self.y, self.width, self.height, 15]


#classe pour créer les tabs
class TaskTab(TabbedPanelItem):
    def __init__(self, category_name, dbname, task_list_screen, **kwargs):
        super().__init__(**kwargs)
        self.text = category_name
        self.dbname = dbname
        self.task_list_screen = task_list_screen
        self.layout = BoxLayout(orientation='vertical')
        self.tasks = []

        # Set white background
        with self.canvas.before:
            Color(1, 1, 1, 1)  # White color
            self.bg = RoundedRectangle(pos=self.pos, size=self.size, radius=[15])
        self.bind(pos=self.update_graphics, size=self.update_graphics)
        # ScrollView for tasks
        #self.scroll_view = ScrollView(size_hint=(1, 1), size=(Window.width, Window.height * 0.8))
        self.scroll_view = ScrollView(size_hint=(1, 1))
        self.task_list_layout = GridLayout(cols=1, spacing=30, size_hint_y=None)
        self.task_list_layout.bind(minimum_height=self.task_list_layout.setter('height'))
        self.scroll_view.add_widget(self.task_list_layout)
        self.layout.add_widget(self.scroll_view)
        self.display_tasks()
        # Add the layout to the screen
        self.add_widget(self.layout)

    def update_graphics(self, *args):
        self.bg.pos = self.pos
        self.bg.size = self.size
    
    #fonction d'affichage normal des tâches
    def display_tasks(self):
        print("hi test")
        # Retrieve tasks from the database
        if self.text == "All":
            tasks = gcommands.tasks(self.dbname)
        elif self.text == "Pending":
            tasks = gcommands.pending(self.dbname)
        elif self.text == "Completed":
            tasks = gcommands.completed_tasks(self.dbname)
        else:
            tasks = []
        self.tasks = tasks
        print("Tasks retrieved:", tasks)
        # Clear the layout before adding tasks
        self.task_list_layout.clear_widgets()
        # Add tasks to the layout
        for task in tasks:
            # Create a framed box for each task
            task_frame = TaskFrame(task, self.task_list_screen)
            # Add the task frame to the layout
            self.task_list_layout.add_widget(task_frame)

    #fonction pour filtrer l'affichage des tâches en fonction d'un mot dans la barre de recherche
    def filter_tasks(self):
        # Filter tasks based on the search query
        filtered_tasks = [task for task in self.tasks if self.task_list_screen.search_query.lower() in task['name'].lower() or self.task_list_screen.search_query.lower() in task['description'].lower()]
        self.task_list_layout.clear_widgets()
        # Add tasks to the layout
        for task in filtered_tasks:
            task_frame = TaskFrame(task, self.task_list_screen)
            self.task_list_layout.add_widget(task_frame)
    
    #fonction pour filtrer les résultats en fonction des résultats de la fonctionnalité filtre
    def filter_feature(self):
        print(self.task_list_screen.filtered_documents)
        print(self.tasks)
        filtered_tasks = [task for task in self.tasks if task in self.task_list_screen.filtered_documents]
        self.task_list_layout.clear_widgets()
        # Add tasks to the layout
        for task in filtered_tasks:
            task_frame = TaskFrame(task, self.task_list_screen)
            self.task_list_layout.add_widget(task_frame)

# Task List Screen
class TaskListScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(TaskListScreen, self).__init__(**kwargs)
        
        self.dbname = dbname
        #initialisation de la valeur de recherche
        self.search_query = ""
        #iniitialisation de l'élément représentant les valeurs de filtrage
        self.filtered_documents = []
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        top_section = BoxLayout(orientation='horizontal', size_hint_y=0.1, padding=[10, 10, 10, 10])
        #créer un layout top section
        current_date = gcommands.datetime.now().strftime(f"%B {get_day_with_suffix(gcommands.datetime.now().day)} %Y, %A")
        date = Label(text=current_date, font_size='20sp', size_hint=(0.5, None), height=50, halign='left', valign='middle', color=(0, 0, 0, 1))
        date.bind(size=date.setter('text_size'))
        # Search field (on the right side)
        # Add a Filter button to open the popup
        self.end_filter = Button(text="Reset", size_hint_x=0.05, height=50)
        self.end_filter.bind(on_press=self.on_enter)
        filter_button = Button(text="Filter Tasks", size_hint_x=0.2, height=50)
        filter_button.bind(on_press=self.show_filter_popup)
        self.search_input = TextInput(hint_text="Search tasks", size_hint_x=0.5, multiline=False)
        self.search_input.bind(text=self.on_search_text)
        # Add logo, date, and search to the top_section layout
        top_section.add_widget(date)
        top_section.add_widget(filter_button)
        top_section.add_widget(self.search_input)
        self.layout.add_widget(top_section)
        self.task_tabs = TabbedPanel(size_hint_y=0.9, do_default_tab=False)
        self.all_tab = TaskTab('All', self.dbname, self)
        self.pending_tab = TaskTab('Pending', self.dbname, self)
        self.completed_tab = TaskTab('Completed', self.dbname, self)
        self.task_tabs.add_widget(self.all_tab)
        self.task_tabs.add_widget(self.pending_tab)
        self.task_tabs.add_widget(self.completed_tab)
        self.layout.add_widget(self.task_tabs)
        add_button = Button(text="Add task", background_color=(0, 0.5, 1, 1), size_hint=(None, None),size=(100, 50))
        add_button.bind(on_press=self.go_add_screen)  # Function to go back to the previous screen
        self.layout.add_widget(add_button)
        self.add_widget(self.layout)

    #cette fonction s'exécute dès qu'on entre dans l'application
    def on_enter(self):
        # Cette méthode est appelée à chaque fois que cet écran est affiché
        print("Screen entered.")
        self.all_tab.display_tasks()
        self.pending_tab.display_tasks()
        self.completed_tab.display_tasks()

    #cette fonction ouvre une nouvelle fenêtre, elle doit donc être placée dans une classe qui hérite de Screen. Elle sera utilisée dans TaskFrame pour mettre à jour les données et ouvrir TaskDetails
    def open_task_details(self, task, instance):
        # Set task data in the TaskDetailScreen and navigate to it
        task_detail_screen = self.manager.get_screen('task_details')
        task_detail_screen.set_task_data(task)
        self.manager.current = 'task_details'

    #cette fonction récupère la valeur entrée dans le bouton de recherche et appelle des fonctions spéciales d'affichage en fonction de cette valeur
    #la fonction est 'bind' à l'input, ce qui explique le paramètre value
    def on_search_text(self, instance, value):
        # Trigger a task refresh for each tab
        self.search_query = value
        self.all_tab.filter_tasks()
        self.pending_tab.filter_tasks()
        self.completed_tab.filter_tasks()
    
    def show_filter_popup(self, instance):
        # Open the Filter Popup
        popup = FilterPopup(self)
        popup.open()
    
    #cette fonction est appelée plus haut dans apply_filter de Filter popup, elle n'intervient donc qu'en cas de filtres
    #ici, on utilise filter_func pour créer une query de conditions à vérifier par MongoDB qui nous sort les documents à afficher
    #dans la classe TaskTab, on a une fonction spéciale pour afficher ces documents là
    def display_filtered_data(self, selected_date, selected_status, selected_category, selected_priority):
        print("category: " + selected_category)
        self.filtered_documents = gcommands.filter_func(selected_date, selected_status, selected_category, selected_priority, self.dbname)
        # Apply the filter to tasks
        self.all_tab.filter_feature()
        self.pending_tab.filter_feature()
        self.completed_tab.filter_feature()

    def go_add_screen(self, instance):
        self.manager.current = 'add_task'

# Task Detail Screen
class TaskDetailScreen(Screen):
    def __init__(self, dbname, **kwargs):
        super(TaskDetailScreen, self).__init__(**kwargs)

        background = Image(source='task_details.png', allow_stretch=True, keep_ratio=False)
        self.add_widget(background)

        main_layout = GridLayout(cols=2, padding=[20, 20, 20, 20], spacing=10, size_hint=(1, 1))
        main_layout.bind(minimum_height=main_layout.setter('height'))

        self.dbname = dbname
        # Left column (Project Name, Project Description, Status)
        left_layout = GridLayout(cols=1, spacing=20, size_hint_y=None)
        left_layout.bind(minimum_height=left_layout.setter('height'))
        # Project Name
        left_layout.add_widget(Label(text="[b]Project Name[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_name = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        left_layout.add_widget(self.project_name)
        # Project Description
        left_layout.add_widget(Label(text="[b]Project description[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.project_description = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        left_layout.add_widget(self.project_description)
        # Status
        left_layout.add_widget(Label(text="[b]Status[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.status = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        left_layout.add_widget(self.status)

        # Right column (Deadline, Category, Priority)
        right_layout = GridLayout(cols=1, spacing=20, size_hint_y=None)
        right_layout.bind(minimum_height=right_layout.setter('height'))
        # Deadline
        right_layout.add_widget(Label(text="[b]Deadline[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.deadline = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        right_layout.add_widget(self.deadline)
        # Category
        right_layout.add_widget(Label(text="[b]Category[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.category = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        right_layout.add_widget(self.category)
        # Priority
        right_layout.add_widget(Label(text="[b]Priority[/b]", size_hint=(1, None), height=50,color=(0, 0, 0, 1),markup=True))
        self.priority = Label(text="", font_size=32, color=(0, 0, 0, 1), halign='center', valign='middle')
        right_layout.add_widget(self.priority)
        # Add left and right layouts to the main layout
        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)
        # Buttons layout (Edit, Delete, Back)
        buttons_layout = BoxLayout(orientation='horizontal', size_hint=(1, None), height=70, spacing=20)
        # Back Button (Placed on the left side, styled to match the others)
        back_button = Button(text="Back", background_color=(0, 0, 1, 1), size_hint=(0.4, 1))
        back_button.bind(on_press=self.go_back)  # Function to go back to the previous screen
        buttons_layout.add_widget(back_button)
        # Edit Button
        edit_button = Button(text="Edit", background_color=(0, 0, 1, 1), size_hint=(0.4, 1))
        edit_button.bind(on_press=self.edit_task)
        buttons_layout.add_widget(edit_button)
        # Delete Button
        delete_button = Button(text="Delete", background_color=(1, 0, 0, 1), size_hint=(0.4, 1))
        buttons_layout.add_widget(delete_button)
        #size_hint=(1, 1)
        final_layout = BoxLayout(orientation='vertical', spacing=10, size_hint=(1, 1), pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.late_task_message = Label(text="", font_size=32, halign='center', valign='middle', markup=True)
        final_layout.add_widget(main_layout)
        final_layout.add_widget(self.late_task_message)
        final_layout.add_widget(buttons_layout)
#
        self.add_widget(final_layout)
        
    #c'est la fonction qui est utilisée dans open_details=_task pour mettre à jour les informations sur l'écran
    def set_task_data(self, task):
        self.task=task
        self.project_name.text = task['name']
        self.project_description.text = task['description']
        self.deadline.text = task['deadline'].strftime('%Y-%m-%d')
        self.category.text = task['category']
        self.priority.text = task['priority']
        self.status.text = task['status']
        if task['deadline'] < gcommands.datetime.today() and task["status"].lower() != 'completed':
            self.late_task_message.text = "This task is late"
            self.late_task_message.color = (1, 0, 0, 1)  # Red color for error
        else:
            self.late_task_message.text = "You still have some time"
            self.late_task_message.color = (0, 0, 0, 1)

    #il y a sur l'écran un edit_button. Quand on clique dessus, cette fonction récupère l'écran d'édition et utilise sa fonction set_task_data pour mettre à jour les infos là bas afin qu'elles soient écrites et affichées
    def edit_task(self, instance):
        edit_task_screen = self.manager.get_screen('edit_task')
        edit_task_screen.set_task_data({
            'name': self.project_name.text,
            'description': self.project_description.text,
            'deadline': gcommands.datetime.strptime(self.deadline.text, '%Y-%m-%d'), # datetime.strptime(key_value["deadline"], '%Y-%m-%d %H:%M:%S'),
            'category': self.category.text,
            'priority': self.priority.text,
            'status': self.status.text
        })
        self.manager.current = 'edit_task'

    #il y a un bouton delete sur l'écran. Cette fonction permet de supprimer la tâche que l'utilisateur visualisait
    def delete(self, instance):
        task_name = self.project_name.text
        #afficher le pop up. Si la réponse est oui, alors on appelle la fonction de déletion
        self.dbname = gcommands.task_deletion(task_name, self.dbname)
        self.go_back(instance)

    def go_back(self, instance):
        # Navigate back to the task list
        self.manager.current = 'task_list'
