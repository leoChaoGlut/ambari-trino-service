from fabric import SerialGroup

result = SerialGroup(
    'dmp-trino-query1-001',
    'dmp-trino-query1-002',
    'dmp-trino-query1-003',
    'dmp-trino-query1-004',
    'dmp-trino-query2-001',
    'dmp-trino-query2-002',
    'dmp-trino-query2-003',
    'dmp-trino-query2-004',
).run('mkdir -p /data/trino/cache')

for res in result.items():
    print(res)
