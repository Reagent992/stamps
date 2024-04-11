from django import forms
from django.core.validators import RegexValidator


class StampTextForm(forms.Form):
    """Форма полей штампа."""

    def __init__(self, fields, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in fields:
            self.fields[field.name] = forms.CharField(
                help_text=field.help_text,
                label=field.name,
                required=True,
                validators=[
                    RegexValidator(
                        regex=field.re,
                        flags=2,
                    )
                ],
            )
