from tkinter import *
import tkinter as tk
from customtkinter import CTkCanvas

class RoundedButton(tk.Canvas):
    def __init__(self, master, width, height, cornerradius, padding, color, bg, command):
        tk.Canvas.__init__(self, master, borderwidth=0,
            relief="flat", highlightthickness=0, bg=bg, command = command)
        self.command = command

        if cornerradius > 0.5*width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5*height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2*cornerradius
        def shape():
            self.create_polygon((padding,height-cornerradius-padding,padding,cornerradius+padding,padding+cornerradius,padding,width-padding-cornerradius,padding,width-padding,cornerradius+padding,width-padding,height-cornerradius-padding,width-padding-cornerradius,height-padding,padding+cornerradius,height-padding), fill=color, outline=color)
            self.create_arc((padding,padding,padding+rad,padding + rad), start=90, extent=90, fill=color, outline=color)
            self.create_arc((width-padding-rad,padding,width-padding,padding+rad), start=0, extent=90, fill=color, outline=color)
            self.create_arc((width-padding,height-rad-padding,width-padding-rad,height-padding), start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding,height-padding-rad,padding+rad,height-padding), start=180, extent=90, fill=color, outline=color)


        id = shape()
        (x0,y0,x1,y1)  = self.bbox("all")
        width = (x1-x0)
        height = (y1-y0)
        self.configure(width=width, height=height)
            
            
class DeleteButton(CTkCanvas):
    def __init__(self, master, width, height, radius, color, bg, command = None):
        CTkCanvas.__init__(self, master, borderwidth = 0, relief = "flat", highlightthickness = 0, bg = bg)
        self.command = command
        
        def shape():
            self.create_aa_circle(x_pos = 15, y_pos = 15, radius = 14, fill = "red")
        
        id = shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1 - x0)
        height = (y1 - y0)
        self.configure(width = width, height = height)
