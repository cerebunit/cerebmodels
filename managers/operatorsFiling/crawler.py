import os

class PathFinder(object):
    """Operator working under FileManager.

    Available methods:
    path_to_dir -- returns path to a desired directory or subdirectory
    path_to_file -- returns path to a desired file in given directory path
    show_files -- returns dictionary of filenames and its path

    """

    @staticmethod
    def search_and_find(search_type=None, working_dir=None, desired_name=None):
        """staticmethod that searches for and finds files or directories.

        Keyword arguments:
        search_type -- valid strings; "files" or "directories"
        working_dir -- path string; "current/working/directory"
        desired_name -- string or list of strings;
                        strings for "file.name" or "a_directory_name";
                        list of strings for ["a_dir_name", "its_subdir"]

        Returned value:
        full path (os specific) to the directory/subdirectory/file

        Raised Exceptions:
        ValueError if search_type is anything else other than "files" or "directories"
        ValueError if directory or file does not exist.

        Use case:
        present_dirpath = "/path/to/current/working/directory"
        ###### To search for a subdirectory ######
        search_for = ["a_dir_name", "its_subdir"]
        search_and_find(search_type="directories",
                        working_dir=present_dirpath,
                        desired_name=search_for)
        ###### To search for a directory ######
        search_for = "a_dir_name"
        search_and_find(search_type="directories",
                        working_dir=present_dirpath,
                        desired_name=search_for)
        ###### To search for a file ####
        search_for = "filename.ext"
        search_and_find(search_type="files",
                        working_dir=present_dirpath,
                        desired_name=search_for)

        """
        for (dirpath, dirnames, filenames) in os.walk(working_dir):
            if search_type=="directories":
                choice = dirnames
            elif search_type=="files":
                choice = filenames
            else:
                raise ValueError("search_type value must be files or directories")
            for name in choice:
                if name==desired_name:
                    return dirpath + os.sep + name
                else:
                    raise ValueError("Given directory/file name does not exist")

    @classmethod
    def path_to_dir(cls, dir_names=None):
        """classmethod that returns path to a desired directory or subdirectory.

        Keyword arguments:
        dir_name -- string or list of strings;
                    strings for just "a_directory_name";
                    list of strings for ["a_dir_name", "its_subdir"]

        Returned value:
        full path (os specific) to the directory/subdirectory

        Note:
        If only one directory name is given it is assumed this is available in
        the current working path (where this method is called from).
        This also applies to the first directory in the list of directory names.

        Use case:
        ###### Path to a directory in current working path ######
        path_to_dir(dir_names="a_dir_name")
        ###### Path to a subdirectory within the directory in current working path ######
        path_to_dir(dir_names=["a_dir_name", "its_subdir"])

        """

        if type(dir_names) is str:
            return  cls.search_and_find(search_type="directories",
                                        working_dir=os.getcwd(),
                                        desired_name=dir_names)
        elif type(dir_names) is list:
            for i, name in enumerate(dir_names):
               if i==0:
                   nthpath = cls.path_to_dir(name)
               else:
                   nthpath = cls.search_and_find(search_type="directories",
                                                 working_dir=nthpath,
                                                 desired_name=name)
            return nthpath

    def path_to_file(self, dir_names=None, file_name=None):
        """instantiated method that returns path to a desired file.

        Keyword arguments:
        dir_name -- string or strings list, where file is thought to reside.
                    strings for just "a_directory_name";
                    list of strings for ["a_dir_name", "its_subdir"]
        file_name -- string; "filename.ext"

        Returned value:
        full path (os specific) to the filename

        Note:
        If only one directory name is given it is assumed this is available in
        the current working path (where this method is called from).
        This also applies to the first directory in the list of directory names.

        Use case:
        ###### Path to a file in current working path ######
        path_to_file(dir_names="a_dir_name", file_name="filename.ext")
        ###### Path to a file in subdirectory within the directory in current working path ######
        path_to_file(dir_names=["a_dir_name", "its_subdir"], file_name="filename.ext")

        """
        dir_path = self.path_to_dir(dir_names)
        file_path = self.search_and_find(search_type="files",
                                         working_dir=dir_path,
                                         desired_name=file_name)
        return file_path

    @staticmethod
    def show_files_with_path(path_to_current_working_directory):
        """staticmethod that searches for all available files within scope

        Argument:
        path_to_current_working_directory -- path string; "current/working/directory"

        Returned value:
        dictionary as {"file1.ext": "its/path/file1.ext", "file2.ext": "a/path/file2.ext"}

        Raised Exceptions:
        if dictionary is empty, returns "There are no files in the current path."

        Use case:
        present_dirpath = "/path/to/current/working/directory"
        ###### To show all the files in current working directory ######
        show_files_with_path(os.getcwd())
        ###### To show all the files in a desired directory ######
        dirpath = "path/to/desired/directory"
        show_files_with_path(dirpath)
        """
        x = {}
        for (dirpath, dirnames, filenames) in os.walk(path_to_current_working_directory):
            for afilename in filenames:
                y = {afilename: dirpath+afilename}
                x.update(y)
        if not x:
            x = "There are no files in the current path."
            print(x)
            return x
        else:
            return x

    def show_files(self, dir_names=None):
        """instantiated method that returns all the available files and its respective path.

        Keyword arguments:
        dir_name -- string or strings list, where file is thought to reside.
                    strings for just "a_directory_name";
                    list of strings for ["a_dir_name", "its_subdir"]

        Returned value:
        dictionary with keys <- filenames and its path in respective value.

        Note:
        If NO directory name is given it will find files in all the directory and subdirectory.
        If only one directory name is given it is assumed this is available in
        the current working path (where this method is called from).
        This also applies to the first directory in the list of directory names.

        Use case:
        ###### For files in current working path ######
        show_files()
        ###### For files in a subdirectory within the directory in current working path ######
        show_files(dir_names=["a_dir_name", "its_subdir"])

        """
        if dir_names is None:
            return self.show_files_with_path(os.getcwd())
        else:
            dir_path = self.path_to_dir(dir_names)
            return self.show_files_with_path(dir_path)
