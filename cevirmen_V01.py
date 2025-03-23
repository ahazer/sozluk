import time
import pyperclip
from deep_translator import GoogleTranslator
from tkinter import Tk, Label

# Pop-up gösterme fonksiyonu
def show_popup(translation):
    root = Tk()
    root.title("Çeviri")
    root.geometry("300x100")
    root.resizable(False, False)
    label = Label(root, text=translation, wraplength=280, justify="center")
    label.pack(expand=True)
    root.after(3000, root.destroy)  # 3 saniye sonra pop-up'ı kapat
    root.mainloop()

# Sürekli panoyu kontrol etme
def clipboard_listener():
    last_text = ""
    while True:
        try:
            # Panodan metni al
            text = pyperclip.paste()
            if text != last_text and text.strip():  # Yeni bir metin varsa
                last_text = text
                # Çeviriyi yap
                result = GoogleTranslator(source="auto", target="tr").translate(text)
                # Çeviri sonucunu göster
                show_popup(result)
        except Exception as e:
            print(f"Hata: {e}")
        time.sleep(1)  # 1 saniye bekle

if __name__ == "__main__":
    clipboard_listener()