import customtkinter as ctk
from tkinter import Menu, messagebox
import cv2
from PIL import Image, ImageTk
import gemini

# Set the appearance mode to dark
ctk.set_appearance_mode("dark")

class InstaMealsApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("InstaMeals")
        self.geometry("1280x720")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.create_menus()
        self.create_main_frame()

        self.camera_frame = None
        self.cap = None

        self.textbox = None

    def create_menus(self):
        menu_bar = Menu(self)

        # About menu directly opens the about page
        menu_bar.add_command(label="About", command=self.show_welcome_and_about)
        menu_bar.add_command(label="Generate", command=self.take_picture)
        menu_bar.add_command(label="Daniel's test", command=lambda: self.generate_meal(["apple", "oatmeal"]))

        self.config(menu=menu_bar)

    def create_main_frame(self):
        self.main_frame = ctk.CTkFrame(self, fg_color="black")
        self.main_frame.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="black")
        self.content_frame.grid(row=1, column=0, sticky="nsew")
        self.show_welcome_and_about()

    def show_welcome_and_about(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        image_path = "InstaMeals.png"  # Replace with your image path
        image = Image.open(image_path)
        photo = ImageTk.PhotoImage(image)
        title_label = ctk.CTkLabel(self.content_frame, image=photo, text="")
        title_label.pack(expand=True, fill="both")
        welcome_label = ctk.CTkLabel(self.content_frame,
                                     text="Welcome to InstaMeals!\nTake a picture of your ingredients to get started.",
                                     font=("Roboto", 16), text_color="#FFFFFF")
        welcome_label.pack(expand=True)

        about_title = ctk.CTkLabel(self.content_frame, text="About InstaMeals", font=("Black Han Sans", 24, "bold"), text_color="#F8C91B")
        about_title.pack(pady=(20, 10))

        about_text = """InstaMeals is a revolutionary app that helps you create delicious meals based on the ingredients you have.

Key Features:
- Ingredient recognition
- Recipe generation
- Meal planning assistance
- Cuisine style suggestions

Version: 1.0
© 2024 InstaMeals Inc."""

        about_label = ctk.CTkLabel(self.content_frame, text=about_text, font=("Roboto", 14), justify="left", text_color="#FFFFFF")
        about_label.pack(pady=10)


    def wrap_text(self, text, width):
        """
        Wraps the text to fit within the specified width.
        """
        import textwrap
        return "\n".join(textwrap.wrap(text, width))


    def generate_meal(self, ingredients):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        self.input_field = ctk.CTkEntry(master=self, width=300)
        self.input_field.grid(row=0, column=0, padx=20, pady=10)

        self.submit_button = ctk.CTkButton(master=self, text="Generate Meal", command=self.get_input_and_generate_meal)
        self.submit_button.grid(row=1, column=0, padx=20, pady=20)


    def get_input_and_generate_meal(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        ingredients = self.input_field.get().split(",")
        response = gemini.prompt("make meal with" + " ".join(ingredients))
        response = self.convert_markdown_to_plain_text(response)
        self.textbox = ctk.CTkTextbox(master=self, width=400, height=200)
        self.textbox.grid(row=0, column=0, padx=20, pady=20)
        self.textbox.insert("0.0", response)
        #meal_label = ctk.CTkLabel(self.content_frame, text=response, font=("Roboto", 14), justify="left", text_color="#FFFFFF")
        #meal_label.pack(pady=10)


    def convert_markdown_to_plain_text(self, markdown_text):
        """
        Converts basic markdown to plain text with some formatting.
        """
        import re

        # Convert headers (e.g., ### Header)
        markdown_text = re.sub(r'#+\s(.+)', r'\1\n', markdown_text)

        # Convert bold text (e.g., **bold** or __bold__)
        markdown_text = re.sub(r'\*\*(.+?)\*\*', r'\1', markdown_text)
        markdown_text = re.sub(r'__(.+?)__', r'\1', markdown_text)

        # Convert italic text (e.g., *italic* or _italic_)
        markdown_text = re.sub(r'\*(.+?)\*', r'\1', markdown_text)
        markdown_text = re.sub(r'_(.+?)_', r'\1', markdown_text)

        # Convert links (e.g., [title](url))
        markdown_text = re.sub(r'\[(.+?)\]\((.+?)\)', r'\1 (\2)', markdown_text)

        return markdown_text

    def take_picture(self):
        if self.cap is None:
            self.cap = cv2.VideoCapture(0)
            if not self.cap.isOpened():
                messagebox.showerror("Camera Error",
                                     "Unable to access the camera. Please check your camera connection.")
                return

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        if self.camera_frame is None:
            self.camera_frame = ctk.CTkLabel(self.content_frame, text="")
            self.camera_frame.pack(expand=True, fill="both", padx=20, pady=20)

        self.update_camera()

        capture_button = ctk.CTkButton(self.content_frame, text="Capture", command=self.capture_image,
                                       fg_color="#F8C91B", hover_color="#F8C91B", text_color="#000000")
        capture_button.pack(pady=(0, 20))

    def update_camera(self):
        ret, frame = self.cap.read()
        if ret:
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            img = Image.fromarray(cv2image)
            img = img.resize((800, 600), Image.LANCZOS)
            imgtk = ImageTk.PhotoImage(image=img)

            # Ensure self.camera_frame is recreated if it was destroyed
            if self.camera_frame is None:
                self.camera_frame = ctk.CTkLabel(self.content_frame, text="")
                self.camera_frame.pack(expand=True, fill="both", padx=20, pady=20)

            # Assign image and update the label
            self.camera_frame.configure(image=imgtk)
            self.camera_frame.imgtk = imgtk

            # Schedule the next update
            self.after(10, self.update_camera)

    def capture_image(self):
        # Here you would add code to capture and process the image
        messagebox.showinfo("Image Captured", "Image captured successfully! Processing...")
        # Add your image processing and meal suggestion logic here

    def on_closing(self):
        if self.cap is not None:
            self.cap.release()
        self.destroy()


if __name__ == "__main__":
    app = InstaMealsApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()
