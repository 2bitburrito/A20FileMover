import os
import pyudev
import psutil
import customtkinter as ctk
from tkinter import filedialog, messagebox


class LinuxDeviceHandler:
    def __init__(self):
        super().__init__()
        self.destination_dir = None
        # self.drive_buttons = {} 
        self.list_drives()


    def select_destination(self):
        self.destination_dir = filedialog.askdirectory()
        if self.destination_dir:
            messagebox.showinfo("Destination Set", f"Destination directory set to:\n{self.destination_dir}")

    def get_mount_point(self, device_node):
        """
        Find the mount point of a given block device.
        """
        for partition in psutil.disk_partitions():
            if device_node in partition.device:
                return partition.mountpoint
        return None

    def get_VID(self):
        target_vid = "1fc9"
        context = pyudev.Context()
        devices = []
        for device in context.list_devices(subsystem='usb'):
            vid = device.get('ID_VENDOR_ID')
            if vid == target_vid:
                for child in device.children:
                    if child.subsystem == 'block' and child.device_type == 'disk':
                        mount_point = self.get_mount_point(child.device_node)
                        devices.append({
                            'vid': vid,
                            'mount_point': mount_point,
                            'device_node': child.device_node
                        })
                        print(f"Found device with VID {vid} at {mount_point} ({child.device_node})")
        return devices

    def list_drives(self, update_ui_callback=None):
        """
        get a list of all mounted drives
        """
        drives_info = []
        drives = self.get_VID()
        # new_drives = set(device['device_node'] for device in drives)

        for drive in drives:
            device_node = drive['device_node']
            mount_point = drive['mount_point']
            if mount_point is not None:
                name = os.path.basename(mount_point)
                drives_info.append({
                    'name' : name,
                    'vid' : "some vid",
                    'mountpoint' : mount_point
                })
                print(f"{name}:{drives}")

            else:
                print(f"Warning: No mount point found for device {device_node}")
        
        if update_ui_callback:
            update_ui_callback(drives)

        return drives_info
        

if __name__ == "__main__":
    controller = LinuxDeviceHandler()
    # devices = controller.update_drive_list()

   
    # app.mainloop()   
    