const express = require("express");
const exphbs = require('express-handlebars')
const app = express();
const bodyParser = require("body-parser");
app.use(bodyParser.json())


// register handlebars
app.use(express.static('public'))
app.engine('.hbs', exphbs({defaultlayout: 'main', extname: '.hbs'}));
app.set('view engine', '.hbs');

// set up account routes
const testRouter = require("./testRouter");

// GET homepage
app.get('/', function (req, res) {res.render('index',{layout:'main'});});

//Handle customer's homepage request
app.use('/analysis', testRouter)

app.listen(process.env.PORT || 3000, () => {
    console.log('The library app is listening on port 3000...')
})