SEA (Sistema de Enxame Adaptativo) - Manual de Operação e Instalação v2.1
Visão Geral
Este manual detalha todos os passos necessários para instalar, configurar e operar a plataforma de Comando e Controle (C2) do Sistema de Enxame Adaptativo (SEA). O sistema é composto por um Backend (o cérebro em Python que gerencia os drones) e um Frontend (a interface visual baseada em web para o operador).
Pré-requisitos de Software
Antes de começar, certifique-se de que os seguintes softwares estão instalados em sua máquina:
Python (versão 3.8 ou superior):
Download: https://www.python.org/downloads/
Importante: Durante a instalação no Windows, marque a caixa "Add Python to PATH".
Git:
Download: https://git-scm.com/downloads
Utilizado para obter o código-fonte do projeto.
Um navegador web moderno: Google Chrome ou Mozilla Firefox são recomendados.
Parte 1: Instalação e Configuração Inicial (Executar apenas uma vez)
Passo 1: Obter o Código-Fonte
Abra um terminal (PowerShell ou CMD no Windows, Terminal no macOS/Linux) e execute o seguinte comando para clonar o repositório do projeto para sua máquina.
Generated bash
git clone https://github.com/seu-usuario/SEA_Prototype.git
Use code with caution.
Bash
(Nota: Substitua a URL pelo link real do seu repositório Git.)
Após a conclusão, um novo diretório chamado SEA_Prototype será criado.
Passo 2: Navegar até o Diretório do Projeto
Use o comando cd (change directory) para entrar na pasta raiz do projeto. Todos os comandos seguintes devem ser executados a partir deste local.
Generated bash
cd SEA_Prototype
Use code with caution.
Bash
Passo 3: Configurar o Ambiente e Instalar as Dependências do Backend
Para manter o projeto isolado, criaremos um ambiente virtual.
Navegue até a pasta do backend:
Generated bash
cd backend
Use code with caution.
Bash
Crie o ambiente virtual (venv):
Generated bash
python -m venv venv
Use code with caution.
Bash
Ative o ambiente virtual:
No Windows (PowerShell):
Generated powershell
.\venv\Scripts\Activate.ps1
Use code with caution.
Powershell
(Se encontrar um erro de execução de script, talvez precise executar Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass e tentar novamente.)
No macOS ou Linux:
Generated bash
source venv/bin/activate
Use code with caution.
Bash
Seu prompt de terminal deve agora exibir (venv) no início da linha.
Instale todas as bibliotecas Python necessárias:
Generated bash
pip install "fastapi[all]" uvicorn djitellopy shapely
Use code with caution.
Bash
Volte para a pasta raiz do projeto:
Generated bash
cd ..
Use code with caution.
Bash
A instalação está completa.
Parte 2: Execução da Aplicação
Siga estes passos toda vez que quiser rodar o sistema SEA.
Passo 1: Iniciar o Servidor Backend
Verifique se você está na pasta raiz do projeto (SEA_Prototype).
Ative o ambiente virtual (se você abriu um novo terminal):
No Windows: .\backend\venv\Scripts\Activate.ps1
No macOS/Linux: source backend/venv/bin/activate
Execute o servidor Uvicorn com o seguinte comando:
Generated bash
python -m uvicorn backend.api.main_api:app --reload
Use code with caution.
Bash
O terminal deverá exibir uma saída parecida com esta, indicando que o servidor está rodando:
Generated code
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [xxxxx]
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     SEA C2 Server Initialized. Awaiting connections...
INFO:     Application startup complete.
Use code with caution.
Deixe este terminal aberto. Ele é o cérebro do sistema.
Passo 2: Abrir a Interface do Operador (Frontend)
Abra o seu explorador de arquivos.
Navegue até a pasta SEA_Prototype/frontend/.
Dê um duplo clique no arquivo index.html para abri-lo no seu navegador padrão.
Passo 3: Verificar a Conexão
No seu navegador, a interface do SEA deve carregar. No painel "Log de Eventos", a primeira mensagem deve ser [hh:mm:ss] Conectado à Plataforma SEA..
No seu terminal do backend, você deverá ver uma nova linha de log: INFO: 127.0.0.1:xxxxx - "WebSocket /ws" [accepted].
Se você vir essas duas mensagens, o sistema está totalmente operacional.
Parte 3: Manual de Operação da Interface
Visão Geral da Tela
Mapa: A área principal onde a posição dos drones e alvos são exibidos.
Painel de Controle (à direita): Contém os comandos globais e os painéis de status.
Status do Enxame: Uma lista de todos os drones, mostrando sua ID, status atual e nível de bateria. A cor à esquerda indica o status.
Log de Eventos: Um registro em tempo real de todas as ações e mudanças de status importantes.
Comandos Disponíveis
DECOLAR ENXAME:
Ação: Envia um comando de decolagem para todos os drones que estão no estado "Landed".
Resultado Esperado: Os drones na lista de status mudarão para "TakingOff" e, em seguida, para "Idle" (pairando no ar).
POUSAR ENXAME:
Ação: Envia um comando de pouso para todos os drones que estão no ar.
Resultado Esperado: Os drones mudarão de status para "Landing" e, em seguida, para "Landed".
DEFINIR ALVO GO-TO:
Ação: Clique com o botão direito do mouse em qualquer ponto do mapa.
Resultado Esperado: Um ícone de alvo vermelho aparecerá no local clicado. Um comando será enviado para que todos os drones voadores se desloquem em direção a esse ponto. O status deles mudará para "Moving". Ao chegarem, mudarão para "Idle".
Parte 4: Solução de Problemas Comuns
Problema: Ao rodar python ..., recebo o erro 'python' não é reconhecido...
Solução: O Python não foi adicionado ao PATH do sistema. Reinstale o Python, garantindo que a caixa "Add Python to PATH" esteja marcada.
Problema: A página do frontend carrega, mas diz "Falha ao conectar" e o Log de Eventos mostra erros.
Solução: O servidor backend não está rodando. Verifique o terminal onde você executou o comando uvicorn. Ele deve estar ativo e sem mensagens de erro. Se ele fechou, inicie-o novamente.
Problema: Ao rodar uvicorn... ou python -m backend.test_script, recebo ImportError ou ModuleNotFoundError.
Solução 1: Verifique se o seu ambiente virtual (venv) está ativo.
Solução 2: Verifique se você está executando o comando a partir da pasta raiz do projeto (SEA_Prototype), e não de dentro da pasta backend.
