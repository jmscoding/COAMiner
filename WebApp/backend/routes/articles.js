const express = require('express')
const router = express.Router();

const { getArticles, newArticle, getSingleArticle, updateArticle, deleteArticle } = require('../controllers/articleController')

router.route('/articles').get(getArticles);
router.route('/article/:id').get(getSingleArticle);

router.route('/admin/article/new').post(newArticle);

router.route('/admin/article/:id')
            .put(updateArticle)
            .delete(deleteArticle);



module.exports = router;