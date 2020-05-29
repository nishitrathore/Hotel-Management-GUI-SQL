import sys,sqlite3,time
from PyQt5 import QtGui
from PyQt5.QtWidgets import QTableWidgetItem,QTableWidget,QComboBox,QVBoxLayout,QGridLayout,QDialog,QWidget, QPushButton, QApplication, QMainWindow,QAction,QMessageBox,QLabel,QTextEdit,QProgressBar,QLineEdit
from PyQt5.QtCore import QCoreApplication

class DBHelper():
    def __init__(self):
        self.conn=sqlite3.connect("hotel.db")
        self.c=self.conn.cursor()
        self.c.execute("CREATE TABLE IF NOT EXISTS employee(ID INTEGER,name TEXT,gender INTEGER,work INTEGER,status INTEGER,status_employed INTEGER,address TEXT,mobile INTEGER)")
        self.c.execute("CREATE TABLE IF NOT EXISTS salary(reciept_no INTEGER,ID INTEGER,fee INTEGER,transfer INTEGER,reciept_date TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS genders(id INTEGER,name TEXT)")
        self.c.execute("CREATE TABLE IF NOT EXISTS workes(id INTEGER,name TEXT)")
    def AddEmployee(self,ID,name,gender,work,status,status_employed,address,mobile):
        try:
            self.c.execute("INSERT INTO employee (ID,name,gender,work,status,status_employed,address,mobile) VALUES (?,?,?,?,?,?,?,?)",(ID,name,gender,work,status,status_employed,address,mobile))
            self.conn.commit()
            self.c.close()
            self.conn.close()
            QMessageBox.information(QMessageBox(),'Successful','EMPLOYEE is added.')
        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add EMPLOYEE!!!.')

    def searchStudent(self,ID):
        self.c.execute("SELECT * from employee WHERE ID="+str(ID))
        self.data=self.c.fetchone()

        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any student with ID no '+str(ID))
            return None
        self.list=[]
        for i in range(0,8):
            self.list.append(self.data[i])
        self.c.close()
        self.conn.close()
        display_employee(self.list)


    def addPayment(self,ID,fee,transfer):
        reciept_no=int(time.time())
        date=time.strftime("%b %d %Y %H:%M:%S")
        try:
            self.c.execute("INSERT INTO salary (reciept_no,ID,fee,transfer,reciept_date) VALUES (?,?,?,?,?)",(reciept_no, ID, fee, transfer, date))
            self.conn.commit()
            QMessageBox.information(QMessageBox(), 'Successful',
                                            'Payment is added successfully to the database.\nReference ID=' + str(
                                                reciept_no))

        except Exception:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not add payment to the database.')

        self.c.close()
        self.conn.close()

    def searchPayment(self,ID):
        self.c.execute("SELECT * from salary WHERE ID="+str(ID)+" ORDER BY reciept_no DESC")
        self.data=self.c.fetchone()
        if not self.data:
            QMessageBox.warning(QMessageBox(), 'Error', 'Could not find any student with ID no '+str(ID))
            return None
        self.list=self.data
        self.c.close()
        self.conn.close()
        showPaymentFunction(self.list)

class Login(QDialog):
    def __init__(self, parent=None):
        super(Login, self).__init__(parent)
        self.userNameLabel=QLabel("Username")
        self.userPassLabel=QLabel("Password")
        self.textName = QLineEdit(self)
        self.textPass = QLineEdit(self)
        self.buttonLogin = QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handleLogin)
        layout = QGridLayout(self)
        layout.addWidget(self.userNameLabel, 1, 1)
        layout.addWidget(self.userPassLabel, 2, 1)
        layout.addWidget(self.textName,1,2)
        layout.addWidget(self.textPass,2,2)
        layout.addWidget(self.buttonLogin,3,1,1,2)

        self.setWindowTitle("Hotel Login")


    def handleLogin(self):
        if (self.textName.text() == '' and
            self.textPass.text() == ''):
            self.accept()
        else:
            QMessageBox.warning(
                self, 'Error', 'Bad user or password')

def display_employee(list):
        ID=0
        gender = ""
        work = ""
        status = ""
        name = ""
        address = ""
        mobile = -1
        status_employed = -1

        ID=list[0]
        name=list[1]

        if list[2]==0:
            gender="Male"
        else:
            gender="Female"

        if list[3]==0:
            work="Chef"
        elif list[3]==1:
            work="Manager"
        elif list[3]==2:
            work="Waiter"
        elif list[3]==3:
            work="Cleaning Staff"


        if list[4]==0:
            status="married"
        elif list[4]==1:
            status="unmarried"
        elif list[4]==2:
            status="single"
        elif list[4]==3:
            status="other"

        status_employed=list[5]
        address=list[6]
        mobile=list[7]

        table=QTableWidget()
        tableItem=QTableWidgetItem()
        table.setWindowTitle("Employee Details")
        table.setRowCount(8)
        table.setColumnCount(2)

        table.setItem(0, 0, QTableWidgetItem("ID"))
        table.setItem(0, 1, QTableWidgetItem(str(ID)))
        table.setItem(1, 0, QTableWidgetItem("Name"))
        table.setItem(1, 1, QTableWidgetItem(str(name)))
        table.setItem(2, 0, QTableWidgetItem("Gender"))
        table.setItem(2, 1, QTableWidgetItem(str(gender)))
        table.setItem(3, 0, QTableWidgetItem("work"))
        table.setItem(3, 1, QTableWidgetItem(str(work)))
        table.setItem(4, 0, QTableWidgetItem("status"))
        table.setItem(4, 1, QTableWidgetItem(str(status)))
        table.setItem(5, 0, QTableWidgetItem("Employed status"))
        table.setItem(5, 1, QTableWidgetItem(str(status_employed)))
        table.setItem(6, 0, QTableWidgetItem("Address"))
        table.setItem(6, 1, QTableWidgetItem(str(address)))
        table.setItem(7, 0, QTableWidgetItem("Mobile"))
        table.setItem(7, 1, QTableWidgetItem(str(mobile)))
        table.horizontalHeader().setStretchLastSection(True)
        table.show()
        dialog=QDialog()
        dialog.setWindowTitle("Student Details")
        dialog.resize(500,300)
        dialog.setLayout(QVBoxLayout())
        dialog.layout().addWidget(table)
        dialog.exec()

def showPaymentFunction(list):
    ID = -1
    recipt_no = -1
    fee = -1
    transfer = -1
    recipt_date = ""

    recipt_no = list[0]
    ID = list[1]
    fee = list[2]
    if list[3] == 0:
        transfer = "card"
    elif list[3]==1:
        transfer = "cash"
    recipt_date=list[4]

    table = QTableWidget()
    tableItem = QTableWidgetItem()
    table.setWindowTitle("Employee Payment Details")
    table.setRowCount(5)
    table.setColumnCount(2)

    table.setItem(0, 0, QTableWidgetItem("Receipt No"))
    table.setItem(0, 1, QTableWidgetItem(str(recipt_no)))
    table.setItem(1, 0, QTableWidgetItem("ID"))
    table.setItem(1, 1, QTableWidgetItem(str(ID)))
    table.setItem(2, 0, QTableWidgetItem("Salary Fee"))
    table.setItem(2, 1, QTableWidgetItem(str(fee)))
    table.setItem(3, 0, QTableWidgetItem("Transfer"))
    table.setItem(3, 1, QTableWidgetItem(str(transfer)))
    table.setItem(4, 0, QTableWidgetItem("Receipt Date"))
    table.setItem(4, 1, QTableWidgetItem(str(recipt_date)))

    table.horizontalHeader().setStretchLastSection(True)
    table.show()
    dialog = QDialog()
    dialog.setWindowTitle("Employee Payment Details")
    dialog.resize(500, 300)
    dialog.setLayout(QVBoxLayout())
    dialog.layout().addWidget(table)
    dialog.exec()
    
class AddEmployee(QDialog):
    def __init__(self):
        super().__init__()

        self.gender=-1
        self.work=-1
        self.status=-1
        self.ID=-1
        self.name=""
        self.address=""
        self.mobile=-1
        self.status_employed=-1


        self.btnCancel=QPushButton("Cancel",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.statusCombo=QComboBox(self)
        self.statusCombo.addItem("married")
        self.statusCombo.addItem("unmarried")
        self.statusCombo.addItem("single")
        self.statusCombo.addItem("other")

        self.genderCombo = QComboBox(self)
        self.genderCombo.addItem("Male")
        self.genderCombo.addItem("Female")

        self.workCombo = QComboBox(self)
        self.workCombo.addItem("Chef")
        self.workCombo.addItem("Manager")
        self.workCombo.addItem("Waiter")
        self.workCombo.addItem("Cleaning Staff")

        self.IDLabel=QLabel("ID No")
        self.nameLabel=QLabel("Name")
        self.addressLabel = QLabel("Address")
        self.mobLabel = QLabel("Mobile")
        self.statusLabel = QLabel("Current status")
        self.statusEmployedLabel = QLabel("Year Employed")
        self.workLabel = QLabel("Work")
        self.genderLabel=QLabel("Gender")

        self.IDText=QLineEdit(self)
        self.nameText=QLineEdit(self)
        self.addressText = QLineEdit(self)
        self.mobText = QLineEdit(self)
        self.statusText = QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.IDLabel,1,1)
        self.grid.addWidget(self.nameLabel,2,1)
        self.grid.addWidget(self.genderLabel, 3, 1)
        self.grid.addWidget(self.addressLabel, 4, 1)
        self.grid.addWidget(self.mobLabel, 5, 1)
        self.grid.addWidget(self.workLabel, 6, 1)
        self.grid.addWidget(self.statusLabel,7,1)
        self.grid.addWidget(self.statusEmployedLabel, 8, 1)

        self.grid.addWidget(self.IDText,1,2)
        self.grid.addWidget(self.nameText,2,2)
        self.grid.addWidget(self.genderCombo, 3, 2)
        self.grid.addWidget(self.addressText, 4, 2)
        self.grid.addWidget(self.mobText, 5, 2)
        self.grid.addWidget(self.workCombo, 6, 2)
        self.grid.addWidget(self.statusCombo,7,2)
        self.grid.addWidget(self.statusText, 8, 2)

        self.grid.addWidget(self.btnCancel,9,3)
        self.grid.addWidget(self.btnAdd,9,1)

        self.btnAdd.clicked.connect(self.AddEmployee)
        self.btnCancel.clicked.connect(QApplication.instance().quit)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Employee Details")
        self.resize(500,300)
        self.show()
        sys.exit(self.exec())

    def reset(self):
        self.IDText.setText("")
        self.statusText.setText("")
        self.nameText.setText("")
        self.addressText.setText("")
        self.mobText.setText("")

    def AddEmployee(self):
        self.gender=self.genderCombo.currentIndex()
        self.status=self.statusCombo.currentIndex()
        self.work=self.workCombo.currentIndex()
        self.ID=int(self.IDText.text())
        self.name=self.nameText.text()
        self.status_employed=int(self.statusText.text())
        self.address=self.addressText.text()
        self.mobile=int(self.mobText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.AddEmployee(self.ID,self.name,self.gender,self.work,self.status,self.status_employed,self.address,self.mobile)

class AddPayment(QDialog):
    def __init__(self):
        super().__init__()

        self.reciept_no=-1
        self.ID=-1
        self.fee=-1
        self.transfer=-1
        self.date=-1

        self.btnCancel=QPushButton("Cancel",self)
        self.btnAdd=QPushButton("Add",self)

        self.btnCancel.setFixedHeight(30)
        self.btnAdd.setFixedHeight(30)

        self.transferCombo = QComboBox(self)
        self.transferCombo.addItem("card")
        self.transferCombo.addItem("cash")

        self.IDLabel=QLabel("ID No")
        self.feeLabel=QLabel("Total Salary")
        self.transferLabel = QLabel("Transfer")

        self.IDText=QLineEdit(self)
        self.feeLabelText=QLineEdit(self)

        self.grid=QGridLayout(self)
        self.grid.addWidget(self.IDLabel,1,1)
        self.grid.addWidget(self.feeLabel,2,1)
        self.grid.addWidget(self.transferLabel, 3, 1)

        self.grid.addWidget(self.IDText,1,2)
        self.grid.addWidget(self.feeLabelText,2,2)
        self.grid.addWidget(self.transferCombo, 3, 2)

        self.grid.addWidget(self.btnCancel,4,3)
        self.grid.addWidget(self.btnAdd,4,1)

        self.btnAdd.clicked.connect(self.addPayment)
        self.btnCancel.clicked.connect(QApplication.instance().quit)

        self.setLayout(self.grid)
        self.setWindowTitle("Add Salary Details")
        self.resize(400,200)
        self.show()
        sys.exit(self.exec())
    def reset(self):
        self.IDText.setText("")
        self.feeLabelText.setText("")

    def addPayment(self):
        self.transfer=self.transferCombo.currentIndex()
        self.ID=int(self.IDText.text())
        self.fee=int(self.feeLabelText.text())

        self.dbhelper=DBHelper()
        self.dbhelper.addPayment(self.ID,self.fee,self.transfer)

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.IDToBeSearched=0
        self.vbox = QVBoxLayout()
        self.text = QLabel("Enter the ID no of the employee")
        self.editField = QLineEdit()
        self.btnSearch = QPushButton("Search", self)
        self.btnSearch.clicked.connect(self.display_employee)
        self.vbox.addWidget(self.text)
        self.vbox.addWidget(self.editField)
        self.vbox.addWidget(self.btnSearch)
        self.dialog = QDialog()
        self.dialog.setWindowTitle("Enter ID No")
        self.dialog.setLayout(self.vbox)

        self.IDForPayment = 0
        self.vboxPayment = QVBoxLayout()
        self.textPayment = QLabel("Enter the ID no of the employee")
        self.editFieldPayment = QLineEdit()
        self.btnSearchPayment = QPushButton("Search", self)
        self.btnSearchPayment.clicked.connect(self.display_employeePayment)
        self.vboxPayment.addWidget(self.textPayment)
        self.vboxPayment.addWidget(self.editFieldPayment)
        self.vboxPayment.addWidget(self.btnSearchPayment)
        self.dialogPayment = QDialog()
        self.dialogPayment.setWindowTitle("Enter ID No")
        self.dialogPayment.setLayout(self.vboxPayment)

        self.Enter_employee=QPushButton("ADD Employee ",self)
        self.btnEnterPayment=QPushButton("ADD Salary",self)
        self.btndisplay_employeeDetails=QPushButton("Show Employee",self)
        self.btnShowPaymentDetails=QPushButton("Show Salary",self)

        self.picLabel=QLabel(self)
        self.picLabel.resize(150,150)
        self.picLabel.move(120,20)
        self.picLabel.setScaledContents(True)
        self.picLabel.setPixmap(QtGui.QPixmap("staff.jpg"))

        self.Enter_employee.move(120,170)
        self.Enter_employee.resize(180,40)
        self.Enter_employeeFont=self.Enter_employee.font()
        self.Enter_employeeFont.setPointSize(13)
        self.Enter_employee.setFont(self.Enter_employeeFont)
        self.Enter_employee.clicked.connect(self.enterstudent)

        self.btnEnterPayment.move(120,200)
        self.btnEnterPayment.resize(180, 40)
        self.btnEnterPaymentFont = self.Enter_employee.font()
        self.btnEnterPaymentFont.setPointSize(13)
        self.btnEnterPayment.setFont(self.btnEnterPaymentFont)
        self.btnEnterPayment.clicked.connect(self.enterpayment)

        self.btndisplay_employeeDetails.move(120, 230)
        self.btndisplay_employeeDetails.resize(180, 40)
        self.btndisplay_employeeDetailsFont = self.Enter_employee.font()
        self.btndisplay_employeeDetailsFont.setPointSize(13)
        self.btndisplay_employeeDetails.setFont(self.btndisplay_employeeDetailsFont)
        self.btndisplay_employeeDetails.clicked.connect(self.display_employeeDialog)

        self.btnShowPaymentDetails.move(120, 260)
        self.btnShowPaymentDetails.resize(180, 40)
        self.btnShowPaymentDetailsFont = self.Enter_employee.font()
        self.btnShowPaymentDetailsFont.setPointSize(13)
        self.btnShowPaymentDetails.setFont(self.btnShowPaymentDetailsFont)
        self.btnShowPaymentDetails.clicked.connect(self.display_employeePaymentDialog)

        self.resize(400,400)
        self.setWindowTitle("Hotel Database Management System")

    def enterstudent(self):
        enterStudent=AddEmployee()
    def enterpayment(self):
        enterpayment=AddPayment()
    def display_employeeDialog(self):
        self.dialog.exec()
    def display_employeePaymentDialog(self):
        self.dialogPayment.exec()
    def display_employee(self):
        if self.editField.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the ID number to show the results for.')
            return None
        display_employee = DBHelper()
        display_employee.searchStudent(int(self.editField.text()))
    def display_employeePayment(self):
        if self.editFieldPayment.text() is "":
            QMessageBox.warning(QMessageBox(), 'Error',
                                'You must give the ID number to show the results for.')
            return None
        display_employee = DBHelper()
        display_employee.searchPayment(int(self.editFieldPayment.text()))
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    login = Login()

    if login.exec_() == QDialog.Accepted:
        window = Window()
        window.show()
    sys.exit(app.exec_())