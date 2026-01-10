import shutil
import sys

from scripts.base import console, Project
from scripts.commands import uvc, hatchc


def main():
    project = Project()
    # 处理新的版本号
    ver = sys.argv[1] if len(sys.argv) > 1 else None

    if ver:
        with console.status('Setting version'):
            hatchc.set_version(project.path, ver)

    for module in project.iter_modules():
        target_reiport_file = project.path / 'hydrogenlib' / (module.name.replace('-', '_') + '.py')
        if (re_import_file := (module.path / 're-import.py')).exists():
            shutil.copy(re_import_file, target_reiport_file)
            console.info(f"{f'<{module.name}>':20} Find existing re-import.py, copy to project dir")
        else:
            # 手动生成 re-import
            target_reiport_file.write_text(
                f"from {module.import_name} import *"
            )
            console.info(f"{f'<{module.name}>':20} Generate re-import.py")

    with console.status('Building project'):
        cp = uvc.uv(['build'], cwd=project.path)


if __name__ == '__main__':
    main()
