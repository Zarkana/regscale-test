import pytest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from tests.page_objects.catalog_card import CatalogCard

@pytest.fixture
def driver():
    driver = webdriver.Chrome()
    yield driver  # Provides the driver instance to the test
    driver.quit()  # Runs after the test is done

@pytest.mark.parametrize("category_type", [
        "catalogs",
        "profiles",
        "other",
    ]
)
def test_web_scrape(driver, category_type):

    # Arrange

    driver.set_window_size(1920, 1080)
    driver.get("https://regscale.com")
    # Dismiss cookies modal
    WebDriverWait(driver, 10).until(
        expected_conditions.element_to_be_clickable((By.ID, "hs-eu-confirmation-button"))
    ).click()
    # Navigate to Catalogs and Profiles
    primary_menu = driver.find_element(By.ID, "primary-menu")
    hover = ActionChains(driver).move_to_element(primary_menu)
    hover.perform()
    driver.find_element(By.LINK_TEXT, 'Catalogs and Profiles').click()

    # Act

    if category_type == "catalogs":
        driver.find_element(By.ID, "type-catalogs").click()
    elif category_type == "profiles":
        driver.find_element(By.ID, "type-profiles").click()
    elif category_type == "other":
        driver.find_element(By.ID, "type-other").click()

    catalog_cards = []
    for _ in range(get_last_page_number(driver)):
        catalog_card_elements = driver.find_elements(By.CLASS_NAME, "catalog-card")
        catalog_cards = catalog_cards + list(map(lambda cat_card: CatalogCard(driver, cat_card), catalog_card_elements))
        try:
            next_button = driver.find_element(By.CLASS_NAME, "next-btn")
            ActionChains(driver).move_to_element(next_button).click().perform()
        except NoSuchElementException:
            break

    # Assert

    for catalog_card in catalog_cards:
        type_text = catalog_card.get_type()
        title_text = catalog_card.get_title()
        print(type_text)
        print(title_text)
        assert isinstance(type_text, str) and type_text != ""
        assert isinstance(title_text, str) and title_text != ""

def get_last_page_number(driver) -> int:
    page_number_elements = driver.find_elements(By.CSS_SELECTOR, ".page-btn")
    last_index = len(page_number_elements) - 1
    return int(page_number_elements[last_index].text)
