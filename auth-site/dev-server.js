const path = require('path');
const express = require('express');
const config = require('./build/get-config');

const app = express();

app.get('/config.json', (req, res) => {
  res.json(config);
});
app.use(express.static('./src'));
app.get('/*', (req, res) => res.sendFile(path.join(__dirname, 'src/index.html')));

app.listen(8080);
