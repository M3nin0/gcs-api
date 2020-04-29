import os, temp, urllib, shutil, requests, tqdm, warnings, tenacity, psycopg2

from psycopg2.extensions import connection
from urls import GOOGLE_INDEX_SENTINEL_L2, GOOGLE_INDEX_LANDSAT


def __download_file(url: str, file: str) -> None:
    """Função para baixar dados

    Args:
        url (str): URL do arquivo a ser baixado
        file (str): Arquivo onde os dados baixados serão salvos
    Returns:
        None
    """

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        with open(file, "wb") as f:
            pbar = tqdm.tqdm(ncols=100, unit_scale=True, unit="B",
                                leave=None, total=(int(r.headers['Content-Length'])))
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    pbar.update(len(chunk))
                    f.write(chunk)


def __extract_gzfile(file: str) -> str:
    """Função para a extração de dados .tar.gz

    Args:
        file (str): Caminho completo até o arquivo
    Returns:
        str: Caminho completo do arquivo criado na extração
    """

    import gzip

    with gzip.open(file, 'rb') as gfile:
        out = file.replace('.gz', '')
        with open(out, 'wb') as cfile:
            shutil.copyfileobj(gfile, cfile)
    return out


def __remove_firstline_in_file(file: str) -> str:
    """Remove a primeira linha do arquivo inserido

    Args:
        file (str): Caminho completo até o arquivo
    Returns:
        str: Caminho completo onde o arquivo criado será salvo
    """

    ofile = open(file, 'r')
    ofile.readline()
    return ofile


@tenacity.retry(stop=tenacity.stop_after_attempt(7), wait=tenacity.wait_fixed(5))
def download_and_import_google_image_index(conn: connection) -> None:
    """Função para baixar e importar o índice de imagens do Google para um banco de dados
    PostGres com extensão espacial

    Args:
        conn (connection): Conexão com o banco de dados onde os dados serão inseridos
    Returns:
        None
    """

    _tmp_dir = temp.tempdir()
    landsat_file = os.path.join(_tmp_dir, "landsat.csv.gz")
    sentinel_file = os.path.join(_tmp_dir, "sentinel_index_l2.csv.gz")

    __download_file(GOOGLE_INDEX_LANDSAT, landsat_file)
    __download_file(GOOGLE_INDEX_SENTINEL_L2, sentinel_file)

    # Extraíndo os dados
    sentinel_file_extracted = __extract_gzfile(sentinel_file)
    landsat_file_extracted = __extract_gzfile(landsat_file)

    try:
        cur = conn.cursor()
        cur.copy_from( __remove_firstline_in_file(landsat_file_extracted), "landsat_index", sep=",")
        cur.copy_from(__remove_firstline_in_file(sentinel_file_extracted), "sentinel_index", sep=",")
        conn.commit()
    except BaseException as error:
        warnings.warn(f"Problemas ao inserir os dados no banco: \n {str(error)}")
    shutil.rmtree(_tmp_dir, ignore_errors=True)
