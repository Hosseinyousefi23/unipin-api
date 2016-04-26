function unfollow(name, index) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            if (xhttp.responseText == 'ok') {
                var id = '#followed' + index
                $(id).css('display', 'none')
            } else {
                alert('error occurred')
            }
        }
    }
    xhttp.open('GET', 'unfollow?name=' + name, true)
    xhttp.send()
}
