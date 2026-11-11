# 🏆 Resta Um: Filmes do Oscar

Uma aplicação web imersiva e interativa desenvolvida em **Python** com **Streamlit**, dedicada a celebrar e explorar a história dos indicados e vencedores da categoria principal do Oscar através de escolhas pessoais e torneios eliminatórios.

👉 **[Resta Um: Filmes do Oscar](https://resta-um-oscar.streamlit.app)**

## ✨ Funcionalidades

- **Seleção por Anos (1929-2026):** Navegue pelos anos da premiação do Oscar, visualize pôsteres oficiais e escolha o seu filme favorito entre os indicados de cada ano.
- **Barra de Progresso:** Acompanhe em tempo real quantos filmes já foram salvos e a porcentagem de conclusão da sua seleção.
- **Modo Mata-Mata:** Um torneio eliminatório estilo *Resta Um* para coroar o grande campeão entre os seus filmes salvos, com opções de chaveamento (Ordenado por Seleção ou Aleatório).
- **Histórico de Confrontos:** Acompanhe o chaveamento e o resumo de cada duelo rodada a rodada durante o torneio.
- **Design Exclusivo:** Interface polida com estética dark/gold clássica inspirada nas grandes noites de gala de Hollywood.

---

## 🛠️ Tecnologias Utilizadas

- **Python**
- **Streamlit** (Interface e gerenciamento de estado)
- **JSON** (Banco de dados de filmes e indicações desacoplado)
- **HTML5 / CSS3 Customizado** (Estilização avançada com efeitos de hover e responsividade)

---

## 📦 Estrutura de Arquivos

```text
├── data/
│   └── filmes_oscar.json  # Banco de dados estruturado com os filmes do Oscar e pôsteres
├── app.py                 # Código principal da aplicação Streamlit
├── requirements.txt       # Dependências do projeto para deploy
└── README.md              # Documentação do projeto
