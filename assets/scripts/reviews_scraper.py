# Import necessary modules
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import time

# Create a firefox webdriver instance
driver = webdriver.Firefox()

# Get the webpage
driver.get('https://www.udacity.com/catalog/all/any-price/any-school/any-skill/any-difficulty/any-duration/nanodegree%20program/most-popular/page-1')
# Create an empty dataframe
df = pd.DataFrame()

for count in range(2):
    # Delay program until the DOM loads
    time.sleep(10)
    # Locate the course elements
    course_elements = driver.find_elements(By.CLASS_NAME, 'css-c5zt4b')
    # Scrape reviews from each course
    for i in range(len(course_elements)):
        # Create an empty list of dictionaries
        reviews_data = []
        # Create an empty ratings list
        ratings = []
        # Create an empty reviews list
        reviews = []
        # Delay program until the DOM loads
        time.sleep(10)
        # Get the target element
        course_element = driver.find_element(By.XPATH, f'//*[@id="__next"]/div/main/div/div/section/div[2]/div[2]/div/div/article[{i + 1}]')
        # Scroll the course element into view
        driver.execute_script('arguments[0].scrollIntoView(false);',course_element)
        # Get the course name
        course_name = course_element.find_element(By.CLASS_NAME, 'css-1rsglaw').text
        # Display the current course being scraped
        print(f'Scraping {course_name.lower()} reviews...')
        # Delay the program until the element is in view
        time.sleep(5)
        # Navigate into the target course
        course_element.click()
        # Delay the program until the DOM loads
        time.sleep(5)
        # Scroll the reviews into view if they exist
        try:
            total_reviews = driver.find_element(By.CLASS_NAME, 'css-14244ja')
            total_reviews.click()
            # Get the next button
            reviews_next_button = driver.find_element(By.XPATH, '//*[@id="reviews"]/div/div[6]/div/button[2]')

            while True:
                time.sleep(2)
                rating_containers = driver.find_elements(By.CLASS_NAME, 'css-8g8ihq')
                for container in rating_containers:
                    rating_element = container.find_element(By.CLASS_NAME, 'css-nbgxi6')
                    rating = float(rating_element.get_attribute('aria-label').split(' ')[1])
                    ratings.append(rating)

                # Scrape reviews
                review_elements = driver.find_elements(By.CLASS_NAME, 'css-lcp7nv')
                for review in review_elements:
                    reviews.append(review.text)

                # Scroll the next button into view
                driver.execute_script('arguments[0].scrollIntoView(false);', reviews_next_button)
                # Delay the program for 2 seconds
                time.sleep(2)
                # Click the next button if it is enabled
                if reviews_next_button.is_enabled():
                    reviews_next_button.click()
                    # driver.execute_script('window.scrollTo(0, 0)')
                    # time.sleep(2)
                    # total_reviews.click()
                    time.sleep(2)
                else:
                    break
            # Add scraped data into a dictionary
            course_reviews = {
                'course_name': course_name,
                'reviews': reviews,
                'ratings': ratings
            }
            # Append each course dictionary into the reviews_data list
            reviews_data.append(course_reviews)
            # Create a dataframe from the list of dictionaries
            current_df = pd.DataFrame(reviews_data).explode(['reviews', 'ratings'])
            # Concatenate the current dataframe to the initial dataframe
            df = df._append(current_df, ignore_index=True)
            # Print the length of the reviews_data list
            print(f'Current total no. of rows: {df.shape[0]}')
            # Move back in window history
            driver.back()
        except NoSuchElementException:
            # Log the name of the course with no reviews
            print(f'{course_name}: No reviews')
        finally:
            # Move back in window history if there are no reviews for the course
            driver.back()
    time.sleep(5)
    course_next_button = driver.find_element(By.XPATH, '//*[@id="__next"]/div/main/div/div/section/div[2]/div[3]/div/button[2]')
    time.sleep(5)
    driver.execute_script('arguments[0].scrollIntoView(false);', course_next_button)
    time.sleep(2)
    course_next_button.click()
    time.sleep(2)

# Preview the first five rows dataframe created
print('\n')
df.info()

# Convert the pandas dataframe into a .csv file
df.to_csv('udacity_reviews.csv')

# Quit the browser when done
driver.quit()
