from django import forms


class FormWithWidget(forms.Form):
    widget_pass = forms.PasswordInput()
    widget_hidden_input = forms.HiddenInput()
    widget_multiple_hidden_input = forms.MultipleHiddenInput()
    widget_radio_select = forms.RadioSelect()
    widget_checkbox_select_multiple = forms.CheckboxSelectMultiple()
    widget_time_input = forms.TimeInput()
    widget_selection_date_widget = forms.SelectDateWidget()
    widget_split_hidden_datetime_widget = forms.SplitHiddenDateTimeWidget()
    widget_file_input = forms.FileInput()
