from pathlib import Path
import subprocess

from invoke import task

import tp_yass


@task
def generate(c):
    """產生文件"""

    proj_root_dir = Path(tp_yass.__file__).parent.parent
    doc_root_dir = proj_root_dir / 'docs'

    delete_list = [doc_root_dir / 'tp_yass' / '*',
                   doc_root_dir / '_build' / 'html']
    for each_entry in delete_list:
        subprocess.run(f'rm -rf {each_entry}', shell=True)

    subprocess.run(f'sphinx-apidoc -f -o {doc_root_dir}/tp_yass {proj_root_dir}/tp_yass', shell=True)
    subprocess.run(f'cd {doc_root_dir} && make html', shell=True)
