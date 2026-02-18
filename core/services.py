def get_select_checkbox(instance):
    return f"""
        <div class="custom-control custom-checkbox">
            <input class="custom-control-input custom-control-input-lightblue" type="checkbox" id="table-select-checkbox-{instance.id}" value="{instance.id}">
            <label for="table-select-checkbox-{instance.id}" class="custom-control-label"></label>
        </div>
    """


def format_as_cash_number(value, decimal_places=2):
    """
    Format a number as cash with a comma as the decimal separator and a dot as the thousands separator.

    Args:
        value (str or float): The value to format.
        decimal_places (int): The number of decimal places to display.

    Returns:
        str: The formatted cash value.
    """
    try:
        num = float(value)
    except (TypeError, ValueError):
        return value

    formatted = f"{num:,.{decimal_places}f}"
    integer_part, fractional_part = formatted.split(".")
    integer_part = integer_part.replace(",", ".")
    return f"{integer_part},{fractional_part}"
