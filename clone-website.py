import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# === DİL SEÇENEKLERİ ===
LANGUAGES = {
    "1": "English",
    "2": "Türkçe",
    "3": "中文",
    "4": "Русский",
    "5": "हिन्दी",
    "6": "Deutsch",
    "7": "Français",
    "8": "Italiano"
}

MESSAGES = {
   "English": {
        "banner": "🔗 Web Site Cloner v1.0\n🚀 Coded by CyberByted\n==========================================",
        "menu": "[1] Clone Website\n[2] Exit\n==========================================",
        "choose": "[?] Make your choice: ",
        "enter_url": "[?] Enter the website URL to clone: ",
        "enter_folder": "[?] Enter folder name to save: ",
        "downloading": "[+] Downloading website...\n==========================================",
        "html_saved": "[+] HTML saved:\n==========================================",
        "completed": "[✅] Cloning completed!\n==========================================",
        "error": "[❌] Failed to fetch the website.\n==========================================",
        "exit": "[🚪] Exiting...\n==========================================",
        "invalid": "[❌] Invalid choice, try again!\n=========================================="
    },
    "Türkçe": {
        "banner": "🔗 Web Sitesi Klonlayıcı v1.0\n🚀 CyberBytedDesk tarafından kodlandı\n==========================================",
        "menu": "[1] Web sitesini klonla\n[2] Çıkış yap\n==========================================",
        "choose": "[?] Seçiminizi yapın: ",
        "enter_url": "[?] Klonlanacak site URL'si: ",
        "enter_folder": "[?] Kaydedilecek klasör adı: ",
        "downloading": "[+] Web sitesi indiriliyor...\n==========================================",
        "html_saved": "[+] HTML kaydedildi:\n==========================================",
        "completed": "[✅] Klonlama tamamlandı!\n==========================================",
        "error": "[❌] Web sitesi alınamadı.\n==========================================",
        "exit": "[🚪] Çıkış yapılıyor...\n==========================================",
        "invalid": "[❌] Geçersiz seçim, tekrar deneyin!\n=========================================="
        
    },
    "中文": {
        "banner": "🔗 网站克隆工具 v1.0\n🚀 由CyberBytedDesk编写\n==========================================",
        "menu": "[1] 复制网站\n[2] 退出\n==========================================",
        "choose": "[?] 请选择: ",
        "enter_url": "[?] 输入要克隆的网站URL: ",
        "enter_folder": "[?] 输入要保存的文件夹名称: ",
        "downloading": "[+] 正在下载网站...\n==========================================",
        "html_saved": "[+] HTML已保存:\n==========================================",
        "completed": "[✅] 复制完成！\n==========================================",
        "error": "[❌] 无法获取网站。\n==========================================",
        "exit": "[🚪] 退出...\n==========================================",
        "invalid": "[❌] 选择无效，请重试！\n=========================================="
    },
    "Русский": {
        "banner": "🔗 Клонирование веб-сайта v1.0\n🚀 Разработано CyberBytedDesk\n==========================================",
        "menu": "[1] Клонировать сайт\n[2] Выйти\n==========================================",
        "choose": "[?] Сделайте выбор: ",
        "enter_url": "[?] Введите URL-адрес сайта: ",
        "enter_folder": "[?] Введите название папки: ",
        "downloading": "[+] Загружается сайт...\n==========================================",
        "html_saved": "[+] HTML сохранен:\n==========================================",
        "completed": "[✅] Клонирование завершено!\n==========================================",
        "error": "[❌] Не удалось получить сайт.\n==========================================",
        "exit": "[🚪] Выход...\n==========================================",
        "invalid": "[❌] Недействительный выбор, попробуйте еще раз!\n=========================================="
    },
    "हिन्दी": {
        "banner": "🔗 वेबसाइट क्लोनर v1.0\n🚀 CyberBytedDesk द्वारा कोडित\n==========================================",
        "menu": "[1] वेबसाइट क्लोन करें\n[2] बाहर निकलें\n==========================================",
        "choose": "[?] अपना चयन करें: ",
        "enter_url": "[?] क्लोन करने के लिए वेबसाइट URL दर्ज करें: ",
        "enter_folder": "[?] फ़ोल्डर का नाम दर्ज करें: ",
        "downloading": "[+] वेबसाइट डाउनलोड हो रही है...\n==========================================",
        "html_saved": "[+] HTML सहेजा गया:\n==========================================",
        "completed": "[✅] क्लोनिंग पूर्ण!\n==========================================",
        "error": "[❌] वेबसाइट लाने में विफल।\n==========================================",
        "exit": "[🚪] बाहर निकलना...\n==========================================",
        "invalid": "[❌] अमान्य चयन, पुनः प्रयास करें!\n=========================================="
    },
    "Deutsch": {
        "banner": "🔗 Website-Kloner v1.0\n🚀 Entwickelt von CyberBytedDesk\n==========================================",
        "menu": "[1] Website klonen\n[2] Beenden\n==========================================",
        "choose": "[?] Wählen Sie eine Option: ",
        "enter_url": "[?] Geben Sie die URL der zu klonenden Website ein: ",
        "enter_folder": "[?] Geben Sie den Ordnernamen zum Speichern ein: ",
        "downloading": "[+] Website wird heruntergeladen...\n==========================================",
        "html_saved": "[+] HTML gespeichert:\n==========================================",
        "completed": "[✅] Klonen abgeschlossen!\n==========================================",
        "error": "[❌] Website konnte nicht abgerufen werden.\n==========================================",
        "exit": "[🚪] Beenden...\n==========================================",
        "invalid": "[❌] Ungültige Auswahl, bitte erneut versuchen!\n=========================================="
    },
    "Français": {
        "banner": "🔗 Cloneur de site web v1.0\n🚀 Développé par CyberBytedDesk\n==========================================",
        "menu": "[1] Cloner un site web\n[2] Quitter\n==========================================",
        "choose": "[?] Faites votre choix : ",
        "enter_url": "[?] Entrez l'URL du site à cloner : ",
        "enter_folder": "[?] Entrez le nom du dossier de sauvegarde : ",
        "downloading": "[+] Téléchargement du site...\n==========================================",
        "html_saved": "[+] HTML enregistré :\n==========================================",
        "completed": "[✅] Clonage terminé !\n==========================================",
        "error": "[❌] Échec de récupération du site.\n==========================================",
        "exit": "[🚪] Quitter...\n==========================================",
        "invalid": "[❌] Choix invalide, réessayez !\n=========================================="
    },
    "Italiano": {
        "banner": "🔗 Clonatore di siti web v1.0\n🚀 Sviluppato da CyberBytedDesk\n==========================================",
        "menu": "[1] Clona il sito web\n[2] Esci\n==========================================",
        "choose": "[?] Fai la tua scelta: ",
        "enter_url": "[?] Inserisci l'URL del sito da clonare: ",
        "enter_folder": "[?] Inserisci il nome della cartella per salvare: ",
        "downloading": "[+] Scaricamento del sito...\n==========================================",
        "html_saved": "[+] HTML salvato:\n==========================================",
        "completed": "[✅] Clonazione completata!\n==========================================",
        "error": "[❌] Impossibile recuperare il sito web.\n==========================================",
        "exit": "[🚪] Uscita...\n==========================================",
        "invalid": "[❌] Scelta non valida, riprova!\n=========================================="
    }
}

# === FONKSİYONLAR ===
def choose_language():
    print("🌍 Select Language / Dil Seçin / 选择语言 / Выберите язык:")
    for key, lang in LANGUAGES.items():
        print(f"[{key}] {lang}")

    while True:
        choice = input("[?] Choice / Seçim / 选择 / Выбор: ")
        if choice in LANGUAGES:
            return LANGUAGES[choice]
        print("❌ Invalid selection. Try again!")

def print_menu(lang):
    print(MESSAGES[lang]["banner"])
    print(MESSAGES[lang]["menu"])

def get_website_html(url):
    """Web sitesinin HTML içeriğini getirir."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.encoding = response.apparent_encoding
        return response.text
    except requests.exceptions.RequestException as e:
        print(f"[-] Error: {e}")
        return None

def save_html(html, folder, lang):
    """HTML dosyasını kaydeder."""
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "index.html")

    with open(file_path, "w", encoding="utf-8") as file:
        file.write(html)

    print(f"{MESSAGES[lang]['html_saved']} {file_path}")

def download_assets(html, base_url, folder, lang):
    """CSS, JS ve resimleri indirir."""
    soup = BeautifulSoup(html, "html.parser")

    for tag in soup.find_all(["link", "script", "img"]):
        if tag.name == "link" and tag.get("href"):
            asset_url = urljoin(base_url, tag["href"])
            save_asset(asset_url, folder, lang)
        elif tag.name == "script" and tag.get("src"):
            asset_url = urljoin(base_url, tag["src"])
            save_asset(asset_url, folder, lang)
        elif tag.name == "img" and tag.get("src"):
            asset_url = urljoin(base_url, tag["src"])
            save_asset(asset_url, folder, lang)

def save_asset(url, folder, lang):
    """CSS, JS ve resimleri kaydeder."""
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        filename = os.path.basename(url)
        filepath = os.path.join(folder, filename)

        with open(filepath, "wb") as file:
            file.write(response.content)

        print(f"[+] {filename} {MESSAGES[lang]['completed']}")

    except requests.exceptions.RequestException as e:
        print(f"[❌] {MESSAGES[lang]['error']}: {e}")

def main():
    lang = choose_language()

    while True:
        print_menu(lang)
        choice = input(MESSAGES[lang]["choose"])

        if choice == "1":
            site_url = input(MESSAGES[lang]["enter_url"])
            folder_name = input(MESSAGES[lang]["enter_folder"])

            print(MESSAGES[lang]["downloading"])
            html_content = get_website_html(site_url)

            if html_content:
                save_html(html_content, folder_name, lang)
                download_assets(html_content, site_url, folder_name, lang)
                print(MESSAGES[lang]["completed"])
            else:
                print(MESSAGES[lang]["error"])

        elif choice == "2":
            print(MESSAGES[lang]["exit"])
            break
        else:
            print(MESSAGES[lang]["invalid"])

if __name__ == "__main__":
    main()
