from django import forms


class UserForm(forms.Form):
    field_name = forms.CharField()
    field_age = forms.IntegerField()
    field_checkbox = forms.BooleanField()
    field_selection = forms.NullBooleanField()
    field_text_input = forms.CharField()
    field_email = forms.EmailField()
    field_ip = forms.GenericIPAddressField()
    field_regex = forms.RegexField(regex="kekule")
    field_url = forms.URLField()
    field_uuid = forms.UUIDField()
    field_combo = forms.ComboField(fields=[field_name, field_age])
    field_path = forms.FilePathField(path="/")
