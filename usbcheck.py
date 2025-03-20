import psutil

def is_usb_connected():
    """Check if a USB storage device is connected"""
    partitions = psutil.disk_partitions()
    for partition in partitions:
        if 'removable' in partition.opts:  # Check if the device is removable (USB)
            print(f"USB device detected: {partition.device}")
            return True
    print("No USB device detected.")
    return False

# Run the check
is_usb_connected()
