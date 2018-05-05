$(document).ready(function(){
    $(".navigation").on('click', function(event) {
          //  event.preventDefault(); // jeszcze nie wiem czy to potrzebne
            var hash = this.hash;
            $('html, body').animate({
                scrollTop: $(hash).offset().top-70
            }, 700, function(){
            });
    });
});