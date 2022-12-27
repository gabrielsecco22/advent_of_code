"""
$ cd /
$ ls
dir dpbwg
dir dvwfscw
dir hccpl
dir jsgbg
dir lhjmzsl
"""


class File:
    def __init__(self, name, size_bytes):
        self.name = name
        self.size_bytes = size_bytes

    def __str__(self):
        return self.name

    def get_size(self):
        return self.size_bytes


class Directory:
    def __init__(self, name, files: dict, subdirs: dict, parent=None):
        self.name = name
        self.files = files
        self.subdirs = subdirs
        self.parent = parent

    def __str__(self):
        return self.name

    def __repr__(self):
        return f"{self.name}"

    def add_dir(self, dir):
        self.subdirs[str(dir)] = dir

    def add_file(self, file):
        self.files[str(file)] = file

    def get_size(self):
        size = 0
        for file in self.files.values():
            size += file.get_size()
        for subdir in self.subdirs.values():
            size += subdir.get_size()
        return size


class FileSystem:
    def __init__(self):
        self.root = Directory("/", dict(), dict())
        self.current_dir = self.root

    def add_file(self, file: File):
        self.current_dir.files[str(file)] = file

    def add_dir(self, directory: Directory):
        directory.parent = self.current_dir
        self.current_dir.subdirs[str(directory)] = directory

    def cd(self, path: str):
        """
            Changes the current directory to the given path.
            The path is absolute and starts with /.
            The path is a directory.
            The path is a valid path.
        """
        if path == "/":
            self.current_dir = self.root
            return
        if path == "..":
            self.current_dir = self.current_dir.parent
            return
        if path[0] == "/":
            self.current_dir = self.root
            path = path[1:]
        dirs = path.split("/")
        c_dir = self.current_dir
        for name in dirs:
            c_dir = c_dir.subdirs[name]
        self.current_dir = c_dir

    def read_ls(self, outputs: list):
        for o in outputs:
            if o.startswith("dir "):
                dir_name = o[4:]
                self.add_dir(Directory(dir_name, dict(), dict(), self.current_dir))
            else:
                size, file_name = o.split(" ")
                self.add_file(File(file_name, int(size)))

    def get_size(self):
        return self.root.get_size()

    def get_all_dirs(self):
        """
            Returns a list of all directories in the file system.
            The list should be ordered as the inverse of the depth-first search(append behavior).
        """
        subdir_stack = list()
        subdir_stack.append(self.root)
        dirs = []
        while subdir_stack:
            dir = subdir_stack.pop()
            dirs.append(dir)
            subdir_stack += dir.subdirs.values()
        return dirs



def read(filename):
    lines = open(filename).read().splitlines()
    return lines


def build_fs(commands, params, outputs):
    fs = FileSystem()
    for cmd, param, output in zip(commands, params, outputs):
        if cmd == "ls":
            fs.read_ls(output)
        elif cmd == "cd":
            fs.cd(param)
    return fs




def read_commands(lines):
    # commands starts with $
    cmd_list, param_list, res_list = [], [], []
    curr_line = 0
    while curr_line < len(lines):
        if curr_line == 1077:
            print("here")
        if lines[curr_line].startswith("$"):
            res = []
            cmd_line = lines[curr_line][2:]
            if cmd_line.startswith("cd"):
                cmd, param = cmd_line.split(" ")
            else:
                cmd, param = cmd_line, ""
            cmd_list.append(cmd)
            param_list.append(param)
            for line in lines[curr_line + 1:]:
                if line.startswith("$") or curr_line == len(lines) - 2:
                    res_list.append(res)
                    break
                else:
                    res.append(line)
            curr_line += len(res) + 1
        else:
            curr_line += 1
    return cmd_list, param_list, res_list


# def solution1(lines):


if __name__ == "__main__":
    lines = read("input.txt")
    cmds, params, res = read_commands(lines)
    print(cmds)
    print(params)
    print(res)
    fs = build_fs(cmds, params, res)
    print(fs.get_size())
    dirs = [(x, x.get_size()) for x in fs.get_all_dirs()]
    # order by size
    dirs.sort(key=lambda x: x[1], reverse=True)
    print(dirs[0])
    # get all dirs with total size of at most 100000
    dirs = [x for x in dirs if x[1] <= 100000]
    # sum of all dirs
    print(sum([x[1] for x in dirs])) # part 1

    required_space = fs.get_size() - 40000000
    print(required_space)

    # get the first dir that has a size greater than the required space
    dirs = [(x, x.get_size()) for x in fs.get_all_dirs()]
    dirs.sort(key=lambda x: x[1], reverse=True)
    dirs = [x for x in dirs if x[1] >= required_space]
    print(dirs[-1])
