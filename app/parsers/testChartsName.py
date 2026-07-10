import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[2]))

from app.db.motor import MongoConnection


async def main():
    mongo = MongoConnection("Charts")
    collection = mongo.get_collection("WDR")
    counter = 0

    async for document in collection.find():

        print(f"Chart Name: {document['name']}")

        for layer in document["layers"]:
            print(f"  Layer: {layer['name']}")
        
        counter += 1
        if counter ==3: break


asyncio.run(main())