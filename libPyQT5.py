"""
problem icon :
find source icon that used in qt
open terminal
pyrcc5 -o icons_rc.py icons.qrc
paste source_rc.py next to your project
"""

import datetime
import sqlite3
import sys
import xlrd
import pandas
import xlsxwriter

from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType

FORM_CLASS, _ = loadUiType("libDsQT5.ui")

####################################################
import matplotlib
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg,NavigationToolbar2QT
from matplotlib.figure import Figure

class MplCanvas(FigureCanvasQTAgg):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        super(MplCanvas, self).__init__(fig)

class Window(QMainWindow, FORM_CLASS):
    def __init__(self,*args, **kwargs):
        super(Window, self).__init__(*args, **kwargs)
        QMainWindow.__init__(self)
        self.setupUi(self)

        self.UI_Changes()
        self.Db_Connect()
        self.Handel_Buttons()
        #self.Open_daily_mouvements_Tab()
        self.Open_login_Tab()
        self.show_All_Category()
        self.show_All_Branch()
        self.show_All_Publisher()
        self.show_All_Author()
        self.show_All_Employee()
        self.Show_All_Clients()
        self.Show_All_Books()
        self.retreive_day_work()
        self.show_permission()
        self.Show_History()
        self.Create_Dashboard()
        self.statusBar().showMessage("START APP")

    #################################################
    # login -----------------------------------------
    #################################################
    def UI_Changes(self):
        self.tabWidget.tabBar().setVisible(False)

    ####################################################

    def Db_Connect(self):
        self.db = sqlite3.connect('libDB.db')
        self.cur = self.db.cursor()
        self.statusBar().showMessage("Db is Connected")

    ####################################################

    def Handel_Buttons(self):
        self.pushButton.clicked.connect(self.Open_daily_mouvements_Tab)
        self.pushButton_2.clicked.connect(self.Open_books_Tab)
        self.pushButton_3.clicked.connect(self.Open_clients_Tab)
        self.pushButton_4.clicked.connect(self.Open_dashboard_Tab)
        self.pushButton_6.clicked.connect(self.Open_history_Tab)
        self.pushButton_7.clicked.connect(self.Open_reports_Tab)
        self.pushButton_5.clicked.connect(self.Open_settings_Tab)
        self.pushButton_8.clicked.connect(self.Handel_to_Day_Work)
        self.pushButton_19.clicked.connect(self.Add_Branch)
        self.pushButton_20.clicked.connect(self.Add_Publisher)
        self.pushButton_21.clicked.connect(self.Add_Author)
        self.pushButton_22.clicked.connect(self.Add_Category)
        self.pushButton_44.clicked.connect(self.Add_Employee)
        self.pushButton_10.clicked.connect(self.Add_New_Book)
        self.pushButton_15.clicked.connect(self.Add_New_Client)
        self.pushButton_12.clicked.connect(self.Edit_Book_Search)
        self.pushButton_17.clicked.connect(self.Edit_Client_Search)
        self.pushButton_16.clicked.connect(self.Edit_Client_Save)
        self.pushButton_18.clicked.connect(self.Delete_Client)
        self.pushButton_13.clicked.connect(self.Edit_Book)
        self.pushButton_11.clicked.connect(self.Delete_Book)
        self.pushButton_9.clicked.connect(self.search_book)
        self.pushButton_30.clicked.connect(self.Show_All_Books)
        self.pushButton_47.clicked.connect(self.check_employee)
        self.pushButton_31.clicked.connect(self.clear_edit_employee)
        self.pushButton_46.clicked.connect(self.Edit_Employee_Data)
        self.pushButton_32.clicked.connect(self.clear_add_book)
        self.pushButton_33.clicked.connect(self.clear_edit_book)
        self.pushButton_34.clicked.connect(self.clear_add_client)
        self.pushButton_35.clicked.connect(self.clear_edit_client)
        self.pushButton_48.clicked.connect(self.Add_Employee_Permissions)
        self.pushButton_25.clicked.connect(self.user_login_permission)
        self.pushButton_53.clicked.connect(self.export_books)
        self.pushButton_52.clicked.connect(self.import_books)
        self.pushButton_54.clicked.connect(self.export_clients)
        self.pushButton_55.clicked.connect(self.import_clients)
        self.pushButton_36.clicked.connect(self.Logout)
        self.pushButton_56.clicked.connect(self.Export_History)
        self.pushButton_23.clicked.connect(self.Search_History)
        self.pushButton_37.clicked.connect(self.Show_History)
        self.comboBox_35.currentTextChanged.connect(self.show_permission)

    ####################################################

    def Handel_Login(self):
        pass

    ####################################################

    def Handel_Reset_Passwords(self):
        pass

    ####################################################

    def Handel_to_Day_Work(self):
        book_code = self.lineEdit.text()
        client_id = self.lineEdit_35.text()
        self.cur.execute("""
                        select title from books
                        where code = ?
                        """, (book_code,))
        books = self.cur.fetchone()
        self.cur.execute("""
                        select name from clients
                        where national_id = ?
                        """, (client_id,))
        clients = self.cur.fetchone()
        if books != None and clients != None:
            book_id = self.lineEdit.text()
            client_id = self.lineEdit_35.text()
            type_action = self.comboBox.currentIndex()
            date_from = datetime.date.today()
            date_to = self.dateEdit_3.text()
            date = datetime.datetime.now()
            branch_id = 1
            employee_id = 2
            self.cur.execute("""
            insert into daily_mouvements (book_id,
                                          client_id,
                                          type,
                                          book_from,
                                          book_to,
                                          date,
                                          branch_id,
                                          employee_id)
            values(?,?,?,?,?,?,?,?)
            """,(book_code,
                 client_id,
                 type_action,
                 date_from,
                 date_to,
                 date,
                 branch_id,
                 employee_id))
            self.db.commit()
            self.retreive_day_work()

        else:
            QMessageBox.warning(self, "check", "the book_id or the client_id is not existe")
            self.statusBar().showMessage("the book_id or the client_id is not existe")

    ####################################################

    def retreive_day_work(self):
        self.cur.execute("""
                        select book_id,
                               client_id,
                                type,
                                book_from,
                                book_to
                        from daily_mouvements
                        """)
        data = self.cur.fetchall()
        self.tableWidget.setRowCount(0)
        for row_number, row_data in enumerate(data):
            self.tableWidget.insertRow(row_number)
            for culomn_number, item in enumerate(row_data):
                if culomn_number == 2:
                    if int(item) == 0:
                        self.tableWidget.setItem(row_number, culomn_number, QTableWidgetItem("rent"))
                    if int(item) == 1:
                        self.tableWidget.setItem(row_number, culomn_number, QTableWidgetItem("retrive"))
                elif culomn_number == 0:
                    self.cur.execute("""
                    select title from books
                    where code = ?
                    """,(item,))
                    book = self.cur.fetchone()
                    self.tableWidget.setItem(row_number, culomn_number, QTableWidgetItem(str(book[0])+" , code = "+str(item)))
                elif culomn_number == 1:
                    self.cur.execute("""
                    select name from clients
                    where national_id = ?
                    """,(item,))
                    client = self.cur.fetchone()
                    self.tableWidget.setItem(row_number, culomn_number, QTableWidgetItem(str(client[0])+" , id = "+str(item)))
                else:
                    self.tableWidget.setItem(row_number, culomn_number, QTableWidgetItem(str(item)))
        self.statusBar().showMessage("retreive_day_work done")
    ################################################
    # Books -----------------------------------------
    #################################################
    def Add_New_Book(self):
        book_title = self.lineEdit_3.text()
        book_description = self.textEdit.toPlainText()
        book_category_id = self.comboBox_3.currentIndex()
        book_code = self.lineEdit_5.text()
        book_barcode = self.lineEdit_34.text()
        book_part_order = self.lineEdit_6.text()
        book_price = self.lineEdit_4.text()
        book_publisher_id = self.comboBox_4.currentIndex()
        book_author_id = self.comboBox_5.currentIndex()
        #book_image =
        book_status = self.comboBox_6.currentIndex()
        book_date = datetime.datetime.now()
        if book_code != "" and book_title !="" and book_category_id !=int(-1) and book_publisher_id !=int(-1) and book_author_id !=int(-1) :
            self.cur.execute("""
                INSERT INTO books(title,
                                  description,
                                  category_id,
                                  code,
                                  barcode,
                                  part_order,
                                  price,
                                  publisher_id,
                                  author_id,
                                  status,
                                  date)
                VALUES(?,?,?,?,?,?,?,?,?,?,?)
                """,(book_title,
                  book_description,
                  book_category_id,
                  book_code,
                  book_barcode,
                  book_part_order,
                  book_price,
                  book_publisher_id,
                  book_author_id,
                  book_status,
                  book_date))
            self.db.commit()
            self.Show_All_Books()
            self.statusBar().showMessage("Add_New_Book done")

            # history add books
            name = self.lineEdit_31.text()
            password = self.lineEdit_32.text()
            date = datetime.datetime.now()
            self.cur.execute(
                """
                select national_id,branch
                from employee
                where name=? and password =?
                """, (name, password))
            data = self.cur.fetchone()
            if data != None:
                self.cur.execute("""
                        insert into history(employee_id,
                                            actions,
                                            tables,
                                            branch_id,
                                            date)
                        values(?,?,?,?,?)
                        """, (data[0],
                              "Add",
                              "Books",
                              int(data[1]),
                              date))
                self.db.commit()
                self.Show_History()

            self.clear_add_book()
        elif book_title =="" :
            QMessageBox.warning(self,"warning","the book_title is empty")
            self.statusBar().showMessage("the book_title is empty")
        elif book_description =="" :
            QMessageBox.warning(self,"warning","the book_description is empty")
            self.statusBar().showMessage("the book_description is empty")
        elif book_category_id ==int(-1) :
            QMessageBox.warning(self,"warning","the category is empty")
            self.statusBar().showMessage("the category is empty")
        elif book_publisher_id ==int(-1) :
            QMessageBox.warning(self,"warning","the publisher is empty")
            self.statusBar().showMessage("the publisher is empty")
        elif book_author_id ==int(-1) :
            QMessageBox.warning(self,"warning","the author is empty")
            self.statusBar().showMessage("the author is empty")
        elif book_price =="" :
            QMessageBox.warning(self,"warning","the price is empty if you don't need price now put 0 or none")
            self.statusBar().showMessage("the price is empty if you don't need price now put 0 or none")
        elif book_code == "":
            QMessageBox.warning(self, "warning", "the code is empty")
            self.statusBar().showMessage("the code is empty")

    ####################################################

    def clear_add_book(self):
        self.lineEdit_3.clear()
        self.textEdit.clear()
        self.lineEdit_5.clear()
        self.lineEdit_34.clear()
        self.lineEdit_6.clear()
        self.lineEdit_4.clear()

    ####################################################

    def Show_All_Books(self):
        self.tableWidget_2.setRowCount(0)

        self.cur.execute("""
            SELECT code,
                    title,
                    category_id,
                    price
            FROM books 
        """)
        books = self.cur.fetchall()
        for row , book in enumerate(books):
            self.tableWidget_2.insertRow(row)
            for column , item in enumerate(book):
                if column == 2:
                    self.cur.execute(
                        """
                        select category_name
                        from category
                        where parent_category=?
                        """,(int(item),)
                    )
                    category_name = self.cur.fetchone()
                    self.tableWidget_2.setItem(row, column, QTableWidgetItem(str(category_name[0])+" , id = "+str(item)))

                else:
                    self.tableWidget_2.setItem(row,column,QTableWidgetItem(str(item)))
        self.db.commit()
        self.statusBar().showMessage("Show_All_Books done")

    ####################################################

    def search_book(self):
        book_title = self.lineEdit_2.text()
        category_id = self.comboBox_2.currentIndex()
        self.cur.execute(
            """
            select code ,
                   title,
                   category_id,
                   price
            from books
            where title=? and category_id=?
            """,(book_title,
                 category_id)
        )
        data = self.cur.fetchall()
        if data != None:
            self.tableWidget_2.setRowCount(0)
            for row_number , row_data in enumerate(data):
                self.tableWidget_2.insertRow(row_number)
                for column_number , item in enumerate(row_data):
                    if column_number == 2:
                        self.cur.execute(
                            """
                            select category_name
                            from category
                            where parent_category = ?
                            """,(int(item),)
                        )
                        category = self.cur.fetchone()
                        self.tableWidget_2.setItem(row_number, column_number,
                                                   QTableWidgetItem(str(category[0]) + " , id = " + str(item)))
                        # history edit books
                        name = self.lineEdit_31.text()
                        password = self.lineEdit_32.text()
                        date = datetime.datetime.now()
                        self.cur.execute(
                            """
                            select national_id,branch
                            from employee
                            where name=? and password =?
                            """, (name, password))
                        data = self.cur.fetchone()
                        if data != None:
                            self.cur.execute("""
                            insert into history(employee_id,
                                                actions,
                                                tables,
                                                branch_id,
                                                date)
                            values(?,?,?,?,?)
                            """, (data[0],
                                  "Search",
                                  "Books",
                                  int(data[1]),
                                  date))
                            self.db.commit()
                            self.Show_History()
                    else:
                        self.tableWidget_2.setItem(row_number, column_number, QTableWidgetItem(str(item)))
            self.db.commit()
        else:
            QMessageBox.warning(self,"search","title or category is wrong")
    ####################################################
    def Edit_Book_Search(self):
        self.lineEdit_8.clear()
        self.lineEdit_9.clear()
        self.textEdit_2.clear()
        self.lineEdit_10.clear()
        book_code = self.lineEdit_7.text()
        self.cur.execute("""
            SELECT * 
            FROM books
            WHERE code = ? 
        """,(book_code,))
        data_book = self.cur.fetchone()
        if data_book != None:
                self.lineEdit_8.setText(str(data_book[7]))
                self.lineEdit_9.setText(str(data_book[1]))
                self.textEdit_2.setPlainText(str(data_book[2]))
                self.lineEdit_10.setText(str(data_book[5]))
                if data_book[3] != None:
                    self.comboBox_9.setCurrentIndex(data_book[3])
                if data_book[8] != None:
                    self.comboBox_10.setCurrentIndex(data_book[8])
                if data_book[9] != None:
                    self.comboBox_7.setCurrentIndex(data_book[9])
                if data_book[11] != None:
                    self.comboBox_8.setCurrentIndex(int(data_book[11]))
        else:
            QMessageBox.warning(self,"search","the code is not existe")


        self.db.commit()
        self.statusBar().showMessage("Edit_Book_Search done")

    ####################################################

    def Edit_Book(self):
        book_title = self.lineEdit_9.text()
        book_description = self.textEdit_2.toPlainText()
        book_category_id = self.comboBox_9.currentIndex()
        book_code = self.lineEdit_7.text()
        book_part_order = self.lineEdit_10.text()
        book_price = self.lineEdit_8.text()
        book_publisher_id = self.comboBox_10.currentIndex()
        book_author_id = self.comboBox_7.currentIndex()
        # book_image =
        book_status = self.comboBox_8.currentIndex()
        book_date = datetime.datetime.now()
        self.cur.execute("""
            UPDATE books SET  title=?,
                              description=?,
                              category_id=?,
                              code=?,
                              part_order=?,
                              price=?,
                              publisher_id=?,
                              author_id=?,
                              status=?,
                              date=?
            WHERE code = ?
            """, (book_title,
                  book_description,
                  book_category_id,
                  book_code,
                  str(book_part_order),
                  str(book_price),
                  book_publisher_id,
                  book_author_id,
                  int(book_status),
                  book_date,
                  book_code))
        self.db.commit()
        self.Show_All_Books()
        self.statusBar().showMessage("Edit_Book_Save done")
        # history edit books
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Edit",
                  "Books",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()
        self.clear_edit_book()

    ####################################################

    def clear_edit_book(self):
        book_title = self.lineEdit_9.clear()
        book_description = self.textEdit_2.clear()
        book_code = self.lineEdit_7.clear()
        book_part_order = self.lineEdit_10.clear()
        book_price = self.lineEdit_8.clear()

    ####################################################

    def Delete_Book(self):
        code_book = self.lineEdit_7.text()
        warning=QMessageBox.warning(self,"warning","delete from books where code = {0}".format(code_book),
                            QMessageBox.Yes | QMessageBox.No)
        try:
            if warning==QMessageBox.Yes:
                self.cur.execute("""
                            DELETE FROM books 
                            WHERE code = ?
                        """, (int(code_book),))
                self.db.commit()
                self.statusBar().showMessage("Delete_Book done")
                self.Show_All_Books()
                # history delete books
                name = self.lineEdit_31.text()
                password = self.lineEdit_32.text()
                date = datetime.datetime.now()
                self.cur.execute(
                    """
                    select national_id,branch
                    from employee
                    where name=? and password =?
                    """, (name, password))
                data = self.cur.fetchone()
                if data != None:
                    self.cur.execute("""
                    insert into history(employee_id,
                                        actions,
                                        tables,
                                        branch_id,
                                        date)
                    values(?,?,?,?,?)
                    """, (data[0],
                          "Delete",
                          "Books",
                          int(data[1]),
                          date))
                    self.db.commit()
                    self.Show_History()

            else :
                self.statusBar().showMessage(" the book is not delete")
        except ValueError:
            QMessageBox.warning(self,"warning","the code is empty")
            self.statusBar().showMessage(" the code is empty")

    #################################################
    # client -----------------------------------------
    #################################################
    def Add_New_Client(self):
        client_name = self.lineEdit_12.text()
        client_mail = self.lineEdit_13.text()
        client_phone = self.lineEdit_14.text()
        client_date = datetime.datetime.now()
        client_national_id = self.lineEdit_15.text()
        if client_national_id != "" and client_name != "":
            self.cur.execute("""
                INSERT INTO clients(name,
                                    mail,
                                    phone,
                                    date,
                                    national_id)
                VALUES(?,?,?,?,?)
            """,(client_name,
                client_mail,
                client_phone,
                client_date,
                client_national_id))
            self.db.commit()
            self.statusBar().showMessage("Add_New_Client")
            self.Show_All_Clients()
            self.clear_add_book()
            # history add clients
            name = self.lineEdit_31.text()
            password = self.lineEdit_32.text()
            date = datetime.datetime.now()
            self.cur.execute(
                """
                select national_id,branch
                from employee
                where name=? and password =?
                """, (name, password))
            data = self.cur.fetchone()
            if data != None:
                self.cur.execute("""
                insert into history(employee_id,
                                    actions,
                                    tables,
                                    branch_id,
                                    date)
                values(?,?,?,?,?)
                """, (data[0],
                      "Add",
                      "Clients",
                      int(data[1]),
                      date))
                self.db.commit()
                self.Show_History()

        else:
            QMessageBox.warning(self,"warning","the client id is empty")
            self.statusBar().showMessage("the client id is empty")

    ####################################################

    def clear_add_client(self):
        self.lineEdit_12.clear()
        self.lineEdit_13.clear()
        self.lineEdit_14.clear()
        self.lineEdit_15.clear()

    ####################################################

    def Show_All_Clients(self):
        self.tableWidget_3.setRowCount(0)
        self.comboBox_12.clear()
        self.cur.execute("""
            SELECT name,
                   mail,
                   phone,
                   national_id,
                   date
            FROM clients
        """)
        clients = self.cur.fetchall()
        for client in clients:
            self.comboBox_12.addItem(client[0])
        for row , client in enumerate(clients):
            self.tableWidget_3.insertRow(row)
            for colomn , item in enumerate(client):
                self.tableWidget_3.setItem(row , colomn , QTableWidgetItem(str(item)))
        self.db.commit()
        self.statusBar().showMessage("Show_All_Clients done")
    ####################################################

    def Edit_Client_Search(self):
        self.lineEdit_16.clear()
        self.lineEdit_19.clear()
        self.lineEdit_17.clear()
        self.lineEdit_18.clear()
        data_client = self.lineEdit_20.text()
        list_data_client = self.comboBox_11.currentIndex()
        if list_data_client==0:
            self.cur.execute(
                """
                SELECT *
                FROM clients
                WHERE name = ?
                """,(data_client,)
            )
            client = self.cur.fetchall()
            try:
                if self.lineEdit_20.text() == str(client[0][1]):
                    self.lineEdit_16.setText(str(client[0][1]))
                    self.lineEdit_19.setText(str(client[0][2]))
                    self.lineEdit_17.setText(str(client[0][3]))
                    self.lineEdit_18.setText(str(client[0][5]))
                    self.db.commit()
                    self.statusBar().showMessage("Edit_Client_Search done")
            except IndexError: self.statusBar().showMessage("this "+data_client+" is not name")

        if list_data_client==1:
            self.cur.execute(
                """
                SELECT *
                FROM clients
                WHERE mail = ?
                """, (data_client,)
            )
            client = self.cur.fetchall()
            try:
                if self.lineEdit_20.text() == str(client[0][2]):
                    self.lineEdit_16.setText(str(client[0][1]))
                    self.lineEdit_19.setText(str(client[0][2]))
                    self.lineEdit_17.setText(str(client[0][3]))
                    self.lineEdit_18.setText(str(client[0][5]))
                    self.db.commit()
                    self.statusBar().showMessage("Edit_Client_Search done")
            except IndexError: self.statusBar().showMessage("this "+data_client+" is not mail")

        if list_data_client==2:
            self.cur.execute(
                """
                SELECT *
                FROM clients
                WHERE phone = ?
                """, (data_client,)
            )
            client = self.cur.fetchall()
            try:
                if self.lineEdit_20.text() == str(client[0][3]):
                    self.lineEdit_16.setText(str(client[0][1]))
                    self.lineEdit_19.setText(str(client[0][2]))
                    self.lineEdit_17.setText(str(client[0][3]))
                    self.lineEdit_18.setText(str(client[0][5]))
                    self.db.commit()
                    self.statusBar().showMessage("Edit_Client_Search done")
            except IndexError: self.statusBar().showMessage("this "+data_client+" is not phone")

        if list_data_client==3:
            self.cur.execute(
                """
                SELECT *
                FROM clients
                WHERE national_id = ?
                """, (data_client,)
            )
            client = self.cur.fetchall()
            try:
                if self.lineEdit_20.text() == str(client[0][5]):
                    self.lineEdit_16.setText(str(client[0][1]))
                    self.lineEdit_19.setText(str(client[0][2]))
                    self.lineEdit_17.setText(str(client[0][3]))
                    self.lineEdit_18.setText(str(client[0][5]))
                    self.db.commit()
                    self.statusBar().showMessage("Edit_Client_Search done")
            except IndexError: self.statusBar().showMessage("this "+data_client+" is not national_id")

    ####################################################

    def Edit_Client_Save(self):
        name_client = self.lineEdit_16.text()
        mail_client = self.lineEdit_19.text()
        phone_client = self.lineEdit_17.text()
        national_id_client = self.lineEdit_18.text()
        self.cur.execute("""
            UPDATE clients
            SET name = ?,
                mail = ?,
                phone = ?,
                national_id = ?
            WHERE national_id = ? 
        """,(name_client,
            mail_client,
            phone_client,
            national_id_client,
            int(national_id_client)))
        self.db.commit()
        self.Show_All_Clients()
        self.statusBar().showMessage("Edit_Client_Save done")
        # history edit clients
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Edit",
                  "Clients",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()

        self.clear_edit_client()

    ####################################################

    def clear_edit_client(self):
        self.lineEdit_16.clear()
        self.lineEdit_20.clear()
        self.lineEdit_19.clear()
        self.lineEdit_17.clear()
        self.lineEdit_18.clear()

    ####################################################

    def Delete_Client(self):
        national_id_client = self.lineEdit_18.text()
        warning=QMessageBox.warning(self,"warnnig","delete from books where national_id = {}".format(national_id_client),
                            QMessageBox.Yes | QMessageBox.No)
        if warning==QMessageBox.Yes:
            try :
                self.cur.execute("""
                    DELETE FROM clients 
                    WHERE national_id = ?
                """,(int(national_id_client),))
                self.db.commit()
                self.statusBar().showMessage("Delete_Client done")
                self.Show_All_Clients()
                # history delete clients
                name = self.lineEdit_31.text()
                password = self.lineEdit_32.text()
                date = datetime.datetime.now()
                self.cur.execute(
                    """
                    select national_id,branch
                    from employee
                    where name=? and password =?
                    """, (name, password))
                data = self.cur.fetchone()
                if data != None:
                    self.cur.execute("""
                    insert into history(employee_id,
                                        actions,
                                        tables,
                                        branch_id,
                                        date)
                    values(?,?,?,?,?)
                    """, (data[0],
                          "Delete",
                          "Clients",
                          int(data[1]),
                          date))
                    self.db.commit()
                    self.Show_History()


            except ValueError:
                QMessageBox.warning(self, "warnnig", "national_id is empty")
        if warning==QMessageBox.No:
            self.statusBar().showMessage("the cient is not delete")

    #################################################

    def export_books(self):
        self.cur.execute(
            """
            select code,title,category_id,price
            from books
            """)
        data = self.cur.fetchall()
        excel_file = xlsxwriter.Workbook("books.xlsx") #create file xlsx
        sheet1 = excel_file.add_worksheet() # create new page
        # create table
        sheet1.write(0,0,"code")
        sheet1.write(0,1,"title")
        sheet1.write(0,2,"category_id")
        sheet1.write(0,3,"price")
        for row , row_item in enumerate(data):
            for column , column_item in enumerate(row_item):
                sheet1.write(row+1,column,str(column_item))
        excel_file.close()
        # history export books
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Export",
                  "Books",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()


    def import_books(self):
        excel_file = pandas.read_excel("books.xlsx")
        table = excel_file.values
        for row , row_item in enumerate(table):
            self.cur.execute(
                """
                select code
                from books
                where code=?
                """,(row_item[0],))
            data = self.cur.fetchone()
            if data != None :
                self.cur.execute(
                    """
                    update books
                    set code=?,
                        title=?,
                        category_id=?,
                        price=?
                    where code=?
                    """,(row_item[0],
                         row_item[1],
                         row_item[2],
                         row_item[3],
                         row_item[0]))
                self.db.commit()
                self.statusBar().showMessage("import books done")
            else:
                barcode = "None"
                status = "0"
                publisher_id = None
                author_id = None

                date = datetime.datetime.now()
                self.cur.execute(
                    """
                    insert into books(code,
                                      title,
                                      category_id,
                                      price,
                                      barcode,
                                      status,
                                      date,
                                      publisher_id,
                                      author_id)
                    values(?,?,?,?,?,?,?,?,?)  
                    """,(row_item[0],
                         row_item[1],
                         row_item[2],
                         row_item[3],
                         barcode,
                         status,
                         date,
                         publisher_id,
                         author_id))
            self.db.commit()
            self.statusBar().showMessage("import books done")
        self.Show_All_Books()
        # history import books
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Import",
                  "Books",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()


    #################################################
    def export_clients(self):
        self.cur.execute(
            """
            select name,
                   mail,
                   phone,
                   national_id,
                   date
            from clients
            """)
        data = self.cur.fetchall()
        file_excel = xlsxwriter.Workbook("clients.xlsx")
        sheet1 = file_excel.add_worksheet()
        sheet1.write(0,0,"name")
        sheet1.write(0,1,"mail")
        sheet1.write(0,2,"phone")
        sheet1.write(0,3,"national_id")
        sheet1.write(0,4,"date")
        for row , row_item in enumerate(data):
            for column , column_item in enumerate(row_item):
                sheet1.write(row+1,column,str(column_item))
        file_excel.close()
        # history export clients
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Export",
                  "Clients",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()


    #################################################

    def import_clients(self):
        file_excel = pandas.read_excel("clients.xlsx")
        data_excel = file_excel.values
        for row , row_item in enumerate(data_excel):
            self.cur.execute(
                """
                select national_id
                from clients
                where national_id=?
                """,(int(row_item[3]),)
            )
            data = self.cur.fetchone()
            if data != None :
                self.cur.execute(
                    """
                    update clients
                    set name=?,
                        mail=?,
                        phone=?,
                        national_id=?,
                        date=?
                    where national_id=?
                    """,(row_item[0],
                         row_item[1],
                         row_item[2],
                         int(row_item[3]),
                         row_item[4],
                         int(row_item[3])))
                self.db.commit()
                self.statusBar().showMessage("import clients done")
            else:
                date = datetime.datetime.now()
                self.cur.execute(
                    """
                    insert into clients(name,
                                      mail,
                                      phone,
                                      national_id,
                                      date)
                    values(?,?,?,?,?)  
                    """,(row_item[0],
                         str(row_item[1]),
                         row_item[2],
                         int(row_item[3]),
                         date)
                )
            self.db.commit()
            self.statusBar().showMessage("import client done")
        self.Show_All_Clients()
        # history import client
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Import",
                  "Clients",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()

    #################################################
    # history -----------------------------------------
    #################################################
    def Show_History(self):
        self.cur.execute("""
        select employee_id,
               actions,
               tables,
               branch_id,
               date
        from history
        """,)
        data = self.cur.fetchall()

        self.tableWidget_4.setRowCount(0)
        for row , row_item in enumerate(data):
            self.tableWidget_4.insertRow(row)
            for column , column_item in enumerate(row_item):
                if column==0:
                    self.cur.execute("""
                    select name,national_id,branch
                    from employee
                    where national_id=?
                    """,(int(column_item),))
                    n = self.cur.fetchone()
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(n[0])+", id="+str(n[1])))
                elif column == 3:
                    name_branch= self.comboBox_18.itemText(int(column_item))
                    self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(name_branch)))
                else:
                    self.tableWidget_4.setItem(row,column,QTableWidgetItem(str(column_item)))
        self.db.commit()
    #################################################

    def Export_History(self):
        self.cur.execute("""
        select employee_id,
               actions,
               tables,
               branch_id,
               date
        from history
        """)
        history_data = self.cur.fetchall()
        file_excel = xlsxwriter.Workbook("History.xlsx")
        sheet1 = file_excel.add_worksheet()
        sheet1.write(0,0,"user")
        sheet1.write(0,1,"action")
        sheet1.write(0,2,"table")
        sheet1.write(0,3,"branch")
        sheet1.write(0,4,"date")
        for row , row_item in enumerate(history_data):
            for  column , column_item in  enumerate(row_item):
                if  column==0:
                    self.cur.execute("""
                    select name
                    from employee
                    where national_id=?
                    """,(int(column_item),))
                    user = self.cur.fetchone()
                    sheet1.write(row+1,column,user[0])
                elif column==3:
                    branch = self.comboBox_18.itemText(int(column_item))
                    sheet1.write(row+1,column,branch)
                else:
                    sheet1.write(row+1,column,column_item)
        file_excel.close()
        # history export history
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Export",
                  "History",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()


    #################################################

    def Search_History(self):
        user = self.comboBox_17.currentText()
        action = self.comboBox_14.currentIndex()
        table = self.comboBox_15.currentIndex()
        print()
        self.cur.execute("""
        select name , national_id
        from employee
        where name=?
        """,(user,))
        data_user = self.cur.fetchone()
        if data_user!=None:
            if action==0 and table ==0:
                self.cur.execute("""
                select employee_id,
                       actions,
                       tables,
                       branch_id,
                       date
                from history
                where employee_id=?
                """,(int(data_user[1]),))
                data_histoty = self.cur.fetchall()
                self.tableWidget_4.setRowCount(0)
                for row , items in enumerate(data_histoty):
                    self.tableWidget_4.insertRow(row)
                    for column , item in enumerate(items):
                        if column == 0:
                            self.cur.execute("""
                            select name,national_id,branch
                            from employee
                            where national_id=?
                            """, (int(item),))
                            n = self.cur.fetchone()
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(n[0]) + ", id=" + str(n[1])))
                        elif column == 3:
                            name_branch = self.comboBox_18.itemText(int(item))
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(name_branch)))
                        else:
                            self.tableWidget_4.setItem(row,column,QTableWidgetItem(str(item)))
            elif action !=0 and table ==0:
                self.cur.execute("""
                                select employee_id,
                                       actions,
                                       tables,
                                       branch_id,
                                       date
                                from history
                                where employee_id=? and actions=?
                                """,(int(data_user[1]),
                                    str(self.comboBox_14.currentText())))
                data_histoty = self.cur.fetchall()
                self.tableWidget_4.setRowCount(0)
                for row, items in enumerate(data_histoty):
                    self.tableWidget_4.insertRow(row)
                    for column, item in enumerate(items):
                        if column == 0:
                            self.cur.execute("""
                                            select name,national_id,branch
                                            from employee
                                            where national_id=?
                                            """, (int(item),))
                            n = self.cur.fetchone()
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(n[0]) + ", id=" + str(n[1])))
                        elif column == 3:
                            name_branch = self.comboBox_18.itemText(int(item))
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(name_branch)))
                        else:
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
            elif action ==0 and table !=0:
                self.cur.execute("""
                                select employee_id,
                                       actions,
                                       tables,
                                       branch_id,
                                       date
                                from history
                                where employee_id=? and tables=?
                                """,(int(data_user[1]),
                                    str(self.comboBox_15.currentText())))
                data_histoty = self.cur.fetchall()
                self.tableWidget_4.setRowCount(0)
                for row, items in enumerate(data_histoty):
                    self.tableWidget_4.insertRow(row)
                    for column, item in enumerate(items):
                        if column == 0:
                            self.cur.execute("""
                                            select name,national_id,branch
                                            from employee
                                            where national_id=?
                                            """, (int(item),))
                            n = self.cur.fetchone()
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(n[0]) + ", id=" + str(n[1])))
                        elif column == 3:
                            name_branch = self.comboBox_18.itemText(int(item))
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(name_branch)))
                        else:
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
            elif action !=0 and table !=0:
                self.cur.execute("""
                                select employee_id,
                                       actions,
                                       tables,
                                       branch_id,
                                       date
                                from history
                                where employee_id=? and tables=? and actions=?
                                """,(int(data_user[1]),
                                    str(self.comboBox_15.currentText()),
                                    str(self.comboBox_14.currentText())))
                data_histoty = self.cur.fetchall()
                self.tableWidget_4.setRowCount(0)
                for row, items in enumerate(data_histoty):
                    self.tableWidget_4.insertRow(row)
                    for column, item in enumerate(items):
                        if column == 0:
                            self.cur.execute("""
                                            select name,national_id,branch
                                            from employee
                                            where national_id=?
                                            """, (int(item),))
                            n = self.cur.fetchone()
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(n[0]) + ", id=" + str(n[1])))
                        elif column == 3:
                            name_branch = self.comboBox_18.itemText(int(item))
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(name_branch)))
                        else:
                            self.tableWidget_4.setItem(row, column, QTableWidgetItem(str(item)))
        self.db.commit()
        self.statusBar().showMessage("shearch history done")

    #################################################
    # dashboard -----------------------------------------
    #################################################
    def Create_Dashboard(self):
        sc = MplCanvas(self, width=5, height=4, dpi=100)
        # plot [x],[y]
        sc.axes.plot([], [])

        toolbar = NavigationToolbar2QT(sc, self)
        self.layout = QVBoxLayout()
        self.layout.addWidget(toolbar)
        self.layout.addWidget(sc)
        self.tab_4.setLayout(self.layout)

    #################################################
    # report book -----------------------------------------
    #################################################
    def All_Books_Report(self):
        self.cur.execute(
            """
            select code,
                   title,
                   category_id,
                   author_id,
                   status,
            from books
            """
        )


    ####################################################

    def Books_Filter_Report(self):
        pass

    ####################################################

    def Book_Export_Report(self):
        pass

    #################################################
    # report client -----------------------------------------
    #################################################
    def All_clients_Report(self):
        pass

    ####################################################

    def clients_Filter_Report(self):
        pass

    ####################################################

    def client_Export_Report(self):
        pass

    #################################################
    # Monthly report -----------------------------------------
    #################################################
    def Monthly_Report(self):
        pass

    ####################################################

    def Monthly_Report_Export(self):
        pass

    #################################################
    # data settings ---------------------------------
    #################################################
    def Add_Branch(self):
        branch_name = self.lineEdit_21.text()
        branch_code = self.lineEdit_22.text()
        branch_location = self.lineEdit_23.text()


        if branch_code != "" and branch_name != "":
            self.cur.execute("""
            select code 
            from branch
            where code=?
            """,(int(branch_code),))
            d = self.cur.fetchone()
            if d == None:
                self.cur.execute("""
                    INSERT INTO branch(name,
                                    code,
                                    location) 
                    VALUES (?,?,?)
                    """, (branch_name,
                          branch_code,
                          branch_location))
                self.db.commit()
                self.show_All_Branch()
                self.statusBar().showMessage("Add_Branch done")
                # history add branch
                name = self.lineEdit_31.text()
                password = self.lineEdit_32.text()
                date = datetime.datetime.now()
                self.cur.execute(
                    """
                    select national_id,branch
                    from employee
                    where name=? and password =?
                    """, (name, password))
                data = self.cur.fetchone()
                if data != None:

                    self.cur.execute("""
                            insert into history(employee_id,
                                                actions,
                                                tables,
                                                branch_id,
                                                date)
                            values(?,?,?,?,?)
                            """, (data[0],
                                  "Add",
                                  "Branch",
                                  int(data[1]),
                                   date))
                    self.db.commit()
                    self.Show_History()
                #########
            else:
                QMessageBox.warning(self,"code erorr"," this code is existe ")
        else :
            QMessageBox.warning(self,"warning","the branch name or code is empty")
            self.statusBar().showMessage("the branch name or code is empty")
        self.lineEdit_21.clear()
        self.lineEdit_22.clear()
        self.lineEdit_23.clear()
    ################################################
    def show_All_Branch(self):
        self.comboBox_18.clear()
        self.comboBox_19.clear()
        self.cur.execute("""
            SELECT name FROM branch
        """)
        branches = self.cur.fetchall()
        for branch in branches:
            self.comboBox_18.addItem(branch[0])
            self.comboBox_19.addItem(branch[0])
        self.db.commit()
        self.statusBar().showMessage("show_All_Branch done")



    ####################################################
    def Add_Category(self):
        category_name = self.lineEdit_28.text()
        parent_category_Text = self.comboBox_13.currentText()
        date = datetime.datetime.now()
        if category_name != "":
            if parent_category_Text=="":
                self.cur.execute("""
                            INSERT INTO category(category_name,parent_category) 
                            VALUES (?,?)
                            """, (category_name,0))
                self.db.commit()

            else:
                self.cur.execute("""
                            SELECT id FROM category WHERE category_name=?
                        """, (parent_category_Text,))

                id_parent_category_Text = self.cur.fetchone()
                parent_category = id_parent_category_Text[0]
                self.cur.execute("""
                    INSERT INTO category(category_name,parent_category) 
                    VALUES (?,?)
                    """, (category_name,parent_category))
                self.db.commit()
            self.show_All_Category()
            self.statusBar().showMessage("Add_Category done")
        else :
            QMessageBox.warning(self,"warning","the category name is empty")
            self.statusBar().showMessage("the category name is empty")
        # history add category
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Add",
                  "Category",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()
        self.lineEdit_28.clear()


    ################################################

    def show_All_Category(self):
        self.comboBox_13.clear()
        self.comboBox_2.clear()
        self.comboBox_3.clear()
        self.comboBox_9.clear()
        self.cur.execute("""
        SELECT category_name FROM category
        """)
        categories = self.cur.fetchall()
        for category in categories:
            self.comboBox_13.addItem(category[0])
            self.comboBox_2.addItem(category[0])
            self.comboBox_3.addItem(category[0])
            self.comboBox_9.addItem(category[0])
        self.db.commit()
        self.statusBar().showMessage("show_All_Category done")

    ###################################################

    def Add_Publisher(self):
        publisher_name = self.lineEdit_25.text()
        publisher_location = self.lineEdit_24.text()
        if publisher_name != "":
            self.cur.execute("""
                INSERT INTO publisher(name,
                                location) 
                VALUES (?,?)
                """, (publisher_name,
                      publisher_location))
            self.db.commit()
            self.statusBar().showMessage("Add_Publisher done")
            self.show_All_Publisher()
        else :
            QMessageBox.warning(self,"warning","the publisher name is empty")
            self.statusBar().showMessage("the publisher name is empty")
            # history add publisher
            name = self.lineEdit_31.text()
            password = self.lineEdit_32.text()
            date = datetime.datetime.now()
            self.cur.execute(
                """
                select national_id,branch
                from employee
                where name=? and password =?
                """, (name, password))
            data = self.cur.fetchone()
            if data != None:
                self.cur.execute("""
                    insert into history(employee_id,
                                        actions,
                                        tables,
                                        branch_id,
                                        date)
                    values(?,?,?,?,?)
                    """, (data[0],
                          "Add",
                          "Publisher",
                          int(data[1]),
                          date))
                self.db.commit()
                self.Show_History()

        self.lineEdit_25.clear()
        self.lineEdit_24.clear()

    ################################################

    def show_All_Publisher(self):
        self.comboBox_10.clear()
        self.comboBox_4.clear()
        self.cur.execute("""
            SELECT name FROM publisher
        """)
        publishers = self.cur.fetchall()
        for publisher in publishers:
            self.comboBox_10.addItem(publisher[0])
            self.comboBox_4.addItem(publisher[0])
        self.db.commit()
        self.statusBar().showMessage("show_All_Publisher done")


    #################################################

    def Add_Author(self):
        author_name = self.lineEdit_26.text()
        author_location = self.lineEdit_27.text()
        if author_name != "":
            self.cur.execute("""
                INSERT INTO author(name,
                                location) 
                VALUES (?,?)
                """, (author_name,
                      author_location))
            self.db.commit()
            self.show_All_Author()
            self.statusBar().showMessage("Add_Author done")

        else :
            QMessageBox.warning(self,"warning","the auther name is empty")
            self.statusBar().showMessage("the auther name is empty")
        # history add author
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Add",
                  "Author",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()

        self.lineEdit_26.clear()
        self.lineEdit_27.clear()

    ####################################################

    def show_All_Author(self):
        self.comboBox_7.clear()
        self.comboBox_5.clear()
        self.cur.execute("""
            SELECT name FROM author
        """)
        authors = self.cur.fetchall()
        for author in authors:
            self.comboBox_7.addItem(author[0])
            self.comboBox_5.addItem(author[0])
        self.db.commit()
        self.statusBar().showMessage("show_All_Author done")

    #################################################
    # employees settings ---------------------------------
    #################################################
    def Add_Employee(self):
        employee_name = self.lineEdit_62.text()
        employee_mail = self.lineEdit_64.text()
        employee_phone = self.lineEdit_63.text()
        employee_branch = self.comboBox_18.currentIndex()
        employee_date = datetime.datetime.now()
        employee_id = self.lineEdit_65.text()
        employee_periority = self.lineEdit_80.text()
        employee_password = self.lineEdit_66.text()
        employee_password_again = self.lineEdit_67.text()
        if self.comboBox_18.currentIndex() != (-1):
            if employee_name != "" and employee_id != "" and employee_password != "" and employee_password_again != "":
                if employee_password == employee_password_again:
                    self.cur.execute("""
                            INSERT INTO employee(name,
                                                mail,
                                                phone,
                                                branch,
                                                date,
                                                national_id,
                                                periority,
                                                password)
                            VALUES(?,?,?,?,?,?,?,?)
                            """, (employee_name,
                                  employee_mail,
                                  employee_phone,
                                  employee_branch,
                                  employee_date,
                                  employee_id,
                                  employee_periority,
                                  employee_password))
                    self.db.commit()
                    # history add employee
                    name = self.lineEdit_31.text()
                    password = self.lineEdit_32.text()
                    date = datetime.datetime.now()
                    self.cur.execute(
                        """
                        select national_id,branch
                        from employee
                        where name=? and password =?
                        """, (name, password))
                    data = self.cur.fetchone()
                    if data != None:
                        self.cur.execute("""
                            insert into history(employee_id,
                                                actions,
                                                tables,
                                                branch_id,
                                                date)
                            values(?,?,?,?,?)
                            """, (data[0],
                                  "add",
                                  "Employee",
                                  int(data[1]),
                                  date))
                        self.db.commit()
                        self.Show_History()

                else:
                    self.statusBar().showMessage("wrong password")

                self.show_All_Employee()
                self.statusBar().showMessage("Add_Employee done")
                self.lineEdit_62.clear()
                self.lineEdit_64.clear()
                self.lineEdit_63.clear()
                self.lineEdit_65.clear()
                self.lineEdit_80.clear()
                self.lineEdit_66.clear()
                self.lineEdit_67.clear()

            elif employee_name=='' :
                QMessageBox.warning(self,"warning","the employee name is empty")
                self.statusBar().showMessage("the employee is empty")

            elif employee_id=='' :
                QMessageBox.warning(self,"warning","the employee id is empty")
                self.statusBar().showMessage("the employee id is empty")
            elif employee_password == '':
                QMessageBox.warning(self, "warning", "the employee password is empty")
                self.statusBar().showMessage("the employee password is empty")
            elif employee_password_again == '':
                QMessageBox.warning(self, "warning", "the employee password again is empty")
                self.statusBar().showMessage("the employee password again is empty")
        else:
            QMessageBox.warning(self, "warning", "select branch")

    ################################################

    def show_All_Employee(self):
        self.comboBox_35.clear()
        self.comboBox_17.clear()
        self.cur.execute("""
            SELECT name FROM employee
        """)
        employees = self.cur.fetchall()
        for employee in employees:
            self.comboBox_35.addItem(employee[0])
            self.comboBox_17.addItem(employee[0])
        self.db.commit()
        self.statusBar().showMessage("show_All_Employee done")

    ####################################################

    def Edit_Employee_Data(self):
        name = self.lineEdit_74.text()
        passwd = self.lineEdit_78.text()
        mail = self.lineEdit_76.text()
        phone = self.lineEdit_75.text()
        branch = self.comboBox_19.currentText()
        id = self.lineEdit_77.text()
        periority = self.lineEdit_81.text()
        password = self.lineEdit_79.text()
        message = QMessageBox.warning(self, "edit", "edit employee", QMessageBox.Yes | QMessageBox.No)
        if message == QMessageBox.Yes :
            self.cur.execute(
                """
                update employee
                set mail=?,
                    phone=?,
                    branch=?,
                    periority=?,
                    password=?
                where password=? and name=?
                """,(mail,
                     phone,
                     branch,
                     periority,
                     password,
                     passwd,
                     name)
            )
            self.db.commit()
            # history edit employee
            name = self.lineEdit_31.text()
            password = self.lineEdit_32.text()
            date = datetime.datetime.now()
            self.cur.execute(
                """
                select national_id,branch
                from employee
                where name=? and password =?
                """, (name, password))
            data = self.cur.fetchone()
            if data != None:
                self.cur.execute("""
                insert into history(employee_id,
                                    actions,
                                    tables,
                                    branch_id,
                                    date)
                values(?,?,?,?,?)
                """, (data[0],
                      "Edit",
                      "Employee",
                      int(data[1]),
                      date))
                self.db.commit()
                self.Show_History()

            self.clear_edit_employee()
        else:
            self.clear_edit_employee()

    ################################################

    def check_employee(self):
        employee_name = self.lineEdit_74.text()
        employee_password = self.lineEdit_78.text()
        self.cur.execute(
            """
            select name,
                   password
            from employee
            where name=? and password=?
            """,(employee_name,employee_password)
        )
        employee_data = self.cur.fetchone()

        if employee_data != None:
            QMessageBox.information(self,"check","name and password is correct")
            self.groupBox_7.setEnabled(True)

            self.cur.execute(
                """
                select mail,
                       phone,
                       branch,
                       national_id,
                       periority,
                       password
                from employee
                where name = ? and password = ?
                """,(employee_name,employee_password)
            )
            data = self.cur.fetchone()
            self.lineEdit_76.setText(str(data[0]))
            self.lineEdit_75.setText(str(data[1]))
            self.comboBox_19.setCurrentText(str(data[2]))
            self.lineEdit_77.setText(str(data[3]))
            self.lineEdit_81.setText(str(data[4]))
            self.lineEdit_79.setText(str(data[5]))

        else:
           QMessageBox.warning(self,"warning","name or password is wrong")


    ################################################

    def clear_edit_employee(self):
        if self.groupBox_7.isChecked() == False:
            self.lineEdit_76.clear()
            self.lineEdit_75.clear()
            self.lineEdit_77.clear()
            self.lineEdit_81.clear()
            self.lineEdit_79.clear()
            self.groupBox_7.setEnabled(False)
        if self.groupBox_7.isChecked() != True:
            self.lineEdit_74.clear()
            self.lineEdit_78.clear()

    #################################################
    # permissions settings ---------------------------------
    #################################################

    def Add_Employee_Permissions(self):
        employee_name = self.comboBox_35.currentText()

        # All Tab
        books_tab = 0
        clients_tab = 0
        dashboard_tab = 0
        history_tab = 0
        reports_tab = 0
        settings_tab = 0

        # Books
        add_book = 0
        edit_book = 0
        delete_book = 0
        import_book = 0
        export_book = 0

        # Clients
        add_client = 0
        edit_client = 0
        delete_client = 0
        import_client = 0
        export_client = 0

        # Settings
        add_branch = 0
        add_publisher = 0
        add_auther = 0
        add_category = 0
        add_employee = 0
        edit_employee = 0

        #check name is exicte or not
        self.cur.execute(
            """
            select employee_name from permission
            where employee_name = ?
            """, (employee_name,)
        )
        data = self.cur.fetchone()

        if self.comboBox_35.currentIndex() != int(-1):
            if self.checkBox_19.isChecked()==True:
                if data==None:
                    self.cur.execute(
                        """
                        insert into permission( employee_name,
                                                books_tab,
                                                clients_tab,
                                                dashboard_tab,
                                                history_tab,
                                                reports_tab,
                                                settings_tab,
                                                add_book,
                                                edit_book,
                                                delete_book,
                                                import_book,
                                                export_book,
                                                add_client,
                                                edit_client,
                                                delete_client,
                                                import_client,
                                                export_client,
                                                add_branch,
                                                add_publisher,
                                                add_auther,
                                                add_category,
                                                add_employee,
                                                edit_employee,
                                                is_admin)
                        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """, (employee_name,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1)
                    )
                    self.db.commit()
                    self.statusBar().showMessage("insert permession for ( employee = " + str(employee_name) + " ) as  admin is done")
                if data != None:
                    self.cur.execute(
                        """
                        update permission set   books_tab=?,
                                                clients_tab=?,
                                                dashboard_tab=?,
                                                history_tab=?,
                                                reports_tab=?,
                                                settings_tab=?,
                                                add_book=?,
                                                edit_book=?,
                                                delete_book=?,
                                                import_book=?,
                                                export_book=?,
                                                add_client=?,
                                                edit_client=?,
                                                delete_client=?,
                                                import_client=?,
                                                export_client=?,
                                                add_branch=?,
                                                add_publisher=?,
                                                add_auther=?,
                                                add_category=?,
                                                add_employee=?,
                                                edit_employee=?,
                                                is_admin=?
                        where employee_name=?
                        """, (1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              1,
                              employee_name)
                    )
                    self.db.commit()
                    self.statusBar().showMessage("update permession for ( employee = " + str(employee_name) + " ) as admin is done")

            if self.checkBox_19.isChecked()==False \
                    and(
                        self.checkBox_7.isChecked() == True
                        or self.checkBox_12.isChecked() == True
                        or self.checkBox_8.isChecked() == True
                        or self.checkBox_9.isChecked() == True
                        or self.checkBox_10.isChecked() == True
                        or self.checkBox_11.isChecked() == True
                        # Books
                        or self.checkBox.isChecked() == True
                        or self.checkBox_2.isChecked() == True
                        or self.checkBox_3.isChecked() == True
                        or self.checkBox_25.isChecked() == True
                        or self.checkBox_24.isChecked() == True
                        # Client
                        or self.checkBox_4.isChecked() == True
                        or self.checkBox_5.isChecked() == True
                        or self.checkBox_6.isChecked() == True
                        or self.checkBox_26.isChecked() == True
                        or self.checkBox_27.isChecked() == True
                        # Settings
                        or self.checkBox_17.isChecked() == True
                        or self.checkBox_18.isChecked() == True
                        or self.checkBox_16.isChecked() == True
                        or self.checkBox_21.isChecked() == True
                        or self.checkBox_22.isChecked() == True
                        or self.checkBox_20.isChecked() == True):
                if data==None:
                    # All Tab
                    if self.checkBox_7.isChecked() == True:
                        books_tab = 1
                    if self.checkBox_12.isChecked() == True:
                        clients_tab = 1
                    if self.checkBox_8.isChecked() == True:
                        dashboard_tab = 1
                    if self.checkBox_9.isChecked() == True:
                        history_tab = 1
                    if self.checkBox_10.isChecked() == True:
                        reports_tab = 1
                    if self.checkBox_11.isChecked() == True:
                        settings_tab = 1

                    # Books
                    if self.checkBox.isChecked() == True:
                        add_book = 1
                    if self.checkBox_2.isChecked() == True:
                        edit_book = 1
                    if self.checkBox_3.isChecked() == True:
                        delete_book = 1
                    if self.checkBox_25.isChecked() == True:
                        import_book = 1
                    if self.checkBox_24.isChecked() == True:
                        export_book = 1

                    # Client
                    if self.checkBox_4.isChecked() == True:
                        add_client = 1
                    if self.checkBox_5.isChecked() == True:
                        edit_client = 1
                    if self.checkBox_6.isChecked() == True:
                        delete_client = 1
                    if self.checkBox_26.isChecked() == True:
                        import_client = 1
                    if self.checkBox_27.isChecked() == True:
                        export_client = 1

                    # Settings
                    if self.checkBox_17.isChecked() == True:
                        add_branch = 1
                    if self.checkBox_18.isChecked() == True:
                        add_publisher = 1
                    if self.checkBox_16.isChecked() == True:
                        add_auther = 1
                    if self.checkBox_21.isChecked() == True:
                        add_category = 1
                    if self.checkBox_22.isChecked() == True:
                        add_employee = 1
                    if self.checkBox_20.isChecked() == True:
                        edit_employee = 1

                    self.cur.execute(
                        """
                        insert into permission( employee_name,
                                                books_tab,
                                                clients_tab,
                                                dashboard_tab,
                                                history_tab,
                                                reports_tab,
                                                settings_tab,
                                                add_book,
                                                edit_book,
                                                delete_book,
                                                import_book,
                                                export_book,
                                                add_client,
                                                edit_client,
                                                delete_client,
                                                import_client,
                                                export_client,
                                                add_branch,
                                                add_publisher,
                                                add_auther,
                                                add_category,
                                                add_employee,
                                                edit_employee,
                                                is_admin)
                        values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                        """, (employee_name,
                              books_tab,
                              clients_tab,
                              dashboard_tab,
                              history_tab,
                              reports_tab,
                              settings_tab,
                              add_book,
                              edit_book,
                              delete_book,
                              import_book,
                              export_book,
                              add_client,
                              edit_client,
                              delete_client,
                              import_client,
                              export_client,
                              add_branch,
                              add_publisher,
                              add_auther,
                              add_category,
                              add_employee,
                              edit_employee,
                              0)
                    )
                    self.db.commit()
                    self.statusBar().showMessage("insert permession for ( employee = " + str(employee_name)+" ) is done")

                if data != None :
                    # All Tab
                    if self.checkBox_7.isChecked() == True:
                        books_tab = 1
                    if self.checkBox_12.isChecked() == True:
                        clients_tab = 1
                    if self.checkBox_8.isChecked() == True:
                        dashboard_tab = 1
                    if self.checkBox_9.isChecked() == True:
                        history_tab = 1
                    if self.checkBox_10.isChecked() == True:
                        reports_tab = 1
                    if self.checkBox_11.isChecked() == True:
                        settings_tab = 1

                    # Books
                    if self.checkBox.isChecked() == True:
                        add_book = 1
                    if self.checkBox_2.isChecked() == True:
                        edit_book = 1
                    if self.checkBox_3.isChecked() == True:
                        delete_book = 1
                    if self.checkBox_25.isChecked() == True:
                        import_book = 1
                    if self.checkBox_24.isChecked() == True:
                        export_book = 1

                    # Client
                    if self.checkBox_4.isChecked() == True:
                        add_client = 1
                    if self.checkBox_5.isChecked() == True:
                        edit_client = 1
                    if self.checkBox_6.isChecked() == True:
                        delete_client = 1
                    if self.checkBox_26.isChecked() == True:
                        import_client = 1
                    if self.checkBox_27.isChecked() == True:
                        export_client = 1

                    # Settings
                    if self.checkBox_17.isChecked() == True:
                        add_branch = 1
                    if self.checkBox_18.isChecked() == True:
                        add_publisher = 1
                    if self.checkBox_16.isChecked() == True:
                        add_auther = 1
                    if self.checkBox_21.isChecked() == True:
                        add_category = 1
                    if self.checkBox_22.isChecked() == True:
                        add_employee = 1
                    if self.checkBox_20.isChecked() == True:
                        edit_employee = 1

                    self.cur.execute(
                        """
                        update permission set   books_tab=?,
                                                clients_tab=?,
                                                dashboard_tab=?,
                                                history_tab=?,
                                                reports_tab=?,
                                                settings_tab=?,
                                                add_book=?,
                                                edit_book=?,
                                                delete_book=?,
                                                import_book=?,
                                                export_book=?,
                                                add_client=?,
                                                edit_client=?,
                                                delete_client=?,
                                                import_client=?,
                                                export_client=?,
                                                add_branch=?,
                                                add_publisher=?,
                                                add_auther=?,
                                                add_category=?,
                                                add_employee=?,
                                                edit_employee=?,
                                                is_admin = ?
                        where employee_name=?
                        """, (books_tab,
                              clients_tab,
                              dashboard_tab,
                              history_tab,
                              reports_tab,
                              settings_tab,
                              add_book,
                              edit_book,
                              delete_book,
                              import_book,
                              export_book,
                              add_client,
                              edit_client,
                              delete_client,
                              import_client,
                              export_client,
                              add_branch,
                              add_publisher,
                              add_auther,
                              add_category,
                              add_employee,
                              edit_employee,
                              0,
                              employee_name)
                    )
                    self.db.commit()
                    self.statusBar().showMessage("update permession for ( employee = " + str(employee_name)+" ) is done")
            if self.checkBox_19.isChecked() == False \
                    and self.checkBox_7.isChecked()== False\
                    and self.checkBox_12.isChecked() == False\
                    and self.checkBox_8.isChecked() == False\
                    and self.checkBox_9.isChecked() == False\
                    and self.checkBox_10.isChecked() == False\
                    and self.checkBox_11.isChecked() == False\
                    and self.checkBox.isChecked() == False\
                    and self.checkBox_2.isChecked() == False\
                    and self.checkBox_3.isChecked() == False\
                    and self.checkBox_25.isChecked() == False\
                    and self.checkBox_24.isChecked() == False\
                    and self.checkBox_4.isChecked() == False\
                    and self.checkBox_5.isChecked() == False\
                    and self.checkBox_6.isChecked() == False\
                    and self.checkBox_26.isChecked() == False\
                    and self.checkBox_27.isChecked() == False\
                    and self.checkBox_17.isChecked() == False\
                    and self.checkBox_18.isChecked() == False\
                    and self.checkBox_16.isChecked() == False\
                    and self.checkBox_21.isChecked() == False\
                    and self.checkBox_22.isChecked() == False\
                    and self.checkBox_20.isChecked() == False:
                QMessageBox.warning(self, "warning", "you need to check one permission or chech admin for all permission")
                self.statusBar().showMessage("you need to check one permission or check admin for all permission")

        if self.comboBox_35.currentIndex() == int(-1):
            QMessageBox.warning(self,"warning","the employee name is empty")
            self.statusBar().showMessage("the employee name is empty")
        self.show_permission()
        # history add permission
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Add",
                  "Permission",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()

    #################################################

    def show_permission(self):
        employee_name = self.comboBox_35.currentText()
        self.cur.execute(
            """
            select employee_name from permission
            where employee_name = ?
            """, (employee_name,)
        )
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute(
                """
                select * from permission
                where employee_name = ?
                """, (employee_name,)
            )
            data_all = self.cur.fetchone()

            # all Tab
            if data_all[2] == 1:
                self.checkBox_7.setChecked(True)
            else:
                self.checkBox_7.setChecked(False)
            if data_all[3] == 1:
                self.checkBox_12.setChecked(True)
            else:
                self.checkBox_12.setChecked(False)
            if data_all[4] == 1:
                self.checkBox_8.setChecked(True)
            else:
                self.checkBox_8.setChecked(False)
            if data_all[5] == 1:
                self.checkBox_9.setChecked(True)
            else:
                self.checkBox_9.setChecked(False)
            if data_all[6] == 1:
                self.checkBox_10.setChecked(True)
            else:
                self.checkBox_10.setChecked(False)
            if data_all[7] == 1:
                self.checkBox_11.setChecked(True)
            else:
                self.checkBox_11.setChecked(False)
            # Books
            if data_all[8] == 1:
                self.checkBox.setChecked(True)
            else:
                self.checkBox.setChecked(False)
            if data_all[9] == 1:
                self.checkBox_2.setChecked(True)
            else:
                self.checkBox_2.setChecked(False)
            if data_all[10] == 1:
                self.checkBox_3.setChecked(True)
            else:
                self.checkBox_3.setChecked(False)
            if data_all[11] == 1:
                self.checkBox_25.setChecked(True)
            else:
                self.checkBox_25.setChecked(False)
            if data_all[12] == 1:
                self.checkBox_24.setChecked(True)
            else:
                self.checkBox_24.setChecked(False)
            if data_all[13] == 1:
            # Clients
                self.checkBox_4.setChecked(True)
            else:
                self.checkBox_4.setChecked(False)
            if data_all[14] == 1:
                self.checkBox_5.setChecked(True)
            else:
                self.checkBox_5.setChecked(False)
            if data_all[15] == 1:
                self.checkBox_6.setChecked(True)
            else:
                self.checkBox_6.setChecked(False)
            if data_all[16] == 1:
                self.checkBox_26.setChecked(True)
            else:
                self.checkBox_26.setChecked(False)
            if data_all[17] == 1:
                self.checkBox_27.setChecked(True)
            else:
                self.checkBox_27.setChecked(False)
            # Settings
            if data_all[18] == 1:
                self.checkBox_17.setChecked(True)
            else:
                self.checkBox_17.setChecked(False)
            if data_all[19] == 1:
                self.checkBox_18.setChecked(True)
            else:
                self.checkBox_18.setChecked(False)
            if data_all[20] == 1:
                self.checkBox_16.setChecked(True)
            else:
                self.checkBox_16.setChecked(False)
            if data_all[21] == 1:
                self.checkBox_21.setChecked(True)
            else:
                self.checkBox_21.setChecked(False)
            if data_all[22] == 1:
                self.checkBox_22.setChecked(True)
            else:
                self.checkBox_22.setChecked(False)
            if data_all[23] == 1:
                self.checkBox_20.setChecked(True)
            else:
                self.checkBox_20.setChecked(False)
            # user as admin
            if data_all[24] == 1:
                self.checkBox_19.setChecked(True)
            else:
                # user as admin
                self.checkBox_19.setChecked(False)
        if data == None:
            # user as admin
            self.checkBox_19.setChecked(False)
            # all tab
            self.checkBox_7.setChecked(False)
            self.checkBox_12.setChecked(False)
            self.checkBox_8.setChecked(False)
            self.checkBox_9.setChecked(False)
            self.checkBox_10.setChecked(False)
            self.checkBox_11.setChecked(False)
            # books
            self.checkBox.setChecked(False)
            self.checkBox_2.setChecked(False)
            self.checkBox_3.setChecked(False)
            self.checkBox_25.setChecked(False)
            self.checkBox_24.setChecked(False)
            # clients
            self.checkBox_4.setChecked(False)
            self.checkBox_5.setChecked(False)
            self.checkBox_6.setChecked(False)
            self.checkBox_26.setChecked(False)
            self.checkBox_27.setChecked(False)
            # settings
            self.checkBox_17.setChecked(False)
            self.checkBox_18.setChecked(False)
            self.checkBox_16.setChecked(False)
            self.checkBox_21.setChecked(False)
            self.checkBox_22.setChecked(False)
            self.checkBox_20.setChecked(False)

    #################################################
    def Logout(self):
        # history logout permission
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Logout",
                  "Permission",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()

        self.lineEdit_31.clear()
        self.lineEdit_32.clear()
        self.Open_login_Tab()

    def user_login_permission(self):
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        self.cur.execute(
            """
            select name ,
                   password
            from employee
            where name=? and password =?
            """,(name,password))
        data = self.cur.fetchone()
        if data != None:
            self.Open_daily_mouvements_Tab()
            self.cur.execute(
            """
            select *
            from permission
            where employee_name= ?
            """,(name,))
            data_all = self.cur.fetchone()
            if data_all != None:
                # today
                self.pushButton.setEnabled(True)

                # books
                if data_all[2] == 1:
                    self.pushButton_2.setEnabled(True)
                else:
                    self.pushButton_2.setEnabled(False)
                #client
                if data_all[3] == 1:
                    self.pushButton_3.setEnabled(True)
                else:
                    self.pushButton_3.setEnabled(False)
                # dashboard
                if data_all[4] == 1:
                    self.pushButton_4.setEnabled(True)
                else:
                    self.pushButton_4.setEnabled(False)
                # history
                if data_all[5] == 1:
                    self.pushButton_6.setEnabled(True)
                else:
                    self.pushButton_6.setEnabled(False)
                # reports
                if data_all[6] == 1:
                    self.pushButton_7.setEnabled(True)
                else:
                    self.pushButton_7.setEnabled(False)
                # sittings
                if data_all[7] == 1:
                    self.pushButton_5.setEnabled(True)
                else:
                    self.pushButton_5.setEnabled(False)
                # add book
                if data_all[8] == 1:
                    self.pushButton_10.setEnabled(True)
                else:
                    self.pushButton_10.setEnabled(False)
                # edit book
                if data_all[9] == 1:
                    self.pushButton_13.setEnabled(True)
                else:
                    self.pushButton_13.setEnabled(False)
                # delete book
                if data_all[10] == 1:
                    self.pushButton_11.setEnabled(True)
                else:
                    self.pushButton_11.setEnabled(False)
                # import book
                if data_all[11] == 1:
                    self.pushButton_52.setEnabled(True)
                else:
                    self.pushButton_52.setEnabled(False)
                # export book
                if data_all[12] == 1:
                    self.pushButton_53.setEnabled(True)
                else:
                    self.pushButton_53.setEnabled(False)
                # add client
                if data_all[13] == 1:
                    self.pushButton_15.setEnabled(True)
                else:
                    self.pushButton_15.setEnabled(False)
                # edit client
                if data_all[14] == 1:
                    self.pushButton_16.setEnabled(True)
                else:
                    self.pushButton_16.setEnabled(False)
                # delete client
                if data_all[15] == 1:
                    self.pushButton_18.setEnabled(True)
                else:
                    self.pushButton_18.setEnabled(False)
                # import client
                if data_all[16] == 1:
                    self.pushButton_55.setEnabled(True)
                else:
                    self.pushButton_55.setEnabled(False)
                # export client
                if data_all[17] == 1:
                    self.pushButton_54.setEnabled(True)
                else:
                    self.pushButton_54.setEnabled(False)
                # add branch
                if data_all[18] == 1:
                    self.pushButton_19.setEnabled(True)
                else:
                    self.pushButton_19.setEnabled(False)
                # add publisher
                if data_all[19] == 1:
                    self.pushButton_20.setEnabled(True)
                else:
                    self.pushButton_20.setEnabled(False)
                # add auther
                if data_all[20] == 1:
                    self.pushButton_21.setEnabled(True)
                else:
                    self.pushButton_21.setEnabled(False)
                # add category
                if data_all[21] == 1:
                    self.pushButton_22.setEnabled(True)
                else:
                    self.pushButton_22.setEnabled(False)
                # add employee
                if data_all[22] == 1:
                    self.pushButton_44.setEnabled(True)
                else:
                    self.pushButton_44.setEnabled(False)
                # edit employee
                if data_all[23] == 1:
                    self.pushButton_47.setEnabled(True)
                else:
                    self.pushButton_47.setEnabled(False)
                # admin
                if data_all[24]  == 1:
                    self.disable_buttons(True)
                self.statusBar().showMessage("login successful")
                self.pushButton_36.setEnabled(True)
            else:
                QMessageBox.warning(self, "login", "you down have any permission")
                self.statusBar().showMessage("you down have any permission")
        else :
            QMessageBox.warning(self,"login","login failed name or password is not correct")
            self.statusBar().showMessage("login failed name or password is not correct")
        # history login permission
        name = self.lineEdit_31.text()
        password = self.lineEdit_32.text()
        date = datetime.datetime.now()
        self.cur.execute(
            """
            select national_id,branch
            from employee
            where name=? and password =?
            """, (name, password))
        data = self.cur.fetchone()
        if data != None:
            self.cur.execute("""
            insert into history(employee_id,
                                actions,
                                tables,
                                branch_id,
                                date)
            values(?,?,?,?,?)
            """, (data[0],
                  "Login",
                  "Permission",
                  int(data[1]),
                  date))
            self.db.commit()
            self.Show_History()



    #################################################
    # Admin settings ---------------------------------
    #################################################
    def Admin_Report(self):
        pass
    #################################################
    #################################################
    def Open_login_Tab(self):
        self.tabWidget.setCurrentIndex(0)
        self.disable_buttons(False)

    def disable_buttons(self,status):
        self.pushButton.setEnabled(status)
        self.pushButton_2.setEnabled(status)
        self.pushButton_3.setEnabled(status)
        self.pushButton_4.setEnabled(status)
        self.pushButton_6.setEnabled(status)
        self.pushButton_7.setEnabled(status)
        self.pushButton_5.setEnabled(status)
        self.pushButton_36.setEnabled(status)

    ####################################################

    def Open_reset_password_Tab(self):
        self.tabWidget.setCurrentIndex(1)

    ####################################################

    def Open_daily_mouvements_Tab(self):
        self.tabWidget.setCurrentIndex(2)

    ####################################################

    def Open_books_Tab(self):
        self.tabWidget.setCurrentIndex(3)
        self.tabWidget_2.setCurrentIndex(0)

    ####################################################

    def Open_clients_Tab(self):
        self.tabWidget.setCurrentIndex(4)
        self.tabWidget_3.setCurrentIndex(0)

    ####################################################

    def Open_dashboard_Tab(self):
        self.tabWidget.setCurrentIndex(5)

    ####################################################

    def Open_history_Tab(self):
        self.tabWidget.setCurrentIndex(6)

    ####################################################

    def Open_reports_Tab(self):
        self.tabWidget.setCurrentIndex(7)
        self.tabWidget_5.setCurrentIndex(0)

    ####################################################

    def Open_settings_Tab(self):
        self.tabWidget.setCurrentIndex(8)
        self.tabWidget_4.setCurrentIndex(0)


    ####################################################


if __name__ == '__main__':
    app = QApplication(sys.argv)
    Win = Window()
    Win.show()
    app.exec_()
