var chai = require('chai')
  , chaiHttp = require('chai-http')
  , expect = require('chai').expect;

  chai.use(chaiHttp);


  describe('#http requests:', function() {
    this.timeout(17000);

    beforeEach(function() {
    })

    it('test simple get request', async function() {

        const response = await fetch("https://reqres.in/api/users?page=2");
        const jsonData = await response.json();
        
        var expElem = {
            id: 7,
            email: 'michael.lawson@reqres.in',
            first_name: 'Michael',
            last_name: 'Lawson',
            avatar: 'https://reqres.in/img/faces/7-image.jpg'
          };
        expect(response.status).to.be.equal(200);
        expect(jsonData.data[0]).to.deep.contains(expElem);
    })

    it('test get request with delay', async function() {

      const response = await fetch("http://uitestingplayground.com/ajaxdata");
      const data = await response.text();

      expect(response.status).to.be.equal(200);
      expect(data).to.deep.equal('Data loaded with AJAX get request.');
  })

    it('test simple post request', async function() {

      var data = {
        "name": "morpheus",
        "job": "leader"
      };
      const response = await fetch("https://reqres.in/api/users", {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify(data),
      });
      const jsonData = await response.json();

      expect(response.status).to.be.equal(201);
      expect(jsonData).to.deep.contains(data);
  })

})