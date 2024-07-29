Documentação detalhada para a API.

### Estrutura do Projeto

```
ifRefeicao/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reservation.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reservation.py
│   ├── crud/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reservation.py
│   │   ├── presence.py
│   ├── database.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── reservation.py
│   │   ├── admin.py
│   │   ├── vigia.py
│   ├── utils.py
├── requirements.txt
├── README.md
└── ... (outros arquivos de configuração e documentação)
```

### Descrição dos Módulos e Arquivos

#### Pasta `app`

Esta pasta contém todos os módulos principais da aplicação.

- **`__init__.py`**: Arquivo de inicialização do pacote. Pode ser vazio ou conter configuração inicial do pacote.
- **`main.py`**: Arquivo principal da aplicação FastAPI onde a instância da aplicação é criada e as rotas são incluídas.

#### Pasta `models`

Esta pasta contém as definições dos modelos de banco de dados usando SQLAlchemy.

- **`__init__.py`**: Arquivo de inicialização do pacote. Pode ser vazio ou conter configuração inicial do pacote.
- **`user.py`**: Define o modelo de usuário (`User`), incluindo campos como `matricula`, `nome_completo`, `is_interno`, e `is_admin`.
- **`reservation.py`**: Define o modelo de reserva (`Reservation`), incluindo campos como `user_id`, `meal_type`, `date`, `present`, e `canceled`.

#### Pasta `schemas`

Esta pasta contém as definições dos esquemas de dados usando Pydantic. Estes esquemas são usados para validação de entrada e saída.

- **`__init__.py`**: Arquivo de inicialização do pacote. Pode ser vazio ou conter configuração inicial do pacote.
- **`user.py`**: Define os esquemas para usuários (`UserCreate`, `User`, etc.).
- **`reservation.py`**: Define os esquemas para reservas (`ReservationCreate`, `Reservation`, etc.).

#### Pasta `crud`

Esta pasta contém funções de manipulação de banco de dados (Create, Read, Update, Delete).

- **`__init__.py`**: Arquivo de inicialização do pacote. Pode ser vazio ou conter configuração inicial do pacote.
- **`user.py`**: Contém funções CRUD para o modelo de usuário (`create_user`, `get_user`, `get_user_by_matricula`, `delete_user`, etc.).
- **`reservation.py`**: Contém funções CRUD para o modelo de reserva (`create_reservation`, `get_reservation`, `get_meal_count`, `cancel_reservation`, etc.).
- **`presence.py`**: Contém funções relacionadas à presença dos usuários (`get_present_users`, `mark_present`).

#### Pasta `routers`

Esta pasta contém os módulos que definem as rotas/endpoints da API.

- **`__init__.py`**: Arquivo de inicialização do pacote. Pode ser vazio ou conter configuração inicial do pacote.
- **`user.py`**: Define as rotas relacionadas aos usuários (`/users`).
- **`reservation.py`**: Define as rotas relacionadas às reservas (`/reservations`).
- **`admin.py`**: Define as rotas e a lógica para a interface de administração, incluindo WebSocket para contagem de presença.
- **`vigia.py`**: Define as rotas relacionadas à validação de presença por QR code.

#### Outros arquivos

- **`database.py`**: Contém a configuração do banco de dados e a função `get_db` para obter uma sessão do banco de dados.
- **`utils.py`**: Contém funções utilitárias, como a geração de QR codes (`generate_qr_code`).
- **`requirements.txt`**: Lista de dependências do projeto.
- **`README.md`**: Documentação geral do projeto.


### Descrição das Rotas

#### Rotas de Usuário (`/users`)

- **POST `/users/`**: Cria um novo usuário.
- **DELETE `/users/{user_id}`**: Deleta um usuário pelo `user_id`.

#### Rotas de Reserva (`/reservations`)

- **POST `/reservations/`**: Cria uma nova reserva.
- **GET `/reservations/{reservation_id}`**: Obtém os detalhes de uma reserva pelo `reservation_id`.
- **DELETE `/reservations/{user_id}/{reservation_id}`**: Cancela uma reserva pelo `user_id` e `reservation_id`.

#### Rotas de Administração (`/admin`)

- **GET `/admin`**: Interface de administração.
- **POST `/upload_csv/`**: Faz upload de um arquivo CSV para atualizar informações de usuários internos.
- **WebSocket `/ws`**: Conexão WebSocket para enviar contagens de presença, agendamentos e cancelamentos para a interface de administração.

#### Rotas de Vigia (`/vigia`)

- **GET `/vigia/validate/{qrcode}`**: Valida um QR code para confirmar a presença de um usuário.

### Executando o Projeto

Para executar o projeto, siga os passos abaixo:

1. **Criar e ativar um ambiente virtual:**

   ```bash
   python -m venv venv
   source venv/bin/activate  # ou `venv\Scripts\activate` no Windows
   ```

2. **Instalar as dependências:**

   ```bash
   pip install -r requirements.txt
   ```

3. **Iniciar o servidor FastAPI:**

   ```bash
   uvicorn app.main:app --reload
   ```

4. **Acessar a documentação da API:**

   Abra o navegador e vá para [http://localhost:8000/docs](http://localhost:8000/docs) para ver a documentação interativa da API.
