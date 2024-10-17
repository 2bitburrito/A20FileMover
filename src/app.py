from typing import Union

import customtkinter as ctk
import os
from typing import Union, Callable
from utils.enums import Colour
from controllers.main_controller import MainController
from controllers.macos_drive_controller import MacUsbDeviceController
from controllers.linux_drive_controller import LinuxDeviceHandler
from utils.system_get import SystemGet
from controllers.mac_usb_controller_v1 import MacUsbControlerV1


# when calling a function from any of the controller modules the syntax is 
# "self.[_reference to controller as listed in script].function

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")  
        
        # configure the window
        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)  
        
        self.geometry("1000x500")
        self.title("A20 TX File Mover")
        

        system_get = SystemGet()
        system_platform = system_get.system_trigger()

        if system_platform == "Darwin":
            self._usb_controller = MacUsbControlerV1()
        elif system_platform == "Linux":
            self._usb_controller  = LinuxDeviceHandler()
        else:
            raise Exception(f"Unsupported platform: {system_platform}")


        # init controllers
        self._controller = MainController()
        # self._usb_controller = MacUsbDeviceController()   
         

        self.grid_rowconfigure((0), weight=0)
        self.grid_rowconfigure((1), weight=1)
        self.grid_columnconfigure((0,1,2), weight=1)

        self.A20_path = ""
        self.folder_path = ""
        self.create_layout()
        self.create_tx_buttons()

# Heading
    def create_layout(self):

        self.frame_header = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_header.grid(row=0, columnspan=3, padx=1, pady=1, sticky="nswe")
        
        self.label_heading =ctk.CTkLabel(self.frame_header)
        self.label_heading.pack(side="left", padx=10, pady=10)
        self.label_heading.configure(text="A20 TX - FILE MOVER", font=("Inclusive Sans", 25))
        

        self.time_heading =ctk.CTkLabel(self.frame_header)
        self.time_heading.pack(side="right", padx=10)
        self.time_heading.configure(text=f"{self._controller.global_time()}", font=("Inclusive Sans", 15))
        
        self.frame_left = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_left.grid(row=1, column=0, rowspan=2, padx=1, pady=1, sticky="nswe")
        self.frame_left.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        self.frame_middle = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_middle.grid(row=1, column=1, rowspan=2, padx=1, pady=1, sticky="nswe")
        self.frame_middle.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)

        self.frame_right = ctk.CTkFrame(self, fg_color=Colour.NORD.value)
        self.frame_right.grid(row=1, column=2, rowspan=2, padx=1, pady=1, sticky="nswe")
        self.frame_right.configure(border_width=1, border_color=Colour.BACKGROUND_DARK.value)
        
        # self.folder_path_select = ctk.CTkButton(self.frame_middle, text="Choose Folder Path", command=self.update_textbox_with_folder_path)
        # self.folder_path_select.pack(pady=20)

# Folder Stuff

        self.folder_path_button = ctk.CTkButton(self.frame_middle, text="Choose Destination", command=self.update_label_with_folder_path)
        self.folder_path_button.pack(pady=20)
        self.folder_path_button.configure(fg_color=Colour.ORANGE.value)


        self.folder_label = ctk.CTkLabel(self.frame_middle)
        self.folder_label.pack(fill="x", expand=True, pady=10, padx=20)
        self.folder_label.configure(text="Placeholder Folder Ha!", font=("Inclusive Sans", 15))





# Manually select path to A20 mount

        self.A20_path_button = ctk.CTkButton(self.frame_left, text="Manually Choose A20", command=self.manual_a20_sel_to_textbox)
        self.A20_path_button.pack(pady=20)
        self.A20_path_button.configure(fg_color=Colour.ORANGE.value)

        self.A20_instance_frame = ctk.CTkFrame(self.frame_left)
        self.A20_instance_frame.pack(side="bottom", fill="both", pady=10, padx=10, ipady=300)
        self.A20_instance_frame.configure(fg_color=Colour.BACKGROUND_COLOR.value, border_width=1, border_color=Colour.OFF_WHITE.value)
        
        self.A20_instance_label = ctk.CTkLabel(self.A20_instance_frame)
        self.A20_instance_label.pack(padx=5, pady=5)
        self.A20_instance_label.configure(text="Transmitter List", font=("Inclusive Sans", 20))
        
        self.A20_textbox = ctk.CTkTextbox(self.frame_middle, height=300)
        self.A20_textbox.pack(side= "bottom", fill="x", expand=True, pady=10, padx=20)
        self.A20_textbox.insert("2.0", "You're files will display here...") # placeholder text
        self.A20_textbox.configure(border_width=1, border_color=Colour.OFF_WHITE.value)

        self.move_files_button = ctk.CTkButton(self.frame_right, text="Move Files to Folders", command=self.call_move_files)
        self.move_files_button.pack(pady=20)
        
# Progress bar

        self.progressbar = ctk.CTkProgressBar(self.frame_right)
        self.progressbar.pack(padx=10, pady=10)
        self.progressbar.configure(fg_color=Colour.ORANGE.value, progress_color=Colour.OFF_WHITE.value)
        self.progressbar.set(0)
        
        self.drive_buttons = {}
    
    updated_date = MainController.A20_convert_name
    
    
    
    
    

    
    
    def manual_a20_sel_to_textbox(self):
            """_summary_
            passes the contents of a manually selected drive through the file renamer to the a20 textbox
            """
            
            path = self._controller.select_A20_path()
            new_names = self._controller.A20_convert_name(path)
            self.A20_textbox.delete("1.0", "end")
            for name in new_names:
                self.A20_textbox.insert("end", name + "\n")

    
    
    
    
    
    
    def update_label_with_folder_path(self):
        
        self.folder_path = self._controller.select_folder_path()
        if self.folder_path:
            folder_list = os.listdir(self.folder_path)
    # self.folder_label.delete("1.0", "end")
            self.folder_label.configure(text=f"PATH:\n{self.folder_path}", font=("Inclusive Sans", 15))
                                          

    
    
    

    
    
    def create_tx_buttons(self, tx_info=None):
        
        if tx_info is None:
            tx_info = self._usb_controller.list_drives()

    # Clear existing drive buttons
        for button in self.drive_buttons.values():
            button.destroy()
        self.drive_buttons.clear()        
        for drive_info in tx_info:
            a20_mount_point: str = drive_info.get('mountpoint')  

            a20_drive_label: str = a20_mount_point.replace("/Volumes/","")  # strips out just the name label
    # Create a new button
            button = ctk.CTkButton(self.A20_instance_frame, text=f"TX: {a20_drive_label}", command=lambda mount_point=a20_mount_point: self.handle_drive_selection(mount_point))
            button.pack(pady=10)  # Adjust layout as needed       

    # Store the button in the dictionary for future reference
            self.drive_buttons[a20_mount_point] = button 
        self.after(5000, self._usb_controller.list_drives)
                
    
    
    def handle_drive_selection(self, a20_mount_point):
    # Convert the file names using the A20_convert_name method
     
        if a20_mount_point:
            try:
                converted_names = self._controller.A20_convert_name(a20_mount_point)
                self.A20_textbox.delete("1.0", "end") 
                for name in converted_names:
                    self.A20_textbox.insert("end", name + "\n")
                print(f"Selected drive: {a20_mount_point}")
            except ValueError:
                print("Couldn't load a20 mount pointt")
        

    

    
    
    def update_progress(self, progress):
        self.progressbar.set(progress)

    
    
    
    
    def call_move_files(self):
        
        if self.A20_path and self.folder_path:
            self._controller.move_files(self.A20_path, self.folder_path, self.update_progress)
        else:
            print("Please select both paths before moving files.")

app = App()
app.mainloop()
