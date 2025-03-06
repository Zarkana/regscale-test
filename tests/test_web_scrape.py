import pytest
from selenium import webdriver
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
    # Go to regscale.com
    driver.get("https://regscale.com")
    # Dismiss cookies modal
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "hs-eu-confirmation-button"))
    )
    driver.find_element(By.ID, "hs-eu-confirmation-button").click()
    # Navigate to Catalogs and Profiles
    primary_menu = driver.find_element(By.ID, "primary-menu")
    hover = ActionChains(driver).move_to_element(primary_menu)
    hover.perform()
    driver.find_element(By.XPATH, "//*[text()='Catalogs and Profiles']").click()
    # Dismiss cookies modal
    WebDriverWait(driver, 5).until(
        expected_conditions.presence_of_element_located((By.ID, "hs-eu-confirmation-button"))
    )
    driver.find_element(By.ID, "hs-eu-confirmation-button").click()

    # Act

    if category_type == "catalogs":
        driver.find_element(By.ID, "type-catalogs").click()
    elif category_type == "profiles":
        driver.find_element(By.ID, "type-profiles").click()
    elif category_type == "other":
        driver.find_element(By.ID, "type-other").click()

    pagination_number_elements = driver.find_elements(By.CLASS_NAME, "page-btn")
    catalog_cards = []

    for pagination_number_element in pagination_number_elements:
        pagination_number_element.click()

        catalog_card_elements = driver.find_elements(By.CLASS_NAME, "catalog-card")
        catalog_cards + list(map(lambda cat_card: CatalogCard(driver, cat_card), catalog_card_elements))

    # Assert

    for catalog_card in catalog_cards:
        type_text = catalog_card.get_type()
        title_text = catalog_card.get_title()
        print(type_text)
        print(title_text)
        assert isinstance(type_text, str)
        assert isinstance(title_text, str)
