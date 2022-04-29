const express = require('express')

// add our router
const testRouter = express.Router()

// require the van controller
const testController = require('./testController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
testRouter.get('/', testController.test)

// export the router
module.exports = testRouter