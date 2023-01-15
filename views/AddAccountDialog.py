from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QComboBox, QDialog, QPushButton, QTextEdit


class AddAccountDialog(QDialog):
    def __init__(self, controller):
        super(AddAccountDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_email = QLineEdit()
        self.edit_pass = QLineEdit()
        self.combo_account = QComboBox()
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton()

        self.account_types = []
        self.account_type_ids = []

        self.uis = [self.edit_email, self.edit_pass]

        self._ui()

    def refactor(self):
        for ui in self.uis:
            ui.setText("")

        # we do not want to include text_details variable, so we make it separated
        self.text_details.setText("")

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        cursor = self.model.conn.cursor()
        cursor.execute("SELECT * FROM account_types")
        data = cursor.fetchall()

        for _, datum in data:
            self.account_type_ids.append(_)
            self.account_types.append(datum)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_account)

        self.edit_email.setPlaceholderText("xxx@gmail.com")
        self.edit_pass.setPlaceholderText("*****")
        self.text_details.setPlaceholderText("Buraya yazın...")

        for account_type in self.account_types:
            self.combo_account.addItem(account_type)

        self.formLayout.addRow("Email Adresi : ", self.edit_email)
        self.formLayout.addRow("Şifre : ", self.edit_pass)
        self.formLayout.addRow("Hesap Tipi : ", self.combo_account)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)

