from tkinter import *
from tkinter import font
from chat import get_response, bot_name

BG_GREY = "#ABB2B9"
BG_COLOR = "#17202A"
TEXT_COL = "#EAECEE"

FONT = "Arial 14"
FONT_BOLD = "Arial 13 bold"


class ChatApp:
    def __init__(self):
        self.window = Tk()
        self._setup_main_window()

    def run(self):
        self.window.mainloop()

    def _setup_main_window(self):
        self.window.title("Chat")
        self.window.resizable(width=False, height=False)
        self.window.configure(width=400, height=550, bg=BG_COLOR)

        # Head label
        head_lable = Label(self.window, bg=BG_COLOR, fg=TEXT_COL,
                           text="Welcome Aboard", font=FONT_BOLD, pady=10)
        head_lable.place(relwidth=1)

        # Small div
        line = Label(self.window, width=380, bg=BG_GREY)
        line.place(relwidth=1, rely=0.07, relheight=0.012)

        # Text box
        self.text_box = Text(self.window, width=20, height=2,
                             bg=BG_COLOR, font=FONT, pady=5, padx=5, fg=TEXT_COL)
        self.text_box.place(relheight=0.745, relwidth=1, rely=0.08)
        self.text_box.configure(cursor="arrow", state=DISABLED)

        # Scroll
        scrollbar = Scrollbar(self.text_box)
        scrollbar.place(relheight=1, relx=.974)
        scrollbar.configure(command=self.text_box.yview)

        # Bottom text command line place
        bot_lable = Label(self.window, bg=BG_GREY, height=80)
        bot_lable.place(relwidth=1, rely=0.825)

        # Message box
        self.msg_box = Entry(bot_lable, bg="#2C3E50", fg=TEXT_COL, font=FONT)
        self.msg_box.place(relwidth=.74, relheight=0.06,
                           rely=0.008, relx=0.011)
        self.msg_box.focus()
        self.msg_box.bind("<Return>", self._on_enter_pressed)

        # Send Button
        send_button = Button(bot_lable, text="Send", font=FONT_BOLD,
                             width=20, bg=BG_GREY, command=lambda: self._on_enter_pressed(None))
        send_button.place(relx=0.77, rely=0.008, relheight=0.06, relwidth=0.22)

    def _on_enter_pressed(self, event):
        msg = self.msg_box.get()
        self._insert_msg(msg, "You")

    def _insert_msg(self, msg, sender):
        if not msg:
            return

        self.msg_box.delete(0, END)
        msg1 = f"{sender}: {msg}\n\n"
        self.text_box.configure(cursor="arrow", state=NORMAL)
        self.text_box.insert(END, msg1)
        self.text_box.configure(cursor="arrow", state=DISABLED)

        botMsg = f"{bot_name}: {get_response(msg)}\n\n"
        self.text_box.configure(cursor="arrow", state=NORMAL)
        self.text_box.insert(END, botMsg)
        self.text_box.configure(cursor="arrow", state=DISABLED)

        self.text_box.see(END)


if __name__ == "__main__":
    app = ChatApp()
    app.run()
