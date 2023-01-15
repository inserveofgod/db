from PyQt5.QtWidgets import QVBoxLayout, QFormLayout, QLineEdit, QDialog, QPushButton, QTextEdit, QCheckBox, QComboBox


class AddWifiDialog(QDialog):
    def __init__(self, controller):
        super(AddWifiDialog, self).__init__()

        self.controller = controller
        self.model = self.controller.model

        self.mainLayout = QVBoxLayout()
        self.formLayout = QFormLayout()

        self.edit_essid = QLineEdit()
        self.edit_bssid = QLineEdit()
        self.edit_pass = QLineEdit()
        self.edit_ip = QLineEdit()
        self.edit_subnet = QLineEdit()
        self.edit_gateway = QLineEdit()
        self.edit_trademark = QLineEdit()
        self.edit_panel_user = QLineEdit()
        self.edit_panel_pass = QLineEdit()
        self.combo_protocol = QComboBox()
        self.edit_loc = QLineEdit()
        self.check_hacked = QCheckBox("Evet")
        self.text_details = QTextEdit()
        self.btn_submit = QPushButton("Ekle")

        self.protocol_names = []
        self.protocol_ids = []

        self.uis = [self.edit_essid, self.edit_bssid, self.edit_pass, self.edit_ip, self.edit_subnet, self.edit_gateway,
                    self.edit_trademark, self.edit_panel_user, self.edit_panel_pass, self.edit_loc]

        self._ui()

    def refactor(self):
        for ui in self.uis:
            ui.setText("")

        self.edit_bssid.setInputMask("xx:xx:xx:xx:xx:xx;_")
        # we do not want to include text_details variable, so we make it separated
        self.text_details.setText("")

    def _ui(self):
        self.setWindowTitle(self.model.title)
        self.setWindowIcon(self.model.icon)
        self.setLayout(self.formLayout)

        self.btn_submit.setText("Ekle")
        self.btn_submit.clicked.connect(self.controller.insert_wifi)

        cursor = self.model.conn.cursor()
        cursor.execute("SELECT * FROM protocols")
        data = cursor.fetchall()

        for _, datum in data:
            self.protocol_ids.append(_)
            self.protocol_names.append(datum)

        self.edit_bssid.setInputMask("xx:xx:xx:xx:xx:xx;_")
        self.edit_pass.setPlaceholderText("*****")
        self.edit_ip.setPlaceholderText("xxx:xxx:xxx:xxx")
        self.edit_subnet.setPlaceholderText("255:255:255:0")
        self.edit_gateway.setPlaceholderText("192:168:1:1")
        self.text_details.setPlaceholderText("Buraya yazın...")

        for protocol_name in self.protocol_names:
            self.combo_protocol.addItem(protocol_name)

        self.formLayout.addRow("ESSID : ", self.edit_essid)
        self.formLayout.addRow("BSSID : ", self.edit_bssid)
        self.formLayout.addRow("Şifre : ", self.edit_pass)
        self.formLayout.addRow("iP : ", self.edit_ip)
        self.formLayout.addRow("Alt ağ : ", self.edit_subnet)
        self.formLayout.addRow("Ağ geçidi : ", self.edit_gateway)
        self.formLayout.addRow("Marka : ", self.edit_trademark)
        self.formLayout.addRow("Panel kullanıcı adı : ", self.edit_panel_user)
        self.formLayout.addRow("Panel kullanıcı şifresi : ", self.edit_panel_pass)
        self.formLayout.addRow("Protokol : ", self.combo_protocol)
        self.formLayout.addRow("Hacklendi : ", self.check_hacked)
        self.formLayout.addRow("Detaylar : ", self.text_details)
        self.formLayout.addWidget(self.btn_submit)
