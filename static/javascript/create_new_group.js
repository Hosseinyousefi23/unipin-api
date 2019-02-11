function readURL(input) {
    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('#profile_img')
                .attr('src', e.target.result);
        };

        reader.readAsDataURL(input.files[0]);
    }
}

function showFileChooser() {
    $('#upload_image').click();
}

function activeCheckboxesOnClick(element) {
    var e = $(element);
    var x = $('input[name=' + e.prop('name') + ']');

    x.prop('checked', !x.prop('checked'));

    if(x.prop('checked'))
        e.css('border', '10px solid');

    else
        e.css('border', '0');
}