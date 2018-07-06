# crawlertest.py
import unittest
import os
import shutil

from crawler import PathFinder

class PathFinderTest(unittest.TestCase):

    def setUp(self):
        self.pf = PathFinder() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    def test_1_evoke_search_type_error(self):
        os.mkdir(os.getcwd()+os.sep+"existing_dir")
        self.assertRaises(ValueError, PathFinder.search_and_find,
                         search_type="anything but 'files' or 'directories'",
                         working_dir=self.pwd,
                         desired_name="existing_dir")
        os.rmdir("existing_dir")

    def test_2_evoke_search_name_error(self):
        os.mkdir(os.getcwd()+os.sep+"existing_dir")
        self.assertRaises(ValueError, PathFinder.search_and_find,
                          search_type="directories",
                          working_dir=self.pwd,
                          desired_name="non_existing_dir")
        os.rmdir("existing_dir")

    def test_3_path_to_subdir(self):
        os.makedirs(os.getcwd()+os.sep+"existing_dir"+os.sep+"existing_subdir")
        subdir_path = PathFinder.path_to_dir(dir_names=["existing_dir",
                                                         "existing_subdir"])
        self.assertTrue(os.path.isdir(subdir_path))
        shutil.rmtree("existing_dir") 

    def test_4_path_to_file(self):
        path = os.getcwd()+os.sep+"existing_dir"+os.sep+"existing_subdir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        file_path = self.pf.path_to_file(dir_names=["existing_dir","existing_subdir"],
                                         file_name="some.file")
        self.assertTrue(os.path.isfile(file_path))
        shutil.rmtree("existing_dir")

    def test_5_evoke_nofiles_in_show_files(self):
        some_dirpath = os.getcwd()+os.sep+"some_dir"
        os.mkdir(some_dirpath)
        x = PathFinder.show_files_with_path(some_dirpath)
        self.assertIs(type(x),str)
        shutil.rmtree("some_dir")

    def test_6_show_files_with_path(self):
        path = os.getcwd()+os.sep+"some_dir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        x = PathFinder.show_files_with_path(os.path.dirname(path))
        self.assertTrue(x["some.file"], path)
        shutil.rmtree("some_dir")

    def test_7_show_files(self):
        path = os.getcwd()+os.sep+"some_dir"+os.sep+"its_subdir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        x = self.pf.show_files(dir_names=["some_dir", "its_subdir"])
        self.assertTrue(x["some.file"], path)
        shutil.rmtree("some_dir")
        
 
if __name__ == '__main__':
    unittest.main()
