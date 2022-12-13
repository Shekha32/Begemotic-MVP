
#MAIN

import json
from fastapi import FastAPI
from pydantic.types import Union

from app.schema import Foo
from app.begemotic import Begemotic


begemotic = Begemotic()
app = FastAPI()


#just for check
@app.get ( "/" )
async def hello_begemotic() -> dict:
        return { "Hello": "Begemotic" }


#radius aggregation
@app.post ( "/radius_aggregation" )
async def radius_aggregation ( data: Foo ) -> Union[int, float, str]:
        return await begemotic.radius_aggregation ( json.loads ( data.json() ) )


#polygon aggregation
@app.post ( "/polygon_aggregation" )
async def polygon_aggregation ( data: Foo ) -> Union[int, float, str]:
        return await begemotic.polygon_aggregation ( json.loads ( data.json() ) )
