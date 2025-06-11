import random
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.popup import Popup
from kivy.core.window import Window
import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules

# Mengatur ukuran layar dan latar belakang
Window.size = (360, 640)
Window.clearcolor = (1, 1, 1, 1)  # Latar belakang putih

# Simulated transaction data for Apriori
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

# Convert the transactions into a DataFrame
def generate_transactions_dataframe(transactions):
    # Membuat dataframe dari transaksi
    df = pd.DataFrame(transactions, columns=['Item1', 'Item2', 'Item3'])
    return df

# Applying Apriori algorithm
def apriori_recommendations(transactions):
    df = generate_transactions_dataframe(transactions)
    
    # One-hot encoding of the transactions
    onehot = pd.get_dummies(df.stack()).groupby(level=0).max()
    
    # Apply Apriori algorithm
    frequent_itemsets = apriori(onehot, min_support=0.3, use_colnames=True)
    
    # Generate association rules
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=1)
    
    return rules

# Boyer-Moore Algorithm for String Matching
def boyer_moore(text, pattern):
    m = len(pattern)
    n = len(text)
    
    # Create the bad character table
    bad_char = [-1] * 256
    for i in range(m):
        bad_char[ord(pattern[i])] = i

    s = 0  # Shift of the pattern with respect to text
    while s <= n - m:
        j = m - 1
        while j >= 0 and pattern[j] == text[s + j]:
            j -= 1
        if j < 0:
            return True  # Match found
            s += (m - bad_char[ord(text[s + m])] if s + m < n else 1)
        else:
            s += max(1, j - bad_char[ord(text[s + j])])

    return False  # No match found

class E_BengkelApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # BoxLayout for main content
        box_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, 0.8))

        # Label for the main page title
        label = Label(text="Selamat datang di E-Bengkel!", size_hint=(1, None), height=50, font_size=18, bold=True, color=(0, 0, 0, 1))
        box_layout.add_widget(label)

        # Description of the app
        description_label = Label(text="Aplikasi E-Bengkel untuk memenuhi kebutuhan perawatan dan penggantian suku cadang kendaraan Anda. Temukan produk berkualitas dan layanan terbaik.",
                                  size_hint=(1, None), font_size=14, color=(0, 0, 0, 1), halign="center", valign="middle")

        # Wrap description label inside ScrollView
        scrollview = ScrollView(size_hint=(1, None), height=description_label.texture_size[1])
        scrollview.add_widget(description_label)
        box_layout.add_widget(scrollview)

        # Chatbot Button
        chatbot_button = Button(text="Buka Chatbot", size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        chatbot_button.bind(on_press=self.open_chatbot)
        box_layout.add_widget(chatbot_button)

        # Products and services button
        products_button = Button(text="Lihat Produk & Layanan", size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'center_y': 0.2})
        products_button.bind(on_press=self.show_products_and_services)
        box_layout.add_widget(products_button)
        
        # Recommend Button
        recommend_button = Button(text="Lihat Rekomendasi", size_hint=(None, None), size=(250, 50), pos_hint={'center_x': 0.5, 'center_y': 0.3})
        recommend_button.bind(on_press=self.show_recommendations)
        box_layout.add_widget(recommend_button)

        # Adding BoxLayout to FloatLayout
        self.layout.add_widget(box_layout)

        return self.layout

    def open_chatbot(self, instance):
        self.chatbot_popup()

    def chatbot_popup(self):
        # Popup for Chatbot
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)

        # Scrollable area for the chat history
        self.chat_history = BoxLayout(orientation='vertical', size_hint_y=None, height=400)
        self.chat_history_scroll = ScrollView(size_hint=(1, None), height=400)
        self.chat_history_scroll.add_widget(self.chat_history)

        # Text input for user query
        self.user_input = TextInput(hint_text="Tulis pertanyaan", size_hint=(1, None), height=40)
        self.user_input.bind(on_text_validate=self.on_enter)

        # Send button
        send_button = Button(text="Kirim", size_hint=(1, None), height=40)
        send_button.bind(on_press=self.on_enter)

        # Add all elements to the popup layout
        popup_layout.add_widget(self.chat_history_scroll)
        popup_layout.add_widget(self.user_input)
        popup_layout.add_widget(send_button)

        # Create and display the popup
        self.popup = Popup(title="Chatbot", content=popup_layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def on_enter(self, instance):
        # Get the user's query from input field
        user_text = self.user_input.text
        self.user_input.text = ''

        # Display the user's query
        self.add_message(f"You: {user_text}")

        # Check if the user input matches predefined patterns using Boyer-Moore
        response = self.chatbot_response(user_text)
        self.add_message(f"Chatbot: {response}")

    def add_message(self, message):
        # Display a message in the chat history
        message_label = Label(text=message, size_hint_y=None, height=40)
        self.chat_history.add_widget(message_label)

    def chatbot_response(self, user_text):
        # Predefined responses (patterns)
        # Extracting products and prices dynamically
        products = [
            {"name": "Oli Motor", "price": "Rp. 100.000"},
            {"name": "Ban Motor", "price": "Rp. 250.000"},
            {"name": "Filter Udara", "price": "Rp. 50.000"},
            {"name": "Paket Ganti Oli", "price": "Rp. 150.000"},
            {"name": "Accu Motor", "price": "Rp. 400.000"},
            {"name": "Kampas Rem", "price": "Rp. 80.000"},
            {"name": "Radiator Mobil", "price": "Rp. 500.000"},
            {"name": "Aki Mobil", "price": "Rp. 600.000"},
            {"name": "Shockbreaker Depan", "price": "Rp. 200.000"},
            {"name": "Oil Filter", "price": "Rp. 75.000"},
            {"name": "Saringan Bensin", "price": "Rp. 40.000"},
            {"name": "Paket Perawatan Mobil", "price": "Rp. 350.000"},
            {"name": "Busi Motor", "price": "Rp. 30.000"},
            {"name": "Sabuk Pengaman", "price": "Rp. 70.000"},
            {"name": "Kabel Rem", "price": "Rp. 20.000"},
            {"name": "Lampu Depan Motor", "price": "Rp. 100.000"},
            {"name": "Lampu Mobil LED", "price": "Rp. 120.000"},
            {"name": "Knalpot Racing", "price": "Rp. 450.000"},
            {"name": "Panel Dashboard", "price": "Rp. 200.000"},
            {"name": "Pompa Oli", "price": "Rp. 250.000"},
            {"name": "Penyaring Udara AC", "price": "Rp. 65.000"}
        ]

        # Match the user query with the product names using Boyer-Moore
        for product in products:
            if boyer_moore(user_text.lower(), product['name'].lower()):
                return f"Produk {product['name']} tersedia dengan harga {product['price']}."
        
        # If no match found, return a default response
        return "Maaf, saya tidak mengerti pertanyaan Anda."

    def show_products_and_services(self, instance):
        print("Menampilkan produk bengkel dan layanan...")

        # Create a vertical layout for products and services
        product_layout = BoxLayout(orientation='vertical', padding=10, spacing=10, size_hint=(1, None))
        product_layout.height = 1500  # Height of the product layout

        # Example products and services
        self.products = [
            {"name": "Oli Motor", "price": "Rp. 100.000"},
            {"name": "Ban Motor", "price": "Rp. 250.000"},
            {"name": "Filter Udara", "price": "Rp. 50.000"},
            {"name": "Paket Ganti Oli", "price": "Rp. 150.000"},
            {"name": "Accu Motor", "price": "Rp. 400.000"},
            {"name": "Kampas Rem", "price": "Rp. 80.000"},
            {"name": "Radiator Mobil", "price": "Rp. 500.000"},
            {"name": "Aki Mobil", "price": "Rp. 600.000"},
            {"name": "Shockbreaker Depan", "price": "Rp. 200.000"},
            {"name": "Oil Filter", "price": "Rp. 75.000"},
            {"name": "Saringan Bensin", "price": "Rp. 40.000"},
            {"name": "Paket Perawatan Mobil", "price": "Rp. 350.000"},
            {"name": "Busi Motor", "price": "Rp. 30.000"},
            {"name": "Sabuk Pengaman", "price": "Rp. 70.000"},
            {"name": "Kabel Rem", "price": "Rp. 20.000"},
            {"name": "Lampu Depan Motor", "price": "Rp. 100.000"},
            {"name": "Lampu Mobil LED", "price": "Rp. 120.000"},
            {"name": "Knalpot Racing", "price": "Rp. 450.000"},
            {"name": "Panel Dashboard", "price": "Rp. 200.000"},
            {"name": "Pompa Oli", "price": "Rp. 250.000"},
            {"name": "Penyaring Udara AC", "price": "Rp. 65.000"}
        ]

        # Add product buttons
        random.shuffle(self.products)  # Mengacak urutan produk setiap kali
        for product in self.products:
            button = Button(
                text=f"{product['name']}\n{product['price']}",
                size_hint=(None, None),
                size=(250, 60),
                background_normal='',
                background_color=(0.1, 0.6, 1, 1),  # Blue color for buttons
                color=(1, 1, 1, 1),  # White text
                border=(10, 10, 10, 10),  # Rounded corners
                font_size=14
            )
            product_layout.add_widget(button)

        # Add Header
        header = Label(
            text="Produk dan Layanan Bengkel",
            size_hint=(1, None),
            height=40,
            color=(0, 0, 0, 1),  # Black color
            font_size=18,
            bold=True
        )

        # Add ScrollView for navigating if there are many products
        scroll_view = ScrollView(size_hint=(1, 0.6))
        scroll_view.add_widget(product_layout)

        # Add "Close" button
        close_button = Button(
            text="Tutup",
            size_hint=(None, None),
            size=(100, 50),
            pos_hint={'center_x': 0.5},
            background_normal='',
            background_color=(0.8, 0.2, 0.2, 1),  # Red close button
            color=(1, 1, 1, 1)  # White text
        )
        close_button.bind(on_press=self.close_popup)

        # Create and show the popup layout
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        popup_layout.add_widget(header)
        popup_layout.add_widget(scroll_view)
        popup_layout.add_widget(close_button)

        # Show the popup
        self.popup = Popup(title="Produk dan Layanan Bengkel", content=popup_layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def show_recommendations(self, instance):
        # Ambil 3 produk acak dari daftar produk (gunakan self.products yang sudah ada)
        random_products = random.sample(self.products, 3)

        # Menampilkan popup dengan rekomendasi produk
        self.recommendation_popup(random_products)

    def recommendation_popup(self, random_products):
        # Create the popup layout for displaying recommendations
        popup_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Header
        header = Label(
            text="Rekomendasi Produk",
            size_hint=(1, None),
            height=40,
            color=(0, 0, 0, 1),
            font_size=18,
            bold=True
        )
        popup_layout.add_widget(header)

        # Add 3 recommended products as buttons
        for product in random_products:
            button = Button(
                text=f"{product['name']}\n{product['price']}",
                size_hint=(None, None),
                size=(250, 60),
                background_normal='',
                background_color=(0.1, 0.6, 1, 1),  # Blue color for buttons
                color=(1, 1, 1, 1),  # White text
                border=(10, 10, 10, 10),  # Rounded corners
                font_size=14
            )
            popup_layout.add_widget(button)

        # Close Button
        close_button = Button(text="Tutup", size_hint=(None, None), size=(100, 50), pos_hint={'center_x': 0.5})
        close_button.bind(on_press=self.close_popup)
        popup_layout.add_widget(close_button)

        # Create and show the popup
        self.popup = Popup(title="Rekomendasi Produk", content=popup_layout, size_hint=(0.8, 0.8))
        self.popup.open()

    def close_popup(self, instance):
        self.popup.dismiss()

if __name__ == '__main__':
    E_BengkelApp().run()
