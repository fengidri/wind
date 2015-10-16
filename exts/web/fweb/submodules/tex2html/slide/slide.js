$(document).ready(function()
{
    set_pos();
    $('body').keypress(function(event){
        event.preventDefault();
        console.log(event.keyCode)
        if (32 == event.keyCode)
        {
            page(1);
            //event.returnValue = false;
        }else if (40 == event.keyCode)
        {
            page(1);
        }else if (28 == event.keyCode)
        {
            page(-1);
        }
    });
})
function page(p)
{
    var offset = $(document).scrollTop()
    var n_n = offset/document.body.clientHeight;
    var n = Math.floor(n_n);
    if (n_n - n > 0.3)
    {
        n = n + 1;
    }
    n = n + p;
    $(document).scrollTop(document.body.clientHeight * n);

}
function set_pos()
{

    var nodes =  $('body > *');
    var slides = [];
    for (var i in nodes)
    {
        var nodeName = nodes[i].nodeName;
        if ('H3' != nodeName && 'H4' != nodeName)
            continue;
        slides.push(nodes[i])
    }
    var index;
    for (index in slides)
    {
        index = index * 1;
        handle(index, slides[index], slides[index + 1]);
    }

    var n = document.body.scrollHeight - document.body.clientHeight * (1*index + 1);
    if (n < 0)
    {
        $('body').append(get_space(-1 *n));
    }

}

function handle(index, target, next)
{
    var target = $(target);
    var next_top;
    if (undefined == next)
    {
        next_top = document.body.scrollHeight;
    }
    else
    {
        next_top = $(next).offset().top;
    }
    var height = document.body.clientHeight - next_top + target.offset().top;

    var target_top = document.body.clientHeight * index + height * 0.4;

    set_top_pos(target, target_top);
}

function set_top_pos(obj, target_top)
{
    var obj_top = obj.offset().top
    var space = get_space(target_top - obj_top);
    obj.before(space);
}

function get_space(h)
{
    var space = $('<div>')
    space.css('margin', 0);
    space.css('padding', 0);
    space.css('border', 'None');
    space.css('height', h);
    return space;
}
