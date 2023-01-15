from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit, QCheckBox


class AddWebsiteDialog(QDialog):
    def __init__(self, controller):
        super(AddWebsiteDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_domain = QLineEdit()
        self.edit_url = QLineEdit()
        self.edit_dns = QLineEdit()
        self.edit_organization = QLineEdit()
        self.check_hacked = QCheckBox("Evet")
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.uis = [self.edit_domain, self.edit_url, self.edit_dns, self.edit_organization]

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
        self.btn_submit.clicked.connect(self.controller.insert_website)

        self.edit_domain.setPlaceholderText("domain.com")
        self.edit_url.setPlaceholderText("https://www.domain.com")
        self.edit_dns.setPlaceholderText("192.168.1.1")
        self.edit_organization.setPlaceholderText("Organizasyon adı girin")
        self.text_details.setPlaceholderText("Buraya yazın...")

        self.formLayout.addRow("Domain : ", self.edit_domain)
        self.formLayout.addRow("URL : ", self.edit_url)
        self.formLayout.addRow("DNS : ", self.edit_dns)
        self.formLayout.addRow("Organizasyon : ", self.edit_organization)
        self.formLayout.addRow("Hacklendi : ", self.check_hacked)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
