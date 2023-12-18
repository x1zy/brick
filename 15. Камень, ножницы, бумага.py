'''
import customtkinter
from tkinter import messagebox as mb
from tkinter import Tk
from PIL import Image
from random import choice
import re
import os


class CustomTkinter(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        self.title("Камень, ножницы, бумага")
        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(Image.open(image_path), size=(1280, 720))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)
        self.geometry("1280x720+330+80")
        self.resizable(False, False)
        self.config(bg="#FFF")
        self.player_list = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.countStones = 0
        self.countScissors = 0
        self.countPapers = 0
        self.victories = 0
        self.losses = 0
        self.draws = 0

    def update_data(self):
        file = open('DatabaseForGame.txt', 'r')
        lines = ""
        new_info = ""
        for line in file:
            if self.player_list[0] == line.split('%%')[0]:
                new_info = f"{'%%'.join([str(i) for i in self.player_list[0:5] + [self.countStones, self.countScissors, self.countPapers, self.victories, self.losses, self.draws]])}\n"
            else:
                lines += line
        file.close()

        file = open('DatabaseForGame.txt', 'w')
        file.write(lines)
        file.write(new_info)
        file.close()

    def check_new_user_reg(self, login):
        file = open('DatabaseForGame.txt')
        for line in file:
            for i in range(11):
                self.player_list[i] = line.split('%%')[i]
            if login == self.player_list[0]:
                return True
        file.close()

    def check_user_log(self, login, password):
        file = open('DatabaseForGame.txt')
        for line in file:
            for i in range(11):
                self.player_list[i] = line.split('%%')[i]
            if login == self.player_list[0] and password == self.player_list[1]:
                return True
        file.close()

    def add_new_user(self, player_login, player_password, player_email, player_gender, player_fav):
        file = open('DatabaseForGame.txt', 'a')
        file.write(
            f"{'%%'.join([player_login, player_password, player_email, player_gender, player_fav, '0', '0', '0', '0', '0', '0'])}\n")
        file.close()

    def sign_up(self):

        enter_lab = customtkinter.CTkLabel(self, text="Регистрация", font=("Roboto", 70, "bold"), bg_color="#FFF")
        enter_lab.place(relx=.5, rely=.1, anchor="center")

        log_lab = customtkinter.CTkLabel(self, text="Логин", font=("Roboto", 9, "bold"), bg_color="#FFF")
        log_lab.place(relx=.42, rely=.45, anchor="center")
        user_login_ent = customtkinter.CTkEntry(app)
        user_login_ent.place(relx=.5, rely=.45, anchor="center")

        pas_lab = customtkinter.CTkLabel(self, text="Пароль", font=("Roboto", 9, "bold"), bg_color="#FFF")
        pas_lab.place(relx=.42, rely=.5, anchor="center")
        user_password_ent = customtkinter.CTkEntry(app)
        user_password_ent.place(relx=.5, rely=.5, anchor="center")

        pas_lab = customtkinter.CTkLabel(self, text="Почта", font=("Roboto", 9, "bold"), bg_color="#FFF")
        pas_lab.place(relx=.42, rely=.55, anchor="center")
        user_email_ent = customtkinter.CTkEntry(app)
        user_email_ent.place(relx=.5, rely=.55, anchor="center")

        gen_lab = customtkinter.CTkLabel(self, text="Пол", font=("Roboto", 9, "bold"), bg_color="#FFF")
        gen_lab.place(relx=.5, rely=.6, anchor="center")
        gender = customtkinter.StringVar()
        female_rad = customtkinter.CTkRadioButton(text="Женщина", bg="#FFF", value="Женщина", variable=gender,
                                                  padx=15, pady=10, master=app)
        female_rad.place(relx=.46, rely=.64, anchor="center")
        male_rad = customtkinter.CTkRadioButton(text="Мужчина", bg="#FFF", value="Мужчина", variable=gender, padx=15,
                                                pady=10, master=app)
        male_rad.place(relx=.53, rely=.64, anchor="center")

        fav_lab = customtkinter.CTkLabel(self, text="Выберите любимый предмет", font=("Roboto", 9, "bold"),
                                         bg_color="#FFF")
        fav_lab.place(relx=.5, rely=.7, anchor="center")
        favorite_subject = customtkinter.StringVar()
        fav_stone_rad = customtkinter.CTkRadioButton(app, text="Камень", fg_color="#FFF",
                                                     value="Камень",
                                                     variable=favorite_subject)
        fav_stone_rad.place(relx=.43, rely=.74, anchor="center")
        fav_scis_rad = customtkinter.CTkRadioButton(app, text="Ножницы", fg_color="#FFF",
                                                    value="Ножницы",
                                                    variable=favorite_subject)
        fav_scis_rad.place(relx=.5, rely=.74, anchor="center")
        fav_pap_rad = customtkinter.CTkRadioButton(app, text="Бумага", fg_color="#FFF", value="Бумага",
                                                   variable=favorite_subject)
        fav_pap_rad.place(relx=.57, rely=.74, anchor="center")

        enter_error = customtkinter.CTkLabel(self, text="", font=("Roboto", 14, "bold"), fg_color="#FFF")
        enter_error.place(relx=.5, rely=.39, anchor="center")

        def get_n_check_data_reg():
            player_login_reg = user_login_ent.get()
            player_password_reg = user_password_ent.get()
            player_email_reg = user_email_ent.get()
            player_gender_reg = gender.get()
            player_fav_reg = favorite_subject.get()

            if player_login_reg == "":
                enter_error['text'] = "Логин не введён"

            elif len(player_login_reg) < 4:
                enter_error['text'] = "Слишком короткий логин"

            elif len(player_login_reg) > 12:
                enter_error['text'] = "Слишком длинный логин"

            elif player_password_reg == "":
                enter_error['text'] = "Пароль не введён"

            elif len(player_password_reg) < 8:
                enter_error['text'] = "Слишком короткий пароль"

            elif player_gender_reg == "":
                enter_error['text'] = "Пол не выбран"

            elif player_fav_reg == "":
                enter_error['text'] = "Любимый предмет не выбран"

            else:
                if re.fullmatch(r'[\w.-]+@[\w.-]+(\.\w+)+', player_email_reg):
                    if self.check_new_user_reg(player_login_reg):
                        enter_error['text'] = "Пользователь с таким логином уже существует"
                    else:
                        self.add_new_user(player_login_reg, player_password_reg, player_email_reg, player_gender_reg,
                                          player_fav_reg)
                        destroy_sign_up()
                        self.check_user_log(player_login_reg, player_password_reg)
                        self.game()
                else:
                    enter_error['text'] = "Почта введена неверно"

        def destroy_sign_up():
            enter_error.destroy()
            enter_lab.destroy()
            log_lab.destroy()
            user_login_ent.destroy()
            user_password_ent.destroy()
            user_email_ent.destroy()
            gen_lab.destroy()
            female_rad.destroy()
            male_rad.destroy()
            fav_lab.destroy()
            fav_stone_rad.destroy()
            fav_scis_rad.destroy()
            fav_pap_rad.destroy()
            log_but.destroy()
            back_but.destroy()
            pas_lab.destroy()

        log_but = customtkinter.CTkButton(text="Зарегистрироваться", font=("Roboto", 10, "bold"),
                                          width=19, height=1, border_width=1,
                                          command=get_n_check_data_reg, master=app
                                          )
        log_but.place(relx=.5, rely=.8, anchor="center")

        def return_log_in():
            destroy_sign_up()
            self.log_in()

        back_but = customtkinter.CTkButton(app, text="Вход", font=("Roboto", 10, "bold"),
                                           width=19, height=1, border_width=1,
                                           command=return_log_in
                                           )
        back_but.place(relx=.2, rely=.9, anchor="center")

    def log_in(self):
        login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        login_frame.grid(row=0, column=0, sticky="ns")

        enter_lab = customtkinter.CTkLabel(login_frame, text="Вход", font=customtkinter.CTkFont(size=70, weight="bold"))
        enter_lab.grid(row=0, column=0, padx=30, pady=(150, 15))

        user_login_ent = customtkinter.CTkEntry(login_frame, width=200, placeholder_text="username")
        user_login_ent.grid(row=1, column=0, padx=30, pady=(15, 15))

        user_password_ent = customtkinter.CTkEntry(login_frame, width=200, show="*", placeholder_text="password")
        user_password_ent.grid(row=2, column=0, padx=30, pady=(0, 15))

        enter_error = customtkinter.CTkLabel(self, text="test", font=("Roboto", 14, "bold"), fg_color="#FFF")
        enter_error.place(relx=.5, rely=.39, anchor="center")

        def get_n_check_data_log():
            player_login_log = user_login_ent.get()
            player_password_log = user_password_ent.get()

            if player_login_log == "":
                enter_error['text'] = "Логин не введён"

            elif player_password_log == "":
                enter_error['text'] = "Пароль не введён"

            else:
                if self.check_user_log(player_login_log, player_password_log):
                    self.destroy()
                    self.game()
                else:
                    enter_error['text'] = "Пользователя с таким логином нет или пароль не верный"

        log_but = customtkinter.CTkButton(login_frame, text="Войти", width=14, height=1, border_width=1,
                                          command=get_n_check_data_log
                                          )

        log_but.place(relx=.5, rely=.55, anchor="center")

        def destroy_log_in():
            enter_error.destroy()
            enter_lab.destroy()
            user_login_ent.destroy()
            user_password_ent.destroy()
            log_but.destroy()
            reg_lab.destroy()
            reg_but.destroy()
            exit_but.destroy()
            pass

        def reg():
            destroy_log_in()
            self.sign_up()

        reg_lab = customtkinter.CTkLabel(self, text="Нет аккаунта?", font=("Roboto", 9, "bold"), bg_color="#FFF")
        reg_lab.place(relx=.45, rely=.6, anchor="center")

        reg_but = customtkinter.CTkButton(text="Зарегистрироваться",
                                          width=18, height=1, border_width=1,
                                          command=reg, master=app
                                          )
        reg_but.place(relx=.55, rely=.6, anchor="center")

        def exit_from_form():
            if mb.askokcancel("Выход", "Вы действительно хотите выйти?"):
                self.destroy()

        self.protocol("WM_DELETE_WINDOW", exit_from_form)

        exit_but = customtkinter.CTkButton(text="Выйти", font=("Roboto", 10, "bold"),
                                           width=18, height=1, border_width=1,
                                           command=exit_from_form, master=app
                                           )
        exit_but.place(relx=.5, rely=.8, anchor="center")

    def game(self):
        count_stones = 0
        count_scissors = 0
        count_papers = 0
        victories = 0
        losses = 0
        draws = 0

        result = customtkinter.CTkLabel(self, text=f"Здравствуйте, {self.player_list[0]}",
                                        font=("Roboto", 43, "bold"), bg_color="#FFF")

        def random_choice():
            return choice([1, 2, 3])

        def for_stone():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_stones += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nНичья"
                count_stones += 1
                draws += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nПобеда"
                count_scissors += 1
                victories += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nПроигрыш"
                count_papers += 1
                losses += 1

        def for_scissors():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_scissors += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nПроигрыш"
                count_stones += 1
                losses += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nНичья"
                count_scissors += 1
                draws += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nПобеда"
                count_papers += 1
                victories += 1

        def for_paper():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_papers += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nПобеда"
                count_stones += 1
                victories += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nПроигрыш"
                count_scissors += 1
                losses += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nНичья"
                count_papers += 1
                draws += 1

        def statistics():
            stat = Tk()
            stat.title("Stat")  # Указание названия
            stat.geometry("400x400+800+250")  # Установка размеров окна
            stat.resizable(False, False)  # Заморозка масштабирования окна
            stat.config(bg="#FFF")  # Установка фонового цвета - белый

            customtkinter.CTkLabel(stat, text=f"Ваша статистика, {self.player_list[0]}", font=("Roboto", 17),
                                   bg_color="#FFF").place(
                relx=.5, rely=.05,
                anchor="center")
            customtkinter.CTkLabel(stat, text=f"""
            # Всего игр: {victories + losses + draws}
            # Побед: {victories}
            # Поражений: {losses}
            # Ничьих: {draws}
        """, font=("Roboto", 11),
                                   bg_color="#FFF",
                                   justify=customtkinter.CENTER,
                                   width=15, height=5
                                   ).place(relx=.5, rely=.19, anchor="center")

            customtkinter.CTkLabel(stat, text="Выкинуто", font=("Roboto", 17), bg_color="#FFF").place(relx=.5,
                                                                                                      rely=.37,
                                                                                                      anchor="center")
            customtkinter.CTkLabel(stat, text=f"""
        # Камней: {count_stones}
        # Ножниц: {count_scissors}
        # Бумаги: {count_papers}
        """, font=("Roboto", 11),
                                   bg_color="#FFF",
                                   justify=customtkinter.CENTER,
                                   width=15, height=3
                                   ).place(relx=.5, rely=.5, anchor="center")

            customtkinter.CTkLabel(stat, text=f"Вы – {self.player_list[3]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(
                relx=.5,
                rely=.65,
                anchor="center")
            customtkinter.CTkLabel(stat, text=f"Ваш любимый предмет – {self.player_list[4]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(relx=.5,
                                                          rely=.73,
                                                          anchor="center")
            customtkinter.CTkLabel(stat, text=f"Ваша почта – {self.player_list[2]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(
                relx=.5, rely=.81,
                anchor="center")

            def save_stat():
                self.update_data()
                mb.showinfo("Информация", "Статистика сохранена")

            customtkinter.CTkButton(stat, text="Cохранить статистику", font=("Roboto", 14), bg="#FFF",
                                    border_width=1,
                                    command=save_stat).place(relx=.5,
                                                             rely=.92,
                                                             anchor="center")

        def rating():
            rating_win = Tk()
            rating_win.title("Рейтинг")  # Указание названия
            rating_win.geometry("400x400+800+250")  # Установка размеров окна
            rating_win.resizable(False, False)  # Заморозка масштабирования окна
            rating_win.config(bg="#FFF")  # Установка фонового цвета - белый

            customtkinter.CTkLabel(rating_win, text="Рейтинг побед", font=("Roboto", 16), bg_color="#FFF").place(
                relx=.5,
                rely=.1,
                anchor="center")

            rating_field = customtkinter.CTkTextbox(rating_win, width=36, border_width=0, height=16,
                                                    font=("Roboto", 15),
                                                    bg="#FFF")
            rating_field.place(relx=.54, rely=.2, anchor="n")

            scroll = customtkinter.CTkScrollbar(rating_win, command=rating_field.yview)
            scroll.pack(side=customtkinter.RIGHT, fill=customtkinter.Y)
            rating_field.config(yscrollcommand=scroll.set)

            file = open('DatabaseForGame.txt')

            rating_dict = {}
            for line in file:
                player_name = line.split('%%')[0]
                player_vict = int(line.split('%%')[8])
                rating_dict[player_name] = player_vict

            sorted_rating = sorted(rating_dict.items(), key=lambda item: item[1], reverse=True)

            for i in range(len(sorted_rating)):
                rating_field.insert(customtkinter.END, f"{i + 1}. {sorted_rating[i][0]}: {sorted_rating[i][1]}\n")

        def exit_to_main():
            if mb.askokcancel("Выход", "Вы действительно хотите выйти в меню?"):
                self.destroy()
                self.log_in()

        customtkinter.CTkButton(self, text="Назад", font=("Roboto", 10, "bold"),
                                width=18, height=1, border_width=1,
                                command=exit_to_main
                                ).place(relx=.02, rely=.02)

        customtkinter.CTkButton(self, text="Камень", font=("Roboto", 14), border_width=1, command=for_stone).place(
            relx=.35,
            rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Ножницы", font=("Roboto", 14), border_width=1,
                                command=for_scissors).place(
            relx=.5, rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Бумага", font=("Roboto", 14), border_width=1, command=for_paper).place(
            relx=.65,
            rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Статистика", font=("Roboto", 14), border_width=1,
                                command=statistics).place(
            relx=.2, rely=.02,
            anchor="center")

        customtkinter.CTkButton(self, text="Рейтинг", font=("Roboto", 14), border_width=1, command=rating).place(
            relx=.8,
            rely=.02,
            anchor="center")

        result.place(relx=.5, rely=.5, anchor="center")

    pass


if __name__ == "__main__":
    app = CustomTkinter()
    app.log_in()
    app.mainloop()
'''

import customtkinter
from CTkMenuBar import *
from tkinter import StringVar
from PIL import Image
from random import randint
import os


class SignIn(customtkinter.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)

        self.exit_from_form = None
        self.sign_in = None
        self.login_event = None
        self.title("Bricks")
        self.geometry("900x600")
        self.resizable(False, False)

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(Image.open(image_path), size=(900, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Hello!",
                                                  font=("Roboto", 32, "bold"))
        self.login_label.grid(row=0, pady=15, sticky="n")
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*",
                                                     placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.mail_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="email")
        self.mail_entry.grid(row=3, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Sign In", command=self.login_event,
                                                    width=100)
        self.login_button.grid(row=4, column=0, pady=(0, 10))
        current_path1 = os.path.dirname(os.path.realpath(__file__))
        image_path1 = os.path.join(current_path1, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(Image.open(image_path1), size=(50, 50))
        self.return_button = customtkinter.CTkButton(self.login_frame, command=self.return_back, width=100)
        self.return_button.grid(row=5, column=0)

        self.exit_button = customtkinter.CTkButton(self.login_frame, text="Exit", width=40, height=30,
                                                   command=self.exit_from_form)
        self.exit_button.grid(row=7, column=0, pady=(200, 0))

    def return_back(self):
        self.Auth = Auth(self)


class BricksApp(customtkinter.CTkToplevel):

    def __init__(self, master=None):
        super().__init__(master)

        self.title("Bricks")
        self.geometry("900x600")
        self.resizable(False, False)

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "background.jpg")
        self.bg_image = customtkinter.CTkImage(Image.open(image_path), size=(900, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # Number of remaining bricks
        self.bricks_label = customtkinter.CTkLabel(master=self, text="Remaining Bricks 🧱:",
                                                   font=customtkinter.CTkFont(size=20, weight="bold"))
        self.bricks_label.grid(row=0, column=0, sticky="N", pady=5)
        self.bricks_amount = randint(12, 20)  # Assuming bricks_amount will be set later
        self.remaining_bricks_var = customtkinter.StringVar(value=str(self.bricks_amount))
        self.remaining_bricks_string = customtkinter.CTkLabel(master=self, textvariable=self.remaining_bricks_var,
                                                              font=customtkinter.CTkFont(size=20, weight="bold"))
        self.remaining_bricks_string.grid(row=0, column=0, sticky="N", pady=40)

        # Frame for human player's turn
        self.human_turn_frame = customtkinter.CTkFrame(master=self)
        self.human_turn_frame.grid(row=0, column=0, sticky="w")

        # Label for human player's turn
        self.human_turn_label = customtkinter.CTkLabel(self.human_turn_frame, text="Your turn:",
                                                       font=customtkinter.CTkFont(size=20, weight="bold"))
        self.human_turn_label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")

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
        self.result_game = customtkinter.CTkLabel(self, font=customtkinter.CTkFont(size=16))
        self.result_game.place(relx=0.5, rely=0.5, anchor="n")

        # Win statistics
        self.win_statistics_count = 0
        self.win_statistics_label = customtkinter.CTkLabel(self, text="Games Won: 0",
                                                           font=customtkinter.CTkFont(size=14))
        self.win_statistics_label.place(relx=0.5, rely=1, anchor="s")

        self.create_menu()

    def create_menu(self):
        menu = CTkTitleMenu(self.master)
        button_1 = menu.add_cascade("Game")

        dropdown1 = CustomDropdownMenu(widget=button_1)
        dropdown1.add_option(option="New game", command=lambda: self.play_again())
        dropdown1.add_option(option="Main menu")
        dropdown1.add_option(option="Statistics")
        dropdown1.add_option(option="Exit", command=lambda: self.exit_the_game())

    def turn(self, amount):
        # Human's turn
        self.bricks_amount = self.bricks_amount - amount
        self.remaining_bricks_var.set(str(self.bricks_amount))

        # Check for game outcomes after human's turn
        if self.bricks_amount == 0:
            # Human wins
            self.win_statistics_count += 1
            self.result_game = customtkinter.CTkLabel(self, text="Вы победили!", fg_color="green")
            self.result_game.place(relx=0.5, rely=0.5, anchor="center")
            self.disable()
        elif self.bricks_amount < 4:
            # Human loses
            self.comp_do_var.set("Взял {0}".format(self.bricks_amount))
            self.bricks_amount = 0
            self.result_game = customtkinter.CTkLabel(self, text="Вы проиграли", fg_color="red")
            self.result_game.place(relx=0.5, rely=0.5, anchor="center")
            self.disable()

        # Update the text for remaining bricks
        self.remaining_bricks_var.set(str(self.bricks_amount))

        # Disable buttons when there are fewer bricks than available for the human to choose
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

            # Disable buttons when there are fewer bricks than available for the human to choose
            if self.bricks_amount == 1:
                self.take_two.configure(state="disabled")
                self.take_three.configure(state="disabled")
            elif self.bricks_amount == 2:
                self.take_three.configure(state="disabled")

            # Check for game outcomes after computer's turn
            if self.bricks_amount == 0:
                # Computer wins
                self.result_game = customtkinter.CTkLabel(self, text="Вы проиграли", fg_color="red")
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

    def exit_the_game(self):
        self.save()
        self.quit()

    def save(self):
        file_save = open('Statistics.txt', 'w')
        file_save.write(f"Games Won: {self.win_statistics_count}")
        file_save.close()


def authenticate(password):
    # Replace this with your actual authentication logic
    # For simplicity, it always returns True for demonstration purposes
    return True


class Auth(customtkinter.CTk):
    width = 900
    height = 600

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SignIn = None
        self.BricksApp = None
        # self.mb = None
        self.title("CustomTkinter Game")
        self.geometry(f"{self.width}x{self.height}")
        self.resizable(False, False)

        # Load and create background image
        current_path = os.path.dirname(os.path.realpath(__file__))
        image_path = os.path.join(current_path, "img", "bg_gradient.jpg")
        self.bg_image = customtkinter.CTkImage(Image.open(image_path), size=(900, 600))
        self.bg_image_label = customtkinter.CTkLabel(self, image=self.bg_image)
        self.bg_image_label.grid(row=0, column=0)

        # create login frame
        self.login_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.login_frame.grid(row=0, column=0, sticky="ns")
        self.login_label = customtkinter.CTkLabel(self.login_frame, text="Hello!",
                                                  font=("Roboto", 32, "bold"))
        self.login_label.grid(row=0, pady=15, sticky="n")
        self.username_entry = customtkinter.CTkEntry(self.login_frame, width=200, placeholder_text="username")
        self.username_entry.grid(row=1, column=0, padx=30, pady=(15, 15))
        self.password_entry = customtkinter.CTkEntry(self.login_frame, width=200, show="*",
                                                     placeholder_text="password")
        self.password_entry.grid(row=2, column=0, padx=30, pady=(0, 15))
        self.login_button = customtkinter.CTkButton(self.login_frame, text="Login", command=self.login_event,
                                                    width=100)
        self.login_button.grid(row=4, column=0, pady=(0, 10))
        self.reg_lab = customtkinter.CTkLabel(self.login_frame, text="Не имеешь аккаунта?",
                                              font=("Roboto", 16, "bold"))
        self.reg_lab.grid(row=5, column=0, pady=(50, 10))
        self.reg_but = customtkinter.CTkButton(self.login_frame, text="Sign In", command=self.open_sign_in_window,
                                               width=75)
        self.reg_but.grid(row=6, column=0)
        self.exit_button = customtkinter.CTkButton(self.login_frame, text="Exit", width=40, height=30,
                                                   command=self.exit_from_form)
        self.exit_button.grid(row=7, column=0, pady=(200, 0))

        # self.gen_lab = customtkinter.CTkLabel(self.login_frame, text="Выберите пол", font=("Roboto", 12, "bold"))
        # self.gen_lab.grid(row=0, column=3)

        # self.gender = customtkinter.StringVar()
        # self.female_rad = customtkinter.CTkRadioButton(self.login_frame, text="Женщина", fg_color="#FFF", value="Женщина",
        #  variable=self.gender)
        # self.female_rad.grid(row=1, column=3, pady=10)
        # self.male_rad = customtkinter.CTkRadioButton(self.login_frame, text="Мужчина", fg_color="#FFF", value="Мужчина",
        # variable=self.gender)
        # self.male_rad.grid(row=2, column=3, pady=10)

        # Создаем список
        # self.age_lab = customtkinter.CTkLabel(self.login_frame, text="Укажите свой диапазон \n возраста",
        # font=("Roboto", 12, "bold"))
        # self.age_lab.grid(row=3, column=3, pady=(20, 20))

        # self.optionmenu_1 = customtkinter.CTkOptionMenu(self.login_frame, dynamic_resizing=False,
        # values=["", "0-18", "18-35", "35+"])
        # self.optionmenu_1.grid(row=4, column=3)

        # self.reg_lab = customtkinter.CTkLabel(self.login_frame, text="Не имеешь аккаунта?",
        # font=("Roboto", 12, "bold"))
        # self.reg_lab.grid(row=10, column=1, sticky="s")

    def login_event(self):
        print("Login pressed - username:", self.username_entry.get(), "password:", self.password_entry.get())

        # Check login credentials (replace this with your actual authentication logic)
        if authenticate(self.username_entry.get() and self.password_entry.get()):

            # Open the BricksApp window upon successful login
            self.BricksApp = BricksApp(self)

        else:
            print("Login failed. Invalid credentials.")

    def open_sign_in_window(self):

        self.SignIn = SignIn(self)

    def exit_from_form(self):
        pass

    def back_event(self):
        self.login_frame.grid(row=0, column=0, sticky="ns")  # show login frame


app = Auth()
app.mainloop()
"""

        count_stones = 0
        count_scissors = 0
        count_papers = 0
        victories = 0
        losses = 0
        draws = 0

        result = customtkinter.CTkLabel(self, text=f"Здравствуйте, {self.player_list[0]}",
                                        font=("Roboto", 43, "bold"), bg_color="#FFF")

        def random_choice():
            return choice([1, 2, 3])

        def for_stone():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_stones += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nНичья"
                count_stones += 1
                draws += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nПобеда"
                count_scissors += 1
                victories += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nПроигрыш"
                count_papers += 1
                losses += 1

        def for_scissors():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_scissors += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nПроигрыш"
                count_stones += 1
                losses += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nНичья"
                count_scissors += 1
                draws += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nПобеда"
                count_papers += 1
                victories += 1

        def for_paper():
            nonlocal count_stones, count_scissors, count_papers, victories, losses, draws
            count_papers += 1
            computer = random_choice()

            if computer == 1:
                result["text"] = "Компьютер выбрал камень – \nПобеда"
                count_stones += 1
                victories += 1

            elif computer == 2:
                result["text"] = "Компьютер выбрал ножницы – \nПроигрыш"
                count_scissors += 1
                losses += 1

            else:
                result["text"] = "Компьютер выбрал бумагу – \nНичья"
                count_papers += 1
                draws += 1

        def statistics():
            stat = Tk()
            stat.title("Stat")  # Указание названия
            stat.geometry("400x400+800+250")  # Установка размеров окна
            stat.resizable(False, False)  # Заморозка масштабирования окна
            stat.config(bg="#FFF")  # Установка фонового цвета - белый

            customtkinter.CTkLabel(stat, text=f"Ваша статистика, {self.player_list[0]}", font=("Roboto", 17),
                                   bg_color="#FFF").place(
                relx=.5, rely=.05,
                anchor="center")
            customtkinter.CTkLabel(stat, text=f
            #Всего игр: {victories + losses + draws}
            #Побед: {victories}
            #Поражений: {losses}
            #Ничьих: {draws}
            , font=("Roboto", 11),
                                   bg_color="#FFF",
                                   justify=customtkinter.CENTER,
                                   width=15, height=5
                                   ).place(relx=.5, rely=.19, anchor="center")

            customtkinter.CTkLabel(stat, text="Выкинуто", font=("Roboto", 17), bg_color="#FFF").place(relx=.5,
                                                                                                      rely=.37,
                                                                                                      anchor="center")
            customtkinter.CTkLabel(stat, text=f
        Камней: {count_stones}
        Ножниц: {count_scissors}
        Бумаги: {count_papers}
        , font=("Roboto", 11),
                                   bg_color="#FFF",
                                   justify=customtkinter.CENTER,
                                   width=15, height=3
                                   ).place(relx=.5, rely=.5, anchor="center")

            customtkinter.CTkLabel(stat, text=f"Вы – {self.player_list[3]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(
                relx=.5,
                rely=.65,
                anchor="center")
            customtkinter.CTkLabel(stat, text=f"Ваш любимый предмет – {self.player_list[4]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(relx=.5,
                                                          rely=.73,
                                                          anchor="center")
            customtkinter.CTkLabel(stat, text=f"Ваша почта – {self.player_list[2]}", font=("Roboto", 14),
                                   bg_color="#FFF").place(
                relx=.5, rely=.81,
                anchor="center")

            def save_stat():
                self.update_data()
                mb.showinfo("Информация", "Статистика сохранена")

            customtkinter.CTkButton(stat, text="Cохранить статистику", font=("Roboto", 14), bg="#FFF",
                                    border_width=1,
                                    command=save_stat).place(relx=.5,
                                                             rely=.92,
                                                             anchor="center")

        def rating():
            rating_win = Tk()
            rating_win.title("Рейтинг")  # Указание названия
            rating_win.geometry("400x400+800+250")  # Установка размеров окна
            rating_win.resizable(False, False)  # Заморозка масштабирования окна
            rating_win.config(bg="#FFF")  # Установка фонового цвета - белый

            customtkinter.CTkLabel(rating_win, text="Рейтинг побед", font=("Roboto", 16), bg_color="#FFF").place(
                relx=.5,
                rely=.1,
                anchor="center")

            rating_field = customtkinter.CTkTextbox(rating_win, width=36, border_width=0, height=16,
                                                    font=("Roboto", 15),
                                                    bg="#FFF")
            rating_field.place(relx=.54, rely=.2, anchor="n")

            scroll = customtkinter.CTkScrollbar(rating_win, command=rating_field.yview)
            scroll.pack(side=customtkinter.RIGHT, fill=customtkinter.Y)
            rating_field.config(yscrollcommand=scroll.set)

            file = open('DatabaseForGame.txt')

            rating_dict = {}
            for line in file:
                player_name = line.split('%%')[0]
                player_vict = int(line.split('%%')[8])
                rating_dict[player_name] = player_vict

            sorted_rating = sorted(rating_dict.items(), key=lambda item: item[1], reverse=True)

            for i in range(len(sorted_rating)):
                rating_field.insert(customtkinter.END, f"{i + 1}. {sorted_rating[i][0]}: {sorted_rating[i][1]}\n")

        def exit_to_main():
            if mb.askokcancel("Выход", "Вы действительно хотите выйти в меню?"):
                self.destroy()
                self.log_in()

        customtkinter.CTkButton(self, text="Назад", font=("Roboto", 10, "bold"),
                                width=18, height=1, border_width=1,
                                command=exit_to_main
                                ).place(relx=.02, rely=.02)

        customtkinter.CTkButton(self, text="Камень", font=("Roboto", 14), border_width=1, command=for_stone).place(
            relx=.35,
            rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Ножницы", font=("Roboto", 14), border_width=1,
                                command=for_scissors).place(
            relx=.5, rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Бумага", font=("Roboto", 14), border_width=1, command=for_paper).place(
            relx=.65,
            rely=.75,
            anchor="center")

        customtkinter.CTkButton(self, text="Статистика", font=("Roboto", 14), border_width=1,
                                command=statistics).place(
            relx=.2, rely=.02,
            anchor="center")

        customtkinter.CTkButton(self, text="Рейтинг", font=("Roboto", 14), border_width=1, command=rating).place(
            relx=.8,
            rely=.02,
            anchor="center")

        result.place(relx=.5, rely=.5, anchor="center")
    pass
        
        



if __name__ == "__main__":
    app = Auth()
    app.mainloop()
"""
