import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext, ttk
import random

class NumberGuessingGame:
    def __init__(self, master):
        """
        Initialize the Number Guessing Game.
        
        :param master: The root window of the application
        """
        self.master = master
        self.master.title("Number Guessing Game")
        self.master.geometry("600x550")
        self.master.resizable(False, False)
        self.master.configure(bg='#f0f0f0')

        # Game state variables
        self.number = ""  # The number to be guessed
        self.digits = 0   # Number of digits in the number
        self.attempts = 0 # Current number of attempts
        self.max_attempts = 0 # Maximum allowed attempts

        self.create_widgets()
        # Start a new game after a short delay to ensure all widgets are created
        self.master.after(100, self.start_new_game)

    def create_widgets(self):
        """Create and arrange all the GUI widgets."""
        main_frame = tk.Frame(self.master, bg='#f0f0f0')
        main_frame.pack(expand=True, fill='both', padx=20, pady=20)

        # Title
        self.title_label = tk.Label(main_frame, text="Number Guessing Game", font=("Arial", 24, "bold"), bg='#f0f0f0', fg='#333333')
        self.title_label.pack(pady=10)

        # Game instructions
        self.instruction_text = scrolledtext.ScrolledText(main_frame, height=6, width=60, wrap=tk.WORD, font=("Arial", 10))
        self.instruction_text.pack(pady=10)
        self.instruction_text.insert(tk.END, "1. Guess a randomly generated number.\n"
                                             "2. The number will have unique digits.\n"
                                             "3. After each guess, you'll get feedback:\n"
                                             "   - 'Full hits': Correct digits in right position.\n"
                                             "   - 'Partial hits': Correct digits in wrong position.\n"
                                             "4. Try to guess the number in as few attempts as possible!")
        self.instruction_text.config(state=tk.DISABLED)

        # Guess input area
        self.guess_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.guess_frame.pack(pady=10)

        self.guess_entry = tk.Entry(self.guess_frame, font=("Arial", 14), justify="center", width=15)
        self.guess_entry.pack(side=tk.LEFT, padx=5)
        self.guess_entry.bind('<Return>', lambda event: self.make_guess())

        self.guess_button = ttk.Button(self.guess_frame, text="Make Guess", command=self.make_guess)
        self.guess_button.pack(side=tk.LEFT, padx=5)

        # Result display
        self.result_label = tk.Label(main_frame, text="", font=("Arial", 12), bg='#f0f0f0', fg='#333333')
        self.result_label.pack(pady=5)

        # Progress tracking
        self.progress_frame = tk.Frame(main_frame, bg='#f0f0f0')
        self.progress_frame.pack(pady=5, fill='x')

        self.progress_label = tk.Label(self.progress_frame, text="Progress: ", font=("Arial", 10), bg='#f0f0f0', fg='#333333')
        self.progress_label.pack(side=tk.LEFT)

        self.progress_bar = ttk.Progressbar(self.progress_frame, length=300, mode='determinate')
        self.progress_bar.pack(side=tk.LEFT, padx=5)

        # Attempt log
        self.log_text = scrolledtext.ScrolledText(main_frame, height=10, width=60, font=("Arial", 10))
        self.log_text.pack(pady=10)
        self.log_text.config(state=tk.DISABLED)

        # New game button
        self.new_game_button = ttk.Button(main_frame, text="New Game", command=self.start_new_game)
        self.new_game_button.pack(pady=5)

    def start_new_game(self):
        """Prompt the user for the number of digits and start a new game."""
        self.digits = simpledialog.askinteger("Number of Digits", "Enter the number of digits to guess (1-10):", 
                                              minvalue=1, maxvalue=10, parent=self.master)
        if not self.digits:
            self.master.quit()
            return

        self.max_attempts = self.digits * 5  # Set max attempts based on number of digits
        self.new_game()

    def new_game(self):
        """Set up a new game with a new number to guess."""
        self.number = self.generate_number()
        self.attempts = 0
        self.result_label.config(text="")
        self.guess_entry.delete(0, tk.END)
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete('1.0', tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.update_progress()
        messagebox.showinfo("New Game", f"A new {self.digits}-digit number has been generated. You have {self.max_attempts} attempts. Good luck!")
        self.guess_entry.focus()

    def generate_number(self):
        """Generate a random number with unique digits."""
        digits = list(range(10))
        random.shuffle(digits)
        return ''.join(map(str, digits[:self.digits]))

    def make_guess(self):
        """Process the player's guess and update the game state."""
        guess = self.guess_entry.get()
        if len(guess) != self.digits:
            messagebox.showerror("Invalid Guess", f"Your guess must be {self.digits} digits long.")
            return

        self.attempts += 1
        full_hits, partial_hits = self.check_guess(guess)

        self.log_attempt(guess, full_hits, partial_hits)
        self.update_progress()

        if full_hits == self.digits:
            messagebox.showinfo("Congratulations!", f"You guessed the number in {self.attempts} attempts.\nThe number was {self.number}.")
            self.start_new_game()
        elif self.attempts >= self.max_attempts:
            messagebox.showinfo("Game Over", f"You've reached the maximum number of attempts.\nThe number was {self.number}.")
            self.start_new_game()
        else:
            self.result_label.config(text=f"Attempt {self.attempts}: Full hits: {full_hits}, Partial hits: {partial_hits}")
        
        self.guess_entry.delete(0, tk.END)
        self.guess_entry.focus()

    def check_guess(self, guess):
        """
        Check the guess against the actual number.
        
        :param guess: The player's guess
        :return: A tuple of (full_hits, partial_hits)
        """
        full_hits = sum(g == n for g, n in zip(guess, self.number))
        partial_hits = sum(min(guess.count(d), self.number.count(d)) for d in set(guess)) - full_hits
        return full_hits, partial_hits

    def log_attempt(self, guess, full_hits, partial_hits):
        """
        Log the current attempt in the attempt history.
        
        :param guess: The player's guess
        :param full_hits: Number of correct digits in correct positions
        :param partial_hits: Number of correct digits in wrong positions
        """
        log_entry = f"Attempt {self.attempts}/{self.max_attempts}: Guess: {guess}, Full hits: {full_hits}, Partial hits: {partial_hits}\n"
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, log_entry)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)

    def update_progress(self):
        """Update the progress bar and label based on the current number of attempts."""
        progress = (self.attempts / self.max_attempts) * 100
        self.progress_bar['value'] = progress
        self.progress_label.config(text=f"Progress: {self.attempts}/{self.max_attempts} attempts")

if __name__ == "__main__":
    root = tk.Tk()
    game = NumberGuessingGame(root)
    root.mainloop()