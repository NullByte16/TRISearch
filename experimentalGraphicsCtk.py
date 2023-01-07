from customtkinter import *
import customtkinter
import Logic
from tkinter import *
from tkinter import ttk
from tkinter.ttk import *
import threading
from time import sleep
from StylizedWidgets import *

# Set default GUI style form CustomTkinter. This might change in the future, to allow choice for the user to select a GUI style.
customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("blue")

import tkinter
print(tkinter.TkVersion)

class GUICtk(CTk):
    def __init__(self):
        
         super().__init__()
        
         # Define window settings.
         self.WIDTH = 500
         self.HEIGHT = 500
         self.FG_COLOR = "#2A2D2E"
         
         self.title("TRISearch")            
         self.geometry(f"{self.WIDTH}x{self.HEIGHT}")
         self.resizable(True, True)
         self.grid_columnconfigure(0, weight = 1)
         self.grid_rowconfigure(0, weight = 1)
         self.focusmodel = "passive"
         
         
         # Create style class to style tkinter widgets - currently the style object is not in use.
         style = ttk.Style()
         style.configure('TEntry', foreground = "red", background = self.FG_COLOR)
         
         # Create list of frames and Initialize Frames.
         self.frames = {
             "dashboard": Dashboard(master = self, width = self.WIDTH, height = self.HEIGHT, fg_color = self.FG_COLOR),
             "new_topic": New_Topic(master = self, width = self.WIDTH, height = self.HEIGHT, fg_color = self.FG_COLOR),
             "view_topic": View_Topic(master = self, width = self.WIDTH, height = self.HEIGHT, fg_color = self.FG_COLOR),
         }
         
         self.frames["dashboard"].tkraise()
         self.raised = "dashboard"
         
         # Loop the GUI.
         self.mainloop()
    
    ##########################################################################################
    ################################### Main GUI methods. ####################################
    ##########################################################################################
    
    # Submits new topic to database.
    # 1. Calls Logic.add_topic to add new topic to database and retrieve information.
    # 2. Adds button for viewing topic information to feed frame list.
    def add_topic(self, title: str, keywords: list, sources: list):
        add_thread = threading.Thread(target = lambda: (Logic.add_topic(title, keywords, sources), self.frames["dashboard"].present_refresh()))
        add_thread.start() # Run Logic.add_topic in a thread so that user can continue using the GUI while information is retrieved.
        
        self.frames["dashboard"].tkraise()
    
    def remove_topic(self, title: str):
        
        original_len = len(Logic.db.list_collection_names())
        remover = threading.Thread(target = Logic.remove_topic, args = [title])
        remover.start() # Run Logic.remove_topic in a thread so that user can continue to use the GUI while information is deleted.
        
        # While loop working as event handler so dashboard update_frames the moment record is removed from the database.
        # This is so we can know precisely when during the run of the remover thread we should call self.init_feed().
        while(original_len == len(Logic.db.list_collection_names())):
            continue

        self.frames["dashboard"].destroy()
        self.frames["dashboard"].refresh()
        
    # Raises a frame to the top of the stack based on the frame name given.
    def show(self, name: str):
        self.frames[name].tkraise()
        self.raised = name
    
    # Raises view_topic and presents the specific information required for the selected topic.
    def view(self, title):
        self.frames["view_topic"].show_infos(title = title)
        self.show(name = "view_topic")
        
    # Event handler for managing the refresh of Feed frame when update_button is shown.
    def present_refresh(self, event: Event, update_var: bool):
        if event.x >= 200 and event.x <= 300 and event.y >= 10 and event.y <= 90 and update_var:
            self.frames["dashboard"].refresh()


# Topic frame class. Each instance of Topic is another topic listed in the Feed frame.
class Topic(CTkFrame):
    def __init__(self, **kwargs):
        # Initialize parent container.
        super().__init__(kwargs["master"])
        
        self.master = kwargs["master"]
        
        # Define width and height properties.
        self.WIDTH = kwargs["width"] - 35
        self.HEIGHT = 80
        self.FG_COLOR = "#1A1B1C"
        
        # Initialize this CTkFrame object.
        CTkFrame.__init__(self, master = kwargs["master"], width = self.WIDTH, height = self.HEIGHT, fg_color = self.FG_COLOR, relief = "raised", highlightbackground = "red", highlightcolor = "red")
        self.place(x = kwargs["x"], y = kwargs["y"])
        
        self.init_widgets(kwargs["title"])
        
    # Initializing widgets the Topic widgets.
    def init_widgets(self, title):
        base_button  = CTkButton(master = self, text = None, fg_color = "", width = self.WIDTH - 4, height = self.HEIGHT - 8, hover_color = "", relief = "flat", border_color = self.FG_COLOR,
                                 command = lambda: self.winfo_toplevel().view(self.title.text))
        base_button.place(x = 2, y = 2)
        #base_button = RoundedButton(master = self, color = self.FG_COLOR, bg = self.FG_COLOR, width = self.WIDTH + 115,
        #                            height = self.HEIGHT + 10, cornerradius = 10, padding = 0, command = lambda: self.winfo_toplevel().show("view_frame"))
        #base_button.place(x = 0, y = 10)
        
        self.title = CTkLabel(self, text = title, text_font = ("Montserrat", 10, ("bold", "underline")), width = 30)
        self.title.place(x = 20, y = 5)
        
        view_image = PhotoImage(file = r"C:/Users/Ezra/VSCode/TRISearch/Resources/view_image.png")
        self.view_button = CTkButton(master = self, text = "", image = view_image, bg_color = self.FG_COLOR, width = 0, hover_color = self.FG_COLOR)
        self.view_button.place(x = self.WIDTH - 200, y = 50)
        
        
        delete_image = PhotoImage(file = r"C:/Users/Ezra/VSCode/TRISearch/Resources/delete_button_image.png")
        self.delete = CTkButton(master = self, text = "", image = delete_image, fg_color = "#1A1B1C", bg_color = "#1A1B1C", width = 0, hover_color = self.FG_COLOR,
                                command = lambda: self.winfo_toplevel().remove_topic(self.title.text))
        self.delete.place(x = self.WIDTH - 35, y = 5)
        
        
# Feed frame class. Contains all instances of Topic frames. Responsible for controlling listing of topics in the Dashboard frame.
class Feed(CTkFrame):
    def __init__(self, **kwargs):
        # Initialize parent container.
        super().__init__(kwargs["master"])
        
        self.master = kwargs["master"]
        
        # Define width and height properties.
        self.WIDTH = kwargs["width"]
        self.HEIGHT = kwargs["height"]
        
        # Initialize this CTkFrame object.
        CTkFrame.__init__(self, kwargs["master"], width = self.WIDTH, height = self.HEIGHT, fg_color = kwargs["fg_color"])
        self.place(x = 20, y = 60)
        
        # Dictionary for storing all the Topic frame objects.
        self.topics = {}
        
        # Initialize Topic frame objects.
        self.init_widgets()
        
    # Initialize a Topic frame object for every collection in the database.    
    def init_widgets(self):
        # Constants for defining x and y coordinates of Topic frames.
        X = 0
        Y = 100
        
        # Create a Topic frame object for every collection in the database.
        for index, title in enumerate(Logic.db.list_collection_names()):
            self.topics[title] = Topic(master = self, x = X, y = index * Y, width  = self.WIDTH, title = title)
    
    # Empties topics dictionary and reinitializes the topics in the frame. Used to renew topic list in the dashboard when adding or deleting topics.
    def refresh(self):
        if not self.master.update_var:
            self.destroy()
            self.init_widgets()
        if self.master.update_var:
            print("Post - Update Destruction")
            reverse_thread = threading.Thread(target = lambda: (self.master.reverse_update_button(), self.destroy(), self.init_widgets()))
            reverse_thread.start()
    
    # Destroy the Topic object that has the given title.
    def destroy(self):
        for topic in self.topics.keys():
            self.topics[topic].destroy()
            

# Dashboard frame class. Manages the dashboard. Contains the Feed. Maintains all operations that occur in the dashboard.        
class Dashboard(CTkFrame):
    def __init__(self, **kwargs):
        # Initialize parent container.
        super().__init__(kwargs["master"])
        
        self.master = kwargs["master"]

        # Define width and height properties.
        self.WIDTH = kwargs["width"]
        self.HEIGHT = kwargs["height"]
        
        # Initialize this CTkFrame object.
        CTkFrame.__init__(self, master = kwargs["master"], fg_color = kwargs["fg_color"], takefocus = True)
        self.grid(row = 0, column = 0, sticky = "nsew")
        
        # Initialize Topic frame objects.
        self.init_widgets(kwargs["fg_color"])
    
    # Initialize the widgets in the dashboard: "Feed" label, button for adding a new topic, and the Feed frame object.        
    def init_widgets(self, fg_color):        
        feed_label = CTkLabel(master = self, text = "Feed:", text_font = ("Montserrat", 15, "bold"))
        feed_label.place(x = 20, y = 10)
        
        new_topic_button = CTkButton(master = self, text = "+", text_font = ("Montserrat", 10),
                                     command = lambda: self.winfo_toplevel().show(name = "new_topic"))
        new_topic_button.place(x = 440, y = 10, width = 55)
        
        # Initialize Feed frame object. Called with self so it can be accessed by other methods of Dashboard.
        self.feed = Feed(master = self, fg_color = fg_color, width = self.WIDTH, height = self.HEIGHT, manager = self.master)
        
        update_image = PhotoImage(file = r"C:/Users/Ezra/VSCode/TRISearch/Resources/update_unsized.png")
        # Initialize the update_button button widget.
        self.update_button = CTkButton(master = self, text = "Update", text_color = "black", width = 0, height = 40, fg_color = "white", bg_color = None,
                                       image = update_image, command = self.feed.refresh)
        self.update_var = False
    
    # This method simply calls the Feed.refresh() method.
    # This method is called by GUIManager class when adding or deleting topics. It is not called directly by GUIManager for encapsulation purposes.
    def refresh(self):
        self.feed.refresh()
        
    # This method simply calls the Feed.destroy() method.
    # This method is called by GUIManager class when deleting topics. It is not called directly by GUIManager for encapsulation purposes.       
    def destroy(self):
        self.feed.destroy()
    
    def present_refresh(self):
        self.update_button.place(x = 200, y = -40)
        self.update_button.configure(width = 100)
        
        #while self.update_button.cget("height") <= 40:
        #    self.update_button.configure(height = self.update_button.cget("height") + 1)
        #    self.winfo_toplevel().after(0)
        
        self.update_button.configure(fg_color = "white")
        
        y2 = -40
        while y2 < 15:
            self.update_button.place(x = 200, y = y2 + 1)
            self.winfo_toplevel().after(0)
            y2 += 1

        while y2 > 10:
            y2 -= 1
            self.update_button.place(x = 200, y = y2)
            self.winfo_toplevel().after(0)

        self.update_var = True
        
    def reverse_update_button(self):
        
        self.update_var = False
        y2 = 10
        while y2 < 15:
            y2 += 1
            self.update_button.place(x = 200, y = y2)
            self.winfo_toplevel().after(1)
        
        while y2 > -40:
            y2 -= 1
            self.update_button.place(x = 200, y = y2)
            self.winfo_toplevel().after(0)
        
        self.update_button.configure(width = 0)
        self.update_button.place_forget()

# New Topic frame class. Manages the new_topic frame, and collecting input for creating new topics.        
class New_Topic(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        
        self.master = kwargs["master"]
        
        # Define width and height properties.
        self.WIDTH = kwargs["width"]
        self.HEIGHT = kwargs["height"]
        
        # Define properties specific to this frame.
        self.sources = ["YouTube", "Google", "Ynet", "Scientific American", "Jerusalem Post", "Calcalist"] # List of available sources to choose from.
        self.boolVars = [] # List of boolean variables to manage wether a checkbox is checked.
        
        # Initialize boolean variable list with BooleanVar objects.
        for i in range(0, len(self.sources)):
            self.boolVars.append(BooleanVar())
        
        # Initialize this CTkFrame object.
        CTkFrame.__init__(self, master = kwargs["master"], fg_color = kwargs["fg_color"])
        self.grid(row = 0, column = 0, sticky = "nsew")
        
        # Initialize New Topic frame widgets.
        self.init_widgets()
        
    def init_widgets(self):
        
        source_checks = {} # Dictionary of source checkboxes.
        source_vars = [] # List of booleanVar variables to check if checkboxes are checked or not.v--> EXPERIMENTAL CODE
        
        # Back button. Returns user to dashboard frame.
        back = CTkButton(master = self, text = "Back", text_font = ("Monserrat", 10), command = lambda: self.winfo_toplevel().show(name = "dashboard"))
        back.place(x = 20, y = 10, width = 70)
        
        # Initialize label and entry widgets for the title and keywords of the new topic.
        XLabel = 30
        YLabel = 50
        
        title = CTkLabel(master = self, text = "Title:", text_font = ("Montserrat", 10, "bold"))
        title.place(x = XLabel, y = YLabel)
        
        title_entry = CTkEntry(master = self, placeholder_text = "Title", placeholder_text_color = "grey", text_font = ("Montserrat", 10))
        title_entry.place(x = XLabel, y = YLabel + 30)
        
        keywords = CTkLabel(master = self, text = "Keywords:", text_font = ("Montserrat", 10, "bold"))
        keywords.place(x = XLabel, y = YLabel + 80)
        
        keywords_entry = CTkEntry(master = self, placeholder_text = "Keywords", placeholder_text_color = "grey", text_font = ("Montserrat", 10))
        keywords_entry.place(x = XLabel, y = YLabel + 110)
        
        # Initialization algorithm of checkboxes for the sources, and their locations.
        X = 75
        Y = 230
        index = 0
        
        for source in self.sources:
            source_checks[source] = CTkCheckBox(master = self, text = source, text_font = ("Montserrat", 10), variable = self.boolVars[index])
            source_checks[source].place(x = X + 200 * (index % 2), y = Y)
            if index % 2 == 1:
                Y += 40
            index += 1
        
        # Submit button.
        submit = CTkButton(master = self, text = "Submit", text_font = ("Montserrat", 10), width = 50,
                            command = lambda: self.master.add_topic(title_entry.get(), keywords_entry.get().split(','), self.checked()))
        submit.place(x = 225, y = Y + 50)
        
    # Returns number names of sources that user checked. Called by submit button when user creates a new topic.
    def checked(self):
        checked = []
        for index, var in enumerate(self.boolVars):
            if var:
                checked.append(self.sources[index])
        return checked
    
# View Topic frame class. Manages the viewing of topics and their information.
class View_Topic(CTkFrame):
    def __init__(self, **kwargs):
        super().__init__(kwargs["master"])
        
        self.master = kwargs["master"]
        
        # Define width and height properties.
        self.WIDTH = kwargs["width"]
        self.HEIGHT = kwargs["height"]
        
        # Initialize this CTkFrame object.
        CTkFrame.__init__(self, master = kwargs["master"], fg_color = kwargs["fg_color"])
        self.grid(row = 0, column = 0, sticky = "nsew")
        
        # Initialize View_Topic frame widgets.
        self.init_widgets()
    
    # Initialize the widgets in this frame.
    def init_widgets(self):
        view_label = CTkLabel(master = self, text = "View Topic")
        view_label.place(x = 200, y = 10)
        
        back_button = CTkButton(master = self, text = "Back", command = lambda: self.winfo_toplevel().show("dashboard"))
        back_button.place(x = 20, y = 10)
    
    # Recevies the title of the topic to be showm. Presents all stored information items on the GUI.
    # Calls Logic.pass_infos(), which extracts all infromation items from database.
    def show_infos(self, title):
        info_cursor = Logic.pass_infos(title = title)
        info_buttons = {}
        
        X = 20
        Y = 100
        for index, info in enumerate(info_cursor):
            info_buttons[info["Name"]] = CTkButton(master = self, text = info["Name"], text_font = ("Montserrat", 10, "bold"), fg_color = "#1A1B1C", bg_color = None, hover_color = None,
                                                   width = 460, height = 80).place(x = X, y = index * Y + Y)
            image_button = CTkButton(master = self, text = "", fg_color = "#1A1B1C", bg_color = "#1A1B1C", width = 40, height = 80, hover_color = None,
                                     image = PhotoImage(file = info["Thumbnail"])).place(x = X + 5, y = index * Y + Y)
        
gui = GUICtk()