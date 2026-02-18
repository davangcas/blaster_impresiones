from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django_datatables_view.base_datatable_view import BaseDatatableView


class CustomAdminViewMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, "No posee los permisos para realizar la accion")
            return HttpResponseRedirect(reverse_lazy("dashboard:login"))

        if not request.user.is_active:
            return HttpResponseRedirect(reverse_lazy("dashboard:login"))

        return super().dispatch(request, *args, **kwargs)


class CustomDatatablesJsonMixin(CustomAdminViewMixin, BaseDatatableView):
    def get_initial_queryset(self):
        filter_lookup = {}
        for key, value in self.request.GET.items():
            if "table_filter" in key:
                try:
                    filter_lookup[key.replace("table_filter_", "")] = datetime.strptime(
                        value, "%d/%m/%Y"
                    ).date()
                except (ValueError, TypeError):
                    filter_lookup[key.replace("table_filter_", "")] = value

        return super().get_initial_queryset().filter(**filter_lookup)

    def filter_queryset(self, qs):
        columns = self._columns

        if not self.pre_camel_case_notation:
            q = Q()
            search = self._querydict.get("search[value]", None)
            filter_method = self.get_filter_method()

            for col_no, col in enumerate(self.columns_data):
                data_field = col["data"]

                try:
                    data_field = int(data_field)
                except ValueError:
                    pass

                if isinstance(data_field, int):
                    column = columns[data_field]
                else:
                    column = data_field

                column = column.replace(".", "__")

                if not hasattr(self.model, column):
                    continue

                if search and col["searchable"]:
                    q |= Q(**{"{0}__{1}".format(column, filter_method): search})

                if col["search.value"]:
                    qs = qs.filter(
                        **{
                            "{0}__{1}".format(column, filter_method): col[
                                "search.value"
                            ]
                        }
                    )
            qs = qs.filter(q)
        return qs

    def get_filter_method(self):
        return self.FILTER_ICONTAINS

    def render_column(self, row, column):
        rendered_column = super().render_column(row, column)
        return rendered_column or "-"
