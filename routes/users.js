var router = require('koa-router')();
var fs = require('fs');
router.get('/', function *(next) {
  yield this.render('users', {
    title: 'users!'
  });
});
router.get('/deadlock', function *(next) {
  yield this.render('deadlock', {
    title: 'deadlock!'
  });
});
router.get('/alert', function *(next) {
  yield this.render('alert', {
    title: 'alert!'
  });
});
router.post('/post', function *(next) {
  console.log(this.request.body);
  fs.writeFileSync(__dirname + '/_' + new Date().getTime() + '.txt', JSON.stringify(this.request.body, undefined, 2), 'utf-8');
  this.body = {
	  ret: 0
  };
});

module.exports = router;
