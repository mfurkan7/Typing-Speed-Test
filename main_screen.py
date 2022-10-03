import random
from tkinter import *
from tkinter import messagebox
from english_words import english_words_lower_set


class MainScreen:

    def __init__(self):
        self.window = Tk()
        self.window.title("Typing Speed Test")
        self.window.geometry("700x500")
        self.window.grid_rowconfigure(1, weight=3)
        self.window.grid_rowconfigure(2, weight=1)
        self.window.grid_columnconfigure(1, weight=9)
        self.window.grid_columnconfigure(3, weight=9)
        self.window.grid_columnconfigure(5, weight=9)
        self.window.resizable(False, False)

        self.maximum_time_in_second = 60
        self.text_start_index = 0
        self.text_end_index = 9
        self.chosen_words = []
        self.word_label_list = []
        self.cpm_score_count = 0
        self.wpm_score_count = 0
        with open("score_log_file.txt", mode="r") as score_log_file_read:
            x = score_log_file_read.read()
            self.best_score_from_log = int(x)

        self.get_word()
        self.text_entry()

        self.window.mainloop()

    def get_word(self):
        for _ in range(200):
            word_index = random.randint(0, len(english_words_lower_set))
            self.chosen_words.append(list(english_words_lower_set)[word_index])

    def text_entry(self):
        self.score_board()
        self.text_display()
        self.user_input = StringVar()
        self.user_input.set("Please start to type after you click the start button")
        self.text_input = Entry(textvariable=self.user_input, bg="azure", font=('Helvetica', 12), justify="center")
        self.text_input.grid(row=2, column=0, columnspan=6, rowspan=2, sticky="nsew")
        self.text_input.bind("<Button-1>", self.clean_entry_box)
        self.text_input.bind("<space>", self.send_input)

    def score_board(self):
        best_score_label = Label(text="Your Best Score:", padx=6, pady=5, font=('Helvetica', 12, 'bold'),
                                 foreground="#42032C")
        best_score_label.grid(row=0, column=0)

        self.best_score = Label(text=self.best_score_from_log, padx=36, pady=5,
                                font=('Helvetica', 12, 'bold'), foreground="#D36B00")
        self.best_score.grid(row=0, column=1)

        character_per_minute = Label(text="CPM(Chracter Per Minute):", padx=6, pady=5,
                                     font=('Helvetica', 12, 'bold'), foreground="#42032C")
        character_per_minute.grid(row=0, column=2)

        self.character_per_minute_score = Label(text=self.cpm_score_count, padx=36,
                                                pady=5, font=('Helvetica', 12, 'bold'), foreground="#D36B00")
        self.character_per_minute_score.grid(row=0, column=3)

        word_per_minute = Label(text="WPM(Word Per Minute):", padx=6, pady=5,
                                font=('Helvetica', 12, 'bold'), foreground="#42032C")
        word_per_minute.grid(row=0, column=4)

        self.word_per_minute_score = Label(text=self.wpm_score_count, padx=36, pady=5, font=('Helvetica', 12, 'bold'),
                                           foreground="#D36B00")
        self.word_per_minute_score.grid(row=0, column=5)

    def text_display(self):
        text_frame = Frame(self.window)
        text_frame.grid(row=1, column=0, columnspan=6, rowspan=3, sticky="nsew")

        self.timer = Label(text=f"Time\n{self.maximum_time_in_second}", font=('Helvetica', 40, 'bold'), fg="brown")
        self.timer.grid(row=1, column=4)

        self.retry_button = Button(text="⟲", font=('Helvetica', 25, 'bold'), command=self.clicked, anchor="center")
        self.retry_button.grid(row=1, column=0)

        # SEQUENCING ALL WORDS IN THE TEXT
        for word in self.chosen_words[self.text_start_index:self.text_end_index]:
            text_to_test = Label(text_frame, pady=2, font=("Helvetica", 20), text=word, anchor=NW)
            self.word_label_list.append(text_to_test)
            text_to_test.pack()
        self.word_label_list[self.text_start_index].configure(foreground="green")

    def clean_entry_box(self, event):
        self.text_input.delete(0, END)
        if self.maximum_time_in_second > 0:
            self.update_time()

    def update_time(self):
        self.maximum_time_in_second -= 1
        self.timer.config(text=f"Time\n{self.maximum_time_in_second}")
        if self.maximum_time_in_second > 0:
            self.timer.after(1000, self.update_time)
        self.character_per_minute_score.config(text=self.cpm_score_count)
        self.word_per_minute_score.config(text=self.wpm_score_count)
        with open("score_log_file.txt", mode="w") as score_log_file_write:
            if self.cpm_score_count >= self.best_score_from_log:
                score_log_file_write.write(str(self.cpm_score_count))
                self.best_score.config(text=self.cpm_score_count)
            else:
                score_log_file_write.write(str(self.best_score_from_log))
                self.best_score.config(text=self.best_score_from_log)
        if self.maximum_time_in_second == 0:
            messagebox.showinfo("Time is Up!", "Please press retry button to play again!")

    def clicked(self):
        self.window.destroy()
        self.__init__()

    def send_input(self, event):
        if self.maximum_time_in_second > 0:
            self.transfer_word = self.user_input.get().lower().replace(" ", "")
            if self.chosen_words[self.text_start_index] == self.transfer_word:
                self.word_label_list[self.text_start_index].configure(foreground="black")
                if self.text_start_index < self.text_end_index - 1:
                    self.word_label_list[self.text_start_index + 1].configure(foreground="green")
                self.wpm_score_count += 1
                self.cpm_score_count += len(self.chosen_words[self.text_start_index])
                self.text_start_index += 1
                self.text_input.delete(0, END)
            else:
                self.word_label_list[self.text_start_index].configure(foreground="red")

            if self.text_start_index == self.text_end_index:
                self.refresh_text_frame()

    def refresh_text_frame(self):
        self.text_end_index += 9
        self.text_entry()
        self.text_input.focus_set()
        self.text_input.delete(0, END)
