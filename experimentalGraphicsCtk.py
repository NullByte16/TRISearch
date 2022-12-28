from customtkinter import *
import customtkinter
import Logic
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import threading

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

class GUICtk():
    
    WIDTH = 500
    HEIGHT = 500
    
    def __init__(self, CTk):
         
         # Create instance of Window.            
         self.window = CTk()
         self.window.title("TRISearch")
         self.window.geometry(f"{GUICtk.WIDTH}x{GUICtk.HEIGHT}")
         self.window.resizable(True, True)
         self.window.grid_columnconfigure(0, weight = 1)
         self.window.grid_rowconfigure(0, weight = 1)
         
         
         
         # Create style class to style tkinter widgets - currently the style object is not in use.
         style = ttk.Style()
         style.configure('TEntry', foreground = "red", background = "#2A2D2E")
         
         # Create list of frames and Initialize Frames.
         self.frames = {
             "dashboard": CTkFrame(master = self.window),
             "new_topic": CTkFrame(master = self.window),
             "view_topic": CTkFrame(master = self.window),
         }
         # Feed frame is added after self.frames initalization, because it's master is the dashboard frame, and that must be initialized first.
         self.frames["feed"] = CTkFrame(master = self.frames["dashboard"], fg_color = "#2A2D2E", width = 500)
                  
         self.init_dashboard()
         
         self.init_feed()
         self.init_new_topic()
         self.init_view_topic()
         
         self.frames["dashboard"].tkraise()
         
         # Loop the GUI.
         self.window.mainloop()

    ##########################################################################################
    ######################### Initialization methods for GUI frames. #########################
    ##########################################################################################
    
    # Initialization method for dashboard frame.
    def init_dashboard(self):
        self.frames["dashboard"].grid(row = 0, column = 0, sticky = "nsew")
        feed_label = CTkLabel(master = self.frames["dashboard"], text = "Feed:", text_font = ("Montserrat", 15, "bold"))
        feed_label.place(x = 20, y = 10)
        new_topic_button = CTkButton(master = self.frames["dashboard"], text = "+", text_font = ("Montserrat", 10), command = self.frames["new_topic"].tkraise)
        new_topic_button.place(x = 440, y = 10, width = 55)
    
    # Initialization method for feed frame.
    def init_feed(self):
        self.frames["feed"].place(x = 20, y = 30)
        topic_buttons = []
        
        X = 20
        Y = 50
        
        for index, title in enumerate(Logic.db.list_collection_names()):
            topic_buttons.append([CTkButton(master = self.frames["feed"], text = title, text_font = ("Montserrat", 10, "bold")), 
                                  CTkButton(master = self.frames["feed"], text = "-", text_font = ("Montserrat", 10, "bold"), fg_color = "red",
                                            command = lambda arg = title: self.remove_topic(arg))])
            topic_buttons[index][0].place(x = X, y = 50 + index * Y, width = 100)
            topic_buttons[index][1].place(x = 425, y = 50 + index * Y, width = 45)
            
            
    
    # Initialization method for new_topic frame.
    def init_new_topic(self):
        self.frames["new_topic"].grid(row = 0, column = 0, sticky = "nsew")
        
        source_list = ["YouTube", "Google", "Ynet", "Scientific American", "Jerusalem Post", "Calcalist"] # String list of source names.
        source_checks = {} # Dictionary of source checkboxes.
        source_vars = [] # List of booleanVar variables to check if checkboxes are checked or not.v--> EXPERIMENTAL CODE
        
        # Back button. Returns user to dashboard frame.
        back = CTkButton(master = self.frames["new_topic"], text = "Back", text_font = ("Monserrat", 10), command = self.frames["dashboard"].tkraise)
        back.place(x = 20, y = 10, width = 70)
        
        # Initialize label and entry widgets for the title and keywords of the new topic.
        XLabel = 30
        YLabel = 50
        
        title = CTkLabel(master = self.frames["new_topic"], text = "Title:", text_font = ("Montserrat", 10, "bold"))
        title.place(x = XLabel, y = YLabel)
        
        title_entry = CTkEntry(master = self.frames["new_topic"], placeholder_text = "Title", placeholder_text_color = "grey", text_font = ("Montserrat", 10))
        title_entry.place(x = XLabel, y = YLabel + 30)
        
        keywords = CTkLabel(master = self.frames["new_topic"], text = "Keywords:", text_font = ("Montserrat", 10, "bold"))
        keywords.place(x = XLabel, y = YLabel + 80)
        
        keywords_entry = CTkEntry(master = self.frames["new_topic"], placeholder_text = "Keywords", placeholder_text_color = "grey", text_font = ("Montserrat", 10))
        keywords_entry.place(x = XLabel, y = YLabel + 110)
        
        # Initialization algorithm of checkboxes for the sources, and their locations.
        X = 75
        Y = 230
        index = 0
        
        for source in source_list:
            source_checks[source] = CTkCheckBox(master = self.frames["new_topic"], text = source, text_font = ("Montserrat", 10), variable = BooleanVar())
            source_checks[source].place(x = X + 200 * (index % 2), y = Y)
            if index % 2 == 1:
                Y += 40
            index += 1
        
        # Submit button.
        submit = CTkButton(master = self.frames["new_topic"], text = "Submit", text_font = ("Montserrat", 10), width = 50,
                            command = lambda: self.organize_input(title_entry.get(), keywords_entry.get(), source_checks))
        submit.place(x = 225, y = Y + 50)
        
    # Initialization method for view_topic frame.
    def init_view_topic(self):
        self.frames["view_topic"].grid(row = 0, column = 0, sticky = "nsew")
        view_label = CTkLabel(master = self.frames["view_topic"], text = "View Topic")
        view_label.place(x = 20, y = 10)
    
    ##########################################################################################
    ################################### Main GUI methods. ####################################
    ##########################################################################################
    
    # Submits new topic to database.
    # 1. Calls Logic.add_topic to add new topic to database and retrieve information.
    # 2. Adds button for viewing topic information to feed frame list.
    def add_topic(self, title: str, keywords: list, sources: list):
        params = {'title': title,
                  'keywords': keywords,
                  'sources': sources
                  }
        
        add_thread = threading.Thread(target = Logic.add_topic, kwargs=params)
        add_thread.start() # Run Logic.add_topic in a thread so that user can continue using the GUI while information is retrieved.
        
        self.init_feed()
        self.frames["dashboard"].tkraise()
    
    def remove_topic(self, title: str):
        print(title)
        
        original_len = len(Logic.db.list_collection_names())
        remover = threading.Thread(target = Logic.remove_topic, args = [title])
        remover.start() # Run Logic.remove_topic in a thread so that user can continue to use the GUI while information is deleted.
        
        # While loop working as event handler so dashboard updates the moment record is removed from the database.
        # This is so we can know precisely when during the run of the remover thread we should call self.init_feed().
        while(original_len == len(Logic.db.list_collection_names())):
            continue
        
        self.init_feed()
        
    
    ##########################################################################################
    ################################### Auxiliary methods. ###################################
    ##########################################################################################
    
    # Receives string of keywords entered by the user in the keywords_entry widget in the new_topic frame.
    # Returns the keywords as a list, separating them according to commas in input.
    def format_keywords(self, keywords: str) -> list:
        return keywords.split(',')  
    
    # Receives list of CTkCheckbox instances.
    # Returns the list of the text values of the checkboxes that were checked.
    def checked_sources(self, source_checks: dict[CTkCheckBox]) -> list[str]:
        checked = []
        for checkbox in source_checks:
            if source_checks[checkbox].variable.get():
                print(source_checks[checkbox].text)
                checked.append(source_checks[checkbox].text)
        return checked
        
    # Manages input from the user in new_topic frame. Purely for aesthetical coding purposes, to make the code more readable.
    def organize_input(self, title: str, keywords: str, source_checks: list[CTkCheckBox]):
        self.add_topic(title, self.format_keywords(keywords), self.checked_sources(source_checks))
     
gui = GUICtk(CTk)