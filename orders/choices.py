ORDER_STATE_CHOICES = (
    ("pending", "Pendiente"),
    ("confirmed", "Confirmada"),
    ("in_progress", "En progreso"),
    ("completed", "Completada"),
    ("delivered", "Entregada"),
    ("canceled", "Cancelada"),
    ("paid", "Pagada"),
)

ORDER_ITEM_PRINT_EDIT_STATES = ("pending", "in_progress")

PRINT_ORDER_ITEM_SELECTABLE_STATE_CHOICES = (
    ("pending", "Pendiente"),
    ("in_progress", "En progreso"),
    ("completed", "Completada"),
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
