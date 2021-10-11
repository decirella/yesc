#!/usr/bin/env python3
"""
Create .protocol file for Presrevica ingest
"""

# -c use path to dir of files
#python3 xip_protocol.py -c ./sips/test_file/

__author__ = "David Cirella"
__version__ = "0.1.0"
__license__ = "MIT"

import os, os.path
import argparse
import hashlib
import uuid
import datetime
import xml.etree.ElementTree as et
from xml.dom import minidom


localAIPstr = ''
sips_out_path = './sips/'


def create_protocol(content_path):
    global localAIPstr
    file_count, data_size = data_stats(content_path)
    print(file_count)
    
    protocol_root = et.Element('protocol')
    protocol_root.attrib = {'xmlns':"http://www.tessella.com/xipcreateprotocol/v1"}
    
    date_create = et.Element('dateCreated')
    time_stamp = str(datetime.datetime.now().isoformat(timespec='microseconds'))
    date_create.text = time_stamp
    protocol_root.append(date_create)
    
    #size
    size =  et.Element('size')
    size.text = str(data_size)
    protocol_root.append(size)
    
    #files
    files =  et.Element('files')
    files.text = str(file_count)
    protocol_root.append(files)
    
    #submissionName
    submissionName =  et.Element('submissionName')
    submissionName.text = str(content_path.split('/')[-2])
    protocol_root.append(submissionName)
    
    #catalogueName
    catalogueName =  et.Element('catalogueName')
    catalogueName.text = str(content_path.split('/')[-2])
    protocol_root.append(catalogueName)
    
    
    #localAIP
    localAIP =  et.Element('localAIP')
    localAIPstr = str(uuid.uuid4())
    localAIP.text = localAIPstr
    protocol_root.append(localAIP)
    
    #globalAIP
    globalAIP =  et.Element('globalAIP')
    globalAIP.text = str(uuid.uuid4())
    protocol_root.append(globalAIP)
    
    #createdBy
    createdBy =  et.Element('createdBy')
    createdBy.text = 'user'
    protocol_root.append(createdBy)
    
    
    write_out(protocol_root, sips_out_path + localAIPstr + '.protocol') 
    
def create_xip(content_path):
    
    xip_root = et.Element('XIP')
    xip_root.attrib = {'xmlns':"http://preservica.com/XIP/v6.2"}
    
    # TODO create SO if need
    
    # TODO loop for all file in content_dir
    # for file, checksum, cp
    for file_to_pack in os.listdir(content_path): 
        if os.path.isfile(content_path + file_to_pack):
    
            # <InformationObject>
            iobj =  et.Element('InformationObject')
            xip_root.append(iobj)
            
            # ref
            iobj_ref =  et.Element('Ref')
            iobj_uuid = str(uuid.uuid4())
            iobj_ref.text = iobj_uuid
            iobj.append(iobj_ref)
            
            # title
            iobj_title =  et.Element('Title')
            iobj_title.text = str(file_to_pack)
            iobj.append(iobj_title)
            
            # security
            iobj_sec =  et.Element('SecurityTag')
            iobj_sec.text = 'open'
            iobj.append(iobj_sec)
            
            # Parent
            iobj_par =  et.Element('Parent')
            iobj_par.text = '8e7c8108-0cd7-4326-965a-db96a893fb12' #test_dest
            iobj.append(iobj_par)
            
            ##
            # Representation
            representation =  et.Element('Representation')
            xip_root.append(representation) 
            
            # io
            rep_iobj =  et.Element('InformationObject')
            rep_iobj.text = iobj_uuid
            representation.append(rep_iobj)
            
            #name
            rep_name =  et.Element('Name')
            rep_name.text = 'Preservation-1'
            representation.append(rep_name)
            
            #type
            rep_type =  et.Element('Type')
            rep_type.text = 'Preservation'
            representation.append(rep_type)
            
            
            #cos
            rep_cobjs =  et.Element('ContentObjects')
            representation.append(rep_cobjs)
            
            #co
            rep_cobj =  et.Element('ContentObject')
            cobj_uuid = str(uuid.uuid4())
            rep_cobj.text = cobj_uuid
            rep_cobjs.append(rep_cobj)
            
            ##
            # Content Object
            cobj =  et.Element('ContentObject')
            xip_root.append(cobj) 
            
            #ref
            cobj_ref = et.Element('Ref')
            cobj_ref.text = cobj_uuid
            cobj.append(cobj_ref)
            
            #title
            cobj_title = et.Element('Title')
            cobj_title.text = str(file_to_pack)
            cobj.append(cobj_title)
            
            #security
            cobj_sec = et.Element('SecurityTag')
            cobj_sec.text = 'open'
            cobj.append(cobj_sec)
            
            
            #parent
            cobj_par = et.Element('Parent')
            cobj_par.text = iobj_uuid
            cobj.append(cobj_par)
            
            
            ##
            # Generation
            gen =  et.Element('Generation')
            gen.attrib  = {'original' : "true", 'active' : "true"}
            xip_root.append(gen) 
            
            #co
            gen_cobj = et.Element('ContentObject')
            gen_cobj.text = cobj_uuid
            gen.append(gen_cobj)
            
            #effectivedate
            gen_effect_d = et.Element('EffectiveDate')
            gen_effect_d.text = str(datetime.datetime.now().isoformat(timespec='microseconds'))
            gen.append(gen_effect_d)
            
            # bitstreams
            gen_bss = et.Element('Bitstreams')
            gen.append(gen_bss)
            
            #bitstream
            gen_bs = et.Element('Bitstream')
            gen_bs.text = str(file_to_pack)
            gen_bss.append(gen_bs)

            ##
            # Bitstream
            bit_stream =  et.Element('Bitstream')
            xip_root.append(bit_stream)
            
            #filename
            bs_file = et.Element('Filename')
            bs_file.text = str(file_to_pack)
            bit_stream.append(bs_file)
                    
            #filesize
            bs_size = et.Element('FileSize')
            bs_size_get = str(os.path.getsize(content_path + file_to_pack))
            bs_size.text = bs_size_get
            bit_stream.append(bs_size)
            
            #physicallocation
            bs_pl =  et.Element('PhysicalLocation')
            bit_stream.append(bs_pl)
            
            #fixities
            bs_fixities =  et.Element('Fixities')
            bit_stream.append(bs_fixities)
            
            #fixity
            bs_fixity =  et.Element('Fixity')
            bs_fixities.append(bs_fixity)
            
            ##fixitiy ALgo
            bs_fixity_algo =  et.Element('FixityAlgorithmRef')
            bs_fixity_algo.text = 'SHA512'
            bs_fixity.append(bs_fixity_algo)
            
            ##fixixty val
            bs_fixity_val =  et.Element('FixityValue')
            bs_checksum = get_checksum(content_path + file_to_pack, 'SHA512')
            bs_fixity_val.text = bs_checksum
            bs_fixity.append(bs_fixity_val)
        
    
    os.mkdir(sips_out_path + localAIPstr)
    xip_out_path = sips_out_path + localAIPstr + '/metadata.xml'  
    write_out(xip_root, xip_out_path) 
    

def get_checksum(bs_file, algo):
    print(bs_file, algo)

    sha512_hash = hashlib.sha512()
    with open(bs_file,"rb") as f:
    # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            sha512_hash.update(byte_block)
        print(sha512_hash.hexdigest())
    return sha512_hash.hexdigest()

def write_out(xml_root, file_path):
  
    xml_out = minidom.parseString(et.tostring(xml_root, encoding='utf8', method='xml').decode('utf-8')).toprettyxml(indent="   ")
    print(xml_out)
    xml_file = open(file_path, "w")
    xml_file.write(xml_out)
    
    return 0
    
def data_stats(data_path):
    print(data_path)
    ### count of files
    #print(len(os.listdir(data_path)))
    
    file_list = [name for name in os.listdir(data_path) if os.path.isfile(data_path + name)]
    file_count = len(file_list)
    print(file_count)
    
    data_size = 0
    for f in file_list:
        data_size += os.path.getsize(data_path + f)
        
    
    
    
    return file_count, data_size
    

def main(args):
    """ Main entry point of the app """
    print(args.content_path)
    
   
    create_protocol(args.content_path)
    create_xip(args.content_path)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    parser = argparse.ArgumentParser()


    # Optional argument flag 
    parser.add_argument("-c", "--content", action="store", dest="content_path")

    args = parser.parse_args()
    main(args)
