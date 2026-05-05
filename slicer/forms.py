from __future__ import annotations

import os

from django import forms
from django.core.validators import FileExtensionValidator

from core.forms import DefaultForm
from prints.models import PrintMaterial
from slicer.choices import ALLOWED_MESH_EXTENSIONS
from slicer.services import validate_mesh_file_size
from slicer.slicer_api import fetch_slicer_machines


class PrintEstimateForm(DefaultForm):
    submit_button_text = "Calcular"

    source_file = forms.FileField(
        label="Modelo",
        required=False,
        help_text=(
            "Archivo STL u OBJ: se envía al servicio slicer para estimar tiempo y gramos. "
            "Si no subís archivo, completá horas, minutos y gramos abajo."
        ),
        validators=[
            FileExtensionValidator(allowed_extensions=list(ALLOWED_MESH_EXTENSIONS)),
            validate_mesh_file_size,
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
    speed = forms.IntegerField(
        label="Velocidad de impresión",
        min_value=1,
        max_value=500,
        initial=40,
        required=False,
        help_text="Velocidad en mm/s enviada al endpoint de estimación cuando hay modelo (por defecto 40).",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    hours = forms.IntegerField(
        label="Horas",
        required=False,
        min_value=0,
        help_text="Solo si no subís modelo: tiempo de impresión manual.",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    minutes = forms.IntegerField(
        label="Minutos",
        required=False,
        min_value=0,
        max_value=59,
        help_text="Solo si no subís modelo; entre 0 y 59.",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
    )
    grams = forms.DecimalField(
        label="Gramos",
        required=False,
        min_value=0,
        max_digits=10,
        decimal_places=2,
        help_text="Solo si no subís modelo: filamento estimado en gramos.",
        widget=forms.NumberInput(attrs={"class": "form-control"}),
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
        uploaded = self.cleaned_data.get("source_file")
        if not uploaded:
            return None
        name = (getattr(uploaded, "name", "") or "").lower()
        ext = os.path.splitext(name)[1].lstrip(".")
        if ext not in ALLOWED_MESH_EXTENSIONS:
            raise forms.ValidationError(
                "Solo se admiten archivos con extensión .stl o .obj.",
                code="invalid_mesh_ext",
            )
        return uploaded

    def clean_speed(self):
        value = self.cleaned_data.get("speed")
        if value is None:
            return 40
        return int(value)

    def clean(self):
        cleaned = super().clean()

        has_file = bool(cleaned.get("source_file"))
        hours = cleaned.get("hours")
        minutes = cleaned.get("minutes")
        grams = cleaned.get("grams")

        if has_file:
            return cleaned

        if hours is None:
            self.add_error(
                "hours",
                "Indicá las horas o subí un modelo STL/OBJ.",
            )
        if minutes is None:
            self.add_error(
                "minutes",
                "Indicá los minutos o subí un modelo STL/OBJ.",
            )
        if grams is None:
            self.add_error(
                "grams",
                "Indicá los gramos o subí un modelo STL/OBJ.",
            )

        if self.errors:
            return cleaned

        if grams is not None and grams <= 0:
            self.add_error(
                "grams",
                "Los gramos deben ser mayores que cero.",
            )

        return cleaned
