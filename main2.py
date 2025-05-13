import sys
import sqlite3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QLineEdit,
    QListWidget, QMessageBox, QCheckBox, QListWidgetItem, QComboBox, QHBoxLayout
)
from PyQt5.QtGui import QPixmap, QFont, QIcon, QColor
from PyQt5.QtCore import Qt

APP_STYLESHEET = """
    /* Genel Stiller */
    QWidget {
        background-color: #f8f9fa;
        font-family: 'Segoe UI', Arial, sans-serif;
    }
    
    /* Mobil Kullanıcı Arayüzü için Özel Stiller */
    GirişFormu, AdresDurumuFormu, AdresEkleFormu {
        min-width: 360px;
        max-width: 480px;
        padding: 15px;
        background-color: #ffffff;
    }
    
    /* Masaüstü Yönetici Arayüzü için Özel Stiller */
    YoneticiPaneli, YoneticiGirisFormu {
        min-width: 800px;
        min-height: 600px;
        padding: 20px;
        background-color: #ffffff;
    }
    
    /* Başlık Stilleri */
    QLabel#title {
        font-size: 24px;
        font-weight: bold;
        color: #4a90e2;
        padding: 15px;
        margin-bottom: 20px;
        border-bottom: 3px solid #4a90e2;
        letter-spacing: 0.5px;
        text-align: center;
    }
    
    /* Buton Stilleri - Yeni Renk Şeması */
    QPushButton {
        background-color: #4a90e2;
        color: black;
        border: 2px solid #357abd;
        border-radius: 10px;
        padding: 12px 20px;
        font-size: 15px;
        font-weight: 600;
        min-width: 130px;
        margin: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        opacity: 1.0;
    }
    
    QPushButton:hover {
        color: black;
        background-color: #357abd;
        border-color: #2868a8;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        transform: translateY(-1px);
    }
    
    QPushButton:pressed {
        color: black;
        background-color: #2868a8;
        border-color: #1e4f82;
        box-shadow: inset 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Giriş/Kayıt Butonları */
    QPushButton#login_btn {
        color: black;
        background-color: #63c2de;
        border-color: #4fabc7;
    }
    
    QPushButton#login_btn:hover {
        color: black;
        background-color: #4fabc7;
        border-color: #3d94b0;
    }
    
    QPushButton#register_btn {
        color: black;
        background-color: #20c997;
        border-color: #1ba97f;
    }
    
    QPushButton#register_btn:hover {
        color: black;
        background-color: #1ba97f;
        border-color: #158765;
    }

    QPushButton#deprem_button {
        color: black;
        background-color: #dc3545;
        border-color: #c82333;
        font-weight: bold;
    }
    
    QPushButton#deprem_button:hover {
        color: black;
        background-color: #c82333;
        border-color: #bd2130;
    }
    
    /* Adres Formu Özel Stilleri */
    AdresDurumuFormu {
        background-color: #ffffff;
        margin: 10px;
        padding: 15px;
    }
    
    AdresDurumuFormu QPushButton {
        width: 200px;
        height: 35px;
        margin: 5px auto;
        display: block;
        font-size: 14px;
        font-weight: bold;
        text-align: center;
        opacity: 1.0;
        border: 1px solid #357abd;
        border-radius: 5px;
        padding: 5px 15px;
        color: black;
    }
    
    AdresDurumuFormu QPushButton#sirala_button {
        background-color: #63c2de;
        border-color: #4fabc7;
    }
    
    AdresDurumuFormu QPushButton#sirala_button::before {
        margin-right: 5px;
    }
    
    AdresDurumuFormu QPushButton#deprem_button {
        background-color: #ff0000;
        border-color: #cc0000;
        color: white;
    }
    
    AdresDurumuFormu QPushButton#deprem_button:hover {
        background-color: red;
    }
    
    AdresDurumuFormu QPushButton#deprem_button::before {
        margin-right: 5px;
    }
    
    AdresDurumuFormu QPushButton#adres_ekle_button {
        background-color: #20c997;
        border-color: #1ba97f;
    }
    
    AdresDurumuFormu QPushButton#adres_ekle_button::before {
        margin-right: 5px;
    }
    
    AdresDurumuFormu QPushButton#adresleri_listele_button {
        background-color: #4a90e2;
        border-color: #357abd;
    }
    
    AdresDurumuFormu QPushButton#adresleri_listele_button::before {
        margin-right: 5px;
    }
    
    QListWidget {
        background-color: #ffffff;
        border: 1px solid #e9ecef;
        padding: 15px;
        margin: 15px 0;
        min-height: 400px;
        font-size: 15px;
    }
    
    QListWidget::item {
        padding: 12px;
        border-bottom: 1px solid #e9ecef;
        margin: 3px 0;
        background-color: #f8f9fa;
    }
    
    QListWidget::item:selected {
        background-color: #ffebee;
        color: #dc3545;
        border-left: 3px solid #dc3545;
        font-weight: bold;
    }
    
    QListWidget::item::before {
        margin-right: 5px;
    }
    
    /* Input Alanları */
    QLineEdit, QComboBox, QTextEdit {
        background-color: #ffffff;
        border: none;
        border-bottom: 1px solid #e9ecef;
        padding: 12px;
        font-size: 15px;
        margin: 8px;
    }
    
    QLineEdit:focus, QComboBox:focus, QTextEdit:focus {
        border: none;
        border-bottom: 2px solid #4a90e2;
    }
    
    QLineEdit::placeholder {
        color: #a0aec0;
    }
    
    /* Kapak Sayfası */
    #welcome_screen {
        background: white;
    }
    
    #image_container {
        margin: 0;
        padding: 0;
    }

    #full_image {
        margin: 0;
        padding: 0;
        width: 100%;
        height: 100%;
    }
    
    #button_overlay {
        background-color: transparent;
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        padding: 20px;
    }
    
    #welcome_button {
        background-color: white;
        color: #4a90e2;
        border: 2px solid #4a90e2;
        font-size: 18px;
        font-weight: bold;
        padding: 10px 30px;
        border-radius: 12px;
        letter-spacing: 2px;
    }

    #welcome_button:hover {
        background-color: #f8f9fa;
        color: #357abd;
        border-color: #357abd;
    }

    #welcome_button:pressed {
        background-color: #e9ecef;
        color: #2868a8;
        border-color: #2868a8;
    }
    
    /* Mobil Responsive Düzenlemeler */
    @media (max-width: 1024px) {
        #welcome_screen {
            min-width: 360px;
            min-height: 640px;
        }

        #welcome_button {
            font-size: 14px;
            padding: 10px 20px;
        }
    }
    
    /* Masaüstü Yönetici Paneli Düzenlemeleri */
    #admin_panel {
        background-color: #f8f9fa;
        padding: 25px;
    }
    
    #admin_panel QListWidget {
        min-height: 400px;
    }
    
    #admin_panel QComboBox {
        min-width: 200px;
    }
    
    /* Adres Ekleme Formu Stilleri */
    AdresEkleFormu {
        background-color: white;
        border-radius: 15px;
        padding: 20px;
        margin: 10px;
    }
    
    AdresEkleFormu QLineEdit {
        background-color: #f8f9fa;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px;
        margin: 8px 0;
        font-size: 15px;
        width: 90%;
    }

    #bottom_container {
        padding: 30px 20px;
        background-color: #ffffff;
        border-top-left-radius: 25px;
        border-top-right-radius: 25px;
        margin: 0 10px;
    }

    #welcome_title {
        font-family: 'Segoe UI', Arial, sans-serif;
        font-size: 28px;
        font-weight: bold;
        color: #4a90e2;
        margin: 0 0 20px 0;
        letter-spacing: 1px;
    }

    #welcome_button {
        background-color: #4a90e2;
        color: white;
        border: none;
        font-size: 14px;
        font-weight: bold;
        padding: 8px 0;
        border-radius: 8px;
        margin: 5px 25px;
    }

    #welcome_button:hover {
        background-color: #357abd;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }

    /* Giriş Seçim Ekranı */
    #login_selection_screen {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1, 
                        stop:0 #4a90e2, stop:1 #63c2de);
    }

    #selection_button {
        background-color: white;
        color: #4a90e2;
        border: none;
        font-size: 18px;
        font-weight: bold;
        border-radius: 15px;
        padding: 20px 40px;
    }

    #selection_button:hover {
        background-color: #4a90e2;
        color: white;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
"""

def veritabani_baglan():
    return sqlite3.connect('adres.db')

def veritabani_olustur():
    conn = veritabani_baglan()
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS kullanicilar (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tc_kimlik TEXT UNIQUE,
                        ad_soyad TEXT,
                        sifre TEXT
                      )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adminler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        kullanici_adi TEXT UNIQUE,
                        sifre TEXT
                    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS adresler (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        tc_kimlik TEXT,
                        sehir TEXT,
                        ilce TEXT,
                        bina_adi TEXT,
                        adres TEXT,
                        telefon TEXT,
                        deprem_durumu TEXT DEFAULT 'güvende'
                    )''')
    conn.commit()
    conn.close()

class GirişFormu(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(APP_STYLESHEET)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Giriş / Kayıt')
        self.setGeometry(0, 0, 360, 640)

        self.ad_label = QLabel('Ad Soyad:')
        self.ad_input = QLineEdit()

        self.email_label = QLabel('E-Posta:')
        self.email_input = QLineEdit()

        self.telefon_label = QLabel('Telefon:')
        self.telefon_input = QLineEdit()

        self.tc_label = QLabel('TC Kimlik No:')
        self.tc_input = QLineEdit()

        self.sifre_label = QLabel('Şifre:')
        self.sifre_input = QLineEdit()
        self.sifre_input.setEchoMode(QLineEdit.Password)

        self.dogruluk_checkbox = QCheckBox('Bilgilerimin doğruluğundan eminim.')

        self.giris_button = QPushButton('Giriş Yap')
        self.giris_button.setObjectName("login_btn")
        self.kayit_button = QPushButton('Kayıt Ol')
        self.kayit_button.setObjectName("register_btn")

        self.giris_button.clicked.connect(self.giris_yap)
        self.kayit_button.clicked.connect(self.kayit_ol)

        layout = QVBoxLayout()
        layout.addWidget(self.ad_label)
        layout.addWidget(self.ad_input)
        layout.addWidget(self.email_label)
        layout.addWidget(self.email_input)
        layout.addWidget(self.telefon_label)
        layout.addWidget(self.telefon_input)
        layout.addWidget(self.tc_label)
        layout.addWidget(self.tc_input)
        layout.addWidget(self.sifre_label)
        layout.addWidget(self.sifre_input)
        layout.addWidget(self.dogruluk_checkbox)
        layout.addWidget(self.giris_button)
        layout.addWidget(self.kayit_button)

        self.setLayout(layout)

    def giris_yap(self):
        tc = self.tc_input.text()
        sifre = self.sifre_input.text()

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc_kimlik = ? AND sifre = ?", (tc, sifre))
        user = cursor.fetchone()
        conn.close()

        if user:
            self.adres_durumu_formu = AdresDurumuFormu(tc)
            self.adres_durumu_formu.show()
            self.hide()
        else:
            self.hata_mesaji('Giriş bilgileri hatalı!')

    def kayit_ol(self):
        if not self.dogruluk_checkbox.isChecked():
            self.hata_mesaji("Lütfen bilgilerin doğruluğunu onaylayınız.")
            return

        tc = self.tc_input.text()
        ad_soyad = self.ad_input.text()
        sifre = self.sifre_input.text()

        if not tc or not ad_soyad or not sifre:
            self.hata_mesaji("Lütfen tüm alanları doldurunuz!")
            return

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM kullanicilar WHERE tc_kimlik = ?", (tc,))
        user = cursor.fetchone()

        if user:
            self.hata_mesaji('Bu TC ile kayıtlı bir kullanıcı var!')
            conn.close()
        else:
            try:
                cursor.execute("INSERT INTO kullanicilar (tc_kimlik, ad_soyad, sifre) VALUES (?, ?, ?)", 
                             (tc, ad_soyad, sifre))
                conn.commit()
                conn.close()
                QMessageBox.information(self, 'Başarılı', 'Kayıt işlemi başarıyla tamamlandı!')
                self.adres_durumu_formu = AdresDurumuFormu(tc)
                self.adres_durumu_formu.show()
                self.hide()
            except Exception as e:
                self.hata_mesaji(f'Kayıt sırasında bir hata oluştu: {str(e)}')
                conn.close()

    def hata_mesaji(self, mesaj):
        QMessageBox.warning(self, 'Hata', mesaj)

class YoneticiGirisFormu(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet(APP_STYLESHEET)
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Yönetici Giriş')
        self.setGeometry(0, 0, 360, 640)
        
        layout = QVBoxLayout()
        
        title_label = QLabel("Yönetici Girişi")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        
        self.kullanici_adi = QLineEdit(placeholderText="Kullanıcı Adı")
        self.sifre = QLineEdit(placeholderText="Şifre", echoMode=QLineEdit.Password)
        self.giris_btn = QPushButton('Giriş Yap')
        self.giris_btn.setObjectName("login_btn")
        self.giris_btn.clicked.connect(self.giris_kontrol)
        
        layout.addWidget(title_label)
        layout.addWidget(self.kullanici_adi)
        layout.addWidget(self.sifre)
        layout.addWidget(self.giris_btn)
        
        self.setLayout(layout)

    def giris_kontrol(self):
        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM adminler WHERE kullanici_adi=? AND sifre=?", 
                      (self.kullanici_adi.text(), self.sifre.text()))
        if cursor.fetchone():
            self.yonetici_panel_ac()
        else:
            QMessageBox.warning(self, 'Hata', 'Geçersiz bilgiler!')
        conn.close()

    def yonetici_panel_ac(self):
        self.close()
        self.panel = YoneticiPaneli()
        self.panel.show()

class YoneticiPaneli(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("admin_panel")
        self.setStyleSheet(APP_STYLESHEET)
        self.initUI()
        self.adresleri_yukle()

    def initUI(self):
        self.setWindowTitle('Yönetici Paneli')
        self.setGeometry(0, 0, 800, 600)
        
        title_label = QLabel("Tüm Kayıtlı Adresler")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)
        
        self.liste = QListWidget()
        self.filtre_combo = QComboBox()
        self.filtre_combo.addItems(['Tümü', 'Güvende', 'Tehlikede'])
        self.filtre_combo.currentIndexChanged.connect(self.adresleri_yukle)
        
        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.filtre_combo)
        layout.addWidget(self.liste)
        
        self.setLayout(layout)

    def adresleri_yukle(self):
        self.liste.clear()
        conn = veritabani_baglan()
        cursor = conn.cursor()
        
        filtre = self.filtre_combo.currentText()
        
        if filtre == 'Tümü':
            cursor.execute("""
                SELECT a.*, k.ad_soyad 
                FROM adresler a 
                LEFT JOIN kullanicilar k ON a.tc_kimlik = k.tc_kimlik 
                WHERE a.deprem_durumu='tehlikede' 
                ORDER BY a.id DESC
            """)
            tehlikeli_adresler = cursor.fetchall()
            
            cursor.execute("""
                SELECT a.*, k.ad_soyad 
                FROM adresler a 
                LEFT JOIN kullanicilar k ON a.tc_kimlik = k.tc_kimlik 
                WHERE a.deprem_durumu='güvende' 
                ORDER BY a.id DESC
            """)
            güvenli_adresler = cursor.fetchall()
            
            for kayit in tehlikeli_adresler:
                ad_soyad = kayit[-1] if kayit[-1] else "İsimsiz Kullanıcı"
                item = QListWidgetItem(f"⚠️ TEHLİKEDE - {kayit[2]} - {kayit[4]} ({kayit[5]}) - {ad_soyad}")
                item.setData(Qt.UserRole, kayit)
                item.setBackground(QColor("#ffebee"))  # Açık kırmızı arka plan
                item.setForeground(QColor("#dc3545"))  
                font = item.font()
                font.setBold(True)
                item.setFont(font)
                self.liste.addItem(item)
            
            for kayit in güvenli_adresler:
                ad_soyad = kayit[-1] if kayit[-1] else "İsimsiz Kullanıcı"
                item = QListWidgetItem(f"✅ GÜVENDE - {kayit[2]} - {kayit[4]} ({kayit[5]}) - {ad_soyad}")
                item.setData(Qt.UserRole, kayit)
                item.setBackground(QColor("#e8f5e9"))  # Açık yeşil arka plan
                item.setForeground(QColor("#28a745"))  # Yeşil yazı rengi
                self.liste.addItem(item)
        else:
            durum = filtre.lower()
            cursor.execute("""
                SELECT a.*, k.ad_soyad 
                FROM adresler a 
                LEFT JOIN kullanicilar k ON a.tc_kimlik = k.tc_kimlik 
                WHERE a.deprem_durumu=? 
                ORDER BY a.id DESC
            """, (durum,))
            for kayit in cursor.fetchall():
                ad_soyad = kayit[-1] if kayit[-1] else "İsimsiz Kullanıcı"
                if durum == 'tehlikede':
                    item = QListWidgetItem(f"⚠️ TEHLİKEDE - {kayit[2]} - {kayit[4]} ({kayit[5]}) - {ad_soyad}")
                    item.setBackground(QColor("#ffebee"))
                    item.setForeground(QColor("#dc3545"))
                    font = item.font()
                    font.setBold(True)
                    item.setFont(font)
                else:
                    item = QListWidgetItem(f"✅ GÜVENDE - {kayit[2]} - {kayit[4]} ({kayit[5]}) - {ad_soyad}")
                    item.setBackground(QColor("#e8f5e9"))
                    item.setForeground(QColor("#28a745"))
                item.setData(Qt.UserRole, kayit)
                self.liste.addItem(item)
        
        conn.close()

class AdresDurumuFormu(QWidget):
    def __init__(self, tc):
        super().__init__()
        self.setStyleSheet(APP_STYLESHEET)
        self.tc = tc
        self.adresler = []
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Adres Durumu')
        self.setGeometry(0, 0, 360, 640)

        title_label = QLabel("Adres Durumu")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        self.adres_liste_widget = QListWidget()

        self.sirala_button = QPushButton('Adres Sıralama')
        self.deprem_button = QPushButton('Deprem Oldu')
        self.adres_ekle_button = QPushButton('Adres Ekle')
        self.adresleri_listele_button = QPushButton('Adresleri Listele')

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(self.adres_liste_widget)
        layout.addWidget(self.sirala_button)
        layout.addWidget(self.deprem_button)
        layout.addWidget(self.adres_ekle_button)
        layout.addWidget(self.adresleri_listele_button)

        self.sirala_button.clicked.connect(self.sirala)
        self.deprem_button.clicked.connect(self.deprem_oldu)
        self.adres_ekle_button.clicked.connect(self.adres_ekle)
        self.adresleri_listele_button.clicked.connect(self.adresleri_guncelle)

        self.setLayout(layout)
        self.adresleri_guncelle()

    def adresleri_guncelle(self):
        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("SELECT id, sehir, adres, bina_adi FROM adresler WHERE tc_kimlik = ?", (self.tc,))
        self.adresler = cursor.fetchall()
        conn.close()

        self.adres_liste_widget.clear()
        for adres in self.adresler:
            self.adres_liste_widget.addItem(f"{adres[1]} - {adres[2]} ({adres[3]})")

    def sirala(self):
        sorted_items = sorted(self.adresler, key=lambda x: x[2], reverse=True)
        self.adres_liste_widget.clear()
        for adres in sorted_items:
            self.adres_liste_widget.addItem(f"{adres[0]} - {adres[1]} ({adres[2]})")

    def adres_ekle(self):
        self.adres_ekleme_formu = AdresEkleFormu(self.tc, self)
        self.adres_ekleme_formu.show()

    def deprem_oldu(self):
        selected = self.adres_liste_widget.currentRow()
        if selected >= 0:
            msg = QMessageBox()
            msg.setWindowTitle("Güvenlik Durumu")
            msg.setText("Güvende misiniz?")
            msg.setIcon(QMessageBox.Question)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
            msg.setDefaultButton(QMessageBox.No)
            
            msg.button(QMessageBox.Yes).setText("Evet, güvendeyim")
            msg.button(QMessageBox.No).setText("Hayır, tehlikedeyim")
            
            msg.setStyleSheet("""
                QMessageBox {
                    background-color: white;
                }
                QPushButton {
                    padding: 10px 20px;
                    font-size: 14px;
                    border-radius: 5px;
                    min-width: 150px;
                }
                QPushButton[text="Evet, güvendeyim"] {
                    background-color: #28a745;
                    color: white;
                    border: none;
                }
                QPushButton[text="Hayır, tehlikedeyim"] {
                    background-color: #dc3545;
                    color: white;
                    border: none;
                }
            """)
            
            cevap = msg.exec_()
            
            adres_id = self.adresler[selected][0]
            conn = veritabani_baglan()
            cursor = conn.cursor()
            
            if cevap == QMessageBox.No:  
                cursor.execute("UPDATE adresler SET deprem_durumu='tehlikede' WHERE id=?", (adres_id,))
                conn.commit()
                
                bildirim = QMessageBox()
                bildirim.setWindowTitle("Acil Durum")
                bildirim.setText("Durumunuz acil yardım ekiplerine bildirildi!")
                bildirim.setIcon(QMessageBox.Warning)
                bildirim.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QPushButton {
                        background-color: #dc3545;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 5px;
                        border: none;
                    }
                    QLabel {
                        color: #dc3545;
                        font-weight: bold;
                    }
                """)
                bildirim.exec_()
            
            else:  
                cursor.execute("UPDATE adresler SET deprem_durumu='güvende' WHERE id=?", (adres_id,))
                conn.commit()
                
                bildirim = QMessageBox()
                bildirim.setWindowTitle("Bilgi")
                bildirim.setText("Güvende olduğunuz kaydedildi.")
                bildirim.setIcon(QMessageBox.Information)
                bildirim.setStyleSheet("""
                    QMessageBox {
                        background-color: white;
                    }
                    QPushButton {
                        background-color: #28a745;
                        color: white;
                        padding: 8px 16px;
                        border-radius: 5px;
                        border: none;
                    }
                    QLabel {
                        color: #28a745;
                        font-weight: bold;
                    }
                """)
                bildirim.exec_()
            
            conn.close()
            self.adresleri_guncelle()
        else:
            QMessageBox.warning(self, 'Hata', 'Lütfen bir adres seçin!')

class AdresEkleFormu(QWidget):
    def __init__(self, tc, parent_form=None):
        super().__init__()
        self.setStyleSheet(APP_STYLESHEET)
        self.tc = tc
        self.parent_form = parent_form
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Adres Ekleme')
        self.setGeometry(0, 0, 360, 640)

        title_label = QLabel("Yeni Adres Ekle")
        title_label.setObjectName("title")
        title_label.setAlignment(Qt.AlignCenter)

        self.sehir_input = QLineEdit()
        self.ilce_input = QLineEdit()
        self.bina_adi_input = QLineEdit()
        self.adres_input = QLineEdit()
        self.telefon_input = QLineEdit()

        self.kaydet_button = QPushButton('Kaydet')
        self.baska_adres_ekle_button = QPushButton('Başka Adres Ekle')
        self.adreslerimi_listele_button = QPushButton('Adreslerimi Listele')

        self.kaydet_button.clicked.connect(self.adres_kaydet)
        self.baska_adres_ekle_button.clicked.connect(self.baska_adres_ekle)
        self.adreslerimi_listele_button.clicked.connect(self.adresleri_listele)

        layout = QVBoxLayout()
        layout.addWidget(title_label)
        layout.addWidget(QLabel('Şehir:'))
        layout.addWidget(self.sehir_input)
        layout.addWidget(QLabel('İlçe:'))
        layout.addWidget(self.ilce_input)
        layout.addWidget(QLabel('Bina Adı:'))
        layout.addWidget(self.bina_adi_input)
        layout.addWidget(QLabel('Adres:'))
        layout.addWidget(self.adres_input)
        layout.addWidget(QLabel('Telefon:'))
        layout.addWidget(self.telefon_input)
        layout.addWidget(self.kaydet_button)
        layout.addWidget(self.baska_adres_ekle_button)
        layout.addWidget(self.adreslerimi_listele_button)

        self.setLayout(layout)

    def adres_kaydet(self):
        sehir = self.sehir_input.text()
        ilce = self.ilce_input.text()
        bina_adi = self.bina_adi_input.text()
        adres = self.adres_input.text()
        telefon = self.telefon_input.text()

        conn = veritabani_baglan()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO adresler (tc_kimlik, sehir, ilce, bina_adi, adres, telefon) VALUES (?, ?, ?, ?, ?, ?)",
                       (self.tc, sehir, ilce, bina_adi, adres, telefon))
        conn.commit()
        conn.close()
        QMessageBox.information(self, 'Adres Eklendi', 'Adres başarıyla kaydedildi!')
        if self.parent_form:
            self.parent_form.adresleri_guncelle()

    def baska_adres_ekle(self):
        self.sehir_input.clear()
        self.ilce_input.clear()
        self.bina_adi_input.clear()
        self.adres_input.clear()
        self.telefon_input.clear()

    def adresleri_listele(self):
        if self.parent_form:
            self.parent_form.adresleri_guncelle()
        self.close()

class KapakSayfasi(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("welcome_screen")
        self.setStyleSheet(APP_STYLESHEET)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Deprem Uygulaması")
        self.setFixedSize(360, 640)

        # Ana layout - kenar boşluklarını kaldırıyoruz
        main_layout = QVBoxLayout()
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # Resim container widget
        image_container = QWidget()
        image_container.setFixedSize(360, 640)
        image_container.setObjectName("image_container")

        # Resim - tam ekran
        self.resim_label = QLabel(image_container)
        self.resim_label.setGeometry(0, 0, 360, 640)  # Label'ı container boyutunda ayarla
        pixmap = QPixmap("DKU/kapakfoto.png")
        scaled_pixmap = pixmap.scaled(360, 640, Qt.IgnoreAspectRatio, Qt.SmoothTransformation)
        self.resim_label.setPixmap(scaled_pixmap)
        self.resim_label.setObjectName("full_image")

        # Buton container - en altta yarı saydam arka planla
        button_container = QWidget()
        button_container.setObjectName("button_overlay")
        button_layout = QVBoxLayout(button_container)
        button_layout.setContentsMargins(20, 20, 20, 40)

        # Devam butonu
        self.devam_button = QPushButton("DEVAM")
        self.devam_button.setObjectName("welcome_button")
        self.devam_button.setFixedSize(280, 60)
        self.devam_button.clicked.connect(self.devam_et)
        
        # Butonu container'a ekle
        button_layout.addWidget(self.devam_button, alignment=Qt.AlignBottom | Qt.AlignHCenter)

        # Ana layout'a widget'ları ekle
        main_layout.addWidget(image_container)
        main_layout.addWidget(button_container)

        self.setLayout(main_layout)

    def devam_et(self):
        self.giris_secim = GirisSecimFormu()
        self.giris_secim.show()
        self.close()

class GirisSecimFormu(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("login_selection_screen")
        self.setStyleSheet(APP_STYLESHEET)
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Giriş Seçimi")
        self.setFixedSize(800, 600)

        main_layout = QVBoxLayout()
        main_layout.setSpacing(20)
        main_layout.setAlignment(Qt.AlignCenter)

        baslik = QLabel("Giriş Türünü Seçiniz")
        baslik.setObjectName("title")
        baslik.setAlignment(Qt.AlignCenter)

        self.kullanici_button = QPushButton("Kullanıcı Girişi")
        self.kullanici_button.setObjectName("selection_button")
        self.kullanici_button.setFixedSize(300, 60)
        self.kullanici_button.clicked.connect(self.kullanici_girisi)

        self.yonetici_button = QPushButton("Yönetici Girişi")
        self.yonetici_button.setObjectName("selection_button")
        self.yonetici_button.setFixedSize(300, 60)
        self.yonetici_button.clicked.connect(self.yonetici_girisi)

        main_layout.addWidget(baslik)
        main_layout.addSpacing(30)
        main_layout.addWidget(self.kullanici_button, alignment=Qt.AlignCenter)
        main_layout.addSpacing(20)
        main_layout.addWidget(self.yonetici_button, alignment=Qt.AlignCenter)

        self.setLayout(main_layout)

    def kullanici_girisi(self):
        self.giris_formu = GirişFormu()
        self.giris_formu.show()
        self.close()

    def yonetici_girisi(self):
        self.yonetici_form = YoneticiGirisFormu()
        self.yonetici_form.show()
        self.close()

def main():
    veritabani_olustur()
    conn = veritabani_baglan()
    cursor = conn.cursor()
    
    # Önce admin kullanıcısını kontrol et
    cursor.execute("SELECT * FROM adminler WHERE kullanici_adi = 'admin'")
    admin = cursor.fetchone()
    
    # Eğer admin yoksa ekle
    if not admin:
        cursor.execute("INSERT INTO adminler (kullanici_adi, sifre) VALUES (?, ?)", ('admin', 'admin123'))
        conn.commit()
    
    conn.close()
    app = QApplication(sys.argv)
    kapak = KapakSayfasi()
    kapak.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()