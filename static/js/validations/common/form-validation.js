$.validator.setDefaults({
    dateFormat: "dd/mm/yyyy",
});

const FormValidation = (form_id, rules, messages) => {
    $(form_id).validate({
        rules: rules,
        messages: messages,
        errorElement: "span",
        errorPlacement: function (error, element) {
            error.addClass("invalid-feedback");
            if (element.hasClass("date")) {
                error.insertAfter(element.parent());
            } else if (element.hasClass("select2")) {
                error.insertAfter(element.next("span"));
            } else if (element.hasClass("timeinput")) {
                error.insertAfter(element.parent());
            } else {
                error.insertAfter(element);
            }
        },
        highlight: function (element, errorClass, validClass) {
            $(element).addClass("is-invalid");
        },
        unhighlight: function (element, errorClass, validClass) {
            $(element).removeClass("is-invalid");
        },
        submitHandler: function (form) {
            form.submit();
        },
    });
};
