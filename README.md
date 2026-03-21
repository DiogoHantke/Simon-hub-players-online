<img src="assets/banner_projeto.png" width="100%" alt="banner_projeto.png">

<h1>Simon Game Ranking System</h1>

<p>
Projeto desenvolvido como extensão do clássico <strong>Arduino Simon Game</strong>, agora com integração web
para cadastro de jogadores e armazenamento de pontuações. O site recebe as pontuações enviadas pelo firmware
do Simon (Arduino/ESP8266) e mantém um ranking atualizado.
</p>

<hr>

<h2>Participantes do Projeto</h2>
<ul>
    <li>Aparecido Orlando Virgili Neto</li>
    <li>Breno Souza Bernardi</li>
    <li>Bruno Travagli Sereço</li>
    <li>Daniel Lourenço Chereze Aparecida</li>
    <li>Diego Martins de Aquino</li>
    <li>Diogo Hantke Rodrigues Garcia</li>
    <li>Leticia Polatto de Novaes</li>
    <li>Luiz dos Santos Menino Neto</li>
    <li>Naiane Garcia da Silva</li>
    <li>Pedro Henrique Fuzaro Mori</li>
    <li>Rafael Rebolo Belarmino</li>
    <li>Samara Hélem Fonseca</li>
    <li>Thiago Augusto Savenhago</li>
    <li>Vinícius Souza Cardozo</li>
    <li>Wesley Mateus Basso</li>
</ul>

<hr>

<h2>Orientação</h2>
<ul>
    <li>Prof. Paulo Palota</li>
    <li>Prof. Ricardo Joaquim</li>
    <li>Prof. Cristiano Donizeti Ferrari</li>
</ul>

<hr>

<h2>Sumário</h2>
<ul>
    <li><a href="#pipeline">Pipeline Completo do Sistema</a></li>
    <li><a href="#sistema">Sistema de Arquivos</a></li>
    <li><a href="#execucao">Execução</a></li>
    <li><a href="#estrutura">Estrutura do Backend</a></li>
    <li><a href="#codigo">Explicação do Código</a></li>
    <li><a href="#melhorias">Melhorias Futuras</a></li>
    <li><a href="#objetivo">Objetivo Educacional</a></li>
</ul>

<hr>

<h2 id="pipeline">Pipeline Completo do Sistema</h2>

<p>O sistema é dividido em várias camadas, cada uma responsável por parte do fluxo de dados:</p>

<ol>
    <li><strong>Jogo Simon (Arduino)</strong>
        <ul>
            <li>O firmware <code>Simon.ino</code> roda no Arduino com LEDs, botões e buzzer.</li>
            <li>O jogador segue a sequência do Simon, e o Arduino calcula a pontuação ao final da partida.</li>
            <li>A pontuação é passada ao ESP8266 (via serial ou simulação) para envio ao backend.</li>
        </ul>
    </li>
    <li><strong>Envio de dados (ESP8266)</strong>
        <ul>
            <li>ESP8266 se conecta à mesma rede que o servidor web.</li>
            <li>Recebe ou simula pontuações via <code>ESP8266.ino</code> ou <code>simul.py</code>.</li>
            <li>Envio via HTTP POST em JSON para backend Python.</li>
        </ul>
    </li>
    <li><strong>Backend Web (Python + Flask)</strong>
        <ul>
            <li>Servidor Flask recebe requisições HTTP e renderiza interface.</li>
            <li>Chama funções do <code>servicesControl.py</code> para validar dados e atualizar ranking.</li>
            <li>Armazena informações no SQLite via <code>databaseControl.py</code>.</li>
        </ul>
    </li>
    <li><strong>Banco de Dados (SQLite)</strong>
        <ul>
            <li>Tabela <code>players</code> com <code>id</code>, <code>username</code> e <code>score</code>.</li>
            <li>Permite armazenamento persistente, consultas e ranking ordenado por pontuação.</li>
        </ul>
    </li>
    <li><strong>Interface Web</strong>
        <ul>
            <li>HTML + JavaScript exibindo ranking dinâmico e formulários para enviar nomes.</li>
            <li>Ranking pode ser baixado em PDF usando jsPDF.</li>
            <li>Mensagens de status para indicar quando há jogadores pendentes.</li>
        </ul>
    </li>
</ol>

<p><strong>Resumo:</strong> Arduino → ESP8266 → HTTP POST → Backend Flask → SQLite → Interface Web → Visualização e PDF do ranking.</p>

<hr>

<h2 id="sistema">Sistema de Arquivos</h2>
<pre>
.
├── backend/
│   └── app/
│       ├── database/
│       │   ├── databaseControl.py
│       │   ├── database.db
│       │   └── __pycache__/
│       ├── services/
│       │   ├── servicesControl.py
│       │   └── __pycache__/
│       ├── static/
│       │   ├── script.js
│       │   └── style.css
│       ├── templates/
│       │   └── index.html
│       ├── main.py
│       └── __init__.py
├── Hardware/
│   ├── ESP8266/
│   │   ├── ESP8266.ino
│   │   └── simul.py
│   └── Simon/
│       └── Simon.ino
└── README.md
</pre>

<hr>

<h2 id="execucao">Execução</h2>
<ol>
    <li>Instalar dependências Python: <code>Flask</code> (pip install flask) e sqlite3 (embutido).</li>
    <li>Executar backend:
        <pre><code>python3 backend/app/main.py</code></pre>
    </li>
    <li>Acessar o site via <code>http://localhost:5000</code>.</li>
    <li>ESP8266 envia dados de jogadores ao backend.</li>
    <li>Ranking é atualizado e exibido na interface web.</li>
</ol>

<hr>

<h2 id="estrutura">Estrutura do Backend</h2>
<ul>
    <li><strong>databaseControl.py</strong> — gerencia CRUD do SQLite.</li>
    <li><strong>servicesControl.py</strong> — lógica de registro de jogadores, pontuação e ranking.</li>
    <li><strong>main.py</strong> — servidor Flask, define rotas HTTP e renderiza templates.</li>
    <li><strong>templates/index.html</strong> — interface web do ranking.</li>
    <li><strong>static/script.js / style.css</strong> — comportamento dinâmico e estilo da página.</li>
</ul>

<hr>

<h2 id="codigo">Explicação Detalhada do Código</h2>

<h3>main.py</h3>
<p>Responsável por inicializar Flask, criar tabelas e definir rotas do sistema:</p>
<ul>
    <li><strong>createTables()</strong> — cria tabela <code>players</code> se não existir.</li>
    <li><strong>Rota "/"</strong> — renderiza <code>index.html</code>.</li>
    <li><strong>Rota "/score"</strong> — recebe JSON com <code>score_player</code>; chama <code>insertScore()</code>.</li>
    <li><strong>Rota "/username"</strong> — recebe JSON com <code>username</code>; chama <code>insertUsername()</code>.</li>
    <li><strong>Rota "/search"</strong> — retorna IDs de jogadores pendentes.</li>
    <li><strong>Rota "/ranking"</strong> — retorna ranking completo via <code>rankingGenerate()</code>.</li>
</ul>

<h3>servicesControl.py</h3>
<p>Lógica de manipulação de pontuação e nomes:</p>
<ul>
    <li><strong>insertScore(data)</strong>:
        <ul>
            <li>Checa se existe <code>score_player</code>.</li>
            <li>Se houver jogador pendente sem nome, retorna status "pause".</li>
            <li>Se não houver pendentes, insere score no DB e retorna "ok".</li>
        </ul>
    </li>
    <li><strong>insertUsername(data)</strong>:
        <ul>
            <li>Checa se existe <code>username</code>.</li>
            <li>Associa nome ao menor ID pendente no DB.</li>
            <li>Retorna "ok" ou "notPeding" se não houver IDs pendentes.</li>
        </ul>
    </li>
    <li><strong>searchPeding()</strong> — retorna lista de IDs pendentes.</li>
    <li><strong>rankingGenerate()</strong> — retorna ranking completo, ordenado por score decrescente.</li>
</ul>

<h3>databaseControl.py</h3>
<p>Gerenciamento do banco SQLite:</p>
<ul>
    <li><strong>createTables()</strong> — cria tabela <code>players</code> (id, username, score).</li>
    <li><strong>insertScoreDB(score)</strong> — insere nova pontuação sem nome.</li>
    <li><strong>GetPendingPlayersDB()</strong> — retorna IDs de jogadores sem username.</li>
    <li><strong>updateNameDB(idUser, username)</strong> — associa username a ID específico.</li>
    <li><strong>searchPlayersDB()</strong> — retorna lista de jogadores com username ordenada por score.</li>
</ul>

<h3>script.js</h3>
<p>Controla a interface web, envio de nomes, ranking e PDF:</p>
<ul>
    <li><strong>sendUsername()</strong> — envia nome ao backend via POST e mostra feedback.</li>
    <li><strong>checkPending()</strong> — consulta IDs pendentes a cada 2s e pisca mensagem.</li>
    <li><strong>Botão Ranking / PDF</strong> — busca ranking via GET, atualiza lista e gera PDF usando jsPDF.</li>
    <li>Interatividade: Enter envia nome; feedback visual com cores e piscamento de mensagem.</li>
</ul>

<hr>

<h2 id="melhorias">Melhorias Futuras</h2>
<ul>
    <li>Autenticação de jogadores.</li>
    <li>Gráficos de desempenho e histórico de pontuações.</li>
    <li>Interface responsiva e mobile-friendly.</li>
    <li>Conexão segura (HTTPS) para envio de pontuações.</li>
    <li>Leaderboard global com múltiplos dispositivos ESP8266.</li>
</ul>

<hr>

<h2 id="objetivo">Objetivo Educacional</h2>
<ul>
    <li>Integração de sistemas embarcados com aplicações web.</li>
    <li>Manipulação de bancos de dados SQLite via Python.</li>
    <li>Desenvolvimento de APIs simples para IoT.</li>
    <li>Design de interfaces web básicas e interativas.</li>
    <li>Compreensão de fluxo de dados de hardware para software em rede local.</li>
</ul>
