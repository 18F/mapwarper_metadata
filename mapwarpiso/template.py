from jinja2 import Template
import json
from datetime import date
import codecs


#
# Load the jinja templating system, and initialize the templates directory
#
from jinja2 import Environment, PackageLoader
env = Environment(loader=PackageLoader('module', 'templates'))

#
# read in the scraped json records
#
json_data=open('data.json')
data = json.load(json_data)
json_data.close()



#
# loop through each entry in the scraped json file
#
for (i, record) in enumerate(data['items']):

   print i,record

   record['tags'] = record['cached_tag_list'].split(',')

   record['docid']='gov.doe.ncep:WARP'+str(i)
   record['doctitle']='WARP'+str(i)
   record['date']=date.today().isoformat()

   bbox = record['bbox'].split(',')

     
   record['minlon'] = bbox[0]
   record['minlat'] = bbox[1]
   record['maxlon'] = bbox[2]
   record['maxlat'] = bbox[3]

   record['wms_url']="http://warp.nepanode.anl.gov/maps/wms/"+str(record['id'])+"?request=GetCapabilities&amp;service=WMS&amp;version=1.1.1"
   record['kml_url']="http://warp.nepanode.anl.gov/maps"+str(record['id'])+".kml"
   # source URI
   record['mapwarper_url']="http://warp.nepanode.anl.gov/maps"
   #record['resolution'] = "maybe 1 degree"

   print record['date']
   print record 
   #
   # Load the isorecord.xml template from the templates directory
   #
   template = env.get_template('isorecord.xml')
   # render the template with record as the variables for the template
   output = template.render(**record)

   # write the output to a new ISO record in the waf directory
   outputfile = codecs.open('waf/'+record['doctitle']+'.xml',"w","UTF-8")
   outputfile.write(output)
   outputfile.close()



