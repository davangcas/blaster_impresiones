from django.views.generic import TemplateView

from products.models import Product


class IndexView(TemplateView):
    template_name = "landing/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Home"
        context["active_section"] = "home"
        context["products"] = Product.objects.filter(
            available=True, image__isnull=False
        ).order_by("-id")[:10]
        return context


class AboutView(TemplateView):
    template_name = "landing/about.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Acerca de nosotros"
        context["active_section"] = "about"
        return context
