from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "dashboard/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Dashboard"
        context["active_section"] = "dashboard"
        return context
