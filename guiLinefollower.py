import tkinter as tk
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from ttkbootstrap.dialogs import Messagebox
import serial

class MonitorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TRAFOBOT")
        self.root.geometry('1250x850')
        root.bind("<Escape>", lambda e: root.destroy())

        self.judul= ["MOTOR", "ASERVO"]
        self.entries= []
        self._setup_ui()

        try:
            self.serial_conn = serial.Serial('COM8', 115200, timeout= 1) 
        except serial.SerialException:
            Messagebox.show_error("Tidak Bisa membuka COM8", "EROR")
            self.serial_conn = None



    def _setup_ui(self):
        #HEADER JUDUL
        header = ttk.Label(self.root, text="SISTEM MOTOR MONITORING", font=("Hevetica", 16, "bold"), bootstyle="primary")
        header.pack(pady=10)
        #HEADER2 TRAFOBOT

        my_label = ttk.Label(self.root, text="TRAFOBOT",font=("Verdana", 20, "bold", "underline"))
        my_label.place(x=20,y=20)
        
        #KONTAINER UTAMA
        content_frame=ttk.Frame(self.root)
        content_frame.pack(padx=20, pady=20, fill="both", expand=True)

        # ANAK DARI KONTAINER UTAMA
        left_frame= ttk.Labelframe(content_frame, text="Input Kontrol", bootstyle="succes")
        left_frame.pack(side="left", anchor='nw', padx=10,pady=10)

        right_frame= ttk.Labelframe(content_frame, text="Kontrol Arah", bootstyle="info")
        right_frame.pack(anchor="n", padx=10, pady=10)

        log_frame = ttk.LabelFrame(content_frame, text="Log Aktivitas", bootstyle="succes")
        log_frame.pack(side="bottom", anchor="s", padx=20,pady=20)
        log_frame.configure(width=500, height=300)
        log_frame.grid_propagate(False)

        self._create_button(right_frame)
        self._create_widgets(left_frame)

    def _create_widgets(self, parent):
        for i, field in enumerate(self.judul):
            ttk.Label(parent, text=f"{field}:", bootstyle="primary", font=("Helvetica", 11, "bold")).grid(row=i*2, column=0, padx=10, pady=5, sticky='w')
            
            entry = ttk.Entry(parent, bootstyle="primary")
            entry.grid(row=i*2 +1 , column=0, padx=10, pady=5, sticky='w')
            self.entries.append(entry)

            ttk.Button(parent, text="OKE", command=lambda e=entry,
                       f=field: self._validate_input(e,f)).grid(row=i*2 + 1, column=1, padx=5,pady=5)
            
    
    def _create_button(self,parent):
        center_frame = ttk.Frame(parent)
        center_frame.pack(expand=YES)
        ttk.Button(center_frame, text="MAJU", width=12,padding=(30,15)).grid(row=0, column=1, pady=20)
        ttk.Button(center_frame, text="KIRI", width=12, padding=(30,15)).grid(row=1,column=0,pady=20)
        ttk.Button(center_frame, text="KANAN", width=12, padding=(30,15)).grid(row=1, column=2,pady=20)
        ttk.Button(center_frame, text="MUNDUR", width=12, padding=(30,15)).grid(row=2, column=1,pady=20)



    def _validate_input(self, entry, label_text):
        value = entry.get()
        if value.isdigit() and 0 <= int(value) <= 200:
         Messagebox.show_info("Sukses", f"{label_text} sebesar: {value}")
         if self.serial_conn and self.serial_conn.is_open:
            try:
                self.serial_conn.write(f"{label_text}:{value}\n".encode())
            except serial.SerialException:
                Messagebox.show_error("Error", "Gagal mengirim data ke perangkat Serial.")
        else:
            Messagebox.show_warning("Error", f"yang bener masukin angkanya {label_text}!")

# Jalankan program
if __name__ == "__main__":
    root = ttk.Window(themename="superhero")
    app = MonitorApp(root)
    root.bind("<Escape>", lambda e: root.destroy())
    root.mainloop()
