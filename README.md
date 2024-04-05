# Fetch Coding Exercise - SDET

This project involves the utilization of Python with Selenium for executing various tasks.

This script is used to conduct tests on the provided [Game](http://sdetchallenge.fetch.com/).

## Tech Stack:

- **Programming Language**: Python
- **Version Control**: GitHub

## Getting Started

### Dependencies

- **selnium**: used to interact with web browsers and applications.
- **webdrivermanager**:  Automated driver management and other helper features for Selenium WebDriver in Python.


### Set up

- Make sure you have [Python](https://www.python.org/downloads/) running on your machine.

- Run ```python3 --version``` in terminal and confirm python is installed.

##  Running the script:
- Clone this repo, and in the root folder run the following:

```
 pip install -r requirements.txt
```

- Now all the dependencies are installed.
- To compile and run the scipt, run the following:

```
python GoldBarGameTest.py
```
## Classes and Methods:
### PageActions Class
This class contains methods to interact with the Gold Bar Challenge webpage.

#### Methods:
- open_page(): Opens the game webpage in a Chrome browser.
- click_weigh_button(driver): Clicks the weigh button on the webpage.
- click_reset_button(driver): Clicks the reset button on the webpage.
- get_weighings_list(driver): Retrieves the list of weighings from the webpage.
- get_result(driver): Retrieves the result of the weighing (>, <, or =).
- set_bowl_cell_value(driver, bowl, box_number, bar_number): Fills the specified box in the bowl with the given bar number.
- load_bowl(driver, bowl, bar_positions): Loads the specified bowl with the given bar positions.
- redistribute_bowl(driver, source_bowl, target_bowl, source_bowl_positions, target_bowl_positions): Redistributes the bars between two bowls.
- click_fake_bar_and_get_alert(driver, bar_number): Clicks the fake gold bar, retrieves the alert message, and holds the alert for 10 seconds.
- verify_alert_message(expected_alert, actual_alert): Verifies if the alert message is correct.
  
### GoldBarGameTest Class
This class contains the main method to execute the Gold Bar Challenge automation.

#### Methods:
- main(): Executes the automation script to find the fake gold bar, display the alert message, and output the results.

You will see output similar to below text, once it is started:

```
#######################
Game Page Open
Test Started
Test Completed
#######################
Alert message is :Yay! You find it! 
Weighings list 
Weighing 1: [0,1,2,3] < [4,5,6,7]
Weighing 2: [0,1] > [3,2]
Weighing 3: [2] < [3]
Number of weighings: 3
Fake Goldbar Number is 2
```
