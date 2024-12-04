from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import csv

# Настройки браузера
chrome_options = Options()
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--ignore-ssl-errors")

# Запуск браузера
driver = webdriver.Chrome(options=chrome_options)

try:
    # Открыть Gismeteo
    driver.get("https://www.gismeteo.ru/")
    
    # Ожидание и поиск поля поиска
    search_box = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Поиск местоположения"]'))
    )
    
    # Ввести название города и выбрать его
    city = "Москва"
    search_box.send_keys(city)
    city_option = WebDriverWait(driver, 20).until(
    EC.presence_of_element_located((By.XPATH, f'//a[contains(@class, "search-item") and contains(text(), "{city}")]'))
)
    city_option.click()

    # Добавляем небольшую задержку, чтобы страница успела загрузиться
    time.sleep(5)

    # Ожидание загрузки данных о погоде
    WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "weather"))
    )

    # Извлечение данных о текущей погоде
    date_now = driver.find_element(By.XPATH, '//div[@class="date date-Invalid Date"]').text
    time_now = driver.find_element(By.XPATH, '//div[@class="day" and @data-pattern="G:i"]').text
    temperature_now = driver.find_element(By.XPATH, '//temperature-value[@value]').text
    feel_temperature_now = driver.find_element(By.XPATH, '//div[@class="weather-feel"]//temperature-value').text

    # Извлечение данных о погоде на сегодня
    date_today = driver.find_element(By.XPATH, '//div[@class="date date-3"]').text
    temp_today_min = driver.find_element(By.XPATH, '//temperature-value[@from-unit="c" and @value="-1"]').text
    temp_today_max = driver.find_element(By.XPATH, '//temperature-value[@from-unit="c" and @value="1"]').text

    # Извлечение данных о погоде на завтра
    date_tomorrow = driver.find_element(By.XPATH, '//div[@class="date date-4"]').text
    temp_tomorrow_min = driver.find_element(By.XPATH, '//temperature-value[@from-unit="c" and @value="-4"]').text
    temp_tomorrow_max = driver.find_element(By.XPATH, '//temperature-value[@from-unit="c" and @value="-2"]').text

    # Вывод данных
    print(f"Текущая погода: {date_now} {time_now}")
    print(f"Температура: {temperature_now}°C, по ощущениям: {feel_temperature_now}°C")
    
    print(f"Погода на сегодня: {date_today}")
    print(f"Температура от: {temp_today_min}°C, до: {temp_today_max}°C")
    
    print(f"Погода на завтра: {date_tomorrow}")
    print(f"Температура от: {temp_tomorrow_min}°C, до: {temp_tomorrow_max}°C")

finally:
    driver.quit()

data = [
    ["Текущая погода", date_now, time_now, temperature_now, feel_temperature_now],
    ["Погода на сегодня", date_today, temp_today_min, temp_today_max],
    ["Погода на завтра", date_tomorrow, temp_tomorrow_min, temp_tomorrow_max]
]

with open('weather_data.csv', mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Описание", "Дата", "Время", "Температура", "Температура по ощущениям"])
    writer.writerows(data)
