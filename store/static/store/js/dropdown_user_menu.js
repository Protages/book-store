var open_menu = document.getElementsByClassName('open-menu')[0]

open_menu.onclick = function() {
  document.getElementById('dropdown-user-menu').classList.toggle('open')
}

window.onclick = function (event) {
  if (!event.target.matches('.open-menu')) {
    var dropdowns = document.getElementsByClassName('dropdown-menu')
    var i
    for (i = 0; i < dropdowns.length; i++) {
      var openDropdown = dropdowns[i]
      if (openDropdown.classList.contains('open')) {
        openDropdown.classList.remove('open')
      }
    }
  }
}

// favouritesSocket.onclose = function(event) {
//   if (event.wasClean) {
//     alert(`[close] Соединение закрыто чисто, код=${event.code} причина=${event.reason}`);
//   } else {
//     // например, сервер убил процесс или сеть недоступна
//     // обычно в этом случае event.code 1006
//     alert('[close] Соединение прервано');
//   }
// };