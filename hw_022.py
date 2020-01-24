import tkinter as tk
import sqlite3
import tkinter.messagebox


# ###
# #### main window class:
# ###


class MainWin:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Заказ отеля')
        self.root.geometry('550x400')

        self.hotelsListBox = tk.Listbox(self.root, selectmode='single', height=15, width=15, font=('Courier', 18))
        self.hotelsListBox.place(x=10, y=50)

        self.orderButton = tk.Button(text="Заказать номер", width=25, height=3, font=('Courier', 18))
        self.orderButton.place(x=250, y=200)

        self.hotel_info_label = tk.Label(self.root, width=25, height=3, font=('Courier', 18))
        self.hotel_info_label.place(x=240, y=70)

        self.hotelsListBox.bind('<<ListboxSelect>>', self.click_on_hotel)

        results = DataBase().getAllHotels()

        for result in results:
            self.hotelsListBox.insert('end', result)

        self.hotelsListBox.select_set(0) #по умолчанию делаем выбранный первый отель
        self.hotelsListBox.event_generate('<<ListboxSelect>>') #вызываем обработчик нажатия на элемент, после выбора элемента (строчка вышше)

        self.orderButton['command'] = self.b1_click

        self.close_button = tk.Button(self.root, text='Выйти', width=25, height=3, font=('Courier', 18), command=self.root.destroy)
        self.close_button.place(x=250, y=270)

        self.root.mainloop()

    def b1_click(self):
        id = self.hotelsListBox.get(self.hotelsListBox.curselection())[0]
        GuestInfo(id)

    def click_on_hotel(self, e):
        widget = e.widget
        if widget != self.hotelsListBox:
            return
        try:
            index = widget.curselection()[0]
            #print(index)
            hotel = self.hotelsListBox.get(index)
            self.hotel_info_label['text'] = DataBase().show_hotel_info(hotel)
        except IndexError:
            pass


# ###
# #### guest info modal window class:
# ###


class GuestInfo:
    def __init__(self, hotelId):
        self.hotelId = hotelId

        self.root = tk.Tk()
        self.root.title('Заполните форму')
        self.root.geometry('450x400')

        self.root.grab_set()
        self.root.focus_set()

        self.label_surname = tk.Label(self.root, text='введите фамилию:', font=('Courier', 15))
        self.label_surname.place(x=0, y=50)
        self.label_name = tk.Label(self.root, text='введите имя:', font=('Courier', 15))
        self.label_name.place(x=0, y=90)
        self.label_country = tk.Label(self.root, text='ваша страна проживания:', font=('Courier', 15))
        self.label_country.place(x=0, y=130)
        self.label_date = tk.Label(self.root, text='ваша дата рождения:\n формат(yyyy-mm-dd)', font=('Courier', 15))
        self.label_date.place(x=0, y=170)

        self.entry_surname = tk.Entry(self.root)
        self.entry_surname.place(x=220, y=50)
        self.entry_name = tk.Entry(self.root)
        self.entry_name.place(x=220, y=90)
        self.entry_country = tk.Entry(self.root)
        self.entry_country.place(x=220, y=130)
        self.entry_date = tk.Entry(self.root)
        self.entry_date.place(x=220, y=170)

        self.entry_button = tk.Button(self.root, text='Подтвердить', width=15, height=3, font=('Courier', 18))
        self.entry_button.place(x=10, y=240)

        self.close_button = tk.Button(self.root, text='Закрыть', width=15, height=3, font=('Courier', 18), command=self.root.destroy)
        self.close_button.place(x=220, y=240)

        self.entry_button['command'] = self.clickAcceptButton

    def clickAcceptButton(self):
        self.accept()


    def accept(self):
        surname = self.entry_surname.get()
        name = self.entry_name.get()
        country = self.entry_country.get()
        date = self.entry_date.get()


        if len(surname) > 0 and len(name) > 0 and len(country) > 0 and len(date) > 0:
            #print('surname = {}, name = {}, country = {}, date = {}'.format(surname, name, country, date))
            guestId = DataBase().insertDataGuest(surname, name, country, date)

            MakeAnOrder(self.hotelId, guestId)

            self.root.destroy()
        else:
            #print('You should fill all fields.')
            tk.messagebox.showinfo("error", "You should fill all fields!")


# ###
# ####  make an order modal window class:
# ###


class MakeAnOrder:
    def __init__(self, hotelId, guestId):
        self.hotelId = hotelId
        self.guestId = guestId

        self.root = tk.Tk()
        self.root.title('Заполните форму')
        self.root.geometry('450x400')

        self.label_currentDate = tk.Label(self.root, text='текущая дата:\n формат(yyyy-mm-dd)', font=('Courier', 15))
        self.label_currentDate.place(x=0, y=70)
        self.label_arrivalDate = tk.Label(self.root, text='дата поселения:\n формат(yyyy-mm-dd)', font=('Courier', 15))
        self.label_arrivalDate.place(x=0, y=130)
        self.label_days = tk.Label(self.root, text='количество дней\n проживания:', font=('Courier', 15))
        self.label_days.place(x=0, y=190)

        self.entry_currentDate = tk.Entry(self.root)
        self.entry_currentDate.place(x=200, y=70)
        self.entry_arrivalDate = tk.Entry(self.root)
        self.entry_arrivalDate.place(x=200, y=130)
        self.entry_days = tk.Entry(self.root)
        self.entry_days.place(x=200, y=190)

        self.entry_button = tk.Button(self.root, text='Подтвердить', width=15, height=3, font=('Courier', 18))
        self.entry_button.place(x=10, y=260)

        self.entry_button['command'] = self.rec

    def rec(self):
        currentDate = self.entry_currentDate.get() # \/
        arrivalDate = self.entry_arrivalDate.get() # НУЖНО БЫЛО ВЗЯТЬ ТЕКСТ С ПОЛЯ
        days = self.entry_days.get()


        if len(currentDate) > 0 and len(arrivalDate) > 0 and len(days) > 0:
            #print('currentDate = {}, currentDate = {}, days = {}'.format(currentDate, arrivalDate, days))
            DataBase().insertDataOrder(self.guestId, self.hotelId, currentDate, arrivalDate, days)
            self.root.destroy()
        else:
            #print('You should fill all fields.')
            tk.messagebox.showinfo("error", "You should fill all fields!")


# ###
# #### database class:
# ###


class DataBase:
    def __init__(self):
        self.database = 'Hotels.db'
        self.hotelsQuery = 'select * from Отели;'
        self.hotelsQueryByName = """
                SELECT код, название
                FROM Отели
                ORDER BY 1;
                """

    def getAllHotels(self):
        return self.get_results(self.hotelsQueryByName)

    def insertDataGuest(self, surname, name, country, birsdaydate):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Гости('фамилия', 'имя', 'страна', 'дата_рождения') VALUES(?, ?, ?, ?);"

            cursor.execute(query, (surname, name, country, birsdaydate))
            connection.commit()
            return cursor.lastrowid

    def insertDataOrder(self, guestId, hotelId, currentDate, arrivalDate, days):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            query = "INSERT INTO Заказы('дата', 'код_гостя', 'код_отеля', 'дата_поселения', 'количество_дней_проживания') VALUES(?, ?, ?, ?, ?);"

            cursor.execute(query,(currentDate, guestId, hotelId , arrivalDate, days))
            connection.commit()

    def get_results(self, query, attr=None):
        with sqlite3.connect(self.database) as connection:
            cursor = connection.cursor()
            if attr:
                cursor.execute(query, attr)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            return results

    def show_hotel_info(self, hotel):
        #print(hotel)
        query3 = """
                SELECT * FROM Отели
                WHERE название = ?
                """
        results = self.get_results(query3, (hotel[1],))
        #print(results)
        stars = results[0][2]
        numbers = results[0][3]
        price = results[0][4]
        return f'\'{stars}\'звезд(ы)\n кол-во номеров: {numbers}\n цена: {price}'


mw = MainWin()




