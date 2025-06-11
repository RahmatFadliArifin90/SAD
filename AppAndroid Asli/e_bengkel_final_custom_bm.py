
import os
import pandas as pd
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from mlxtend.frequent_patterns import apriori, association_rules

Window.size = (360, 640)

def boyer_moore_search(text, pattern):
    m = len(pattern)
    n = len(text)
    if m == 0:
        return 0
    bad_char = [-1] * 256
    for i in range(m):
        bad_char[ord(pattern[i])] = i
    s = 0
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return s
        else:
            s += max(1, j - bad_char[ord(text[s + j])])
    return -1



transactions = [
    ['Oli Motor', 'Ban Motor', 'Filter Udara'],
    ['Paket Ganti Oli', 'Oli Motor', 'Ban Motor'],
    ['Oli Motor', 'Radiator Mobil', 'Kampas Rem'],
    ['Knalpot Racing', 'Ban Motor', 'Paket Ganti Oli'],
    ['Aki Mobil', 'Filter Udara', 'Pompa Oli'],
    ['Oli Motor', 'Paket Ganti Oli'],
    ['Lampu Depan Motor', 'Busi Motor', 'Ban Motor'],
    ['Paket Ganti Oli', 'Kampas Rem', 'Oli Motor'],
    ['Saringan Bensin', 'Aki Mobil', 'Kampas Rem'],
    ['Radiator Mobil', 'Oli Motor', 'Paket Ganti Oli'],
]

products = [
    {"name": "Oli Motor", "price": "Rp. 100.000", "image": "oli.png"},
    {"name": "Ban Motor", "price": "Rp. 250.000", "image": "ban.png"},
    {"name": "Filter Udara", "price": "Rp. 50.000", "image": "filter.png"},
    {"name": "Paket Ganti Oli", "price": "Rp. 150.000", "image": "ganti_oli.png"},
    {"name": "Accu Motor", "price": "Rp. 400.000", "image": "accu.png"},
    {"name": "Kampas Rem", "price": "Rp. 75.000", "image": "kampas_rem.png"},
    {"name": "Busi Motor", "price": "Rp. 30.000", "image": "busi.png"},
    {"name": "Lampu Depan", "price": "Rp. 40.000", "image": "lampu_depan.png"},
    {"name": "Aki Mobil", "price": "Rp. 650.000", "image": "aki_mobil.png"},
    {"name": "Knalpot Racing", "price": "Rp. 500.000", "image": "knalpot.png"},
    {"name": "Radiator Mobil", "price": "Rp. 700.000", "image": "radiator.png"},
    {"name": "Pompa Oli", "price": "Rp. 200.000", "image": "pompa_oli.png"},
    {"name": "Saringan Bensin", "price": "Rp. 45.000", "image": "saringan_bensin.png"},
    {"name": "Paket Servis Lengkap", "price": "Rp. 350.000", "image": "servis_lengkap.png"},
    {"name": "Shockbreaker Belakang", "price": "Rp. 300.000", "image": "shockbreaker.png"}
]

promos = [
    "Promo Ganti Oli - Diskon 20% (26 Mei)",
    "Diskon Ban Motor - Rp. 50.000 Off (28 Mei)",
    "Servis Lengkap Gratis Cuci Motor (30 Mei)"
]

knowledge_base = [
    {"key": "motor mati tiba-tiba", "answer": "Motor bisa mati tiba-tiba karena bensin habis, aki lemah, busi rusak, atau masalah kelistrikan."},
    {"key": "ganti oli", "answer": "Gantilah oli setiap 2000–3000 km atau sebulan sekali, tergantung pemakaian."},
    {"key": "ban bocor", "answer": "Ban bocor bisa karena tertusuk benda tajam, tekanan angin tidak stabil, atau keausan."},
    {"key": "lampu mati", "answer": "Periksa bohlam, soket, sekring, atau kabel. Bisa jadi salah satunya rusak."},
    {"key": "rem bunyi", "answer": "Kemungkinan kampas rem aus atau kotor. Periksa juga cakram rem."},
    {"key": "motor susah nyala", "answer": "Periksa aki, busi, dan bensin. Jika tidak berhasil, cek sistem starter atau pengapian."},
    {"key": "servis berkala", "answer": "Servis berkala disarankan setiap 3.000–5.000 km atau setiap 3 bulan."},
    {"key": "oli terbaik", "answer": "Gunakan oli sesuai rekomendasi pabrik. Untuk motor matic, pilih oli matic dengan SAE yang sesuai."},
    {"key": "oli rembes", "answer": "Oli yang rembes bisa karena seal bocor. Segera bawa ke bengkel sebelum merusak komponen lain."}
]

def apriori_recommendations(transactions):
    df = pd.DataFrame(transactions)
    onehot = pd.get_dummies(df.stack()).groupby(level=0).max()
    frequent_itemsets = apriori(onehot, min_support=0.3, use_colnames=True)
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    recommendations = set()
    for item in rules['consequents']:
        for i in item:
            recommendations.add(i)
    return list(recommendations)[:5]

def get_chatbot_response(text):
    text_lower = text.lower()

    # Cek produk
    for p in products:
        product_name = p["name"].lower()
        if boyer_moore_search(text_lower, product_name) != -1:
            return f"{p['name']} tersedia dengan harga {p['price']}."
    for item in knowledge_base:
        if boyer_moore_search(text_lower, item["key"]) != -1:
            return item["answer"]

    # Jawaban umum seputar otomotif (diperluas kata kuncinya)
    if "motor" in text_lower and ("mati" in text_lower or "tiba-tiba" in text_lower):
        return "Motor bisa mati tiba-tiba karena bensin habis, aki lemah, busi rusak, atau masalah kelistrikan."
    elif "ganti oli" in text_lower or ("oli" in text_lower and "kapan" in text_lower):
        return "Gantilah oli setiap 2000–3000 km atau sebulan sekali, tergantung pemakaian."
    elif "ban bocor" in text_lower or ("ban" in text_lower and "bocor" in text_lower):
        return "Ban bocor bisa karena tertusuk benda tajam, tekanan angin tidak stabil, atau keausan."
    elif "lampu" in text_lower and ("mati" in text_lower or "tidak nyala" in text_lower):
        return "Periksa bohlam, soket, sekring, atau kabel. Bisa jadi salah satunya rusak."
    elif "rem" in text_lower and "bunyi" in text_lower:
        return "Kemungkinan kampas rem aus atau kotor. Periksa juga cakram rem."
    elif "motor" in text_lower and ("susah nyala" in text_lower or "sulit dinyalakan" in text_lower):
        return "Periksa aki, busi, dan bensin. Jika tidak berhasil, cek sistem starter atau pengapian."
    elif "servis" in text_lower and "berkala" in text_lower:
        return "Servis berkala disarankan setiap 3.000–5.000 km atau setiap 3 bulan."
    elif "oli terbaik" in text_lower or ("oli" in text_lower and "bagus" in text_lower):
        return "Gunakan oli sesuai rekomendasi pabrik. Untuk motor matic, pilih oli matic dengan SAE yang sesuai."
    elif "oli" in text_lower and "rembes" in text_lower:
        return "Oli yang rembes bisa karena seal bocor. Segera bawa ke bengkel sebelum merusak komponen lain."

    # Default
    return "Maaf, saya belum bisa menjawab pertanyaan itu. Silakan coba pertanyaan lain seputar otomotif."


class E_BengkelApp(App):
    def build(self):
        self.cart = []  # ← Tambahan
        self.root = BoxLayout(orientation='vertical')
        self.main_content = BoxLayout(orientation='vertical', size_hint=(1, 0.9))
        self.search_input = None
        self.current_page = "home"
        self.root.add_widget(self.main_content)
        self.root.add_widget(self.build_bottom_nav())
        self.show_home(None)
        return self.root

    def add_search_bar(self, placeholder, search_func):
        bar = BoxLayout(size_hint_y=None, height=40)
        self.search_input = TextInput(hint_text=placeholder, multiline=False, size_hint=(1, 1))
        self.search_input.bind(on_text_validate=search_func)
        bar.add_widget(self.search_input)
        self.main_content.add_widget(bar)

    def build_bottom_nav(self):
        nav = BoxLayout(size_hint=(1, 0.1))
        nav.add_widget(Button(text="Beranda", on_press=self.show_home))
        nav.add_widget(Button(text="Toko", on_press=self.show_products))
        nav.add_widget(Button(text="Chatbot", on_press=self.open_chatbot))
        nav.add_widget(Button(text="Notifikasi", on_press=self.show_notifications))
        nav.add_widget(Button(text="Profil", on_press=self.show_profile))
        return nav

    def show_products(self, instance):
        self.main_content.clear_widgets()
        self.current_page = "toko"
        self.add_search_bar("Cari produk di toko...", self.search_store)

        scroll = ScrollView()
        layout = GridLayout(cols=1, spacing=5, padding=5, size_hint_y=None)
        layout.bind(minimum_height=layout.setter('height'))

        for p in products:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=100, spacing=10)

            img = Image(source=p["image"], size_hint=(None, None), size=(60, 60)) \
                if os.path.exists(p["image"]) else Label(text="🛠️")
            box.add_widget(img)

            info = Label(text=f"{p['name']}\n{p['price']}", halign='left')
            box.add_widget(info)

            actions = BoxLayout(orientation='vertical', size_hint_x=0.5)
            actions.add_widget(Button(text="Pesan", size_hint_y=0.5,
                                      on_press=lambda instance, prod=p: self.show_order_page(prod)))
            actions.add_widget(Button(text="Keranjang", size_hint_y=0.5,
                                      on_press=lambda instance, prod=p: self.handle_cart(prod)))

            box.add_widget(actions)
            layout.add_widget(box)

        scroll.add_widget(layout)
        self.main_content.add_widget(scroll)
        
    def show_cart(self, instance):
        self.main_content.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="🛒 Keranjang Saya", size_hint_y=None, height=40))
    
        total = 0
        for item in self.cart:
            box = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
            img = Image(source=item["image"], size_hint=(None, None), size=(60, 60)) if os.path.exists(item["image"]) else Label(text="🛠️")
            box.add_widget(img)
            box.add_widget(Label(text=f"{item['name']}\n{item['price']}"))
            layout.add_widget(box)
        
            try:
                total += int(item['price'].replace("Rp.", "").replace(".", "").strip())
            except:
                pass
    
        layout.add_widget(Label(text=f"Total: Rp{total:,}".replace(",", ".")))
        layout.add_widget(Button(text="Checkout", size_hint_y=None, height=40))
        self.main_content.add_widget(layout)
        
    def show_order_page(self, product):
        self.main_content.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        img = Image(source=product["image"], size_hint=(None, None), size=(200, 200)) if os.path.exists(product["image"]) else Label(text="🛠️")
        layout.add_widget(img)
        layout.add_widget(Label(text=product["name"], font_size=20))
        layout.add_widget(Label(text=f"Harga: {product['price']}"))
        layout.add_widget(Label(text="Cicilan 0% - Tersedia PayLater"))
        layout.add_widget(Button(text="Beli Sekarang", on_press=lambda x: self.confirm_order(product)))
        layout.add_widget(Button(text="Kembali", on_press=self.show_products))
        self.main_content.add_widget(layout)

    def confirm_order(self, product):
        popup = Popup(title="Konfirmasi Pesanan",
                      content=Label(text=f"Pesanan {product['name']} berhasil dibuat!"),
                      size_hint=(0.7, 0.3))
        popup.open()

    def add_to_cart(self, product):
        popup = Popup(title="Keranjang",
                      content=Label(text=f"{product['name']} telah ditambahkan ke keranjang."),
                      size_hint=(0.7, 0.3))
        popup.open()

    def show_notifications(self, instance):
        self.main_content.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        layout.add_widget(Label(text="Promo Tersedia", size_hint_y=None, height=30))
        for p in promos:
            layout.add_widget(Label(text=p))
        self.main_content.add_widget(layout)

    def handle_order(self, product):
        popup = Popup(title="Pesan Produk",
                      content=Label(text=f"Anda memesan: {product['name']} seharga {product['price']}"),
                      size_hint=(0.7, 0.3))
        popup.open()

    def handle_cart(self, product):
        self.cart.append(product)  # ← simpan ke list keranjang
        popup = Popup(title="Keranjang",
                      content=Label(text=f"{product['name']} telah ditambahkan ke keranjang."),
                      size_hint=(0.7, 0.3))
        popup.open()

    def show_home(self, instance):
        self.main_content.clear_widgets()
        self.current_page = "home"
        self.add_search_bar("Cari rekomendasi...", self.search_home)

        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)

    # Tambahkan tombol keranjang di kanan atas
        top = BoxLayout(size_hint_y=None, height=50, padding=[0, 0, 10, 0])
        top.add_widget(Label(text="Beranda", size_hint_x=0.9))
        cart_btn = Button(text="🛒", size_hint_x=0.1)
        cart_btn.bind(on_press=self.show_cart)
        top.add_widget(cart_btn)
        
        layout.add_widget(top)
        
        layout.add_widget(Label(text="Rekomendasi Produk", size_hint_y=None, height=30))
        for r in apriori_recommendations(transactions):
            for p in products:
                if p["name"] == r:
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
                    img = Image(source=p["image"], size_hint=(None, None), size=(60, 60)) if os.path.exists(p["image"]) else Label(text="🛠️")
                    box.add_widget(img)
                    box.add_widget(Label(text=f"{p['name']}\n{p['price']}"))
                    layout.add_widget(box)
        self.main_content.add_widget(layout)

    def search_home(self, instance):
        keyword = self.search_input.text.lower()
        result = [p for p in apriori_recommendations(transactions) if keyword in p.lower()]
        self.show_search_result(result)

    def search_store(self, instance):
        keyword = self.search_input.text.lower()
        result = [p["name"] for p in products if keyword in p["name"].lower()]
        self.show_search_result(result)

    def show_search_result(self, names):
        layout = BoxLayout(orientation='vertical', spacing=5, padding=5)
        layout.add_widget(Label(text="Hasil Pencarian", size_hint_y=None, height=30))
        for name in names:
            for p in products:
                if p["name"] == name:
                    box = BoxLayout(orientation='horizontal', size_hint_y=None, height=80, spacing=10)
                    img = Image(source=p["image"], size_hint=(None, None), size=(60, 60)) if os.path.exists(p["image"]) else Label(text="🛠️")
                    box.add_widget(img)
                    box.add_widget(Label(text=f"{p['name']}\n{p['price']}"))
                    layout.add_widget(box)
        self.main_content.clear_widgets()
        if self.current_page == "home":
            self.add_search_bar("Cari rekomendasi...", self.search_home)
        elif self.current_page == "toko":
            self.add_search_bar("Cari produk di toko...", self.search_store)
        self.main_content.add_widget(layout)

    def open_chatbot(self, instance):
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.chat_history = BoxLayout(orientation='vertical', size_hint_y=None, height=300)
        scroll = ScrollView(size_hint=(1, None), height=300)
        scroll.add_widget(self.chat_history)
        self.user_input = TextInput(hint_text="Tulis pertanyaan", size_hint=(1, None), height=40)
        self.user_input.bind(on_text_validate=self.on_enter)
        send_button = Button(text="Kirim", size_hint=(1, None), height=40)
        send_button.bind(on_press=self.on_enter)
        popup_layout.add_widget(scroll)
        popup_layout.add_widget(self.user_input)
        popup_layout.add_widget(send_button)
        self.popup = Popup(title="Chatbot", content=popup_layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def on_enter(self, instance):
        text = self.user_input.text
        self.user_input.text = ''
        self.chat_history.add_widget(Label(text=f"You: {text}", size_hint_y=None, height=30))
        response = get_chatbot_response(text)
        print("DEBUG - RESPONSE:", response)  # ← Debug
        self.chat_history.add_widget(Label(text=f"Chatbot: {response}", size_hint_y=None, height=30))


    def show_notifications(self, instance):
        self.main_content.clear_widgets()
        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(Label(text="📢 Promo Terkini", size_hint_y=None, height=30))
        for promo in promos:
            layout.add_widget(Label(text=promo, size_hint_y=None, height=30))
        self.main_content.add_widget(layout)

    def show_profile(self, instance):
        self.main_content.clear_widgets()
        layout = BoxLayout(orientation='vertical', spacing=10, padding=10)
        profile_pic = Image(source="profile.png", size_hint=(None, None), size=(100, 100))
        center = AnchorLayout(anchor_x='center', anchor_y='top')
        center.add_widget(profile_pic)
        layout.add_widget(center)
        layout.add_widget(Label(text="Chrislin_", font_size=20))
        layout.add_widget(Label(text="Saldo: Rp. 1.500.000", size_hint_y=None, height=30))
        buttons = BoxLayout(size_hint_y=None, height=40)
        buttons.add_widget(Button(text="Edit Profil"))
        buttons.add_widget(Button(text="Bagikan Profil"))
        layout.add_widget(buttons)
        layout.add_widget(Label(text="Riwayat Transaksi", size_hint_y=None, height=30))
        layout.add_widget(Label(text="• Ganti Oli - 24 Mei"))
        layout.add_widget(Label(text="• Beli Kampas Rem - 22 Mei"))
        layout.add_widget(Label(text="• Servis Lengkap - 20 Mei"))
        self.main_content.add_widget(layout)

if __name__ == '__main__':
    E_BengkelApp().run()
