from pyramid_wtforms import (Form,
                             StringField,
                             FieldList,
                             FormField,
                             HiddenField)
from pyramid_wtforms.validators import InputRequired, Length


class SysConfigEntryForm(Form):
    name = HiddenField('name', [InputRequired('name 為必填欄位'), Length(min=1)])
    value = StringField('value', [InputRequired('value 為必填欄位'), Length(min=1)])
    description = StringField('description', [InputRequired('description 為必填欄位'), Length(min=1)])


class SysConfigForm(Form):
    config = FieldList(FormField(SysConfigEntryForm))
