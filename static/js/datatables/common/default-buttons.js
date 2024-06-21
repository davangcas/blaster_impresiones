const buttons_config = {
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

const initDatatableComplete = () => {
    console.log("Datatable initialized");
};
