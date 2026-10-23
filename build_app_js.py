import json

with open(r"C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web\data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Python code of practica_pandas.py
with open(r"C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web\practica_pandas.py", "r", encoding="utf-8") as f:
    py_code = f.read()

app_js_content = f"""// ==============================================================================
// LOGICA INTERACTIVA - PRÁCTICA PANDAS Y MATPLOTLIB
// ==============================================================================

const APP_DATA = {json.dumps(data, ensure_ascii=False)};
const PYTHON_CODE = {json.dumps(py_code, ensure_ascii=False)};

document.addEventListener('DOMContentLoaded', () => {{
  initTheme();
  renderStudentTable();
  renderFilters();
  renderSummaries();
  renderCodeViewer();
  initLightbox();
  initScrollSpy();
}});

// --- 1. TEMA OSCURO / CLARO ---
function initTheme() {{
  const toggleBtn = document.getElementById('themeToggle');
  const savedTheme = localStorage.getItem('tecnm_theme') || 'dark';
  document.documentElement.setAttribute('data-theme', savedTheme);
  updateThemeIcon(savedTheme);

  if (toggleBtn) {{
    toggleBtn.addEventListener('click', () => {{
      const current = document.documentElement.getAttribute('data-theme') || 'dark';
      const nextTheme = current === 'dark' ? 'light' : 'dark';
      document.documentElement.setAttribute('data-theme', nextTheme);
      localStorage.setItem('tecnm_theme', nextTheme);
      updateThemeIcon(nextTheme);
      showToast(`Modo ${{nextTheme === 'dark' ? 'Oscuro' : 'Claro'}} activado`);
    }});
  }}
}}

function updateThemeIcon(theme) {{
  const icon = document.getElementById('themeIcon');
  if (icon) {{
    icon.textContent = theme === 'dark' ? '☀️' : '🌙';
  }}
}}

// --- 2. RENDER DE TABLA DE ALUMNOS (PROMEDIOS Y BUSCADOR) ---
let currentSearch = '';
let currentFilterGrupo = 'ALL';

function renderStudentTable() {{
  const tbody = document.getElementById('studentsTableBody');
  if (!tbody) return;

  let list = APP_DATA.promedio_alumnos;

  // Filtrado
  const filtered = list.filter(item => {{
    const matchText = item.nombre.toLowerCase().includes(currentSearch.toLowerCase()) || 
                      item.matricula.toLowerCase().includes(currentSearch.toLowerCase());
    return matchText;
  }});

  tbody.innerHTML = '';

  filtered.forEach((item, idx) => {{
    const tr = document.createElement('tr');
    const isApproved = item.promedio >= 70;
    
    let rankBadge = `<span style="font-weight:700; color:var(--text-dim);">#${{idx + 1}}</span>`;
    if (idx === 0) rankBadge = `<span style="font-size:1.1rem;">🥇</span>`;
    else if (idx === 1) rankBadge = `<span style="font-size:1.1rem;">🥈</span>`;
    else if (idx === 2) rankBadge = `<span style="font-size:1.1rem;">🥉</span>`;

    const progressClass = isApproved ? 'green' : 'red';

    tr.innerHTML = `
      <td>${{rankBadge}}</td>
      <td><span class="badge-group">${{item.matricula}}</span></td>
      <td style="font-weight:600;">${{item.nombre}}</td>
      <td>
        <div class="progress-bar-container">
          <div class="progress-track">
            <div class="progress-fill ${{progressClass}}" style="width: ${{Math.min(item.promedio, 100)}}%;"></div>
          </div>
          <span style="font-weight:700; font-family:'JetBrains Mono'; min-width:45px;">${{item.promedio.toFixed(2)}}</span>
        </div>
      </td>
      <td>
        <span class="badge ${{isApproved ? 'badge-success' : 'badge-danger'}}">
          ${{isApproved ? 'Aprobado' : 'Reprobado'}}
        </span>
      </td>
    `;
    tbody.appendChild(tr);
  }});
}}

window.handleStudentSearch = function(val) {{
  currentSearch = val;
  renderStudentTable();
}};

// --- 3. RENDER DE RESÚMENES (MATERIAS Y GRUPOS) ---
function renderSummaries() {{
  // Promedio por Materia
  const matContainer = document.getElementById('materiasSummaryGrid');
  if (matContainer) {{
    matContainer.innerHTML = '';
    const materias = APP_DATA.promedio_materia;
    for (const [mat, prom] of Object.entries(materias)) {{
      const card = document.createElement('div');
      card.className = 'filter-card';
      const isLowest = mat === 'Matematicas discretas';
      const color = isLowest ? 'var(--accent-rose)' : 'var(--accent-cyan)';
      
      card.innerHTML = `
        <div class="filter-card-header">
          <span class="filter-title">${{mat}}</span>
          <span class="badge ${{isLowest ? 'badge-danger' : 'badge-info'}}">${{isLowest ? 'Promedio Más Bajo' : 'Aprobatoria'}}</span>
        </div>
        <div style="font-size: 2.25rem; font-weight:800; font-family:'Outfit'; color:${{color}}; margin-bottom:0.5rem;">
          ${{prom.toFixed(2)}} <span style="font-size:1rem; color:var(--text-dim);">/ 100</span>
        </div>
        <div class="progress-track" style="margin-top:0.5rem;">
          <div class="progress-fill ${{isLowest ? 'red' : 'blue'}}" style="width:${{prom}}%;"></div>
        </div>
      `;
      matContainer.appendChild(card);
    }}
  }}

  // Promedio por Unidad
  const unidadesContainer = document.getElementById('unidadesSummaryGrid');
  if (unidadesContainer) {{
    unidadesContainer.innerHTML = '';
    const u = APP_DATA.promedio_unidad;
    for (const [unidad, val] of Object.entries(u)) {{
      const card = document.createElement('div');
      card.className = 'filter-card';
      const isU3 = unidad === '3';
      card.innerHTML = `
        <div class="filter-card-header">
          <span class="filter-title">Unidad ${{unidad}}</span>
          <span class="badge ${{isU3 ? 'badge-danger' : 'badge-info'}}">${{isU3 ? 'Mayor Dificultad' : 'Estable'}}</span>
        </div>
        <div style="font-size: 2.25rem; font-weight:800; font-family:'Outfit'; color:${{isU3 ? 'var(--accent-rose)' : 'var(--accent-emerald)'}};">
          ${{val.toFixed(2)}}
        </div>
        <div class="filter-query" style="margin-top:0.75rem;">Todas las materias promediadas</div>
      `;
      unidadesContainer.appendChild(card);
    }}
  }}
}}

// --- 4. RENDER DE FILTROS ---
function renderFilters() {{
  const bdTableBody = document.getElementById('bdFilteredTableBody');
  if (bdTableBody && APP_DATA.filtros.bd_b_80_records) {{
    bdTableBody.innerHTML = '';
    APP_DATA.filtros.bd_b_80_records.forEach((row, i) => {{
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td>#${{i + 1}}</td>
        <td><span class="badge-group">${{row.matricula}}</span></td>
        <td style="font-weight:600;">${{row.nombre}}</td>
        <td>${{row.materia}}</td>
        <td>Unidad ${{row.unidad}}</td>
        <td style="font-weight:700; color:var(--accent-emerald); font-family:'JetBrains Mono';">${{row.calificacion}}</td>
        <td>${{row.asistencias}}</td>
      `;
      bdTableBody.appendChild(tr);
    }});
  }}
}}

// --- 5. VISOR DE CÓDIGO PYTHON ---
function renderCodeViewer() {{
  const codeEl = document.getElementById('pythonCodeBlock');
  if (codeEl) {{
    codeEl.textContent = PYTHON_CODE;
  }}
}}

window.copyCode = function() {{
  navigator.clipboard.writeText(PYTHON_CODE).then(() => {{
    showToast('¡Código Python copiado al portapapeles!');
  }}).catch(() => {{
    showToast('Error al copiar el código');
  }});
}};

window.downloadCode = function() {{
  const blob = new Blob([PYTHON_CODE], {{ type: 'text/x-python;charset=utf-8' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'practica_pandas.py';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Descargando practica_pandas.py...');
}};

window.downloadPromediosCSV = function() {{
  let csvContent = "matricula,nombre,promedio\\n";
  APP_DATA.promedio_alumnos.forEach(row => {{
    csvContent += `${{row.matricula}},${{row.nombre}},${{row.promedio}}\\n`;
  }});
  const blob = new Blob([csvContent], {{ type: 'text/csv;charset=utf-8' }});
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = 'promedios_alumnos.csv';
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
  URL.revokeObjectURL(url);
  showToast('Descargando promedios_alumnos.csv...');
}};

// --- 6. LIGHTBOX PARA GRÁFICAS ---
function initLightbox() {{
  const modal = document.getElementById('imageModal');
  const modalImg = document.getElementById('modalImage');
  const closeBtn = document.getElementById('modalClose');

  if (!modal || !modalImg) return;

  document.querySelectorAll('.chart-media-box').forEach(box => {{
    box.addEventListener('click', () => {{
      const img = box.querySelector('img');
      if (img) {{
        modalImg.src = img.src;
        modal.classList.add('active');
      }}
    }});
  }});

  if (closeBtn) {{
    closeBtn.addEventListener('click', () => {{
      modal.classList.remove('active');
    }});
  }}

  modal.addEventListener('click', (e) => {{
    if (e.target === modal) {{
      modal.classList.remove('active');
    }}
  }});

  document.addEventListener('keydown', (e) => {{
    if (e.key === 'Escape' && modal.classList.contains('active')) {{
      modal.classList.remove('active');
    }}
  }});
}}

// --- 7. SCROLL SPY Y NAVEGACIÓN ---
function initScrollSpy() {{
  const sections = document.querySelectorAll('section[id]');
  const navTabs = document.querySelectorAll('.nav-tab');

  window.addEventListener('scroll', () => {{
    let currentId = '';
    const scrollPos = window.scrollY + 120;

    sections.forEach(sec => {{
      const top = sec.offsetTop;
      const height = sec.offsetHeight;
      if (scrollPos >= top && scrollPos < top + height) {{
        currentId = sec.getAttribute('id');
      }}
    }});

    navTabs.forEach(tab => {{
      tab.classList.remove('active');
      if (tab.getAttribute('href') === `#${{currentId}}`) {{
        tab.classList.add('active');
      }}
    }});
  }});
}}

// --- 8. TOAST NOTIFICATIONS ---
function showToast(message) {{
  let container = document.querySelector('.toast-container');
  if (!container) {{
    container = document.createElement('div');
    container.className = 'toast-container';
    document.body.appendChild(container);
  }}

  const toast = document.createElement('div');
  toast.className = 'toast';
  toast.innerHTML = `<span>✨</span><span>${{message}}</span>`;
  container.appendChild(toast);

  setTimeout(() => {{
    toast.style.opacity = '0';
    toast.style.transform = 'translateY(10px)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }}, 3000);
}}
"""

with open(r"C:\Users\Luis Fernando Salas\.gemini\antigravity-ide\scratch\practica_pandas_web\app.js", "w", encoding="utf-8") as f:
    f.write(app_js_content)

print("app.js generado con éxito!")
