var json2csv = require('json2csv');
var fs = require('fs');
var data = require('./imdb_data_detail.json');
json2csv({data: data, fields: ['id', 'name', 'year']}, function(err, csv) {
  if (err) console.log(err);
  fs.writeFile('file.csv', csv, function(err) {
    if (err) throw err;
    console.log('file saved');
  });
});