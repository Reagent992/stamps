from time import sleep


class Scrolls:
    def __init__(self, driver, action):
        self.driver = driver
        self.action = action

    def scroll_by(self, x, y):
        self.driver.execute_script(f"window.scrollTo({x}, {y})")

    def scroll_to_bottom(self):
        self.driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight)"
        )

    def scroll_to_bottom_with_sleep(self, sleep_time=0.3) -> None:
        last_height = 0
        while True:
            self.driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            sleep(sleep_time)
            # Define new page height
            new_height = self.driver.execute_script(
                "return document.body.scrollHeight"
            )
            # If the height has not changed,
            # then the end of the page has been reached
            if new_height == last_height:
                break
            last_height = new_height

    def scroll_to_top(self):
        self.driver.execute_script("window.scrollTo(0, 0)")

    def scroll_to_element(self, element):
        self.action.scroll_to_element(element).perform()
        self.driver.execute_script(
            """
        window.scrollTo({
            top: window.scrollY + 700,
        });
        """
        )
