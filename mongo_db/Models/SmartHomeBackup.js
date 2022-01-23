const { Schema, model } = require('mongoose');

const backupSchema = new Schema({
    rooms: {
        type: [String],
        default: []
    },
    devices: {
        type: Schema.Types.Mixed
    },
    date: {
        type: Date,
        default: new Date()
    }
});

module.exports = model('SmartHomeBackup', backupSchema);
