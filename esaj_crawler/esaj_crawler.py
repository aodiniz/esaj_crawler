import argparse
import json
import os


supported_crawling_modes = {
    "esaj_data": "",
    "esaj_metadata": ""
}

class esajCrawler():

    root_path = os.path.abspath(os.path.dirname(__file__))

    def __init__(self) -> None:
        self.supported_courts = os.listdir(os.path.join(self.root_path, "config"))

        self.data_folder_path = os.path.join(os.path.abspath(os.path.dirname(self.root_path)), "data")
        os.makedirs(self.data_folder_path, True)

    def __init__(self, **args) -> None:
        self.__init__()

        self.output_json_path = os.path.join(self.data_folder_path, f"args['justice_court'].json")
        self.set_output_json_obj()

        self.set_search_criteria(**args)

    def get_supported_courts(self):
        return self.supported_courts

    def get_output_json_obj(self):
        return self.output_json_obj

    def set_output_json_obj(self):
        try:
            self.output_json_obj = json.load(self.output_json_path)
        except:
            self.output_json_obj = dict()


    def set_search_criteria(self, **args):
        if "search" in args:
            pass
    
    def run(self):
        pass


if __name__ == "__main__":

    ec = esajCrawler()

    parser = argparse.ArgumentParser(description="e-SAJ Crawler")

    parser.add_argument("-jc", "--justice_court", action="store", type=str,
                        choices=ec.get_supported_courts(),
                        help="Justice Court for the crawling process.")
    parser.add_argument("-cm", "--crawling_mode", action="store", type=str,
                        default="esaj_data",
                        choices=supported_crawling_modes.keys(),
                        help="Justice Court for the crawling process.")
    parser.add_argument("-sc", "--search_criteria", action="store", type=str,
                        help="Filters for crawling in JSON format.")
    parser.add_argument("-dp", "--download_pdf", action="store_true",
                        help="Flag to download PDF file(s) for each entry, if available.")
    parser.add_argument("-sp", "--sequential_processing", action="store_true",
                        help="Flag to set the crawling to be performed sequentially, instead of parallelly.")

    parsed_args = parser.parse_args()
