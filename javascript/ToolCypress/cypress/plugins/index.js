/// <reference types="cypress" />

/**
 * @type {Cypress.PluginConfig}
 */

  console.log(process.env.SENDGRID_HOST);
  console.log(process.env.SENDGRID_USER);
  //console.log(process.env.SENDGRID_PASSWORD);
module.exports = (on, config) => {
    require('cypress-email-results')(on, config, {
      email: ['andriana.vaskiv+cypress1@gmail.com', 'andriana.vaskiv+cypress2@gmail.com'],
      emailOnSuccess: false,
    })
  }