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






var book_favourites_url = `ws://${window.location.host}/ws/socket-server/store/book_favourites/`
var book_cart_url = `ws://${window.location.host}/ws/socket-server/store/book_cart/`

const favouritesSocket = new WebSocket(book_favourites_url)
const cartSocket = new WebSocket(book_cart_url)


// Favourites books methods

function add_remove_book_favourites(el) {
  var book_id = el.id

  favouritesSocket.send(JSON.stringify({
    'message_type': 'add_remove_book_favourites',
    'book_id': book_id
  }))

  el.classList.toggle('in_favourites')
  if(el.classList.contains('in_favourites')) {
    el.innerHTML = 'В избранном'
  }
  else {
    el.innerHTML = 'В избранное'
  }
}

function books_in_favourites(element) {
  if(favouritesSocket.readyState) {
    var books = element.getElementsByClassName('book')
    
    favouritesSocket.send(JSON.stringify({
      'message_type': 'books_in_favourites'
    }))
  
    favouritesSocket.onmessage = function (e) {
      var data = JSON.parse(e.data)
      var books_id_set = data['books_id_set']
      for(var i=0; i < books.length; i++) {
        if(books_id_set.includes(parseInt(books[i].id))) {
          var favourites_btn = books[i].getElementsByClassName('favourites')[0].getElementsByTagName('span')[0]
          favourites_btn.classList.add('in_favourites')
          favourites_btn.innerHTML = 'В избранном'
        }
      }
    }
    
  }
  else {
    setTimeout(function() {
      books_in_favourites(element)
    }, 50)
  }
}


// Cart books methods

function add_remove_book_cart(el) {
  var book_id = el.id

  if(el.classList.contains('in_cart')) {
    el.setAttribute('href', '/profile/cart/')
  }

  if(!el.classList.contains('in_cart')) {
    console.log('Send book_id to add book in user cart!')
    cartSocket.send(JSON.stringify({
      'message_type': 'add_remove_book_cart',
      'book_id': book_id
    }))
  }

  el.classList.add('in_cart')
  el.getElementsByTagName('span')[0].innerHTML = 'Оформить'
}

function books_in_cart(element) {
  if(cartSocket.readyState) {
    var books = element.getElementsByClassName('book')
    
    cartSocket.send(JSON.stringify({
      'message_type': 'books_in_cart'
    }))
  
    cartSocket.onmessage = function (e) {
      var data = JSON.parse(e.data)
      var books_id_set = data['books_id_set']
      for(var i=0; i < books.length; i++) {
        if(books_id_set.includes(parseInt(books[i].id))) {
          var buy_btn = books[i].getElementsByClassName('btn-buy-authenticated')[0]
          buy_btn.classList.add('in_cart')
          buy_btn.getElementsByTagName('span')[0].innerHTML = 'Оформить'
        }
      }
    }
    
  }
  else {
    setTimeout(function() {
      books_in_cart(element)
    }, 50)
  }
}


if(document.getElementsByClassName('books').length > 0) {
  console.log('We have books element on the page!')
  var books_element = document.getElementsByClassName('books')[0]
  books_in_favourites(books_element)
  books_in_cart(books_element)
}


// User profile cart methods

function activate_deactivate_position(el) {
  var position_el = el.parentElement
  var position_id = position_el.id
  
  if(el.checked) {
    console.log('We activate ' ,el.checked)
    cartSocket.send(JSON.stringify({
      'message_type': 'activate_position',
      'position_id': position_id
    }))
  }
  else {
    console.log('We deactivate ' ,el.checked)
    cartSocket.send(JSON.stringify({
      'message_type': 'deactivate_position',
      'position_id': position_id
    }))
  }
  

  calculate_total_price()
}

function minus_book_count(el) {
  var position_el = document.getElementById(el.id)
  var count_input_el = position_el.getElementsByClassName('count-input')[0]
  var count = parseInt(count_input_el.value)
  
  if(count > 1) {
    var price_el = position_el.getElementsByClassName('price-rub')[0]
    var price = parseInt(price_el.textContent) / count

    count = count - 1
    count_input_el.value = count
    price_el.innerHTML = (price * count).toString()

    var price_count_el = position_el.getElementsByClassName('price-count')[0]
    price_count_el.innerHTML = `за ${count}шт.`

    calculate_total_price()

    cartSocket.send(JSON.stringify({
      'message_type': 'minus_book_count',
      'position_id': el.id
    }))
  }
}

function plus_book_count(el) {
  var position_el = document.getElementById(el.id)
  var count_input_el = position_el.getElementsByClassName('count-input')[0]
  var count = parseInt(count_input_el.value)

  var price_el = position_el.getElementsByClassName('price-rub')[0]
  var price = parseInt(price_el.textContent) / count

  count = count + 1
  count_input_el.value = count
  price_el.innerHTML = (price * count).toString()

  var price_count_el = position_el.getElementsByClassName('price-count')[0]
  price_count_el.innerHTML = `за ${count}шт.`

  calculate_total_price()

  cartSocket.send(JSON.stringify({
    'message_type': 'plus_book_count',
    'position_id': el.id
  }))
}

function remove_position_from_cart(el) {
  var position_el = document.getElementById(el.id)
  var position_checkbox_el = position_el.getElementsByClassName('position-checkbox')[0]
  position_checkbox_el.checked = false
  position_el.style = 'display: none;'
  var recover_el = document.getElementById(`recover-for-${el.id}`)
  recover_el.style = 'display: inline-block;'

  calculate_total_price()

  cartSocket.send(JSON.stringify({
    'message_type': 'remove_position_from_cart',
    'position_id': el.id
  }))
}

function recover_position_from_cart(el) {
  var position_id = el.id.split('-')[2]
  var position_el = document.getElementById(position_id)
  var position_checkbox_el = position_el.getElementsByClassName('position-checkbox')[0]
  position_checkbox_el.checked = true
  position_el.style = 'display: block;'
  var recover_el = document.getElementById(`recover-for-${position_id}`)
  recover_el.style = 'display: none;'

  var book_id = position_checkbox_el.value
  var count = position_el.getElementsByClassName('count-input')[0].value

  calculate_total_price()

  cartSocket.send(JSON.stringify({
    'message_type': 'recover_position_from_cart',
    'book_id': book_id,
    'count': count
  }))

  document.location.reload()
}

function calculate_total_price() {
  var positions = document.getElementsByClassName('position')
  var total_price = 0
  for(var i=0; i < positions.length; i++) {
    var position_checkbox_el = positions[i].getElementsByClassName('position-checkbox')[0]
    if(position_checkbox_el.checked) {
      var price_el = positions[i].getElementsByClassName('price-rub')[0]
      var price = parseInt(price_el.textContent)
      total_price = total_price + price
    }
  }
  var total_price_el = document.getElementById('total-price')
  total_price_el.innerHTML = `Общая цена: ${total_price}`
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