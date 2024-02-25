$(function() {
    $(".alerts-resolved").next().hide();
    $(".alerts-resolved").click(function() {
        $(this).find(".fas").toggleClass("fa-chevron-up fa-chevron-down");
        $(this).next().slideToggle();
    });
});