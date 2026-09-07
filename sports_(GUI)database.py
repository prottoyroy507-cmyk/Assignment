import json
import os
import tkinter as tk
from tkinter import messagebox, scrolledtext

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_path(filename):
    return os.path.join(BASE_DIR, filename)


# ===================== PLAYER =====================
class PlayerManager:
    def __init__(self, file_name='player.json'):
        self.file_name = get_path(file_name)
        self.players = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    self.players = json.load(f)
            except:
                self.players = []
        else:
            self.players = []

    def save_data(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.players, f, indent=2)


# ===================== MATCH =====================
class MatchManager:
    def __init__(self, file_name='match.json'):
        self.file_name = get_path(file_name)
        self.matches = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    self.matches = json.load(f)
            except:
                self.matches = []
        else:
            self.matches = []

    def save_data(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.matches, f, indent=2)


# ===================== PERFORMANCE =====================
class PerformanceManager:
    def __init__(self, file_name='performance.json'):
        self.file_name = get_path(file_name)
        self.data = []
        self.load_data()

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, 'r') as f:
                    self.data = json.load(f)
            except:
                self.data = []
        else:
            self.data = []

    def save_data(self):
        with open(self.file_name, 'w') as f:
            json.dump(self.data, f, indent=2)


# ===================== GUI =====================
class SportsGUI:
    def __init__(self):
        self.pm = PlayerManager()
        self.mm = MatchManager()
        self.perf = PerformanceManager()

        self.root = tk.Tk()
        self.root.title("Sports Management System")
        self.root.geometry("1100x650")
        self.root.configure(bg="black")

        self.left_panel()
        self.center_panel()

        self.root.mainloop()

    # ================= LEFT PANEL =================
    def left_panel(self):
        frame = tk.Frame(self.root, bg="black", width=250)
        frame.pack(side="left", fill="y")

        tk.Label(frame, text="MENU", bg="black", fg="red",
                 font=("Impact", 20)).pack(pady=20)

        style = {"bg": "black", "fg": "red",
                 "width": 25, "height": 2, "font": ("Arial", 11)}

        tk.Button(frame, text="Add Player", command=self.add_player, **style).pack(pady=3)
        tk.Button(frame, text="View Players", command=self.view_players, **style).pack(pady=3)
        tk.Button(frame, text="Toggle Player Activity", command=self.toggle_player, **style).pack(pady=3)
        tk.Button(frame, text="Delete Player", command=self.delete_player, **style).pack(pady=3)

        tk.Button(frame, text="Add Match", command=self.add_match, **style).pack(pady=3)
        tk.Button(frame, text="View Matches", command=self.view_matches, **style).pack(pady=3)
        tk.Button(frame, text="Update Match", command=self.update_match, **style).pack(pady=3)
        tk.Button(frame, text="Delete Match", command=self.delete_match, **style).pack(pady=3)

        tk.Button(frame, text="Add Performance", command=self.add_perf, **style).pack(pady=3)
        tk.Button(frame, text="View Performance", command=self.view_perf, **style).pack(pady=3)
        tk.Button(frame, text="Update Performance", command=self.update_perf, **style).pack(pady=3)
        tk.Button(frame, text="Delete Performance", command=self.delete_perf, **style).pack(pady=3)

        tk.Button(frame, text="Exit", command=self.root.destroy, **style).pack(pady=15)

    # ================= CENTER =================
    def center_panel(self):
        frame = tk.Frame(self.root, bg="black")
        frame.pack(side="right", fill="both", expand=True)

        tk.Label(frame, text="OUTPUT", bg="black", fg="red",
                 font=("Impact", 22)).pack(pady=10)

        self.output = scrolledtext.ScrolledText(
            frame, bg="black", fg="red", font=("Courier", 11))
        self.output.pack(fill="both", expand=True, padx=10, pady=10)

    def show(self, text):
        self.output.delete("1.0", tk.END)
        self.output.insert(tk.END, text)

    # ================= PLAYER =================
    def add_player(self):
        win = tk.Toplevel(bg="black")

        fields = {}
        for lbl in ["Name", "Age", "Jersey No", "Position"]:
            tk.Label(win, text=lbl, bg="black", fg="red").pack()
            e = tk.Entry(win, bg="black", fg="red")
            e.pack()
            fields[lbl] = e

        def save():
            self.pm.players.append({
                "player_id": len(self.pm.players) + 1,
                "name": fields["Name"].get(),
                "age": fields["Age"].get(),
                "jersey_no": fields["Jersey No"].get(),
                "position": fields["Position"].get(),
                "available": True
            })
            self.pm.save_data()
            messagebox.showinfo("Done", "Player Added")
            win.destroy()

        tk.Button(win, text="Save", bg="black", fg="red", command=save).pack(pady=10)

    def view_players(self):
        text = ""
        for p in self.pm.players:
            text += str(p) + "\n\n"
        self.show(text or "No players")

    def toggle_player(self):
        win = tk.Toplevel(bg="black")

        tk.Label(win, text="Player ID", bg="black", fg="red").pack()
        e = tk.Entry(win, bg="black", fg="red")
        e.pack()

        def go():
            pid = int(e.get())
            for p in self.pm.players:
                if p["player_id"] == pid:
                    p["available"] = not p["available"]
                    self.pm.save_data()
                    messagebox.showinfo("Done", "Toggled")
                    win.destroy()
                    return
            messagebox.showerror("Error", "Not found")

        tk.Button(win, text="Toggle", bg="black", fg="red", command=go).pack()

    def delete_player(self):
        win = tk.Toplevel(bg="black")

        tk.Label(win, text="Player ID", bg="black", fg="red").pack()
        e = tk.Entry(win, bg="black", fg="red")
        e.pack()

        def go():
            pid = int(e.get())
            self.pm.players = [p for p in self.pm.players if p["player_id"] != pid]
            self.pm.save_data()
            messagebox.showinfo("Done", "Deleted")
            win.destroy()

        tk.Button(win, text="Delete", bg="black", fg="red", command=go).pack()

    # ================= MATCH =================
    def add_match(self):
        win = tk.Toplevel(bg="black")
        fields = {}

        for lbl in ["Opponents", "Date", "Venue"]:
            tk.Label(win, text=lbl, bg="black", fg="red").pack()
            e = tk.Entry(win, bg="black", fg="red")
            e.pack()
            fields[lbl] = e

        def save():
            self.mm.matches.append({
                "match_id": len(self.mm.matches) + 1,
                "opponents": fields["Opponents"].get(),
                "date": fields["Date"].get(),
                "venue": fields["Venue"].get()
            })
            self.mm.save_data()
            messagebox.showinfo("Done", "Match Added")
            win.destroy()

        tk.Button(win, text="Save", bg="black", fg="red", command=save).pack()

    def view_matches(self):
        text = ""
        for m in self.mm.matches:
            text += str(m) + "\n\n"
        self.show(text or "No matches")

    def update_match(self):
        win = tk.Toplevel(bg="black")

        labels = ["Match ID", "Opponents", "Date", "Venue"]
        fields = {}

        for l in labels:
            tk.Label(win, text=l, bg="black", fg="red").pack()
            e = tk.Entry(win, bg="black", fg="red")
            e.pack()
            fields[l] = e

        def go():
            mid = int(fields["Match ID"].get())
            for m in self.mm.matches:
                if m["match_id"] == mid:
                    m["opponents"] = fields["Opponents"].get()
                    m["date"] = fields["Date"].get()
                    m["venue"] = fields["Venue"].get()
                    self.mm.save_data()
                    messagebox.showinfo("Done", "Updated")
                    win.destroy()

        tk.Button(win, text="Update", bg="black", fg="red", command=go).pack()

    def delete_match(self):
        win = tk.Toplevel(bg="black")

        tk.Label(win, text="Match ID", bg="black", fg="red").pack()
        e = tk.Entry(win, bg="black", fg="red")
        e.pack()

        def go():
            mid = int(e.get())
            self.mm.matches = [m for m in self.mm.matches if m["match_id"] != mid]
            self.mm.save_data()
            messagebox.showinfo("Done", "Deleted")
            win.destroy()

        tk.Button(win, text="Delete", bg="black", fg="red", command=go).pack()

    # ================= PERFORMANCE =================
    def add_perf(self):
        win = tk.Toplevel(bg="black")
        labels = ["Player ID", "Match ID", "Goals", "Assists", "Fouls", "Saves"]
        fields = {}

        for l in labels:
            tk.Label(win, text=l, bg="black", fg="red").pack()
            e = tk.Entry(win, bg="black", fg="red")
            e.pack()
            fields[l] = e

        def go():
            self.perf.data.append({
                "player_id": int(fields["Player ID"].get()),
                "match_id": int(fields["Match ID"].get()),
                "goals": int(fields["Goals"].get()),
                "assists": int(fields["Assists"].get()),
                "fouls": int(fields["Fouls"].get()),
                "saves": int(fields["Saves"].get())
            })
            self.perf.save_data()
            messagebox.showinfo("Done", "Added")
            win.destroy()

        tk.Button(win, text="Save", bg="black", fg="red", command=go).pack()

    def view_perf(self):
        text = ""
        for d in self.perf.data:
            text += str(d) + "\n\n"
        self.show(text or "No data")

    def update_perf(self):
        win = tk.Toplevel(bg="black")
        labels = ["Player ID", "Match ID", "Goals", "Assists", "Fouls", "Saves"]
        fields = {}

        for l in labels:
            tk.Label(win, text=l, bg="black", fg="red").pack()
            e = tk.Entry(win, bg="black", fg="red")
            e.pack()
            fields[l] = e

        def go():
            pid = int(fields["Player ID"].get())
            mid = int(fields["Match ID"].get())

            for d in self.perf.data:
                if d["player_id"] == pid and d["match_id"] == mid:
                    d["goals"] = int(fields["Goals"].get())
                    d["assists"] = int(fields["Assists"].get())
                    d["fouls"] = int(fields["Fouls"].get())
                    d["saves"] = int(fields["Saves"].get())
                    self.perf.save_data()
                    messagebox.showinfo("Done", "Updated")
                    win.destroy()

        tk.Button(win, text="Update", bg="black", fg="red", command=go).pack()

    def delete_perf(self):
        win = tk.Toplevel(bg="black")

        tk.Label(win, text="Player ID", bg="black", fg="red").pack()
        p = tk.Entry(win, bg="black", fg="red")
        p.pack()

        tk.Label(win, text="Match ID", bg="black", fg="red").pack()
        m = tk.Entry(win, bg="black", fg="red")
        m.pack()

        def go():
            pid = int(p.get())
            mid = int(m.get())
            self.perf.data = [
                d for d in self.perf.data
                if not (d["player_id"] == pid and d["match_id"] == mid)
            ]
            self.perf.save_data()
            messagebox.showinfo("Done", "Deleted")
            win.destroy()

        tk.Button(win, text="Delete", bg="black", fg="red", command=go).pack()


# RUN
if __name__ == "__main__":
    SportsGUI()