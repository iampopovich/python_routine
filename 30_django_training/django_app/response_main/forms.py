from django import forms


class UserForm(forms.Form):
    field_name = forms.CharField(required=False)
    field_age = forms.IntegerField(required=False)
    field_checkbox = forms.BooleanField(required=False)
    field_selection = forms.NullBooleanField(required=False)
    field_text_input = forms.CharField(required=False)
    field_email = forms.EmailField(required=False)
    field_ip = forms.GenericIPAddressField(required=False)
    field_regex = forms.RegexField(regex="kekule", required=False)
    field_url = forms.URLField(required=False)
    field_uuid = forms.UUIDField(required=False)
    field_combo = forms.ComboField(
        fields=[field_name, field_age], required=False)
    field_path = forms.FilePathField(path="/")
    field_file = forms.FileField(required=False)
    field_image = forms.ImageField(required=False)
    field_date = forms.DateField(required=False)
    field_time = forms.TimeField(required=False)
    field_datetime = forms.DateTimeField(required=False)
    field_duration = forms.DurationField(required=False)
    field_split_date_time = forms.SplitDateTimeField(required=False)
    field_integer_value = forms.IntegerField()
    field_decimal_value = forms.DecimalField()
    field_float_value = forms.FloatField()
    field_choice = forms.ChoiceField((0, 'zero'), (1, 'one'), (2, 'two'))
