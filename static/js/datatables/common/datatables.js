const CommonDataTable = (function () {
    const defaultButtonConfig = {
        pageLength: {
            extend: "pageLength",
            text: "Registros por página",
            className: "btn btn-default",
            options: [10, 25, 50, 100, 500, -1],
            postfix: " entradas",
        },
        copy: {
            extend: "copy",
            className: "btn btn-secondary",
            exportOptions: {
                columns: ":not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        csv: {
            extend: "csv",
            className: "btn btn-info",
            exportOptions: {
                columns: ":not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        excel: {
            extend: "excel",
            className: "btn btn-success",
            exportOptions: {
                columns: ":not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
        pdf: {
            extend: "pdf",
            className: "btn btn-danger",
            exportOptions: {
                columns: ":not(:last-child)",
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
                columns: ":not(:last-child)",
                modifier: {
                    page: "all",
                },
            },
        },
    };

    const initTable = function (settings) {
        const table_id = settings.table_id;
        const source_url = settings.source_url;
        const table_filters = {};

        const buttonsConfig = settings.buttonsConfig || {};
        const buttons = Object.keys(defaultButtonConfig).map((buttonKey) => {
            return {
                ...defaultButtonConfig[buttonKey],
                ...buttonsConfig[buttonKey],
            };
        });

        const commonTable = $(table_id).DataTable({
            responsive: true,
            lengthChange: true,
            pageLength: 10,
            lengthMenu: [
                [10, 25, 50, 100, 500, -1],
                [10, 25, 50, 100, 500, "Todos"],
            ],
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

        $(".table-reloader").on("click", function () {
            commonTable.ajax.reload();
        });

        return commonTable;
    };

    return {
        init: function (settings) {
            initTable(settings);
        },
    };
})();
