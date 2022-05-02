const express = require('express')

// add our router
const sydResultRouter = express.Router()

// require the van controller
const sydResultController = require('./sydResultController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
sydResultRouter.get('/', sydResultController.sydResult)

// export the router
module.exports = sydResultRouter