import time
from pathlib import Path

from treelib import Tree

from aliyunpan.api.type import FileInfo


class PathList:
    def __init__(self, disk):
        self._tree = Tree()
        self._disk = disk
        self._tree.create_node(tag='root', identifier='root')
        self.depth = 3

    def update_path_list(self, file_id='root', depth=None, is_fid=True):
        if depth is None:
            depth = self.depth
        if not is_fid:
            file_id = self.get_path_fid(file_id, auto_update=False)
        file_list = self._disk.get_file_list(file_id)
        if 'items' not in file_list:
            return False
        for i in file_list['items']:
            if i['type'] == 'file':
                file_info = FileInfo(name=i['name'], id=i['file_id'], pid=i['parent_file_id'], type=True,
                                     ctime=time.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                     update_time=time.strptime(i['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                     hidden=i['hidden'],
                                     category=i['category'], size=i['size'], content_hash_name=i['content_hash_name'],
                                     content_hash=i['content_hash'], download_url=i['download_url'])
            else:
                file_info = FileInfo(name=i['name'], id=i['file_id'], pid=i['parent_file_id'], type=False,
                                     ctime=time.strptime(i['created_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                     update_time=time.strptime(i['updated_at'], '%Y-%m-%dT%H:%M:%S.%fZ'),
                                     hidden=i['hidden'])
            if self._tree.get_node(file_info.id):
                self._tree.update_node(file_id, data=file_info)
            else:
                self._tree.create_node(tag=file_info.name, identifier=file_info.id, data=file_info, parent=file_id)
            if not file_info.type and depth:
                self.update_path_list(file_id=file_info.id, depth=depth - 1)
        return True

    def tree(self, path='root', auto_update=True):
        file_id = self.get_path_fid(path, auto_update=auto_update)
        if not file_id:
            raise Exception('No such file or directory')
        self._tree.show(file_id)

    def get_path_list(self, path, auto_update=True):
        file_id = self.get_path_fid(path, auto_update=auto_update)
        return self.get_fid_list(file_id, auto_update=auto_update)

    def get_fid_list(self, file_id, auto_update=True):
        self.auto_update_path_list(auto_update)
        if not file_id:
            raise Exception('No such file or directory')
        if file_id != 'root' and self._tree.get_node(file_id).data.type:
            return [self._tree.get_node(file_id).data]
        return [i.data for i in self._tree.children(file_id)]

    def get_path_fid(self, path, file_id='root', auto_update=True):
        self.auto_update_path_list(auto_update)
        path = Path(path)
        if str(path) in ('', '/', '\\', '.', 'root'):
            return 'root'
        flag = False
        for i in filter(None, path.as_posix().split('/')):
            flag = False
            for j in self._tree.children(file_id):
                if i == j.tag:
                    flag = True
                    file_id = j.identifier
                    break
        if flag:
            return file_id
        return False

    def get_path_node(self, path, auto_update=True):
        file_id = self.get_path_fid(path, auto_update=auto_update)
        if file_id:
            return self._tree.get_node(file_id)
        return False

    def get_path_parent_node(self, path, auto_update=True):
        file_id = self.get_path_fid(path, auto_update=auto_update)
        if file_id:
            node = self._tree.parent(file_id)
            if node:
                return node
        return False

    def auto_update_path_list(self, auto_update=True):
        if auto_update and len(self._tree) == 1:
            return self.update_path_list()
