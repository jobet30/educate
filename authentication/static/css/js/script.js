// static/js/ajax.js

$(document).ready(function () {
    function checkPasswordStrength(password) {
        let strength = 0;
        if (password.length >= 8) strength++;
        if (/[A-Z]/.test(password)) strength++;
        if (/[a-z]/.test(password)) strength++;
        if (/\d/.test(password)) strength++;
        if (/[^A-Za-z0-9]/.test(password)) strength++;

        if (strength < 3) {
            $('#password-strength').html('<div class="alert alert-warning">Weak password. Try adding more complexity.</div>');
        } else if (strength === 3) {
            $('#password-strength').html('<div class="alert alert-info">Moderate password. Good, but can be improved.</div>');
        } else {
            $('#password-strength').html('<div class="alert alert-success">Strong password!</div>');
        }
    }

    $('input[name="password1"]').on('input', function () {
        const password = $(this).val();
        checkPasswordStrength(password);
    });

    $('#registration-form').on('submit', function (e) {
        e.preventDefault(); // Prevent the form from submitting the traditional way

        const formData = $(this).serialize(); // Serialize the form data
        $('#loading-indicator').show(); // Show loading indicator
        $('#response-message').empty(); // Clear previous messages

        $.ajax({
            type: 'POST',
            url: '/register/', // Adjust this URL based on your Django view
            data: formData,
            dataType: 'json', // Expect JSON response
            success: function (response) {
                $('#loading-indicator').hide(); // Hide loading indicator

                if (response.success) {
                    $('#response-message').html(
                        `<div class="alert alert-success">${response.message}</div>`
                    );
                    $('#registration-form')[0].reset(); // Reset the form
                    $('#password-strength').empty(); // Clear password strength feedback
                } else {
                    // Loop through error messages and display them
                    let errorMessage = '<div class="alert alert-warning"><ul>';
                    response.errors.forEach(function (error) {
                        errorMessage += `<li>${error}</li>`;
                    });
                    errorMessage += '</ul></div>';
                    $('#response-message').html(errorMessage);
                }
            },
            error: function (xhr, status, error) {
                $('#loading-indicator').hide(); // Hide loading indicator
                $('#response-message').html(
                    `<div class="alert alert-danger">An unexpected error occurred: ${xhr.statusText}</div>`
                );
                console.error('AJAX Error:', status, error);
            }
        });
    });

    // Real-time validation for username and email
    $('input[name="username"]').on('input', function () {
        const username = $(this).val();
        if (username.length < 3) {
            $('#username-feedback').html('<div class="alert alert-warning">Username must be at least 3 characters long.</div>');
        } else {
            $.ajax({
                type: 'GET',
                url: '/check-username/', 
                data: { username: username },
                success: function (response) {
                    if (response.available) {
                        $('#username-feedback').html('<div class="alert alert-success">Username is available.</div>');
                    } else {
                        $('#username-feedback').html('<div class="alert alert-warning">Username is already taken.</div>');
                    }
                },
                error: function () {
                    $('#username-feedback').html('<div class="alert alert-danger">Error checking username.</div>');
                }
            });
        }
    });

    $('input[name="email"]').on('input', function () {
        const email = $(this).val();
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(email)) {
            $('#email-feedback').html('<div class="alert alert-warning">Please enter a valid email address.</div>');
        } else {
            $.ajax({
                type: 'GET',
                url: '/check-email/',
                data: { email: email },
                success: function (response) {
                    if (response.available) {
                        $('#email-feedback').html('<div class="alert alert-success">Email is available.</div>');
                    } else {
                        $('#email-feedback').html('<div class="alert alert-warning">Email is already in use.</div>');
                    }
                },
                error: function () {
                    $('#email-feedback').html('<div class="alert alert-danger">Error checking email.</div>');
                }
            });
        }
    });
});
