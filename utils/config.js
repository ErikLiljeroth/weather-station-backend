require('dotenv').config()

let PORT = process.env.PORT
let DB_HOST = process.env.DB_HOST
let DB_PORT = process.env.DB_PORT
let DB_DATABASE = process.env.DB_DATABASE
let DB_TABLE = process.env.DB_TABLE
let DB_USER = process.env.DB_USER
let DB_PASSWORD = process.env.DB_PASSWORD

module.exports = {
  PORT, DB_HOST, DB_PORT, DB_DATABASE, DB_TABLE, DB_USER, DB_PASSWORD
}