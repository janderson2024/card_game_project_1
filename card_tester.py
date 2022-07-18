import tkinter
import Card
from tkinter import *
from PIL import Image, ImageTk


def flip_card(card):
    card.set_display()
    card_image = card.image
    image = Image.open(f'card_images/{card_image}').convert("RGBA")
    resize_image = image.resize((250, 363))
    img = ImageTk.PhotoImage(resize_image)
    card_space.configure(image=img)
    card_space.img = img
    image_label_text.configure(text=f'{card.image}')
    image_label_text.text = f'{card.image}'
    displayable_label_text.configure(text=f'{card.displayable}')
    displayable_label_text.text = f'{card.displayable}'
    str_label_text.configure(text=f'{card.__str__()}')
    str_label_text.text = f'{card.__str__()}'


def flip_card2(card):
    card.set_display()
    card_image = card.image
    image = Image.open(f'card_images/{card_image}').convert("RGBA")
    resize_image = image.resize((250, 363))
    img = ImageTk.PhotoImage(resize_image)
    card_space2.configure(image=img)
    card_space2.img = img
    image_label_text2.configure(text=f'{card.image}')
    image_label_text2.text = f'{card.image}'
    displayable_label_text2.configure(text=f'{card.displayable}')
    displayable_label_text2.text = f'{card.displayable}'
    str_label_text2.configure(text=f'{card.__str__()}')
    str_label_text2.text = f'{card.__str__()}'


if __name__ == '__main__':
    # card1 = Card.Card('\u2660', "A")
    card1 = Card.Card(4, 1)
    # card2 = Card.Card(None, 'L')
    card2 = Card.Card(0, 14)

    app = tkinter.Tk()
    app.title('Card Tester')
    app.configure(background='green')

    card_image = card1.image
    image = Image.open(f'card_images/{card_image}').convert("RGBA")
    resize_image = image.resize((250, 363))
    img = ImageTk.PhotoImage(resize_image)
    card_space = Label(app, image=img, background='green')
    card_space.grid(row=0, column=0, columnspan=2)

    card_image2 = card2.image
    image2 = Image.open(f'card_images/{card_image2}').convert("RGBA")
    resize_image2 = image2.resize((250, 363))
    img2 = ImageTk.PhotoImage(resize_image2)
    card_space2 = Label(app, image=img2, background='green')
    card_space2.grid(row=0, column=2, columnspan=2)

    flip_button = Button(app, text='Flip Card', command=lambda: flip_card(card1))
    flip_button.grid(row=1, column=0, columnspan=2)

    flip_button2 = Button(app, text='Flip Card', command=lambda: flip_card2(card2))
    flip_button2.grid(row=1, column=2, columnspan=2)

    rank_label = Label(app, text='Card Rank:', font='bold', width=20)
    rank_label.grid(row=3, column=0)
    rank_label_text = Label(app, text=f'{card1.rank}', font='bold', width=20)
    rank_label_text.grid(row=3, column=1)
    suit_label = Label(app, text='Card Suit:', font='bold', width=20)
    suit_label.grid(row=4, column=0)
    suit_label_text = Label(app, text=f'{card1.suit}', font='bold', width=20)
    suit_label_text.grid(row=4, column=1)
    suit_symbol_label = Label(app, text='Suit Text:', font='bold', width=20)
    suit_symbol_label.grid(row=5, column=0)
    suit_symbol_label_text = Label(app, text=f'{card1.suit_text}', font='bold', width=20)
    suit_symbol_label_text.grid(row=5, column=1)
    color_label = Label(app, text='Color:', font='bold', width=20)
    color_label.grid(row=6, column=0)
    color_label_text = Label(app, text=f'{card1.color}', font='bold', width=20)
    color_label_text.grid(row=6, column=1)
    image_label = Label(app, text='Image Displayed:', font='bold', width=20)
    image_label.grid(row=7, column=0)
    image_label_text = Label(app, text=f'{card1.image}', font='bold', width=20)
    image_label_text.grid(row=7, column=1)
    displayable_label = Label(app, text='Displayable:', font='bold', width=20)
    displayable_label.grid(row=8, column=0)
    displayable_label_text = Label(app, text=f'{card1.displayable}', font='bold', width=20)
    displayable_label_text.grid(row=8, column=1)
    str_label = Label(app, text='__str__:', font='bold', width=20)
    str_label.grid(row=9, column=0)
    str_label_text = Label(app, text=f'{card1.__str__()}', font='bold', width=20)
    str_label_text.grid(row=9, column=1)

    rank_label2 = Label(app, text='Card Rank:', font='bold', width=20)
    rank_label2.grid(row=3, column=2)
    rank_label_text2 = Label(app, text=f'{card2.rank}', font='bold', width=20)
    rank_label_text2.grid(row=3, column=3)
    suit_label2 = Label(app, text='Card Suit:', font='bold', width=20)
    suit_label2.grid(row=4, column=2)
    suit_label_text2 = Label(app, text=f'{card2.suit}', font='bold', width=20)
    suit_label_text2.grid(row=4, column=3)
    suit_symbol_label2 = Label(app, text='Suit Text:', font='bold', width=20)
    suit_symbol_label2.grid(row=5, column=2)
    suit_symbol_label_text2 = Label(app, text=f'{card2.suit_text}', font='bold', width=20)
    suit_symbol_label_text2.grid(row=5, column=3)
    color_label2 = Label(app, text='Color:', font='bold', width=20)
    color_label2.grid(row=6, column=2)
    color_label_text2 = Label(app, text=f'{card2.color}', font='bold', width=20)
    color_label_text2.grid(row=6, column=3)
    image_label2 = Label(app, text='Image Displayed:', font='bold', width=20)
    image_label2.grid(row=7, column=2)
    image_label_text2 = Label(app, text=f'{card2.image}', font='bold', width=20)
    image_label_text2.grid(row=7, column=3)
    displayable_label2 = Label(app, text='Displayable:', font='bold', width=20)
    displayable_label2.grid(row=8, column=2)
    displayable_label_text2 = Label(app, text=f'{card2.displayable}', font='bold', width=20)
    displayable_label_text2.grid(row=8, column=3)
    str_label2 = Label(app, text='__str__:', font='bold', width=20)
    str_label2.grid(row=9, column=2)
    str_label_text2 = Label(app, text=f'{card2.__str__()}', font='bold', width=20)
    str_label_text2.grid(row=9, column=3)

    app.mainloop()
