import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk, ImageEnhance

class PhotoEditor(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        self.minsize(1000, 600)
        
        # Layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')
        
        # Canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0
        
        # Image placeholder
        self.img = None
        self.displayed_img = None

        # Widgets
        self.image_import_button = ctk.CTkButton(self, text="Importar Imagem", command=self.open_file_dialog)
        self.image_import_button.grid(column=0, row=0, sticky='nsew')
        
        self.canvas = ctk.CTkCanvas(self, bg="gray")
        self.canvas.grid(column=1, row=0, sticky='nsew')
        self.canvas.bind("<Configure>", self.resize_image)

        # Menu placeholder
        self.menu = None

        # Run 
        self.mainloop()
        # Tipo de imagem
    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.import_image(file_path)
    
    def import_image(self, file_path):
        self.img = Image.open(file_path)
        self.image_ratio = self.img.width / self.img.height
        self.display_image(self.img)
        if self.menu is None:
            self.menu = Menu(self)
        self.menu.show_controls()

    def display_image(self, img):
        self.canvas.delete("all")
        self.displayed_img = ImageTk.PhotoImage(img)
        self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, anchor='center', image=self.displayed_img)

    def adjust_brightness(self, value):
        if self.img:
            enhancer = ImageEnhance.Brightness(self.img)
            bright_img = enhancer.enhance(float(value))
            self.display_image(bright_img)

    def adjust_contrast(self, value):
        if self.img:
            enhancer = ImageEnhance.Contrast(self.img)
            contrast_img = enhancer.enhance(float(value))
            self.display_image(contrast_img)

    def rotate_image(self):
        if self.img:
            self.img = self.img.rotate(90, expand=True)
            self.image_ratio = self.img.width / self.img.height
            self.display_image(self.img)

    def resize_image(self, event):
        self.canvas_width = event.width
        self.canvas_height = event.height

        canvas_ratio = self.canvas_width / self.canvas_height

        if canvas_ratio > self.image_ratio:
            self.image_height = self.canvas_height
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = self.canvas_width
            self.image_height = int(self.image_width / self.image_ratio)

        self.place_image()

    def place_image(self):
        if self.img:
            self.canvas.delete('all')
            resized_image = self.img.resize((self.image_width, self.image_height))
            self.displayed_img = ImageTk.PhotoImage(resized_image)
            self.canvas.create_image(self.canvas_width // 2, self.canvas_height // 2, anchor='center', image=self.displayed_img)

class Menu(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master=parent)
        self.parent = parent
        self.grid(row=0, column=0, sticky='nsew')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        
        # Tabs
        self.tab_view = ctk.CTkTabview(self)
        self.tab_view.pack(expand=True, fill='both')

        # Add tabs
        self.brightness_tab = self.tab_view.add('Brilho')
        self.contrast_tab = self.tab_view.add('Contraste')
        self.rotation_tab = self.tab_view.add('Rotação')

    def show_controls(self):
        # Slider para ajustar o brilho
        brightness_label = ctk.CTkLabel(self.brightness_tab, text="Brilho")
        brightness_label.pack()
        brightness_slider = ctk.CTkSlider(self.brightness_tab, from_=0.1, to=2.0, command=self.parent.adjust_brightness)
        brightness_slider.set(1.0)
        brightness_slider.pack()

        # Slider para ajustar o contraste
        contrast_label = ctk.CTkLabel(self.contrast_tab, text="Contraste")
        contrast_label.pack()
        contrast_slider = ctk.CTkSlider(self.contrast_tab, from_=0.1, to=2.0, command=self.parent.adjust_contrast)
        contrast_slider.set(1.0)
        contrast_slider.pack()

        # Botão para rotacionar a imagem
        rotate_button = ctk.CTkButton(self.rotation_tab, text="Rotacionar", command=self.parent.rotate_image)
        rotate_button.pack()

# Inicialização da aplicação
if __name__ == "__main__":
    app = PhotoEditor()
