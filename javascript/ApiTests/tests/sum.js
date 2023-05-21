var expect = require('chai').expect;

function sum(...args) {
  let sum = 0;
  for (let arg of args) sum += arg;
  return sum;
}

describe('#sum()', function() {

    // add a test hook
    beforeEach(function() {
      // ...some logic before each test is run
    })
  
    // test a functionality
    it('should add numbers', function() {
      // add an assertion
      expect(sum(1, 2, 3, 4, 5)).to.equal(15);
    })
  
    // ...some more tests
  
  })