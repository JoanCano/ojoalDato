import json
from shapely.geometry import shape
import requests
import csv

georeferencedfile = "georeferencedSample.csv"

if __name__ == "__main__":
    with open("trayecto_usuario_2018.csv") as m:
        muestra = csv.reader(m, delimiter=";")
        with open("estacionesBiZi.csv") as e:
            estaciones = csv.reader(e, delimiter=",")

            stationCoords = {}

            for row in estaciones:
                if row[2] != "ref":
                    stationCoords[int(row[2])] = {"x": float(row[0]), "y": float(row[1])}

            final_rows = []
            firstRow = True

            for row in muestra:
                auxrow = row
                if not firstRow:
                    x1 = stationCoords[int(row[4])]["x"]
                    y1 = stationCoords[int(row[4])]["y"]
                    x2 = stationCoords[int(row[6])]["x"]
                    y2 = stationCoords[int(row[6])]["y"]
                    auxrow.append(x1)
                    auxrow.append(y1)
                    auxrow.append(x2)
                    auxrow.append(y2)
                    call = requests.get(
                        "http://sid03.cps.unizar.es:7000/route/v1/cycling/"
                        + str(x1) + "," + str(y1) + ";" + str(x2) + "," + str(y2)
                        + "?steps=false&geometries=geojson")
                    geom = json.loads(call.text)["routes"][0]["geometry"]
                    s = shape(geom)
                    auxrow.append(s.wkt)
                else:
                    auxrow.append("x1")
                    auxrow.append("y1")
                    auxrow.append("x2")
                    auxrow.append("y2")
                    auxrow.append("lineroute")
                    firstRow = False
                final_rows.append(auxrow)

            with open("georeferencedSample.csv", "w") as f:
                gfwriter = csv.writer(f, delimiter=";")
                for row in final_rows:
                    gfwriter.writerow(row)
