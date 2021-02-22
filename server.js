const express = require('express');
const path = require('path');

const app = express();

app.get('/', (req, res) => {
  res.status(200).sendFile(path.join(__dirname, 'index.html'));
  const fsLibrary  = require('fs')
  if (req.query.token) {
    let data = req.query.token
    fsLibrary.writeFile('token.txt', data, (error) => {

      // In case of a error throw err exception.
      if (error) throw err;
    })
  }
});

app.listen(process.env.PORT, () => {
  console.info('Running on port ' + process.env.PORT);
});

app.use('/api/nightbot', require('./api/nightbot'))



app.use((err, req, res, next) => {
  switch (err.message) {
    case 'NoCodeProvided':
      return res.status(400).send({
        status: 'ERROR',
        error: err.message,
      });
    default:
      return res.status(500).send({
        status: 'ERROR',
        error: err.message,
      });
  }
});
