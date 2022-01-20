const express = require('express');
const router = express.Router();

const Login = require('../models/Login');

router.get('/', async (req, res) => {
    try {

        const logins_array = []
        const logins = await Login.find({})
        logins.forEach((user) => logins_array.push(`${user.login} (${user.role})`));
        return res.json(logins_array)

    } catch (err) {
        return res.status(500).json({err})
    }
})

router.get('/:login', async (req, res) => {
    const { login } = req.params;
    const { password } = req.body;
    if (!(password) || Object.keys(req.body).length !== 1){
        return res.status(400).json({err: "Invalid arguments"})
    }
    try {

        const result = await Login.findOne({login});
        if (!(result)){
            return res.status(404).json({err: "Login not found"});
        }
        const logged = result.password === password
        return res.json({logged, role: result.role})

    } catch (err) {
        return res.status(500).json({err})
    }
})


router.post('/', async (req, res) => {
    const {login, password, role} = req.body;
    if (!(login && password && role) || Object.keys(req.body).length !== 3){
        return res.status(400).json({err: "Invalid arguments"})
    }
    try {

        const created = await Login.create({login, password, role})
        return res.json(created)

    } catch (err) {
        return res.status(500).json({err})
    }
})

module.exports = router;