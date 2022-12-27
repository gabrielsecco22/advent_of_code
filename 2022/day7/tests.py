from solution import File, Directory, FileSystem


class TestFile:
    def test_file(self):
        file = File("file1", 100)
        assert file.name == "file1"
        assert file.size_bytes == 100
        assert str(file) == "file1"
        assert file.get_size() == 100


class TestDirectory:
    # create fixture for directory tests
    """
    /
        dir1
            file1 - 100
        dir2
            file2 - 200
            dir3
                file3 - 300
                file4 - 400
                dir4
    """

    def setup_method(self):
        self.file1 = File("file1", 100)
        self.file2 = File("file2", 200)
        self.file3 = File("file3", 300)
        self.file4 = File("file4", 400)

        self.dir1 = Directory("dir1", dict(), dict())
        self.dir1.add_file(self.file1)

        self.dir2 = Directory("dir2", dict(), dict())
        self.dir2.add_file(self.file2)

        self.dir3 = Directory("dir3", dict(), dict())
        self.dir3.add_file(self.file3)
        self.dir3.add_file(self.file4)

        self.dir4 = Directory("dir4", dict(), dict())

        self.dir2.add_dir(self.dir3)
        self.dir3.add_dir(self.dir4)

    def test_directory(self):
        assert self.dir1.name == "dir1"
        assert self.dir1.subdirs == {}
        assert str(self.dir1) == "dir1"
        assert self.dir1.get_size() == 100
        assert self.dir1.files == {"file1": self.file1}

        assert self.dir2.name == "dir2"
        assert self.dir2.files == {"file2": self.file2}
        assert self.dir2.subdirs == {"dir3": self.dir3}
        assert str(self.dir2) == "dir2"
        assert self.dir2.get_size() == 900

        assert self.dir3.name == "dir3"
        assert self.dir3.files == {"file3": self.file3, "file4": self.file4}
        assert self.dir3.subdirs == {"dir4": self.dir4}
        assert str(self.dir3) == "dir3"
        assert self.dir3.get_size() == 700

        assert self.dir4.name == "dir4"
        assert self.dir4.files == {}
        assert self.dir4.subdirs == {}
        assert str(self.dir4) == "dir4"
        assert self.dir4.get_size() == 0

        # change file1 size
        self.file1.size_bytes = 1200
        assert self.dir1.get_size() == 1200

        # add file5 to dir4
        file5 = File("file5", 500)
        self.dir4.add_file(file5)
        assert self.dir4.get_size() == 500
        assert self.dir3.get_size() == 1200
        assert self.dir2.get_size() == 1400


class TestFileSystem:
    # create fixture for fileSystem tests
    """
    /
        dir1
            file1 - 100->1200
        dir2
            file2 - 200
            dir3
                file3 - 300
                file4 - 400
                dir4
                    file5 - 500
        dir5
            dir6
        file6 - 600
    """
    def setup_method(self):
        self.file1 = File("file1", 100)
        self.file2 = File("file2", 200)
        self.file3 = File("file3", 300)
        self.file4 = File("file4", 400)

        self.dir1 = Directory("dir1", dict(), dict())
        self.dir1.add_file(self.file1)

        self.dir2 = Directory("dir2", dict(), dict())
        self.dir2.add_file(self.file2)

        self.dir3 = Directory("dir3", dict(), dict())
        self.dir3.add_file(self.file3)
        self.dir3.add_file(self.file4)

        self.dir4 = Directory("dir4", dict(), dict())

        self.dir2.add_dir(self.dir3)
        self.dir3.add_dir(self.dir4)

        self.fs = FileSystem()
        self.fs.add_dir(self.dir1)
        self.fs.add_dir(self.dir2)

    def test_file_system(self):
        assert self.fs.root.name == "/"
        assert self.fs.root.subdirs == {"dir1": self.dir1, "dir2": self.dir2}
        assert self.fs.root.files == {}
        assert str(self.fs.root) == "/"
        assert self.fs.root.get_size() == 1000

        # change file1 size
        self.file1.size_bytes = 1200
        assert self.fs.root.get_size() == 2100

        # add file5 to dir4
        file5 = File("file5", 500)
        self.dir4.add_file(file5)
        assert self.fs.root.get_size() == 2600

        # add dir5 to root
        dir5 = Directory("dir5", dict(), dict())
        self.fs.add_dir(dir5)
        assert self.fs.root.subdirs == {
            "dir1": self.dir1,
            "dir2": self.dir2,
            "dir5": dir5,
        }
        assert self.fs.root.get_size() == 2600

        # add file6 to root
        file6 = File("file6", 600)
        self.fs.add_file(file6)
        assert self.fs.root.files == {"file6": file6}
        assert self.fs.root.get_size() == 3200

        # add dir6 to dir5
        dir6 = Directory("dir6", dict(), dict())

    def test_get_all_dirs(self):
        dir5 = Directory("dir5", dict(), dict())
        self.dir1.add_dir(dir5)
        dirs = self.fs.get_all_dirs()
        assert dirs == [
            self.dir2,
            self.dir3,
            self.dir4,
            self.dir1,
            dir5,
        ]
