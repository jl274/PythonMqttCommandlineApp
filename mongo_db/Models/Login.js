const { Schema, model } = require('mongoose');

const loginSchema = new Schema({
    login: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    role: {
        type: String,
        enum: {
            values: ["root", "user"],
            message: '{VALUE} is not supported'
        }

    }
});

module.exports = model('Login', loginSchema);
