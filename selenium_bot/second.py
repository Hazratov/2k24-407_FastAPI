import time
import json
import psycopg2
from time import sleep
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains

# DATABASE CONFIGURATION
DB_HOST = "localhost"
DB_NAME = "selenium"
DB_USER = "postgres"
DB_PASSWORD = "postgres"

# FIREFOX CONFIGURATION
gecko_path = "/snap/firefox/current/usr/lib/firefox/geckodriver"
firefox_path = "/snap/firefox/current/usr/lib/firefox/firefox"

service = Service(gecko_path)
options = webdriver.FirefoxOptions()
options.add_argument("--window-size=1920x1080")
options.add_argument("--incognito")
options.binary_location = firefox_path

driver = webdriver.Firefox(service=service, options=options)

# DATABASE CONNECTION
def connect_to_db():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        return conn
    except Exception as e:
        print(f"Database connection error: {e}")
        return None

# DATA INSERT FUNCTION
def save_project_to_db(title, date, description, image_url, type_badges, technologies, project_links):
    conn = connect_to_db()
    if conn:
        try:
            cursor = conn.cursor()
            insert_query = """
                INSERT INTO projects (title, date_range, description, image_url, type_badges, technologies, project_links)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(insert_query, (
                title.strip(),
                date.strip(),
                description.strip(),
                image_url.strip(),
                json.dumps(type_badges),
                json.dumps(technologies),
                json.dumps(project_links)
            ))
            conn.commit()
            print("✅ Project data saved to database successfully.")
        except Exception as e:
            print(f"❌ Error saving to database: {e}")
        finally:
            cursor.close()
            conn.close()
    else:
        print("❌ Could not connect to database")

# SCRAPER LOGIC
try:
    driver.get("https://shaxzodbek.com/")
    sleep(3)

    try:
        projects_menu = driver.find_element(By.XPATH, "//a[contains(text(), 'Projects')]")
        driver.execute_script("arguments[0].scrollIntoView();", projects_menu)
        sleep(1)
        projects_menu.click()
        sleep(3)
    except Exception as e:
        print(f"❌ Projects bo'limiga o'tishda xatolik: {e}")
        driver.quit()
        exit()

    all_project_cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'project-card')]")

    fitness_card = None
    for card in all_project_cards:
        title_element = card.find_element(By.XPATH, ".//h3")
        if "Fitness Tracker App" in title_element.text:
            fitness_card = card
            break

    if fitness_card:
        try:
            view_btn = fitness_card.find_element(By.XPATH, ".//a[contains(text(), 'Details')]")
            driver.execute_script("arguments[0].scrollIntoView();", view_btn)
            sleep(1)
            ActionChains(driver).move_to_element(view_btn).click().perform()
            sleep(3)

            # HEADER MA'LUMOTLARI
            header = driver.find_element(By.CLASS_NAME, "project-header")
            title = header.find_element(By.TAG_NAME, "h1").text.strip()
            date = header.find_element(By.CLASS_NAME, "project-date").text.strip()
            badges = [badge.text for badge in header.find_elements(By.CLASS_NAME, "type-badge")]

            # RASM
            try:
                image_url = driver.find_element(By.CLASS_NAME, "project-featured-image").find_element(By.TAG_NAME, "img").get_attribute("src")
            except:
                image_url = ""

            # DESCRIPTION
            desc_div = driver.find_element(By.CLASS_NAME, "project-description")
            description = desc_div.text.strip()

            # TECHNOLOGIYALAR
            tech_elements = driver.find_elements(By.CLASS_NAME, "technology-item")
            technologies = [tech.find_element(By.TAG_NAME, "span").text.strip() for tech in tech_elements]

            # LINKLAR
            links = driver.find_elements(By.XPATH, "//div[@class='project-links']/a")
            project_links = {}
            for link in links:
                text = link.text.strip()
                href = link.get_attribute("href")
                if "GitHub" in text:
                    project_links["github"] = href
                elif "Live Demo" in text:
                    project_links["live_demo"] = href

            # SAVE TO DB
            save_project_to_db(title, date, description, image_url, badges, technologies, project_links)

        except Exception as e:
            print(f"❌ Ma'lumotlarni olishda xatolik: {e}")
    else:
        print("❌ Fitness Tracker App topilmadi.")

except Exception as e:
    print(f"❌ Xatolik yuz berdi: {e}")

finally:
    sleep(2)
    driver.quit()
