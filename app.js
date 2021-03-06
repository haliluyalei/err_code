var app = require('koa')()
  , koa = require('koa-router')()
  , logger = require('koa-logger')
  , json = require('koa-json')
  , views = require('koa-views')
  , onerror = require('koa-onerror');

var index = require('./routes/index');
var code = require('./routes/code');
var utest = require('./routes/utest');
var users = require('./routes/users');
var sourcemap = require('./routes/sourcemap');

// global middlewares
app.use(views('views', {
  root: __dirname + '/views',
  default: 'ejs'
}));
app.use(require('koa-bodyparser')());
app.use(json());
app.use(logger());

app.use(function *(next) {
  var start = new Date;
  yield next;
  var ms = new Date - start;
  console.log('%s %s - %s', this.method, this.url, ms);
});

app.use(require('koa-static')(__dirname + '/public'));

// routes definition
koa.use('/', index.routes(), index.allowedMethods());
koa.use('/utest.xml', utest.routes(), index.allowedMethods());
koa.use('/code', code.routes(), code.allowedMethods());
koa.use('/test', users.routes(), users.allowedMethods());
koa.use('/sourcemap', sourcemap.routes(), users.allowedMethods());

// mount root routes
app.use(koa.routes());

app.on('error', function (err, ctx) {
  console.log(err);
  // logger.error('server error', err, ctx);
});

module.exports = app;
