// Данные метрик
const metrics = {
    total_links: 115,
    russian_links: 19,
    regional_links: 58,
    international_links: 38,
    country_counts: {
        "Другая": 19,
        "Международная организация": 3,
        "Китай": 2,
        "Индия": 2,
        "США (исламская экономика)": 1,
        "Саудовская Аравия": 1,
        "Швейцария": 1,
        "Катар": 1,
        "Малайзия": 1,
        "Кипр": 1,
        "Казахстан": 1,
        "Италия": 1,
        "Франция": 1,
        "Азербайджан": 1,
        "Южная Корея": 1,
        "Германия": 1
    },
    investment_links_count: 32
};

// Заполняем метрики на главной
document.addEventListener('DOMContentLoaded', function() {
    document.getElementById('total-links').textContent = metrics.total_links;
    document.getElementById('russian-links').textContent = metrics.russian_links;
    document.getElementById('regional-links').textContent = metrics.regional_links;
    document.getElementById('international-links').textContent = metrics.international_links;
    document.getElementById('investment-links').textContent = metrics.investment_links_count;

    // Заполняем список стран
    const countryList = document.getElementById('country-list');
    for (const [country, count] of Object.entries(metrics.country_counts)) {
        const badge = document.createElement('div');
        badge.className = 'country-badge';
        badge.innerHTML = `<span class="count">${count}</span> ${country}`;
        countryList.appendChild(badge);
    }

    // Загружаем CSV с ссылками
    loadLinksCSV().then(links => {
        console.log('Загружено ссылок:', links.length);
        populateLinksTable(links);
        populateInvestmentList(links);
    });

    // Переключение вкладок
    const tabs = document.querySelectorAll('.tab');
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            const tabId = tab.getAttribute('data-tab');
            switchTab(tabId);
        });
    });

    // Удаляем блок "Технологии" на вкладке "О проекте"
    const techNote = document.querySelector('#about .note');
    if (techNote) {
        techNote.remove();
    }
});

// Загружаем CSV с ссылками (исправленный файл)
async function loadLinksCSV() {
    try {
        const response = await fetch('enriched_links_fixed2.csv');
        const text = await response.text();
        // Убираем BOM если есть
        const cleanText = text.replace(/^\uFEFF/, '');
        // Разделяем строки, убираем \r
        const rows = cleanText.split(/\r?\n/).slice(1); // пропускаем заголовок
        console.log('Всего строк в CSV:', rows.length);
        const links = rows.filter(row => row.trim() !== '').map(row => {
            const cols = row.split(',');
            // Теперь колонок 8: sheet, description, url, row, col, category, country, investment
            if (cols.length >= 8) {
                // Обрезаем возможные пробелы и \r
                const sheet = cols[0].trim();
                const description = cols[1].trim();
                const url = cols[2].trim();
                const rowNum = cols[3].trim();
                const colNum = cols[4].trim();
                const category = cols[5].trim();
                const country = cols[6].trim();
                const investment = cols[7].trim().replace('\r', '');
                console.log(`Ссылка: ${description}, investment: ${investment}`);
                return {
                    sheet,
                    description,
                    url,
                    row: rowNum,
                    col: colNum,
                    category,
                    country,
                    investment
                };
            } else {
                console.warn('Строка с неправильным количеством колонок:', row);
                return null;
            }
        }).filter(x => x);
        console.log('Успешно распарсено ссылок:', links.length);
        return links;
    } catch (error) {
        console.error('Ошибка загрузки CSV:', error);
        return [];
    }
}

// Заполняем таблицу ссылок
function populateLinksTable(links) {
    const tbody = document.getElementById('links-table-body');
    tbody.innerHTML = '';
    console.log('Заполняем таблицу, количество ссылок:', links.length);
    if (links.length === 0) {
        const tr = document.createElement('tr');
        tr.innerHTML = `<td colspan="7" style="text-align: center; color: gray;">Нет данных</td>`;
        tbody.appendChild(tr);
        return;
    }
    links.forEach((link, index) => {
        const tr = document.createElement('tr');
        tr.innerHTML = `
            <td>${index + 1}</td>
            <td>${link.sheet}</td>
            <td>${link.description}</td>
            <td><a href="${link.url}" target="_blank">${link.url}</a></td>
            <td>${link.row}</td>
            <td>${link.col}</td>
            <td><span class="badge">${link.category}</span></td>
        `;
        tbody.appendChild(tr);
    });
}

// Заполняем список инвестиционных ссылок (используем столбец investment)
function populateInvestmentList(links) {
    const investmentList = document.getElementById('investment-list');
    investmentList.innerHTML = '';
    const investmentLinks = links.filter(link => link.investment === 'True');
    console.log('Инвестиционных ссылок:', investmentLinks.length);
    if (investmentLinks.length === 0) {
        const li = document.createElement('li');
        li.textContent = 'Нет инвестиционных ссылок';
        investmentList.appendChild(li);
        return;
    }
    investmentLinks.forEach(link => {
        const li = document.createElement('li');
        li.innerHTML = `<a href="${link.url}" target="_blank">${link.description}</a> (лист: ${link.sheet})`;
        investmentList.appendChild(li);
    });
}

// Переключение вкладок
function switchTab(tabId) {
    // Убираем активный класс у всех вкладок и контента
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
    // Активируем выбранную вкладку и контент
    document.querySelector(`.tab[data-tab="${tabId}"]`).classList.add('active');
    document.getElementById(tabId).classList.add('active');
}