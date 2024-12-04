$(document).ready(function() {
    $('#verify-email-btn').click(function() {
        var email = $('#email').val();

        $.ajax({
            url: '{% url "verify_email" %}',
            method: 'POST',
            data: {
                email: email,
                csrfmiddlewaretoken: $('input[name="csrfmiddlewaretoken"]').val()
            },
            success: function(response) {
                if (response.status === 'success') {
                    $('#email-feedback').html('<span class="text-success">Email verified!</span>');
                    // Show the password fields once email is verified
                    $('#password-fields').show();
                } else {
                    $('#email-feedback').html('<span class="text-danger">' + response.message + '</span>');
                }
            },
            error: function() {
                $('#email-feedback').html('<span class="text-danger">An error occurred. Please try again.</span>');
            }
        });
    });
});
