from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from django.views.generic import ListView


class CustomAdminViewMixin(LoginRequiredMixin, PermissionRequiredMixin):
    def dispatch(self, request, *args, **kwargs):
        if not self.has_permission():
            messages.error(request, "No posee los permisos para realizar la accion")
            return HttpResponseRedirect(reverse_lazy("dashboard:login"))
        return super().dispatch(request, *args, **kwargs)


class PostListViewMixin(CustomAdminViewMixin, ListView):
    def post(self, request, *args, **kwargs):
        self.object_list = self.get_queryset()
        data = self.serializer_class(self.object_list, many=True).data
        response = JsonResponse({"data": data}, safe=False)
        return response
