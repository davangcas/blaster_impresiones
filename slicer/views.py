import os
from types import SimpleNamespace

from django.conf import settings
from django.views.generic import FormView

from core.mixins import CustomAdminViewMixin
from printrates.models import PrintRateVariables
from prints.services import calculate_print_price
from slicer.forms import PrintEstimateForm
from slicer.slicer_api import post_slicer_estimate


class PrintEstimateView(CustomAdminViewMixin, FormView):
    form_class = PrintEstimateForm
    template_name = "slicer/estimate.html"
    permission_required = "prints.view_printmaterial"

    def get_initial(self):
        initial = super().get_initial()
        default_machine = (
            PrintRateVariables.get_singleton().default_machine or ""
        ).strip()
        if default_machine:
            initial["machine"] = default_machine
        return initial

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Calcular impresión"
        context["active_section"] = "print_estimate"
        context["slicer_configured"] = bool(
            (getattr(settings, "SLICER_HOST", None) or "").strip()
        )
        context.setdefault("estimate_result", None)
        return context

    def form_valid(self, form):
        uploaded = form.cleaned_data["source_file"]
        try:
            uploaded.seek(0)
        except OSError:
            pass

        material_obj = form.cleaned_data["material"]
        machine = (form.cleaned_data.get("machine") or "").strip()

        data, err = post_slicer_estimate(
            file_obj=uploaded,
            filename=os.path.basename(uploaded.name or "model.stl"),
            slicer_material=material_obj.slicer_filament,
            machine_id=machine or None,
        )
        if err:
            form.add_error(None, err)
            return self.form_invalid(form)

        grams_int = int(round(float(data["grams"])))
        pseudo = SimpleNamespace(
            material=material_obj,
            hours=int(data["hours"]),
            minutes=int(data["minutes"]),
            grams=grams_int,
        )
        price = calculate_print_price(pseudo)

        fresh_form = self.get_form_class()(initial=self.get_initial())
        context = self.get_context_data(
            form=fresh_form,
            estimate_result={
                "hours": int(data["hours"]),
                "minutes": int(data["minutes"]),
                "grams": data["grams"],
                "grams_int": grams_int,
                "price": price,
                "material_name": material_obj.name,
                "slicer_filament": material_obj.get_slicer_filament_display(),
            },
        )
        return self.render_to_response(context)
