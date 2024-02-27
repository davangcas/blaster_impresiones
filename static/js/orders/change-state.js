const getChangeOrderStateButton = (url, state) => {
    const state_options = {
        completed: "fas fa-truck",
        delivered: "far fa-money-bill-alt",
    };

    if (!["completed", "delivered"].includes(state)) {
        return "";
    }

    return `<a href="${url}" class="btn btn-success">
                <i class="${state_options[state]}"></i>
            </a>`;
};

const getAddOrderItemButton = (url, state) => {
    if (!["pending", "in_process", "completed"].includes(state)) {
        return "";
    }

    return `<a href="${url}" class="btn btn-primary">
                <i class="fas fa-plus"></i>
            </a>`;
};
