const CommonDataTable = (function () {
    const defaultButtonConfig = {
        pageLength: {
            extend: "pageLength",
            text: "Registros por página",
            className: "btn btn-default",
            options: [10, 25, 50, 100, -1],
            postfix: " entradas",
        },
        copy: {
            extend: "copy",
            className: "btn btn-secondary",
            exportOptions: {
                columns: ":visible:not(:first-child):not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        csv: {
            extend: "csv",
            className: "btn btn-info",
            exportOptions: {
                columns: ":visible:not(:first-child):not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        excel: {
            extend: "excel",
            className: "btn btn-success",
            exportOptions: {
                columns: ":visible:not(:first-child):not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        pdf: {
            extend: "pdf",
            className: "btn btn-danger",
            exportOptions: {
                columns: ":visible:not(:first-child):not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
            customize: function (doc) {
                doc.content[1].layout = "noBorders";
                doc.content[1].table.widths = Array(
                    doc.content[1].table.body[0].length + 1
                )
                    .join("*")
                    .split("");
                const document_table = doc.content[1].table;
                document_table.body.forEach(function (row) {
                    row.forEach(function (cell) {
                        cell.alignment = "center";
                    });
                });
            },
        },
        print: {
            extend: "print",
            className: "btn btn-gray",
            exportOptions: {
                columns: ":visible:not(:first-child):not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        colvis: {
            extend: "colvis",
            className: "btn btn-warning",
            text: "Columnas visibles",
            columns: ":not(:first-child):not(:last-child)",
        },
    };

    const initTable = function (settings) {
        const table_id = settings.table_id;
        const source_url = settings.source_url;
        const table_filters = {};
        const defaultColumnDefs = [];

        if (settings.columnDefs) {
            settings.columnDefs = defaultColumnDefs.concat(settings.columnDefs);
        } else {
            settings.columnDefs = defaultColumnDefs;
        }

        const buttonsConfig = settings.buttonsConfig || {};
        const buttons = Object.keys(defaultButtonConfig).map((buttonKey) => {
            let buttonsettings = {
                ...defaultButtonConfig[buttonKey],
                ...buttonsConfig[buttonKey],
            };
            buttonsettings.title =
                $(settings.table_id).attr("data-title") || document.title;

            if (buttonKey === "print") {
                buttonsettings.title = "";
                buttonsettings.messageTop = function () {
                    const title =
                        $(settings.table_id).attr("data-title") ||
                        document.title;
                    return `
                        <div style="text-align: center; margin-bottom: 20px;" id="print-header">
                            <img src="${organization_logo}" alt="Logo" style="max-width: 100px;"/><br>
                            <strong>${title}</strong><br>
                        </div>
                    `;
                };
                buttonsettings.messageBottom = function () {
                    let rendered_text = `<div style="text-align: left; margin-top: 20px;">${organization_name}<br>`;

                    if (organization_phone_number) {
                        rendered_text += `Teléfono: ${organization_phone_number}<br>`;
                    }

                    if (organization_email) {
                        rendered_text += `Email: ${organization_email}<br>`;
                    }

                    if (organization_cuit) {
                        rendered_text += `CUIT: ${organization_cuit}<br>`;
                    }

                    rendered_text += `</div>`;
                    return rendered_text;
                };
            } else if (buttonKey === "pdf") {
                let originalPdfCustomize = buttonsettings.customize;

                buttonsettings.customize = function (doc) {
                    if (typeof originalPdfCustomize === "function") {
                        originalPdfCustomize(doc);
                    }

                    let rendered_text = `${organization_name}\n`;

                    if (organization_phone_number) {
                        rendered_text += `Teléfono: ${organization_phone_number}\n`;
                    }

                    if (organization_email) {
                        rendered_text += `Email: ${organization_email}\n`;
                    }

                    if (organization_cuit) {
                        rendered_text += `CUIT: ${organization_cuit}\n`;
                    }

                    doc.content.push({
                        text: rendered_text,
                        margin: [0, 20, 0, 0],
                        alignment: "left",
                        fontSize: 10,
                        bold: true,
                    });
                };
            } else if (buttonKey === "excel") {
                const currencyRe =
                    /^\s*\$\s*(?:\d{1,3}(?:\.\d{3})*|\d+)(?:,\d+)?\s*$/;

                buttonsettings.customizeData = function (data) {
                    data.body.forEach((row) => {
                        row.forEach((cell, colIndex) => {
                            if (
                                typeof cell !== "string" ||
                                !currencyRe.test(cell.trim())
                            ) {
                                return;
                            }

                            let raw = cell.replace(/[^0-9,\.]/g, "");
                            raw = raw.replace(/[\.\s]/g, "");
                            raw = raw.replace(/,([^,]*)$/, ".$1");
                            row[colIndex] = raw;
                        });
                    });
                };
            }

            return buttonsettings;
        });

        const commonTable = $(table_id).DataTable({
            responsive: true,
            lengthChange: true,
            pageLength: 10,
            lengthMenu: [
                [10, 25, 50, 100, -1],
                [10, 25, 50, 100, "Todos"],
            ],
            select: settings.multiSelect
                ? {
                    style: "multi",
                    blurable: false,
                    selector: 'td:first-child input[type="checkbox"]',
                }
                : false,
            autoWidth: false,
            paging: true,
            processing: true,
            serverSide: true,
            searching: true,
            ordering: true,
            info: true,
            deferRender: true,
            dom: "Bfrtip",
            buttons: buttons,
            language: {
                sProcessing: "Procesando...",
                sLengthMenu: "Mostrar _MENU_ registros",
                sZeroRecords: "No se encontraron resultados",
                sEmptyTable: "Ningún dato disponible en esta tabla",
                sInfo: "Mostrando registros del _START_ al _END_ de un total de _TOTAL_ registros",
                sInfoEmpty:
                    "Mostrando registros del 0 al 0 de un total de 0 registros",
                sInfoFiltered: "(filtrado de un total de _MAX_ registros)",
                sInfoPostFix: "",
                sSearch: "Buscar",
                sUrl: "",
                sInfoThousands: ",",
                sLoadingRecords: "Cargando...",
                oPaginate: {
                    sFirst: "Primero",
                    sLast: "Último",
                    sNext: "Siguiente",
                    sPrevious: "Anterior",
                },
                oAria: {
                    sSortAscending:
                        ": Activar para ordenar la columna de manera ascendente",
                    sSortDescending:
                        ": Activar para ordenar la columna de manera descendente",
                },
                buttons: {
                    colvis: "Columnas visibles",
                    copy: "Copiar",
                    print: "Imprimir",
                },
                select: {
                    rows: {
                        _: "%d filas seleccionadas",
                        0: "Ninguna fila seleccionada",
                        1: "1 fila seleccionada",
                    },
                },
            },
            ajax: {
                url: source_url,
                data: function (d) {
                    return $.extend({}, d, table_filters);
                },
            },
            columnDefs: settings.columnDefs,
            initComplete: function () {
                this.api()
                    .buttons()
                    .container()
                    .appendTo(`${table_id}_wrapper .col-md-6:eq(0)`);

                if (settings.initComplete) {
                    settings.initComplete();
                }

                $(table_id).on("draw.dt", function () {
                    if (settings.initComplete) {
                        settings.initComplete();
                    }
                });
            },
        });

        $("#filter-button").on("click", function () {
            $(".table-filter").each(function () {
                if ($(this).val()) {
                    table_filters[`table_filter_${$(this).attr("name")}`] =
                        $(this).val();
                }
            });
            commonTable.ajax.reload();
        });

        $("#clean-filters-button").on("click", function () {
            $(".table-filter").each(function () {
                if ($(this).is("select")) {
                    $(this).find("option").prop("selected", false);
                    $(this).trigger("change");
                } else {
                    $(this).val("");
                }
            });

            Object.keys(table_filters).forEach(function (key) {
                delete table_filters[key];
            });
            commonTable.ajax.reload();
        });

        const tableCard = $(table_id).closest(".card");
        const selectAllCheckbox = $(table_id).find("#select-all-items-checkbox");
        if (settings.multiSelect && selectAllCheckbox.length) {
            selectAllCheckbox.on("change", function () {
                const checked = $(this).prop("checked");
                const checkboxes = $(table_id).find("tbody input[type='checkbox']");
                checkboxes.prop("checked", checked).trigger("change");

                if (checked) {
                    checkboxes.each(function () {
                        const row = $(this).closest("tr");
                        commonTable.row(row).select();
                    });
                    tableCard.find(".custom-table-actions-button").show();
                } else {
                    checkboxes.each(function () {
                        const row = $(this).closest("tr");
                        commonTable.row(row).deselect();
                    });
                    tableCard.find(".custom-table-actions-button").hide();
                }
            });
        }

        const tableActionsButton = tableCard.find(".custom-table-actions-button");
        if (settings.multiSelect && tableActionsButton.length) {
            tableActionsButton.on("click", function () {
                const selectedRows = commonTable.rows({ selected: true });
                const selectedData = selectedRows.nodes().toArray();
                const selectedIds = selectedData.map((row) => {
                    return $(row).find("input[type='checkbox']").val();
                });

                if (selectedIds.length) {
                    const actionButton = $(this);
                    const url = actionButton.data("url");
                    const displayedText = actionButton.data("text");
                    const modalType = actionButton.data("modal-type");
                    const formUrl = actionButton.data("form-url");
                    const csrfToken = $(
                        "input[name=csrfmiddlewaretoken]"
                    ).val();
                    const basePayload = {
                        selected_ids: selectedIds,
                        csrfmiddlewaretoken: csrfToken,
                    };

                    const bodyContent = formUrl
                        ? (displayedText
                              ? `<p class="mb-2">${displayedText}</p><div id="custom-table-action-form-container">Cargando...</div>`
                              : '<div id="custom-table-action-form-container">Cargando...</div>')
                        : displayedText ||
                          "¿Está seguro que desea realizar esta acción?";

                    const modalHtml = `
                        <div class="modal fade" id="custom-table-action-modal" tabindex="-1" aria-hidden="true">
                            <div class="modal-dialog">
                                <div class="modal-content bg-${modalType || "info"}">
                                    <div class="modal-header">
                                        <h5 class="modal-title">Confirmar acción</h5>
                                        <button type="button" class="close" data-dismiss="modal" aria-label="Cerrar">
                                            <span aria-hidden="true">&times;</span>
                                        </button>
                                    </div>
                                    <div class="modal-body">
                                        ${bodyContent}
                                    </div>
                                    <div class="modal-footer">
                                        <button type="button" class="btn btn-secondary" id="cancel-custom-table-action-modal" data-dismiss="modal">Cancelar</button>
                                        <button type="button" class="btn btn-primary" id="confirm-custom-table-action-modal">Confirmar</button>
                                    </div>
                                </div>
                            </div>
                        </div>
                    `;
                    $("body").append(modalHtml);
                    $("#custom-table-action-modal").modal("show");

                    const formContainer = $("#custom-table-action-form-container");
                    if (formUrl && formContainer.length) {
                        $.get(formUrl)
                            .done(function (formHtml) {
                                formContainer.html(formHtml);
                            })
                            .fail(function () {
                                toastr.error("Error al cargar el formulario");
                                $("#custom-table-action-modal").modal("hide");
                                $("#custom-table-action-modal").on(
                                    "hidden.bs.modal",
                                    function () {
                                        $("#custom-table-action-modal").remove();
                                    }
                                );
                            });
                    }

                    $("#cancel-custom-table-action-modal").on("click", function () {
                        $("#custom-table-action-modal").modal("hide");
                        $("#custom-table-action-modal").on(
                            "hidden.bs.modal",
                            function () {
                                $("#custom-table-action-modal").remove();
                            }
                        );
                    });

                    $("#confirm-custom-table-action-modal").on(
                        "click",
                        function () {
                            const confirmBtn = $(this);
                            const modalForm = $("#custom-table-action-modal form");
                            let postData;
                            if (modalForm.length) {
                                const formSerialized = modalForm.serialize();
                                const extraParams = $.param({
                                    selected_ids: selectedIds,
                                    csrfmiddlewaretoken: csrfToken,
                                });
                                postData =
                                    formSerialized +
                                    (formSerialized ? "&" : "") +
                                    extraParams;
                            } else {
                                postData = basePayload;
                            }

                            $("#custom-table-action-modal").modal("hide");
                            confirmBtn.prop("disabled", true);
                            confirmBtn.text("Procesando...");

                            $.ajax({
                                url: url,
                                type: "POST",
                                data: postData,
                                success: function (response) {
                                    $("#custom-table-action-modal").on(
                                        "hidden.bs.modal",
                                        function () {
                                            $("#custom-table-action-modal").remove();
                                        }
                                    );
                                    tableCard.find(".custom-table-actions-button").hide();
                                    $(table_id).find("#select-all-items-checkbox").prop(
                                        "checked",
                                        false
                                    );
                                    $(table_id).find("#select-all-items-checkbox").trigger(
                                        "change"
                                    );

                                    if (response.success) {
                                        commonTable.ajax.reload();
                                        toastr.success(response.message);
                                    } else {
                                        toastr.error(
                                            response.message ||
                                                "Ocurrió un error al realizar la acción"
                                        );
                                    }
                                },
                                error: function () {
                                    toastr.error(
                                        "Ocurrió un error al realizar la acción"
                                    );
                                },
                            });
                        }
                    );
                }
            });
        }

        if (settings.multiSelect) {
            $(table_id).on("change", "tbody input[type='checkbox']", function () {
                if (
                    $(table_id).find("tbody input[type='checkbox']:checked").length
                ) {
                    tableCard.find(".custom-table-actions-button").show();
                } else {
                    tableCard.find(".custom-table-actions-button").hide();
                }
            });
        }

        $(".table-reloader").on("click", function () {
            commonTable.ajax.reload();
        });

        $(document).on("click", ".table-element-ajax-request", function () {
            $.ajax({
                url: $(this).data("url"),
                type: "POST",
                data: {
                    csrfmiddlewaretoken: $(
                        "input[name=csrfmiddlewaretoken]"
                    ).val(),
                },
                complete: function () {
                    commonTable.ajax.reload();
                },
            });
        });

        return commonTable;
    };

    return {
        init: function (settings) {
            return initTable(settings);
        },
    };
})();
