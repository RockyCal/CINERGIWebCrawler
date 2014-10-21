__author__ = 'Raquel'


def find_term_links(string):
    ret_url = []

    # Domains
    for each in string:
        if "Agriculture" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/agr2.jpg, ")
        if "Atmosphere" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/atmos.jpg, ")
        if "Biodiversity" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/biod.jpg, ")
        if "Biology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/bio.jpg, ")
        if "Cadastral" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/cadas.jpg, ")
        if "Chemistry" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/chem.jpg, ")
        if "Climatology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/clima.jpg, ")
        if "Coastal Science" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/coastal.jpg, ")
        if "Data Systems" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/datasys.jpg, ")
        if "Earth Science" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/earths.jpg, ")
        if "Ecology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/eco.jpg, ")
        if "Environmental Science" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/environ.jpg, ")
        if "Estuarine Science" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/estua.jpg, ")
        if "Extreme Events" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/extremeevents.jpg, ")
        if "Forestry" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/forestry.jpg, ")
        if "Geochemistry" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geochem.jpg, ")
        if "Geochronology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geochron.jpg, ")
        if "Geodesy" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geodesy.jpg, ")
        if "Geography" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geograph.jpg, ")
        if "Geology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geology.jpg, ")
        if "Geophysics" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/geophys.jpg, ")
        if "GIS" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/gis.jpg, ")
        if "Glaciology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/glacia.jpg, ")
        if "Human Dimensions" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/humandim.jpg, ")
        if "Hydrobiology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/hydrobio.jpg, ")
        if "Hydrology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/hydrology.jpg, ")
        if "Infrastructure" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/infra.jpg, ")
        if "LIDAR" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/lidar.jpg, ")
        if "Limnology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/limno.jpg, ")
        if "Maps/Imaging" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/maps.jpg, ")
        if "Marine Biology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/marinebio.jpg, ")
        if "Marine Geology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/marinegeo.jpg, ")
        if "Meteorology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/meteor.jpg, ")
        if "Mineralogy" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/minera.jpg, ")
        if "Mining" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/mining.jpg, ")
        if "Oceanography" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/oceano.jpg, ")
        if "Paleobiology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/paleobio.jpg, ")
        if "Paleontology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/paleo.jpg, ")
        if "Petrology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/petro.jpg, ")
        if "Planetary Science" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/planetary.jpg, ")
        if "Plate Tectonics" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/platetect.jpg, ")
        if "Polar/Ice Satellite" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/polar.jpg, ")
        if "Sedimentology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/sediment.jpg, ")
        if "Seismology" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/seism.jpg, ")
        if "Soil" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/soil.jpg, ")
        if "Spatial" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/spatial.jpg, ")
        if "Taxonomy" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/taxon.jpg, ")
        if "Topography" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/topog.jpg, ")

        # Resource Types
        if "Activity" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/activity.jpg, ")
        if "Consensus effort" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/conseffort.jpg, ")
        if "Data service" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/dataservice.jpg, ")
        if "Catalog" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/catalog.jpg, ")
        if "Community" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/community.jpg, ")
        if "Web application" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/webapp.jpg, ")
        if "Organizational portal" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/orgport.jpg, ")
        if "Specification" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/specific.jpg, ")
        if "Image collection" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/imagecollect.jpg, ")
        if "Web page" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/webpage.jpg, ")
        if "Interchange format" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/interformat.jpg, ")
        if "Vocabulary" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/vocab.jpg, ")
        if "Service" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/service.jpg, ")
        if "Digital repository" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/digitalrepo.jpg, ")
        if "Functional specification" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/functspec.jpg, ")
        if "Software" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/software.jpg, ")
        if "Forum" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/forum.jpg, ")
        if "Organization" in string:
            ret_url.append("http://cinergiterms.weebly.com/uploads/7/5/1/1/7511984/organization.jpg, ")

    return ret_url
