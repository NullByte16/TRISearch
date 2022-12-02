"""
TO DO:
* CRITICAL - In function strip_name, supposed to accept arguments of type string, but instead gets passed
    two arguments, one of type Research, and the other of type string containing thumbnail image title.

    Need to solve so only image title gets sent to strip_name function, and image title string is stripped from
    incompatible characters.

"""

import Logic
import tkinter as tk
from PyQt5 import Qt5
from tkinter import ttk

"""
class Graphics():

    def __init__(self):
        button1 = tk.Button(self)
        button1.location('TOP') """

# Create window.
window = tk.Tk()
window.geometry("500x500")

# Create dashboard frame. This is the first frame that the user sees on launch.
dashboard = tk.Frame(master=window)
dashboard.grid(row = 0, column = 0, sticky = 'W')
topics = {} # Initialize topics dictionary


# Initialize Dashboard frame objects
feed_label = tk.Label(master=dashboard, text="Feed:")
feed_frame = tk.Frame(master=dashboard)
topic_frame = tk.Frame(master=window)
new_topic_frame = tk.Frame(master=window)


# Receives the current displayed frame, hides the frame, and displays dashboard frame. 
def back_to_dashboard(f: tk.Frame):
    f.grid_forget()

    for element in f.slaves():
        element = None
    dashboard.grid(row = 0, column = 0, sticky = 'W')
    feed_frame.grid(row=1, column=0, sticky="W", pady=4)
    r=0
    for topic in Logic.topics:
        topics[topic.title].grid(row = r, column = 0, sticky = 'W', pady = 2, padx = 10)
        r+=1

        
# "Fetches" info through Logic module, of all infos under the topic that was selected in dashboard, displays topic_frame frame.       
def fetch_info(arg):
    names = Logic.fetch(arg)

    if names == None:
        none_msg = tk.Toplevel(window)
        none_msg.geometry("350x150")
        none_msg.title("No Information Found")
        tk.Label(none_msg, text="Sorry, no information was found for the requested topic...").pack(side="top")
        return None

    for f in frames:
        f.grid_forget()

    topic_frame.grid(row = 0, column = 0, sticky = 'E')
    back_button = tk.Button(master=topic_frame, text="Back", command= lambda: back_to_dashboard(topic_frame))
    back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)
    label_frame = tk.Frame(master=topic_frame)
    label_frame.grid(row=2, column=0, sticky="W", pady=2, padx=10)
    r = 0
    for name in names:
        l = tk.Label(master=label_frame, text=name)
        l.grid(row = r, column = 2, sticky = "W", pady=2, padx=10)
        r+=1

        
# Initialize all stored topics on dashboard frame.
def init_feed_frame():
    global topics
    r = 0
    for topic in Logic.topics:
        topics[topic.title] = tk.Button(master=feed_frame, text=topic.title[:20] + "...", command=lambda arg=topic.title: fetch_info(arg))
        topics[topic.title].grid(row = r, column = 0, sticky = 'W', pady = 2, padx=10)
        r+=1

        

def init_new_topic_frame():
    for f in frames:
        f.grid_forget()

    new_topic_frame.grid(row=0, column=0, sticky="W")
    
    back_button = tk.Button(master=new_topic_frame, text="Back", command= lambda: back_to_dashboard(new_topic_frame))
    back_button.grid(row = 0, column=0, sticky="W", pady=2, padx=10)

    ntf_title = tk.Label(master=new_topic_frame, text="Create New Topic")
    ntf_title.grid(row=0, column=0, sticky="W", pady=2, padx=215)

    # TODO: Create, title, keywords and sources labels and their respective entry boxes.
    title_label = tk.Label(master=new_topic_frame, text="Title:")
    title_label.grid(row=2, column=0, sticky="W", pady=2, padx=10)

    title_entry = tk.Entry(master=new_topic_frame)
    title_entry.grid(row=4, column=0, sticky="W", pady=2, padx=10)
    title_entry.insert(0, "Title")

    keywords_label = tk.Label(master=new_topic_frame, text="Keywords (separate each new search term with a comma):")
    keywords_label.grid(row=6, column=0, sticky="W", pady=2, padx=10)

    keywords_entry = tk.Entry(master=new_topic_frame)
    keywords_entry.grid(row=7, column=0, sticky="W", pady=2, padx=10)

    sources_label = tk.Label(master=new_topic_frame, text="Sources:")
    sources_label.grid(row=9, column=0, sticky="W", pady=2, padx=10)


# Grid GUI objects
feed_label.grid(row=0, column=0, sticky='W', pady=2)
feed_frame.grid(row = 1, column = 0)
new_topic_button = tk.Button(master=dashboard, text=" + ", command= init_new_topic_frame)
new_topic_button.grid(row=0, column=1, sticky="E", pady=2)
init_feed_frame()
topic_frame.grid_forget()


# Store all frames in a frames list for future reference (see fetch_info function above.)
frames = [dashboard, feed_frame, topic_frame]

window.mainloop()