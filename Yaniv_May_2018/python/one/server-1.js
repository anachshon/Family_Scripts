
const http = require( 'http' );
const url = require( 'url' );
const fs = require( 'fs' );
const net = require('net');

http.createServer((request, response) => {

    //console.log( request )
    var queryData = url.parse(request.url, true).query;
    cmd = queryData.command;
    if ( cmd == 'sendmail' )
        arg = queryData.mail
    else
        arg = ''
    if ( cmd != null && cmd != '' )
    {
        send_tcp( cmd, arg );
        console.log( 'Command : ' + queryData.command );
    }
//        console.log( queryData.mail );

  fs.readFile('ex1.html', function(err, data) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(data);
    response.end();
})
}).listen(1337);

function send_tcp( cmd, arg )
{
    var client = new net.Socket();
    client.connect( 10000, '127.0.0.1', function() {
        console.log('Connected');
        if ( arg != '' )
            client.write( cmd + '&' + arg );
        else
            client.write( cmd );
    });
    client.on('data', function(data) {
	    console.log('Received: ' + data);
	    client.destroy();
    });
}