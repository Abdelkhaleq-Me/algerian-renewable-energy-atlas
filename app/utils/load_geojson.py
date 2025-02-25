# app/utils/load_geojson.py
import geopandas as gpd
from shapely.geometry import MultiPolygon
from geoalchemy2 import WKTElement  # Import WKTElement
from app.extensions import db
from app.models.energy_models import AlgeriaWelayes, AlgeriaBoundary

def load_geojson(geojson_file, model):
    """Loads GeoJSON data into the database, handling geometry conversion."""
    gdf = gpd.read_file(geojson_file)

    if gdf.crs != 'epsg:4326':
        gdf = gdf.to_crs('epsg:4326')

    data = []
    for _, row in gdf.iterrows():
        geom = row.geometry
        if model == AlgeriaWelayes:
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon([geom])
            elif geom.geom_type != 'MultiPolygon':
                raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
            properties = row.drop('geometry').to_dict()
            wilaya_name = properties.get('name')  # Correct key
            if wilaya_name is None:
              wilaya_name = properties.get('ADM1_REF')
              if wilaya_name is None:
                raise ValueError("Could not find Wilaya name in GeoJSON properties.")

            # Convert Shapely geometry to WKTElement
            wkt_geom = WKTElement(geom.wkt, srid=4326)  # CRITICAL CHANGE

            data.append({
                'name': wilaya_name,
                'properties': properties,
                'geom': wkt_geom  # Insert the WKTElement
            })
        elif model == AlgeriaBoundary:
            if geom.geom_type != 'Polygon':
                raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
            properties = row.drop('geometry').to_dict()

            # Convert Shapely geometry to WKTElement
            wkt_geom = WKTElement(geom.wkt, srid=4326)  # CRITICAL CHANGE

            data.append({
                'properties': properties,
                'geom': wkt_geom  # Insert the WKTElement
            })

    with db.session.begin():
        db.session.bulk_insert_mappings(model, data)
    print(f"GeoJSON Data Load to {model.__tablename__} Complete")