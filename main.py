import customtkinter as ctk
import os
import subprocess
import requests
import threading
from PIL import Image

GITHUB_USER = "Morgan-Kot"
GITHUB_REPO = "KotliteTest" 

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("green")

class KotliteLauncher(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Kotlite Browser Launcher")

        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        ww, wh = int(sw * 0.8), int(sh * 0.8)
        self.geometry(f"{ww}x{wh}+{(sw-ww)//2}+{(sh-wh)//2}")

        self.base_path = os.path.join(os.getenv('APPDATA'), "KotliteBrowser")
        self.versions_folder = os.path.join(self.base_path, "versions")
        os.makedirs(self.versions_folder, exist_ok=True)

        self.available_remote_versions = {} 

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=3)
        self.grid_columnconfigure(1, weight=1)

        self.setup_news_panel()
        self.setup_sidebar()

        threading.Thread(target=self.fetch_github_releases, daemon=True).start()

    def setup_news_panel(self):
        self.news_frame = ctk.CTkFrame(self, corner_radius=10)
        self.news_frame.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="nsew")

        self.news_label = ctk.CTkLabel(self.news_frame, text="Kotlite News & Updates", font=("Helvetica", 32, "bold"))
        self.news_label.pack(pady=(30, 20), padx=30, anchor="w")

        self.news_textbox = ctk.CTkTextbox(self.news_frame, font=("Helvetica", 16), wrap="word", fg_color="transparent")
        self.news_textbox.pack(fill="both", expand=True, padx=30, pady=(0, 20))
        self.news_textbox.insert("0.0", "Checking for latest versions from GitHub...")
        self.news_textbox.configure(state="disabled")

    def setup_sidebar(self):
        self.sidebar_frame = ctk.CTkFrame(self, corner_radius=10, fg_color="transparent")
        self.sidebar_frame.grid(row=0, column=1, padx=(10, 20), pady=20, sticky="nsew")

        self.selected_version = ctk.StringVar()
        self.scroll_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Installations", label_font=("Helvetica", 16, "bold"))
        self.scroll_frame.pack(fill="both", expand=True, pady=(0, 15))

        self.launch_container = ctk.CTkFrame(self.sidebar_frame, fg_color="transparent")
        self.launch_container.pack(fill="x", side="bottom")

        self.status_label = ctk.CTkLabel(self.launch_container, text="Syncing with GitHub...", text_color="gray")
        self.status_label.pack(pady=(0, 5))

        self.launch_btn = ctk.CTkButton(
            self.launch_container, text="Launch", font=("Helvetica", 28, "bold"), 
            height=70, fg_color="#11C659", command=self.handle_action
        )
        self.launch_btn.pack(fill="x")

    def fetch_github_releases(self):
        """Gets release data from GitHub API."""
        try:
            url = f"https://api.github.com/repos/{GITHUB_USER}/{GITHUB_REPO}/releases"
            response = requests.get(url)
            releases = response.json()

            self.available_remote_versions = {}
            for release in releases:
                version_name = release['tag_name']

                for asset in release['assets']:
                    if asset['name'].endswith(".exe"):
                        self.available_remote_versions[version_name] = asset['browser_download_url']

            self.after(0, self.update_version_list)
        except Exception as e:
            self.after(0, lambda: self.status_label.configure(text="Offline / GitHub Error", text_color="red"))

    def update_version_list(self):
        """Refreshes the sidebar with versions found on GitHub."""
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        versions = sorted(self.available_remote_versions.keys(), reverse=True)

        if not versions:
            ctk.CTkLabel(self.scroll_frame, text="No releases found.").pack(pady=20)
            return

        for v in versions:

            is_downloaded = os.path.exists(os.path.join(self.versions_folder, f"{v}.exe"))
            suffix = " (Installed)" if is_downloaded else " (Cloud)"

            rb = ctk.CTkRadioButton(
                self.scroll_frame, text=f"{v}{suffix}", variable=self.selected_version, 
                value=v, font=("Helvetica", 16), command=self.update_button_text
            )
            rb.pack(fill="x", pady=5, padx=5)

        self.selected_version.set(versions[0])
        self.update_button_text()
        self.status_label.configure(text="Ready", text_color="gray")

    def update_button_text(self):
        """Changes button to 'Install' if file is missing."""
        target = self.selected_version.get()
        exe_path = os.path.join(self.versions_folder, f"{target}.exe")

        if os.path.exists(exe_path):
            self.launch_btn.configure(text="Launch", fg_color="#11C659", state="normal")
        else:
            self.launch_btn.configure(text="Install", fg_color="#3b8ed0", state="normal")

    def handle_action(self):
        target = self.selected_version.get()
        exe_path = os.path.join(self.versions_folder, f"{target}.exe")

        if os.path.exists(exe_path):
            self.status_label.configure(text="Starting Kotlite...", text_color="#11C659")
            subprocess.Popen(exe_path)
            self.after(2000, self.destroy)
        else:
            self.launch_btn.configure(state="disabled", text="Downloading...")
            threading.Thread(target=self.download_file, args=(target,)).start()

    def download_file(self, version):
        """Downloads the exe from GitHub."""
        try:
            url = self.available_remote_versions[version]
            r = requests.get(url, stream=True)
            path = os.path.join(self.versions_folder, f"{version}.exe")

            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

            self.after(0, self.update_version_list)
        except Exception:
            self.after(0, lambda: self.status_label.configure(text="Download Failed", text_color="red"))

if __name__ == "__main__":
    app = KotliteLauncher()
    app.mainloop()
