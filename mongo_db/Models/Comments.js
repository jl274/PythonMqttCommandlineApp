const { Schema, model } = require('mongoose');

const commentSchema = new Schema({
    login: {
        type: {type: Schema.Types.ObjectId, ref: 'Login'}
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
