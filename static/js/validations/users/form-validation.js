$(document).ready(function(){
    FormValidation('#main-form', {
        username: {
            required: true,
            maxlength: 150,
        },
        first_name: {
            required: true,
        },
        last_name: {
            required: true,
        },
        email: {
            email: true,
        },
    });
});
