
$(document).ready(function() {

    //Uyarılar 3 saniye dolunca gösterilme kapanır
    $('.alert').delay(2000).hide(500);

    //Günlük verimi hesaplayıp ilerleme barını verime göre doldurur
    var total_score = document.getElementById('total_score').innerHTML;
    console.log('Bugünkü verimin: '+total_score+'%')
    var progress_bar = document.getElementById('bar');
    var progress_bar_collapse = document.getElementById('progress')
    progress_bar.style.width = 1+'%';
    var total_score = total_score + '%';
    if (total_score != 0){
        timing = setInterval(frame, 10);
        function frame(){
            if(progress_bar.style.width == total_score){
                clearInterval(timing)
            }
            else if (parseInt(total_score) == 0){
                progress_bar.style.width = '1%';
            }
            else if (parseInt(total_score) > 100){
                clearInterval(timing)
                progress_bar.style.width = '100%';
            }

            else{
                width = progress_bar.style.width
                width = parseInt(width)
                width = 1 + parseInt(width);
                progress_bar.style.width = width + '%';
            }
        }
        progress_bar.style.boxShadow = '0px 0px 20px 5px #4CAF50';
    }
});

function TaskCreateForm(){
    e.preventDefault();
    var form = $('#task_create_form');
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data){
            form.submit();
        }
    });
};

function TaskUpdate(slug){
    $('#done'+slug).modal('show');
};

function TaskUpdateForm(){
    $('#task_update_form').submit(function(e){
        e.preventDefault();
        var form = $(this);
        var url = form.attr('action');
        $.ajax({
            type: 'POST',
            url: url,
            data: form.serialize(),
            success: function(data){
                form.submit();
                location.reload()
            }
        })

    })
};

function TaskDelete(slug){
    $.ajax({
        type: 'GET',
        url: $('#'+slug).attr('url'),
        data: $('#'+slug).serialize(),
        dataType: 'json',
        success: function(data){
            $('#task'+slug).remove();
        }
    })
};



function LetterCountCreate(){
    $('#task_title_input').keyup(function(){
        lettercount = $(this).val().length;
        $('#letters').html(lettercount);
    })
};

function LetterCountUpdate(slug){
    $('#task_title_input'+slug).keyup(function(){
        lettercount = $(this).val().length;
        $('#letters'+slug).html(lettercount);
    })
};




