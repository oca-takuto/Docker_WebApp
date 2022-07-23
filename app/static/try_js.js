color = "";

function change_table(){
    if(color == "red"){
        color = "blue";
    }else{
        color = "red";
    }
    table_obj = document.getElementById('table_id');
    table_obj.style.backgroundColor = color;
}

function change_select(){
    table_obj = document.getElementById('table_id');

    color = document.getElementById('select_id').value;
    
    table_obj.style.backgroundColor = color;
}
