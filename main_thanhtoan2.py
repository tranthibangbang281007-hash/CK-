import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
import pic5_rc

class PenaltyTransferWindow(QMainWindow):
    def __init__(self, thong_tin):
        super().__init__()
        uic.loadUi("thanhtoan2.ui", self)
        
        self.fix_font()
        self.thong_tin = thong_tin
        
        # Kết nối nút ĐÃ THANH TOÁN
        self.ptndathanhtoan.clicked.connect(self.xu_ly_da_thanh_toan)
    
    def fix_font(self):
        for label in [self.lblcuphap]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(9)
            label.setFont(font)
        for label in [self.lblstk, self.lbltentk, self.lblnganhang]:
            font.setBold(True)
            font.setPointSize(11)
            label.setFont(font)
        for button in [self.ptndathanhtoan]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(9)
            button.setFont(font)

    def xu_ly_da_thanh_toan(self):
        """Xử lý khi bấm ĐÃ THANH TOÁN"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Xác nhận thanh toán phạt")
        msg.setText("Vui lòng đợi xác nhận từ cửa hàng trong giây lát!")
        msg.setInformativeText("Sau khi xác nhận, sách sẽ được cập nhật trạng thái đã trả.")
        msg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if msg.exec() == QMessageBox.StandardButton.Yes:
            QMessageBox.information(
                None, 
                "Thành công", 
                "Đã thanh toán phạt thành công!\nCảm ơn bạn đã hợp tác."
            )
            
            # Quay về màn hình chính
            try:
                from main_manhinhchinh import MainWindow
                self.main = MainWindow()
                self.main.show()
            except:
                pass
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    thong_tin_mau = {
        'sdt': '0123456789', 
        'masach': 'PY001',
        'so_ngay_qua_han': 5
    }
    window = PenaltyTransferWindow(thong_tin_mau)
    window.show()
    sys.exit(app.exec())