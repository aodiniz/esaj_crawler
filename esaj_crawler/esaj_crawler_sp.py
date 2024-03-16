import argparse

from esaj_crawler import esajCrawler

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import ElementNotVisibleException, ElementNotSelectableException

class esajCrawlerSP(esajCrawler):

    _justice_court = "sp"

    def __init__(self, **args):
        print(args)
        super().__init__(**args)
        print(self.__dict__)


    def clear_search_fields(self):
        level_1_class_name = "secaoFormBody"
        level_2_tag_name = "img"
        level_3_property_src = self.get_esaj_url(url_suffix="imagens/spw/botLimpar.gif")

        clear_buttons = [i
            for i in self._driver.find_elements(
                By.CLASS_NAME, level_1_class_name
            )[1].find_elements(
                By.TAG_NAME, level_2_tag_name
            ) if i.get_property("src") == level_3_property_src
        ]

        for b in clear_buttons:
            b.click()


    def set_search_fields(self):
        for k, v in self._search_criteria.items():
            input_text_search_criteria = self._driver.find_element(By.ID, self._search_criteria_key_json_obj[k])
            input_text_search_criteria.send_keys(v)


    def crawling(self, **args):
        if args.get("crawling_mode") == "esaj_data":
            self.clear_search_fields()
            self.set_search_fields()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="e-SAJ Crawler (Justice Court of São Paulo)")

    parser.add_argument("-cm", "--crawling_mode", action="store", type=str,
                        default="esaj_data",
                        choices=esajCrawlerSP._supported_crawling_modes.keys(),
                        help="Justice Court for the crawling process.")
    parser.add_argument("-sc", "--search_criteria", action="store", type=str, required=False,
                        help="Filters for crawling in JSON format.")
    parser.add_argument("-dp", "--download_pdf", action="store_true",
                        help="Flag to download PDF file(s) for each entry, if available.")
    parser.add_argument("-sp", "--sequential_processing", action="store_true",
                        help="Flag to set the crawling to be performed sequentially, instead of parallelly.")

    parsed_args = parser.parse_args()

    ec = esajCrawlerSP(**vars(parsed_args))

