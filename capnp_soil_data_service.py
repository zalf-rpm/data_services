
from scipy.interpolate import NearestNDInterpolator
import numpy as np

#import argparse
import capnp
import data_services_capnp

def read_header(path_to_ascii_grid_file):
    "read metadata from esri ascii grid file"
    metadata = {}
    header_str = ""
    with open(path_to_ascii_grid_file) as _:
        for i in range(0, 6):
            line = _.readline()
            header_str += line
            sline = [x for x in line.split() if len(x) > 0]
            if len(sline) > 1:
                metadata[sline[0].strip().lower()] = float(sline[1].strip())
    return metadata, header_str

def create_ascii_grid_interpolator(arr, meta, ignore_nodata=True):
    "read an ascii grid into a map, without the no-data values"

    rows, cols = arr.shape

    cellsize = int(meta["cellsize"])
    xll = int(meta["xllcorner"])
    yll = int(meta["yllcorner"])
    nodata_value = meta["nodata_value"]

    xll_center = xll + cellsize // 2
    yll_center = yll + cellsize // 2
    yul_center = yll_center + (rows - 1)*cellsize

    points = []
    values = []

    for row in range(rows):
        for col in range(cols):
            value = arr[row, col]
            if ignore_nodata and value == nodata_value:
                continue
            r = xll_center + col * cellsize
            h = yul_center - row * cellsize
            points.append([r, h])
            values.append(value)

    return NearestNDInterpolator(np.array(points), np.array(values))

class SoilDataService(data_services_capnp.SoilDataService.Server):
    "Implementation of SoilDataService Cap'n Proto interface."

    def __init__(self, path_to_soil_grid):
        
        soil_metadata, _ = read_header(path_to_soil_grid)
        soil_grid = np.loadtxt(path_to_soil_grid, dtype=int, skiprows=6)
        self.soil_gk5_interpolate = create_ascii_grid_interpolator(soil_grid, soil_metadata)
        print("read: ", path_to_soil_grid)

    def getSoilIdAt(self, gkCoord, _context, **kwargs):
        return 5


class DataServicesImpl(data_services_capnp.DataServices.Server):
    "Implementation of the DataServices Cap'n Proto interface."

    def __init__(self, path_to_data_dir):
        #pass
        self.soil_data_service_instance = SoilDataService(path_to_data_dir + "germany/buek1000_1000_gk5.asc")

    def getAvailableSoilDataServices(self, _context, **kwargs): 
        msg = data_services_capnp.SoilDataServiceInfo.new_message()
        msg.id = 1
        msg.name = "BUEK1000"
        msg.service = self.soil_data_service_instance
        return [msg]
    
    def getSoilDataService(self, id, _context, **kwargs): 
        return self.soil_data_service_instance

    def getCoord(self, _context, **kwargs):
        #coord = data_services_capnp.GKCoord.new_message(meridianNo=5, r=1, h=2)
        return {"meridianNo": 5, "r": 1, "h": 2} 

    def getText(self, _context, **kwargs):
        return "bla"

    #def evaluate(self, expression, _context, **kwargs):
    #    return evaluate_impl(expression).then(lambda value: setattr(_context.results, 'value', ValueImpl(value)))

    #def defFunction(self, paramCount, body, _context, **kwargs):
    #    return FunctionImpl(paramCount, body)

    #def getOperator(self, op, **kwargs):
    #    return OperatorImpl(op)



def main():
    #address = parse_args().address

    server = capnp.TwoPartyServer("*:8000", bootstrap=DataServicesImpl("/home/berg/archive/data/"))
    server.run_forever()

if __name__ == '__main__':
    main()