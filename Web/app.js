//
// Part of COMP90024 Cluster and Cloud Computing from The University of Melbourne 
//
// Assignment 2 - Team 20
//
// Collective Team Details (Member's Name/Student ID/Location): 
//
//  * Cenxi Si 1052447 China
//  * Yipei Liu 1067990 China
//  * Jingdan Zhang 1054101 China
//  * Chengyan Dai 1054219 Melbourne
//  * Ruimin Sun 1052182 China
//


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
const melResultRouter = require("./melResultRouter");
const sydResultRouter = require("./sydResultRouter");

// GET homepage
//app.get('/', function (req, res) {res.render('index',{layout:'main'});});
app.use('/',melResultRouter)
//app.get('/sydmap', function (req, res) {res.render('syd_index',{layout:'main'});});
app.use('/sydmap',sydResultRouter)
app.get('/member', function (req, res) {res.render('member',{layout:'main'});});
//Handle customer's homepage request
app.use('/analysis', function (req, res) {res.render('analysis',{layout:'main'});});

//Handle customer's homepage request
app.use('/wordCloud', function (req, res) {res.render('wordCloud',{layout:'main'});});

app.listen(process.env.PORT || 3000, '0.0.0.0', () => {
    console.log('The library app is listening on port 3000...')
});
