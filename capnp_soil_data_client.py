import capnp
import data_services_capnp

def main():
    #address = parse_args().address

    client = capnp.TwoPartyClient("localhost:8000")

    data_services = client.bootstrap().cast_as(data_services_capnp.DataServices)

    text_prom = data_services.getText_request().send()
    text = text_prom.wait()

    gk_coord = data_services.getCoord_request().send().wait()

    req = data_services.getSoilDataService_request()
    req.id = 1
    sds_prom = req.send()
    sds = sds_prom.wait()
    soil_req = sds_prom.soilDataService.getSoilIdAt_request()
    soil_req.gkCoord.meridianNo = 5
    soil_req.gkCoord.r = 1000
    soil_req.gkCoord.h = 2000
    soilId_prom = soil_req.send()
    resp = soilId_prom.wait()
    
    print(resp.soilId)



if __name__ == '__main__':
    main()