// ===== Конфигурация =====
const API_BASE_URL = 'http://127.0.0.1:8000';
let currentPage = 1;
const ITEMS_PER_PAGE = 20;

// ===== Утилиты =====
function showMessage(elementId, message, type = 'info') {
    const el = document.getElementById(elementId);
    if (!el) return;
    el.className = `result-message ${type}`;
    el.textContent = message;
    setTimeout(() => { if (el.className.includes(type)) el.textContent = ''; }, 5000);
}

function formatDate(dateString) {
    return new Date(dateString).toLocaleString('ru-RU');
}

// ===== Глобальная статистика =====
async function loadGlobalStats() {
    const container = document.getElementById('global-stats');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/stats/global`);
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        const stats = await response.json();
        
        container.innerHTML = `
            <div class="stat-item">
                <div class="stat-value">${stats.total_documents || 0}</div>
                <div class="stat-label">Документов</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${stats.total_tokens?.toLocaleString() || 0}</div>
                <div class="stat-label">Токенов</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${stats.unique_lemmas?.toLocaleString() || 0}</div>
                <div class="stat-label">Уникальных лемм</div>
            </div>
            <div class="stat-item">
                <div class="stat-value">${stats.avg_tokens_per_doc?.toFixed(1) || 0}</div>
                <div class="stat-label">Среднее токенов/док</div>
            </div>
        `;
    } catch (error) {
        console.error('Ошибка загрузки статистики:', error);
        container.innerHTML = `<p class="text-muted">Не удалось загрузить статистику</p>`;
    }
}

// ===== Загрузка документа =====
document.getElementById('upload-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const fileInput = document.getElementById('file-input');
    const metaInput = document.getElementById('meta-input');
    
    const formData = new FormData();
    formData.append('file', fileInput.files[0]);
    
    const metaText = metaInput.value.trim();
    if (metaText) {
        try {
            const metaObj = JSON.parse(metaText);
            formData.append('metadata', JSON.stringify(metaObj));
        } catch (e) {
            showMessage('upload-result', '❌ Ошибка в формате JSON метаданных', 'error');
            return;
        }
    }
    
    try {
        showMessage('upload-result', '⏳ Загрузка...', 'info');
        const response = await fetch(`${API_BASE_URL}/documents/upload`, {
            method: 'POST',
            body: formData,
        });
        
        if (!response.ok) {
            const errorText = await response.text();
            throw new Error(`Ошибка ${response.status}: ${errorText}`);
        }
        
        const data = await response.json();
        showMessage('upload-result', `✅ Документ "${data.filename}" загружен (ID: ${data.id})`, 'success');
        fileInput.value = '';
        metaInput.value = '';
        loadDocuments();
        loadGlobalStats();
    } catch (error) {
        console.error('Ошибка загрузки:', error);
        showMessage('upload-result', `❌ ${error.message}`, 'error');
    }
});

// ===== Поиск =====
document.getElementById('search-form')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const query = document.getElementById('query-input').value.trim();
    if (!query) {
        alert('Введите запрос');
        return;
    }
    
    const resultsDiv = document.getElementById('search-results');
    resultsDiv.innerHTML = '<p class="text-center">🔍 Поиск...</p>';
    
    const searchParams = {
        query: query,
        query_type: document.getElementById('query-type-select').value,
        context_window: parseInt(document.getElementById('context-window').value),
        limit: parseInt(document.getElementById('result-limit').value),
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/search`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(searchParams),
        });
        
        if (!response.ok) throw new Error(`Ошибка ${response.status}: ${await response.text()}`);
        const data = await response.json();
        
        if (!data.results?.length) {
            resultsDiv.innerHTML = `<p class="text-muted">Ничего не найдено для "${query}"</p>`;
            return;
        }
        
        resultsDiv.innerHTML = `
            <p><strong>Найдено:</strong> ${data.total_found} вхождений 
            <span class="text-muted">(${data.execution_time_ms}ms)</span></p>
        `;
        
        data.results.forEach(item => {
            const div = document.createElement('div');
            div.className = 'concordance-item';
            const left = item.left_context?.slice(-50) || '';
            const right = item.right_context?.slice(0, 50) || '';
            div.innerHTML = `
                <strong>📄 ${item.filename}</strong> 
                <small>(ID: ${item.document_id})</small><br>
                <em>${left}<mark>${item.target}</mark>${right}</em><br>
                <small>POS: ${item.grammemes?.join(', ') || '—'}</small>
            `;
            resultsDiv.appendChild(div);
        });
    } catch (error) {
        console.error('Ошибка поиска:', error);
        resultsDiv.innerHTML = `<p class="result-message error">❌ ${error.message}</p>`;
    }
});

// ===== Список документов =====
async function loadDocuments(page = 1) {
    const listEl = document.getElementById('documents-list');
    if (!listEl) return;
    
    listEl.innerHTML = '<li class="text-center">⏳ Загрузка...</li>';
    
    try {
        const response = await fetch(
            `${API_BASE_URL}/documents?skip=${(page - 1) * ITEMS_PER_PAGE}&limit=${ITEMS_PER_PAGE}`
        );
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        const documents = await response.json();
        
        listEl.innerHTML = '';
        if (!documents.length) {
            listEl.innerHTML = '<li class="text-muted">Корпус пуст. Загрузите первый документ!</li>';
            updatePagination(0, page);
            return;
        }
        
        documents.forEach(doc => {
            const li = document.createElement('li');
            li.className = 'doc-item';
            li.dataset.docId = doc.id;
            li.dataset.meta = JSON.stringify(doc.meta_data || {});
            
            li.innerHTML = `
                <strong>📄 ${doc.filename}</strong> 
                <small>ID: ${doc.id} | ${doc.file_type}</small><br>
                <small>🕐 ${formatDate(doc.created_at)}</small>
                <small>✅ ${doc.is_processed ? 'Обработан' : 'В обработке...'}</small>
                <div class="doc-actions">
                    <button class="btn btn-sm btn-secondary" onclick="downloadDocument(${doc.id})">📥</button>
                    <button class="btn btn-sm btn-secondary" onclick="toggleDocStats(${doc.id})">📊</button>
                    <button class="btn btn-sm btn-secondary" onclick="editMetadata(${doc.id}, this)">✏️</button>
                    <button class="btn btn-sm btn-danger" onclick="deleteDocument(${doc.id})">🗑️</button>
                </div>
                <div id="stats-${doc.id}" class="doc-stats hidden"></div>
            `;
            listEl.appendChild(li);
        });
        
        updatePagination(documents.length, page);
    } catch (error) {
        console.error('Ошибка загрузки списка:', error);
        listEl.innerHTML = `<li class="result-message error">❌ ${error.message}</li>`;
    }
}

function updatePagination(loadedCount, currentPage) {
    const prevBtn = document.getElementById('prev-page-btn');
    const nextBtn = document.getElementById('next-page-btn');
    const pageInfo = document.getElementById('page-info');
    
    if (!prevBtn || !nextBtn || !pageInfo) return;
    
    pageInfo.textContent = `Страница ${currentPage}`;
    prevBtn.disabled = currentPage === 1;
    nextBtn.disabled = loadedCount < ITEMS_PER_PAGE;
}

// Пагинация
document.getElementById('prev-page-btn')?.addEventListener('click', () => {
    if (currentPage > 1) {
        currentPage--;
        loadDocuments(currentPage);
    }
});

document.getElementById('next-page-btn')?.addEventListener('click', () => {
    currentPage++;
    loadDocuments(currentPage);
});

document.getElementById('refresh-docs-btn')?.addEventListener('click', () => {
    currentPage = 1;
    loadDocuments(currentPage);
});

// ===== Скачивание документа =====
function downloadDocument(docId) {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL}/documents/${docId}/download`;
    link.download = '';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ===== Экспорт корпуса =====
function exportCorpus() {
    const link = document.createElement('a');
    link.href = `${API_BASE_URL}/corpus/export`;
    link.download = 'corpus_export.zip';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
}

// ===== Статистика документа =====
async function toggleDocStats(docId) {
    const statsDiv = document.getElementById(`stats-${docId}`);
    if (!statsDiv) return;
    
    if (!statsDiv.classList.contains('hidden')) {
        statsDiv.classList.add('hidden');
        return;
    }
    
    statsDiv.classList.remove('hidden');
    statsDiv.innerHTML = '<span class="loading"></span> Загрузка...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${docId}?with_stats=true`);
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        const doc = await response.json();
        
        if (!doc.stats) {
            statsDiv.innerHTML = '<em>Статистика недоступна</em>';
            return;
        }
        
        const s = doc.stats;
        const topLemmas = s.top_lemmas?.slice(0, 5).map(l => 
            `${l.lemma || l} (${l.count || l})`
        ).join(', ') || '—';
        
        const posDist = Object.entries(s.pos_distribution || {})
            .slice(0, 5)
            .map(([pos, count]) => `${pos}:${count}`)
            .join(', ') || '—';
        
        statsDiv.innerHTML = `
            <strong>📊 Статистика:</strong><br>
            Токенов: ${s.total_tokens?.toLocaleString() || 0}<br>
            Уникальных лемм: ${s.unique_lemmas?.toLocaleString() || 0}<br>
            TOP-5 лемм: ${topLemmas}<br>
            POS: ${posDist}
        `;
    } catch (error) {
        console.error('Ошибка статистики:', error);
        statsDiv.innerHTML = `<span class="text-muted">Ошибка: ${error.message}</span>`;
    }
}

async function editMetadata(docId, button) {
    const li = button.closest('.doc-item');
    const currentMeta = JSON.parse(li.dataset.meta || '{}');
    const currentFilename = li.querySelector('strong').textContent.replace(/\s*\(ID:.*\)/, '');
    
    const newFilename = prompt('Новое имя файла:', currentFilename);
    if (newFilename === null) return;
    
    const newMetaStr = prompt('Метаданные (JSON):', JSON.stringify(currentMeta, null, 2));
    if (newMetaStr === null) return;
    
    let newMeta = {};
    if (newMetaStr.trim()) {
        try {
            newMeta = JSON.parse(newMetaStr);
        } catch (e) {
            alert('❌ Ошибка в формате JSON');
            return;
        }
    }
    
    await updateDocument(docId, newFilename, newMeta, li);
}

async function updateDocument(docId, filename, meta_data, listItem) {
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
            method: 'PUT',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ filename, meta_data }),
        });
        
        if (!response.ok) throw new Error(`Ошибка ${response.status}: ${await response.text()}`);
        
        const updated = await response.json();
        listItem.querySelector('strong').textContent = `📄 ${updated.filename}`;
        listItem.dataset.meta = JSON.stringify(updated.meta_data || {});
        showMessage('upload-result', '✅ Документ обновлён', 'success');
    } catch (error) {
        console.error('Ошибка обновления:', error);
        alert(`❌ ${error.message}`);
    }
}

// ===== Удаление документа =====
async function deleteDocument(docId) {
    if (!confirm('Удалить этот документ? Это действие нельзя отменить.')) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/documents/${docId}`, {
            method: 'DELETE',
        });
        
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        
        showMessage('upload-result', '✅ Документ удалён', 'success');
        loadDocuments(currentPage);
        loadGlobalStats();
    } catch (error) {
        console.error('Ошибка удаления:', error);
        alert(`❌ ${error.message}`);
    }
}

// ===== Информация о лемме =====
async function showLemmaInfo(lemma) {
    const section = document.getElementById('lemma-section');
    const content = document.getElementById('lemma-content');
    const title = document.getElementById('lemma-title');
    
    if (!section || !content) return;
    
    section.classList.remove('hidden');
    title.textContent = lemma;
    content.innerHTML = '<span class="loading"></span> Загрузка...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/lemmas/${encodeURIComponent(lemma)}`);
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        const data = await response.json();
        
        const forms = data.word_forms?.slice(0, 10).join(', ') || '—';
        const examples = data.examples?.slice(0, 3).map(ex => 
            `<em>${ex}</em>`
        ).join('<br>') || '—';
        
        content.innerHTML = `
            <dl>
                <dt>Лемма:</dt><dd><strong>${data.lemma || lemma}</strong></dd>
                <dt>Часть речи:</dt><dd>${data.pos || '—'}</dd>
                <dt>Частотность:</dt><dd>${data.frequency?.toLocaleString() || 0} вхождений</dd>
                <dt>Формы слова:</dt><dd><div class="lemma-forms">
                    ${data.word_forms?.slice(0, 15).map(f => 
                        `<span class="lemma-form">${f}</span>`
                    ).join('') || '—'}
                </div></dd>
                <dt>Примеры:</dt><dd>${examples}</dd>
            </dl>
        `;
    } catch (error) {
        console.error('Ошибка загрузки леммы:', error);
        content.innerHTML = `<p class="text-muted">❌ ${error.message}</p>`;
    }
}

document.getElementById('close-lemma-btn')?.addEventListener('click', () => {
    document.getElementById('lemma-section')?.classList.add('hidden');
});

// ===== Справка API =====
async function loadApiHelp() {
    const container = document.getElementById('api-help-content');
    if (!container) return;
    
    try {
        const response = await fetch(`${API_BASE_URL}/help/api`);
        if (!response.ok) throw new Error(`Ошибка ${response.status}`);
        const help = await response.json();
        
        container.innerHTML = `
            <pre><code>${JSON.stringify(help, null, 2)}</code></pre>
        `;
    } catch (error) {
        console.error('Ошибка загрузки справки:', error);
        container.innerHTML = `<p class="text-muted">Не удалось загрузить справку API</p>`;
    }
}

// ===== Инициализация =====
document.addEventListener('DOMContentLoaded', () => {
    // Загружаем статистику и документы только на главной странице
    if (document.getElementById('global-stats')) {
        loadGlobalStats();
        loadDocuments(1);
    }
    
    // Обработчик клика по лемме в результатах поиска (делегирование)
    document.getElementById('search-results')?.addEventListener('click', (e) => {
        if (e.target.tagName === 'MARK') {
            showLemmaInfo(e.target.textContent);
        }
    });
});