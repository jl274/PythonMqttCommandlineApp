const { Schema, model } = require('mongoose');

const commentSchema = new Schema({
    login: {
        type: Schema.Types.ObjectId, ref: 'Login', required: true
    },
    date: {
        type: Date,
        default: new Date()
    },
    text: {
        type: String,
        required: true,
        min: 5
    }
});

module.exports = model('Comment', commentSchema);
