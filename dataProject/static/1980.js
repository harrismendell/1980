$(function() {
    $('.menuitem').each(function() {
        if(window.location.pathname == $(this).find('a').attr('href')){
            $(this).addClass('active');
        }
    });

    //Courtesy of http://bootsnipp.com/snippets/featured/thumbnail-caption-hover-effect
    $('.shopthumbnail').hover(
        function(){
            $(this).find('.caption').slideDown(300);
        },
        function(){
            $(this).find('.caption').slideUp(300);
        }
);

});

function validateForm() {
    var x = document.forms["signup"]["username"].value;
    var y = document.forms["signup"]["password"].value;
    var z = document.forms["signup"]["retype"].value;

    if (x == null || x == "") {
        alert("Name must be filled out");
        return false;
    }
    if (x.length < 6) {
        alert("Name must be at least 6 characters");
        return false;
    }
    if (y.length < 6) {
        alert("Password must be at least 6 characters");
        return false;
    }

    if (y != z){
        alert("Passwords must match");
        return false;
    }
}


