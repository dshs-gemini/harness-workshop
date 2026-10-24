const L = require('./lib');
const N = require('./notes.json');
const pres = L.makePres();
require('./slides_a')(pres, N);
require('./slides_b')(pres, N);
pres.writeFile({ fileName: __dirname + '/온라인클래스룸_교원연수.pptx' }).then(f => console.log('wrote', f));
