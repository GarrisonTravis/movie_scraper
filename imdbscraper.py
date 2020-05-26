# Garrison Travis
# imdb web scraper
# Program that gets all movies/tv shows for an actor/actress from user input
# Can also supply a rating to get the last 5 projects with a rating higher than user input rating

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options


# Function that gets the last 5 movies/tv shows that have a better rating than the rating given by the user
def rating_specific(rating_greater_than, movies, driver):
    # Iterate through all the movies/tv shows
    count = 0
    project = []
    projects = []
    for i in range(0, len(movies)):
        # Click on the actor/actress tab to get the list of movies/tv shows they have acted in
        # Necessary because they might have a tab for producer before the actor tab
        actor_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
            (By.XPATH, "//a[contains(@href, '#act')]"))).click()

        # Have to find the movies again, if this isn't done will get a stale element exception
        movies = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located(
            (By.XPATH, "//div[contains(@id, 'actor-') or contains(@id, 'actress-')]")))

        # Don't include pre/post production projects
        if "pre-production" not in movies[i].text and "post-production" not in movies[i].text and "announced" not in \
                movies[i].text and "filming" not in movies[i].text and "completed" not in movies[i].text:
            # print(movies[i].get_attribute('innerHTML'))
            character = movies[i].text
            character = character.splitlines()[2]
            title = movies[i].find_element_by_xpath(".//a[contains(@href, 'title')]").text
            year = movies[i].find_element_by_xpath(".//span[contains(@class, 'year_column')]").text
            year = year[1:]  # Remove blank space at beginning

            # Use . to search current web element
            WebDriverWait(movies[i], 10).until(EC.presence_of_element_located((By.XPATH, ".//a[contains(@href, 'title')]"))).click()

            # Find the movie/tv show rating if it exists (might not have a rating yet)
            try:
                rating = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, "//span[contains(@itemprop, 'ratingValue')]"))).text
                if rating > rating_greater_than:
                    count += 1
                    project.append(title)
                    project.append(year)
                    project.append(character)
                    project.append(rating)
                    projects.extend(project)
                driver.back()
            except NoSuchElementException:
                driver.back()
            except TimeoutException:
                driver.back()

            project.clear()

            if count == 5:
                break

    # Print out the projects
    i = 0
    while i < len(projects):
        print(projects[i] + " | " + projects[i+1] + " | " + projects[i+2] + " | " + projects[i+3])
        i += 4


# Function that prints all the movies/tv shows the actor/actress has appeared in
# Will print Date | Title | Character | Episode (If applicable)
def non_rating_specific(movies):
    print("Date | Title | Character | Episode (If applicable)\n")
    for i in movies:
        if "pre-production" not in i.text and "post-production" not in i.text and "announced" not in i.text and "filming" \
                not in i.text and "completed" not in i.text:
            project = i.text.splitlines()

            for j in range(0, 3):
                if j == 2:
                    print(project[j])
                else:
                    print(project[j] + "  |  ", end='')


def main():
    actor_name = input("Enter actor or actress: ")
    # actor_name = actor_name.title()

    choice = input("Rating specific? (yes or no): ")
    if choice == "yes":
        rating_greater_than: str
        rating_greater_than = input("Projects with rating above: ")

    # options = Options()
    # options.headless = True
    # options.add_argument("--window-size=1920,1200")

    DRIVER_PATH = r"C:\Users\gtrav\PycharmProjects\imdbscraper\chromedriver.exe"
    driver = webdriver.Chrome(executable_path=DRIVER_PATH)
    #driver = webdriver.Chrome(options=options, executable_path=DRIVER_PATH)
    driver.get('https://imdb.com')

    # Enter the actor's name into the search bar, hit Enter
    search_bar = driver.find_element_by_id("suggestion-search")
    search_bar.click()
    search_bar.send_keys(actor_name)
    search_bar.send_keys(Keys.ENTER)

    # Click on the actors link to get to their specific page
    actor_link = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "//a[contains(text(), '%s')]" %
                                                                                 actor_name))).click()

    # Click on the actor/actress tab to get the list of movies/tv shows they have acted in
    # Necessary because they might have a tab for producer before the actor tab
    actor_tab = WebDriverWait(driver, 10).until(EC.presence_of_element_located(
        (By.XPATH, "//a[contains(@href, '#act')]"))).click()

    # Get a list of all the movies/tv shows the actor/actress has been in
    movies = WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//div[contains(@id, 'actor-') or contains(@id, 'actress-')]")))

    if choice == "yes":
        rating_specific(rating_greater_than, movies, driver)
    else:
        non_rating_specific(movies)

    driver.quit()


main()
