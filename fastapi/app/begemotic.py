
import h3
import csv
from pydantic.types import Union

from app.schema import Foo


class Begemotic():

        #constructor
        def __init__ ( self ) -> None:

                self.__hex_list = {}                            #dict {hex: [apartments id's list]}
                self.__apartments = {}                          #dict {apartment id: {apartment info}}
                self.__is_dict = False                          #sign of created dicts
                self.__file_path = "./app/data/apartments.csv"


        #destructor
        def __del__ ( self ) -> None:

                self.__is_dict = False
                self.__hex_list.clear()
                self.__apartments.clear()


        #creation of dicts with apartments info
        def __create_dict ( self ) -> None:
                
                with open ( self.__file_path, mode='r' ) as file:

                        keys = file.readline().split ( "," )            #extracting keys to create a dict
                        keys [ -1 ] = keys [ -1 ].rstrip()              #remove '\n' from the last field of a line
                        reader = csv.reader ( file )

                        for row in reader:

                                item = {}
                                coordinates = eval ( row [ 1 ] ) [ 'coordinates' ]                              #extracting apartments coordinates
                                hex = h3.geo_to_h3 ( coordinates [ 1 ], coordinates [ 0 ], resolution=11 )      #getting the hex that owns the apartment
                                [ item.update ( { keys [ ind ]: row [ ind ] } ) for ind in range ( 1, len ( keys ) ) ]
                                self.__apartments.update ( { row [ 0 ]: item } )                                #creating a dict with all info about apartments

                                if hex not in self.__hex_list.keys():
                                        self.__hex_list [ hex ] = [ row [ 0 ] ]
                                else:
                                        self.__hex_list [ hex ].append ( row [ 0 ] )
                
                self.__is_dict = True


        #calculation
        async def __calculate ( self, mas: list, aggr: str ) -> Union[int, float]:

                d = {
                        'min': min ( mas ),
                        'max': max ( mas ),
                        'sum': sum ( mas ),
                        'avg': sum ( mas ) / len ( mas )
                }

                return d [ aggr ] #if aggr in d.keys() else 'calculate_error'


        #aggregation - search for the required elements
        async def __aggregation ( self, data: dict, area: set ) -> Union[int, float, str]:

                mas = []

                for hex in area:

                        if hex not in self.__hex_list.keys():
                                continue
                        else:
                                for id in self.__hex_list [ hex ]:

                                        field = self.__apartments [ id ] [ data [ 'field' ] ]
                                        field = float ( field ) if field.find ( "." ) != -1 else int ( field )
                                        mas.append ( field )

                return await self.__calculate ( mas, data [ 'aggr' ] ) if len ( mas ) else 'no results in specified area'


        #radius aggregation - calculate aggregation within r hex radius from given point
        async def radius_aggregation ( self, data: Foo ) -> Union[int, float, str]:

                if not self.__is_dict:
                        self.__create_dict()

                coordinates = data [ 'geometry' ] [ 'coordinates' ]
                hex = h3.geo_to_h3 ( coordinates [ 1 ], coordinates [ 0 ], resolution=11 )
                area = h3.k_ring ( hex, k=data [ 'r' ] )

                return await self.__aggregation ( data, area )


        #polygon aggregation - calculate of aggregation in a given polygon
        async def polygon_aggregation ( self, data: Foo ) -> Union[int, float, str]:

                if not self.__is_dict:
                        self.__create_dict()

                [ item.reverse() for item in data [ 'geometry' ] [ 'coordinates' ] [ 0 ] ]
                area = h3.polyfill ( data [ 'geometry' ], res=11 )

                return await self.__aggregation ( data, area )
