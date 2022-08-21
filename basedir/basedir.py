#!/user/local/bin/python3
# -*- coding: utf-8 -*-

import os, shutil

class basedir(object):

    def __init__(self, path='./'):
        if os.path.isdir(path): self._path = path
        else: self._path = None
        self._dirs = []
        self._files = []
        self._read = False
        self.read()

    def read(self):
        self._dirs = []
        self._files = []
        self._read = False
        if not self._path: return
        for name in os.listdir(self._path):
            path = self._path + '/' + name
            if os.path.isdir(path):
                sub = subdir(name,self)
                if sub.path(): self._dirs.append(sub)
            if os.path.isfile(path): self._files.append(path)
        self._read = True

    def basedir(self): return self

    def get_subdir(self, name, make_if_not=False):
        if not self._path: return None
        for dir in self.subdirs():
            if name == dir.name(): return dir
        if make_if_not: return self.make_subdir(name)
        return None

    def make_subdir(self, name):
        sub = self.get_subdir(name,make_if_not=False)
        if sub: return sub
        path = self._path + '/' + name
        if not os.path.isdir(path): os.mkdir(path)
        sub = subdir(name,self)
        self._dirs.append(sub)
        return sub
                
    def level(self): return 0
       
    def path(self): return self._path

    def paths_from_base(self):
        paths = []
        paths.append(self.path())
        return paths

    def name(self): return os.path.basename(self._path)

    def subdirs(self):
        if not self._read: self.read()
        return self._dirs

    def names_subdirs(self):
        names = []
        for dir in self.subdirs(): names.append(dir.name())
        return names

    def subdir_path(self,name):
        sub = self.get_subdir(name)
        if sub: sub.path()
        return None

    def exist_dir(self,subdir):
        if isinstance(subdir, str): return subdir in self.names_subdirs()
        if not isinstance(subdir, (basedir, subdir)):
            for dir in self.subdirs(): return subdir.path() == dir.path()
        return False

    def files(self):
        if not self._read: self.read()
        return self._files

    def names_files(self):
        names = []
        for file in self.files(): names.append(os.path.basename(file))
        return names

    def file_path(self,name):
        for file in self.files():
            if name == os.path.basename(file): return file
        return None

    def file_ext(self,name):
        for file in self.files():
            if name == os.path.basename(file):
                base, ext = os.path.splitext(file)
                return ext
        return None

    def exist_file(self,name): return name in self.names_files()

    def remove_subdir(self, name):
        sub = self.get_subdir(name,make_if_not=False)
        if sub:
            if os.path.isdir(sub.path()): os.rmdir(sub.path())
            self._dirs.remove(sub)

    def remove_file(self, name):
        file_path = self.file_path(name)
        if not file_path: return
        self._files.remove(file_path)
        if os.path.isfile(file_path): os.remove(file_path)

    def copy(self,src,dest=None):
        if isinstance(src,str) and isinstance(dest, (basedir, subdir)): self.copy_to(src,dest)
        self.copy_here(src,dest)

    def copy_here(self,src,name=None):
        if isinstance(src, str): self.copy_file_here(src,name)
        elif isinstance(src, (basedir, subdir)): self.copy_dir_here(src,name)

    def copy_file_here(self,file_path,name=None):
        if not os.path.isfile(file_path): return
        if not name: name = os.path.basename(file_path)
        dest_path = self.path() + '/' + name
        if not self.exist_file(name): self._files.append(dest_path)
        shutil.copyfile(file_path, dest_path)

    def copy_dir_here(self,src_dir,name=None):
        if not isinstance(src_dir, (basedir, subdir)): return
        if not name: name = src_dir.name()
        shutil.copytree(src_dir.path(), self.path() + '/' + name)
        sub = self.get_subdir(name)
        if sub: sub.read()
        else: self.make_subdir(name)

    def copy_to(self,name,dest):
        if self.exist_file(name): self.copy_file_to(name, dest)
        elif self.exist_dir(name): self.copy_dir_to(name, dest)

    def copy_file_to(self, name, dest_dir):
        file_path = self.file_path(name)
        if not file_path: return
        if not isinstance(dest_dir, (basedir, subdir)): return
        dest_dir.copy_file_here(file_path)

    def copy_dir_to(self, name, dest_dir):
        if not isinstance(dest_dir, (basedir, subdir)): return
        sub = self.get_subdir(name)
        if sub: dest_dir.copy_dir_here(sub)

    def move(self,src,dest=None):
        if isinstance(src,str) and isinstance(dest, (basedir, subdir)): self.move_to(src,dest)
        self.move_here(src,dest)

    def move_here(self,src,name=None):
        if isinstance(src, str): self.move_file_here(src,name)
        elif isinstance(src, (basedir, subdir)): self.move_dir_here(src,name)

    def move_file_here(self,file_path, name=None):
        if not os.path.isfile(file_path): return
        if not name: name = os.path.basename(file_path)
        dest_path = self.path() + '/' + name
        if not self.exist_file(name): self._files.append(dest_path)
        shutil.move(file_path,self.path())

    def move_dir_here(self,src_dir, name=None):
        if not isinstance(src_dir, (basedir, subdir)): return
        if not name: name = src_dir.name()
        dest_path = self.path() + '/' + name
        shutil.move(src_dir.path(),dest_path)
        sub = self.get_subdir(name)
        if sub: sub.read()
        else: self.make_subdir(name)
        src_dir.remove_me()

    def move_to(self,name,dest):
        if self.exist_file(name): self.move_file_to(name, dest)
        elif self.exist_dir(name): self.move_dir_to(name, dest)

    def move_file_to(self, name, dest_dir):
        file_path = self.file_path(name)
        if not file_path: return
        if not isinstance(dest_dir, (basedir,subdir)): return
        dest_dir.move_file_here(file_path)
        self.remove_file(name)

    def move_dir_to(self, name, dest_dir):
        if not isinstance(dest_dir, (basedir, subdir)): return
        sub = self.get_subdir(name)
        if sub: dest_dir.move_dir_here(sub)

    def dprint(self):
        print('----------------')
        print('PATH:[' + self.path() + '] NAME:[' + self.name() + '] LEVEL:[' + str(self.level()) + ']')
        for file in self.names_files(): print('FILE:[' + file + ']')
        for dir in self.subdirs(): dir.dprint()

    def is_below(self, dir):
        if not isinstance(dir, (basedir, subdir)): return False
        return dir.path() in self.paths_from_base()

    def is_above(self,dir):
        if not isinstance(dir, (basedir, subdir)): return False
        return self.path() in dir.paths_from_base()

    @classmethod
    def same_family(cls,dir1,dir2):
        if not isinstance(dir1, (basedir, subdir)): return False
        if not isinstance(dir2, (basedir, subdir)): return False
        if not dir1.basedir(): return False
        if not dir2.basedir(): return False
        return dir1.basedir().path() == dir2.basedir().path()

    @classmethod
    def in_straight(cls,dir1,dir2):
        if not isinstance(dir1, (basedir, subdir)): return False
        if not isinstance(dir2, (basedir, subdir)): return False
        return dir1.is_below(dir2) or dir1.is_above(dir2)



class subdir(basedir):

    def __init__(self, name, parent):
        self._level = parent.level() + 1
        self._parent = None
        super().__init__(parent.path() + '/' + name)        
        if self.path(): self._parent = parent
        else: self._level = -1

    def level(self): return self._level

    def parent(self): return self._parent

    def basedir(self):
        if not self._parent: return None
        return self._parent.basedir()

    def paths_from_base(self):
        if not self._parent: return []
        paths = self.parent().paths_from_base()
        paths.append(self.path())
        return paths

    def remove_me(self):
        self.parent().remove_subdir(self.name())

def test():

    base = basedir("/Users/kawazome/Documents/Develop/python/sas_contents/output/root/foo")
    ja = base.get_subdir("ja")
    json = ja.get_subdir("json")
    hoge = ja.make_subdir("hoge")
    json.copy("faq.json",hoge)
    json.move("news.json",hoge)
    hoge.copy("/Users/kawazome/Documents/Develop/python/sas_contents/output/root/foo/en/json/language.json")
    ja.copy(hoge,"aho")
    images = base.get_subdir("en").get_subdir("images")
    hoge.move(images,"images2")
    ja.dprint()

if __name__ == '__main__':
    test()







