from crispy_forms.layout import HTML, Div, Field, Layout, Submit


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
