const express = require('express')
const db = require('./db')

const app = express()
app.use(require('body-parser').json())

app.get('/', (req, res) => {
    res.send([
      '<h1>ECE DevOps Chat</h1>'
    ].join(''))
  })