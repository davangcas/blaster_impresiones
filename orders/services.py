from django.urls import reverse_lazy


def get_order_state_button(order):
    state_options = {
        "completed": "fas fa-truck",
        "delivered": "far fa-money-bill-alt",
    }

    if order.state not in ("completed", "delivered"):
        return ""

    url = reverse_lazy("orders:change_state", kwargs={"pk": order.pk})

    return f"""
        <a href="{url}" class="btn btn-success">
            <i class="{state_options[order.state]}"></i>
        </a>
    """


def get_add_item_button(order):
    if order.state in ("paid", "delivered"):
        return ""

    url = reverse_lazy("orders:items_create", kwargs={"pk": order.pk})
    return f"""
        <a href="{url}" class="btn btn-primary">
            <i class="fas fa-plus"></i>
        </a>
    """


def get_order_buttons(order):
    update_url = reverse_lazy("orders:update", kwargs={"pk": order.id})
    delete_url = reverse_lazy("orders:delete", kwargs={"pk": order.id})
    items_url = reverse_lazy("orders:items", kwargs={"pk": order.id})
    change_state_button = get_order_state_button(order)
    add_item_button = get_add_item_button(order)
    update_content = ""

    if order.state not in ("paid", "delivered"):
        update_content = f"""
            <a href="{update_url}" class="btn btn-warning">
                <i class="fas fa-edit"></i>
            </a>
        """

    return f"""
        {change_state_button}
        {add_item_button}
        <a href="{items_url}" class="btn btn-info">
            <i class="fas fa-eye"></i>
        </a>
        {update_content}
        <a href="{delete_url}" class="btn btn-danger">
            <i class="fas fa-trash"></i>
        </a>
    """


def get_order_item_buttons(order_item):
    update_url = reverse_lazy("orders:items_update", kwargs={"pk": order_item.id})
    delete_url = reverse_lazy("orders:items_delete", kwargs={"pk": order_item.id})
    detail_url = reverse_lazy("orders:print_order_items", kwargs={"pk": order_item.id})
    update_content = ""
    delete_content = ""

    if order_item.state not in ("paid", "delivered"):
        update_content = f"""
            <a href="{update_url}" class="btn btn-warning">
                <i class="fas fa-edit"></i>
            </a>
        """
        delete_content = f"""
            <a href="{delete_url}" class="btn btn-danger">
                <i class="fas fa-trash"></i>
            </a>
        """

    return f"""
        <a href="{detail_url}" class="btn btn-info">
            <i class="fas fa-eye"></i>
        </a>
        {update_content}
        {delete_content}
    """


def get_print_order_item_buttons(print_order_item):
    change_state_foward_content = ""
    change_state_cancel_content = ""
    update_content = ""

    update_url = reverse_lazy(
        "orders:print_order_items_update", kwargs={"pk": print_order_item.pk}
    )
    change_state_url = reverse_lazy(
        "orders:print_order_items_change_state", kwargs={"pk": print_order_item.pk}
    )
    detail_url = reverse_lazy(
        "orders:print_order_items_detail", kwargs={"pk": print_order_item.pk}
    )
    detail_content = f"""
        <a href="{detail_url}" class="btn btn-info">
            <i class="fas fa-eye"></i>
        </a>
    """

    if print_order_item.state not in ("delivered", "paid"):
        change_state_foward_content = f"""
            <a href="{change_state_url}?next_step=True" class="btn btn-dark">
                <i class="fas fa-step-forward"></i>
            </a>
        """
        change_state_cancel_content = f"""
            <a href="{change_state_url}?next_step=False" class="btn btn-danger">
                <i class="fas fa-times-circle"></i>
            </a>
        """
        update_content = f"""
            <a href="{update_url}" class="btn btn-primary">
                <i class="fas fa-tint"></i>
            </a>
        """

    return f"""
        {change_state_foward_content}
        {change_state_cancel_content}
        {update_content}
        {detail_content}
    """
