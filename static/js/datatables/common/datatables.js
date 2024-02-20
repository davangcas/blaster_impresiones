const CommonDataTable = (function () {
    const initTable = function (settings) {
        const table_id = settings.table_id;
        const source_url = settings.source_url;
        const commonTable = $(table_id).DataTable({
            responsive: true,
            lengthChange: false,
            autoWidth: false,
            paging: true,
            processing: true,
            serverSide: false,
            searching: true,
            ordering: true,
            info: true,
            deferRender: true,
            buttons: [
                { extend: "copy", className: "btn btn-secondary" },
                { extend: "csv", className: "btn btn-info" },
                { extend: "excel", className: "btn btn-success" },
                { extend: "pdf", className: "btn btn-danger" },
                { extend: "print", className: "btn btn-gray" },
                { extend: "colvis", className: "btn btn-warning" },
            ],
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
                type: "POST",
                dataSrc: "data",
                data: {
                    csrfmiddlewaretoken: $(
                        "input[name=csrfmiddlewaretoken]"
                    ).val(),
                },
            },
            columns: settings.columns,
            columnDefs: settings.columnDefs,
        });
        return commonTable;
    };

    return {
        init: function (settings) {
            initTable(settings);
        },
        buttonsRender: function (table_id) {
            $(table_id).on("draw.dt", function () {
                $(table_id)
                    .DataTable()
                    .buttons()
                    .container()
                    .appendTo($(`${table_id}_wrapper .col-md-6:eq(0)`));
            });
        },
    };
})();
