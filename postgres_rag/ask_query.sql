SELECT langchain_pg_collection.uuid AS langchain_pg_collection_uuid,
       langchain_pg_collection.name AS langchain_pg_collection_name,
       langchain_pg_collection.cmetadata AS langchain_pg_collection_cmetadata
FROM langchain_pg_collection
WHERE langchain_pg_collection.name = %(name_1) s:: VARCHAR
    LIMIT %(param_1) s:: INTEGER
    INFO:sqlalchemy.engine.Engine:[cached since 0.8485 s ago] {
    'name_1': 'ask_django_docs'
    , 'param_1': 1}
    INFO:sqlalchemy.engine.Engine:
SELECT langchain_pg_embedding.id            AS langchain_pg_embedding_id,
       langchain_pg_embedding.collection_id AS langchain_pg_embedding_collection_id,
       langchain_pg_embedding.embedding     AS langchain_pg_embedding_embedding,
       langchain_pg_embedding.document      AS langchain_pg_embedding_document,
       langchain_pg_embedding.cmetadata     AS langchain_pg_embedding_cmetadata,
       langchain_pg_embedding.embedding <=> %(embedding_1)s AS distance
FROM langchain_pg_embedding JOIN langchain_pg_collection
ON langchain_pg_embedding.collection_id = langchain_pg_collection.uuid
WHERE langchain_pg_embedding.collection_id = %(collection_id_1) s::UUID
ORDER BY distance ASC
    LIMIT %(param_1) s:: INTEGER
    INFO:sqlalchemy.engine.Engine:[generated in 0.00227 s] {
    'embedding_1': '[0.0011466781617060161,-0.012150052505765452,0.013489534704652115,-0.008943412822597847,-0.00741450845176939,0.015911427052851247,-0.0198622242375401 ... (32629 characters truncated) ... .02680317795794701,-0.03450181850347583,-0.010309955531331043,-0.009139599656339965,-0.006230622787516355,-0.011027052523005803,-0.03688312101822777]', 'collection_id_1': UUID('37ac9758-0fee-466d-9690-d61ce4e030b2'),
    'param_1': 1
    }

