import json
from tkinter import *
from tkinter import messagebox
import pyperclip  # this pyperclip is inter platform clipboard copy and paste module

password = ""

# ---------------------------- PASSWORD GENERATOR ------------------------------- #


def pass_generator():
    import random
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']
    global password
    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_list = [random.choice(letters) for _ in range(nr_letters)]
    password_list += [random.choice(symbols) for _ in range(nr_symbols)]
    password_list += [random.choice(numbers) for _ in range(nr_numbers)]
    random.shuffle(password_list)

    password = "".join(password_list)
    password_entry.delete(0, END)
    password_entry.insert(0, password)
    print(f"Your password is: {password}")

    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save_pass():
    website_data = website_entry.get()
    email_data = email_entry.get()
    pass_data = password_entry.get()
    new_data = {
        website_data: {
            "email": email_data,
            "password": pass_data
        }
    }
    if len(website_entry.get()) == 0 or len(password_entry.get()) == 0 or len(email_entry.get()) == 0:
        messagebox.showerror(title="Oops", message="Please make sure you haven't left any empty fields.")
    else:
        is_ok = messagebox.askokcancel(title=website_data,
                                       message=f"These are the details entered: \nEmail: {email_data} "
                                               f"\nPassword: {pass_data} \nIs it ok to save?")

        if is_ok:
            # with open("all data gathered by password manager.txt", mode="a") as data:
            #     all_data = f"{website_data} | {email_data} | {pass_data} \n"
            #     data.write(all_data)
            try:
                with open("data.json", "r") as data_file:
                    # read old data
                    data = json.load(data_file)
            except FileNotFoundError:
                with open("data.json", "w") as data_file:
                    json.dump(new_data, data_file, indent=4)
                # update old data with new data
            else:
                data.update(new_data)

                with open("data.json", "w") as data_file:
                    # saving updated data
                    json.dump(data, data_file, indent=4)
            finally:
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- PASSWORD FINDER ---------------------------- #

def find_password():
    website_data = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)

    except FileNotFoundError:
        messagebox.showerror(message="No Data File Found")
    # except KeyError:
    #     messagebox.showerror(message=f"No details for the {website_data} exists.")
    else:
        if website_data in data:
            found_email = data[website_data]["email"]
            found_pass = data[website_data]["password"]
            messagebox.showinfo(title=website_data, message=f"Email = {found_email}\nPassword = {found_pass}")
        else:
            messagebox.showerror(message=f"No details for the {website_data} exists.")

# note an exception catching is happened rarely and if else catching happens continuously so there is difference
# between catching errors by exception and catching with if else statements


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)
canvas = Canvas(width=200, height=200)
logo_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_image)
canvas.grid(column=1, row=0)

# all labels
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

# all entry
website_entry = Entry(width=41)
website_entry.grid(column=1, row=1, columnspan=1)
email_entry = Entry(width=60)
email_entry.grid(column=1, row=2, columnspan=3)
email_entry.insert(0, "modi.2024@aayega.com")
password_entry = Entry(width=42)
password_entry.grid(column=1, row=3, columnspan=1)

# all buttons
generate_button = Button(text="Generate Password", command=pass_generator)
generate_button.grid(column=2, row=3, columnspan=2)
add_button = Button(text="Add", width=51, command=save_pass)
add_button.grid(column=1, row=4, columnspan=3)

search_button = Button(text="Search", width=14, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
