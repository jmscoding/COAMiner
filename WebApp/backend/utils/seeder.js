const Article = require('../articles/article');
const dotenv = require('dotenv');
const connectDatabase = require('../config/database');

const articles = require('../data/article');
const { connect } = require('mongoose');

// Setting dotenv file
dotenv.config({ path: 'backend/config/config.env'})

connectDatabase();

const seedArticle = async () => {
    try {

        await Article.deleteMany();
        console.log('Articles are deleted');
        
        await Article.insertMany(articles);
        console.log('Articles are added');

        process.exit();


    } catch(error){
        console.log(error.message);
        process.exit();
    }
}

seedArticle();