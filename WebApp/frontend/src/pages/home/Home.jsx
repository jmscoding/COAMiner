import React, { useEffect } from 'react'
import FeaturedInfo from "../../components/featuredInfo/FeaturedInfo"
import "./home.css"

import { useDispatch, useSelector } from 'react-redux'
import { getArticles } from '../../actions/articleaction'
import { DataGrid } from '@mui/x-data-grid';

export default function Home(){
    const dispatch = useDispatch();

    const { loading, articles, error, articlesCount } = useSelector(state => state.articles)

    useEffect(() => {
        dispatch(getArticles());  
    }, [dispatch])

    return(
        <div className="home">
            <div className="articles">
                {articles && articles.map(article => (
                    <div key={article._id} className="articlebody">
                        <a>{article.title}</a>
                    </div>
                ))}

            </div>
        </div>
    )
}