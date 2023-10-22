import tkinter as tk
from tkinter import scrolledtext
from metatube_classes import MetaTube


def get_product_info():
    """gets user information from entry widgets and returns them as a dictionary

    :return: dictionary, user input (product name, type, num of revies)
    """
    name = name_entry.get()
    product_type = type_entry.get()
    num_reviews = num_reviews_entry.get()
    return {
        "name": name,
        "type": product_type,
        "num": int(num_reviews)
    }


def add_to_progress(message):
    """adds a string as a message to the progress box

    :param message: string, message to display to user
    """
    progress_text.config(state="normal")
    progress_text.insert("end", message + "\n")
    progress_text.config(state="disabled")


def display_output(message):
    """displays a string in the output box (editable)

    :param message: a string to display as output to the user
    """
    result_text.config(state="normal")
    result_text.delete(1.0, "end")
    result_text.insert("end", message)
    result_text.config(state="normal")


def go():
    """a function that runs when the go button is pressed
    gets the info from the user, then uses the Metatube class to:
    - search YouTube videos
    - retrieve transcripts
    - create the prompt and send it to Claude
    - receive a response from Claude
    and shows the response in the output box
    """
    params = get_product_info()

    add_to_progress('Searching youtube...')
    mt = MetaTube(params['num'], params['type'], params['name'])

    add_to_progress('Recovering data...')

    try:
        response = mt.run()
    except ValueError:
        response = 'You have reached your limit of Claude messages.'

    add_to_progress('Recovering summary...')
    display_output(response)


window = tk.Tk()
window.title("Product Information")

# entry widgets
name_label = tk.Label(window, text="Name of Product")
name_label.pack()
name_entry = tk.Entry(window)
name_entry.pack()

type_label = tk.Label(window, text="Type of Product")
type_label.pack()
type_entry = tk.Entry(window)
type_entry.pack()

num_reviews_label = tk.Label(window, text="Number of Reviews")
num_reviews_label.pack()
num_reviews_entry = tk.Entry(window)
num_reviews_entry.pack()

# smaller non-editable progress textbox
progress_label = tk.Label(window, text="Progress:")
progress_label.pack()
progress_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=40, height=3, state="disabled")
progress_text.pack()

# larger output textbox
result_label = tk.Label(window, text="Output:")
result_label.pack()
result_text = scrolledtext.ScrolledText(window, wrap=tk.WORD, width=60, height=15, state="normal")
result_text.pack()

# go button
process_button = tk.Button(window, text="Go", command=go)
process_button.pack()

window.mainloop()
