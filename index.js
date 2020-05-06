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
    const sql = `SELECT * FROM (SELECT dtg, temperature, humidity FROM ${config.DB_TABLE} ORDER BY dtg DESC LIMIT 1446) AS output ORDER BY dtg ASC`
    db.query(sql, (error, result) => {
        if (error) throw error
        response.json(result)
    })
})

app.get('api/alldata', (request, response) => {
    const sql = `SELECT * FROM ${config.DB_TABLE} ORDER BY dtg ASC`
    db.query(sql, (error, result) => {
        if (error) throw error
        response.json(result)
    })
})

app.get('/info', (request, response) => {
    const sql = `SELECT * FROM ${config.DB_TABLE} ORDER BY dtg ASC`
    db.query(sql, (error, result) => {
        if (error) throw error

        const first_day = result[0].dtg.split(' ')[0]
        const last_day = result[result.length - 1].dtg.split(' ')[0]
        const noSamples = result.length

        const info = [{
            total_measurements: noSamples,
            first_day_of_measurements: first_day,
            last_day_of_measurements: last_day
        }]

        response.json(info)
    })
})


app.listen(config.PORT, () => {
    logger.info(`Server running on port ${config.PORT}`)
})