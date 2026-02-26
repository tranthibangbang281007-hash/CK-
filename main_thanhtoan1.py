import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
import pic3_rc

class BankTransferWindow(QMainWindow):
    def __init__(self, thong_tin):
        super().__init__()
        uic.loadUi("thanhtoan1.ui", self)
        
        self.fix_font()
        self.thong_tin = thong_tin
        self.next_window = None
        
        # Kết nối nút ĐÃ THANH TOÁN
        self.ptnthanhtoan1.clicked.connect(self.xu_ly_da_thanh_toan)
    

    def fix_font(self):
        for label in [self.lblchuyencuphap]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(9)
            label.setFont(font)
        for label in [self.lblstk, self.lbltennganhang, self.lbltentk]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(11)
            label.setFont(font)    
        for button in [self.ptnthanhtoan1]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(10)
            button.setFont(font)

    def xu_ly_da_thanh_toan(self):
        """Xử lý khi bấm ĐÃ THANH TOÁN"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Xác nhận thanh toán")
        msg.setInformativeText("Vui lòng đợi xác nhận từ cửa hàng trong giây lát.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                None, 
                "Thành công!", 
                "Phiếu thuê đã được ghi nhận.\nBookflow xin cảm ơn vì đã sử dụng dịch vụ và chúc bạn có một ngày vui vẻ."
            )

            # Quay về màn hình chính 
            try:
                from main_manhinhchinh import MainWindow
                self.main = MainWindow()
                self.main.show()
            except:
                # Nếu không có, chỉ cần đóng
                pass
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    thong_tin_mau = {'sdt': '0123456789', 'masach': 'PY001'}
    window = BankTransferWindow(thong_tin_mau)
    window.show()
    sys.exit(app.exec())