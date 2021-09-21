import { USER_TYPES } from './actions';

const initialState = {
    email: '',
    currentLevel: 0.1
};

const userReducer = (state = initialState, action ) => {
    switch(action.type) {
        case USER_TYPES.SET_EMAIL: return {
            ...state,
            email: action.payload.email,
        };
        case USER_TYPES.UNSET_EMAIL: return {
            ...state,
            email: '',
        };
        case USER_TYPES.SET_LEVEL: return {
            ...state,
            currentLevel: action.payload.level
        }
        default: return state;
    }
}

export default userReducer;