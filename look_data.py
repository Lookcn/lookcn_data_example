import json
import asyncio
import uvloop
import asyncpg
import datetime


DB_CONFIG = {
    'host': '127.0.0.1',
    'user': '*',
    'password': '*',
    'port': '5432',
    'database': 'lookcn'
}

NEED_LABEL = {'title': '标题',
              'url': 'url',
              'author': '作者',
              'latitude': '经度',
              'longitude': '纬度',
              'province_ab': '省份拼音首字母缩写',
              'province': '省份',
              'town_code': '区县代码',
              'town_name': '区县名称',
              'taga': 'A 组分类',
              'tagb': 'B',
              'tagc': 'C',
              'tagd': 'D',
              'tage': 'E',
              'commenta': '备注 1',
              'commentb': '备注 2',
              'updated': '是否更新',
              'lastModified': '最后一次修改时间',
              'contag': '根据标签生成的代码，用于地图 js 代码，生成规则参考 lookcn_data.xls 内容'
              }

loop = uvloop.new_event_loop()
asyncio.set_event_loop(loop)


async def mongodb_to_pg():
    pg_pool = await asyncpg.create_pool(**DB_CONFIG, loop=loop, max_size=100)
    async with pg_pool.acquire() as connection:
        datas = []
        mongodb_data = open('lookcn/lookchina.dat').readlines()
        for data in mongodb_data:
            data = json.loads(data)
            info_json = {key: value for key, value in data.items() if key in NEED_LABEL.keys()}
            last_modified = info_json.pop('lastModified')
            last_date = last_modified['$date']
            last_date = datetime.datetime.strptime(last_date, '%Y-%m-%dT%H:%M:%S.%fZ')
            datas.append({'info_json': info_json, 'create_date': last_date, 'write_date': last_date})
        datas.sort(key=lambda x: x['write_date'])
        for data in datas:
            info_json = json.dumps(data['info_json'])
            query = f"""INSERT INTO look_china (info_json, create_date, write_date) 
                        VALUES ('{info_json}', '{data['create_date']}', '{data['write_date']}')"""
            await connection.execute(query)

if __name__ == '__main__':
    loop.run_until_complete(mongodb_to_pg())
