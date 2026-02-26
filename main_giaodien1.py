import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import Qt
import giaodien1_rc

class CustomerInfoWindow(QMainWindow):
    def __init__(self, thong_tin=None):
        super().__init__()
        uic.loadUi("giaodien.ui", self)
        
        self.fix_font()
        # Lưu thông tin
        self.thong_tin = thong_tin if thong_tin else {}
        self.next_window = None
        
        # Nếu có thông tin thì hiển thị lên form
        if thong_tin:
            self.hien_thi_thong_tin()

        # Kết nối nút Xác nhận
        self.ptnxacnhan.clicked.connect(self.xu_ly_xac_nhan)
        self.ptnquaylai.clicked.connect(self.close)
    
    def fix_font(self):
        for label in [self.lblHoTen, self.lblSdt, self.lblCCCD, self.lblTensach, self.lblMasach, self.lblDiachi]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(11)
            label.setFont(font)
        for line_edit in [self.ledHovaTen, self.ledSdt, self.ledCCCD, self.ledTensach, self.ledMasach, self.ledDiachi]:
            font = line_edit.font()
            font.setBold(True)
            font.setPointSize(10)
            line_edit.setFont(font)
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for button in [self.ptnquaylai, self.ptnxacnhan]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(11)
            button.setFont(font)

    def hien_thi_thong_tin(self):
        """Hiển thị thông tin lên các ô nhập"""
        self.ledHovaTen.setText(self.thong_tin.get('hoten', ''))
        self.ledSdt.setText(self.thong_tin.get('sdt', ''))
        self.ledCCCD.setText(self.thong_tin.get('cmt', ''))
        self.ledTensach.setText(self.thong_tin.get('tensach', ''))
        self.ledMasach.setText(self.thong_tin.get('masach', ''))
        self.ledDiachi.setText(self.thong_tin.get('diachi', ''))
    
    def lay_thong_tu_form(self):
        """Lấy thông tin từ form"""
        hoten = self.ledHovaTen.text().strip()
        sdt = self.ledSdt.text().strip()
        cmt = self.ledCCCD.text().strip()
        tensach = self.ledTensach.text().strip()
        masach = self.ledMasach.text().strip()
        diachi = self.ledDiachi.text().strip()
        
        # Kiểm tra thông tin bắt buộc
        if not hoten or not sdt or not masach:
            QMessageBox.warning(None, "Thiếu thông tin", 
                               "Vui lòng nhập đủ họ tên, SĐT và mã sách!")
            return None
        
        return {
            'hoten': hoten,
            'sdt': sdt,
            'cmt': cmt,
            'tensach': tensach,
            'masach': masach,
            'diachi': diachi
        }
    
    def xu_ly_xac_nhan(self):
        """Xử lý khi bấm nút Xác nhận"""
        thong_tin = self.lay_thong_tu_form()
        if thong_tin:
            #Giữ lại thông tin ngày tháng từ màn hình trước:
            if 'ngay_muon' in self.thong_tin:
                thong_tin['ngay_muon'] = self.thong_tin['ngay_muon']
                thong_tin['ngay_tra'] = self.thong_tin['ngay_tra']
            # Chuyển sang màn hình thời gian
            from main_giaodien2 import TimeInfoWindow
            self.next_window = TimeInfoWindow(thong_tin)
            self.next_window.show()
            self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CustomerInfoWindow()
    window.show()
    sys.exit(app.exec())