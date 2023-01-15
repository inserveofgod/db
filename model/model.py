import json
import os
import sqlite3

from PyQt5.QtGui import QIcon


class Model:
    def __init__(self):
        self.root = os.getcwd()
        self.config = self.read()

        self.encoding = "UTF-8"
        self.title = "Db"

        self.TABLE_PEOPLE = "people"
        self.TABLE_WEBSITE = "website"
        self.TABLE_WIFI = "wifi"
        self.TABLE_ACCOUNT = "account"

        self.PEOPLE = "Kişiler"
        self.WEBSITE = "İnternet siteleri"
        self.WIFI = "Kablosuz Bağlantılar"
        self.ACCOUNT = "Hesaplar"

        self.selected_table = None
        self.selected_row = None
        self.selected_id = None

        self.select_people_sql = "SELECT id, name, surname, phone, mother_name, father_name, job, workplace_name," \
                                 " person_loc, married FROM people"

        self.select_website_sql = "SELECT id, domain, public_url, dns, organization, hacked FROM website"

        self.select_wifi_sql = "SELECT w.id, w.essid, w.bssid, w.password, w.public_ip, w.subnet, w.gateway, " \
                               "w.trademark, w.panel_user, w.panel_pass, p.protocol_name, w.location, " \
                               "w.hacked FROM wifi as w INNER JOIN protocols p on p.id = w.protocol_id;"

        self.select_account_sql = "SELECT a.id, a.email, a.pass, at.account_type FROM account as a " \
                                  "INNER JOIN account_types at on a.account_type_id = at.id;"

        self.img_assets = os.path.join(self.root, "assets", "img")
        self.css_assets = os.path.join(self.root, "assets", "css")
        self.config_path = os.path.join(self.root, "model", "config.json")

        self.icon = QIcon(os.path.join(self.img_assets, "database.png"))

        self.database = os.path.join(self.root, "model", "datatable.db")
        self.conn = sqlite3.connect(self.database)

        self.add_icon = QIcon(os.path.join(self.img_assets, "database--plus.png"))
        self.del_icon = QIcon(os.path.join(self.img_assets, "database--minus.png"))
        self.edit_icon = QIcon(os.path.join(self.img_assets, "database--pencil.png"))
        self.show_det_icon = QIcon(os.path.join(self.img_assets, "database-property.png"))
        self.show_loc_icon = QIcon(os.path.join(self.img_assets, "geolocation.png"))
        self.exit_icon = QIcon(os.path.join(self.img_assets, "door-open-in.png"))

        self.full_icon = QIcon(os.path.join(self.img_assets, "application-resize-full.png"))
        self.menu_icon = QIcon(os.path.join(self.img_assets, "ui-menu.png"))
        self.toolbar_icon = QIcon(os.path.join(self.img_assets, "ui-toolbar.png"))
        self.dark_icon = QIcon(os.path.join(self.img_assets, "smiley-glass.png"))

        self.help_icon = QIcon(os.path.join(self.img_assets, "question.png"))
        self.about_icon = QIcon(os.path.join(self.img_assets, "information.png"))

    def is_selected(self) -> bool:
        """
        Seçilme ile ilgili verilerin seçili olup olmadığını yansıtır
        :rtype: bool
        """
        if self.selected_id is not None and self.selected_row is not None and self.selected_table is not None:
            return True
        return False

    def deselect(self) -> None:
        """
        Seçili verileri seçilmemiş haline geri döndürür
        :rtype: None
        """
        self.selected_id = self.selected_row = self.selected_table = None

    def _write(self) -> None:
        """
        Sınıf içerisinde dosyaya yazmak için kullanılmalıdır.
        :rtype: None
        """
        dumping = json.dumps(self.config, indent=4, sort_keys=True)

        with open(self.config_path, "w") as f:
            f.write(dumping)

    def update(self, key: str, value: any) -> None:
        """
        Belli bir ayarı değiştirmek ve kaydetmek için kullanılır
        :rtype: None
        """
        self.config = self.read()
        self.config[key] = value
        self._write()

    def read(self) -> dict:
        """
        Ayarları okutur ve geri döndürür
        :rtype: dict
        """
        with open(os.path.join(self.root, "model", "config.json")) as f:
            json_data = f.read()
            dict_data = json.loads(json_data)
            self.config = dict_data
            return dict_data

    def read_stylesheets(self) -> any:
        """
        json dosyasından alınıp css dosyasına yazılan verileri döndürür
        :rtype: any
        """
        self.config = self.read()

        if self.config.get('dark'):
            with open(os.path.join(self.css_assets, "{}.min.css".format('dark'))) as f:
                return f.read()
        return None
