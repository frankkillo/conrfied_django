from sentinelsat import SentinelAPI, read_geojson, geojson_to_wkt, make_path_filter
import rasterio
import os
import os.path
import shutil


def get_product(api, footprint):
    """
    This func return products from Copernicus Open Access Hub API
    """
    resp = api.query(footprint,
        date=("NOW-1MONTH", "NOW"),
        platformname='Sentinel-2',
        processinglevel = 'Level-2A',
        limit=1,
        cloudcoverpercentage=(0, 5)
    )

    if resp:
        for prod in resp:
            oData = api.get_product_odata(prod)
            product = prod
            filename = oData["title"] + ".SAFE"

        return [product, filename]
    return

def get_ndvi(user, password, coords):
    """
    This function return filename of  NDVI image 
    """
    api = SentinelAPI(user, password, 'https://apihub.copernicus.eu/apihub')
    footprint = geojson_to_wkt(coords)
    product = get_product(api, footprint)

    if product:
        resp = None
        path_filter = make_path_filter("*IMG_DATA/R10m/*")
        api.download(product[0], directory_path="data/", nodefilter=path_filter)
        b4, b8 = '', ''
        for dir, dirs, files in os.walk("data/"+product[1]):
            for c in files:
                if c.endswith("_B04_10m.jp2"):
                    b4 = dir+"/"+c
                elif c.endswith("_B08_10m.jp2"):
                    b8 = dir+"/"+c
        if b4:
            b4 = rasterio.open(b4)
            b8 = rasterio.open(b8)
            # read Red(b4) and NIR(b8) as arrays
            red = b4.read()
            nir = b8.read()

            # Calculate ndvi
            ndvi = (nir.astype(float)-red.astype(float))/(nir+red)
            # Write the NDVI image
            meta = b4.meta
            meta.update(driver='GTiff')
            meta.update(dtype=rasterio.float32)

            with rasterio.open('data/NDVI.tif', 'w', **meta) as dst:
                dst.write(ndvi.astype(rasterio.float32))

            shutil.rmtree('data/'+product[1])
        
            resp = 'data/NDVI.tif'
        return resp
    return

        
if __name__ == "__main__":
    user = "frankkillo"
    password = "game-need-a-BREAK69"
    geo = 'map.geojson'

    get_ndvi(user, password, geo)