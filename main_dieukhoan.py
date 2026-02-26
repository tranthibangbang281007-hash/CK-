import sys
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
import pic2_rc

class TermsWindow(QMainWindow):
    def __init__(self, thong_tin):
        super().__init__()
        uic.loadUi("dieukhoan.ui", self)
        
        self.fix_font()
        self.thong_tin = thong_tin
        self.next_window = None
        
        # Kết nối nút đồng ý
        self.ptndongy.clicked.connect(self.xu_ly_dong_y)
    
    def fix_font(self):
        for button in [self.ptndongy]:
            font = button.font()
            font.setBold(True)
            button.setFont(font)

    def xu_ly_dong_y(self):
        """Xử lý khi đồng ý điều khoản"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Xác nhận đồng ý")
        msg.setText("Xác nhận! Bạn đã hoàn thành thủ tục mượn sách")
        msg.setInformativeText("Vui lòng chấp hành quy định của cửa hàng và thanh toán đúng hạn.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)

        if msg.exec() == QMessageBox.StandardButton.Yes:
            # Chuyển sang màn hình thanh toán
            from main_thanhtoan1 import BankTransferWindow
            self.next_window = BankTransferWindow(self.thong_tin)
            self.next_window.show()
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    thong_tin_mau = {'hoten': 'Test'}
    window = TermsWindow(thong_tin_mau)
    window.show()
    sys.exit(app.exec())