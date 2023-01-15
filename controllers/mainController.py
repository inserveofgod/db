from PyQt5.QtWidgets import QMessageBox, QTabWidget, QTreeView, QInputDialog

from model.model import Model
from views.AddAccountDialog import AddAccountDialog
from views.AddPeopleDialog import AddPeopleDialog
from views.AddWebsiteDialog import AddWebsiteDialog
from views.AddWifiDialog import AddWifiDialog
from views.MainWindow import MainWindow
from views.Menus import Menus
from views.Toolbar import Toolbar
from views.ViewTab import ViewTab


class MainController:
    def __init__(self):
        # model
        self.model = Model()

        # views
        self.mainWindow = MainWindow(self)
        self.menus = Menus(self)
        self.toolBar = Toolbar(self)

        people_tab_titles = ["ID", "İsim", "Soyisim", "Telefon", "Anne Adı", "Baba Adı", "İş", "İş Yeri", "Lokasyon",
                             "Evli"]
        website_tab_titles = ["ID", "Domain", "Ortak iP", "DNS", "Organizasyon", "Hacklendi"]
        wifi_tab_titles = ["ID", "ESSID", "BSSID", "Şifre", "Ortak iP", "Alt Ağ", "Ağ Geçidi", "Marka",
                           "Panel Kullanıcı Adı", "Panel Kullanıcı Şifresi", "Güvenlik Protokolü", "Lokasyon",
                           "Hacklendi"]
        account_tab_titles = ["ID", "Email Adresi", "Şifre", "Hesap Tipi"]

        self.peopleTab = ViewTab(self, people_tab_titles, self.model.TABLE_PEOPLE)
        self.websiteTab = ViewTab(self, website_tab_titles, self.model.TABLE_WEBSITE)
        self.wifiTab = ViewTab(self, wifi_tab_titles, self.model.TABLE_WIFI)
        self.accountTab = ViewTab(self, account_tab_titles, self.model.TABLE_ACCOUNT)

        self.addAccountDialog = AddAccountDialog(self)
        self.addPeopleDialog = AddPeopleDialog(self)
        self.addWebsiteDialog = AddWebsiteDialog(self)
        self.addWifiDialog = AddWifiDialog(self)

    # starters
    def main(self):
        self.mainWindow.main()
        self.menus.main()
        self.toolBar.main()

        self.peopleTab.main()
        self.websiteTab.main()
        self.wifiTab.main()
        self.accountTab.main()

    def tabs(self):
        tab = QTabWidget()
        tab.addTab(self.peopleTab, self.model.PEOPLE)
        tab.addTab(self.websiteTab, self.model.WEBSITE)
        tab.addTab(self.wifiTab, self.model.WIFI)
        tab.addTab(self.accountTab, self.model.ACCOUNT)
        self.mainWindow.setCentralWidget(tab)

    # table loaders

    def remove_data(self):
        self.peopleTab.tableModel.setRowCount(0)
        self.websiteTab.tableModel.setRowCount(0)
        self.wifiTab.tableModel.setRowCount(0)
        self.accountTab.tableModel.setRowCount(0)

    def append_data(self, which: str, data: tuple):
        table_model = None

        if which == self.model.TABLE_PEOPLE:
            table_model = self.peopleTab.tableModel

        elif which == self.model.TABLE_WEBSITE:
            table_model = self.websiteTab.tableModel

        elif which == self.model.TABLE_WIFI:
            table_model = self.wifiTab.tableModel

        elif which == self.model.TABLE_ACCOUNT:
            table_model = self.accountTab.tableModel

        table_model.insertRow(0)

        for i in range(len(data)):
            table_model.setData(table_model.index(0, i), data[i])

    def reload_tables(self):
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_people_sql)
        people_data = cursor.fetchall()

        # refresh cursor for each fetching
        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_website_sql)
        website_data = cursor.fetchall()

        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_wifi_sql)
        wifi_data = cursor.fetchall()

        cursor = self.model.conn.cursor()
        cursor.execute(self.model.select_account_sql)
        account_data = cursor.fetchall()

        self.remove_data()

        # load data into tables
        for people_datum in people_data:
            self.append_data(self.model.TABLE_PEOPLE, people_datum)

        for website_datum in website_data:
            self.append_data(self.model.TABLE_WEBSITE, website_datum)

        for wifi_datum in wifi_data:
            self.append_data(self.model.TABLE_WIFI, wifi_datum)

        for account_datum in account_data:
            self.append_data(self.model.TABLE_ACCOUNT, account_datum)

    # sql listeners

    def insert_people(self):
        row_id = self.model.selected_id
        dialog = self.addPeopleDialog
        contents = [ui.text() for ui in dialog.uis]
        name, surname, phone, mother_name, father_name, job, workplace, loc = contents
        details = dialog.text_details.toPlainText()
        married = dialog.check_married.isChecked()

        if row_id is None:
            sql = "INSERT INTO people(id, name, surname, phone, mother_name, father_name, job, workplace_name, " \
                  "person_loc, married, details) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        else:
            sql = "UPDATE people " \
                  "SET id = ?, name = ?, surname = ?, phone = ?, mother_name = ?, father_name = ?, job = ?, " \
                  "workplace_name = ?, person_loc = ?, married = ?, details = ? " \
                  f"WHERE id = {row_id}"

        row = (row_id, name, surname, phone, mother_name, father_name, job, workplace, loc, married, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        self.addPeopleDialog.close()
        self.reload_tables()

    def insert_website(self):
        row_id = self.model.selected_id
        dialog = self.addWebsiteDialog
        contents = [ui.text() for ui in dialog.uis]
        domain, url, dns, organization = contents
        hacked = dialog.check_hacked.isChecked()
        details = dialog.text_details.toPlainText()

        if row_id is None:
            sql = "INSERT INTO website(id, domain, public_url, dns, organization, hacked, details)" \
                  "VALUES(?, ?, ?, ?, ?, ?, ?)"

        else:
            sql = "UPDATE website " \
                  "SET id = ?, domain = ?, public_url = ?, dns = ?, organization = ?, hacked = ?, details = ?" \
                  f" WHERE id = {row_id}"

        row = (row_id, domain, url, dns, organization, hacked, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        self.addWebsiteDialog.close()
        self.reload_tables()

    def insert_wifi(self):
        row_id = self.model.selected_id
        dialog = self.addWifiDialog
        contents = [ui.text() for ui in dialog.uis]
        essid, bssid, passwd, ip, subnet, gateway, trademark, panel_user, panel_pass, loc = contents
        hacked = dialog.check_hacked.isChecked()
        protocol = dialog.combo_protocol.currentIndex()
        details = dialog.text_details.toPlainText()

        protocol_id = dialog.protocol_ids[protocol]

        if row_id is None:
            sql = "INSERT INTO wifi(id, essid, bssid, password, public_ip, subnet, gateway, trademark, " \
                  "panel_user, panel_pass, protocol_id, location, hacked, details) " \
                  "VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"

        else:
            sql = "UPDATE wifi " \
                  "SET id = ?, essid = ?, bssid = ?, password = ?, public_ip = ?, subnet = ?, gateway = ?, " \
                  "trademark = ?, panel_user = ?, panel_pass = ?, protocol_id = ?, location = ?, hacked = ?, " \
                  f"details = ? WHERE id = {row_id}"

        row = (row_id, essid, bssid, passwd, ip, subnet, gateway, trademark, panel_user, panel_pass, protocol_id,
               loc, hacked, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        self.addWifiDialog.close()
        self.reload_tables()

    def insert_account(self):
        row_id = self.model.selected_id
        dialog = self.addAccountDialog
        contents = [ui.text() for ui in dialog.uis]
        email, passwd = contents
        account = dialog.combo_account.currentIndex()
        details = dialog.text_details.toPlainText()
        account_id = dialog.account_type_ids[account]

        if row_id is None:
            sql = "INSERT INTO account(id, email, pass, account_type_id, details) VALUES (?, ?, ?, ?, ?)"

        else:
            sql = "UPDATE account " \
                  "SET id = ?, email = ?, pass = ?, account_type_id = ?, details = ?" \
                  f" WHERE id = {row_id}"

        row = (row_id, email, passwd, account_id, details)
        cursor = self.model.conn.cursor()

        cursor.execute(sql, row)
        self.model.conn.commit()
        self.addAccountDialog.close()
        self.reload_tables()

    # table listeners
    def selected(self, table: QTreeView, which: str):
        table_model = table.model()
        indexes = table.selectedIndexes()

        if indexes:
            self.model.selected_row = indexes[0].row()
            self.model.selected_table = which
            self.model.selected_id = table_model.data(table_model.index(self.model.selected_row, 0))

            self.menus.enable()
            self.toolBar.enable()

        print(self.model.selected_table, self.model.selected_row, self.model.selected_id)

    # listeners
    def action_manage_add(self) -> None:
        selected, _ = QInputDialog.getItem(self.mainWindow, self.model.title, "Seç : ",
                                           [self.model.PEOPLE, self.model.WEBSITE, self.model.WIFI, self.model.ACCOUNT],
                                           0, False)

        if _:
            self.model.deselect()
            self.menus.disable()
            self.toolBar.disable()

            if selected == self.model.PEOPLE:
                self.addPeopleDialog.refactor()
                self.addPeopleDialog.show()

            elif selected == self.model.WEBSITE:
                self.addWebsiteDialog.refactor()
                self.addWebsiteDialog.show()

            elif selected == self.model.WIFI:
                self.addWifiDialog.refactor()
                self.addWifiDialog.show()

            elif selected == self.model.ACCOUNT:
                self.addAccountDialog.refactor()
                self.addAccountDialog.show()

    def action_manage_del(self) -> None:
        if self.model.is_selected():
            confirm = QMessageBox.question(self.mainWindow, self.mainWindow.windowTitle(),
                                           f"Bu satırı silmek istediğinize emin misiniz?\n"
                                           f"id={self.model.selected_id}, table={self.model.selected_table}")

            if confirm == QMessageBox.Yes:
                sql = f"DELETE FROM {self.model.selected_table} WHERE id={self.model.selected_id}"
                cursor = self.model.conn.cursor()

                try:
                    cursor.execute(sql)
                    self.model.conn.commit()
                except Exception as exc:
                    QMessageBox.critical(self.mainWindow, self.mainWindow.windowTitle(), "Veri silinemedi!\n"
                                                                                         f"Hata : {str(exc)}")

                else:
                    self.model.deselect()
                    self.menus.disable()
                    self.toolBar.disable()
                    self.reload_tables()
                    QMessageBox.information(self.mainWindow, self.mainWindow.windowTitle(), "Veri silindi")

    def action_manage_edit(self) -> None:
        if self.model.is_selected():
            dialog = data = None
            cursor = self.model.conn.cursor()

            if self.model.selected_table == self.model.TABLE_PEOPLE:
                sql = "SELECT name, surname, phone, mother_name, father_name, job, workplace_name, person_loc, " \
                      f"details FROM people WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addPeopleDialog

            elif self.model.selected_table == self.model.TABLE_WEBSITE:
                sql = "SELECT domain, public_url, dns, organization, details FROM website " \
                      f"WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addWebsiteDialog

            elif self.model.selected_table == self.model.TABLE_WIFI:
                sql = "SELECT essid, bssid, password, public_ip, subnet, gateway, trademark, " \
                  f"panel_user, panel_pass, location, details FROM wifi WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addWifiDialog

            elif self.model.selected_table == self.model.TABLE_ACCOUNT:
                sql = f"SELECT email, pass, details FROM account WHERE id={self.model.selected_id}"
                cursor.execute(sql)
                data = cursor.fetchone()
                dialog = self.addAccountDialog

            for i in range(len(dialog.uis)):
                dialog.uis[i].setText(data[i])

            dialog.btn_submit.setText("Düzenle")
            dialog.show()

    def action_manage_show_det(self) -> None:
        if self.model.is_selected():
            sql = f"SELECT details FROM {self.model.selected_table} WHERE id = {self.model.selected_id}"
            cursor = self.model.conn.cursor()
            cursor.execute(sql)

            # 0 is the first argument of data we are interested of
            data = cursor.fetchone()[0]
            QMessageBox.information(self.mainWindow, self.mainWindow.windowTitle(), f"Detaylar : '{data}'")

    def action_manage_exit(self) -> bool:
        ask = QMessageBox.question(self.mainWindow, self.model.title, "Uygulamadan çıkmak istediğinize emin misiniz?",
                                   QMessageBox.Yes | QMessageBox.No)
        return True if ask == QMessageBox.Yes else False

    def action_view_full(self) -> None:
        if self.mainWindow.isFullScreen():
            self.mainWindow.showNormal()

        else:
            self.mainWindow.showFullScreen()

    def action_view_menu(self) -> None:
        menubar = self.mainWindow.menuBar()
        menubar.setVisible(False if menubar.isVisible() else True)

    def action_view_toolbar(self) -> None:
        toolbar = self.toolBar.toolbar
        toolbar.setVisible(False if toolbar.isVisible() else True)

    def action_view_dark(self) -> None:
        if self.model.config.get('dark'):
            self.model.update("dark", False)

        else:
            self.model.update("dark", True)

        stylesheets = self.model.read_stylesheets()

        if stylesheets is not None:
            # todo : append stylesheets in order to make program dark or light
            pass

    def action_help_help(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Program hakkında yardım için\ninserveofgod@gmail.com adresine mail gönderebilirsiniz",
                                QMessageBox.Ok)

    def action_help_about(self) -> None:
        QMessageBox.information(self.mainWindow, self.model.title,
                                "Bu program Python programalama dili ile PyQt5\n"
                                "kütüphanesi kullanılarak yapılmıştır.",
                                QMessageBox.Ok)

