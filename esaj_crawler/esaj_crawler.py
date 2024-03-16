import os
import json
import utils as u

from abc import ABC, abstractmethod
from concurrent.futures import ThreadPoolExecutor, as_completed
from pprint import pformat
from selenium import webdriver


class esajCrawler(ABC):

    _justice_court = None
    _root_path = os.path.abspath(os.path.dirname(__file__))
    _supported_crawling_modes = {
        "esaj_data": "",
        "esaj_metadata": ""
    }


    def __init__(self, **args) -> None:
        self._config_folder_path = os.path.join(self._root_path, "config")
        self._supported_courts = [i for i in os.listdir(self._config_folder_path) if os.path.isdir(os.path.join(self._config_folder_path, i))]
        assert self._justice_court in self._supported_courts, f"Justice Court '{self._justice_court}' is not supported."

        self._data_folder_path = os.path.join(os.path.abspath(os.path.dirname(self._root_path)), "data")
        self._data_justice_court_folder_path = os.path.join(self._data_folder_path, self._justice_court)
        os.makedirs(self._data_justice_court_folder_path, exist_ok=True)

        self._cases_json_obj = None
        self._cases_json_path = os.path.join(self._data_justice_court_folder_path, "cases.json")
        self.__set_cases_json_obj()

        self._config_common_json_obj = u.json_load(os.path.join(
            self._config_folder_path,
            "common.json"
        ))

        self._config_justice_court_base_json_obj = u.json_load(os.path.join(
            self._config_folder_path,
            self._justice_court,
            "base.json"
        ))

        self._search_criteria_key_json_obj = u.json_load(os.path.join(
            self._config_folder_path,
            self._justice_court,
            "search_criteria_key.json"
        ))

        self._search_criteria = None
        if args.get("search_criteria"):
            self.__set_search_criteria(args.get("search_criteria"))

        self._profile = None
        if args.get("download_pdf"):
            self.__set_firefox_profile()

        if self._profile:
            self._driver = webdriver.Firefox(self._profile)
        else:
            self._driver = webdriver.Firefox()


    def __set_cases_json_obj(self):
        try:
            self._cases_json_obj = u.json_load(self._cases_json_path)
        except:
            self._cases_json_obj = list()


    def __set_search_criteria(self, search_criteria_str):
        try:
            search_criteria = json.loads(search_criteria_str)
        except:
            # Accept search criteria formated as [criteria #A]>[value #A1]|[criteria #A]>[value #A2];[criteria #B]>[value #B1]
            search_criteria = [
                {
                    i.split(">")[0]: i.split(">")[-1] for i in sc.split(";")
                } for sc in search_criteria_str.split("|")
            ]

        non_recognized_search_criteria = dict(
            filter(
                lambda t: t[1],
                {
                    i: [
                        k for k in sc if k not in self._search_criteria_key_json_obj
                    ] for i,sc in enumerate(search_criteria)
                }.items()
            )
        )

        if non_recognized_search_criteria:
            raise ValueError(f"Non recognized Search Criteria:\n{pformat(non_recognized_search_criteria)}")

        self._search_criteria = search_criteria


    def __set_firefox_profile(self):
        self._profile = webdriver.FirefoxProfile()

        for k, v in self._config_common_json_obj["profile"]["firefox"].items():
            self._profile.set_preference(k, v)

        self._profile.set_preference("browser.download.dir", self._data_justice_court_folder_path)


    def get_supported_courts(self):
        return self._supported_courts


    def get_entry_json_obj(self):
        return self._entry_json_obj


    def get_esaj_url(self, url_suffix=""):
        return self._config_justice_court_base_json_obj["esaj_url"] + url_suffix


    def run(self, **args):
        if args.get("crawling_mode") == "esaj_data":
            if args.get("sequential_processing"):
                for search_criteria in args["search_criteria"]:
                    procs = {**procs, **self.crawling(search_criteria, **args)}
                    u.json_dump(self._cases_json_path, self._cases_json_obj)
            else:
                crawling_exec = ThreadPoolExecutor(max_workers=max(1, self._config_common_json_obj["num_workers"]))
                crawling_inst = list()

                for search_criteria in args["search_criteria"]:
                    crawling_inst.append(crawling_exec.submit(self.crawling, search_criteria, args))

                for si in as_completed(crawling_inst):
                    procs = {**procs, **si.result()}
                    u.json_dump(self._cases_json_path, self._cases_json_obj)


    @abstractmethod
    def crawling(self, search_criteria, **args):
        pass
