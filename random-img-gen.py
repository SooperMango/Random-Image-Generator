import requests
import io
import tkinter as tk
from tkinter import filedialog, simpledialog
from PIL import Image, ImageTk
from ttkbootstrap import Style

root = tk.Tk()
root.title('Random Image Generator')
root.geometry('700x500')
root.config(bg='white')
root.resizable(True, True)
style = Style(theme="sandstone")

def display_image(category):
    url = f'https://api.unsplash.com/photos/random?query={category}&orientation=landscape&client_id=kQI4yDmON9IZj74e7jI2U42kwSXanb_gQAp_mpEjUAs'
    data = requests.get(url).json()
    img_data = requests.get(data['urls']['regular']).content

    global photo, current_image_data
    current_image_data = img_data
    photo = ImageTk.PhotoImage(Image.open(io.BytesIO(img_data)).resize((700, 500), resample=Image.LANCZOS))
    label.config(image=photo)
    label.image = photo

def enable_button(*args):
    generate_button.config(state='normal' if category_var.get() != "Choose Category" else "disabled")

def save_image():
    if current_image_data:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg"), ("PNG files", "*.png"), ("WebP files", "*.webp"), ("SVG files", "*.svg"), ("All files", "*.*")])
        if file_path:
            img = Image.open(io.BytesIO(current_image_data))
            ext = file_path.split('.')[-1]
            img.save(file_path, format=ext.upper())

def on_right_click(event):
    context_menu.post(event.x_root, event.y_root)

def create_gui():
    global category_var, generate_button, label, current_image_data, context_menu

    current_image_data = None

    category_var = tk.StringVar(value="Choose Category")
    category_options = ["Choose Category", 'Food', 'Animals', 'People', 'Music', 'Art', 'Vehicles', 'Sports', 'Architecture', 'Travel', 'Nature' ,'Random']
    category_dropdown = tk.OptionMenu(root, category_var, *category_options, command=enable_button)
    category_dropdown.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
    category_dropdown.config(width=15, bg='black')

    generate_button = tk.Button(text='Generate Image', state='disabled', command=lambda: display_image(category_var.get()))
    generate_button.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
    generate_button.config(background='black')

    label = tk.Label(root, background="white")
    label.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")
    label.bind("<Button-3>", on_right_click)
    context_menu = tk.Menu(root, tearoff=0)
    context_menu.add_command(label="Download Image", command=save_image)

    root.columnconfigure([0, 1], weight=1)
    root.rowconfigure(1, weight=1)
    root.rowconfigure(2, weight=1)
    root.mainloop()

if __name__ == '__main__':
    create_gui()
