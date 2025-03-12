import cv2
import matplotlib.pyplot as plt
# %matplotlib inline
from PIL import Image
import glob
from pathlib import Path
from natsort import natsorted
import tkinter as tk
import os
from PIL import Image, ImageTk

# Function to save the image to the specified folder
def save_image(image_name, image, folder):
    if not os.path.exists(folder):
        os.makedirs(folder)
    filename = f"{image_name}.png"
    cv2.imwrite(os.path.join(folder, filename), image)
    print(f"Image {image_name} saved to '{folder}' folder.")


def load_image(index):
    # Ensure index is within the range of available images
    if index < 0 or index >= len(sorted_image_paths):
        print("No more images to display.")
        root.destroy()
        return
    
    img_path = sorted_image_paths[index]
    image_name = Path(img_path).stem
    image = cv2.imread(img_path)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    root.title(image_name)

    # Convert the image to PIL format and resize
    pil_image = Image.fromarray(image)
    resized_pil_image = pil_image.resize((400, 200), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(image=resized_pil_image)

    # Update label and buttons for the new image
    label.config(image=photo)
    label.image = photo  

    # Update button commands
    approve_button.config(command=lambda: approve_and_next(index))
    reject_button.config(command=lambda: reject_and_next(index))

def approve_and_next(index):
    image_name = Path(sorted_image_paths[index]).stem
    image = cv2.imread(sorted_image_paths[index])
    save_image(image_name, image, "approved")
    load_image(index + 1)

def reject_and_next(index):
    image_name = Path(sorted_image_paths[index]).stem
    original_image_path = os.path.join(original_images_dir, f"{image_name}.BMP")
    if not os.path.exists(original_image_path):
        print(f"Original image {original_image_path} not found.")
        return
    image = cv2.imread(original_image_path)
    save_image(image_name, image, "not_approved")
    load_image(index + 1)
    
# Initialize the main application window and frame
root = tk.Tk()
frame = tk.Frame(root)
frame.pack()
image_dir = 'bounding_box/'
original_images_dir = 'images/'
image_paths = glob.glob(image_dir + '*.BMP')
sorted_image_paths = natsorted(image_paths)
# Setup UI components
label = tk.Label(frame)
label.pack()
approve_button = tk.Button(frame, text="Approve")
approve_button.pack(side="left", padx=10, pady=10)

reject_button = tk.Button(frame, text="Reject")
reject_button.pack(side="right", padx=10, pady=10)

# Load the first image
load_image(0)

root.mainloop()
