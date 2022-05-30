var form_groups = document.getElementsByClassName('form-group');

for(var i=0; i < form_groups.length; i++) {
    var inp = form_groups[i].getElementsByTagName('input')[0];

    if(inp.required){
        var label = form_groups[i].getElementsByTagName('label')[0]
        label.innerHTML = label.textContent + '*'
        // alert(label);
    }
}
// alert(inputs.length);