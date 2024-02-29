from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django.forms import DecimalField, IntegerField


class CommonLayout(Layout):
    def __init__(self, *fields, **kwargs):
        creation_layout = Div(
            *fields,
            css_class="card-body",
        )
        footer_div = Div(
            Div(
                Div(
                    HTML(
                        "<a class='btn btn-outline-secondary' href='{{ cancel_url }}'>Cancelar</a>"
                    ),
                    Submit("submit", "Guardar", css_class="btn-primary"),
                    css_class="col-12 text-center",
                ),
                css_class="row",
            ),
            css_class="card-footer",
        )
        initial_fields = (creation_layout, footer_div)
        self.fields = list(initial_fields)


class CustomDateField(Field):
    template = "core/fields/custom_date_field.html"


class CustomTimeField(Field):
    template = "core/fields/custom_time_field.html"


class CustomSelectMultiple(Field):
    template = "core/fields/custom_select_multiple.html"


class CustomPriceFieldLayout(Field):
    template = "core/fields/custom_price_field.html"


class CustomPercentageFieldLayout(Field):
    template = "core/fields/custom_percentage_field.html"


class CustomPriceDecimalField(DecimalField):
    pass


class CustomPercentageField(IntegerField):
    pass
