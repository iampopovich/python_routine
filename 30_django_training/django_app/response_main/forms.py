from django import forms


class UserForm(forms.Form):
    name = forms.CharField()
    age = forms.IntegerField()
    checkbox = forms.BooleanField()
    selection = forms.NullBooleanField()
    text_input = forms.CharField()
    field_email = forms.EmailField()
    field_ip = forms.GenericIPAddressField()
    field_regex = forms.RegexField (regex="kekule")
    field_url = forms.URLField()
