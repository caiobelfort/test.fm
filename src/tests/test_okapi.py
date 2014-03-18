"""
Nosetest package for the okapi connector class. This test implies that you have access to the okapi server or something
"""

__author__ = 'joaonrb'

from testfm.okapi.connector import RandomOkapi, OkapiNoResultError
import testfm
import pandas as pd
from pkg_resources import resource_filename


class TestRandomOkapi(object):
    """
    Test for okapi connector
    """

    def setUp(self):
        self.df = pd.read_csv(resource_filename(testfm.__name__, 'data/movielenshead.dat'), sep="::", header=None,
                              names=['user', 'item', 'rating', 'date', 'title'])
        self.random_okapi = RandomOkapi()

    def test_get_result(self):
        """
        Test if result exist behavior and get result.
        """
        result_file = self.random_okapi.get_result_location(self.df)
        if self.random_okapi.result_exist_for(result_file):
            user, item = self.random_okapi.result
            assert isinstance(user, pd.DataFrame), "First element in tuple is not a pandas DataFrame"
            assert isinstance(item, pd.DataFrame), "Second element in tuple is not a pandas DataFrame"
        else:
            try:
                result = self.random_okapi.result
            except OkapiNoResultError:
                pass
            else:
                assert False, "RandomOkapi.result is returning %s when RandomOkapi.result_exist_for is false" % result

    def test_map(self):
        """
        Test the mapping
        """
        self.random_okapi.map_data(self.df)
        users = enumerate(set(self.df["user"]))
        items = enumerate(set(self.df["item"]))
        for user_id, user in users:
            assert self.random_okapi.data_map["user_to_id"] == user_id, "Mapping in user to id is not correct"
            assert self.random_okapi.data_map["id_to_user"][user_id] == user, "Mapping in id user is not correct"

        for item_id, item in items:
            assert self.random_okapi.data_map["item_to_id"][item] == item_id, "Mapping in item to id is not correct"
            assert self.random_okapi.data_map["id_to_item"][item_id] == item, "Mapping in id item is not correct"
