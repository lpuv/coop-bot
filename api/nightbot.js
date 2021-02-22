const express = require('express');
const fetch = require('node-fetch');
const btoa = require('btoa');
const { catchAsync } = require('../utils');
const router = express.Router();

const CLIENT_ID = process.env.CLIENT_ID;
const CLIENT_SECRET = process.env.CLIENT_SECRET;
const redirect = encodeURIComponent('https://cc-chamber-bot.herokuapp.com/api/nightbot/callback');

router.get('/login', (req, res) => {
  res.redirect(`https://api.nightbot.tv/oauth2/authorize?client_id=${CLIENT_ID}&scope=commands&response_type=code&redirect_uri=${redirect}`);
});

router.get('/callback', catchAsync(async (req, res) => {
  if (!req.query.code) throw new Error('NoCodeProvided');
  const code = req.query.code;
  const creds = btoa(`${CLIENT_ID}:${CLIENT_SECRET}`);
  const response = await fetch(`https://api.nightbot.tv/oauth2/token?grant_type=authorization_code&code=${code}&redirect_uri=${redirect}&client_id=${CLIENT_ID}&client_secret=${CLIENT_SECRET}`,
    {
      method: 'POST',
      //headers: {
      //  Authorization: `Basic ${creds}`,
      //},
    });
  const json = await response.json();
  res.redirect(`/?token=${json.access_token}`);
}));

router.get('/refreshcommand', catchAsync(async (req, res) => {
  const fs = require('fs')
  fsLibrary.readFile('token', (error, txtString) => {

    if (error) throw err;

    const token = txtString.toString()

  })
  const response = await fetch('https://api.nightbot.tv/1/commands',
  {
    method: 'GET',
    headers: {
      Authorization: `Bearer ${token}`
    },
  });
  console.log(response.json())
}));

module.exports = router;
