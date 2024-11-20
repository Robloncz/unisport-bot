from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
from datetime import datetime, timedelta

class UnisportRegistration:
    def __init__(self):
        self.driver = webdriver.Chrome()
        self.driver.maximize_window()
        
    def try_registration(self, duration_minutes=5):
        start_time = datetime.now()
        end_time = start_time + timedelta(minutes=duration_minutes)
        
        while datetime.now() < end_time:
            try:
                print(f"Attempt at {datetime.now().strftime('%H:%M:%S')}")
                
                # Navigate to the football courses page
                self.driver.get("https://unisport.koeln/sportspiele/fussball/kurse/index_ger.html")
                
                # Wait for the table to load
                WebDriverWait(self.driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "isis_table"))
                )
                
                # Store the original window handle
                original_window = self.driver.current_window_handle
                
                # Find the row containing the target course
                rows = self.driver.find_elements(By.CSS_SELECTOR, "table.isis_table tbody tr")
                target_row = None
                
                for row in rows:
                    course_name = row.find_element(By.CSS_SELECTOR, "td[data-tablehead='Bezeichnung']").text
                    if "Level 2 - halbes Feld" in course_name:
                        registration_cell = row.find_element(By.CSS_SELECTOR, "td[data-tablehead='Anmeldung']")
                        
                        # Check if registration is possible
                        if "keine Buchung" not in registration_cell.text:
                            target_row = row
                            print("Registration link found! Attempting to register...")
                            break
                        else:
                            print("Registration not yet available. Retrying...")
                            time.sleep(1)  # Wait 1 second before refresh
                            continue
                
                if target_row:
                    # Found an active registration link
                    book_link = target_row.find_element(By.CSS_SELECTOR, "a[href*='anmeldung.fcgi']")
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", book_link)
                    time.sleep(1)
                    book_link.click()
                    
                    # Wait for the new window to appear
                    WebDriverWait(self.driver, 10).until(EC.number_of_windows_to_be(2))
                    
                    # Switch to the new window
                    for window_handle in self.driver.window_handles:
                        if window_handle != original_window:
                            self.driver.switch_to.window(window_handle)
                            break
                    
                    # Wait for the form to be present
                    WebDriverWait(self.driver, 10).until(
                        EC.presence_of_element_located((By.NAME, "Formular"))
                    )
                    
                    return True
                
            except Exception as e:
                print(f"An error occurred: {e}")
                time.sleep(1)  # Wait before retry
                
        print("Time limit reached. Could not register.")
        return False

    def fill_form(self, user_data):
        try:
            # Select gender
            gender_radio = self.driver.find_element(By.ID, f"{user_data['gender']}")
            gender_radio.click()
            
            # Fill in personal information
            self.driver.find_element(By.NAME, "Vorname").send_keys(user_data['first_name'])
            self.driver.find_element(By.NAME, "Name").send_keys(user_data['last_name'])
            self.driver.find_element(By.NAME, "Strasse").send_keys(user_data['street'])
            self.driver.find_element(By.NAME, "Ort").send_keys(user_data['city'])
            
            # Select status (Student)
            status_select = Select(self.driver.find_element(By.NAME, "Statusorig"))
            status_select.select_by_value("S-UNI")
            
            # Fill in student number
            self.driver.find_element(By.NAME, "Matnr").send_keys(user_data['student_number'])
            
            # Fill in contact information
            self.driver.find_element(By.NAME, "Mail").send_keys(user_data['email'])
            self.driver.find_element(By.NAME, "Tel").send_keys(user_data['phone'])
            
            # Click the first submit button "weiter zur Buchung"
            submit_button = self.driver.find_element(By.CSS_SELECTOR, "input[value='weiter zur Buchung']")
            submit_button.click()
            
            print("Initial form submitted! Proceeding to final confirmation...")
            
            # Wait for the confirmation page and final submit button
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[value='verbindliche Buchung']"))
            )
            
            # Click the final "verbindliche Buchung" button
            final_submit = self.driver.find_element(By.CSS_SELECTOR, "input[value='verbindliche Buchung']")
            final_submit.click()
            
            print("Final registration submitted successfully!")
            time.sleep(5)
            
        except Exception as e:
            print(f"An error occurred while filling the form: {e}")
        
    def close(self):
        self.driver.quit()

# Example usage
if __name__ == "__main__":
    user_data = {
        'gender': 'maennlich',  # or 'weiblich' or 'divers'
        'first_name': 'Rene',
        'last_name': 'Oblonczek',
        'street': 'Eisentraße 43',
        'city': '50825 Koeln',
        'student_number': '7354753',
        'email': 'robloncz@smail.uni-koeln.de',
        'phone': '+491602439105'
    }
    
    bot = UnisportRegistration()
    
    # Try registration for 5 minutes
    if bot.try_registration(duration_minutes=5):
        print("Registration link found and clicked! Filling form...")
        bot.fill_form(user_data)
    else:
        print("Could not find an active registration link within the time limit.")
    
    # Keep the browser open for a few seconds
    time.sleep(120)
    bot.close()