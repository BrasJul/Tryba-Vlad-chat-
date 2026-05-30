import threading
from socket import *
from customtkinter import *
from tkinter import filedialog
from PIL import Image, ImageDraw
import base64
import io
import os
class Messenger(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("1000x500")
        self.title("LogiiTalk")
        set_appearance_mode("light")
        set_default_color_theme("blue")
        self.current_theme = "light"
        self.username = "User"
        self.avatar = None
        self.connected = False
        try:
            self.sock = socket(AF_INET, SOCK_STREAM)
            self.sock.connect(("192.168.1.167", 8080))
            self.connected = True
        except Exception as e:
            print(e)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.sidebar = CTkFrame(
            self,
            width=220,
            fg_color="#09E715",
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )
        self.avatar_button = CTkButton(
            self.sidebar,
            text="📷",
            width=50,
            height=50,
            corner_radius=15,
            command=self.choose_avatar
        )
        self.avatar_button.pack(
            pady=(20, 10)
        )
        self.avatar_label = CTkLabel(
            self.sidebar,
            text="🙂",
            font=("Arial", 50)
        )
        self.avatar_label.pack(
            pady=10
        )
        self.name_label = CTkLabel(
            self.sidebar,
            text="Введіть ім'я",
            text_color="black",
            font=("Arial", 20, "bold")
        )
        self.name_label.pack(
            pady=(10, 5)
        )
        self.name_entry = CTkEntry(
            self.sidebar,
            width=170,
            height=40,
            corner_radius=12
        )
        self.name_entry.pack(
            pady=10
        )
        self.save_button = CTkButton(
            self.sidebar,
            text="Зберегти",
            height=40,
            corner_radius=12,
            command=self.save_profile
        )

        self.save_button.pack(
            pady=20,
            padx=20,
            fill="x"
        )
        self.theme_menu = CTkOptionMenu(
            self.sidebar,
            values=[
                "Світла тема",
                "Дуже темна тема"
            ],
            command=self.change_theme
        )

        self.theme_menu.pack(
            side="bottom",
            pady=20
        )
        self.chat_container = CTkFrame(
            self,
            fg_color="#F81212",
            corner_radius=0
        )
        self.chat_container.grid(
            row=0,
            column=1,
            sticky="nsew"
        )

        self.chat_container.grid_rowconfigure(0, weight=1)
        self.chat_container.grid_columnconfigure(0, weight=1)

        self.chat_frame = CTkScrollableFrame(
            self.chat_container,
            fg_color="#533DAC"
        )
        self.chat_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=15,
            pady=15
        )
        self.input_frame = CTkFrame(
            self.chat_container,
            height=80,
            corner_radius=15
        )
        self.input_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=15,
            pady=15
        )
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = CTkEntry(
            self.input_frame,
            placeholder_text="Введіть повідомлення...",
            height=50,
            corner_radius=15,
            font=("Arial", 15)
        )

        self.message_entry.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(15, 10),
            pady=15
        )

        self.bind(
            "<Return>",
            lambda e: self.send_message()
        )

        self.image_button = CTkButton(
            self.input_frame,
            text="📷",
            width=60,
            height=50,
            corner_radius=15,
            command=self.send_image
        )

        self.image_button.grid(
            row=0,
            column=1,
            padx=(0, 10),
            pady=15
        )
        self.send_button = CTkButton(
            self.input_frame,
            text="Надіслати",
            width=140,
            height=50,
            corner_radius=15,
            command=self.send_message
        )
        self.send_button.grid(
            row=0,
            column=2,
            padx=(0, 15),
            pady=15
        )
        
        if self.connected:
            threading.Thread(
                target=self.receive_messages,
                daemon=True
            ).start()

            self.system_message(
                "Підключено до сервера"
            )

        else:
            self.system_message(
                "Сервер недоступний"
            )
    def change_theme(self, value):
        if value == "Дуже темна тема":
            set_appearance_mode("dark")
            self.current_theme = "dark"
            self.sidebar.configure(
                fg_color="#4070A0"
            )
            self.chat_container.configure(
                fg_color="#6E7482"
            )
            self.chat_frame.configure(
                fg_color="#6D88C7"
            )
            self.input_frame.configure(
                fg_color="#3C4863"
            )
            self.name_label.configure(
                text_color="white"
            )
        else:
            set_appearance_mode("light")
            self.current_theme = "light"
            self.sidebar.configure(
                fg_color="#FFFFFF"
            )
            self.chat_container.configure(
                fg_color="#ECECEC"
            )
            self.chat_frame.configure(
                fg_color="#ECECEC"
            )
            self.input_frame.configure(
                fg_color="#F2F2F2"
            )
            self.name_label.configure(
                text_color="black"
            )
    def save_profile(self):
        name = self.name_entry.get()
        if name:
            self.username = name
            self.system_message(
                f"Ваш нік: {self.username}"
            )
    def choose_avatar(self):
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )
        if not path:
            return
        image = Image.open(path).convert("RGB")
        image = image.resize((80, 80))
        mask = Image.new("L", (80, 80), 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            (0, 0, 80, 80),
            fill=255
        )
        output = Image.new(
            "RGB",
            (80, 80),
            (0, 0, 0)
        )
        output.paste(
            image,
            (0, 0),
            mask
        )
        self.avatar = CTkImage(
            light_image=output,
            dark_image=output,
            size=(80, 80)
        )
        self.avatar_label.configure(
            image=self.avatar,
            text=""
        )
    def system_message(self, text):
        label = CTkLabel(
            self.chat_frame,
            text=text,
            text_color="gray",
            font=("Arial", 14)
        )
        label.pack(
            pady=5
        )
    def add_message(self, author, message):
        container = CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        container.pack(
            fill="x",
            pady=10,
            padx=10
        )
        if self.avatar:
            avatar = CTkLabel(
                container,
                image=self.avatar,
                text=""
            )
        else:
            avatar = CTkLabel(
                container,
                text="🙂",
                font=("Arial", 35),
                width=80
            )
        avatar.pack(
            side="left",
            padx=10
        )
        bubble_color = (
            "#06254D"
            if self.current_theme == "dark"
            else "#D6EAF5"
        )
        text_color = (
            "white"
            if self.current_theme == "dark"
            else "black"
        )
        bubble = CTkFrame(
            container,
            corner_radius=25,
            fg_color=bubble_color
        )
        bubble.pack(
            side="left",
            fill="x",
            expand=True,
            padx=5
        )
        name = CTkLabel(
            bubble,
            text=author,
            font=("Arial", 16, "bold"),
            text_color=text_color
        )
        name.pack(
            anchor="w",
            padx=20,
            pady=(12, 0)
        )
        text = CTkLabel(
            bubble,
            text=message,
            font=("Arial", 15),
            wraplength=700,
            justify="left",
            text_color=text_color
        )
        text.pack(
            anchor="w",
            padx=20,
            pady=(5, 15)
        )
        self.scroll_down()
    def add_image(self, author, image):
        container = CTkFrame(
            self.chat_frame,
            fg_color="transparent"
        )
        container.pack(
            fill="x",
            pady=10,
            padx=10
        )
        bubble_color = (
            "#2C4E7B"
            if self.current_theme == "dark"
            else "#D6EAF5"
        )
        text_color = (
            "white"
            if self.current_theme == "dark"
            else "black"
        )
        bubble = CTkFrame(
            container,
            corner_radius=25,
            fg_color=bubble_color
        )
        bubble.pack(
            side="left",
            padx=10
        )
        name = CTkLabel(
            bubble,
            text=author,
            font=("Arial", 16, "bold"),
            text_color=text_color
        )
        name.pack(
            anchor="w",
            padx=15,
            pady=(10, 5)
        )
        image.thumbnail((350, 350))

        chat_image = CTkImage(
            light_image=image,
            dark_image=image,
            size=image.size
        )
        image_label = CTkLabel(
            bubble,
            image=chat_image,
            text=""
        )
        image_label.image = chat_image

        image_label.pack(
            padx=15,
            pady=(0, 15)
        )
        self.scroll_down()
    def scroll_down(self):

        self.after(
            100,
            lambda:
            self.chat_frame._parent_canvas.yview_moveto(1.0)
        )
    def send_image(self):
        if not self.connected:
            self.system_message(
                "Підключення до сервера відсутнє"
            )
            return
        path = filedialog.askopenfilename(
            filetypes=[
                ("Images", "*.png *.jpg *.jpeg")
            ]
        )
        if not path:
            return
        try:
            with open(path, "rb") as file:
                image_bytes = file.read()
            image_data = base64.b64encode(
                image_bytes
            ).decode()
            filename = os.path.basename(path)
            data = (
                f"IMAGE@{self.username}"
                f"@{filename}@{image_data}\n"
            )
            self.sock.sendall(
                data.encode("utf-8")
            )
            image = Image.open(path)
            self.add_image(
                self.username,
                image
            )
        except Exception as e:

            self.system_message(
                f"Помилка фото: {e}"
            )
    def send_message(self):
        if not self.connected:
            self.system_message(
                "Немає підключення до сервера"
            )
            return
        message = self.message_entry.get()
        if not message:
            return
        self.add_message(
            self.username,
            message
        )
        data = f"TEXT@{self.username}@{message}\n"
        try:
            self.sock.sendall(
                data.encode("utf-8")
            )
        except Exception as e:
            self.system_message(
                f"Socket error: {e}"
            )
        self.message_entry.delete(
            0,
            END
        )
    def receive_messages(self):
        buffer = ""
        while True:
            try:
                chunk = self.sock.recv(999999)
                if not chunk:
                    break
                buffer += chunk.decode()
                while "\n" in buffer:
                    line, buffer = buffer.split(
                        "\n",
                        1
                    )
                    self.handle_message(
                        line.strip()
                    )
            except:
                break
    def handle_message(self, line):
        if not line:
            return
        parts = line.split("@", 3)
        if parts[0] == "TEXT":
            author = parts[1]
            message = parts[2]
            self.add_message(
                author,
                message
            )
        elif parts[0] == "IMAGE":
            author = parts[1]
            image_data = parts[3]
            image_bytes = base64.b64decode(
                image_data
            )
            image = Image.open(
                io.BytesIO(image_bytes)
            )
            self.add_image(
                author,
                image
            )
app = Messenger()
app.mainloop()