
import customtkinter
from CTkMenuBar import *
from tkinter import StringVar
from PIL import Image
from random import randint
import os
import re
from tkinter import messagebox


class Auth(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SignIn = None
        self.BricksApp = None
        # self.mb = None
        self.title("Auth")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(
            Image.open(image_path), size=(900, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Hello!",
                                                  font=("Roboto", 32, "bold"))
        self.login_label.grid(row=0, pady=15, sticky="n")
        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*",
                                                     placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event,
                                                    width=100)
        self.login_button.grid(row=4, column=0, pady=(0, 10))
        self.reg_lab = customtkinter.CTkLabel(self.login_frame, text="Don't have an account?",
                                              font=("Roboto", 16, "bold"))
        self.reg_lab.grid(row=5, column=0, pady=(50, 10))
        self.reg_but = customtkinter.CTkButton(self.login_frame, text="Sign In", command=self.open_sign_in_window,
                                               width=75)
        self.reg_but.grid(row=6, column=0)
        self.exit_button = customtkinter.CTkButton(self.login_frame, text="Exit", width=40, height=30,
                                                   command=self.exit_from_form)
        self.exit_button.grid(row=7, column=0, pady=(200, 0))

    def login_event(self):
        print(
            "Login pressed - username:",
            self.username_entry.get(),
            "password:",
            self.password_entry.get())

        # Check login credentials (replace this with your actual authentication
        # logic)
        if self.check_user_log(self.username_entry.get(),
                               self.password_entry.get()):
            # Open the BricksApp window upon successful login
            self.BricksApp = BricksApp(self, self.username_entry.get())
        else:
            messagebox.showinfo(
                "Login Failed",
                "Invalid credentials. Please try again.",
                parent=self)

    def register_event(self, player_login, player_password,
                       player_email, player_gender, player_age_range):
        # Check if the username and password meet your criteria
        if len(player_login) < 4 or len(player_password) < 8:
            messagebox.showinfo(
                "Login Failed",
                "Login or password is too short.",
                parent=self)
            return

        # Check if the username is already taken
        if self.check_new_user_reg(player_login):
            messagebox.showinfo(
                "Login Failed",
                "Username is already taken.",
                parent=self)
            return

        # Perform additional checks if needed

        # Add the new user
        self.add_new_user(
            player_login,
            player_password,
            player_email,
            player_gender,
            player_age_range)

        # Open the BricksApp window upon successful registration
        self.BricksApp = BricksApp(self, player_login)

    def add_new_user(self, player_login, player_password,
                     player_email, player_gender, player_age_range):
        """Function to write user data to the file"""
        file_path = f'{player_login}_user_statistics.txt'  # Use a unique file for each user
        with open(file_path, 'w') as file:
            # Initialize user statistics to 0 games won and 0 total games
            file.write("0 0\n")

        file_path = 'DatabaseForGame.txt'
        with open(file_path, 'a') as file:
            file.write(
                f"{'%%'.join([player_login, player_password, player_email, player_gender, player_age_range, '0', '0', '0', '0', '0', '0'])}\n")

    def check_user_log(self, login, password):
        file = open('DatabaseForGame.txt')
        for line in file:
            player_list = line.split('%%')
            if login == player_list[0] and password == player_list[1]:
                return True
        file.close()
        return False

    def check_new_user_reg(self, login):
        file = open('DatabaseForGame.txt')
        for line in file:
            if login == line.split('%%')[0]:
                return True
        file.close()
        return False

    def exit_from_form(self):
        self.destroy()

    def open_sign_in_window(self):
        self.SignIn = SignIn(master=self, exit_command=self.exit_from_form,
                             register_command=self.register_event, auth_instance=self)
        self.SignIn.focus_force()


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, master=None, exit_command=None,
                 register_command=None, auth_instance=None):
        super().__init__(master)

        self.attributes("-topmost", True)

        self.exit_from_form = exit_command
        self.register_event = register_command

        self.exit_from_form = exit_command

        self.title("SignIn")
        self.geometry("900x700")
        self.resizable(False, False)

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(
            Image.open(image_path), size=(900, 700))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Registrarion",
                                                  font=("Roboto", 32, "bold"))
        self.login_label.grid(row=0, pady=15, sticky="n")
        self.username_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*",
                                                     placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.mail_entry = customtkinter.CTkEntry(
            self.login_frame, width=200, placeholder_text="email")
        self.mail_entry.grid(row=3, column=0, padx=30, pady=(0, 15))

        self.gen_lab = customtkinter.CTkLabel(
            self.login_frame, text="Select gender", font=(
                "Roboto", 16, "bold"))
        self.gen_lab.grid(row=4, column=0, pady=10)

        self.gender = customtkinter.StringVar()
        self.female_rad = customtkinter.CTkRadioButton(self.login_frame, text="Woman", fg_color="#FFF",
                                                       value="Женщина",
                                                       variable=self.gender)
        self.female_rad.grid(row=5, column=0, pady=10)
        self.male_rad = customtkinter.CTkRadioButton(self.login_frame, text="Man", fg_color="#FFF", value="Мужчина",
                                                     variable=self.gender)
        self.male_rad.grid(row=6, column=0, pady=10)

        # Создаем список
        self.age_lab = customtkinter.CTkLabel(self.login_frame, text="State your age \n range",
                                              font=("Roboto", 16, "bold"))
        self.age_lab.grid(row=7, column=0, pady=(20, 20))

        self.optionmenu_1 = customtkinter.CTkOptionMenu(self.login_frame, dynamic_resizing=False,
                                                        values=["", "0-18", "18-35", "35+"])
        self.optionmenu_1.grid(row=8, column=0)

        self.login_button = customtkinter.CTkButton(self.login_frame, text="Sign In", command=self.sign_in_event,
                                                    width=100)
        self.login_button.grid(row=9, column=0, pady=(50, 50))

        self.button_image = customtkinter.CTkImage(
            Image.open("img/return.png"), size=(26, 26))
        self.return_button = customtkinter.CTkButton(self.login_frame, text="", command=self.return_back, width=100,
                                                     image=self.button_image)
        self.return_button.grid(row=10, column=0, pady=(0, 10))

        self.exit_button = customtkinter.CTkButton(self.login_frame, text="Exit", width=40, height=30,
                                                   command=self.exit_from_form)
        self.exit_button.grid(row=11, column=0)

        self.auth_instance = auth_instance

    def sign_in_event(self):
        player_login_reg = self.username_entry.get()
        player_password_reg = self.password_entry.get()
        player_email_reg = self.mail_entry.get()
        player_gender_reg = self.gender.get()
        player_age_range = self.optionmenu_1.get()

        # Проверка заполнения всех полей
        if not all([player_login_reg, player_password_reg,
                   player_email_reg, player_gender_reg, player_age_range]):
            # Если какое-то поле не заполнено, выведите сообщение об ошибке
            messagebox.showinfo(
                "Login Failed",
                "Please fill in all fields.",
                parent=self)
            return

        # Проверка формата электронной почты
        if not re.fullmatch(r'[\w.-]+@[\w.-]+(\.\w+)+', player_email_reg):
            messagebox.showinfo(
                "Login Failed",
                "Invalid email format.",
                parent=self)
            return

        # Проверка длины логина и пароля
        if len(player_login_reg) < 4 or len(player_password_reg) < 8:
            messagebox.showinfo(
                "Login Failed",
                "Login or password is too short.",
                parent=self)
            return

        if self.auth_instance.check_new_user_reg(player_login_reg):
            messagebox.showinfo(
                "Login Failed",
                "A user with this login already exists",
                parent=self)
        else:
            self.auth_instance.add_new_user(player_login_reg, player_password_reg, player_email_reg, player_gender_reg,
                                            player_age_range)
            # destroySingUp()
            self.register_event(player_login_reg, player_password_reg, player_email_reg, player_gender_reg,
                                player_age_range)
            print("Все гуд")

            # Переход на экран игры (просто пример, замените на ваш реальный
            # код)
            self.destroy()

    def return_back(self):
        self.destroy()


class BricksApp(customtkinter.CTkToplevel):

    def __init__(self, master=None, username=""):
        super().__init__(master)

        self.title("Bricks")
        self.geometry("900x600")
        self.resizable(False, False)

        self.attributes("-topmost", True)

        self.username = username
        self.player_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        self.win_statistics_count = 0

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "background.jpg")
        self.bg_image = customtkinter.CTkImage(
            Image.open(image_path), size=(900, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        self.greeting_label = customtkinter.CTkLabel(self, text=f"Hello, {self.username}",
                                                     font=("Roboto", 43, "bold"))
        self.greeting_label.grid(row=0, column=0, sticky="N", pady=5)
        # Number of remaining bricks
        self.bricks_label = customtkinter.CTkLabel(self, text="Remaining Bricks 🧱:",
                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bricks_label.grid(row=0, column=0, sticky="N", pady=80)
        # Assuming bricks_amount will be set later
        self.bricks_amount = randint(12, 20)
        self.remaining_bricks_var = customtkinter.StringVar(
            value=str(self.bricks_amount))
        self.remaining_bricks_string = customtkinter.CTkLabel(master=self, textvariable=self.remaining_bricks_var,
                                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        self.remaining_bricks_string.grid(
            row=0, column=0, sticky="N", pady=120)

        # Frame for human player's turn
        self.human_turn_frame = customtkinter.CTkFrame(self)
        self.human_turn_frame.grid(row=0, column=0, sticky="W")

        # Label for human player's turn
        self.human_turn_label = customtkinter.CTkLabel(self.human_turn_frame, text="Your turn:",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.human_turn_label.grid(
            row=0, column=0, padx=10, pady=(
                10, 0), sticky="W")

        # Buttons for human player's turn
        self.take_one = customtkinter.CTkButton(self.human_turn_frame, text="Take 1", width=100,
                                                command=lambda: self.turn(1))
        self.take_one.grid(row=1, column=0, padx=5, pady=5)
        self.take_two = customtkinter.CTkButton(self.human_turn_frame, text="Take 2", width=100,
                                                command=lambda: self.turn(2))
        self.take_two.grid(row=2, column=0, padx=5, pady=5)
        self.take_three = customtkinter.CTkButton(self.human_turn_frame, text="Take 3", width=100,
                                                  command=lambda: self.turn(3))
        self.take_three.grid(row=3, column=0, padx=5, pady=5)

        # Frame for computer player's turn
        self.comp_turn_frame = customtkinter.CTkFrame(self)
        self.comp_turn_frame.place(relx=1, rely=0.5, anchor="e")

        self.comp_turn_label = customtkinter.CTkLabel(self.comp_turn_frame, text="Computer's Turn:",
                                                      font=customtkinter.CTkFont(size=14))
        self.comp_turn_label.pack(pady=5)

        self.comp_do_var = StringVar(value="Your turn first")
        self.comp_do = customtkinter.CTkLabel(self.comp_turn_frame, textvariable=self.comp_do_var,
                                              font=customtkinter.CTkFont(size=12))
        self.comp_do.pack()

        # Result label
        self.result_game = customtkinter.CTkLabel(
            self, font=customtkinter.CTkFont(size=16))
        self.result_game.place(relx=0.5, rely=0.5, anchor="n")

        # Win statistics
        self.win_statistics_count = 0
        self.win_statistics_label = customtkinter.CTkLabel(self, text=f"Games Won: {0}",
                                                           font=customtkinter.CTkFont(size=14))
        self.win_statistics_label.place(relx=0.5, rely=1, anchor="s")

        self.create_menu()

    def create_menu(self):
        menu = CTkTitleMenu(self.master)
        button_1 = menu.add_cascade("Game")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(
            option="New game",
            command=lambda: self.play_again())
        dropdown1.add_option(option="Main menu",
                             command=lambda: self.return_to_main_menu())
        dropdown1.add_option(
            option="Statistics",
            command=lambda: self.statistics())
        dropdown1.add_option(
            option="Exit",
            command=lambda: self.exit_the_game())

    def return_to_main_menu(self):
        self.destroy()  # Destroy the current BricksApp window

    def turn(self, amount):
        # Human's turn
        self.bricks_amount = self.bricks_amount - amount
        self.remaining_bricks_var.set(str(self.bricks_amount))

        # Check for game outcomes after human's turn
        if self.bricks_amount == 0:
            # Human wins
            self.win_statistics_count += 1
            self.statistics()
            self.update_user_statistics(1, 1)
            self.update_all_users_statistics(
                self.username, 1, 1)  # Update all users statistics
            self.result_game = customtkinter.CTkLabel(
                self, text="You Win!", fg_color="green", width=75, height=50)
            self.result_game.place(relx=0.5, rely=0.5, anchor="center")
            self.disable()
        elif self.bricks_amount < 4:
            # Human loses
            self.comp_do_var.set("Взял {0}".format(self.bricks_amount))
            self.bricks_amount = 0
            self.result_game = customtkinter.CTkLabel(
                self, text="You Lose", fg_color="red", width=75, height=50)
            self.result_game.place(relx=0.5, rely=0.5, anchor="center")
            self.disable()

        # Update the text for remaining bricks
        self.remaining_bricks_var.set(str(self.bricks_amount))

        # Disable buttons when there are fewer bricks than available for the
        # human to choose
        if self.bricks_amount == 1:
            self.take_two.configure(state="disabled")
            self.take_three.configure(state="disabled")
        elif self.bricks_amount == 2:
            self.take_three.configure(state="disabled")

        self.update_idletasks()  # Force an immediate redraw

        # Computer's turn
        if self.bricks_amount > 0:
            comp_turn = randint(1, min(3, self.bricks_amount))
            self.bricks_amount = self.bricks_amount - comp_turn
            self.comp_do_var.set("Взял {0}".format(comp_turn))

            # Update the text for remaining bricks
            self.remaining_bricks_var.set(str(self.bricks_amount))

            if self.bricks_amount == 0:
                # Computer wins
                self.statistics()
                self.update_all_users_statistics(
                    self.username, 0, 1)  # Update all users statistics
                self.result_game = customtkinter.CTkLabel(
                    self, text="You lose", fg_color="red")
                self.result_game.place(relx=0.5, rely=0.5, anchor="center")
                self.disable()

            # Disable buttons when there are fewer bricks than available for
            # the human to choose
            if self.bricks_amount == 1:
                self.take_two.configure(state="disabled")
                self.take_three.configure(state="disabled")
            elif self.bricks_amount == 2:
                self.take_three.configure(state="disabled")

            # Check for game outcomes after computer's turn
            if self.bricks_amount == 0:
                # Computer wins
                self.result_game = customtkinter.CTkLabel(
                    self, text="You lose", fg_color="red")
                self.result_game.place(relx=0.5, rely=0.5, anchor="center")
                self.disable()

        self.update_idletasks()  # Force an immediate redraw

    def disable(self):
        self.take_one.configure(state="disabled")
        self.take_two.configure(state="disabled")
        self.take_three.configure(state="disabled")

    def enable_buttons(self):
        self.take_one.configure(state="normal")
        self.take_two.configure(state="normal")
        self.take_three.configure(state="normal")

    def play_again(self):
        self.bricks_amount = randint(12, 20)
        self.remaining_bricks_var.set(str(self.bricks_amount))
        self.result_game["fg"] = "grey"
        self.result_game.place_forget()
        self.enable_buttons()

    # Add this method to the BricksApp class
    def statistics(self):
        user_statistics = self.get_user_statistics()
        all_users_statistics = self.get_all_users_statistics()

        message = f"Your Statistics:\nGames Won: {user_statistics['games_won']}\nTotal Games Played: {user_statistics['total_games']}\n\n"
        message += "All Users Statistics:\n"
        for i, stats in enumerate(all_users_statistics, start=1):
            message += f"{i}. Username: {stats['username']}, Games Won: {stats['games_won']}, Total Games Played: {stats['total_games']}\n"

        # Update the label showing games won and total games in the Statistics
        # window
        self.win_statistics_label.configure(
            text=f"Games Won: {user_statistics['games_won']}, Total Games Played: {user_statistics['total_games']}")

        # Update the label showing games won and total games in the main window
        if hasattr(self.master, 'win_statistics_label'):
            self.master.win_statistics_label.configure(
                text=f"Games Won: {user_statistics['games_won']}, Total Games Played: {user_statistics['total_games']}")

        messagebox.showinfo("Statistics", message, parent=self)

    def get_user_statistics(self):
        # Load user statistics from the individual file
        user_stats = {"games_won": 0, "total_games": 0}
        try:
            file_path = f'{self.username}_user_statistics.txt'
            with open(file_path, 'r') as file:
                lines = file.readlines()
                if lines:
                    user_stats["games_won"], user_stats["total_games"] = map(
                        int, lines[0].split())
        except FileNotFoundError:
            pass

        return user_stats

    def update_user_statistics(self, games_won, total_games):
        # Update and save user statistics to the individual file
        user_stats = self.get_user_statistics()
        user_stats["games_won"] += games_won
        user_stats["total_games"] += total_games

        file_path = f'{self.username}_user_statistics.txt'
        with open(file_path, 'w') as file:
            file.write(
                f"{user_stats['games_won']} {user_stats['total_games']}")

    def get_all_users_statistics(self):
        # Load and return statistics for all users
        all_users_stats = []
        try:
            with open('all_users_statistics.txt', 'r') as file:
                for line in file:
                    username, games_won, total_games = line.split()
                    all_users_stats.append(
                        {"username": username, "games_won": int(games_won), "total_games": int(total_games)})
        except FileNotFoundError:
            pass

        return sorted(all_users_stats,
                      key=lambda x: x["games_won"], reverse=True)

    def update_all_users_statistics(self, username, games_won, total_games):
        # Update and save statistics for all users to file
        all_users_stats = self.get_all_users_statistics()
        existing_user = next(
            (user for user in all_users_stats if user["username"] == username), None)

        if existing_user:
            existing_user["games_won"] += games_won
            existing_user["total_games"] += total_games
        else:
            all_users_stats.append(
                {"username": username, "games_won": games_won, "total_games": total_games})

        with open('all_users_statistics.txt', 'w') as file:
            for user in all_users_stats:
                file.write(
                    f"{user['username']} {user['games_won']} {user['total_games']}\n")

    def exit_the_game(self):
        self.save()
        self.quit()

    def save(self):
        # Save user statistics and update all users statistics
        self.update_user_statistics(self.win_statistics_count, 1)
        self.update_all_users_statistics(
            self.username, self.win_statistics_count, 1)


app = Auth()
app.mainloop()
