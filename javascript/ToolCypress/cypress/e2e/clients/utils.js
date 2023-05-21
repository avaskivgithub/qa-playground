function goToPageAndCheckRedirectedLocation(elementHref, pageLink, timeoutValue=2000){
  cy.get(elementHref, { timeout: timeoutValue }).click(); //.debug();
  cy.location("href").should("eq", pageLink);

}

function getElementByLabel(labelText) {
  return cy.contains(labelText);
}

function checkContainTextWithTimeout(elementText, timeoutValue){
  cy.contains(elementText, { timeout: timeoutValue }).should(($element) => {
    // timeout here will be passed down to the '.should()'
    // unless an assertion throws earlier,
    // ALL of the assertions will retry for up to timeoutValue/1000 secs
    expect($element).to.not.have.class('error')
    expect($element).to.not.be.disabled
  });
}

function checkGetWithTimeout(elementQuery, timeoutValue){
  cy.get(elementQuery, { timeout: timeoutValue }).should(($element) => {
    // ALL of the assertions will retry for up to timeoutValue/1000 secs
    expect($element).to.not.have.class('error')
    expect($element).to.not.be.disabled
  });
}

exports.goToPageAndCheckRedirectedLocation = goToPageAndCheckRedirectedLocation;
exports.getElementByLabel = getElementByLabel;
exports.checkContainTextWithTimeout = checkContainTextWithTimeout;
exports.checkGetWithTimeout = checkGetWithTimeout;