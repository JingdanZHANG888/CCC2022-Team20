const express = require('express')

// add our router
const melResultRouter = express.Router()

// require the van controller
const melResultController = require('./melResultController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
melResultRouter.get('/', melResultController.melResult)

// export the router
module.exports = melResultRouter