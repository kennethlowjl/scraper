import pandas as pd
import tkinter as tk
from tkinter import ttk, StringVar

class CarRecommenderChatBotGUI:
    def __init__(self, df):
        self.df = df
        self.user_prefs = {}
        self.root = tk.Tk()
        self.root.title("Car Recommender ChatBot")

        # Creating GUI Elements
        self.create_gui_elements()

    # Function to recommend cars based on user preference
    def recommend_cars(self):
        filtered_cars = self.df
        for column, preference in self.user_prefs.items():
            if column == "brand":
                filtered_cars = filtered_cars[filtered_cars[column].str.lower().str.contains(preference.lower())]
            elif column == "model":
                filtered_cars = filtered_cars[filtered_cars[column].str.lower().str.contains(preference.lower())]
            elif column in ["price", "age"]:
                filtered_cars = filtered_cars[filtered_cars[column] <= preference]
        top_10_cars = filtered_cars.head(10)
        return top_10_cars

    def update_prefs(self):
        user_input = self.entry.get().strip()
        preference_type = self.selected.get()
        if user_input:
            if preference_type in ['price', 'age']:
                self.user_prefs[preference_type] = float(user_input)
            else:
                self.user_prefs[preference_type] = user_input
            # Displaying the user's input in the panel and clear the entry field
            self.panel.insert(tk.END, f"{preference_type.capitalize()}: {user_input}\n")
            self.entry.delete(0, 'end')

    def search(self):
        recommended_cars = self.recommend_cars()

        # Clearing the treeview before inserting new search results
        for row in self.treeview.get_children():
            self.treeview.delete(row)

        # Inserting the search results into the treeview
        for _, row in recommended_cars.iterrows():
            self.treeview.insert('', 'end', values=row.tolist())

    def create_gui_elements(self):
        # Creating dropdown for input selection
        self.selected = StringVar()
        dropdown = ttk.Combobox(self.root, textvariable=self.selected)
        dropdown['values'] = ['brand', 'model', 'price', 'age']
        dropdown.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        dropdown.current(0)

        # Creating entry for input
        self.entry = tk.Entry(self.root)
        self.entry.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        # Creating a button to enter the preference
        tk.Button(self.root, text='Enter', command=self.update_prefs).grid(row=0, column=2, padx=5, pady=5, sticky='w')

        # Creating a button to start the search
        tk.Button(self.root, text='Search', command=self.search).grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        # Creating a treeview for the search results
        self.treeview = ttk.Treeview(self.root, columns=self.df.columns.tolist(), show='headings')
        self.treeview.grid(row=2, column=0, columnspan=3, sticky='nsew', padx=5, pady=5)

        for col in self.df.columns:
            self.treeview.heading(col, text=col)

        # Configuring the row that contains the treeview to expand with the window
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        # Creating a panel to display the user's input
        self.panel = tk.Text(self.root, height=10, width=30)
        self.panel.grid(row=0, column=3, rowspan=3, padx=5, pady=5, sticky='w')

    def run(self):
        self.root.mainloop()

# Load your cleaned data
cars = pd.read_csv('C:/Users/USER/Desktop/scraper/cleaned_cars.csv')

# Convert 'age' and 'owners' to integers
cars['age'] = cars['age'].astype(float).astype(int)
cars['owners'] = cars['owners'].astype(float).astype(int)

bot = CarRecommenderChatBotGUI(cars)
bot.run()











