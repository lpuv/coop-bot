const express = require('express');
const path = require('path');
const pg = require('pg');
const R = require('ramda')


const app = express();

app.get('/', (req, res) => {
  var currentChamber;

  var pgClient = new pg.Client(process.env.DATABASE_URL);
  pgClient.connect(); 

  var query = pgClient.query("SELECT index from CURRENTCHAMBER;").then(res => {

    const result = R.head(R.values(R.head(res.rows)));

    var query2 = pgClient.query("SELECT name FROM CHAMBERS WHERE index=" + result + ";").then(res => {   

      var currentChamber = res.rows[0]
  
      //console.log(result);
  }).finally(() => pgClient.end());

    //console.log(result);
}).finally(() => pgClient.end());

  res.status(200).send(currentChamber) /*sendFile(path.join(__dirname, 'index.html'));*/
  //const fsLibrary  = require('fs')
//  if (req.query.token) {
//    let data = req.query.token
//    fsLibrary.writeFile('token.txt', data, (error) => {

      // In case of a error throw err exception.
//      if (error) throw err;
  //  })
  //}
});

app.listen(process.env.PORT, () => {
  console.info('Running on port ' + process.env.PORT);
});

//app.use('/api/nightbot', require('./api/nightbot'))



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
