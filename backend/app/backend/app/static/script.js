const submitBtn = document.getElementById('submitBtn');
const listBtn = document.getElementById('listBtn');
const messageLabel = document.getElementById('messageLabel'); 
const input = document.getElementById('usernameInput');
const rankingContainer = document.getElementById('rankingContainer');
const rankingList = document.getElementById('rankingList');

let blinkInterval = null;

// Envia o nome
async function sendUsername() {
    const username = input.value.trim();
    if (!username) {
        messageLabel.textContent = 'Por favor, digite um nome!';
        messageLabel.style.color = 'red';
        return;
    }

    try {
        const response = await fetch('/username', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username})
        });
        const data = await response.json();

        if (data.status === 'ok') {
            messageLabel.textContent = 'Nome enviado com sucesso!';
            messageLabel.style.color = 'lime';
            input.value = '';
            rankingContainer.style.display = 'none';
            rankingList.innerHTML = '';

            if (blinkInterval) {
                clearInterval(blinkInterval);
                blinkInterval = null;
                messageLabel.style.visibility = 'visible';
            }
        } else {
            messageLabel.textContent = 'Erro ao enviar nome.';
            messageLabel.style.color = 'red';
        }
    } catch {
        messageLabel.textContent = 'Falha na conexão!';
        messageLabel.style.color = 'red';
    }

    setTimeout(() => messageLabel.textContent = '', 3000);
}

submitBtn.addEventListener('click', sendUsername);

input.addEventListener('keydown', (e) => {
    if (e.key === 'Enter') sendUsername();
});

// Ranking + PDF
listBtn.addEventListener('click', async () => {
    try {
        const response = await fetch('/ranking');
        const data = await response.json();

        rankingList.innerHTML = '';
        data.forEach(player => {
            const li = document.createElement('li');
            li.textContent = `${player.username ?? 'Pending'} - ${player.score}`;
            rankingList.appendChild(li);
        });

        rankingContainer.style.display = 'flex';

        // === Gerar PDF ===
        const { jsPDF } = window.jspdf;
        const doc = new jsPDF();

        doc.setFontSize(18);
        doc.text("Ranking de Jogadores", 105, 20, null, null, "center");
        doc.setFontSize(12);

        let y = 40;
        data.forEach((player, index) => {
            const name = player.username ?? 'Pending';
            const score = player.score ?? 0;
            doc.text(`${index + 1}. ${name} - ${score} pts`, 20, y);
            y += 10;
        });

        // Download automático
        doc.save('ranking.pdf');

    } catch {
        messageLabel.textContent = 'Erro ao buscar ranking';
        messageLabel.style.color = 'red';
    }
});

// Checa jogadores pendentes
async function checkPending() {
    try {
        const response = await fetch('/search');
        const data = await response.json();

        if (data.pending && data.pending.length > 0) {
            messageLabel.textContent = 'Digite o nome do jogador!';
            messageLabel.style.color = 'red';

            if (!blinkInterval) {
                blinkInterval = setInterval(() => {
                    messageLabel.style.visibility =
                        messageLabel.style.visibility === 'hidden' ? 'visible' : 'visible';
                }, 500);
            }
        } else {
            if (blinkInterval) {
                clearInterval(blinkInterval);
                blinkInterval = null;
            }
            messageLabel.style.visibility = 'visible';
            messageLabel.textContent = '';
        }
    } catch {
        console.error('Erro ao checar jogadores pendentes');
    }
}

setInterval(checkPending, 2000);