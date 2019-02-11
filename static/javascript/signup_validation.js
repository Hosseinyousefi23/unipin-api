console.log('script running...');
var username_regex = new RegExp("^[a-z0-9_-]{3,16}$")
var username_field = $('input[name=username]')
var password_field = $('input[name*=password]')

username_field.on('input', function () {
    if (username_field[0].value == '') {
        username_field[0].setAttribute('style', 'border: solid 4px lightgray');
    } else if (username_regex.test(username_field[0].value)) {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function () {
            if (xhttp.readyState == 4 && xhttp.status == 200) {
                if (xhttp.responseText == 'valid') {
                    username_field[0].setAttribute('style', 'border: solid 4px green');
                } else {
                    username_field[0].setAttribute('style', 'border: solid 4px yellow');
                }
            }
        }
        xhttp.open('GET', 'check_username?username=' + username_field[0].value, true)
        xhttp.send()
        username_field[0].setAttribute('style', 'border: solid 4px green');
    } else {
        username_field[0].setAttribute('style', 'border: solid 4px red');
    }
});
password_field.on('input', function () {
    if (password_field[1].value == '') {
        password_field[0].setAttribute('style', 'border: solid 4px lightgray');
        password_field[1].setAttribute('style', 'border: solid 4px lightgray');
    } else if (password_field[1].value != '' && password_field[0].value != password_field[1].value) {
        password_field[0].setAttribute('style', 'border: solid 4px red');
        password_field[1].setAttribute('style', 'border: solid 4px red');
    } else if (password_field[0].value == password_field[1].value) {
        password_field[0].setAttribute('style', 'border: solid 4px green');
        password_field[1].setAttribute('style', 'border: solid 4px green');
    }
});

