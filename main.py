import tkinter as tk
from tkinter import messagebox
import random
import string

class PasswordGeneratorApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Password Generator")
        self.geometry("400x380")
        self.light_bg = "#f0f0f0"
        self.light_fg = "black"
        self.dark_bg = "#333333"
        self.dark_fg = "white"
        self.configure(bg=self.light_bg)
        self.dark_mode = tk.BooleanVar(value=False)
        
        tk.Label(self, text="Password Length:", font=("Helvetica", 12), bg=self.light_bg, fg=self.light_fg).pack(pady=(10,5))
        self.length_scale = tk.Scale(self, from_=1, to=64, orient=tk.HORIZONTAL, length=250, bg=self.light_bg, fg=self.light_fg, highlightbackground=self.light_bg)
        self.length_scale.set(12)
        self.length_scale.pack(pady=5)

        self.include_letters = tk.BooleanVar(value=True)
        self.include_numbers = tk.BooleanVar(value=True)
        self.include_special = tk.BooleanVar(value=True)
        self.include_punctuation = tk.BooleanVar(value=True)
        
        options_frame = tk.Frame(self, bg=self.light_bg)
        options_frame.pack(pady=5)
        
        self.letters_cb = tk.Checkbutton(options_frame, text="Letters", variable=self.include_letters, bg=self.light_bg, fg=self.light_fg, font=("Helvetica", 10), selectcolor=self.light_bg)
        self.letters_cb.grid(row=0, column=0, padx=5, pady=2)
        
        self.numbers_cb = tk.Checkbutton(options_frame, text="Numbers", variable=self.include_numbers, bg=self.light_bg, fg=self.light_fg, font=("Helvetica", 10), selectcolor=self.light_bg)
        self.numbers_cb.grid(row=0, column=1, padx=5, pady=2)
        
        self.special_cb = tk.Checkbutton(options_frame, text="Special", variable=self.include_special, bg=self.light_bg, fg=self.light_fg, font=("Helvetica", 10), selectcolor=self.light_bg)
        self.special_cb.grid(row=1, column=0, padx=5, pady=2)
        
        self.punct_cb = tk.Checkbutton(options_frame, text="Punctuation", variable=self.include_punctuation, bg=self.light_bg, fg=self.light_fg, font=("Helvetica", 10), selectcolor=self.light_bg)
        self.punct_cb.grid(row=1, column=1, padx=5, pady=2)
        
        # Dark Mode Toggle
        self.dark_mode_cb = tk.Checkbutton(self, text="Dark Mode", variable=self.dark_mode, command=self.toggle_dark_mode, bg=self.light_bg,fg=self.light_fg, font=("Helvetica", 10), selectcolor=self.light_bg)
        self.dark_mode_cb.pack(pady=5)
        
        # Generate Button
        self.generate_button = tk.Button(self, text="Generate Password", command=self.generate_password, font=("Helvetica", 12), bg=self.light_bg, fg=self.light_fg)
        self.generate_button.pack(pady=10)

        # Password Display
        tk.Label(self, text="Generated Password:", font=("Helvetica", 12), bg=self.light_bg, fg=self.light_fg).pack(pady=(10,2))
        self.password_display = tk.Entry(self, width=40, font=("Helvetica", 12), bg="white", fg="black")
        self.password_display.pack(pady=5)
        self.password_display.bind("<Button-1>", self.select_all)

        self.copy_button = tk.Button(self, text="Copy to Clipboard", command=self.copy_to_clipboard, font=("Helvetica", 10), bg=self.light_bg, fg=self.light_fg)
        self.copy_button.pack(pady=5)
        
        self.notification_label = None

        self.credits_label = tk.Label(self, text="Made by ObsessedGamer77", font=("Helvetica", 8), bg=self.light_bg, fg="gray")
        self.credits_label.pack(side=tk.BOTTOM, pady=5)
        
    def toggle_dark_mode(self):
        """Toggle between light and dark mode and update widget colors."""
        if self.dark_mode.get():
            bg_color = self.dark_bg
            fg_color = self.dark_fg
            entry_bg = "#555555"
            entry_fg = "white"
            cb_selectcolor = "#555555"
        else:
            bg_color = self.light_bg
            fg_color = self.light_fg
            entry_bg = "white"
            entry_fg = "black"
            cb_selectcolor = self.light_bg
        
        self.configure(bg=bg_color)
        # Update all direct children
        for widget in self.winfo_children():
            cls = widget.__class__.__name__
            if cls in ["Label", "Button", "Checkbutton"]:
                widget.configure(bg=bg_color, fg=fg_color)
                if cls == "Checkbutton":
                    widget.configure(selectcolor=cb_selectcolor)
            elif cls == "Scale":
                widget.configure(bg=bg_color, fg=fg_color, highlightbackground=bg_color)
            elif cls == "Frame":
                widget.configure(bg=bg_color)
                for child in widget.winfo_children():
                    if child.__class__.__name__ in ["Label", "Checkbutton"]:
                        child.configure(bg=bg_color, fg=fg_color)
                        if child.__class__.__name__ == "Checkbutton":
                            child.configure(selectcolor=cb_selectcolor)
        self.password_display.configure(bg=entry_bg, fg=entry_fg)
        if self.notification_label:
            self.notification_label.configure(bg=bg_color, fg="green")
        
    def select_all(self, event):
        """Select all text when the password entry is clicked."""
        event.widget.select_range(0, tk.END)
        event.widget.icursor(tk.END)
        return 'break'
        
    def copy_to_clipboard(self):
        """Copy the generated password to the clipboard and show a temporary overlay notification."""
        password = self.password_display.get()
        self.clipboard_clear()
        self.clipboard_append(password)
        
        if self.notification_label is not None:
            self.notification_label.destroy()
        
        self.notification_label = tk.Label(self, text="Password copied to clipboard!", font=("Helvetica", 10), bg=self.light_bg, fg="green")
        self.notification_label.place(relx=0.5, rely=0.9, anchor="center")
        
        self.after(2000, self.remove_notification)
    
    def remove_notification(self):
        """Remove the temporary notification label."""
        if self.notification_label is not None:
            self.notification_label.destroy()
            self.notification_label = None
    
    def generate_password(self):
        length = self.length_scale.get()
        if length > 32:
            if not messagebox.askyesno("Warning", "Many websites do not support passwords longer than 32 characters. Continue?"):
                return
        
        characters = ""
        if self.include_letters.get():
            characters += string.ascii_letters
        if self.include_numbers.get():
            characters += string.digits
        if self.include_special.get():
            characters += "!@#$%^&*()"
        if self.include_punctuation.get():
            characters += ".,;:<>?/"
        
        if not characters:
            messagebox.showerror("Error", "No character types selected!")
            return

        password = ''.join(random.choice(characters) for _ in range(length))
        self.password_display.delete(0, tk.END)
        self.password_display.insert(0, password)

if __name__ == "__main__":
    app = PasswordGeneratorApp()
    app.mainloop()
