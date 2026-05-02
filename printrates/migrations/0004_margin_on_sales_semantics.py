from django.db import migrations, models


def markup_to_margin_on_sales(apps, schema_editor):
    PrintRateVariables = apps.get_model("printrates", "PrintRateVariables")
    for row in PrintRateVariables.objects.all():
        k = int(row.general_profit_margin)
        if k <= 0:
            m = 0
        elif k >= 100:
            m = 99
        else:
            m = round(100 * k / (100 + k))
        if row.general_profit_margin != m:
            row.general_profit_margin = m
            row.save(update_fields=["general_profit_margin"])


def margin_on_sales_to_markup(apps, schema_editor):
    PrintRateVariables = apps.get_model("printrates", "PrintRateVariables")
    for row in PrintRateVariables.objects.all():
        m = int(row.general_profit_margin)
        if m <= 0:
            k = 0
        elif m >= 99:
            k = 99
        else:
            k = round(100 * m / (100 - m))
        row.general_profit_margin = k
        row.save(update_fields=["general_profit_margin"])


class Migration(migrations.Migration):
    dependencies = [
        ("printrates", "0003_printratevariables_expected_hours_and_margin"),
    ]

    operations = [
        migrations.RunPython(markup_to_margin_on_sales, margin_on_sales_to_markup),
        migrations.AlterField(
            model_name="printratevariables",
            name="maintenance_cost",
            field=models.DecimalField(
                decimal_places=2,
                default=0,
                help_text=(
                    "Costo fijo por impresión (repuestos, limpieza, etc.) que no esté "
                    "ya incluido en costos mensuales, para no duplicar el mismo gasto."
                ),
                max_digits=15,
            ),
        ),
        migrations.AlterField(
            model_name="printratevariables",
            name="minutes_spent_per_print",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text=(
                    "Minutos de mano de obra u operación por pieza cobrados a la "
                    "tarifa horaria; evitar solapar con tiempo que ya implícitamente "
                    "cubren los salarios usados en esa tarifa."
                ),
            ),
        ),
        migrations.AlterField(
            model_name="printratevariables",
            name="general_profit_margin",
            field=models.PositiveSmallIntegerField(
                default=33,
                help_text=(
                    "Margen bruto (%) sobre el precio de venta de cada impresión: "
                    "(precio - costo) / precio. Valores entre 0 y 99."
                ),
            ),
        ),
    ]
