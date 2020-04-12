
import logging
import json
import pickle
import os


class GAChecker:
    
    #TODO Constants for NOT DEFINED
    #TODO add logging level in config
    def __init__(self, config_file = "config.json", test_case = "NOT DEFINED"):
        cfg = self.__getConfig(config_file)
        self.hits_file = cfg["hits_file"]
        self.log_file = cfg["log_file"]
        self.pickle_file = cfg["pickle_file"]
        self.tracking_file = cfg["tracking_plan_file"]
        self.set_test_case(test_case)
        self.checklist = []

    def __get_hits_from_file(self, file_name : str, test_case: str) -> dict:
        try:
            with open(file_name, "r") as f:
                content = json.load(f)
                hits = content[test_case]
                f.close()
        except FileNotFoundError:
            logging.warning(
                    "No hits file found. Verify that proxy is started with GALogger addon :" + self.hits_file
                )
        return hits

    def set_test_case(self, test_case :str):
        """update test case and store it to share with GALogger"""
        self.test_case = test_case
        self.__store_test_case(test_case)

    def clear_test_case(self):
        #TODO CONSTANT
        self.test_case = "NOT DEFINED"
        self.__remove_test_case()

    def __store_test_case(self, test_case: str):
        with open(self.pickle_file, "wb") as f :
            pickle.dump(test_case, f )

    def __remove_test_case(self):
        os.remove(self.pickle_file)

    def check_tracking(self) -> list:

        if self.test_case == "NOT DEFINED":
            logging.warning("test case is not defined, use 'GALogger.update_test_case()' to update it'")
        log = self.__get_hits_from_file(self.hits_file, self.test_case)
        tracking = self.__get_hits_from_file(self.tracking_file, self.test_case)

        for m in tracking:
            logging.debug("check tracking: {}".format(m))
            check = False
            for hit in log:
                logging.debug("check hit: {}".format(hit))
                if (m.items() <= hit.items()):
                    check = True
                    logging.debug("hit OK")
                    break
                logging.debug("hit NOK")
            if check:
                logging.debug("check tracking: OK")
            else:
                logging.debug("check tracking: KO")
            self.checklist.append(check)

        logging.debug("results: {}".format(self.checklist))
        return self.checklist


    def __getConfig(self, file: str) -> dict:
        with open(file) as f:
            config = json.load(f)
        return config

