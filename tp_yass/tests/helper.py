import plaster
from sqlalchemy import engine_from_config
from sqlalchemy.orm import sessionmaker


def get_ini_settings(ini_file_path):
    """Return ini settings"""

    return plaster.get_settings(ini_file_path, 'app:main')


def import_test_db_data(ini_file_path):
    """Import test data to test database"""

    from mixer.backend.sqlalchemy import Mixer

    ini_settings = get_ini_settings(ini_file_path)
    engine = engine_from_config(ini_settings)
    Session = sessionmaker(bind=engine)
    mixer = Mixer(session=Session(), commit=True, locale='zh_TW')

    # mixer.blend('tp_yass.models.mymodel', id=1, name='foo', value=1)

    # with mixer.ctx(commit=False):
    #     session = Session()
    #     data = mixer.blend('tp_yass.models.mymodel',
    #                        id=2, name='bar', value=2)
    #     session.add(data)
    #     session.commit()

