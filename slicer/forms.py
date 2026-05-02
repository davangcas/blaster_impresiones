from __future__ import annotations

import os

from django import forms
from django.core.validators import FileExtensionValidator

from core.forms import DefaultForm
from prints.models import PrintMaterial
from slicer.slicer_api import fetch_slicer_machines

_MESH_EXTENSIONS = ("stl", "obj")
_MAX_MESH_BYTES = 50 * 1024 * 1024


def _validate_mesh_file_size(uploaded):
    size = getattr(uploaded, "size", None)
    if size is not None and size > _MAX_MESH_BYTES:
        raise forms.ValidationError(
            "El archivo supera el tamaño máximo permitido (50 MB).",
            code="mesh_too_large",
        )


class PrintEstimateForm(DefaultForm):
    submit_button_text = "Calcular"

    source_file = forms.FileField(
        label="Modelo",
        required=True,
        help_text="Archivo de malla para estimar tiempo y consumo de filamento.",
        validators=[
            FileExtensionValidator(allowed_extensions=list(_MESH_EXTENSIONS)),
            _validate_mesh_file_size,
        ],
        widget=forms.ClearableFileInput(
            attrs={"class": "form-control-file", "accept": ".stl,.obj,model/stl"}
        ),
    )
    material = forms.ModelChoiceField(
        queryset=PrintMaterial.objects.all().order_by("name"),
        label="Material",
        required=True,
        help_text="Material del catálogo (precio por kg y tipo Cura para el slicer).",
        widget=forms.Select(
            attrs={
                "class": "select2bs4 select2-hidden-accessible",
                "style": "width: 100%;",
            }
        ),
    )
    machine = forms.ChoiceField(
        label="Máquina",
        required=False,
        choices=[],
        help_text="Perfil de impresora (GET /machines). Opcional; vacío usa la máquina por defecto del servicio.",
        widget=forms.Select(
            attrs={
                "class": "select2bs4 select2-hidden-accessible",
                "style": "width: 100%;",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        machines = fetch_slicer_machines()
        choices = [(m["id"], m["name"]) for m in machines]

        current = ""
        if self.initial.get("machine") is not None:
            current = str(self.initial.get("machine") or "").strip()
        elif "machine" in self.data:
            current = (self.data.get("machine") or "").strip()

        if not choices:
            self.fields["machine"].choices = [
                ("", "— No hay máquinas disponibles (revisá SLICER_HOST) —"),
            ]
            self.fields["machine"].disabled = True
        else:
            if current and all(c[0] != current for c in choices):
                choices.insert(0, (current, f"{current} (valor previo)"))
            self.fields["machine"].choices = [
                ("", "— Sin máquina específica (usa la del servicio) —"),
                *choices,
            ]

    def clean_machine(self):
        value = (self.cleaned_data.get("machine") or "").strip()
        if not value:
            return ""
        if self.fields["machine"].disabled:
            return ""
        return value

    def clean_source_file(self):
        uploaded = self.cleaned_data["source_file"]
        name = (getattr(uploaded, "name", "") or "").lower()
        ext = os.path.splitext(name)[1].lstrip(".")
        if ext not in _MESH_EXTENSIONS:
            raise forms.ValidationError(
                "Solo se admiten archivos con extensión .stl o .obj.",
                code="invalid_mesh_ext",
            )
        return uploaded
