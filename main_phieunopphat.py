import sys
from PyQt6.QtWidgets import QMainWindow, QApplication
from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
import pic4_rc

class PenaltyWindow(QMainWindow):
    def __init__(self, thong_tin):
        super().__init__()
        uic.loadUi("phieunopphat.ui", self)
        
        self.fix_font()
        self.thong_tin = thong_tin
        self.next_window = None
        
        # Hiển thị thông tin
        self.hien_thi_thong_tin()
        
        # Kết nối nút THANH TOÁN
        self.ptnThanhtoan.clicked.connect(self.xu_ly_thanh_toan)

    def fix_font(self):
        for label in [self.lblhoten, self.lblsdt, self.lbltensach, self.lblmasach, self.lblngaymuon, self.lblngaytradk, self.lblngaytratt, self.lblsongayquahan, self.lblsotiencantra]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(10)
            label.setFont(font)
        for line_edit in [self.ledHoten, self.ledSdt, self.ledNgaymuon, self.ledTensach, self.ledMasach, self.ledNgaytradk, self.ledNgaytratt, self.ledSongayquahan, self.ledSotiencantra]:
            font = line_edit.font()
            font.setBold(True)
            font.setPointSize(7)
            line_edit.setFont(font)
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for button in [self.ptnThanhtoan]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(10)
            button.setFont(font)

    def hien_thi_thong_tin(self):
        """Hiển thị thông tin lên các ô"""
        # Thông tin cơ bản
        self.ledHoten.setText(self.thong_tin.get('hoten', ''))
        self.ledSdt.setText(self.thong_tin.get('sdt', ''))
        self.ledTensach.setText(self.thong_tin.get('tensach', ''))
        self.ledMasach.setText(self.thong_tin.get('masach', ''))
        self.ledNgaymuon.setText(self.thong_tin.get('ngay_muon', ''))
        self.ledNgaytradk.setText(self.thong_tin.get('ngay_tra_du_kien', ''))
        
        # Ngày trả thực tế là hôm nay
        ngay_hom_nay = QDate.currentDate().toString("dd/MM/yyyy")
        self.ledNgaytratt.setText(ngay_hom_nay)
        
        # Tính số ngày quá hạn
        try:
            ngay_tra_du_kien = datetime.strptime(self.thong_tin.get('ngay_tra_du_kien', ''), '%d/%m/%Y')
            ngay_hom_nay_date = datetime.strptime(ngay_hom_nay, '%d/%m/%Y')
            so_ngay_qua_han = (ngay_hom_nay_date - ngay_tra_du_kien).days
            if so_ngay_qua_han < 0:
                so_ngay_qua_han = 0
        except:
            so_ngay_qua_han = 0
        
        self.ledSongayquahan.setText(str(so_ngay_qua_han))
        
        # Tính tiền phạt
        tien_phat = so_ngay_qua_han * 10000
        self.ledSotiencantra.setText(f"{tien_phat:,.0f} VNĐ")
        
        # Lưu lại
        self.so_ngay_qua_han = so_ngay_qua_han
        self.thong_tin['so_ngay_qua_han'] = so_ngay_qua_han
    
    def xu_ly_thanh_toan(self):
        """Xử lý khi bấm THANH TOÁN"""
        from main_thanhtoan2 import PenaltyTransferWindow
        self.next_window = PenaltyTransferWindow(self.thong_tin)
        self.next_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    thong_tin_mau = {
        'hoten': 'Nguyễn Văn A',
        'sdt': '0123456789',
        'tensach': 'Lập trình Python',
        'masach': 'PY001',
        'ngay_muon': '01/02/2026',
        'ngay_tra_du_kien': '15/02/2026'
    }
    window = PenaltyWindow(thong_tin_mau)
    window.show()
    sys.exit(app.exec())