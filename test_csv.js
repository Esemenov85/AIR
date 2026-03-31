const fs = require('fs');
const path = require('path');

function testCSV() {
    const csvPath = path.join(__dirname, 'enriched_links_fixed2.csv');
    const data = fs.readFileSync(csvPath, 'utf8');
    const rows = data.split(/\r?\n/).slice(1);
    console.log('Всего строк:', rows.length);
    const links = rows.filter(row => row.trim() !== '').map(row => {
        const cols = row.split(',');
        if (cols.length >= 8) {
            return {
                sheet: cols[0].trim(),
                description: cols[1].trim(),
                url: cols[2].trim(),
                row: cols[3].trim(),
                col: cols[4].trim(),
                category: cols[5].trim(),
                country: cols[6].trim(),
                investment: cols[7].trim().replace('\r', '')
            };
        }
        return null;
    }).filter(x => x);
    console.log('Успешно распарсено:', links.length);
    console.log('Первая ссылка:', links[0]);
    console.log('Количество инвестиционных (True):', links.filter(l => l.investment === 'True').length);
}

testCSV();