const mysql = require('mysql');
const config = require('../utils/config')
const logger = require('../utils/logger')

const connection = mysql.createConnection({
  host: config.DB_HOST,
  port: config.DB_PORT,
  database: config.DB_DATABASE,
  user: config.DB_USER,
  password: config.DB_PASSWORD,
  dateStrings: true
})

connection.connect((err) => {
  if (err) {
    logger.error('error connecting: ' + err.stack);
    return;
  }
  logger.info('connected as id ' + connection.threadId);
});

module.exports = connection