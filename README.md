# a1-linguagens-de-programacao
Trabalho para a disciplina de Linguagens de Programação na FGV EMAp. Analisamos [dados de partidas de futebol](https://www.kaggle.com/datasets/davidcariboo/player-scores/data) coletados no Kaggle a fim de verificarmos e respondermos as seguintes hipóteses:

1. Há uma diferença na performance dos times quando estes jogam em casa, como visitantes e fora do país?
2. Quais foram as compras de jogadores com melhores e piores custo-benefício registradas?
3. A posição dos jogadores em campo influencia na quantidade de cartões que estes recebem?
4. Vendas e compras posteriores de um jogador por um mesmo time costumam gerar lucro para o time?
5. Jogadores com preço fora do comum tem o desempenho proporcional?

## Testes unitários

Para rodar todos os testes, execute:
```bash
  PYTHONPATH=src python -m unittest discover tests 
```

Para rodar apenas um dos arquivos de teste, execute:
```bash
  PYTHONPATH=src python tests/test_[arquivo].py 
```
