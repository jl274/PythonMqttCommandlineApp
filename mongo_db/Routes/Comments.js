const express = require('express');
const router = express.Router();

const Comment = require('../models/Comments');
const Login = require('../models/Login');

router.get('/', async (req, res) => {
    try {

        const comments = await Comment.find({}).populate('login')
        return res.json(comments)

    } catch (err) {
        return res.status(400).json({err})
    }
})

router.post('/', async (req, res) => {
    const { login, text, date } = req.body;
    if (!(login && text) || !([2,3].includes(Object.keys(req.body).length))){
        return res.status(400).json({err: "Invalid body arguments"})
    }
    try {

        const postDate = date ? date : new Date();
        const user = await Login.findOne({login});
        if (!(user)){
            return res.status(404).json({err: "User not found"})
        }
        console.log(user._id)
        const created = await Comment.create({login: user._id, date: postDate, text});
        return res.json(created)

    } catch (err) {
        return res.status(400).json({err})
    }
})

router.patch('/', async (req, res) => {
    const { id, text } = req.body;
    if (!(text) || !([2].includes(Object.keys(req.body).length))){
        return res.status(400).json({err: "Invalid body arguments"})
    }
    try {

        const comment = await Comment.findOne({_id: id})
        comment.text = text;
        await comment.save();
        return res.json(comment)

    } catch (err) {
        return res.status(400).json({err})
    }
})

router.delete('/:id', async (req, res) => {
    const { id } = req.params;

    try {

        const deleted = await Comment.deleteOne({_id: id});
        if (deleted.deletedCount === 0){
            return res.status(404).json({err: "Comment not found"})
        }
        return res.json(id)

    } catch (err) {
        return res.status(400).json({err})
    }
})


module.exports = router;