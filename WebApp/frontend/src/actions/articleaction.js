import axios from 'axios';

import { 
    ALL_ARTICLES_REQUEST,
    ALL_ARTICLES_SUCCESS,
    ALL_ARTICLES_FAIL,
    CLEAR_ERRORS
} from '../constants/articleconstants';


export const getArticles = () => async(dispatch) => {
    try {
        dispatch({
            type: ALL_ARTICLES_REQUEST
        })

        const { data } = await axios.get('/api/v1/articles')

        dispatch({
            type: ALL_ARTICLES_SUCCESS,
            payload: data
        })


    } catch(error){
        dispatch({
            type: ALL_ARTICLES_FAIL,
            payload: error.response.data.message
        })
    }
}

// Clear Errors
export const clearErrors = () => async (dispatch) => {
    dispatch({
        type: CLEAR_ERRORS
    })
}
