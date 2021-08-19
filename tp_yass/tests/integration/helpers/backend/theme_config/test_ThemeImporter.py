from tp_yass.helpers.backend.theme_config import ThemeImporter


def test_import_theme_banners_with_theme_name_should_copy_banners_to_dest(tmp_path):
    src_dir = tmp_path / 'original'
    dest_dir = tmp_path / 'uploads'
    src_dir.mkdir(exist_ok=True)
    dest_dir.mkdir(exist_ok=True)
    banner_file_name = 'bar.png'
    src_banner = src_dir / banner_file_name
    src_banner.touch()
    assert not (dest_dir / banner_file_name).exists()
    theme_importer = ThemeImporter('tp_yass2020', tmp_path)
    theme_importer.import_theme_banners(src_dir, dest_dir)
    assert (dest_dir / banner_file_name).exists()
