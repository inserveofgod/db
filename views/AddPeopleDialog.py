from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit, QCheckBox


class AddPeopleDialog(QDialog):
    def __init__(self, controller):
        super(AddPeopleDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_name = QLineEdit()
        self.edit_surname = QLineEdit()
        self.edit_phone = QLineEdit()
        self.edit_mother_name = QLineEdit()
        self.edit_father_name = QLineEdit()
        self.edit_job = QLineEdit()
        self.edit_workplace = QLineEdit()
        self.edit_loc = QLineEdit()
        self.check_married = QCheckBox("Evet")
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.uis = [self.edit_name, self.edit_surname, self.edit_phone, self.edit_mother_name, self.edit_father_name,
                    self.edit_job, self.edit_workplace, self.edit_loc]

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

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_people)

        self.edit_phone.setPlaceholderText("+90.(000).000.00.00")
        self.edit_job.setPlaceholderText("x meslek")
        self.edit_workplace.setPlaceholderText("x mekan")
        self.edit_loc.setPlaceholderText("0.000000,0.000000")
        self.text_details.setPlaceholderText("Buraya yazın...")

        self.formLayout.addRow("İsim : ", self.edit_name)
        self.formLayout.addRow("Soyisim : ", self.edit_surname)
        self.formLayout.addRow("Telefon : ", self.edit_phone)
        self.formLayout.addRow("Anne Adı : ", self.edit_mother_name)
        self.formLayout.addRow("Baba Adı : ", self.edit_father_name)
        self.formLayout.addRow("İş : ", self.edit_job)
        self.formLayout.addRow("İş Yeri Adresi ", self.edit_workplace)
        self.formLayout.addRow("Ev Lokasyonu : ", self.edit_loc)
        self.formLayout.addRow("Evli : ", self.check_married)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
