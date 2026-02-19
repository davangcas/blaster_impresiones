from datetime import datetime

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.exceptions import FieldDoesNotExist
from django.db.models import CharField, F, ForeignKey, Q, TextField
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import View
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
                except Exception:
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
                    try:
                        model = self.model
                        parts = column.split("__")

                        for part in parts[:-1]:
                            field = model._meta.get_field(part)
                            if isinstance(field, ForeignKey):
                                model = field.remote_field.model
                            else:
                                raise FieldDoesNotExist

                        final_field = model._meta.get_field(parts[-1])

                        if isinstance(final_field, (CharField, TextField)):
                            q |= Q(**{f"{column}__{filter_method}": search})

                    except FieldDoesNotExist:
                        continue

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
        return super().render_column(row, column) or "-"


class DeleteMultipleObjectsMixin(CustomAdminViewMixin, View):
    model = None

    def post(self, request, *args, **kwargs):
        self.model.objects.filter(
            pk__in=request.POST.getlist("selected_ids[]")
        ).delete()
        return JsonResponse(
            {"success": True, "message": "Elementos eliminados con éxito"}
        )


class ActiveToggleMultipleObjecsMixin(CustomAdminViewMixin, View):
    model = None

    def post(self, request, *args, **kwargs):
        queryset = self.model.objects.filter(
            pk__in=request.POST.getlist("selected_ids[]")
        )
        queryset.update(is_active=~F("is_active"))
        return JsonResponse(
            {"success": True, "message": "Elementos actualizados con éxito"}
        )
