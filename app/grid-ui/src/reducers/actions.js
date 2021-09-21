export const USER_TYPES = {
    SET_EMAIL: 'user/set_email',
    UNSET_EMAIL: 'user/unset_email',
    SET_LEVEL: 'user/set_level'
};

export const addEmail = (email) => {
    return {
        type: USER_TYPES.SET_EMAIL,
        payload: {email: email},
    };
}

export const removeEmail = () => {
    return {
        type: USER_TYPES.UNSET_EMAIL,
    };
}

export const setLevel = (level) => {
    return {
        type: USER_TYPES.SET_LEVEL,
        payload: {level: level}
    };
}