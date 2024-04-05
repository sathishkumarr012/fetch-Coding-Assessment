from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
import time

class PageActions:
    left = "left"
    right = "right"

    ALERT_MESSAGE_RIGHT = "Yay! You find it!"
    ALERT_MESSAGE_WRONG = "Oops! Try Again!"

    @staticmethod
    def open_page():
        # Maximizes the window and launches Google Chrome to the webpage for the scaling simulation
        driver = webdriver.Chrome()
        driver.get("http://sdetchallenge.fetch.com/")
        driver.maximize_window()
        return driver

    @staticmethod
    def click_weigh_button(driver):
        # Clicks the weigh button
        original_length_of_weighings = len(PageActions.get_weighings_list(driver))

        button = driver.find_element(By.ID, "weigh")
        button.click()

        # Wait until weighing list is updated
        WebDriverWait(driver, 10).until(lambda d: len(PageActions.get_weighings_list(d)) > original_length_of_weighings)

    @staticmethod
    def click_reset_button(driver):
        # Clicks reset button
        button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[4]/button")
        button.click()

    @staticmethod
    def get_weighings_list(driver):
        # Gets the list of weighings from the webpage
        ol = driver.find_element(By.CSS_SELECTOR, "#root > div > div.game > div.game-info > ol")
        weighings = ol.find_elements(By.TAG_NAME, "li")
        return weighings

    @staticmethod
    def get_result(driver):
        # Gets the result (comparison operator in between boxes)
        button = driver.find_element(By.XPATH, "/html/body/div/div/div[1]/div[2]/button")
        return button.text

    @staticmethod
    def set_bowl_cell_value(driver, bowl, box_number, bar_number):
        # Fills the 'bar_number' in corresponding 'box_number' of the 'bowl' (left or right)
        cell = driver.find_element(By.ID, f"{bowl}_{box_number}")
        cell.send_keys(str(bar_number))

        WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element_value((By.ID, f"{bowl}_{box_number}"), str(bar_number)))

    @staticmethod
    def load_bowl(driver, bowl, bar_positions):
        # Fills the corresponding 'bowl' with elements in 'bar_positions'
        for entry in bar_positions:
            box_number, bar_number = entry
            PageActions.set_bowl_cell_value(driver, bowl, box_number, bar_number)

    @staticmethod
    def redistribute_bowl(driver, source_bowl, target_bowl, source_bowl_positions, target_bowl_positions):
        # Empties the destination bowl and redistributes the contents of the source bowl evenly,
        # ensuring that half of the elements remain in the source bowl and the other half are transferred to the target bowl.
        PageActions.click_reset_button(driver)

        target_bowl_positions.clear()
        length = len(source_bowl_positions)
        mid = length // 2
        target_start_position = 0

        for i in range(length - 1, mid - 1, -1):
            position = source_bowl_positions.pop(i)
            position[0] = target_start_position
            target_bowl_positions.append(position)
            target_start_position += 1

        PageActions.load_bowl(driver, source_bowl, source_bowl_positions)
        PageActions.load_bowl(driver, target_bowl, target_bowl_positions)

    @staticmethod
    def click_fake_bar_and_get_alert(driver, bar_number):
        # Clicks the fake gold bar and gets the alert message
        bar = driver.find_element(By.ID, f"coin_{bar_number}")
        bar.click()
        time.sleep(10)

        alert = Alert(driver)
        message = alert.text
        alert.accept()
        

        return message

    @staticmethod
    def verify_alert_message(expected_alert, actual_alert):
        # Verifies alert message is right/wrong based on if fake bar number clicked is correct/incorrect.
        if expected_alert:
            return PageActions.ALERT_MESSAGE_RIGHT == actual_alert
        else:
            return PageActions.ALERT_MESSAGE_WRONG == actual_alert


class GoldBarGameTest:
    left_bowl_positions = []
    right_bowl_positions = []
    fake_bar = -1

    @staticmethod
    def main():
        driver = PageActions.open_page()
        print("------------------------")
        print("Game Page Open")
        print("Test Started")

        GoldBarGameTest.left_bowl_positions = [
            [0, 0],
            [1, 1],
            [2, 2],
            [3, 3]
        ]

        # Fill the left bowl with 4 bars
        PageActions.load_bowl(driver, PageActions.left, GoldBarGameTest.left_bowl_positions)

        GoldBarGameTest.right_bowl_positions = [
            [0, 4],
            [1, 5],
            [2, 6],
            [3, 7]
        ]

        # Fill the right bowl with remaining 4 bars
        PageActions.load_bowl(driver, PageActions.right, GoldBarGameTest.right_bowl_positions)

        # Execute the loop until fake bar is found
        while len(GoldBarGameTest.left_bowl_positions) > 1 or len(GoldBarGameTest.right_bowl_positions) > 1:
            PageActions.click_weigh_button(driver)
            result = PageActions.get_result(driver)
            
            if result == "<":
                PageActions.redistribute_bowl(driver, PageActions.left, PageActions.right, GoldBarGameTest.left_bowl_positions, GoldBarGameTest.right_bowl_positions)
            elif result == ">":
                PageActions.redistribute_bowl(driver, PageActions.right, PageActions.left, GoldBarGameTest.right_bowl_positions, GoldBarGameTest.left_bowl_positions)
            else:
                GoldBarGameTest.fake_bar = 3
                break

        if GoldBarGameTest.fake_bar != 3:
            PageActions.click_weigh_button(driver)
            result = PageActions.get_result(driver)
            if result == "<":
                GoldBarGameTest.fake_bar = GoldBarGameTest.left_bowl_positions[0][1]
            else:
                GoldBarGameTest.fake_bar = GoldBarGameTest.right_bowl_positions[0][1]

        # Test the result
        alert_message = PageActions.click_fake_bar_and_get_alert(driver, GoldBarGameTest.fake_bar)
        is_alert_correct = PageActions.verify_alert_message(True, alert_message)
        if not is_alert_correct:
            print(f"Actual Alert Message: {alert_message}")
        assert is_alert_correct
        

        # Output the result
        print("Test Completed")
        print("------------------------")
        print(f"Alert message is :{alert_message} ")
        print("Weighings list ")
        weighings = PageActions.get_weighings_list(driver)
        for i, element in enumerate(weighings):
            text = element.text
            print(f"Weighing {i + 1}: {text}")
        
        print(f"Number of weighings: {len(weighings)}")
        print(f"Fake Goldbar Number is {GoldBarGameTest.fake_bar}")
        time.sleep(5)
        driver.quit()


if __name__ == "__main__":
    GoldBarGameTest.main()
