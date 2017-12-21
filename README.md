# TCCgo
O TCCgo é um analisador de TCC's baseado em regras gramaticais cadastradas por usuários. As regras são, em sua base, uma [expressão regular](https://en.wikipedia.org/wiki/Regular_expression), e a partir de um escaneamento do texto a partir dessas regras é possível encontrar possíveis erros muitas vezes difíceis de notar ao corrigir textos longos e desgastantes.

## Instalação
O TCCgo é uma plataforma web, que utiliza as tecnologias Django (framework da linguagem python, no programa utilizado para gerenciar o backend) e Angular JS (framework web, utilizado na configuração e apresentação do frontend), além das linguagens HTML, CSS, nativamente suportadas pelos Browsers. Assim, para executar o programa é necessário instalar as ferramentas necessárias.

Essa seção será um guia de instalação para se executar a aplicação nativamente e aproveitá-la. Considera-se nesse tutorial que o Sistema Operacional do computador pe Linux, baseado em Debian (de preferência o Ubuntu 16.04). Outros sistemas não serão abordados, porém os requisitos são de fácil instalação em geral.

#### Django
O Django é um framework do Python, sendo assim baixado pelo próprio gerenciador de pacotes da linguagem, o Pip. Portanto, será necessário inicialmente instalar (ou atualizar, pois muitos sistema Unix possuem nativamente o Python) a linguagem Python. Para isso, execute:
```
$ sudo apt-get install python3
```
A versão do Python é opcional, porém foi escolhida a versão 3 pois é a mais recente. Após a instalação do Python, é necessário instalar o gerenciador de pacotes:
```
$ sudo apt-get install python3-pip
```
Após a instalação do gerenciador, para que não haja conflito entre pacotes de python utilizados pelo Sistema Operacional e os pacotes utilizados pelo TCCgo, é necessário criar um ambiente virtual python. Esse ambiente funciona como um diretório a parte onde se pode instalar pacotes relacionados à linguagem sem que se altere os pacotes pré-existentes. A instalação do programa que cria ambiente é feita da seguinte forma:
```
$ sudo pip install virtualenv
```
Para criar um novo ambiente virtual, basta executar o comando:
```
$ cd ~
$ virtualenv -p python3 TCCgoEnv
```
Onde `TCCgoEnv` é o nome do ambiente virtual a ser criado, e o parâmetro `-p` específica a versão do Python a ser utilizada.

#### Ativando o ambiente virtual
Para ativar o ambiente (deve ser feito sempre que se deseja executar a aplicação), deve-se executar o arquivo `activate` da seguinte forma, dentro da pasta do ambiente virtual.
```
$ source bin/activate
```

#### Desativando o ambiente virtual
```
$ desactivate
```

### Dependências
Com o ambiente ativado, pode-se instalar o Django:
```
$ pip install django==1.11.5
```

### Criando um arquivo de dependências
Para facilitar a instalação, criamos um arquivo com as dependências do projeto, para atualiza-lo, basta executar o comando;
```
$ pip freeze > requirements.txt
```

### Instalando dependências
Dentro da pasta do projeto que contém o arquivo com as dependências, execute:
```
$ pip install -r requirements.txt
```

#### Código Fonte
Para se instalar o código fonte é necessário navegar até a pasta onde se deseja que ele fique e clonar o repositório que se encontra no git:
```
$ git clone https://github.com/andrelbol/TCCgo.git
```

## Execução
Após ativar o ambiente virtual execute o arquivo `manage.py` com o seguinte comando:
```
$ python TCCgo/manage.py runserver
```
Após isso, é possível acessar o aplicativo no endereço `localhost:8000`.
