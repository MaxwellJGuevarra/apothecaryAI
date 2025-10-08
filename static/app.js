const fileInput = document.getElementById('csvFile');
const uploadBtn = document.getElementById('uploadBtn');
const resultsDiv = document.getElementById('results');

uploadBtn.onclick = async () => {
    if (!fileInput.files[0]) { alert('No file chosen'); return; }
  
    uploadBtn.disabled = true;
    uploadBtn.textContent = 'Analysing…';
  
    try {
      const form = new FormData();
      form.append('file', fileInput.files[0]);
  
      const res = await fetch('/audit/report', {method:'POST', body: form});
      if (!res.ok) throw new Error(`${res.status} ${res.statusText}`);
  
      const data = await res.json();
      showResults(data);
    } catch (err) {
      console.error(err);
      alert('Upload failed:\n' + err.message);
    } finally {
      uploadBtn.disabled = false;
      uploadBtn.textContent = 'Analyse';
    }
  };

function showResults(r) {
  resultsDiv.style.display = 'block';
  document.getElementById('totalRows').textContent = r.total_rows;
  document.getElementById('poisonRows').textContent  = r.poison_rows;
  document.getElementById('poisonPct').textContent   = r.poison_percent + ' %';

  const tbody = document.getElementById('sampleTable');
  tbody.innerHTML = '';
  r.sample_triggers.forEach(t => {
    const tr = document.createElement('tr');
    tr.innerHTML = `<td><code>${t}</code></td>`;
    tbody.appendChild(tr);
  });

  // tiny bar chart
  const ctx = document.getElementById('chart').getContext('2d');
  new Chart(ctx, {
    type: 'bar',
    data: {
      labels: ['Clean', 'Poison'],
      datasets: [{
        label: 'Rows',
        data: [r.total_rows - r.poison_rows, r.poison_rows],
        backgroundColor: ['#00d1b2','#ff3860']
      }]
    },
    options: {plugins:{legend:{display:false}}, scales:{y:{beginAtZero:true}}}
  });
}

fileInput.addEventListener('change', () => {
    const name = fileInput.files[0]?.name || 'Choose CSV…';
    uploadBtn.textContent = 'Analyse: ' + name;
  });