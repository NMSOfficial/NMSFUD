import sys
import base64
import zlib
import random
import string
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QVBoxLayout, QLabel, QComboBox, QTextEdit, QPushButton, QMessageBox, QFileDialog
import webbrowser

def rastgele_string(uzunluk):
    karakterler = string.ascii_letters + string.digits
    return ''.join(random.choice(karakterler) for i in range(uzunluk))

class NMSFUD(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("NMSFUD v3.5")
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

        # Kod İmzalama Dokümantasyonu butonu
        self.dokuman_buton = QtWidgets.QPushButton("Kod İmzalama Dokümantasyonu")
        self.dokuman_buton.clicked.connect(self.dokumantasyon_ac)
        ana_dikey_düzen.addWidget(self.dokuman_buton)

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

    def dokumantasyon_ac(self):
        webbrowser.open("https://learn.microsoft.com/tr-tr/dotnet/framework/tools/signtool-exe")

class HataPencere(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Hata Bildir")
        self.setGeometry(100, 100, 400, 300)

        self.layout = QVBoxLayout(self)

        self.email_label = QLabel("Hangi e-mail servisiyle hata bildirmek istiyorsunuz?")
        self.layout.addWidget(self.email_label)

        self.email_servisleri = QComboBox(self)
        self.email_servisleri.addItems(["Gmail", "Outlook", "Yahoo", "ProtonMail", "Zoho", "Yandex", "GMX", "AOL", "Mail.com", "iCloud"])
        self.layout.addWidget(self.email_servisleri)

        self.hata_label = QLabel("Aldığınız Hatayı Anlatın:")
        self.layout.addWidget(self.hata_label)

        self.hata_metni = QTextEdit(self)
        self.layout.addWidget(self.hata_metni)

        self.ekran_goruntusu_label = QLabel("Karşılaştığınız Hatanın Ekran Görüntüsü (opsiyonel):")
        self.layout.addWidget(self.ekran_goruntusu_label)

        self.ekran_goruntusu_buton = QPushButton("Dosya Seç", self)
        self.ekran_goruntusu_buton.clicked.connect(self.dosya_sec)
        self.layout.addWidget(self.ekran_goruntusu_buton)

        self.gonder_buton = QPushButton("Gönder", self)
        self.gonder_buton.clicked.connect(self.gonder)
        self.layout.addWidget(self.gonder_buton)

        self.dosya_yolu = None

    def dosya_sec(self):
        dosya_ad, _ = QFileDialog.getOpenFileName(self, "Ekran Görüntüsü Seç", "", "Resim Dosyaları (*.png *.jpg *.jpeg *.bmp)")
        if dosya_ad:
            self.dosya_yolu = dosya_ad

    def gonder(self):
        email_servisi = self.email_servisleri.currentText()
        hata_metni = self.hata_metni.toPlainText()

        if not hata_metni:
            QMessageBox.warning(self, "Hata", "Lütfen hatayı açıklayın.")
            return

        mesaj = f"E-posta Servisi: {email_servisi}\n\nHata Açıklaması:\n{hata_metni}"
        if self.dosya_yolu:
            with open(self.dosya_yolu, "rb") as file:
                dosya_adi = self.dosya_yolu.split("/")[-1]
                dosya_icerik = file.read()
                dosya_base64 = base64.b64encode(dosya_icerik).decode()

            mesaj += f"\n\nEkran Görüntüsü: {dosya_adi}\nLütfen dosyanızı aşağıdan yükleyiniz. Bu mail servisi doğrudan içerik yüklemesine izin vermemektedir."

        url = ""
        if email_servisi == "Gmail":
            url = f"https://mail.google.com/mail/?view=cm&fs=1&to=nms@workmail.com&su=Hata Bildirimi&body={mesaj}"
        elif email_servisi == "Outlook":
            url = f"https://outlook.live.com/owa/?path=/mail/action/compose&to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "Yahoo":
            url = f"https://compose.mail.yahoo.com/?to=nms@workmail.com&subj=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "ProtonMail":
            url = f"https://mail.protonmail.com/compose?to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "Zoho":
            url = f"https://mail.zoho.com/zm/#compose/to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "Yandex":
            url = f"https://mail.yandex.com/compose?mailto=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "GMX":
            url = f"https://www.gmx.com/mail/compose?to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "AOL":
            url = f"https://mail.aol.com/webmail-std/en-us/compose?to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "Mail.com":
            url = f"https://www.mail.com/mail/compose/?to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"
        elif email_servisi == "iCloud":
            url = f"https://www.icloud.com/mail/compose?to=nms@workmail.com&subject=Hata%20Bildirimi&body={mesaj}"

        webbrowser.open(url)
        QMessageBox.information(self, "Başarılı", "Tarayıcınızda yeni bir sekme açıldı ve hata bildiriminiz oluşturuldu.")

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    pencere = NMSFUD()
    hata_pencere = HataPencere()  # HataPencere sınıfı oluşturuldu
    pencere.show()
    hata_pencere.show()  # Hata bildirme ekranı gösterildi
    sys.exit(app.exec_())

