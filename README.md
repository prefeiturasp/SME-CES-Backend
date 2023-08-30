# SME-CES-Backend

Sistema de Pesquisas CES para Avaliação de Sentimento de Usuários em Ações de sistemas cadastrados.

# Descrição

Projeto de pesquisas baseado na metodologia CES (Customer Effort Score), projetado para coletar informações sobre o sentimento dos usuários em relação às ações executadas no sistema alvo. Com uma arquitetura flexível, a plataforma permite configurar quais ações específicas serão alvo de pesquisas, com a capacidade de integrar-se com diversos sistemas através de APIs.

# Recursos Principais:

Implementação da Metodologia CES: A plataforma emprega a metodologia Customer Effort Score (CES) para medir o esforço dos usuários em relação a ações específicas nos sistemas de cadastro, oferecendo insights sobre a experiência do usuário.

Configuração Flexível de Ações: Os administradores podem configurar quais ações ou eventos desejam avaliar, permitindo uma adaptação precisa às necessidades de coleta de informações.

Integração de Sistemas via API: A plataforma oferece uma API para integração direta com sistemas externos, possibilitando o envio de respostas de pesquisas e coleta de dados em tempo real.

Geração de Relatórios Detalhados: O sistema gera relatórios detalhados sobre o sentimento dos usuários, permitindo uma análise profunda das tendências, pontos de melhoria e a eficácia das ações tomadas.

Personalização de Perguntas: Os administradores podem personalizar as perguntas de pesquisa de acordo com as características de cada ação ou contexto.

## Tecnologias

- Django 4.2.4
- Django Admin
- Python 3.11
- PostgreSQL

## Instalação

1. Faça o clone do repositório.

2. Crie um ambiente virtual:

   ```
   python -m venv env
   ```

3. Ative o ambiente virtual:

   ```
   source venv/bin/activate
   ```

4. Instale as dependências:

   ```
   pip install -r requirements.txt
   ```

5. Crie um banco de dados PostgreSQL e configure as variáveis de ambiente para a conexão com o banco de dados.

6. Execute as migrações:

   ```
   python manage.py migrate
   ```

7. Crie um superusuário:

   ```
   python manage.py createsuperuser
   ```

8. Execute o servidor:

   ```
   python manage.py runserver
   ```
