function follow(name, iteration) {
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (xhttp.readyState == 4 && xhttp.status == 200) {
            if (xhttp.responseText == 'ok') {
                var id = '#suggestion' + iteration
                $(id).css('display', 'none')
            } else {
                alert('error occurred')
            }
        }
    }
    xhttp.open('GET', 'follow?name=' + name, true)
    xhttp.send()
}
