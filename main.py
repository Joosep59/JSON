import json
import tkinter as tk
from tkinter import filedialog, messagebox
from person_data import PersonData

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Eesti Isikud")
        self.create_widgets()

    def create_widgets(self):
        self.load_button = tk.Button(self.root, text="Vali JSON Fail", command=self.load_file)
        self.load_button.pack(pady=20)
        self.results_text = tk.Text(self.root, wrap=tk.WORD, width=80, height=20)
        self.results_text.pack(pady=20)

    def load_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            self.person_data = PersonData(data)
            self.show_results()
        else:
            messagebox.showwarning("Hoiatus", "Faili ei valitud.")

    def show_results(self):
        results = [
            "Isikute arv kokku: {}".format(self.person_data.total_people()),
            "Kõige pikem nimi ja tähemärkide arv: {} {} (sündinud {})".format(
                *self.person_data.longest_name()
            ),
            "Kõige vanem elav inimene: {} {} (sündinud {})".format(
                *self.person_data.oldest_living_person()
            ),
            "Kõige vanem surnud inimene: {} {} (sündinud {}, surnud {})".format(
                *self.person_data.oldest_deceased_person()
            ),
            "Näitlejate koguarv: {}".format(self.person_data.total_actors()),
            "Sündinud 1997 aastal: {}".format(self.person_data.born_in_year(1997)),
            "Erinevate elukutsete arv: {}".format(self.person_data.unique_occupations()),
            "Nimi sisaldab rohkem kui kaks nime: {}".format(self.person_data.names_with_more_than_two_parts()),
            "Sünniaeg ja surmaaeg on sama v.a. aasta: {}".format(self.person_data.birth_death_same_except_year()),
            "Elavaid isikuid: {}, Surnud isikuid: {}".format(*self.person_data.living_and_deceased_count())
        ]
        self.results_text.delete(1.0, tk.END)
        self.results_text.insert(tk.END, "\n".join(results))

    def run(self):
        self.root.mainloop()


if __name__ == "__main__":
    gui = GUI()
    gui.run()
