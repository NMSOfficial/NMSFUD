import sys
import base64
import zlib
import random
import string
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog

def rastgele_string(uzunluk):
    karakterler = string.ascii_letters + string.digits
    return ''.join(random.choice(karakterler) for i in range(uzunluk))

class NMSFUD(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NMSFUD v3")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QtGui.QIcon('logo.png'))

        merkezi_widget = QtWidgets.QWidget()
        self.setCentralWidget(merkezi_widget)
        ana_dikey_düzen = QtWidgets.QVBoxLayout(merkezi_widget)

        self.logo = QtWidgets.QLabel(self)
        pixmap = QtGui.QPixmap('logo.png')
        self.logo.setPixmap(pixmap)
        self.logo.setAlignment(QtCore.Qt.AlignCenter)
        ana_dikey_düzen.addWidget(self.logo)

        self.dosya_buton = QtWidgets.QPushButton("Python Dosyası Seç")
        self.dosya_buton.clicked.connect(self.dosya_sec)
        ana_dikey_düzen.addWidget(self.dosya_buton)

        self.sonuc_label = QtWidgets.QLabel("")
        ana_dikey_düzen.addWidget(self.sonuc_label)

        self.mesaj_label = QtWidgets.QLabel("NMSHacking tarafından oluşturuldu. NMSHacking kötüye kullanımda sorumluluk kabul etmeyecek.")
        ana_dikey_düzen.addWidget(self.mesaj_label)
        self.mesaj_label.setAlignment(QtCore.Qt.AlignCenter)

    def dosya_sec(self):
        dosya_ad, _ = QFileDialog.getOpenFileName(self, "Python Dosyası Seç", "", "Python Dosyaları (*.py)")
        if dosya_ad:
            self.sifrele(dosya_ad)

    def sifrele(self, dosya_ad):
        with open(dosya_ad, "r") as f:
            orijinal_kod = f.read()

        # Import ifadelerini bul
        import_satirlari = []
        for satir in orijinal_kod.split('\n'):
            if satir.strip().startswith('import') or satir.strip().startswith('from'):
                import_satirlari.append(satir)

        # Şifreli kodu oluştur
        sikistirilmis_kod = zlib.compress(orijinal_kod.encode())
        encode_edilmis_kod = base64.b64encode(sikistirilmis_kod).decode()

        decode_fonksiyonu = '''
import base64
import zlib

{}
encoded_kod = "{}"
sikistirilmis_kod = base64.b64decode(encoded_kod)
orijinal_kod = zlib.decompress(sikistirilmis_kod).decode()
exec(orijinal_kod)
'''.format('\n'.join(import_satirlari), encode_edilmis_kod)

        obfuscate_edilmis_kod = decode_fonksiyonu.replace('encoded_kod', rastgele_string(10)).replace('sikistirilmis_kod', rastgele_string(10)).replace('orijinal_kod', rastgele_string(10))

        with open("obfuscate_edilmis_kod.py", "w") as f:
            f.write(obfuscate_edilmis_kod)

        self.sonuc_label.setText("Kod obfuscate edildi ve 'obfuscate_edilmis_kod.py' dosyasına kaydedildi.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pencere = NMSFUD()
    pencere.show()
    sys.exit(app.exec_())

