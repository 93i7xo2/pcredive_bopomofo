const cheerio = require('cheerio')
const fs = require('fs')

function main(err,data){
        if (err) throw err;
        const $ = cheerio.load(data);
        let result = [];
        $('tbody tr').map(function(i,el){
            // example:
            // {
            //     icon_id: '20065',
            //     property: 'puricone',
            //     name: '聖德蕾女的狂人',
            //     head: 'ㄥ',
            //     tail: 'ㄣ',
            //     info: '聖德蕾女的狂人。那就是優妮。'
            //   }
            let icon_id = $(this).children('.icon').attr('icon-id'),
            property = $(this).children('.icon').next().attr('class'),
            name = $(this).children('.icon').next().text(),
            head = $(this).children('.head').text(),
            tail = $(this).children('.tail').text(),
            info = $(this).children('.tail').next().text();
            result.push({
                icon_id,
                property,
                name,
                head,
                tail,
                info
            });
        });
        fs.writeFile('./data.json', JSON.stringify(result),()=>{
            console.log("Success");
        })
}

fs.readFile('./data.html', 'utf8', main);
