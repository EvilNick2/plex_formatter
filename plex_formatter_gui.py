import tkinter as tk
from tkinter import simpledialog, messagebox
from imdb import IMDb

# Define dark mode colors
dark_bg_color = "#333333"
light_text_color = "#FFFFFF"
button_bg_color = "#555555"
button_fg_color = "#FFFFFF"
text_bg_color = "#424242"
text_fg_color = "#E0E0E0"

class CustomDialog(tk.Toplevel):
    def __init__(self, parent, title=None, prompt=None, options=None):
        super().__init__(parent)
        self.transient(parent)
        self.title(title)
        self.result = None

        self.configure(bg=dark_bg_color)
        self.prompt = tk.Label(self, text=prompt, bg=dark_bg_color, fg=light_text_color)
        self.prompt.pack(pady=5)

        self.listbox = tk.Listbox(self, bg=text_bg_color, fg=text_fg_color, selectbackground=button_bg_color, selectforeground=light_text_color, height=10, width=50)
        if options:
            for option in options:
                self.listbox.insert(tk.END, option)
        self.listbox.pack(pady=5, padx=5)

        self.listbox.bind('<Double-1>', self.on_ok)

        self.button_ok = tk.Button(self, text="OK", command=self.on_ok, bg=button_bg_color, fg=button_fg_color)
        self.button_ok.pack(pady=5)

        self.bind("<Return>", self.on_ok)

    def on_ok(self, event=None):
        self.result = self.listbox.curselection()
        self.destroy()

def get_movie_details_gui(movie_name):
    ia = IMDb()
    search_results = ia.search_movie(movie_name)
    
    if search_results:
        options = [f"{movie['title']} ({movie.get('year', 'N/A')})" for movie in search_results[:5]]
        dialog = CustomDialog(root, title="Select Movie", prompt="Found movies:\nSelect the correct movie:", options=options)
        root.wait_window(dialog)

        if dialog.result:
            choice = dialog.result[0]
            movie = search_results[choice]
            ia.update(movie)
            
            title = movie['title']
            year = movie['year']
            imdb_id = movie.movieID
            
            formatted_name = f"{title} ({year}) {{imdb-tt{imdb_id}}}"
            return formatted_name
        else:
            messagebox.showerror("Error", "Invalid selection.", parent=root)
            return None
    else:
        messagebox.showerror("Error", "Movie not found.", parent=root)
        return None

def on_search_click():
    movie_name = entry.get()
    if movie_name:
        result = get_movie_details_gui(movie_name)
        if result:
            text_result.delete(1.0, tk.END)
            text_result.insert(tk.END, result)
            with open('movies.txt', 'a') as file:
                file.write(result + '\n')

root = tk.Tk()
root.title("Movie Details Fetcher")
root.configure(bg=dark_bg_color)

label = tk.Label(root, text="Enter Movie Name:", bg=dark_bg_color, fg=light_text_color)
label.pack()

entry = tk.Entry(root, bg=text_bg_color, fg=text_fg_color, insertbackground=light_text_color)
entry.pack()
entry.bind("<Return>", lambda event: on_search_click())

search_button = tk.Button(root, text="Search", command=on_search_click, bg=button_bg_color, fg=button_fg_color)
search_button.pack()

text_result = tk.Text(root, height=5, width=50, bg=text_bg_color, fg=text_fg_color)
text_result.pack()

root.mainloop()