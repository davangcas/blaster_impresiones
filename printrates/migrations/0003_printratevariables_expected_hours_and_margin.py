# Generated manually for print pricing redesign

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("printrates", "0002_historicalprintrate"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="printratevariables",
            name="available_printers",
        ),
        migrations.AddField(
            model_name="printratevariables",
            name="expected_daily_print_hours",
            field=models.PositiveSmallIntegerField(
                default=6,
                help_text="Horas de impresión esperadas por día; se multiplican por 30 para repartir costos mensuales.",
            ),
        ),
        migrations.AddField(
            model_name="printratevariables",
            name="general_profit_margin",
            field=models.PositiveSmallIntegerField(
                default=50,
                help_text="Margen de ganancia (%) sobre el costo total de cada impresión.",
            ),
        ),
    ]
