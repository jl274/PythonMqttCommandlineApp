const express = require('express');
const router = express.Router();

const Comment = require('../models/Comments');

router.get('/', async (req, res) => {
    try {

        const comments = await Comment.find({})
        return res.json(comments)

    } catch (err) {
        return res.status(400).json({err})
    }
})


module.exports = router;