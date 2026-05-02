from django import forms

from slicer.choices import MAX_MESH_BYTES


def validate_mesh_file_size(uploaded):
    size = getattr(uploaded, "size", None)
    if size is not None and size > MAX_MESH_BYTES:
        raise forms.ValidationError(
            "El archivo supera el tamaño máximo permitido (50 MB).",
            code="mesh_too_large",
        )
