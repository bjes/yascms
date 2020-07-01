from pyramid_wtforms import widgets
from pyramid_wtforms import SelectMultipleField


class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget()
    option_widget = widgets.CheckboxInput()
