from tp_yass.views.helper.file import convert_image_file


def test_convert_image_file_should_convert_image_successfully(datadir, tmp_path):
    new_img_name = 'new_logo.png'
    destination_path = tmp_path / 'new_logo.png'
    assert convert_image_file(str(datadir / 'logo.png'), str(destination_path)) == new_img_name
    assert destination_path.exists()
