from customtkinter import CTk
import customtkinter
import Logic
import tkinter

# TODO - Line 54, make new_topic_button background colour to be like the blue background colour of buttons on feed_frame.


class GUICtk():



    def __init__(self) -> None:
        self.window = CTk()
        self.window.set_appearance_mode("dark")


        #Gridding
        self.window.geometry("500x500")
        self.window.title("TRISearch")
        self.window.resizable(True, True)
        self.window.grid_columnconfigure(0, weight = 1)
        self.window.grid_rowconfigure(0, weight = 1)
        
        # Create dashboard frame. This is the first frame that the user sees on launch.
        self.dashboard = customtkinter.CTkFrame(master=self.window, height=500, width=500)
        self.dashboard.grid(row = 0, column = 0, sticky = "nsew")

        self.dashboard.set_appearance_mode('dark')

        # Initialize Dashboard frame objects
        self.feed_label = customtkinter.CTkLabel(master=self.dashboard, text="Feed:", text_color="white", bg_color="#2A2D2E", fg_color="#2A2D2E")
        self.feed_frame = customtkinter.CTkFrame(master=self.dashboard, bg_color="#2A2D2E", fg_color="#2A2D2E")
        self.feed_frame.set_appearance_mode('dark')
        self.empty_space = customtkinter.CTkLabel(self.dashboard, text="", bg_color="#2A2D2E",
         fg_color="#2A2D2E", width=210)

        print(str(self.dashboard.bg_color) + "                      " + str(self.dashboard.fg_color))

        # Initialize additional frames that will switch dashboard
        self.topic_frame = customtkinter.CTkFrame(master=self.window)
        self.topic_frame.set_appearance_mode('dark')
        self.new_topic_frame = customtkinter.CTkFrame(master=self.window)
        self.new_topic_frame.set_appearance_mode('dark')

        # Grid GUI objects
        self.feed_label.grid(row=0, column=0, sticky='W', pady=5, padx=10)
        self.feed_frame.grid(row = 1, column = 0, columnspan = 3)
        self.empty_space.grid(row = 0, column = 1, sticky = "W", padx = 35)
        self.new_topic_button = customtkinter.CTkButton(master=self.dashboard, text=" + ", bg_color="#2A2D2E", command= self.init_new_topic_frame,
         width=20)
        self.new_topic_button['background'] = 'blue' # TODO - BUG - MAKE BUTTON BACKGROUND COLOUR ==> BLUE LIKE THE OTHER BUTTONS
        self.new_topic_button.grid(row=0, column=2, sticky="E", pady=10)
        #self.init_feed_frame() --->>> Commented out. Imports all topic feeds through Logic.


        # Store all frames in a frames list for future reference (see fetch_info function above.)
        self.frames = [self.dashboard, self.feed_frame, self.topic_frame]

        self.init_feed_frame()

        self.window.mainloop()



    # ---------------------------------------------------------------------- #
    # ---------------------------------------------------------------------- #
    # ------------------------------METHODS--------------------------------- #
    # ---------------------------------------------------------------------- #
    # ---------------------------------------------------------------------- #


    # Auxialiary recursive function for back_to_dashboard. Erases all elements in a main frame (main frame is a frame who's master is window).
    def erase_frame(self, f: customtkinter.CTkFrame):
        for element in f.winfo_children():
            element.destroy()
        f.grid_forget()
                

    # Receives the current displayed frame, hides the frame, and displays dashboard frame. 
    def back_to_dashboard(self, f: customtkinter.CTkFrame):
        self.erase_frame(f)
        self.dashboard.grid(row = 0, column = 0, sticky = 'NESW')
        
        # BUG - Restore + button (new_topic_button) for dashboard frame when returning to it.
        self.new_topic_button = customtkinter.CTkButton(master=self.dashboard, text=" + ", bg_color="#2A2D2E", command= self.init_new_topic_frame,
         width=20)
        self.new_topic_button.grid(row=0, column=2, sticky="E", pady=10)
        # BUG
        
        self.feed_frame.grid(row=1, column=0, sticky="W", pady=10)
        self.init_feed_frame()

            
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

        self.topic_frame.grid(row = 0, column = 0, sticky = 'NSWE')
        back_button = customtkinter.CTkButton(master=self.topic_frame, text="Back", command= lambda: self.back_to_dashboard(self.topic_frame))
        back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)
        label_frame = customtkinter.CTkFrame(master=self.topic_frame)
        label_frame.grid(row=2, column=0, sticky="W", pady=2, padx=10)
        r = 0
        for name in names:
            l = customtkinter.CTkLabel(master=label_frame, text=name)
            l.grid(row = r, column = 2, sticky = "W", pady=2, padx=10)
            r+=1
            
    # Delete a topic.
    def delete_topic(self, title: str):
        if Logic.delete_topic(title):
            self.init_feed_frame()
        else:
            fail_msg = customtkinter.CTkToplevel(self.window, height = 250, width = 250)
            fail_msg.set_appearance_mode('dark')
            fail_msg.title("Delete Failed")
            fail_lbl = customtkinter.CTkLabel(master = fail_msg, text="Failed to delete resources. Don't even try again, it won't work.")
            fail_lbl.grid(row = 0, column = 0, sticky="NSEW", pady = 10)
        
    
    # Initialize all stored topics on dashboard frame.
    def init_feed_frame(self):
        r = 0
        for title in Logic.db.list_collection_names():
            if len(title) > 20:
                title = title[:20] + "..."
            customtkinter.CTkButton(master=self.feed_frame, text=title, command=lambda arg=title: self.fetch_info(arg)).grid(
                row = r, column = 0, sticky = 'W', pady = 2, padx=10)
            
            # Download "refresh" button image, and replace the text with that.
            # Place the image into a new folder called "Resources" in the project folder of TRISearch.
            # Set "Delete" button color to red.
            customtkinter.CTkButton(master=self.feed_frame, text="-", fg_color="red", width=30, command=lambda arg=title: self.delete_topic(arg)).grid(
                row = r, column = 2, sticky = "E", pady = 10)
            r+=1
        empty_space = customtkinter.CTkLabel(self.feed_frame, text="", bg_color="#2A2D2E",
         fg_color="#2A2D2E", width=210)
        if r > 0:
            empty_space.grid(row = 0, rowspan = r, column = 1, sticky = "W", padx = 35)
        else:
            empty_space.grid(row = 0, column = 1, sticky = "W", padx = 35)

    
    # Auxiliary function for init_new_topic_frame -> submit_button command.
    # Retrievs checked source checkboxes in new_topic_frame. If there are none, returns None and does NOT create database collection, raises TopLevel Window to notify the user.
    # Otherwise, calls Logic.add_topic function to create collection in TRISearch DB.
    def create_new_topic(self, title: str, keywords: list[str], sources: list[customtkinter.CTkCheckBox]):
        checked = []
        for source in sources:
            if source.variable.get() == 1:
                checked.append(source.text)
        
        
        if checked == []:
            print("script attempted to enter the NONE MSG if statement.")
            none_msg = customtkinter.CTkToplevel(self.window)
            none_msg.set_appearance_mode("dark")
            none_msg.geometry("350x150")
            none_msg.title("No Sources Selected")
            customtkinter.CTkLabel(master=none_msg, text="Oops! You didn't select any sources to search.", text_color="white", bg_color="#2A2D2E", fg_color="#2A2D2E").pack(side="top")
            return None
        Logic.add_topic(title, keywords, checked)
        completed_msg = customtkinter.CTkToplevel(self.window)
        completed_msg.set_appearance_mode("dark")
        completed_msg.geometry("250x350")
        completed_msg.title("Topic Added Successfully")
        completed_lbl = customtkinter.CTkLabel(master=completed_msg, text="Topic added successfully!", text_color="white", bg_color="#2A2D2E", fg_color="#2A2D2E")
        completed_lbl.grid()
        self.back_to_dashboard(self.new_topic_frame)


    # Generate New Topic creation page.
    def init_new_topic_frame(self):
    
        sources_lst = ["YouTube", "Google", "Jerusalem Post", "Ynet", "Calcalist", "Scientific American"] # Will be changed to acquire updated source list from SQL database.
        sources_checkboxes = []

        for f in self.frames:
            f.grid_forget()

        self.new_topic_frame.grid(row=0, column=0, sticky="NSEW")
        
        back_button = customtkinter.CTkButton(master=self.new_topic_frame, text="Back", width=40, bg_color="#2A2D2E", command= lambda: self.back_to_dashboard(self.new_topic_frame))
        back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)

        ntf_title = customtkinter.CTkLabel(master=self.new_topic_frame, text="Create New Topic", text_color="white", bg_color="#2A2D2E")
        ntf_title.grid(row=0, column=0, sticky="W", pady=2, padx=200)

        title_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Title:", text_color="white", bg_color="#2A2D2E")
        title_label.grid(row=2, column=0, sticky="W", pady=12, padx=10)

        title_entry = customtkinter.CTkEntry(master=self.new_topic_frame, bg_color="#2A2D2E", placeholder_text="Title")
        title_entry.grid(row=4, column=0, sticky="W", pady=2, padx=10)

        keywords_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Keywords (separate each new search term with a comma):",
         text_color="white", bg_color="#2A2D2E")

        keywords_label.grid(row=6, column=0, sticky="W", pady=12, padx=10)

        keywords_entry = customtkinter.CTkEntry(master=self.new_topic_frame, bg_color="#2A2D2E", placeholder_text="Keywords")
        keywords_entry.grid(row=7, column=0, sticky="W", pady=2, padx=10)

        sources_label = customtkinter.CTkLabel(master=self.new_topic_frame, text="Sources:", text_color="white", bg_color="#2A2D2E")
        sources_label.grid(row=9, column=0, sticky="W", pady=12, padx=10)

        src_row = 10
        x = 170

        for index,source in enumerate(sources_lst): 
            cb = customtkinter.CTkCheckBox(master=self.new_topic_frame, text=source, text_color='white',
             bg_color="#2A2D2E", variable=tkinter.IntVar())
             
            cb.grid(row=src_row, column=0, sticky = 'W', pady=2, padx = (index % 2) * x + 10)
            sources_checkboxes.append(cb)

            if index % 2 == 1:
                src_row += 1
        
        # Change so button calls function that interfaces with Logic for collection creation.
        submit_button = customtkinter.CTkButton(master=self.new_topic_frame, text="Submit", bg_color="#2A2D2E", width=50,
         command = lambda: self.create_new_topic(title_entry.get(), keywords_entry.get().split(','),
          sources_checkboxes)).grid(row = src_row + 1, column = 0, pady = 22)

GCtk= GUICtk()