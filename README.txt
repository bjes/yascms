tp_yass
=======

Getting Started
---------------

- Change directory into your newly created project.

    cd tp_yass

- Create a Python virtual environment.

    python3 -m venv .venv

- Upgrade packaging tools.

    .venv/bin/pip install --upgrade pip setuptools pipenv

- Install the project in editable mode with its testing requirements.

    .venv/bin/pipenv sync --dev

- Initialize and upgrade the database using Alembic.

    - Generate your first revision.

        .venv/bin/alembic -c development.ini revision --autogenerate -m "init"

    - Upgrade to that revision.

        .venv/bin/alembic -c development.ini upgrade head

- Load default data into the database using a script.

    .venv/bin/initialize_tp_yass_db development.ini

- Run your project's tests.

    .venv/bin/pytest

- Run your project.

    .venv/bin/pserve development.ini
