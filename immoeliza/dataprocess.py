from scrapy.item import Item
from scrapy import Field
import json,re


mapping={
    "id" : {"PropertyId": lambda x :x},
    "type" : {"TypeOfProperty":lambda x : 1 if x=="house" else 2},
    "zip" : { "PostalCode": lambda x : int(str(x.strip().lower())) if str(x.strip().lower()).isdigit() else None},
    "subtype":{"SubtypeOfProperty":lambda x : x},
    "transactionType":{"TypeOfSale": lambda x: 1 if "sale" in x.strip().lower() else 2},
    "price":{"Price": lambda x : int(x) if str(x).isdigit() else None},
    "kitchen" : {"Kitchen": lambda x : x["type"].strip().lower() if len(x["type"].strip())>0 else None},
    "building" : {"StateOfBuilding": lambda x : x["condition"].strip().lower() if len(x["condition"].strip())>1 else None},
    "energy" : {"Heating": lambda x : x["heatingType"].strip().lower() if len(x["heatingType"].strip())>0 else None},
    "bedroom" : {"Bedrooms": lambda x : int(x["count"].strip()) if str(x["count"].strip()).isdigit() else None},
    "land": {"SurfaceOfGood": lambda x : float(x) if  str(x).replace(".","").isdigit() else None},
    "outdoor" : {"Terrace" : lambda x : "exists" in x["terrace"] and "true" in str(x["terrace"]["exists"].strip())},
    "wellnessEquipment": {"SwimmingPool": lambda x : ("true" in x["hasSwimmingPool"] or "yes" in x["hasSwimmingPool"])},
    "land" : {"SurfaceOfGood" : lambda x : float(x["surface"]) if  str(x["surface"]).replace(".","").isdigit() else None }
}


class ImmoItem(Item):
    js=Field()
    html_elems=Field()
    Url=Field()
    PostalCode=Field()
    PropertyId  = Field()
    TypeOfProperty=Field()
    SubtypeOfProperty=Field()
    TypeOfSale=Field()
    Bedrooms=Field()
    LivingArea=Field()
    SurfaceOfGood=Field()
    Terrace=Field()
    Garden=Field()
    GardenArea=Field()
    Price=Field()
    Kitchen=Field()
    Furnished=Field()
    Openfire=Field()
    NumberOfFacades=Field()
    SwimmingPool=Field()
    StateOfBuilding=Field()
    Heating=Field()
    ConstructionYear=Field()
    
    
    def transform(self):
        self["Openfire"]=False
        self["Furnished"]=False
        self["Terrace"]=False
        self["Garden"]=False
        for k,v in mapping.items():
            if k in self["js"]:
                key,func=list(v.items())[0] 
                self[key]=func(self["js"][k])
        for k,v in self["html_elems"].items():
            v=v.strip().lower()
            k=k.strip().lower()
            if "bedroom" in k and ("Bedrooms" not in self.keys() or self["Bedrooms"] is None):
                self["Bedrooms"]=int(v) if str(v).isdigit() else None
            elif re.search("(living.*area|livable.*space)",k) is not None and ("LivingArea" not in self.keys() or self["LivingArea"] is None):
                v=re.sub("m[²2]","",v)
                self["LivingArea"]=float(v) if str(v.replace(".","").replace(",","")).isdigit() else None
            elif re.search("(surface.*plot|of land)",k) is not None and ("SurfaceOfGod" not in self.keys() or self["SurfaceOfGood"] is  None):
                v=re.sub("m[²2]","",v)
                self["SurfaceOfGood"]=float(v) if str(v.replace(".","").replace(",","")).isdigit() else None
            elif re.search("number.*(frontage|facade)",k) is not None and ("NumberOfFacades" not in self.keys() or self["NumberOfFacades"] is None):
                self["NumberOfFacades"]=int(v) if str(v).isdigit() else None
            elif re.search("kitchen.*type",k ) is not None and ("Kitchen" not in self.keys() or self["Kitchen"] is None):
                self["Kitchen"]=v
            elif re.match("garden",k) is not None and ("Garden" not in self.keys() or self["Garden"] is None) :
                self["Garden"]=re.search("(true|yes)",v) is not None
            elif re.search("garden.*(area|surface)",k) is not None and ("GardenArea" not in self.keys() or self["GardenArea"] is None):
                v=re.sub("m[²2]","",v)
                self["Garden"]=True
                self["GardenArea"]=float(v) if str(v.replace(".","").replace(",","")).isdigit() else None
            elif re.match("terrace",k) is not None and ("Terrace" not in self.keys() or (self["Terrace"] is None or self["Terrace"] is False)):
                self["Terrace"]=re.search("(true|yes)",v) is not None
            elif re.search("terrace",k) is not None and ("Terrace" not in self.keys() or (self["Terrace"] is None or self["Terrace"] is False)):
                self["Terrace"]=re.search("(no|false)",v) is not None
            elif re.search("construction.*year",k) is not None and "ConstructionYear" not in self.keys():
                self["ConstructionYear"]=int(v) if v.isdigit() else None 
            elif re.search("(openfire|fireplace)",k) is not None and ("Openfire" not in self.keys() or self["Openfire"] is not None):
                self["Openfire"]=re.search("(yes|true)",v) is not None   
            elif re.search("furnished",k) is not None and ("Furnished" not in self.keys() or (self["Furnished"] is None or self["Furnished"] is False)):
                self["Furnished"]=re.search("(yes|true|[0-9]+)",v) is not None 
                
                    