var router = require('koa-router')();


router.get('/', function *(next) {
	this.body = 'utest';

});

router.get('/utest.xml', function *(next){
	yield this.render('index', {
    title: 'this is for utest check'
  });
	
})


  module.exports = router;



