require('dotenv').config()
const db = require('./db.js')

db.query('select * from sensordata limit 3', (error, result, fields) =>{
    const res = result
    console.log('result:', res)
})

db.end()

