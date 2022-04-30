const express = require('express')

// add our router
const wordCloudRouter = express.Router()

// require the van controller
const wordCloudController = require('./wordCloudController.js')

// handle the GET request to obtain the full list of vans (For Customer Web App)
wordCloudRouter.get('/', wordCloudController.wordCloud)

// export the router
module.exports = wordCloudRouter