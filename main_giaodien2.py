import sys
from PyQt6.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt6 import uic
from PyQt6.QtCore import QDate, Qt
from datetime import datetime
import giaodien2_rc

class TimeInfoWindow(QMainWindow):
    def __init__(self, thong_tin):
        super().__init__()
        uic.loadUi("giaodien2.ui", self)
        
        self.fix_font()
        self.thong_tin = thong_tin
        self.next_window = None
        
        #Hiển thị ngày tháng từ màn hình mượn sách
        self.hien_thi_ngay_tu_form_truoc()

        #Tính số ngày tự động
        self.tinh_so_ngay()
        
        # Tính tiền
        self.tinh_tien()
        
        # Kết nối sự kiện
        self.ptnThanhtoan.clicked.connect(self.xu_ly_thanh_toan)
        self.ptnquaylai2.clicked.connect(self.quay_lai)
        
        # Kết nối sự kiện thay đổi ngày
        self.ledngaythue.textChanged.connect(self.tinh_so_ngay)
        self.ledngaytra.textChanged.connect(self.tinh_so_ngay)
        self.ledsongaythue.textChanged.connect(self.tinh_tien)

    def fix_font(self):
        for label in [self.lblNgaythue, self.lblNgaytra, self.lblSongaythue, self.lblTongtien]:
            font = label.font()
            font.setBold(True)
            font.setPointSize(10)
            label.setFont(font)
        for line_edit in [self.ledngaythue, self.ledngaytra, self.ledsongaythue, self.ledTongtien]:
            font = line_edit.font()
            font.setBold(True)
            font.setPointSize(8)
            line_edit.setFont(font)
            line_edit.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for button in [self.ptnThanhtoan]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(12)
            button.setFont(font)
        for button in [self.ptnquaylai2]:
            font = button.font()
            font.setBold(True)
            font.setPointSize(10)
            button.setFont(font)
    
    def hien_thi_ngay_tu_form_truoc(self):
        """Hiển thị ngày tháng đã nhập từ màn hình mượn sách"""
        if 'ngay_muon' in self.thong_tin:
            self.ledngaythue.setText(self.thong_tin['ngay_muon'])
        
        if 'ngay_tra' in self.thong_tin:
            self.ledngaytra.setText(self.thong_tin['ngay_tra'])
    
    def tinh_so_ngay(self):
        """Tính số ngày thuê dựa trên ngày mượn và ngày trả"""
        try:
            ngay_muon_str = self.ledngaythue.text().strip()
            ngay_tra_str = self.ledngaytra.text().strip()
            
            if ngay_muon_str and ngay_tra_str:
                # Chuyển đổi string sang datetime
                ngay_muon = datetime.strptime(ngay_muon_str, '%d/%m/%Y')
                ngay_tra = datetime.strptime(ngay_tra_str, '%d/%m/%Y')
                
                # Tính số ngày
                so_ngay = (ngay_tra - ngay_muon).days
                
                if so_ngay > 0:
                    self.ledsongaythue.setText(str(so_ngay))
                else:
                    self.ledsongaythue.setText("0")
                    QMessageBox.warning(None, "Lỗi", "Ngày trả phải sau ngày mượn!")
            else:
                self.ledsongaythue.setText("0")
                
        except Exception as e:
            self.ledsongaythue.setText("0")
            print(f"Lỗi tính ngày: {e}")
        
        # Tính lại tiền sau khi tính số ngày
        self.tinh_tien()

    def tinh_tien(self):
        """Tính tổng tiền dựa trên số ngày"""
        try:
            so_ngay = int(self.ledsongaythue.text()) if self.ledsongaythue.text() else 0
            tong_tien = so_ngay * 10000 + 100000  # 10k/ngày + 100k cọc
            self.ledTongtien.setText(f"{tong_tien:,.0f} VNĐ")
            return tong_tien
        except:
            self.ledTongtien.setText("0 VNĐ")
            return 0
    
    def lay_thong_tu_form(self):
        """Lấy thông tin thời gian từ form"""
        ngay_thue = self.ledngaythue.text().strip()
        ngay_tra = self.ledngaytra.text().strip()
        
        try:
            so_ngay = int(self.ledsongaythue.text()) if self.ledsongaythue.text() else 0
        except:
            so_ngay = 0
        
        # Kiểm tra ngày hợp lệ
        if not ngay_thue or not ngay_tra:
            QMessageBox.warning(None, "Lỗi", "Vui lòng nhập đầy đủ ngày tháng!")
            return None
        
        return {
            'ngay_muon': ngay_thue,
            'ngay_tra': ngay_tra,
            'so_ngay': so_ngay
        }
    
    def xu_ly_thanh_toan(self):
        """Xử lý khi bấm nút THANH TOÁN"""
        thong_tin_thoi_gian = self.lay_thong_tu_form()
        # Cập nhật thông tin
        self.thong_tin['ngay_muon'] = self.ledngaythue.text().strip()
        self.thong_tin['ngay_tra'] = self.ledngaytra.text().strip()
        self.thong_tin['so_ngay'] = int(self.ledsongaythue.text()) if self.ledsongaythue.text() else 0
        self.thong_tin['tong_tien'] = self.tinh_tien()
            
        # Chuyển sang màn hình điều khoản
        from main_dieukhoan import TermsWindow
        self.next_window = TermsWindow(self.thong_tin)
        self.next_window.show()
        self.close()
    
    def quay_lai(self):
        """Quay lại màn hình trước"""
        from main_giaodien1 import CustomerInfoWindow
        self.next_window = CustomerInfoWindow(self.thong_tin)
        self.next_window.show()
        self.close()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = TimeInfoWindow()
    window.show()

    sys.exit(app.exec())
