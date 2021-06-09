$(document).ready(function() {


    //Dakika ve Saniye Geri Sayım
    title = $('#title_input').val();
    minute = $('#minute_input').val();
    second = 00;
    rest_minute = $('#rest_m_input').val();
    rest_second = $('#rest_s_input').val();
    pomodoro_work_timing = setInterval(PomodoroWorkTime, 1000)

    function PomodoroWorkTime() {
        $('#pomodoro_title').html(title+"<small class='ml-5'>-Work");
        if (second == 00 && minute > 00) {
            second = 59;
            minute--;
        } 
        else if (second == 00 && minute == 00) {
            clearInterval(pomodoro_work_timing)
            pomodoro_rest_timing = setInterval(PomodoroRestTime, 1000)
            function PomodoroRestTime(){
            $('#pomodoro_title').html(title+"<small class='ml-5'>-Rest");
                if (rest_second==00){
                    rest_second = 59;
                    if (rest_minute > 00){
                        rest_minute--;
                    }
                }
                else{
                    rest_second--;
                }
                if (rest_second==00 && rest_minute==0){
                    clearInterval(pomodoro_rest_timing)
                    location.reload()
                }

                if (rest_minute < 10){
                    $('#minute').html('0' + rest_minute)
                }
                else{
                    $('#minute').html(rest_minute);
                }
                if (rest_second < 10){
                    $('#seconds').html('0' + rest_second);
                }else {
                    $('#seconds').html(rest_second);
                }
            }
        }
        else if (second > 00 && minute > 00){
            second--;
        }
        else if(second > 00 && minute == 00){
            second--;
        }
        if (minute < 10) {
            $('#minute').html('0' + minute);
        } else {
            $('#minute').html(minute);
        }
        if (second < 10) {
            $('#seconds').html('0' + second);
        } else {
            $('#seconds').html(second);
        }
    }
    }
)




function PomodoroCreate(e){
    form = $('pomodoro_create_form');
    form.submit(function(e){
        e.preventDefault();
        $.ajax({
            type: 'POST',
            url: form.attr('action'),
            data: form.serialize(),
            success: function(data){
                form.submit();
            }
        })
    })
}

