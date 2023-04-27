const pages = require('./clients/pages');
const utils = require('./clients/utils');


describe("test uitestingplayground", () => {

  beforeEach(() => {
    cy.visit(pages.MainPage.pageLink)
  })

    it("test Dynamic ID page", () => {
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementDynamicId, pages.DynamicIdPage.pageLink);

      utils.getElementByLabel(pages.DynamicIdPage.elementText).click();
      utils.getElementByLabel(pages.DynamicIdPage.elementText).should('be.enabled');
      // Same with controlled timeout with Chai expect
      // Assertions will retry for up to 2 secs
      utils.checkContainTextWithTimeout(pages.DynamicIdPage.elementText, 2000 );     
    });

    it("test class attr", () => {
      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementClassAttr, pages.ClassAttrPage.pageLink);

      cy.get(pages.ClassAttrPage.elementAttr).click();
      utils.checkGetWithTimeout(pages.ClassAttrPage.elementAttr, 2000 );     
    });

    it("test hidden layer, check that green button can not be hit twice", () => {
      const testPage = pages.HiddenLayersPage;

      utils.goToPageAndCheckRedirectedLocation(pages.MainPage.elementHiddenLayers, testPage.pageLink);

      cy.get(testPage.elementHiddenAttr).should('not.exist');

      cy.get(testPage.elementAttr).then(($selectedElement) => {
        debugger;
        $selectedElement.get(0).click();
      });
      cy.log("debugger did not work :( because tests were opned not on Electron");
      console.log("why logging is not obvious?");

      cy.get(testPage.elementHiddenAttr).should('exist');
      cy.get(testPage.elementAttr).shouldNotBeActionable;
      cy.get(testPage.elementHiddenAttr).shouldBeActionable;    
    });

  });