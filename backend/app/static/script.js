const submitBtn = document.getElementById('submitBtn');
const listBtn = document.getElementById('listBtn');
const messageLabel = document.getElementById('messageLabel');
const input = document.getElementById('usernameInput');
const rankingContainer = document.getElementById('rankingContainer');
const rankingList = document.getElementById('rankingList');

let blinkInterval = null;

function showMessage(text, color = 'red') {
  messageLabel.textContent = text;
  messageLabel.style.color = color;
  messageLabel.style.visibility = 'visible';
}

function stopBlink() {
  if (blinkInterval) {
    clearInterval(blinkInterval);
    blinkInterval = null;
  }
  messageLabel.style.visibility = 'visible';
}

function startBlink() {
  if (blinkInterval) {
    return;
  }

  blinkInterval = setInterval(() => {
    messageLabel.style.visibility =
      messageLabel.style.visibility === 'hidden' ? 'visible' : 'hidden';
  }, 500);
}

async function sendUsername() {
  const username = input.value.trim();

  if (!username) {
    showMessage('Por favor, digite um nome!', 'red');
    return;
  }

  try {
    const response = await fetch('/username', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username })
    });

    const data = await response.json();

    if (response.ok && data.status === 'ok') {
      showMessage('Nome enviado com sucesso!', 'lime');
      input.value = '';
      stopBlink();
      await loadRanking();
      await checkPending();
    } else if (data.status === 'notPending') {
      showMessage('Não há jogador pendente agora.', 'orange');
    } else {
      showMessage('Erro ao enviar nome.', 'red');
    }
  } catch (error) {
    showMessage('Falha na conexão!', 'red');
  }
}

function renderRanking(data) {
  rankingList.innerHTML = '';

  if (!Array.isArray(data) || data.length === 0) {
    const li = document.createElement('li');
    li.textContent = 'Nenhum jogador cadastrado ainda.';
    rankingList.appendChild(li);
    return;
  }

  data.forEach((player, index) => {
    const li = document.createElement('li');
    const name = player.username ?? 'Pendente';
    const score = player.score ?? 0;
    li.textContent = `${index + 1}. ${name} - ${score} pts`;

    if (index === 0) li.classList.add('first-place');
    else if (index === 1) li.classList.add('second-place');
    else if (index === 2) li.classList.add('third-place');

    rankingList.appendChild(li);
  });
}

async function loadRanking() {
  const response = await fetch('/ranking');
  const data = await response.json();
  renderRanking(data);
}

submitBtn.addEventListener('click', sendUsername);
input.addEventListener('keydown', (e) => {
  if (e.key === 'Enter') sendUsername();
});

listBtn.addEventListener('click', async () => {
  if (rankingContainer.style.display === 'flex') {
    rankingContainer.style.display = 'none';
    return;
  }

  try {
    await loadRanking();
    rankingContainer.style.display = 'flex';
  } catch (error) {
    showMessage('Erro ao buscar ranking', 'red');
  }
});

async function checkPending() {
  try {
    const response = await fetch('/search');
    const data = await response.json();

    if (data.pending && data.pending.length > 0) {
      showMessage('Jogador pendente!', 'red');
      startBlink();
    } else {
      stopBlink();
      messageLabel.textContent = '';
    }
  } catch (error) {
    console.error('Erro ao checar jogadores pendentes');
  }
}

setInterval(checkPending, 2000);
checkPending();
