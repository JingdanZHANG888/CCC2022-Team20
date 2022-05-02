const express = require("express");
const exphbs = require('express-handlebars')
const app = express();
const bodyParser = require("body-parser");
const path = require('path');
app.use(bodyParser.json())


// register handlebars
//app.use(express.static('public'))
app.use(express.static(path.join(__dirname,'../frontend/public')))
app.engine('.hbs', exphbs({defaultlayout: '../../../frontend/views/layouts/main', extname: '.hbs'}));
app.set('view engine', '.hbs');

// set up account routes
const melResultRouter = require("./melResultRouter");
const sydResultRouter = require("./sydResultRouter");

// GET homepage
//app.get('/', function (req, res) {res.render('index',{layout:'main'});});
app.use('/',melResultRouter)
//app.get('/sydmap', function (req, res) {res.render('syd_index',{layout:'main'});});
app.use('/sydmap',sydResultRouter)
app.get('/member', function (req, res) {res.render('../../frontend/views/member',{layout:'../../../frontend/views/layouts/main'});});
//Handle customer's homepage request
app.use('/analysis', function (req, res) {res.render('../../frontend/views/analysis',{layout:'../../../frontend/views/layouts/main'});});

//Handle customer's homepage request
app.use('/wordCloud', function (req, res) {res.render('../../frontend/views/wordCloud',{layout:'../../../frontend/views/layouts/main'});});

app.listen(process.env.PORT || 3000, () => {
    console.log('The library app is listening on port 3000...')
})