from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.views.generic import TemplateView
from clients.models import Client
from products.models import Product
from orders.models import Order


class IndexView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["active_section"] = "dashboard"
        context["clients_count"] = Client.objects.all().count()
        context["products_count"] = Product.objects.all().count()
        context["completed_orders_count"] = Order.objects.filter(state="completed").count()
        context["pending_orders_count"] = Order.objects.exclude(state="completed").count()
        return context


class LoginFormView(LoginView):
    template_name = "dashboard/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("dashboard:index")
        return super().dispatch(request, *args, **kwargs)
