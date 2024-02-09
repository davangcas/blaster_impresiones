class CustomAdminViewMixin:
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["custom_admin_view"] = True
        return context
