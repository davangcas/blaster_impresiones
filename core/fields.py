from crispy_forms.layout import HTML, Div, Field, Layout, Submit
from django.forms import DecimalField, IntegerField


class CommonLayout(Layout):
    submit_button_text = "Guardar"

    def __init__(self, *fields, **kwargs):
        include_footer_buttons = kwargs.pop("include_footer_buttons", True)
        creation_layout = Div(
            Div(css_id="previous-form-content", css_class="row"),
            *fields,
            Div(css_id="next-form-content", css_class="row"),
            css_class="card-body",
        )
        if include_footer_buttons:
            footer_div = Div(
                Div(
                    Div(
                        HTML(
                            "<a class='btn btn-outline-secondary m-1' href='{{ cancel_url }}' id='cancel-button' >Cancelar</a>"
                        ),
                        Submit(
                            "submit",
                            self.submit_button_text,
                            css_class="btn-primary m-1",
                        ),
                        css_class="col-12 text-center",
                    ),
                    css_class="row",
                ),
                css_class="card-footer",
            )
            initial_fields = (creation_layout, footer_div)
        else:
            initial_fields = (creation_layout,)
        self.fields = list(initial_fields)


class CustomDateField(Field):
    template = "core/fields/custom_date_field.html"


class CustomDateTimeField(Field):
    template = "core/fields/custom_datetime_field.html"


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
