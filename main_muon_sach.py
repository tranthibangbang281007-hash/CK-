import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QMessageBox , QAbstractSpinBox
from PyQt6.QtCore import QDate, QDateTime
from PyQt6 import uic
from phieu_muon_sach import PhieuMuon
from TapCacPhieuMuon import QuanLyMuonSach


class RentBookWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("giaodien_muonsach.ui", self)

        self.quan_ly = QuanLyMuonSach()
        hom_nay = QDate.currentDate()
        self.datemuon.setDate(hom_nay)
        self.datemuon.setReadOnly(True)
        self.datemuon.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)  # khóa ô không cho sửa

        self.datetra.setMinimumDate(hom_nay)
        ngay_toi_da = hom_nay.addDays(30)
        self.datetra.setMaximumDate(ngay_toi_da)
        self.datetra.dateChanged.connect(self.tinh_tien)
        self.tinh_tien()

        self.btnycmuon.clicked.connect(self.yeucauthanhcong)
        self.btnquaylai.clicked.connect(self.quay_lai_sua)
        self.btnhoantat.clicked.connect(self.luu_phieu_that)
        self.btnquaylai_2.clicked.connect(self.ve_menu)

    def tinh_tien(self):
        d_muon = self.datemuon.date()
        d_tra = self.datetra.date()

        so_ngay = d_muon.daysTo(d_tra)
        if so_ngay <= 0:
            so_ngay = 1

        thanh_tien = so_ngay * 10000
        chuoi_tien = f"{thanh_tien:,}"
        self.txttongtien.setText(chuoi_tien)
        return chuoi_tien

    def yeucauthanhcong(self):
        pass


    def quay_lai_sua(self):
        self.stackedWidget.setCurrentIndex(0)
    def luu_phieu_that(self):
        hoten = self.viewhoten.text()
        sdt = self.viewsdt.text()
        diachi = self.viewdiachi.text()
        tensach = self.viewtensach.text()
        masach = self.viewmasach.text()
        ngay_muon = self.viewngaymuon.text()
        ngay_tra = self.viewngaytra.text()

        du_lieu_dong = f"{masach},{tensach},{ngay_tra}\n"

        try:
            with open("sach_dang_muon.txt", "a", encoding="utf-8") as f:
                f.write(du_lieu_dong)
        except Exception as e:
            print(f"Lỗi không lưu được file: {e}")

        thanh_cong, thong_bao = self.quan_ly.tao_phieu_moi(hoten, sdt, diachi, tensach, masach, ngay_muon, ngay_tra)

        if thanh_cong:
            QMessageBox.information(self, "Thành công", "Xác nhận mượn thành công!")
            from main_manhinhchinh import MainWindow
            self.mh_chinh = MainWindow()
            self.mh_chinh.show()
            self.close()
        else:
            QMessageBox.warning(self, "Lỗi", thong_bao)

    def xoa_trang_form(self):
        self.txttensach.setText("")
        self.txtmasach.setText("")

    def ve_menu(self):
        from main_manhinhchinh import MainWindow
        self.mh_chinh = MainWindow()
        self.mh_chinh.show()
        self.hide()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = RentBookWindow()
    window.show()
    sys.exit(app.exec())