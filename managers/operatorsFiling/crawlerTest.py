# ../managers/operatorsFiling/crawlertest.py
import unittest
import os
import shutil

from crawler import Crawler as cr

class CrawlerTest(unittest.TestCase):

    def setUp(self):
        #self.cr = Crawler() #instance for non: static & class methods.
        self.pwd = os.getcwd()

    #@unittest.skip("reason for skipping")
    def test_1_list_dirs_invalid_searchpath(self):
        invalid_path = self.pwd+os.sep+"nonexisting_dir" 
        self.assertRaises(ValueError, cr.list_dirs,
                          search_path=invalid_path)

    #@unittest.skip("reason for skipping")
    def test_2_list_dirs_no_subdirs(self):
        valid_path = self.pwd+os.sep+"existing_dir"
        os.mkdir(valid_path)
        self.assertEqual(cr.list_dirs(search_path=valid_path), [])
        os.rmdir("existing_dir")

    #@unittest.skip("reason for skipping")
    def test_3_list_dirs(self):
        valid_path = self.pwd+os.sep+"existing_dir"
        for i in range(3):
            os.makedirs(valid_path+os.sep+"subdir"+str(i+1))
        self.assertEqual(len(cr.list_dirs(search_path=valid_path)), 3)
        shutil.rmtree("existing_dir")
 
    #@unittest.skip("reason for skipping")
    def test_4_evoke_search_type_error(self):
        os.mkdir(os.getcwd()+os.sep+"existing_dir")
        self.assertRaises(ValueError, cr.search_and_find,
                         search_type="anything but 'files' or 'directories'",
                         working_dir=self.pwd,
                         desired_name="existing_dir")
        os.rmdir("existing_dir")

    #@unittest.skip("reason for skipping")
    def test_5_evoke_search_name_error(self):
        os.mkdir(os.getcwd()+os.sep+"existing_dir")
        self.assertRaises(ValueError, cr.search_and_find,
                          search_type="directories",
                          working_dir=self.pwd,
                          desired_name="non_existing_dir")
        os.rmdir("existing_dir")

    #@unittest.skip("reason for skipping")
    def test_6_path_to_subdir(self):
        os.makedirs(os.getcwd()+os.sep+"existing_dir"+os.sep+"existing_subdir")
        subdir_path = cr.path_to_dir(dir_names=["existing_dir",
                                                "existing_subdir"])
        self.assertTrue(os.path.isdir(subdir_path))
        shutil.rmtree("existing_dir") 

    #@unittest.skip("reason for skipping")
    def test_7_path_to_file(self):
        path = os.getcwd()+os.sep+"existing_dir"+os.sep+"existing_subdir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        file_path = cr.path_to_file(dir_names=["existing_dir","existing_subdir"],
                                         file_name="some.file")
        self.assertTrue(os.path.isfile(file_path))
        shutil.rmtree("existing_dir")

    #@unittest.skip("reason for skipping")
    def test_8_evoke_nofiles_in_show_files(self):
        some_dirpath = os.getcwd()+os.sep+"some_dir"
        os.mkdir(some_dirpath)
        x = cr.show_files_with_path(some_dirpath)
        self.assertIs(type(x),str)
        shutil.rmtree("some_dir")

    #@unittest.skip("reason for skipping")
    def test_9_show_files_with_path(self):
        path = os.getcwd()+os.sep+"some_dir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        x = cr.show_files_with_path(os.path.dirname(path))
        #print(x)
        self.assertTrue(x["some.file"], path)
        shutil.rmtree("some_dir")

    #@unittest.skip("reason for skipping")
    def test_10_show_files(self):
        path = os.getcwd()+os.sep+"some_dir"+os.sep+"its_subdir"+os.sep+"some.file"
        os.makedirs(os.path.dirname(path))
        with open(path, 'w') as temp_file:
            temp_file.write("blah blah blah")
        x = cr.show_files(dir_names=["some_dir", "its_subdir"])
        #print(x)
        self.assertTrue(x["some.file"], path)
        shutil.rmtree("some_dir")
        
 
if __name__ == '__main__':
    unittest.main()
