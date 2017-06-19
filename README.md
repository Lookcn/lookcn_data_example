lookcn_data_example

# 生成数据库方法
安装 postgresql  
createdb lookcn

## 生成数据表
    CREATE EXTENSION pgcrypto;
    CREATE TABLE look_china
    (
        id UUID DEFAULT gen_random_uuid() PRIMARY KEY NOT NULL,
        info_json JSONB,
        create_date TIMESTAMP WITH TIME ZONE DEFAULT now(),
        write_date TIMESTAMP WITH TIME ZONE DEFAULT now()
    );
    CREATE UNIQUE INDEX look_china_id_uindex ON look_china (id);
    CREATE INDEX info_json_index ON look_china USING gin (info_json);

## 数据库查询 json 方法
    SELECT info_json->>'title' AS title FROM look_china WHERE info_json->>'author'='子文东';
