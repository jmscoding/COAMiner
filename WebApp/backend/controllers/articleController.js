const { response } = require('express');
const { accepts } = require('express/lib/request');
const Article = require('../articles/article')

// create a new article => /api/v1/article/new
exports.newArticle = async(req, res, next) => {
    const article = await Article.create(req.body);

    res.status(201).json({
        success: true,
        article
    })
}


// Get all articles => /api/v1/articles
exports.getArticles = async (req, res, next) => {

    const articles = await Article.find();
    const articlesCount = await Article.countDocuments();


    res.status(200).json({
        success: true,
        articlesCount,
        articles
    })
}


// Get single Article  => /api/v1/article/:id

exports.getSingleArticle = async (req, res, next) =>{
    const article = await Article.findById(req.params.id);

    if(!article){
        return res.status(404).json({
            success: false,
            message: 'Article not found'
        })
    }

    res.status(200).json({
        success: true,
        article
    })

}

// Update Article => /api/v1/admin/article/:id
exports.updateArticle = async (req, res, next) => {

    let article = await Article.findById(req.params.id);

    if(!article){
        return res.status(404).json({
            success: false,
            message: 'Article not found'
        })
    }

    article = await Article.findByIdAndUpdate(req.params.id, req.body, {
        new: true,
        runValidators: true,
        useFindAndModify: false
    });

    res.status(200).json({
        success: true,
        article
    })

}


// Delete Article => /api/v1/admin/article/:id
exports.deleteArticle = async (req, res, next) => {
    
    const article = await Article.findById(req.params.id);

    if(!article){
        return res.status(404).json({
            success: false,
            message: 'Article not found'
        })
    }

    await article.remove();

    res.status(200).json({
        success: true,
        message: 'Article is deleted'
    })
}

