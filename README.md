# 📍 Excel GeoMapper

Aplicativo interativo construído com **Streamlit**, **Folium**, **SQLite**, **LocationIQ** e **JavaScript personalizado** para transformar planilhas Excel com endereços e datas em **mapas de calor mensais e acumulados**.

---

## 🎯 Objetivo do Projeto

Este projeto surgiu da necessidade de **visualizar informações espaciais e temporais extraídas de planilhas**, como ocorrências, visitas ou eventos, com uma **interface simples para usuários não técnicos**, mas utilizando um backend robusto. 

A solução precisou integrar diversas ferramentas que, isoladamente, **não cobriam todos os requisitos**, exigindo soluções criativas e personalizadas ao longo do caminho.

---

## 🚀 Funcionalidades

- Upload de arquivos `.xlsx` ou `.xls`
- Detecção automática da linha de cabeçalho
- Seleção interativa das colunas de endereço, cidade, estado, país, data e descrição.
- Suporte a colunas fixas ou dinâmicas para estado e país
- Geocodificação automática via LocationIQ com fallback para edição manual
- Visualização prévia em mapa
- Geração de mapa de calor por mês e acumulado com **HeatMapWithTime**
- Clusterização por mês com **JavaScript customizado**
- **Exportação do mapa para um arquivo `heatMap.html`**, permitindo utilização externa
- Armazenamento local em SQLite com **persistência incremental**

---

---

## 🧩 Desafios Técnicos e Integração de Ferramentas

- **Streamlit** foi usado para construir a interface, mas não oferece suporte direto à visualização de mapas temporais interativos com Folium.
- **Folium**, apesar de poderoso, **não oferece uma API nativa para criar clustes dinâmicos separados por mês**, exigindo **injeção de código JavaScript customizado** no mapa final para complementar o comportamento.
- **LocationIQ** foi utilizado para geocodificar os endereços. No entanto, nem sempre todos os dados retornam com coordenadas completas, o que exigiu:
  - Adição de campos opcionais além de somente o endereço para que o usuário possa melhorar a confiabilidade das coordenadas.
  - Implementar uma etapa de **revisão e correção manual** dos dados no app.
  - Adicionar **retries automáticos e delays com tolerância a falhas** na API.
- Para manter os dados entre sessões e permitir expansão incremental do mapa, foi usado um **banco de dados SQLite** local. Isso permite:
  - Armazenar geolocalizações para reaproveitamento.
  - Continuar adicionando dados ao longo do tempo sem sobrescrever o mapa existente.

---

## 🛠️ Instalação

Clone o repositório:

```bash
git clone https://github.com/seu-usuario/excel-geomapper.git
cd excel-geomapper
```

Instale as dependências:
``` bash
pip install -r requirements.txt
```

Crie um conta [LocationIQ](https://locationiq.com/) e gere um token de API

Crie um arquivo `.env` com sua chave da LocationIQ:
```ini
TOKEN=sua_chave_locationiq
```

---

## ▶️ Como usar
Inicie o app com:
```bash
streamlit run main.py
```

Siga as etapas na interface:
1. Upload & Select: Envie seu arquivo Excel e selecione as colunas relevantes.
2. Geocoding: Veja uma prévia dos dados com coordenadas. Corrija manualmente se necessário.
3. Map: Gere o mapa de calor por mês e visualize no app.

---

## 💾 Armazenamento e Reutilização
- Os dados são armazenados localmente no arquivo geoloc.db (SQLite).
- O mapa gerado é salvo em heatMap.html, que pode ser aberto fora do Streamlit ou incorporado em outros sites.
- A cada nova execução com dados diferentes, os novos marcadores são adicionados ao banco de dados existente, enriquecendo o mapa com novas entradas.

## 🖼️ Exemplos de Uso
![opera_823UmsTmqo](https://github.com/user-attachments/assets/1b0cdcb4-1131-4f4f-9dc0-10ab309c3faa)
