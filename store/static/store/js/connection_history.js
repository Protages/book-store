var connection_url = `ws://${window.location.host}/ws/socket-server/store/connection/`

const connectionSocket = new WebSocket(connection_url)


connectionSocket.addEventListener('open', (event) => {
    var user_id = document.getElementById('user-id').value
    if(user_id != 'none'){
        var agent = navigator.userAgent
        console.log('Connection open!!!!')
        console.log(agent)
        connectionSocket.send(JSON.stringify({
            'message_type': 'update_user_status',
            'user_id': user_id,
            'agent': agent,
            'status': 'online'
        }))
    }
})

connectionSocket.addEventListener('close', (event) => {
    var user_id = document.getElementById('user-id').value
    if(!user_id=='none'){
        var agent = navigator.userAgent
        console.log('Connection open!!!!')
        console.log(agent)
        connectionSocket.send(JSON.stringify({
            'message_type': 'update_user_status',
            'user_id': user_id,
            'agent': agent,
            'status': 'offline'
        }))
    }
})