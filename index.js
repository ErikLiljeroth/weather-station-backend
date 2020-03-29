require('dotenv').config()
const config = require('./utils/config')
const logger = require('./utils/logger')
const express = require('express')
const app = express()
const cors = require('cors')
const db = require('./db/db.js')
app.use(express.static('build'))
app.use(cors())
app.use(express.json())

app.get('/api/data', (request, response) => {
    const sql = `SELECT dtg, temperature, humidity FROM ${config.DB_TABLE} ORDER BY dtg DESC LIMIT 1446`
    db.query(sql, (error, result) => {
        if (error) throw error
        response.json(result)
    })
})

app.listen(config.PORT, () => {
    logger.info(`Server running on port ${config.PORT}`)
})