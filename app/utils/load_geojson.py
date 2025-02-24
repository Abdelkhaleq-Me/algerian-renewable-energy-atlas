import geopandas as gpd
from shapely.geometry import MultiPolygon
from app.extensions import db
from app.models.energy_models import AlgeriaWelayes, AlgeriaBoundary
from app import create_app  # Import create_app function

def load_geojson(geojson_file, model):
    """Loads GeoJSON data into the database."""

    # Read the GeoJSON file with GeoPandas
    gdf = gpd.read_file(geojson_file)

    # Ensure the GeoDataFrame is in EPSG:4326
    if gdf.crs != 'epsg:4326':
        gdf = gdf.to_crs('epsg:4326')

    # Convert the GeoDataFrame to a list of dictionaries, handling geometries
    data = []
    for _, row in gdf.iterrows():
        # Use GeoAlchemy2's WKBElement for geometry
        geom = row.geometry
        if model == AlgeriaWelayes:
            # Ensure the geometry is a MultiPolygon
            if geom.geom_type == 'Polygon':
                geom = MultiPolygon([geom])  # Wrap single Polygon in a MultiPolygon
            elif geom.geom_type != 'MultiPolygon':
                raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
            properties = row.drop('geometry').to_dict()  # All columns except geometry

            # Get the wilaya name correctly
            # Adjust this line based on the actual column name in your GeoJSON
            wilaya_name = properties.get('NAME_1')  # Or whatever the correct key is
            if wilaya_name is None:
              wilaya_name = properties.get('ADM1_REF') #IF NAME_1 doesn't work
              if wilaya_name is None:
                raise ValueError("Could not find Wilaya name in GeoJSON properties.")

            data.append({
                'name': wilaya_name,
                'properties': properties,
                'geom': geom
            })
        elif model == AlgeriaBoundary:
            # Ensure the geometry is a Polygon (as per model definition)
            if geom.geom_type != 'Polygon':
                raise ValueError(f"Unexpected geometry type: {geom.geom_type}")
            properties = row.drop('geometry').to_dict()
            data.append({
                'properties': properties,
                'geom': geom
            })

    # Use SQLAlchemy's bulk insert (efficient for large datasets)
    with db.session.begin():
        db.session.bulk_insert_mappings(model, data)
    print(f"GeoJSON Data Load to {model.__tablename__} Complete")


if __name__ == '__main__':
    # Create a Flask app context so we can use the database.
    app = create_app()
    with app.app_context():
        db.create_all()  # Create tables if they don't exist

        # --- IMPORTANT: Adjust file paths below! ---
        load_geojson('app/utils/algeria_welayes.json', AlgeriaWelayes)  # Correct path
        load_geojson('app/utils/algeria_boundry.json', AlgeriaBoundary)  # Correct path
    print("Data loading process complete.")