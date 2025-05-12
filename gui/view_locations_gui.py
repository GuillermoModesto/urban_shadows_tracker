import tkinter as tk
from tkinter import ttk
from models.location import Location
from utils.data_manager import load_data

DATA_FILE = "locations.json"

def run_view_locations_gui():
    """
    Runs the GUI for viewing locations. Displays a table with location details including ID, name, description, area, and details.
    """
    # Create a new window for viewing locations
    window = tk.Toplevel()
    window.title("View Locations")

    # Set up the Treeview widget to display location data
    tree = ttk.Treeview(window, columns=("Name", "Description", "Area", "Details"), show='headings')
    
    # Configure the columns for the Treeview
    for col in tree["columns"]:
        tree.heading(col, text=col)  # Set the heading for each column
        tree.column(col, width=100)  # Set the width for each column
        
    tree.pack(expand=True, fill="both")  # Pack the Treeview widget into the window

    # Load the list of locations from the data file and convert to Location objects
    locations = [Location.from_dict(d) for d in load_data(DATA_FILE)]  # Load data and convert to Location objects

    # Insert each location into the Treeview
    for loc in locations:
        tree.insert("", "end", values=(
            loc.name,  # Location name
            loc.description,  # Location description
            loc.area,  # Location area
            loc.details  # Location details (assuming it's a string or a list)
        ))

    # Start the Tkinter event loop
    window.mainloop()
