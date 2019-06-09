
const http = require( 'http' );
const url = require( 'url' );
const fs = require( 'fs' );

http.createServer((request, response) => {

    //console.log( request )
    var queryData = url.parse(request.url, true).query;
    console.log( queryData );

  fs.readFile('ex1.html', function(err, data) {
    response.writeHead(200, {'Content-Type': 'text/html'});
    response.write(data);
    response.end();
})
}).listen(1337);