const jsdom = require('jsdom');
const { JSDOM } = jsdom;
const fs = require('fs');
const path = require('path');

const html = fs.readFileSync(path.join(__dirname, 'dashboard.html'), 'utf8');
const dom = new JSDOM(html, {
    runScripts: 'dangerously',
    resources: 'usable',
    url: 'http://localhost:8080'
});

const window = dom.window;

// Ждём загрузки скриптов и данных
setTimeout(() => {
    const tbody = window.document.getElementById('links-table-body');
    if (!tbody) {
        console.error('ERROR: tbody не найден');
        process.exit(1);
    }
    const rows = tbody.querySelectorAll('tr');
    console.log('Количество строк в таблице:', rows.length);
    if (rows.length === 0) {
        console.error('ERROR: таблица пуста');
        // Проверим, есть ли ошибки в консоли
        console.log('Логи консоли:', window.console.logs);
        process.exit(1);
    } else {
        console.log('SUCCESS: таблица содержит данные');
        // Проверим инвестиционные ссылки
        const investmentList = window.document.getElementById('investment-list');
        const investmentItems = investmentList.querySelectorAll('li');
        console.log('Количество инвестиционных ссылок:', investmentItems.length);
        if (investmentItems.length === 0) {
            console.error('ERROR: список инвестиционных ссылок пуст');
            process.exit(1);
        } else {
            console.log('SUCCESS: инвестиционные ссылки отображаются');
        }
    }
    process.exit(0);
}, 2000); // даём время на загрузку CSV