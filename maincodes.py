# import all converted GUI Files
from GUI.index import *
from GUI.login import *
from GUI.signup import *
from GUI.mainWindow import *

# PyQt Package
from PyQt5.QtWidgets import *
import mysql.connector
from mysql.connector import errorcode
import sys

#Database
from database import *

#Database Configuration
DataBaseConfiguration = {"host": "localhost", "user": "root", "password": "admin", "database": "todoListApp"}

users = []
usernames = []
tasks = []
idTask = []

# INDEX WINDOW
class indexWindow(Ui_indexWindow, QMainWindow):
    def __init__(self):
        super(indexWindow, self).__init__()
        self.setupUi(self)

        self.pushButtonIndexLogin.clicked.connect(self.loginWindow)
        self.pushButtonIndexSignup.clicked.connect(self.signupWindow)


    def loginWindow(self):
        index.hide()
        login.show()

    def signupWindow(self):
        index.hide()
        signup.show()

# LOG IN WINDOW
class loginWindow(Ui_loginWindow, QMainWindow):
    def __init__(self):
        super(loginWindow, self).__init__()
        self.setupUi(self)

        self.pushButtonLoginBack.clicked.connect(self.backtoIndex)
        self.pushButtonLoginLogin.clicked.connect(self.loginToMain)

        self.mydb = mysql.connector.connect(**DataBaseConfiguration)
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT username,password FROM users;")
        for logs in mycursor:
            users.append(logs)
        print("Username & Password")
        print(users)


    def loginToMain(self):
        loginUsername = self.lineEditLoginUsername.text()
        loginPassword = self.lineEditLoginPassword.text()
        for x in range(len(users)):
            if users[x][0] == loginUsername and users[x][1] == loginPassword:
                self.lineEditLoginUsername.clear()
                self.lineEditLoginPassword.clear()

                main.labelMainUser.setText(loginUsername)

                login.hide()
                main.show()

                self.mydb = mysql.connector.connect(**DataBaseConfiguration)
                mycursor = self.mydb.cursor()
                sql = "SELECT task FROM tasks WHERE id = %s;"
                mycursor.execute(sql, (loginUsername,))
                data = mycursor.fetchall()

                for task in data:
                    main.listWidgetmainTask.addItems(task)
                    tasks.append(task)
                print("Tasks")
                print(tasks)
                return

        QMessageBox.warning(self, "Login Failed", "<FONT COLOR='#eeeeee'>You entered incorrect Username or Password</FONT>")
        self.lineEditLoginUsername.clear()
        self.lineEditLoginPassword.clear()

    def backtoIndex(self):
        self.lineEditLoginUsername.clear()
        self.lineEditLoginPassword.clear()
        login.hide()
        index.show()

# SIGN UP WINDOW
class signupWindow(Ui_signupWindow, QMainWindow):
    def __init__(self):
        super(signupWindow, self).__init__()
        self.setupUi(self)

        self.mydb = mysql.connector.connect(**DataBaseConfiguration)
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT username FROM users;")
        for username in mycursor:
            usernames.append(username)
        print("Username")
        print(usernames)

        self.pushButtonSignupBack.clicked.connect(self.backtoIndex)
        self.pushButtonSignupSignup.clicked.connect(self.signupToLogin)


    def signupToLogin(self):
        name = self.lineEditSignupName.text()
        username = self.lineEditSignupUsername.text()
        password = self.lineEditSignupPassword.text()
        confirmpassword = self.lineEditSignupConfirmPassword.text()

        for x in range(len(usernames)):
            if usernames[x][0] == username:
                QMessageBox.warning(self, "Signup Failed", "<FONT COLOR='#eeeeee'>The Username you entered is not available.</FONT>")
                self.lineEditSignupUsername.clear()
                self.lineEditSignupPassword.clear()
                self.lineEditSignupConfirmPassword.clear()
                return

        if password != confirmpassword:
            QMessageBox.warning(self, "Signup Failed", "<FONT COLOR='#eeeeee'>The password you entered doesn't match.</FONT>")
            self.lineEditSignupPassword.clear()
            self.lineEditSignupConfirmPassword.clear()
            return

        if name != "" and username != "" and password != "" and confirmpassword != "":
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO users (name,username,password) VALUES (%s,%s,%s);"
            val = (name, username, password)
            mycursor.execute(sql, val)
            self.mydb.commit()

            self.mydb = mysql.connector.connect(**DataBaseConfiguration)
            mycursor = self.mydb.cursor()
            mycursor.execute("SELECT username,password FROM users;")

            users.clear()
            for user in mycursor:
                users.append(user)
            print(users)

            QMessageBox.information(self, "Signup Success",
                                "<FONT COLOR='#eeeeee'>Account created successfully.</FONT>")

            signup.hide()
            login.show()

            self.lineEditSignupName.clear()
            self.lineEditSignupUsername.clear()
            self.lineEditSignupPassword.clear()
            self.lineEditSignupConfirmPassword.clear()
        else:
            QMessageBox.information(self, "Signup Failed", "<FONT COLOR='#eeeeee'>Please fill up all field.</FONT>")

    def backtoIndex(self):
        signup.hide()
        index.show()

#MAIN WINDOW
class mainWindow(Ui_MainWindow, QMainWindow):
    def __init__(self):
        super(mainWindow, self).__init__()
        self.setupUi(self)

        self.mydb = mysql.connector.connect(**DataBaseConfiguration)
        mycursor = self.mydb.cursor()
        mycursor.execute("SELECT id,task FROM tasks;")
        for data in mycursor:
            idTask.append(data)
        print("ID & Task")
        print(idTask)

        self.pushButtonMainCreate.clicked.connect(self.create)
        self.pushButtonMainUpdate.clicked.connect(self.update)
        self.pushButtonMainDelete.clicked.connect(self.delete)
        self.pushButtonMainLogout.clicked.connect(self.logout)

    def create(self):
        currentUser = self.labelMainUser.text()
        task = self.lineEditMainTask.text()
        existdata = self.listWidgetmainTask.findItems(task, QtCore.Qt.MatchExactly)

        if task == "":
            QMessageBox.warning(self, "Task not created", "<FONT COLOR='#eeeeee'>The Task cannot be empty.</FONT>")
            self.lineEditMainTask.clear()

            print("INPUT IS EMPTY")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)
            return

        elif self.listWidgetmainTask.count() == 0:
            self.mydb = mysql.connector.connect(**DataBaseConfiguration)
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO tasks (id,task) VALUES (%s,%s);"
            val = (currentUser, task,)
            mycursor.execute(sql, val)
            self.mydb.commit()

            self.listWidgetmainTask.clear()

            mycursor = self.mydb.cursor()
            sql = "SELECT task FROM tasks WHERE id = %s;"
            mycursor.execute(sql, (currentUser,))
            data = mycursor.fetchall()

            for task in data:
                main.listWidgetmainTask.addItems(task)
                tasks.append(task)

            print("DATA RECORDED")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)

            self.lineEditMainTask.clear()
            QMessageBox.information(self, "Task created","<FONT COLOR='#eeeeee'>The Task was created successfully.</FONT>")
            return

        elif (len(existdata) > 0) == True:
            QMessageBox.warning(self, "Task not created", "<FONT COLOR='#eeeeee'>The task already exist.</FONT>")
            self.lineEditMainTask.clear()

            print("DATA EXIST")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)
            return

        elif (len(existdata) > 0) == False:
            self.mydb = mysql.connector.connect(**DataBaseConfiguration)
            mycursor = self.mydb.cursor()
            sql = "INSERT INTO tasks (id,task) VALUES (%s,%s);"
            val = (currentUser, task,)
            mycursor.execute(sql, val)
            self.mydb.commit()

            self.listWidgetmainTask.clear()

            mycursor = self.mydb.cursor()
            sql = "SELECT task FROM tasks WHERE id = %s;"
            mycursor.execute(sql, (currentUser,))
            data = mycursor.fetchall()

            tasks.clear()

            for task in data:
                main.listWidgetmainTask.addItems(task)
                tasks.append(task)


            print("DATA RECORDED")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)

            self.lineEditMainTask.clear()
            QMessageBox.information(self, "Task created", "<FONT COLOR='#eeeeee'>The Task was created successfully.</FONT>")
            return

    def update(self):
        currentUser = self.labelMainUser.text()
        task = self.lineEditMainTask.text()
        existdata = self.listWidgetmainTask.findItems(task, QtCore.Qt.MatchExactly)
        selectedItem = self.listWidgetmainTask.selectedItems()

        if task == "":
            QMessageBox.warning(self, "Task not updated", "<FONT COLOR='#eeeeee'>The task cannot be empty.</FONT>")
            self.lineEditMainTask.clear()

            print("INPUT IS EMPTY")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)
            return

        elif self.listWidgetmainTask.count() == 0:
            QMessageBox.warning(self, "Task not updated", "<FONT COLOR='#eeeeee'>The list is empty, nothing to update.</FONT>")
            self.lineEditMainTask.clear()
            return

        elif (len(existdata) > 0) == True:
            QMessageBox.warning(self, "Task not created", "<FONT COLOR='#eeeeee'>The task already exist.</FONT>")
            self.lineEditMainTask.clear()

            print("DATA EXIST")
            print("Current ID")
            print(currentUser)
            print("Tasks")
            print(tasks)
            return

        elif (len(existdata) > 0) == False:
            for item in selectedItem:
                itemselected = item.text()
                item.setText(task)
                print(itemselected)
                self.lineEditMainTask.clear()

                self.mydb = mysql.connector.connect(**DataBaseConfiguration)
                mycursor = self.mydb.cursor()
                sql = "UPDATE tasks SET task=%s WHERE task=%s AND id=%s;"
                mycursor.execute(sql, (task, itemselected, currentUser,))
                self.mydb.commit()



                self.listWidgetmainTask.clear()

                mycursor = self.mydb.cursor()
                sql = "SELECT task FROM tasks WHERE id = %s;"
                mycursor.execute(sql, (currentUser,))
                data = mycursor.fetchall()

                tasks.clear()

                for task in data:
                    main.listWidgetmainTask.addItems(task)
                    tasks.append(task)

                print("DATA RECORDED")
                print("Current ID")
                print(currentUser)
                print("Tasks")
                print(tasks)

                self.lineEditMainTask.clear()
                QMessageBox.information(self, "Task Updated", "<FONT COLOR='#eeeeee'>The Task was updated successfully.</FONT>")
                return

    def delete(self):
        print("delete")
        currentUser = self.labelMainUser.text()
        task = self.lineEditMainTask.text()
        selectedItem = self.listWidgetmainTask.selectedItems()

        if self.listWidgetmainTask.count() == 0:
            QMessageBox.warning(self, "Task Empty",
                                "<FONT COLOR='#eeeeee'>The list is empty, nothing to delete.</FONT>")
            self.lineEditMainTask.clear()
            return

        for item in selectedItem:
            itemselected = item.text()
            print(itemselected)
            self.lineEditMainTask.clear()
            answer = QMessageBox.warning(self, 'Delete Task?',
                                          "<FONT COLOR='#eeeeee'>Are you sure you want to Delete selected Task?</FONT>",
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:

                self.mydb = mysql.connector.connect(**DataBaseConfiguration)
                mycursor = self.mydb.cursor()
                sql = "DELETE FROM tasks WHERE task=%s AND id=%s;"
                mycursor.execute(sql, (itemselected, currentUser,))
                self.mydb.commit()

                self.listWidgetmainTask.clear()

                mycursor = self.mydb.cursor()
                sql = "SELECT task FROM tasks WHERE id = %s;"
                mycursor.execute(sql, (currentUser,))
                data = mycursor.fetchall()

                tasks.clear()

                for task in data:
                    main.listWidgetmainTask.addItems(task)
                    tasks.append(task)

                print("DATA RECORDED")
                print("Current ID")
                print(currentUser)
                print("Tasks")
                print(tasks)

                self.lineEditMainTask.clear()
                QMessageBox.information(self, "Task deleted successfully", "<FONT COLOR='#eeeeee'>The task was deleted successfully.</FONT>")
                return

    def logout(self):
        answer = QMessageBox.question(self, 'Log-out', "<FONT COLOR='#eeeeee'>Are you sure you want to Log-out?</FONT>",
                                      QMessageBox.Yes | QMessageBox.No)
        if answer == QMessageBox.Yes:
            tasks.clear()
            self.listWidgetmainTask.clear()
            main.hide()
            index.show()



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    index = indexWindow()
    index.show()

    login = loginWindow()
    login.hide()

    signup = signupWindow()
    signup.hide()

    main = mainWindow()
    main.hide()

    sys.exit(app.exec())
