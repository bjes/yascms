from pathlib import Path
import subprocess

from invoke import task

import yascms


@task
def generate(c):
    """產生文件"""

    proj_root_dir = Path(yascms.__file__).parent.parent
    doc_root_dir = proj_root_dir / 'docs'

    delete_list = [doc_root_dir / 'yascms' / '*',
                   doc_root_dir / '_build' / 'html']
    for each_entry in delete_list:
        subprocess.run(f'rm -rf {each_entry}', shell=True)

    subprocess.run(f'sphinx-apidoc -f -o {doc_root_dir}/yascms {proj_root_dir}/yascms', shell=True)
    subprocess.run(f'pyreverse -p yascms {proj_root_dir}/yascms', shell=True)
    subprocess.run(f'dot {proj_root_dir}/classes_yascms.dot -T png -o {doc_root_dir}/images/uml_class_diagram.png', shell=True)
    subprocess.run(f'dot {proj_root_dir}/packages_yascms.dot -T png -o {doc_root_dir}/images/package_import_diagram.png', shell=True)
    subprocess.run(f'rm {proj_root_dir}/classes_yascms.dot packages_yascms.dot', shell=True)
    subprocess.run(f'cd {doc_root_dir} && make html', shell=True)
