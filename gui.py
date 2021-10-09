import tkinter as tk
from tkinter.ttk import Progressbar
import tkinter.filedialog as filedialog
from utils import *
import time


class GUI:
    def __init__(self):
        self.prog_title = "Cropper v0.5"
        self.title_size = 14
        self.reg_size = 12
        self.small_size = 10
        self.type_list = ['jpeg', 'jpg', 'tif', 'tiff', 'png']
        self.bar_length = 500

        self.window = tk.Tk()
        self.window.geometry("720x480")
        self.window.wm_title(self.prog_title)
        self.window.resizable(False, False)

        self.src_entry = None
        self.src_check_label = None
        self.src_test_label = None
        self.src_type = None

        self.dst_entry = None
        self.dst_check_label = None
        self.dst_test_label = None
        self.dst_type = None

        self.size_entry = None
        self.size_check_label = None

        self.start_btn = None
        self.check_btn = None

        self.prog_bar = None
        self.prog_text = None

        self.cropper = None

        self.init_gui()

    def init_gui(self):

        self.init_frames()
        self.window.mainloop()

    def init_frames(self):
        top_frame = tk.Frame(self.window)
        title = tk.Label(top_frame, text=self.prog_title)
        title.config(anchor=tk.CENTER, font=("none", self.title_size))
        title.pack()
        top_frame.pack()

        frame = tk.Frame(self.window)

        frame.columnconfigure([0, 5], minsize=20)
        frame.rowconfigure([0, 10], minsize=20)

        # Source
        src_label = tk.Label(frame, text="Source Settings: ")
        src_label.config(font=("none", self.reg_size))
        src_label.grid(row=0, column=0, padx=10, sticky="sw")

        src_browse_btn = tk.Button(frame, text="Browse", width=6, height=1, command=lambda: self.browse_folder(True))
        src_browse_btn.config(font=f"none {self.small_size}")
        src_browse_btn.grid(row=1, column=0, sticky="ne", padx=10)

        self.src_entry = tk.Entry(frame, width=50)
        self.src_entry.grid(row=1, column=1)

        self.src_check_label = tk.Label(frame, text="X")
        self.src_check_label.config(font=f"none {self.reg_size} bold", fg='red')
        self.src_check_label.grid(row=1, column=2)

        type_src_label = tk.Label(frame, text="Type:")
        type_src_label.config(font=("none", self.reg_size))
        type_src_label.grid(row=1, column=3, sticky="ne", padx=10)

        self.src_type = tk.Entry(frame, width=5)
        self.src_type.config(font=f"none {self.reg_size}")
        self.src_type.insert(tk.END, 'png')
        self.src_type.grid(row=1, column=4)

        self.src_test_label = tk.Label(frame, text="    ")
        self.src_test_label.config(font=f"none 10 bold")
        self.src_test_label.grid(row=2, column=1)

        # Destination
        dst_label = tk.Label(frame, text="Destination Settings: ")
        dst_label.config(font=("none", self.reg_size))
        dst_label.grid(row=4, column=0, padx=10, sticky="sw")

        dst_browse_btn = tk.Button(frame, text="Browse", width=6, height=1, command=lambda: self.browse_folder(False))
        dst_browse_btn.config(font=f"none {self.small_size}")
        dst_browse_btn.grid(row=5, column=0, sticky="ne", padx=10)

        self.dst_entry = tk.Entry(frame, width=50)
        self.dst_entry.grid(row=5, column=1)

        self.dst_check_label = tk.Label(frame, text="X")
        self.dst_check_label.config(font=f"none {self.reg_size} bold", fg='red')
        self.dst_check_label.grid(row=5, column=2)

        type_dst_label = tk.Label(frame, text="Type:")
        type_dst_label.config(font=("none", self.reg_size))
        type_dst_label.grid(row=5, column=3, sticky="ne", padx=10)

        self.dst_type = tk.Entry(frame, width=5)
        self.dst_type.config(font=f"none {self.reg_size}")
        self.dst_type.insert(tk.END, 'png')
        self.dst_type.grid(row=5, column=4)

        self.dst_test_label = tk.Label(frame, text="    ")
        self.dst_test_label.config(font=f"none {self.small_size} bold")
        self.dst_test_label.grid(row=7, column=1)

        # Size
        size_label = tk.Label(frame, text="Crop size: ")
        size_label.config(font=("none", self.reg_size))
        size_label.grid(row=8, column=0, padx=10, sticky="sw")

        size_label = tk.Label(frame, text="Size (px):")
        size_label.config(font=("none", self.reg_size))
        size_label.grid(row=9, column=0, padx=10, sticky="ne")

        self.size_entry = tk.Entry(frame, width=10)
        self.size_entry.grid(row=9, column=1, sticky="sw")
        self.size_entry.config(font=("none", self.reg_size))
        self.size_entry.insert(tk.END, '400')

        self.size_check_label = tk.Label(frame, text="X")
        self.size_check_label.config(font=f"none {self.reg_size} bold", fg='red')
        self.size_check_label.grid(row=9, column=2)

        frame.pack()

        dmy_label = tk.Label(self.window, text=" ")
        dmy_label.config(font=f"none 10 bold")
        dmy_label.pack()

        self.check_btn = tk.Button(text="Check", width=8, height=2, command=self.check_input)
        self.check_btn.config(font=f"none {self.reg_size} bold")
        self.check_btn.pack()

        self.start_btn = tk.Button(text="Start", width=8, height=2, command=self.start_cropping, state=tk.DISABLED)
        self.start_btn.config(font=f"none {self.reg_size} bold")
        self.start_btn.pack(pady=10)

        prog_frame = tk.Frame(self.window)
        prog_frame.columnconfigure([0, 2], minsize=20)
        prog_frame.rowconfigure([0, 3], minsize=20)

        self.prog_text = tk.Label(prog_frame, text="Progress:")
        self.prog_text.config(font=("none", self.reg_size))
        self.prog_text.grid(row=1, column=1, padx=10)

        self.prog_bar = Progressbar(prog_frame, orient=tk.HORIZONTAL,
                                    length=self.bar_length, mode='determinate')
        self.prog_bar.grid(row=2, column=1)

        prog_frame.pack()

    def check_input(self) -> None:

        src_str = self.src_entry.get()
        src_type = self.src_type.get()

        dts_str = self.dst_entry.get()
        dst_type = self.dst_type.get()

        size = int(self.size_entry.get())

        fl_type = False

        src_stat = check_ex(src_str)
        dst_stat = check_ex(dts_str, True)

        if (src_type in self.type_list) or (dst_type in self.type_list):
            fl_type = True

        if src_stat == 1:
            self.src_check_label.config(text="V", fg='green')
        else:
            self.src_check_label.config(text="X", fg='red')
            self.src_test_label.config(text="Path does not exist!", fg='red', font=f"none 10 bold")
        if dst_stat == 1:
            self.dst_check_label.config(text="V", fg='green')
            self.dst_test_label.config(text="Path is found.", fg='green', font=f"none 10 bold")
        elif dst_stat == 2:
            self.dst_check_label.config(text="V", fg='dark orange')
            self.dst_test_label.config(text="Path is created!", fg='dark orange', font=f"none 10 bold")
        else:
            self.dst_check_label.config(text="X", fg='red')
            self.dst_test_label.config(text="Path does not exist!", fg='red', font=f"none 10 bold")
        if 0 < size < 2000:
            self.size_check_label.config(text="V", fg='green')
        else:
            self.size_check_label.config(text="X", fg='red')

        if (src_stat == 1) and (dst_stat > 0) and fl_type:
            self.start_btn.config(state=tk.ACTIVE)
            self.cropper = Cropper(src_str, dts_str, src_type, dst_type, size)
            self.src_test_label.config(text=f"{len(self.cropper)} images are found.", fg='green', font=f"none 10 bold")

    def browse_folder(self, s_d: bool) -> None:
        filename = filedialog.askdirectory()

        if s_d:
            self.src_entry.insert(0, filename)
        else:
            self.dst_entry.insert(0, filename)

    def start_cropping(self):

        self.check_btn.config(state=tk.DISABLED)
        self.start_btn.config(state=tk.DISABLED)

        n_images = len(self.cropper)

        sum_crops = 0

        for img_idx, img_path in enumerate(self.cropper.src_list):

            sum_crops += self.cropper.img2crops(img_path)

            self.prog_bar['value'] = ((img_idx + 1) / n_images) * 100
            self.prog_text.config(text=f"Progress: {self.prog_bar['value']:.1f}%")
            self.window.update()

        self.check_btn.config(state=tk.ACTIVE)
        self.prog_text.config(text=f"Progress: Done! {sum_crops} files were created.")


if __name__ == "__main__":
    g = GUI()

    # C:\Users\Serge\Desktop\Sensors submittion\System IEEE\Figures
