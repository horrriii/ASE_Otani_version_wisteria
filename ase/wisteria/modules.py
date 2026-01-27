import os
import shutil
from pathlib import Path
from typing import Optional


def make_calculation_directory(
    directory_name: str, outdir: str, srcdir_of_tmp: Optional[Path] = None
):
    DFT_path = Path.cwd() / directory_name
    target_path = DFT_path / outdir
    link_path = Path(str(target_path).replace("work/03", "data/scratch", 1))
    kernel_path = Path("~/QE/src/vdW_kernel_table").expanduser()

    os.makedirs(name=DFT_path, exist_ok=True)
    if srcdir_of_tmp is not None:
        srcdir_of_tmp = (srcdir_of_tmp / "tmp").expanduser()
        srcdir_of_tmp = Path(str(srcdir_of_tmp).replace("work/03", "data/scratch", 1))
        if os.path.lexists(link_path):
            if os.path.islink(link_path):
                os.unlink(link_path)
            elif os.path.isdir(link_path):
                shutil.rmtree(link_path)
            else:
                os.remove(link_path)
        shutil.copytree(src=srcdir_of_tmp, dst=link_path)
    else:
        os.makedirs(name=link_path, exist_ok=True)
    if os.path.lexists(target_path):
        os.remove(target_path)
    if os.path.lexists(DFT_path / "vdW_kernel_table"):
        os.remove(DFT_path / "vdW_kernel_table")
    os.symlink(link_path, target_path)
    os.symlink(kernel_path, DFT_path / "vdW_kernel_table")


def copy_temp_file(directory_name: str, outdir: str, save_dir: str, prefix: str):
    DFT_path = Path.cwd() / directory_name
    target_path = DFT_path / outdir

    os.makedirs(name=save_dir, exist_ok=True)
    for i in [".1drism", ".esm1", ".rism1"]:
        src_path = target_path / f"{prefix}{i}"
        if Path(src_path).exists():
            shutil.copy(src=src_path, dst=save_dir)
        else:
            pass


def get_total_charge(src_path: Path):
    with open(src_path / "espresso.pwo") as f:
        lines = [line for line in f if "FCP: Total Charge" in line]

    if not lines:
        with open(src_path / "espresso.pwi") as f:
            lines = [line for line in f if "tot_charge" in line]
        final_line = lines[-1]

    else:
        final_line = lines[-1]

    final_charge = final_line.split("=")[1]
    final_charge = float(final_charge)

    return final_charge
