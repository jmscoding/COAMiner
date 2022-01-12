import { 
    ALL_ARTICLES_REQUEST,
    ALL_ARTICLES_SUCCESS,
    ALL_ARTICLES_FAIL,
    CLEAR_ERRORS
} from '../constants/articleconstants';

export const articlesReducer = (state = { articles: [] }, action) => {
    switch(action.type){
        case ALL_ARTICLES_REQUEST:
            return{
                loading: true,
                articles: []
            }
        case ALL_ARTICLES_SUCCESS:
            return{
                loading: false,
                articles: action.payload.articles,
                articlesCount: action.payload.articles.articlesCount
        }
        case ALL_ARTICLES_FAIL:
            return {
                loading: false,
                error: action.payload
            }
        case CLEAR_ERRORS:
            return {
                ...state,
                error: null
            }

        default:
            return state;
    }

}