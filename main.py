from operator import index
from tkinter import *
import pandas
import random

from pandas.core.interchange.dataframe_protocol import DataFrame

word = {}


try:
    df = pandas.read_csv("./data/words_to_learn.csv")
except FileNotFoundError:
    df = pandas.read_csv("./data/french_words.csv")
    data = df.to_dict(orient="records")
else:
    data = df.to_dict(orient="records")
    # df_learn = pandas.DataFrame(data)
    # df_learn.to_csv("./data/words_to_learn.csv", index=False)


#----------------------------FLIP THE CARD-------------------------------------#
def flip_card():
    canvas.itemconfig(canvas_img, image=new_image)
    canvas.itemconfig(lang_text, text="English", fill="white")
    english_word = word["English"]
    canvas.itemconfig(word_text, text=english_word, fill="white")


#----------------------------READ FROM CSV FILE--------------------------------#
def read_csv():
    global word, flip_cards  #
    window.after_cancel(flip_cards)
    word = random.choice(data)
    french_word = word["French"]
    canvas.itemconfig(word_text, text=french_word, fill="black")
    canvas.itemconfig(lang_text, text="French", fill="black")
    canvas.itemconfig(canvas_img, image=old_image)
    flip_cards = window.after(3000, func=flip_card)


def is_known():
    data.remove(word)
    read_csv()
    print(len(data))
    df_to_learn = pandas.DataFrame(data)
    df_to_learn.to_csv("./data/words_to_learn.csv", index=False)



#----------------------------- UI SETUP----------------------------------------#
BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("Flashy")
window.minsize(width=800, height=526)
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)
flip_cards = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)

old_image = PhotoImage(file="./images/card_front.png")
new_image = PhotoImage(file="./images/card_back.png")
canvas_img = canvas.create_image(400, 263, image=old_image)
lang_text = canvas.create_text(400, 150, text="French", font=("Ariel", 40, "italic"))
word_text = canvas.create_text(400, 263, text="English", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2, padx=50, pady=50)

right_image = PhotoImage(file="./images/right.png")
right_btn = Button(image=right_image, highlightthickness=0, command=is_known)
right_btn.grid(row=1, column=1)

wrong_image = PhotoImage(file="./images/wrong.png")
wrong_btn = Button(image=wrong_image, highlightthickness=0, command=read_csv)
wrong_btn.grid(row=1, column=0)

read_csv()

window.mainloop()
