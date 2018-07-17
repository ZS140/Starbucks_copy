/**
 * Created by 冯周 on 2018/6/22.
 */
$(document).ready(function() {
    $(function () {
        $('.carousel').carousel({
            interval: 2000
        })
    });
    //控制子菜单隐藏显示
    var num;
    $('.nav-main>li[id]').hover(function(){
        var Obj = $(this).attr('id');
        num = Obj.substring(3, Obj.length);
        $('#box-'+num).slideDown(300);
    },function(){
        $('#box-'+num).hide();
    });
    $('.hidden-box').hover(function () {
        $(this).show();
    },function () {
        $(this).slideUp(200);
    });

    var n;
    $('.img').hover(function() {
        var Obj = $(this).attr('id');
        n = Obj.substring(4,Obj.length);
        $('#tag-'+n).animate({left:'toggle',transition: 'all 0.5s'},350);
    });


});
function pageScroll() {
    window.scrollBy(0,-10);
    scrolldelay=setTimeout("pageScroll()",100);
    if (document.documentElement.scrollTop===0){
        clearTimeout(scrolldelay);

    }

}