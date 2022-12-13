
from pydantic.types import Union
from geojson import Point, Polygon
from pydantic import BaseModel, root_validator


#validation model
class Foo ( BaseModel ):
        
        geometry: Union[Point, Polygon]
        field: str
        aggr: str
        r: int = None

        @root_validator
        def check ( cls, values ) -> Union[dict, str]:

                if values [ 'field' ] not in [ "apartments", "price", "year" ]:
                        raise ValueError ( "ERROR: 'field' could be only 'apartments', 'price' or 'year'" )

                if values [ 'aggr' ] not in [ "min", "max", "sum", "avg" ]:
                        raise ValueError ( "ERROR: 'aggr' could be only 'min', 'max', 'sum' or 'avg'" )

                if values [ 'geometry' ] [ 'type' ] == "Point":
                        if values [ 'r' ] == None or values [ 'r' ] < 0:
                                raise ValueError ( "ERROR: 'r' could be only non-negative integer" )

                return values
