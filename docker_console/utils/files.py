import os
import tempfile
import uuid
import shutil
import tarfile

def copy_file(src, dst, force):
    if not os.path.exists(dst) or force:
        shutil.copyfile(
            src,
            dst
        )

def create_dir_copy(path, dest_path=None, force_update=False):
    if dest_path is None:
        temp_dir = tempfile.gettempdir()
        dest_path = os.path.join(temp_dir, str(uuid.uuid4()))
        os.mkdir(dest_path)
    for root, dirs, files in os.walk(path):
        path_tail = root.split(path)[-1]
        if not path_tail:
            path_tail = "/"
        for dir in dirs:
            dest_dir_path = dest_path + os.path.join(path_tail, dir)
            if not os.path.exists(dest_dir_path):
                os.mkdir(dest_dir_path)
        for name in files:
            dest_file_path = dest_path + os.path.join(path_tail, name)
            src = os.path.join(root, name)

            if not os.path.exists(dest_file_path) or force_update:
                shutil.copyfile(
                    src,
                    dest_file_path
                )

    return dest_path

def unpack_tar(src, dest):
    if src[-6:] == 'tar.gz':
        tar = tarfile.open(src)
        tar.extractall(dest)
        tar.close()
        return tar

def sql_files(members):
    for tarinfo in members:
        if os.path.splitext(tarinfo.name)[1] == ".sql" or os.path.splitext(tarinfo.name)[1] == ".msql":
            yield tarinfo
