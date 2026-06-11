const taskForm = document.querySelector('#taskForm');
const taskList = document.querySelector('#taskList');
const taskTemplate = document.querySelector('#taskTemplate');
const emptyState = document.querySelector('#emptyState');
const formStatus = document.querySelector('#formStatus');
const submitButton = document.querySelector('#submitButton');
const refreshButton = document.querySelector('#refreshButton');
const taskCount = document.querySelector('#taskCount');
const totalMinutes = document.querySelector('#totalMinutes');
const hardTasks = document.querySelector('#hardTasks');
const heroTotal = document.querySelector('#heroTotal');
const heroAverage = document.querySelector('#heroAverage');
const heroFocus = document.querySelector('#heroFocus');
const searchInput = document.querySelector('#searchInput');
const filterComplexity = document.querySelector('#filterComplexity');

let allTasks = [];
const API_BASE_URL = (window.API_BASE_URL || '').replace(/\/$/, '');
const apiUrl = (path) => `${API_BASE_URL}${path}`;

const complexityLabels = {
  low: 'Лёгкая',
  medium: 'Средняя',
  high: 'Сложная',
};

const presets = {
  report: {
    title: 'Подготовить отчёт',
    description: 'Собрать данные, выделить ключевые выводы и оформить итоговый отчёт для команды.',
    complexity: 'medium',
  },
  meeting: {
    title: 'Провести встречу',
    description: 'Подготовить повестку, обсудить открытые вопросы и зафиксировать следующие шаги.',
    complexity: 'low',
  },
  learning: {
    title: 'Изучить новую тему',
    description: 'Разобраться в материале, сделать короткий конспект и применить знания на практике.',
    complexity: 'high',
  },
};

function setStatus(message = '', type = '') {
  formStatus.textContent = message;
  formStatus.className = `status ${type}`.trim();
}

function getVisibleTasks() {
  const query = searchInput.value.trim().toLowerCase();
  const complexity = filterComplexity.value;

  return allTasks.filter((task) => {
    const matchesQuery = !query || [task.title, task.description, task.category]
      .some((value) => String(value || '').toLowerCase().includes(query));
    const matchesComplexity = complexity === 'all' || task.complexity === complexity;
    return matchesQuery && matchesComplexity;
  });
}

function updateStats(tasks) {
  const total = allTasks.length;
  const minutes = allTasks.reduce((sum, task) => sum + Number(task.estimated_minutes || 0), 0);
  const hard = allTasks.filter((task) => task.complexity === 'high').length;
  const average = total ? Math.round(minutes / total) : 0;
  const focusTask = [...allTasks].sort((a, b) => Number(b.estimated_minutes || 0) - Number(a.estimated_minutes || 0))[0];

  taskCount.textContent = total;
  totalMinutes.textContent = minutes;
  hardTasks.textContent = hard;
  heroTotal.textContent = total;
  heroAverage.textContent = `${average} мин`;
  heroFocus.textContent = focusTask ? focusTask.title : 'Добавьте первую задачу';

  const noResults = allTasks.length > 0 && tasks.length === 0;
  emptyState.querySelector('h3').textContent = noResults ? 'Ничего не найдено' : 'Пока задач нет';
  emptyState.querySelector('p').textContent = noResults
    ? 'Измените поиск или фильтр сложности.'
    : 'Добавьте первую задачу — она появится здесь с категорией и оценкой времени.';
}

function renderTasks() {
  const tasks = getVisibleTasks();
  taskList.innerHTML = '';
  emptyState.classList.toggle('visible', tasks.length === 0);
  updateStats(tasks);

  tasks.forEach((task) => {
    const item = taskTemplate.content.cloneNode(true);
    const article = item.querySelector('.task-item');
    const title = item.querySelector('h3');
    const description = item.querySelector('.task-description');
    const meta = item.querySelector('.meta');
    const deleteButton = item.querySelector('.danger');

    article.dataset.complexity = task.complexity;
    title.textContent = task.title;
    description.textContent = task.description;
    meta.innerHTML = `
      <span class="badge">${task.category}</span>
      <span class="badge">≈ ${task.estimated_minutes} мин</span>
      <span class="badge">${complexityLabels[task.complexity] || task.complexity}</span>
    `;

    deleteButton.addEventListener('click', async () => {
      const confirmed = confirm(`Удалить задачу «${task.title}»?`);
      if (!confirmed) return;

      deleteButton.disabled = true;
      deleteButton.textContent = 'Удаляем...';

      try {
        const response = await fetch(apiUrl(`/tasks/${task.id}`), { method: 'DELETE' });
        if (!response.ok) throw new Error('Не удалось удалить задачу');
        await loadTasks();
      } catch (error) {
        alert(error.message);
        deleteButton.disabled = false;
        deleteButton.textContent = 'Удалить';
      }
    });

    taskList.appendChild(item);
  });
}

async function loadTasks() {
  refreshButton.disabled = true;
  refreshButton.textContent = 'Загрузка...';

  try {
    const response = await fetch(apiUrl('/tasks/'));
    if (!response.ok) throw new Error('Не удалось загрузить задачи');
    allTasks = await response.json();
    renderTasks();
  } catch (error) {
    emptyState.classList.add('visible');
    emptyState.querySelector('h3').textContent = 'Ошибка загрузки';
    emptyState.querySelector('p').textContent = error.message;
  } finally {
    refreshButton.disabled = false;
    refreshButton.textContent = 'Обновить';
  }
}

taskForm.addEventListener('submit', async (event) => {
  event.preventDefault();
  setStatus('Добавляем задачу и получаем AI-оценку...');
  submitButton.disabled = true;
  submitButton.textContent = 'Добавляем...';

  const payload = {
    title: taskForm.title.value.trim(),
    description: taskForm.description.value.trim(),
    complexity: taskForm.complexity.value,
  };

  try {
    const response = await fetch(apiUrl('/tasks/'), {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    });

    if (!response.ok) throw new Error('Проверьте данные задачи и попробуйте снова');

    taskForm.reset();
    taskForm.complexity.value = 'medium';
    setStatus('Задача добавлена', 'success');
    await loadTasks();
  } catch (error) {
    setStatus(error.message, 'error');
  } finally {
    submitButton.disabled = false;
    submitButton.textContent = 'Добавить задачу';
  }
});

document.querySelectorAll('[data-preset]').forEach((button) => {
  button.addEventListener('click', () => {
    const preset = presets[button.dataset.preset];
    taskForm.title.value = preset.title;
    taskForm.description.value = preset.description;
    taskForm.complexity.value = preset.complexity;
    setStatus('Шаблон заполнен — можно добавить задачу.');
  });
});

refreshButton.addEventListener('click', loadTasks);
searchInput.addEventListener('input', renderTasks);
filterComplexity.addEventListener('change', renderTasks);
loadTasks();
