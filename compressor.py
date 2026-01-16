import tkinter as tk
from tkinter import filedialog, messagebox, Scale, HORIZONTAL
from PIL import Image, ImageEnhance, ImageTk
import os

# Global variables to store image objects
original_image = None
processed_image = None
tk_image = None

def load_image():
    global original_image
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    if file_path:
        original_image = Image.open(file_path)
        # Convert to RGB to handle PNGs and ensure consistency
        if original_image.mode != 'RGB':
            original_image = original_image.convert('RGB')
            
        # Reset sliders and update preview
        brightness_slider.set(1.0)
        color_slider.set(1.0)
        update_preview()
        btn_save.config(state=tk.NORMAL)
        status_label.config(text="Image loaded. Adjust and save.")

def update_preview(*args):
    global processed_image, tk_image
    if original_image:
        # 1. Enhance Brightness
        enhancer_b = ImageEnhance.Brightness(original_image)
        processed_image = enhancer_b.enhance(brightness_slider.get())
        
        # 2. Enhance Color (Saturation)
        enhancer_c = ImageEnhance.Color(processed_image)
        processed_image = enhancer_c.enhance(color_slider.get())
        
        # Resize for preview window (keep aspect ratio)
        preview_size = (300, 300)
        img_for_preview = processed_image.copy()
        img_for_preview.thumbnail(preview_size)
        
        # Convert to Tkinter-compatible format
        tk_image = ImageTk.PhotoImage(img_for_preview)
        preview_label.config(image=tk_image)

def save_image():
    if not processed_image:
        return

    try:
        save_path = filedialog.asksaveasfilename(
            title="Save Enhanced & Compressed Image",
            defaultextension=".jpg",
            filetypes=[("JPEG Image", "*.jpg"), ("PNG Image", "*.png")]
        )
        
        if not save_path:
            return

        # --- Compression Logic ---
        # We use JPEG with quality=85 for the best balance of size and quality.
        # This is the standard for high-quality web images.
        processed_image.save(save_path, "JPEG", optimize=True, quality=85)

        # Calculate stats
        original_size = os.path.getsize(original_image.filename)
        new_size = os.path.getsize(save_path)
        reduction = ((original_size - new_size) / original_size) * 100
        
        messagebox.showinfo("Success", f"Image saved!\nSize reduced by {int(reduction)}%.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# --- GUI Setup ---
app = tk.Tk()
app.title("Jewelry Photo Enhancer & Compressor")
app.geometry("400x550")

# Styling
font_bold = ("Helvetica", 12, "bold")
font_plain = ("Helvetica", 10)

# 1. Load Button
btn_load = tk.Button(app, text="1. Select Image", command=load_image, font=font_bold, bg="#e1e1e1", padx=10)
btn_load.pack(pady=10)

# 2. Preview Area
preview_frame = tk.Frame(app, width=300, height=300, bg="#f0f0f0")
preview_frame.pack(pady=5)
preview_frame.pack_propagate(False) # Don't shrink
preview_label = tk.Label(preview_frame, text="No image selected", bg="#f0f0f0")
preview_label.pack(expand=True)

# 3. Enhancement Controls
controls_frame = tk.LabelFrame(app, text="Enhance Look", font=font_bold, padx=10, pady=10)
controls_frame.pack(fill="x", padx=20, pady=10)

tk.Label(controls_frame, text="Brightness:", font=font_plain).pack(anchor="w")
brightness_slider = Scale(controls_frame, from_=0.5, to=1.5, resolution=0.05, orient=HORIZONTAL, command=update_preview)
brightness_slider.set(1.0) # Default value
brightness_slider.pack(fill="x")

tk.Label(controls_frame, text="Color Saturation:", font=font_plain).pack(anchor="w")
color_slider = Scale(controls_frame, from_=0.0, to=2.0, resolution=0.05, orient=HORIZONTAL, command=update_preview)
color_slider.set(1.0) # Default value
color_slider.pack(fill="x")

# 4. Save Button
btn_save = tk.Button(app, text="2. Compress & Save", command=save_image, font=font_bold, bg="#4CAF50", fg="white", padx=10, state=tk.DISABLED)
btn_save.pack(pady=10)

status_label = tk.Label(app, text="Welcome!", font=font_plain, fg="grey")
status_label.pack(side="bottom", pady=10)

app.mainloop()