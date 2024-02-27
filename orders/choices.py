ORDER_STATE_CHOICES = (
    ("pending", "Pendiente"),
    ("confirmed", "Confirmada"),
    ("in_progress", "En progreso"),
    ("completed", "Completada"),
    ("delivered", "Entregada"),
    ("canceled", "Cancelada"),
    ("paid", "Pagada"),
)

ORDER_STATE_STYLES_DICT = {
    "pending": "secondary",
    "confirmed": "warning",
    "in_progress": "info",
    "completed": "primary",
    "delivered": "primary",
    "canceled": "danger",
    "paid": "success",
}
