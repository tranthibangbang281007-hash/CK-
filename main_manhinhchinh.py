import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6 import uic

from main_muon_sach import RentBookWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("giaodien_manhinhchinh.ui", self)

        self.btnmuonsach.clicked.connect(self.mo_man_hinh_muon)
        self.btndangxuat.clicked.connect(self.xu_ly_dang_xuat)
        self.btntrasach.clicked.connect(self.mo_man_hinh_tra)
        self.btnlichsu.clicked.connect(self.mo_lich_su)

    def mo_man_hinh_muon(self):
        self.mh_muon = RentBookWindow()
        self.mh_muon.show()
    def xu_ly_dang_xuat(self):
        self.close()
        from main_dangnhap import LoginWindow
        self.mh_login = LoginWindow()
        self.mh_login.show()

    def mo_man_hinh_tra(self):
        from main_trasach import ReturnBookWindow
        self.mh_tra = ReturnBookWindow()
        self.mh_tra.show()
        self.hide()

    def mo_lich_su(self):
        try:
            # Import và mở màn hình
            from main_lichsu import HistoryWindow
            self.mh_su = HistoryWindow()
            self.mh_su.show()

            # Chỉ ẩn menu khi mở thành công
            self.hide()

        except Exception as e:
            # Nếu có lỗi thì in ra và hiện thông báo
            print(f"LỖI CHI TIẾT: {e}")
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.critical(self, "Lỗi Lịch Sử", f"Không mở được vì:\n{e}")


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())