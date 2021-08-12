from tp_yass.views.backend import helper


def test_generate_group_trees_should_return_group_trees(init_db_session):
    group_trees = helper.generate_group_trees()
    assert isinstance(group_trees, dict)
    for key in ('id', 'name', 'type', 'inheritance', 'descendants'):
        assert key in group_trees


def test_theme_importer_import_theme_banners_with_theme_name_should_copy_banners_to_dest(tmp_path):
    src_dir = tmp_path / 'original'
    dest_dir = tmp_path / 'uploads'
    src_dir.mkdir(exist_ok=True)
    dest_dir.mkdir(exist_ok=True)
    banner_file_name = 'bar.png'
    src_banner = src_dir / banner_file_name
    src_banner.touch()
    assert (dest_dir / banner_file_name).exists() is False
    theme_importer = helper.ThemeImporter('tp_yass2020', tmp_path)
    theme_importer.import_theme_banners(src_dir, dest_dir)
    assert (dest_dir / banner_file_name).exists() is True
