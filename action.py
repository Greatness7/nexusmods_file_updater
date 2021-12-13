import os
import re
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait


class Action:
    username: str
    password: str
    game_domain_name: str
    mod_id: str
    file_name: str
    file_version: str
    update_version: bool
    file_category: str
    new_existing_version: bool
    original_file: str
    remove_old_version: bool
    file_description: str
    remove_nmm_button: bool
    set_as_main_nmm: bool
    requirements_pop_up: bool
    file_path: str

    def __init__(self):
        """Initialize and validate input parameters passed via env variables."""
        self.username = os.environ["USERNAME"]
        self.password = os.environ["PASSWORD"]
        self.game_domain_name = os.environ["GAME_DOMAIN_NAME"]
        self.mod_id = os.environ["MOD_ID"]
        self.file_name = os.environ["FILE_NAME"]
        self.file_version = os.environ["FILE_VERSION"]
        self.update_version = os.environ["UPDATE_VERSION"]
        self.file_category = os.environ["FILE_CATEGORY"]
        self.new_existing_version = os.environ["NEW_EXISTING_VERSION"]
        self.original_file = os.environ["ORIGINAL_FILE"]
        self.remove_old_version = os.environ["REMOVE_OLD_VERSION"]
        self.file_description = os.environ["FILE_DESCRIPTION"]
        self.remove_nmm_button = os.environ["REMOVE_NMM_BUTTON"]
        self.set_as_main_nmm = os.environ["SET_AS_MAIN_NMM"]
        self.requirements_pop_up = os.environ["REQUIREMENTS_POP_UP"]
        self.file_path = os.environ["FILE_PATH"]

        # ensure required inputs are not empty
        assert self.username, "username must not be empty"
        assert self.password, "password must not be empty"
        assert self.game_domain_name, "game_domain_name must not be empty"
        assert self.mod_id, "mod_id must not be empty"
        assert self.file_name, "file_name must not be empty"
        assert self.file_version, "file_version must not be empty"
        assert self.file_description, "file_description must not be empty"
        assert self.file_path, "file_path must not be empty"

        # ensure it's a valid file category
        assert self.file_category in ("Main Files",
                                      "Updates",
                                      "Optional files",
                                      "Old versions",
                                      "Miscellaneous",
                                      "Archived")

        # ensure description is not too long
        assert len(self.file_description) <= 255

        # ensure the file path actually exists
        assert os.path.isfile(self.file_path)

        # ensure file path has valid extension
        _, extension = os.path.splitext(self.file_path)
        assert extension.lower() in (".rar", ".zip", ".7z", ".exe", ".omod")

    def login(self, driver):
        driver.get("https://www.nexusmods.com/users/myaccount")

        login = driver.find_element(By.ID, "login")
        login.click()

        user_login = driver.find_element(By.ID, "user_login")
        user_login.send_keys(self.username)

        password = driver.find_element(By.ID, "password")
        password.send_keys(self.password)

        commit = driver.find_element(By.NAME, "commit")
        commit.click()

        time.sleep(15)  # wait cloudflare timer

        try:
            driver.find_element(By.XPATH, "//*[contains(text(), 'Invalid Login')]")
        except:
            print("Login successful!")
        else:
            raise ValueError("Invalid Login")

    def update(self, driver):
        driver.get(f"https://www.nexusmods.com/{self.game_domain_name}/mods/edit/?id={self.mod_id}&step=files")

        # File Name

        file_name = driver.find_element(By.NAME, "name")
        file_name.send_keys(self.file_name)

        # File Version

        file_version = driver.find_element(By.NAME, "file-version")
        file_version.send_keys(self.file_version)

        if self.update_version:
            update_version = driver.find_element(By.NAME, "update-version")
            update_version.click()

        # File Category

        file_category_container = driver.find_element(By.ID, "select2-select-file-category-container")
        file_category_container.click()

        file_category_options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
        for option in file_category_options:
            if option.text == self.file_category:
                option.click()
                break

        if self.new_existing_version:
            new_existing = driver.find_element(By.NAME, "new-existing")
            new_existing.click()

            original_file_container = driver.find_element(By.ID, "select2-select-original-file-container")
            original_file_container.click()

            original_file_options = driver.find_elements(By.CLASS_NAME, "select2-results__option")
            for option in original_file_options:
                if re.search(self.original_file, option.text):
                    option.click()
                    break
            else:
                raise ValueError("Original file not found!")

            if self.remove_old_version:
                remove_old_version = driver.find_element(By.NAME, "remove-old-version")
                remove_old_version.click()

        # File Description

        file_description = driver.find_element(By.NAME, "brief-overview")
        file_description.send_keys(self.file_description)

        # File Options

        if self.remove_nmm_button:
            remove_nmm_button = driver.find_element(By.NAME, "remove_nmm_button")
            remove_nmm_button.click()

        if self.set_as_main_nmm:
            set_as_main_nmm = driver.find_element(By.NAME, "set_as_main_nmm")
            set_as_main_nmm.click()

        if not self.requirements_pop_up:
            requirements_pop_up = driver.find_element(By.NAME, "requirements_pop_up")
            requirements_pop_up.click()

        # Add File

        browse_file = driver.find_element(By.ID, "add_file_browse")

        file_select = browse_file.find_elements(By.XPATH, ".//*")[0]
        file_select.send_keys(os.path.abspath(self.file_path))

        print("Waiting for upload to finish...")
        WebDriverWait(driver, 1500).until(
            lambda x: x.find_element(By.ID, "upload_success").is_displayed()
        )

        # Save File

        save_file = driver.find_element(By.ID, "js-save-file")
        save_file.click()

        print("Finished!")


if __name__ == "__main__":
    print("Validating input parameters...")
    action = Action()

    print("Configuring webdriver options...")
    opt = webdriver.firefox.options.Options()
    opt.headless = True

    print("Starting webdriver...")
    driver = webdriver.Firefox(options=opt)

    print("Logging in...")
    action.login(driver)

    print("Updating File...")
    action.update(driver)
