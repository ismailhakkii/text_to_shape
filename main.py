import random
import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse, Circle, Rectangle, Polygon
from tkinter import Tk, Label, Entry, Button, StringVar, filedialog, Text, Frame, Scrollbar
import math
import string


class EncryptionVisualizer:
    def __init__(self):
        # Alfabe tanımlama
        self.alphabet = list(string.ascii_letters + string.digits + "!@#₺&%()*+-/:;<=>?@[\\]^_`{|}~")
        self.shapes_mapping = self.initialize_shapes()
        self.setup_gui()

    def initialize_shapes(self):
        shapes = {
            # Küçük harfler - Normal boyut (scale=1.0)
            'a': ('circle', 'blue'),
            'b': ('square', 'red'),
            'c': ('triangle', 'green'),
            'd': ('star', 'yellow'),
            'e': ('pentagon', 'purple'),
            'f': ('hexagon', 'orange'),
            'g': ('octagon', 'cyan'),
            'h': ('diamond', 'pink'),
            'i': ('parallelogram', 'brown'),
            'j': ('ellipse', 'teal'),
            'k': ('circle', 'darkblue'),
            'l': ('square', 'darkred'),
            'm': ('triangle', 'darkgreen'),
            'n': ('star', 'gold'),
            'o': ('pentagon', 'indigo'),
            'p': ('hexagon', 'coral'),
            'q': ('octagon', 'skyblue'),
            'r': ('diamond', 'magenta'),
            's': ('parallelogram', 'sienna'),
            't': ('ellipse', 'turquoise'),
            'u': ('circle', 'navy'),
            'v': ('square', 'crimson'),
            'w': ('triangle', 'forestgreen'),
            'x': ('star', 'goldenrod'),
            'y': ('pentagon', 'violet'),
            'z': ('hexagon', 'orangered'),
        }

        # Büyük harfler - Küçük harflerin şekilleri ama %50 daha büyük (scale=1.5)
        for char in string.ascii_uppercase:
            shapes[char] = shapes[char.lower()]

        # Sayılar - %25 daha küçük (scale=0.75)
        number_shapes = {
            '0': ('circle', 'blue'),
            '1': ('square', 'red'),
            '2': ('triangle', 'green'),
            '3': ('star', 'yellow'),
            '4': ('pentagon', 'purple'),
            '5': ('hexagon', 'orange'),
            '6': ('octagon', 'cyan'),
            '7': ('diamond', 'pink'),
            '8': ('parallelogram', 'brown'),
            '9': ('ellipse', 'teal')
        }
        shapes.update(number_shapes)

        # Özel karakterler - %10 daha küçük (scale=0.9)
        special_chars = "!@#₺&%()*+-/:;<=>?@[\\]^_`{|}~"
        for i, char in enumerate(special_chars):
            shapes[char] = shapes[list(string.ascii_lowercase)[i % 26]]

        return shapes

    def get_shape_scale(self, char):
        """Karaktere göre ölçek faktörünü belirle"""
        if char.isupper():
            return 1.5  # Büyük harfler %50 daha büyük
        elif char.isdigit():
            return 0.75  # Sayılar %25 daha küçük
        elif not char.isalnum():
            return 0.9  # Özel karakterler %10 daha küçük
        return 1.0  # Küçük harfler normal boyut

    def draw_shape(self, ax, shape_info, x, y, char):
        """Geometrik şekil çiz"""
        shape, color = shape_info
        scale = self.get_shape_scale(char)

        if shape == "circle":
            circle = Circle((x, y), 0.4 * scale, color=color)
            ax.add_artist(circle)
        elif shape == "square":
            square = Rectangle((x - 0.4 * scale, y - 0.4 * scale),
                               0.8 * scale, 0.8 * scale, color=color)
            ax.add_artist(square)
        elif shape == "triangle":
            triangle = Polygon([[x, y + 0.4 * scale],
                                [x - 0.4 * scale, y - 0.4 * scale],
                                [x + 0.4 * scale, y - 0.4 * scale]], color=color)
            ax.add_artist(triangle)
        elif shape == "star":
            points = []
            for i in range(10):
                angle = i * 36 * 3.14159 / 180
                r = 0.4 * scale if i % 2 == 0 else 0.2 * scale
                points.append([x + r * math.cos(angle), y + r * math.sin(angle)])
            star = Polygon(points, color=color)
            ax.add_artist(star)
        elif shape == "pentagon":
            points = []
            for i in range(5):
                angle = (i * 72 - 18) * 3.14159 / 180
                points.append([x + 0.4 * scale * math.cos(angle),
                               y + 0.4 * scale * math.sin(angle)])
            pentagon = Polygon(points, color=color)
            ax.add_artist(pentagon)
        elif shape == "hexagon":
            points = []
            for i in range(6):
                angle = i * 60 * 3.14159 / 180
                points.append([x + 0.4 * scale * math.cos(angle),
                               y + 0.4 * scale * math.sin(angle)])
            hexagon = Polygon(points, color=color)
            ax.add_artist(hexagon)
        elif shape == "octagon":
            points = []
            for i in range(8):
                angle = i * 45 * 3.14159 / 180
                points.append([x + 0.4 * scale * math.cos(angle),
                               y + 0.4 * scale * math.sin(angle)])
            octagon = Polygon(points, color=color)
            ax.add_artist(octagon)
        elif shape == "diamond":
            diamond = Polygon([[x, y + 0.4 * scale],
                               [x - 0.4 * scale, y],
                               [x, y - 0.4 * scale],
                               [x + 0.4 * scale, y]], color=color)
            ax.add_artist(diamond)
        elif shape == "parallelogram":
            parallelogram = Polygon([[x - 0.3 * scale, y + 0.2 * scale],
                                     [x + 0.3 * scale, y + 0.2 * scale],
                                     [x + 0.5 * scale, y - 0.2 * scale],
                                     [x - 0.1 * scale, y - 0.2 * scale]], color=color)
            ax.add_artist(parallelogram)
        elif shape == "ellipse":
            ellipse = Ellipse((x, y), 0.8 * scale, 0.4 * scale, color=color)
            ax.add_artist(ellipse)

        # Karakteri şeklin içine yaz - boyut farkını burada da uygula
        font_size = 10 * scale
        ax.text(x, y, char, ha='center', va='center', fontsize=font_size)

    def encrypt_text(self, input_text):
        """Metni şifrele"""
        encrypted = ""
        for char in input_text:
            if char in self.alphabet:
                left_random = random.choice(self.alphabet)
                right_random = random.choice(self.alphabet)
                encrypted += f"{left_random}{char}{right_random}"
            else:
                encrypted += char
        return encrypted

    def decrypt_text(self, encrypted_text):
        """Şifrelenmiş metni çöz"""
        decrypted = ""
        i = 0
        while i < len(encrypted_text):
            if i + 2 < len(encrypted_text):
                decrypted += encrypted_text[i + 1]
                i += 3
            else:
                decrypted += encrypted_text[i:]
                break
        return decrypted

    def visualize_text(self, text):
        """Metni görselleştir"""
        chars_per_row = 10
        num_rows = math.ceil(len(text) / chars_per_row)

        fig, ax = plt.subplots(figsize=(12, 2 * num_rows))
        ax.set_xlim(-1, chars_per_row + 1)
        ax.set_ylim(-1, num_rows + 1)
        ax.axis('off')

        for i, char in enumerate(text):
            if char in self.shapes_mapping:
                row = num_rows - 1 - (i // chars_per_row)
                col = i % chars_per_row
                self.draw_shape(ax, self.shapes_mapping[char], col, row, char)

        filepath = filedialog.asksaveasfilename(defaultextension=".png",
                                                filetypes=[("PNG files", "*.png")])
        if filepath:
            plt.savefig(filepath, bbox_inches='tight', dpi=300)
            plt.close()
            return f"Görsel başarıyla '{filepath}' olarak kaydedildi!"
        plt.close()
        return "Kaydetme işlemi iptal edildi."

    def setup_gui(self):
        """Kullanıcı arayüzünü oluştur"""
        self.root = Tk()
        self.root.title("Metin Şifreleme ve Görselleştirme")
        self.root.geometry("800x600")

        main_frame = Frame(self.root, padx=20, pady=20)
        main_frame.pack(expand=True, fill='both')

        Label(main_frame, text="Metin Giriniz:", font=("Arial", 12)).pack(pady=5)
        self.input_text = Text(main_frame, height=5, width=50, font=("Arial", 12))
        self.input_text.pack(pady=5)

        button_frame = Frame(main_frame)
        button_frame.pack(pady=10)

        Button(button_frame, text="Şifrele", command=self.encrypt_and_visualize,
               font=("Arial", 12), bg="lightblue").pack(side='left', padx=5)

        Button(button_frame, text="Şifre Çöz", command=self.decrypt_and_visualize,
               font=("Arial", 12), bg="lightgreen").pack(side='left', padx=5)

        Label(main_frame, text="Sonuç:", font=("Arial", 12)).pack(pady=5)
        self.result_text = Text(main_frame, height=5, width=50, font=("Arial", 12))
        self.result_text.pack(pady=5)

        self.status_var = StringVar()
        Label(main_frame, textvariable=self.status_var, font=("Arial", 12),
              fg="blue", wraplength=700).pack(pady=10)

    def encrypt_and_visualize(self):
        """Metni şifrele ve görselleştir"""
        input_text = self.input_text.get("1.0", "end-1c")
        if input_text:
            encrypted = self.encrypt_text(input_text)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", encrypted)
            status = self.visualize_text(encrypted)
            self.status_var.set(status)
        else:
            self.status_var.set("Lütfen bir metin giriniz!")

    def decrypt_and_visualize(self):
        """Şifrelenmiş metni çöz ve görselleştir"""
        encrypted_text = self.input_text.get("1.0", "end-1c")
        if encrypted_text:
            decrypted = self.decrypt_text(encrypted_text)
            self.result_text.delete("1.0", "end")
            self.result_text.insert("1.0", decrypted)
            status = self.visualize_text(decrypted)
            self.status_var.set(status)
        else:
            self.status_var.set("Lütfen şifrelenmiş metni giriniz!")

    def run(self):
        """Uygulamayı başlat"""
        self.root.mainloop()


if __name__ == "__main__":
    app = EncryptionVisualizer()
    app.run()