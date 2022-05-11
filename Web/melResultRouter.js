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


const express = require('express')

// add our router
const melResultRouter = express.Router()

// require the van controller
const melResultController = require('./melResultController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
melResultRouter.get('/', melResultController.melResult)

// export the router
module.exports = melResultRouter
