from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy


class CustomAdminViewMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, "No posee los permisos para realizar la accion")
            return HttpResponseRedirect(reverse_lazy("dashboard:login"))
        return super().dispatch(request, *args, **kwargs)
