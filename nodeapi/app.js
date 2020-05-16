const express = require('express');
const app = express();
const bsv = require('bsv')
app.use(express.json());

app.get('/', (req, res) => {
    res.send('bnoteapi REST API');
});

app.get('/hello/:name', (req, res) => {
    res.send('Hello ' + req.params.name);
});

app.get('/generateaddress', (req, res) => {
    jsondata = generate_address("main")
    res.header('Content-Type', 'application/json; charset=utf-8')
    res.send(jsondata);
});

//envname : test
app.get('/generateaddress/:envname', (req, res) => {
    envname = req.params.envname
    jsondata = generate_address(envname)
    res.header('Content-Type', 'application/json; charset=utf-8')
    res.send(jsondata);
});

//envname : main or test
generate_address = function(envname){
    env = ""
    if(envname == 'test'){
        env = "testnet"
    }
    const privateKey = bsv.PrivateKey.fromRandom(env)
    console.log(privateKey.toWIF())
    const address = bsv.Address.fromPrivateKey(privateKey, env)
    console.log(address.toString())
    return `{ "address" : "${address.toString()}" , "privatekey_wif" : "${privateKey.toWIF()}" }`
}

app.get('/j', (req, res) => {
    res.header('Content-Type', 'application/json; charset=utf-8')
    //jsondata = `{ "address" : ${address.toString()}, "privatekey_wif" : ${privateKey.toWIF()} }`
    res.send('{ "aaaa" : "bbbb" , "aaaa1" : "bbbb" }');
});

// app.get('/api/courses', (req, res) => {
//     res.send(courses);
// });

// app.get('/api/courses/:id', (req, res) => {
//     const course = courses.find(c => c.id === parseInt(req.params.id));
//     if (!course) return res.status(404).send('The course with the given ID was not found.');
//     res.send(course);
// });

// app.get('/api/posts/:year/:month', (req, res) => {
//     res.send(req.query);
// });

// app.post('/api/courses', (req, res) => {
//     const course = {
//         id: courses.length + 1,
//         name: req.body.name
//     };
//     courses.push(course);
//     res.send(course);
// });

// app.put('/api/courses/:id', (req, res) => {
//     const course = courses.find(c => c.id === parseInt(req.params.id));
//     if (!course) return res.status(404).send('The course with the given ID was not found.');

//     course.name = req.body.name;
//     res.send(course);
// });

// app.delete('/api/courses/:id', (req, res) => {
//     const course = courses.find(c => c.id === parseInt(req.params.id));
//     if (!course) return res.status(404).send('The course with the given ID was not found.');

//     const index = courses.indexOf(course);
//     courses.splice(index, 1);

//     res.send(course);
// });


const port = process.env.PORT || 3000;
app.listen(port, () => console.log(`Listening on port ${port}... http://localhost:${port}`));
