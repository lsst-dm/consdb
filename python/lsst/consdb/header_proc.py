import asyncio
import json
import os
import random
import time
from typing import TYPE_CHECKING

import aiokafka
import httpx
import kafkit
from lsst.resources import ResourcePath
from sqlalchemy import create_engine, text

if TYPE_CHECKING:
    import lsst.resources

# Environment variables from deployment

kafka_cluster = os.environ["KAFKA_CLUSTER"]
schema_url = os.environ["SCHEMA_URL"]
db_url = os.environ["DB_URL"]
tenant = os.environ.get("BUCKET_TENANT", None)
kafka_group_id = 1

topic = "lsst.ATHeaderService.logevent_largeFileObjectAvailable"

engine = create_engine(db_url)


def process_resource(resource: lsst.resources.ResourcePath) -> None:
    content = json.loads(resource.read())
    with engine.begin() as conn:
        # TODO get all fields and tables, do as a transaction
        # conn.execute(
        #     text("INSERT INTO exposure (a, b, c, d, e)" " VALUES(:a, :b, :c, :d, :e)"),
        #     [dict(a=content["something"], b=2, c=3, d=4, e=5)],
        # )
        print(f"Processing {resource}: {content[0:100]}")
        # TODO check result


async def main() -> None:
    async with httpx.AsyncClient() as client:
        schema_registry = kafkit.registry.RegistryApi(client=client, url=schema_url)
        deserializer = kafkit.registry.Deserializer(registry=schema_registry)

        # Alternative 2:
        # Something like
        # asyncio.run(queue_check())

        consumer = aiokafka.AIOKafkaConsumer(
            topic,
            bootstrap_servers=kafka_cluster,
            group_id=kafka_group_id,
            auto_offset_reset="earliest",
        )
        await consumer.start()
        try:
            async for msg in consumer:
                message = (await deserializer.deserialize(msg.value)).message
                resource = ResourcePath(message.url)
                if tenant:
                    new_scheme = resource.scheme
                    new_netloc = f"{tenant}:{resource.netloc}"
                    new_path = resource.path
                    resource = ResourcePath(f"{new_scheme}://{new_netloc}/{new_path}")
                # Alternative 1: block for file
                while not resource.exists():
                    time.sleep(random.uniform(0.1, 2.0))
                process_resource(resource)

                # Alternative 2: queue
                # r.sadd("EXPOSURE_QUEUE", str(resource))

        finally:
            await consumer.stop()


# Alternative 2:
# async def queue_check():
#     resource_list = r.slist("EXPOSURE_QUEUE", 0, -1)
#     for resource in resource_list:
#         if r.exists():
#             process_resource(resource)
#             r.sremove("EXPOSURE_QUEUE", resource)

asyncio.run(main())
