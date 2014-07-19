var system = require('system');
var page = require('webpage').create();
var url = system.args[1];
var parser = document.createElement('a');
parser.href = url;

var re = /\//;
var filename = 'snapshots/' + parser.pathname.replace(re, '--') + '.png';

console.log(url + '  -->  '  + filename)
page.open(url, function() {
  page.render(filename);
  phantom.exit();
});
