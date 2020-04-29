-- extensão espacial para facilitar as consultas aos dados
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE sentinel_index (
    granule_id VARCHAR(200),
    product_id VARCHAR(200),
    datatake_identifier VARCHAR(200),
    mgrs_tile VARCHAR(200),
    sensing_time TIMESTAMP,
    total_size VARCHAR(50),
    cloud_cover REAL,
    geometric_quality_flag VARCHAR(200),
    generation_time TIMESTAMP,
    north_lat REAL,
    south_lat REAL,
    west_lon REAL,
    east_lon REAL,
    base_url VARCHAR(500)
);

CREATE TABLE landsat_index (
    scene_id VARCHAR(200),
    product_id VARCHAR(200),
    spacecraft_id VARCHAR(200),
    sensor_id VARCHAR(200),
    date_acquired DATE,
    collection_number VARCHAR(20),
    collection_category VARCHAR(200),
    sensing_time TIMESTAMP,
    data_type VARCHAR(200),
    wrs_path INTEGER,
    wrs_row INTEGER,
    cloud_cover REAL,
    north_lat REAL,
    south_lat REAL,
    west_lon REAL,
    east_lon REAL,
    total_size INTEGER,
    base_url VARCHAR(500)
);
