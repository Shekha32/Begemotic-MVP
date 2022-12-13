Begemotic MVP

The microservice implements two main methods based on information from the database:
1) '/radius_aggregation' - calculate aggregation within a radius of hexes from a point;
2) '/polygon_aggregation' - calculate the aggregation in the given polygon.

Used technologies: FastAPI, uvicorn, h3, GeoJSON, Pydantic, Docker-Compose.

How to run?

The project launch is in two parts: build and start.

Build:

        $ sudo docker-compose build


Launch:

        $ sudo docker-compose up

Stops containers and remove containers, images… created by docker-compose up:

        $ sudo docker-compose down

Lists containers:

        $ sudo docker-compose ps

Lists images:

        $ sudo docker-compose images

Examples of using:

After launch, you can use the functionality of the microservice by opening the link http://localhost:8000/docs

1)
        Request:
                curl -X 'GET' 'http://0.0.0.0:8000/' -H 'accept: application/json'
        Response:
                {"Hello": "Begemotic"}

2)
        Request:
                curl -X 'POST' \
                'http://localhost:8000/radius_aggregation' \
                -H 'accept: application/json' \
                -H 'Content-Type: application/json' \
                -d '{ "geometry": { "type": "Point", "coordinates": [37.517259, 55.542444] }, "field": "apartments", "aggr": "sum", "r": 4 }'
        Response:
                1501

3)
        Request:
                curl -X 'POST' \
                'http://localhost:8000/polygon_aggregation' \
                -H 'accept: application/json' \
                -H 'Content-Type: application/json' \
                -d '{ "geometry": { "type": "Polygon", "coordinates": [[ [37.520123, 55.54413], [37.515671, 55.54399], [37.514662, 55.541793], [37.521218, 55.542612],  [37.520123, 55.54413] ]] }, "field": "price", "aggr": "avg" }'
        Response:
                238302.85714285713
