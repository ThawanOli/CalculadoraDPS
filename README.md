# Anime Astral DPS Calculator

O **Anime Astral DPS Calculator** é um painel tático web desenvolvido para otimizar o progresso de jogadores no modo incremental do jogo Anime Astral (Roblox). A ferramenta realiza o cálculo preciso de dano por segundo (DPS) e analisa automaticamente até qual onda o jogador consegue avançar em múltiplos modos de jogo.

---

##  Funcionalidades

- **Cálculo de DPS Real:** Suporte total para as fórmulas com ou sem o Gamepass *Fast Click* ($3.66\times$ ou $2.66\times$).
- **Suporte a Números Gigantes:** Interpretador inteligente de sufixos de escala curta (de Milhões `M` até potências extremas como `βH`).
- **Análise de Fronteira (Progresso Estimado):** Varre os requisitos do jogo em tempo real, indicando até onde o jogador limpa a fase e quanto falta de DPS para o próximo objetivo.
- **Barras de Progresso Visuais:** Feedback gráfico em porcentagem de conclusão para cada modo tático.
- **Calculadora Reversa:** Permite selecionar um objetivo específico (Wave/Room) na Wiki integrada para diagnosticar os requisitos de combate necessários.

---

##  Tecnologias Utilizadas

- **Python** (Lógica principal e processamento de dados)
- **Streamlit** (Interface web responsiva e moderna)
- **RegEx** (Expressões regulares para tratamento de strings e siglas gigantes)

---

##  Modos de Jogo Mapeados

O sistema conta com um banco de dados integrado contendo os requisitos de:
* Ninja Raid (Waves 5 a 100)
* Trial (Rooms 5 a 50)
* Titan Defense (Waves 5 a 80)
* Timeless Raid (Waves 5 a 50)
* Infinity Castle
* Gates (Rank E, D e C)

---

##  Como Rodar o Projeto Localmente

Se quiser clonar o repositório e executar na sua máquina:

1. Clone o repositório:
   ```bash
   git clone https://github.com/ThawanOli/CalculadoraDPS.git
2. Acesse a pasta do projeto:
   ```Bash
   cd CalculadoraDPS
3. Instale as dependências
   ```Bash
   pip install -r requirements.txt
4. Execute o servidor Streamlit
   ```Bash
   streamlit run CalculadoraDPS.py
## Autor
Desenvolvido por Thawan Oliveira

[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/thawanoliveira)