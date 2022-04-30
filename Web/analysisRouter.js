const express = require('express')

// add our router
const analysisRouter = express.Router()

// require the van controller
const analysisController = require('./analysisController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
analysisRouter.get('/', analysisController.analysis)

// export the router
module.exports = analysisRouter