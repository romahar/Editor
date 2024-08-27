import customtkinter as ctk 
from PIL import Image, ImageTk, ImageOps, ImageEnhance, ImageFilter
from tkinter import filedialog

# Constantes (defina seus valores padrão)
ROTATE_DEFAULT = 0.0
ZOOM_DEFAULT = 1.0
FLIP_OPTIONS = ["None", "Horizontal", "Vertical", "Both"]
BRIGHTNESS_DEFAULT = 1.0
VIBRANCE_DEFAULT = 1.0
BLUR_DEFAULT = 0.0
CONTRAST_DEFAULT = 1.0
EFFECT_OPTIONS = ["None", "Emboss", "Find edges", "Contour", "Edge enhance"]

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        ctk.set_appearance_mode('dark')
        self.geometry('1000x600')
        self.title('Photo Editor')
        self.minsize(800, 500)
        
        # layout
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=2, uniform='a')
        self.columnconfigure(1, weight=6, uniform='a')
        
        # canvas data
        self.image_width = 0
        self.image_height = 0
        self.canvas_width = 0
        self.canvas_height = 0
        
        # widgets
        self.image_import_button = ctk.CTkButton(self, text="Importar Imagem", command=self.open_file_dialog)
        self.image_import_button.grid(column=0, row=0, sticky='nsew')
        
        # Inicializar parâmetros
        self.init_parameters()
        
        # run 
        self.mainloop()

    def open_file_dialog(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif")])
        if file_path:
            self.import_image(file_path)
   
    def init_parameters(self):
        self.rotate_float = ctk.DoubleVar(value=ROTATE_DEFAULT)
        self.zoom_float = ctk.DoubleVar(value=ZOOM_DEFAULT)

        self.rotate_float.trace('w', self.manipulate_image)
        self.zoom_float.trace('w', self.manipulate_image)
        
        self.pos_vars = {
            'rotate': self.rotate_float,
            'zoom': self.zoom_float,
            'flip': ctk.StringVar(value=FLIP_OPTIONS[0])
        }
        
        self.color_vars = {
            'brightness': ctk.DoubleVar(value=BRIGHTNESS_DEFAULT),
            'vibrance': ctk.DoubleVar(value=VIBRANCE_DEFAULT),
            'grayscale': ctk.BooleanVar(value=False),
            'invert': ctk.BooleanVar(value=False)
        }
        
        self.effect_vars = {
            'blur': ctk.DoubleVar(value=BLUR_DEFAULT),
            'contrast': ctk.DoubleVar(value=CONTRAST_DEFAULT),
            'effect': ctk.StringVar(value=EFFECT_OPTIONS[0])
        }

        self.color_vars['brightness'].trace('w', self.manipulate_image)
        self.color_vars['vibrance'].trace('w', self.manipulate_image)
        self.color_vars['grayscale'].trace('w', self.manipulate_image)
        self.color_vars['invert'].trace('w', self.manipulate_image)

        self.effect_vars['blur'].trace('w', self.manipulate_image)
        self.effect_vars['contrast'].trace('w', self.manipulate_image)
        self.effect_vars['effect'].trace('w', self.manipulate_image)

    def manipulate_image(self, *args):
        if not hasattr(self, 'original'):
            return
        self.image = self.original.copy()
       
        # rotate
        self.image = self.image.rotate(self.rotate_float.get(), expand=True)
        
        # zoom
        zoom_factor = self.zoom_float.get()
        new_size = (int(self.image.width * zoom_factor), int(self.image.height * zoom_factor))
        self.image = self.image.resize(new_size, Image.ANTIALIAS)
       
        # flip
        flip_option = self.pos_vars['flip'].get()
        if flip_option == 'Horizontal':
            self.image = ImageOps.mirror(self.image)
        elif flip_option == 'Vertical':
            self.image = ImageOps.flip(self.image)
        elif flip_option == 'Both':
            self.image = ImageOps.mirror(self.image)
            self.image = ImageOps.flip(self.image)

        # brightness and vibrance 
        if self.color_vars['brightness'].get() != BRIGHTNESS_DEFAULT:
            brightness_enhancer = ImageEnhance.Brightness(self.image) 
            self.image = brightness_enhancer.enhance(self.color_vars['brightness'].get())
        if self.color_vars['vibrance'].get() != VIBRANCE_DEFAULT:
            vibrance_enhancer = ImageEnhance.Color(self.image)
            self.image = vibrance_enhancer.enhance(self.color_vars['vibrance'].get())
       
        # Colors invert
        if self.color_vars['grayscale'].get():
            self.image = ImageOps.grayscale(self.image)
        if self.color_vars['invert'].get():
            self.image = ImageOps.invert(self.image)
      
        # blur and contrast 
        if self.effect_vars['blur'].get() != BLUR_DEFAULT:
            self.image = self.image.filter(ImageFilter.GaussianBlur(self.effect_vars['blur'].get()))
        if self.effect_vars['contrast'].get() != CONTRAST_DEFAULT:
            contrast_enhancer = ImageEnhance.Contrast(self.image)
            self.image = contrast_enhancer.enhance(self.effect_vars['contrast'].get())
        
        # effects
        effect_option = self.effect_vars['effect'].get()
        if effect_option == 'Emboss':
            self.image = self.image.filter(ImageFilter.EMBOSS)
        elif effect_option == 'Find edges':
            self.image = self.image.filter(ImageFilter.FIND_EDGES)
        elif effect_option == 'Contour':
            self.image = self.image.filter(ImageFilter.CONTOUR)
        elif effect_option == 'Edge enhance':
            self.image = self.image.filter(ImageFilter.EDGE_ENHANCE_MORE)
       
        self.place_image()

    def import_image(self, path):
        self.original = Image.open(path) 
        self.image = self.original
        self.image_ratio = self.image.width / self.image.height
        self.image_tk = ImageTk.PhotoImage(self.image)

        self.image_import_button.grid_forget()
        self.image_output = ctk.CTkCanvas(self)
        self.image_output.grid(column=1, row=0, sticky='nsew')
        self.image_output.bind('<Configure>', self.resize_image)
        self.close_button = ctk.CTkButton(self, text="Fechar", command=self.close_edit)
        self.close_button.place(relx=1.0, rely=0.0, anchor='ne')
        
        self.menu = Menu(self, self.rotate_float, self.zoom_float, self.pos_vars, self.color_vars, self.effect_vars)
        self.menu.grid(column=0, row=0, sticky='nsew')
        self.init_parameters()
    
    def close_edit(self):
        self.image_output.grid_forget()
        self.close_button.place_forget()
        self.menu.grid_forget()
        self.image_import_button = ctk.CTkButton(self, text="Importar Imagem", command=self.open_file_dialog)
        self.image_import_button.grid(column=0, row=0, sticky='nsew')
    
    def resize_image(self, event): 
        canvas_ratio = event.width / event.height
        # update canvas attributes
        self.canvas_width = event.width
        self.canvas_height = event.height

        if canvas_ratio > self.image_ratio:
            self.image_height = int(event.height)
            self.image_width = int(self.image_height * self.image_ratio)
        else:
            self.image_width = int(event.width)
            self.image_height = int(self.image_width / self.image_ratio)
         
        self.place_image()

    def place_image(self):
        self.image_output.delete('all')
        resized_image = self.image.resize((self.image_width, self.image_height))
        self.image_tk = ImageTk.PhotoImage(resized_image)
        self.image_output.create_image(self.canvas_width / 2, self.canvas_height / 2, image=self.image_tk)

class SliderPanel(ctk.CTkFrame):
    def __init__(self, parent, text, data_var, min_value, max_value):
        super().__init__(parent=parent)

        # layout
        self.rowconfigure((0, 1), weight=1)
        self.columnconfigure((0, 1), weight=1)

        ctk.CTkLabel(self, text=text).grid(column=0, row=0, sticky='W', padx=5)    
        self.num_label = ctk.CTkLabel(self, text=data_var.get())
        self.num_label.grid(column=1, row=0, sticky='E', padx=5)
        ctk.CTkSlider(self, variable=data_var, from_=min_value, to=max_value, command=self.update_text).grid(row=1, column=0, columnspan=2, sticky='ew', padx=5)

    def update_text(self, value):
        self.num_label.configure(text=f'{round(value, 2)}')

class PositionFrame(ctk.CTkFrame):
    def __init__(self, parent, pos_vars):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.pos_vars = pos_vars

        SliderPanel(self, 'Rotation', self.pos_vars['rotate'], 0, 360).pack(padx=10, pady=5)
        SliderPanel(self, 'Zoom', self.pos_vars['zoom'], 0, 2).pack(padx=10, pady=5)
        
        ctk.CTkLabel(self, text='Flip').pack(padx=10, pady=5)
        for option in FLIP_OPTIONS:
            ctk.CTkRadioButton(self, text=option, variable=self.pos_vars['flip'], value=option).pack(anchor='w', padx=10)

class ColorFrame(ctk.CTkFrame):
    def __init__(self, parent, color_vars):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.color_vars = color_vars

        SliderPanel(self, 'Brightness', self.color_vars['brightness'], 0, 2).pack(padx=10, pady=5)
        SliderPanel(self, 'Vibrance', self.color_vars['vibrance'], 0, 2).pack(padx=10, pady=5)
        
        ctk.CTkCheckBox(self, text="Grayscale", variable=self.color_vars['grayscale']).pack(padx=10, pady=5)
        ctk.CTkCheckBox(self, text="Invert", variable=self.color_vars['invert']).pack(padx=10, pady=5)

class EffectsFrame(ctk.CTkFrame):
    def __init__(self, parent, effect_vars):
        super().__init__(master=parent)
        self.pack(expand=True, fill='both')

        self.effect_vars = effect_vars

        SliderPanel(self, 'Blur', self.effect_vars['blur'], 0, 10).pack(padx=10, pady=5)
        SliderPanel(self, 'Contrast', self.effect_vars['contrast'], 0, 2).pack(padx=10, pady=5)
        
        ctk.CTkLabel(self, text='Effects').pack(padx=10, pady=5)
        for effect in EFFECT_OPTIONS:
            ctk.CTkRadioButton(self, text=effect, variable=self.effect_vars['effect'], value=effect).pack(anchor='w', padx=10)

class Menu(ctk.CTkTabview):
    def __init__(self, parent, rotation, zoom, pos_vars, color_vars, effect_vars):
        super().__init__(master=parent)
        self.grid(row=0, column=0, sticky='nsew')
        # tabs
        self.add('Position')
        self.add('Color')
        self.add('Effects')
        self.add('Export')
        
        # widgets 
        PositionFrame(self.tab('Position'), pos_vars)
        ColorFrame(self.tab('Color'), color_vars)
        EffectsFrame(self.tab('Effects'), effect_vars)

if __name__ == "__main__":
    App()
