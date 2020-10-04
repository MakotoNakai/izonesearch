
$(document).ready(function(){
    $('select[name="name"]').change(function(){
            localStorage.setItem('selected_name', $(this).val());
            $('select[name="name"]').value(localStorage.getItem('selected_name'));
    });
});







