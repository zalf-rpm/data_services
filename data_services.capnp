
struct ADate {
  # A standard Gregorian calendar date.

  year @0 :Int16;
  # The year. Must include the century.
  # Negative value indicates BC.

  month @1 :UInt8;   # Month number, 1-12.
  day @2 :UInt8;     # Day number, 1-31.
}

struct GKCoord {
  meridianNo @0 :UInt8;
  r @1 :Int64; # right value
  h @2 :Int64; # height value
}

struct SoilDataServiceInfo {
  id @0 :UInt64;
  name @1 :Text;
  description @2 :Text;
  service @3 :SoilDataService;
}

interface SoilDataService {
  
  getSoilIdAt @0 (gkCoord :GKCoord) :Int64;
}

interface DataServices {
  # the bootstrap interface to the different data services

  getAvailableSoilDataServices @0 () :List(SoilDataServiceInfo);
  getSoilDataService @1 (id :UInt64) :SoilDataService;
  
  #landkreisId @1 (gkCoord :GKCoord) :Int64;
}
