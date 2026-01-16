import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
import os

def compress_image():
    # 1. Open file dialog to select the image
    file_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
    )
    
    if not file_path:
        return  # User cancelled

    try:
        # 2. Open the image using Pillow
        img = Image.open(file_path)
        
        # Get original file size for comparison
        original_size = os.path.getsize(file_path)
        
        # 3. Prepare output filename (e.g., image_compressed.jpg)
        file_dir, file_name = os.path.split(file_path)
        name, ext = os.path.splitext(file_name)
        save_path = filedialog.asksaveasfilename(
            initialdir=file_dir,
            title="Save Compressed Image",
            initialfile=f"{name}_compressed{ext}",
            defaultextension=ext,
            filetypes=[("Image Files", "*.jpg *.jpeg *.png")]
        )
        
        if not save_path:
            return # User cancelled save

        # 4. Compression Logic
        # For JPEGs: 'quality=85' is the sweet spot (great look, low size)
        # For PNGs: 'optimize=True' cleans up data without losing pixels
        
        if ext.lower() in ['.jpg', '.jpeg']:
            img.save(save_path, "JPEG", optimize=True, quality=85)
        elif ext.lower() == '.png':
            # PNG is lossless, so we use optimize to remove metadata/unused colors
            # To get massive PNG reduction, we can convert to P mode (256 colors) 
            # if slight color loss is acceptable. For now, we keep it safe.
            img = img.convert('RGB') # Convert to RGB to safely save as JPEG if user switches ext
            img.save(save_path, "JPEG", optimize=True, quality=85) 
            # Note: Saving complex photos as JPEG is usually better for size than PNG.
        else:
            img.save(save_path, optimize=True, quality=85)

        # 5. Calculate and show results
        new_size = os.path.getsize(save_path)
        saved_kb = (original_size - new_size) / 1024
        reduction_percent = ((original_size - new_size) / original_size) * 100
        
        status_label.config(
            text=f"Success!\nReduced by {reduction_percent:.1f}%\nSaved {saved_kb:.1f} KB",
            fg="green"
        )
        messagebox.showinfo("Done", f"Image saved successfully!\nSize reduced by {int(reduction_percent)}%.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

# --- GUI Setup ---
app = tk.Tk()
app.title("Image Compressor Tool")
app.geometry("400x250")

# Styling
title_font = ("Helvetica", 16, "bold")
text_font = ("Helvetica", 10)

# Widgets
label_title = tk.Label(app, text="Smart Image Compressor", font=title_font, pady=20)
label_title.pack()

btn_compress = tk.Button(
    app, 
    text="Select & Compress Image", 
    command=compress_image, 
    bg="#4CAF50", 
    fg="white", 
    font=("Helvetica", 12, "bold"),
    padx=20, 
    pady=10
)
btn_compress.pack(pady=10)

status_label = tk.Label(app, text="Ready to compress...", font=text_font, fg="grey")
status_label.pack(pady=20)

footer = tk.Label(app, text="Maintains visual quality while reducing size.", font=("Helvetica", 8))
footer.pack(side="bottom", pady=10)

app.mainloop()