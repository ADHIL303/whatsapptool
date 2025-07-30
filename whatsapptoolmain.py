from whatsapptools import WhatsAppDriver
import os   


# ---------- CONFIG ---------- #MESSAGE = "Hello, this is a test message from Python automation!"
IMAGE_PATH = "path/to/image.jpg"  # Use absolute path
numbers = ["21423", "7406073514", "6235305505", "9744080036"]
MESSAGE = "Hello, this is a test message from Python automation!"
wts = WhatsAppDriver()
# ---------- MAIN ---------- #
successful_numbers = []     
list_wrong_numbers = []
for number in numbers:
        wts.send_message_to_contact(number, MESSAGE)
