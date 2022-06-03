var cart_url = `ws://${window.location.host}/ws/socket-server/store/cart/`

const cartSocket = new WebSocket(cart_url)


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