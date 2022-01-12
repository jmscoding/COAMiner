const express = require('express')
const app = express();

app.use(express.json());

// Import all routes
const  articles = require('./routes/articles');

app.use('/api/v1', articles)


module.exports = app