function CategoryCreate(e){
    e.preventDefault();
    form = $('#category_form')
    console.log(form)
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data){
            form.submit();
        }
    })
};

function GoalCreate(e){
    e.preventDefault();
    form = $('#goal_form')
    $.ajax({
        type: 'POST',
        url: form.attr('action'),
        data: form.serialize(),
        success: function(data){
            form.submit();
        }
    })
};

