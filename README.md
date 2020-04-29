# gcs-api

API de busca para os dados do Landsat-8 e Sentinel-2 (L2) no catálogo de imagens do Google Cloud Storage (GCS). 

A ferramenta está dividida em duas partes:

- `gcs_api`: API para a consulta dos dados
- `gcs_importer`: Ferramenta para baixar e inserir no banco de dados o índice de imagens do GCS

## Executando

- 1° Crie um banco de dados com as tabelas do arquivo `schema.sql`
- 2° Acesse o diretório `gcs_importer`, altere as informações do banco no `app.py` e execute;
- 3° Acesse o diretório do `gcs_api`, altere as informações do banco no `app.py` e execute.

## Exemplos de consulta

* Imagens em um retângulo envolvente dentro de um intervalo de tempo (Sentinel-2)

```shell
http://127.0.0.1:5000/api/images/sentinel/rangesearch?time=2019-11-01/2019-11-20&bbox=-0.489,51.28,0.236,51.686
```

* Imagens em um retângulo envolvente dentro de um intervalo de tempo (Landast)

```shell
http://127.0.0.1:5000/api/images/landsat/rangesearch?time=2019-11-01/2019-11-20&bbox=-0.489,51.28,0.236,51.686&platform=LANDSAT_8
```

Para o landsat é possível ainda adicionar o sensor

```shell
http://127.0.0.1:5000/api/images/landsat/rangesearch?time=2019-11-01/2019-11-20&bbox=-0.489,51.28,0.236,51.686&platform=LANDSAT_7&sensor=ETM
```

> Lembrando que o bbox da consulta é definido como bbox = min Longitude , min Latitude , max Longitude , max Latitude 

## Informações gerais

A relação de sensores e plataformas para consultas do Landsat é apresentado na tabela abaixo

| Plataforma | Sensor   |
|------------|----------|
| LANDSAT_2  | MSS      |
| LANDSAT_8  | TIRS     |
| LANDSAT_1  | MSS      |
| LANDSAT_8  | OLI      |
| LANDSAT_7  | ETM      |
| LANDSAT_5  | TM       |
| LANDSAT_4  | TM       |
| LANDSAT_3  | MSS      |
| LANDSAT_5  | MSS      |
| LANDSAT_4  | MSS      |
| LANDSAT_8  | OLI_TIRS |


> O código foi criado rapidamente para resolver um problema pontual, caso necessário, uma melhora pode ser feita no código posteriormente.
