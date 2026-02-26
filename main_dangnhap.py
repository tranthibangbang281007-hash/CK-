import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox, QLineEdit
from PyQt6 import uic

from taikhoan import TaiKhoan
from TapTaiKhoan import DanhSachTaiKhoan
from main_muon_sach import RentBookWindow

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("giaodien_dangnhap.ui", self)

        self.quan_ly = DanhSachTaiKhoan()

        self.stackedWidget.setCurrentIndex(0)
        self.txtmk.setEchoMode(QLineEdit.EchoMode.Password)

        self.btndangki.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
        self.btnquenmk.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(2))
        self.btnquaylai.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))

        self.btndangnhap.clicked.connect(self.xu_ly_dang_nhap)
        self.btnxacnhandk.clicked.connect(self.xu_ly_dang_ky)
        self.btnxacthuc.clicked.connect(self.xu_ly_quen_mk)

    def xu_ly_dang_nhap(self):
        sdt = self.txtsdt.text().strip()
        mk = self.txtmk.text().strip()

        nguoi_dung = self.quan_ly.kiem_tra_dang_nhap(sdt, mk)


        if nguoi_dung:
            QMessageBox.information(self, "Thành công", f"Xin chào {nguoi_dung.ho_ten}!")
            from main_manhinhchinh import MainWindow
            self.man_hinh_chinh = MainWindow()
            self.man_hinh_chinh.show()
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", "Sai thông tin đăng nhập!")

    def xu_ly_dang_ky(self):
        hoten = self.txthoten.text().strip()
        sdt = self.txtsdt2.text().strip()
        mk = self.txtmk2.text().strip()
        gmail = self.txtgmail.text().strip()
        if not hoten or not sdt or not mk or not gmail:
            QMessageBox.warning(self, "Thiếu thông tin", "Vui lòng điền đầy đủ tất cả các ô!")
            return
        if len(mk) < 6:
            QMessageBox.warning(self, "Mật khẩu yếu", "Mật khẩu phải có ít nhất 6 ký tự!")
            return


        from taikhoan import TaiKhoan  # Đảm bảo đã import
        tk_moi = TaiKhoan(sdt, mk, hoten, email=gmail)
        ket_qua = self.quan_ly.them_moi(tk_moi)

        if ket_qua:
            QMessageBox.information(self, "Thành công", "Đăng ký thành công! Mời bạn đăng nhập.")
            self.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.warning(self, "Lỗi", "Số điện thoại này đã được đăng ký rồi!")


    def xu_ly_quen_mk(self):
        thong_tin = self.txtsdt3.text().strip()
        mk_tim_thay = self.quan_ly.tim_kiem_mk(thong_tin)

        if mk_tim_thay:
            QMessageBox.information(self, "Tìm thấy", f"Mật khẩu của bạn là: {mk_tim_thay}")
            self.stackedWidget.setCurrentIndex(0)
        else:
            QMessageBox.critical(self, "Lỗi", "Không tìm thấy tài khoản này!")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())