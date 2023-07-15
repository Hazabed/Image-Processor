# Import the necessary libraries
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2


# This class defines the image processor application.
class ImageProcessor:

    # Initialize the class.
    def __init__(self, root):
        # Save the root window.
        self.root = root
        root.state('zoomed')
        # Set the window title.
        self.root.title('Image Processor')

        # Set the window background color.
        self.root.configure(bg="gray70")

        # Initialize the image and the modified flag.
        self.filename = None
        self.image = None
        self.modified = False

        # Create the GUI elements.
        name_label = tk.Label(root, text='By: Hassan Abid', font=('Arial', 12))
        name_label.pack(side='bottom', pady=10)

        self.header_label = tk.Label(self.root, text="Image Processor", font=("Arial", 24, "bold"), bg="gray30", fg="white")
        self.header_label.pack(pady=10, fill="x")

        self.frame = tk.Frame(self.root, bg="gray70")
        self.frame.pack(fill="both", expand=True, padx=50, pady=10)

        self.image_label = tk.Label(self.frame, borderwidth=2, relief="groove")
        self.image_label.pack(side="left", padx=20, pady=10)

        self.buttons_frame = tk.Frame(self.frame, bg="gray70")
        self.buttons_frame.pack(side="right", padx=20, pady=10)

        self.select_button = tk.Button(self.buttons_frame, text="Select Image", command=self.select_image, font=("Arial", 14))
        self.select_button.pack(padx=10, pady=10, fill="x")

        self.reset_button = tk.Button(self.buttons_frame, text="Reset", command=self.reset_image, font=("Arial", 14))
        self.reset_button.pack(padx=10, pady=10, fill="x")

        self.grayscale_button = tk.Button(self.buttons_frame, text="Grayscale", command=self.grayscale_image, font=("Arial", 14))
        self.grayscale_button.pack(padx=10, pady=10, fill="x")

        self.invert_button = tk.Button(self.buttons_frame, text="Invert", command=self.invert_image, font=("Arial", 14))
        self.invert_button.pack(padx=10, pady=10, fill="x")

        self.resize_label = tk.Label(self.buttons_frame, text="Enter new size (width, height):", font=("Arial", 14), bg="gray70")
        self.resize_label.pack(padx=10, pady=10, fill="x")

        self.resize_entry = tk.Entry(self.buttons_frame, font=("Arial", 14))
        self.resize_entry.pack(padx=10, pady=10, fill="x")

        self.resize_button = tk.Button(self.buttons_frame, text="Resize", command=self.resize_image, font=("Arial", 14))
        self.resize_button.pack(padx=10, pady=10, fill="x")

        self.rotate_label = tk.Label(self.buttons_frame, text="Enter rotation angle (degrees):", font=("Arial", 14), bg="gray70")
        self.rotate_label.pack(padx=10, pady=10, fill="x")

        self.rotate_entry = tk.Entry(self.buttons_frame, font=("Arial", 14))
        self.rotate_entry.pack(padx=10, pady=10, fill="x")

        self.rotate_button = tk.Button(self.buttons_frame, text="Rotate", command=self.rotate_image, font=("Arial", 14))
        self.rotate_button.pack(padx=10, pady=10, fill="x")

        self.save_button = tk.Button(self.buttons_frame, text="Save Image", command=self.save_image, font=("Arial", 14))
        self.save_button.pack(padx=10, pady=10, fill="x")

        

    # Select an image file.
    def select_image(self):
        # Open a file dialog to select an image file.
        filename = filedialog.askopenfilename(filetypes=[('Image Files', ('.jpeg', '.jpg', '.png', '.bmp'))])

        # If an image file was selected, load it and display it.
        if filename:
            self.filename = filename
            self.image = cv2.imread(self.filename)
            self.modified = False  # reset modified flag
            self.display_image()

    # Display the image.
    def display_image(self):
        # If there is an image, convert it to RGB format and display it.
        if self.image is not None:
            image = cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image)
            self.image_label.image = image

    # Reset the image to the original.
    def reset_image(self):
        # Load the original image and reset the modified flag.
        self.image = cv2.imread(self.filename)
        self.modified = False
        self.display_image()

    # Convert the image to grayscale.
    def grayscale_image(self):
        # Convert the image to grayscale and set the modified flag.
        self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.modified = True
        self.display_image()

    # Invert the image.
    def invert_image(self):
        # Invert the image and set the modified flag.
        self.image = cv2.bitwise_not(self.image)
        self.modified = True
        self.display_image()

    # Resize the image.
    def resize_image(self):
        # Get the width and height from the resize entry.
        try:
            width, height = map(int, self.resize_entry.get().split(','))
        except ValueError:
            # Display an error message if the input is invalid.
            messagebox.showerror("Error", "Invalid input for image size")
            return

        # Resize the image and set the modified flag.
        self.image = cv2.resize(self.image, (width, height))
        self.modified = True
        self.display_image()

    # Rotate the image.
    def rotate_image(self):
        # Get the angle from the rotate entry.
        try:
            angle = int(self.rotate_entry.get())
        except ValueError:
            # Display an error message if the input is invalid.
            messagebox.showerror("Error", "Invalid input for rotation angle")
            return

        # Rotate the image and set the modified flag.
        rows, cols, _ = self.image.shape
        rotation_matrix = cv2.getRotationMatrix2D((cols/2, rows/2), angle, 1)
        self.image = cv2.warpAffine(self.image, rotation_matrix, (cols, rows))
        self.modified = True
        self.display_image()

    # Save the image.
    def save_image(self):
        # If the image has been modified, save it.
        if self.modified:
            # Get the filename from the save entry.
            filename = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[('PNG Files', '*.png')])

            # If a filename was entered, save the image.
            if filename:
                cv2.imwrite(filename, self.image)
                self.modified = False  # reset modified flag

            else:
                # The user did not enter a filename, so do nothing.
                return

        else:
            # The image has not been modified, so do not save it.
            return

    # Run the application.
    def run(self):
        # Start the mainloop.
        self.root.mainloop()


# This is the main function.
if __name__ == '__main__':
    # Create the root window.
    root = tk.Tk()

    # Create the image processor application.
    app = ImageProcessor(root)

    # Run the application.
    app.run()
