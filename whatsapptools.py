import time
import os
import pickle
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ---------- CONFIG ---------- #

list_wrong_numbers = []
successful_numbers = []


#whatsapp drive class
class WhatsAppDriver:
    def __init__(self):
        pass
    def login(self):
        self.driver = webdriver.Chrome()
        self.driver.get("https://web.whatsapp.com")
        self.WAIT = 5  # seconds between steps
        self.wait = WebDriverWait(self.driver, 200)
        self.wait2 = WebDriverWait(self.driver, 20)
        self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@role="textbox"]'))
        )
        time.sleep(60)
        print("✅ Logged in to WhatsApp Web")
        
    def collect_numbers_from_whatsapp(self, title):
         # Wait for search box
        search_box = self.wait.until(
            EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
        )

        # ✅ Wait for any overlay/dialog to disappear
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//div[@role="dialog"]'))
            )
        except:
            print("⚠️ Dialog did not disappear in time. Trying to continue anyway.")

        # ✅ Try JS click to bypass overlay if needed
        try:
            self.driver.execute_script("arguments[0].click();", search_box)
        except Exception as e:
            print(f"⚠️ JavaScript click failed: {e}")
            return set()

        time.sleep(1)
        search_box.send_keys(Keys.CONTROL + "a")
        search_box.send_keys(Keys.DELETE)
        search_box.send_keys(title)
        time.sleep(2)
        search_box.send_keys(Keys.ENTER)
        time.sleep(3)

        # Wait for header span to load
        try:
            title_span = self.wait.until(
                EC.presence_of_element_located((By.XPATH, '//header//span[@title]'))
            )
            title_content = title_span.get_attribute("title")

            # Extract numbers
            items = [item.strip() for item in title_content.split(",")]
            number_set = set()
            for item in items:
                if item.startswith("+") and item[1:].replace(" ", "").isdigit():
                    number_set.add(item)

            print(f"\n✅ Extracted {len(number_set)} numbers from header:")
            print(number_set)
            return number_set

        except Exception as e:
            print("❌ Failed to extract numbers from header:", e)
            return set()
        
    def send_message_to_contact(self,number, message, ):
        try:
            WebDriverWait(self.driver, 10).until(
                EC.invisibility_of_element_located((By.XPATH, '//span[@data-icon="new-chat-outline"]'))
            )
        except:
            print("⚠️ Dialog did not disappear in time. Trying to continue anyway.")

        number=number
        message=message
        try:
            print(f"📨 Sending to: {number}")
            # ✅ Click "New Chat" button
            new_chat_btn =self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="new-chat-outline"]')))
            new_chat_btn.click()
            time.sleep(2)

            # ✅ Search for number
            search_box =self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            search_box.clear()
            search_box.send_keys(number)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)
            # ✅ Wait for chat to open or fallback if invalid
            try:
                no_results = self.driver.find_element(
                    By.XPATH,
                    f"//span[contains(text(), 'No results found for')]"
                )
                if no_results:
                    print(f"❌ No contact found for: {number}")
                    return
            except:
                pass 
            try:
                # Check if message box appears
                message_box =self.wait2.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
            except:
                print(f"⚠️ Chat not opened — number likely invalid: {number}")
                # Click refresh/back to reset the UI
                try:
                    back_btn = self.driver.find_element(By.XPATH, '//span[@data-icon="back-refreshed"]')
                    back_btn.click()
                except:
                    print("❌ Unable to find back button, skipping this number.")
                return

            # ✅ Send message
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            time.sleep(self.WAIT)

        
            send_btn = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_btn.click()
            time.sleep(self.WAIT)

            print(f"✅ Sent to {number}")
            successful_numbers.append(number)

        except Exception as e:
            print(f"❌ Error with {number}: {e}")
            list_wrong_numbers.append(number)
            time.sleep(2)

    def send_message_img_to_contact(self,number, message,image_path):
     try:
        input("iam ready to send message, press enter")
        if not os.path.exists(image_path):
            print(f"❌ Image not found at: {image_path}")
            return
        number=number
        message=message
        try:
            print(f"📨 Sending to: {number}")
            # ✅ Click "New Chat" button
            new_chat_btn =self.wait.until(EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="new-chat-outline"]')))
            new_chat_btn.click()
            time.sleep(2)

            # ✅ Search for number
            search_box =self.wait.until(EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]')))
            search_box.clear()
            search_box.send_keys(number)
            time.sleep(2)
            search_box.send_keys(Keys.ENTER)
            time.sleep(3)

            # ✅ Wait for chat to open or fallback if invalid
            try:
                # Check if message box appears
                message_box =self.wait.until(EC.presence_of_element_located(
                    (By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')))
            except:
                print(f"⚠️ Chat not opened — number likely invalid: {number}")
                # Click refresh/back to reset the UI
                try:
                    back_btn = self.driver.find_element(By.XPATH, '//span[@data-icon="back-refreshed"]')
                    back_btn.click()
                except:
                    print("❌ Unable to find back button, skipping this number.")
                return

            # ✅ Send message
            message_box.send_keys(message)
            message_box.send_keys(Keys.ENTER)
            time.sleep(self.WAIT)

        

           
            send_btn = self.driver.find_element(By.XPATH, '//span[@data-icon="send"]')
            send_btn.click()
            time.sleep(self.WAIT)

            print(f"✅ Sent to {number}")
            successful_numbers.append(number)

        except Exception as e:
            print(f"❌ Error with {number}: {e}")
            list_wrong_numbers.append(number)
            time.sleep(2)
     except Exception as e:
      return "enter the corretc image path"
     

