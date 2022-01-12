const mongoose = require('mongoose')


const articleSchema = new mongoose.Schema({
    title: {
        type: String,
        required: [true, 'Title']
    },
    text: {type: String},
    createdAt: {
        type: Date,
        default: Date.now
    }

});

module.exports = mongoose.model('Article', articleSchema);