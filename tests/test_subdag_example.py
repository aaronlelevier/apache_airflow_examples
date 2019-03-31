import unittest
from apache_airflow_examples import subdag_example



class SubdagExampleTests(unittest.TestCase):

    def setUp(self):
        self.non_existing_file = '/tmp/wat'
        self.existing_file = __file__

    def test_filename_if_exists(self):
        ret = subdag_example.filename_if_exists(self.existing_file)

        assert ret == 'test_subdag_example'

    def test_filename_if_exists__false__returns_nothing(self):
        ret = subdag_example.filename_if_exists(
            self.non_existing_file)

        assert ret == 'NOTHING'

    def test_bool_if_file_exists(self):
        ret = subdag_example.bool_if_file_exists(self.existing_file)
        assert ret == True

    def test_bool_if_file_exists__false(self):
        ret = subdag_example.bool_if_file_exists(self.non_existing_file)
        assert ret == False
