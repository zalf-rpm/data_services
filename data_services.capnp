@0xd3f8859c7688b76b;

using Date = import "date.capnp".Date;
using Geo = import "geo_coord.capnp".Geo;

struct SoilDataServiceInfo {
  id @0 :UInt64;
  name @1 :Text;
  description @2 :Text;
  service @3 :SoilDataService;
}

interface SoilDataService {
  getSoilIdAt @0 (gkCoord :Geo.GKCoord) -> (soilId :Int64);
}

interface DataServices {
  # the bootstrap interface to the different data services

  getAvailableSoilDataServices @0 () -> (availableSoilDataServices :List(SoilDataServiceInfo));
  getSoilDataService @1 (id :UInt64) -> (soilDataService :SoilDataService);
  getCoord @2 () -> (coord :Geo.GKCoord);
  getText @3 () -> (text :Text);

  #landkreisId @1 (gkCoord :GKCoord) :Int64;
}
