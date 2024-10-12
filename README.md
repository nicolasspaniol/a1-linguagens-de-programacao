# a1-linguagens-de-programacao
Trabalho para a disciplina de Linguagens de Programação na FGV EMAp. Analisamos [dados de partidas de futebol](https://www.kaggle.com/datasets/davidcariboo/player-scores/data) coletados no Kaggle a fim de verificarmos e respondermos as seguintes hipóteses:

- Dentre os times visitantes de cada partida, jogar dentro ou fora do país influencia o resultado da partida? (vitória, empate ou derrota)
- Quais foram as compras de jogadores com melhores e piores custo-benefício registradas?
- A posição dos jogadores em campo influencia na quantidade de cartões que estes recebem?
- Vendas e compras posteriores de um jogador por um mesmo time costumam gerar lucro para o time?
- Jogadores com preço fora do comum tem o desempenho proporcional?
- Pessoas que nascem na primeira metade do ano tem mais chance de se tornarem jogadores profissionais?

## Testes unitários

Para rodar todos os testes, execute:
```bash
  PYTHONPATH=src python -m unittest discover tests 
```

Para rodar apenas um dos arquivos de teste, execute:
```bash
  PYTHONPATH=src python tests/test_[arquivo].py 
```
