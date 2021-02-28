require('dotenv').config();

module.exports = {
  localDomain: process.env.LOCAL_DOMAIN || 'local',
  spotify: {
    clientId: process.env.SPOTIFY_CLIENT_ID,
  },
};
