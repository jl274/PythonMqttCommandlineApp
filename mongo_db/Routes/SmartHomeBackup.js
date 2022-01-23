const express = require('express');
const router = express.Router();

const Backup = require('../models/SmartHomeBackup');

router.get('/', async (req, res) => {
    try {

        const backup = await Backup.find({});
        if (backup.length == 0){
            return res.status(404).json({err: "No backup in DB"})
        }
        return res.json(backup)

    } catch (err) {
        return res.status(400).json({err})
    }
})

router.post('/', async (req, res) => {
    const { devices } = req.body;
    try {

        const backup = await Backup.create({rooms: Object.keys(devices), devices})
        return res.json(backup)

    } catch (err) {
        return res.status(400).json({err})
    }
})

module.exports = router;