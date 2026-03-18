// Адрес вашего backend API
const API_BASE_URL = 'http://127.0.0.1:8000';

// --- Загрузка документа ---
document.getElementById('upload-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file-input');
    const metaInput = document.getElementById('meta-input');
    const resultDiv = document.getElementById('upload-result');

    const formData = new FormData();
    formData.append('file', fileInput.files[0]);

    // Добавляем метаданные, если есть
    const metaText = metaInput.value.trim();
    if (metaText) {
        try {
            const metaObj = JSON.parse(metaText);
            formData.append('metadata', JSON.stringify(metaObj));
        } catch (e) {
            alert('Ошибка в формате JSON метаданных.');
            return;
        }
    }

    try {
        resultDiv.textContent = 'Загрузка...';
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData, // FormData автоматически устанавливает Content-Type multipart/form-data
        });

        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}: ${await response.text()}`);
        }

        const data = await response.json();
        resultDiv.innerHTML = `<p style="color:green;">✅ Документ "${data.filename}" загружен (ID: ${data.id}).</p>`;
        fileInput.value = ''; // Очистить инпут файла
        metaInput.value = ''; // Очистить инпут метаданных
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        resultDiv.innerHTML = `<p style="color:red;">❌ Ошибка: ${error.message}</p>`;
    }
});

// --- Поиск по корпусу ---
document.getElementById('search-form').addEventListener('submit', async (e) => {
    e.preventDefault();
    const queryInput = document.getElementById('query-input');
    const queryTypeSelect = document.getElementById('query-type-select');
    const contextWindowInput = document.getElementById('context-window');
    const resultLimitInput = document.getElementById('result-limit');
    const resultsDiv = document.getElementById('search-results');

    const query = queryInput.value.trim();
    if (!query) {
        alert('Введите запрос.');
        return;
    }

    const searchParams = {
        query: query,
        query_type: queryTypeSelect.value,
        context_window: parseInt(contextWindowInput.value),
        limit: parseInt(resultLimitInput.value),
    };

    try {
        resultsDiv.innerHTML = '<p>Поиск...</p>';
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(searchParams),
        });

        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}: ${await response.text()}`);
        }

        const data = await response.json();
        resultsDiv.innerHTML = '';

        if (data.results.length === 0) {
            resultsDiv.innerHTML = `<p><i>Ничего не найдено для "${query}".</i></p>`;
            return;
        }

        resultsDiv.innerHTML = `<h3>Найдено: ${data.total_found} вхождений</h3>`;
        data.results.forEach(item => {
            const itemEl = document.createElement('div');
            itemEl.className = 'concordance-item';
            // Обрезаем длинные контексты для лучшего отображения
            const leftCtx = item.left_context ? item.left_context.slice(-50) : '';
            const rightCtx = item.right_context ? item.right_context.slice(0, 50) : '';
            itemEl.innerHTML = `
                <strong>Документ:</strong> ${item.filename} (ID: ${item.document_id})<br>
                <em>${leftCtx} <mark>${item.target}</mark> ${rightCtx}</em><br>
                <small>POS: ${item.grammemes.join(', ')}</small>
            `;
            resultsDiv.appendChild(itemEl);
        });
    } catch (error) {
        console.error('Ошибка поиска:', error);
        resultsDiv.innerHTML = `<p style="color:red;">❌ Ошибка: ${error.message}</p>`;
    }
});

// --- Список документов ---
document.getElementById('refresh-docs-btn').addEventListener('click', loadDocuments);

async function loadDocuments() {
    const listEl = document.getElementById('documents-list');
    listEl.innerHTML = '<li>Загрузка...</li>';

    try {
        const response = await fetch(`${API_BASE_URL}/documents`);
        if (!response.ok) {
            throw new Error(`Ошибка ${response.status}: ${await response.text()}`);
        }
        const documents = await response.json();

        listEl.innerHTML = '';
        if (documents.length === 0) {
            listEl.innerHTML = '<li>Корпус пуст.</li>';
            return;
        }

        documents.forEach(doc => {
            const li = document.createElement('li');
            li.className = 'doc-item';
            li.innerHTML = `
                <strong>${doc.filename}</strong> (ID: ${doc.id}) -
                Тип: ${doc.file_type}, Обработан: ${doc.is_processed ? 'Да' : 'Нет'}<br>
                <small>Дата: ${new Date(doc.created_at).toLocaleString()}</small>
            `;
            listEl.appendChild(li);
        });
    } catch (error) {
        console.error('Ошибка загрузки списка документов:', error);
        listEl.innerHTML = `<li style="color:red;">❌ Ошибка: ${error.message}</li>`;
    }
}

// Загрузить список документов при запуске
document.addEventListener('DOMContentLoaded', loadDocuments);