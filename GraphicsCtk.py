from customtkinter import CTk
import customtkinter
import Logic
import tkinter

class GUICtk():



    def __init__(self) -> None:
        self.window = CTk()
        self.window.set_appearance_mode("dark")


        #Gridding
        self.window.geometry("500x500")
        self.window.title("TRISearch")
        self.window.resizable(True, True)
        
        # Create dashboard frame. This is the first frame that the user sees on launch.
        self.dashboard = customtkinter.CTkFrame(master=self.window)
        self.dashboard.grid()
        
        self.dashboard.set_appearance_mode('dark')
        self.topics = {} # Initialize topics dictionary

        # Initialize Dashboard frame objects
        self.feed_label = customtkinter.CTkLabel(master=self.dashboard, text="Feed:")
        self.feed_frame = customtkinter.CTkFrame(master=self.dashboard)
        self.feed_frame.set_appearance_mode('dark')
        self.topic_frame = customtkinter.CTkFrame(master=self.window)
        self.topic_frame.set_appearance_mode('dark')
        self.new_topic_frame = customtkinter.CTkFrame(master=self.window)
        self.new_topic_frame.set_appearance_mode('dark')

        # Grid GUI objects
        self.feed_label.grid(row=0, column=0, sticky='W', pady=2)
        self.feed_frame.grid(row = 1, column = 0)
        self.new_topic_button = customtkinter.CTkButton(master=self.dashboard, text=" + ", command= self.init_new_topic_frame)
        self.new_topic_button.grid(row=0, column=1, sticky="E", pady=2)
        #self.init_feed_frame() --->>> Commented out. Imports all topic feeds through Logic.


        # Store all frames in a frames list for future reference (see fetch_info function above.)
        self.frames = [self.dashboard, self.feed_frame, self.topic_frame]

        self.init_feed_frame()

        self.window.mainloop()



    # ---------------------------------------------------------------------- #
    # ---------------------------------------------------------------------- #
    # -------------------------IMPORTED CODE-------------------------------- #
    # ---------------------------------------------------------------------- #
    # ---------------------------------------------------------------------- #




    # Receives the current displayed frame, hides the frame, and displays dashboard frame. 
    def back_to_dashboard(self, f: customtkinter.CTkFrame):
        f.grid_forget()

        for element in f.slaves():
            element = None
        self.dashboard.grid(row = 0, column = 0, sticky = 'W')
        self.feed_frame.grid(row=1, column=0, sticky="W", pady=4)
        r=0
        for topic in Logic.topics:
            self.topics[topic.title].grid(row = r, column = 0, sticky = 'W', pady = 2, padx = 10)
            r+=1

            
    # "Fetches" info through Logic module, of all infos under the topic that was selected in dashboard, displays topic_frame frame.       
    def fetch_info(self, arg):
        names = Logic.fetch(arg)

        if names == None:
            none_msg = customtkinter.CTkToplevel(self.window)
            none_msg.set_appearance_mode('dark')
            none_msg.geometry("350x150")
            none_msg.title("No Information Found")
            customtkinter.CTkLabel(none_msg, text="Sorry, no information was found for the requested topic...").pack(side="top")
            return None

        for f in self.frames:
            f.grid_forget()

        self.topic_frame.grid(row = 0, column = 0, sticky = 'E')
        back_button = customtkinter.CTkButton(master=self.topic_frame, text="Back", command= lambda: self.back_to_dashboard(self.topic_frame))
        back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)
        label_frame = customtkinter.CTkFrame(master=self.topic_frame)
        label_frame.grid(row=2, column=0, sticky="W", pady=2, padx=10)
        r = 0
        for name in names:
            l = customtkinter.CTkLabel(master=label_frame, text=name)
            l.grid(row = r, column = 2, sticky = "W", pady=2, padx=10)
            r+=1

            
    # Initialize all stored topics on dashboard frame.
    def init_feed_frame(self):
        r = 0
        for topic in Logic.topics:
            self.topics[topic.title] = customtkinter.CTkButton(master=self.feed_frame, text=topic.title[:20] + "...", command=lambda arg=topic.title: self.fetch_info(arg))
            self.topics[topic.title].grid(row = r, column = 0, sticky = 'W', pady = 2, padx=10)
            r+=1

            
    # Generate New Topic creation page.
    def init_new_topic_frame(self):
    
        for f in self.frames:
            f.grid_forget()

        self.new_topic_frame.grid(row=0, column=0, sticky="W")
        
        back_button = customtkinter.CTkButton(master=self.new_topic_frame, text="Back", command= lambda: self.back_to_dashboard(self.new_topic_frame))
        back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)

        ntf_title = customtkinter.CTkLabel(master=self.new_topic_frame, text="Create New Topic")
        ntf_title.grid(row=0, column=0, sticky="W", pady=2, padx=215)

        # TODO: Create, title, keywords and sources labels and their respective entry boxes.
        title_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Title:")
        title_label.grid(row=2, column=0, sticky="W", pady=2, padx=10)

        title_entry = customtkinter.CTkEntry(master=self.new_topic_frame)
        title_entry.grid(row=4, column=0, sticky="W", pady=2, padx=10)
        title_entry.insert(0, "Title")

        keywords_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Keywords (separate each new search term with a comma):")
        keywords_label.grid(row=6, column=0, sticky="W", pady=2, padx=10)

        keywords_entry = customtkinter.CTkEntry(master=self.new_topic_frame)
        keywords_entry.grid(row=7, column=0, sticky="W", pady=2, padx=10)

        sources_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Sources:")
        sources_label.grid(row=9, column=0, sticky="W", pady=2, padx=10)


GCtk= GUICtk()