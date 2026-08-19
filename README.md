# 🏠 Projeto de Consultoria Estatística

## Descrição

Este repositório reúne os materiais desenvolvidos na disciplina de Consultoria Estatística do Curso de Bacharelado em Estatística da Universidade Estadual da Paraíba (UEPB).

O projeto tem como objetivo desenvolver um sistema de apoio à precificação de imóveis utilizando técnicas de Estatística e Ciência de Dados.

Inicialmente, foram realizados o tratamento e a análise exploratória dos dados, seguidos do ajuste de Modelos Lineares Generalizados (MLG). Posteriormente, foi realizada uma etapa de validação preditiva comparando o Modelo Linear Generalizado (MLG) Gamma com o modelo Random Forest.

Como resultado da validação, o **Random Forest** apresentou melhor desempenho preditivo e foi selecionado como modelo final. A partir desse modelo, foram desenvolvidas uma API utilizando **FastAPI** e uma aplicação utilizando **Streamlit**, permitindo que o usuário estime o preço de venda de um imóvel a partir de suas características estruturais.

---

## Objetivos

- Realizar o tratamento e a limpeza da base de dados;
- Desenvolver uma análise exploratória dos dados;
- Ajustar Modelos Lineares Generalizados (MLG);
- Realizar a validação preditiva comparando o MLG Gamma e o Random Forest;
- Selecionar o modelo com melhor desempenho preditivo;
- Desenvolver uma API em FastAPI para disponibilizar o modelo preditivo;
- Desenvolver uma aplicação em Streamlit para estimativa automática do preço de imóveis;
- Disponibilizar o sistema on-line para acesso aos usuários.

---

## Base de dados

Foi utilizada a base **House Prices: Advanced Regression Techniques**, disponibilizada na plataforma Kaggle.

A base contém informações estruturais de imóveis residenciais localizados na cidade de Ames, Iowa (Estados Unidos), sendo o preço de venda (**SalePrice**) a variável resposta do estudo.

---

## Modelagem estatística e preditiva

Na etapa de modelagem foram ajustados Modelos Lineares Generalizados, incluindo os modelos com distribuições Gaussiana e Gamma.

Posteriormente, foi realizada uma validação preditiva comparando o **MLG Gamma** com o algoritmo de aprendizado de máquina **Random Forest**.

O desempenho dos modelos foi avaliado em uma base de teste composta por 20% das observações, não utilizadas no treinamento do modelo de validação.

O Random Forest apresentou melhor desempenho preditivo e, por isso, foi selecionado como modelo final para o desenvolvimento do sistema.

### Desempenho do modelo final

As principais métricas obtidas pelo Random Forest na base de teste foram:

- **RMSE:** 29.999,78
- **MAE:** 19.945,98
- **R²:** 0,8827

---

## Produto desenvolvido

Como produto final do projeto, foi desenvolvido um sistema on-line para estimativa do preço de venda de imóveis.

O sistema é composto por três elementos principais:

- **Streamlit:** interface utilizada pelo usuário para informar as características do imóvel e visualizar a estimativa;
- **FastAPI:** API responsável pela comunicação entre a aplicação e o modelo preditivo;
- **Random Forest:** modelo responsável por gerar a estimativa do preço de venda.

De forma simplificada, o funcionamento do sistema pode ser representado por:

**Usuário → Streamlit → FastAPI → Random Forest → Previsão**

O usuário informa as características do imóvel na aplicação. Essas informações são enviadas para a API, que utiliza o modelo Random Forest para realizar a previsão. O resultado é então devolvido à aplicação e apresentado ao usuário.

---

## Variáveis utilizadas na previsão

O modelo utiliza sete características do imóvel:

- **GrLivArea:** área construída acima do nível do solo;
- **OverallQual:** qualidade geral da construção e do acabamento;
- **GarageCars:** capacidade da garagem em número de veículos;
- **BedroomAbvGr:** número de quartos acima do nível do solo;
- **LotArea:** área total do terreno;
- **YearBuilt:** ano de construção do imóvel;
- **FullBath:** número de banheiros completos.

---

## API FastAPI

Foi desenvolvida uma API utilizando o framework **FastAPI** para disponibilizar o modelo preditivo.

A API possui os seguintes endpoints:

- `GET /health` — verifica o funcionamento da API e o carregamento do modelo;
- `GET /model-info` — apresenta informações sobre o modelo utilizado;
- `GET /metrics` — retorna as métricas de desempenho do modelo;
- `POST /predict` — realiza a previsão para um imóvel;
- `POST /predict-batch` — permite realizar previsões para múltiplos imóveis.

A API foi hospedada no **Render**, permitindo seu acesso pela internet.

---

## Aplicação Streamlit

A interface do sistema foi desenvolvida utilizando **Streamlit**.

Por meio da aplicação, o usuário pode:

- Informar as características estruturais de um imóvel;
- Visualizar um resumo das informações fornecidas;
- Solicitar a estimativa do preço de venda;
- Visualizar o preço estimado pelo modelo Random Forest;
- Consultar as métricas de desempenho do modelo.

---

## 🌐 Acesso ao sistema

### Aplicação Streamlit

https://projeto1consultoria-acgdwvmokbufm7dqmtwln5.streamlit.app

### API FastAPI — documentação

https://statistical-consultancy.onrender.com/docs

A aplicação e a API estão hospedadas on-line, permitindo que o sistema seja acessado por outros usuários sem a necessidade de execução local do projeto.

> **Observação:** devido às características do serviço de hospedagem utilizado para a API, o primeiro acesso após um período de inatividade pode apresentar um pequeno tempo de espera até que o serviço seja inicializado.

---

## Estrutura do projeto

```text
projeto_1_consultoria/

├── dados/
├── scripts/
├── relatorio/
├── apresentacao/
├── app/
├── api/
├── modelos/
├── imagens/
├── requirements.txt
└── README.md
```

---

## Como executar localmente

1. Clone o repositório;
2. Abra o projeto em um ambiente Python;
3. Instale as dependências presentes no arquivo `requirements.txt`;
4. Execute a API FastAPI;
5. Execute a aplicação Streamlit.

Para iniciar a aplicação Streamlit:

```bash
streamlit run app/app.py
```

Para utilização completa do sistema localmente, a API também deve estar em execução.

---

## Tecnologias utilizadas

- Python
- Pandas
- NumPy
- Scikit-learn
- Matplotlib
- Seaborn
- Plotly
- Streamlit
- FastAPI
- Uvicorn
- Git e GitHub
- Render

---

## Autoras

- Eduarda da Silva Brito
- Maria Helena
- Ana Maria

**Universidade Estadual da Paraíba – UEPB**  
Curso de Bacharelado em Estatística  
Disciplina: Consultoria Estatística  
Professor: Pedro Monteiro de Almeida Júnior
