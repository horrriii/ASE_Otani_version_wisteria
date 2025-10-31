import os
import shutil
from pathlib import Path


def make_calculation_directory(directory_name: int, outdir: int):
    DFT_path = os.getcwd() + "/" + directory_name
    target_path = DFT_path + "/" + outdir
    link_path = target_path.replace("work/03", "data/scratch", 1)
    kernel_path = str(Path("~/QE/src/vdW_kernel_table").expanduser())

    os.makedirs(name=directory_name, exist_ok=True)
    os.makedirs(name=link_path, exist_ok=True)
    if os.path.lexists(target_path):
        os.remove(target_path)
    if os.path.lexists(os.path.join(DFT_path, "vdW_kernel_table")):
        os.remove(os.path.join(DFT_path, "vdW_kernel_table"))
    os.symlink(link_path, target_path)
    os.symlink(kernel_path, os.path.join(DFT_path, "vdW_kernel_table"))

def copy_temp_file(directory_name: int, outdir: int, save_dir: int, prefix: int):
    DFT_path = os.getcwd() + "/" + directory_name
    target_path = DFT_path + "/" + outdir

    os.makedirs(name=save_dir, exist_ok=True)
    for i in [".esm1"]:
        shutil.copy(src=target_path + "/" + prefix + i, dst=save_dir + "/")
