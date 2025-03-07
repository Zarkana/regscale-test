from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement

class CatalogCard:

    def __init__(self, driver: WebDriver, catalog_card: WebElement):
        self.driver: WebDriver = driver
        self.card = catalog_card
        self.type_text = catalog_card.find_element(By.CLASS_NAME, "topics").text
        self.name_text = catalog_card.find_element(By.CLASS_NAME, "title").text

    def get_type(self) -> str:
        return self.type_text

    def get_title(self) -> str:
        return self.name_text
