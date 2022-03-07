#!/usr/bin/env python3
"""
Create .protocol file for Presrevica ingest
"""


# python3 xip_protocol.py -input ./sips/test_file/ -o ./sips/ 

__author__ = "David Cirella"
__version__ = "0.1.3"
__license__ = "MIT"

import os
import sys
import shutil
import argparse
import hashlib
import uuid
import datetime
import xml.etree.ElementTree as et
from xml.dom import minidom
from lxml import etree
from pathlib import Path


localAIPstr = ''
sips_out_path = ''


## user set defaults
default_security_tag = 'open'



def create_protocol(content_path):
    global localAIPstr
    file_count, data_size = data_stats(content_path)

    
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
    submissionName.text = str(Path(content_path).parts[-1])
    protocol_root.append(submissionName)
    
    #catalogueName
    catalogueName =  et.Element('catalogueName')
    catalogueName.text = str(Path(content_path).parts[-1])
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
    reporting_std_out(localAIPstr, file_count, data_size)
    
def create_xip(args):
    ###    
    def create_xip_recurse(content_path, parent_set):
        sobj =  et.Element('StructuralObject')
        xip_root.append(sobj)
        
        # ref
        sobj_ref =  et.Element('Ref')
        sobj_uuid = str(uuid.uuid4())
        sobj_ref.text = sobj_uuid
        sobj.append(sobj_ref)
        
        # title
        sobj_title =  et.Element('Title')
        sobj_title.text = args.sotitle or str(Path(content_path).parts[-1])
        sobj.append(sobj_title)
            
    
        # description
        sobj_desc =  et.Element('Description')
        sobj_desc.text = args.sodescription
        sobj.append(sobj_desc)
        
        # security
        sobj_sec =  et.Element('SecurityTag')
        sobj_sec.text = args.securitytag
        sobj.append(sobj_sec)
    

        # Parent
        sobj_par =  et.Element('Parent')
        sobj_par.text = parent_set
        sobj.append(sobj_par)
        print(sobj_par.text, ' sobj_par.text')
    

        iobj_parent_set = sobj_uuid
        
        
        for file_to_pack in Path(content_path).iterdir():
            if Path(file_to_pack).is_file():
        
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
                iobj_title.text = Path(file_to_pack).name
                iobj.append(iobj_title)
                
                 # description
                iobj_desc =  et.Element('Description')
                iobj_desc.text = args.iodescription
                iobj.append(iobj_desc)
                
                # security
                iobj_sec =  et.Element('SecurityTag')
                iobj_sec.text = args.securitytag
                iobj.append(iobj_sec)
                
                # Parent
                iobj_par =  et.Element('Parent')
                iobj_par.text = iobj_parent_set
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
                cobj_title.text = Path(file_to_pack).name
                cobj.append(cobj_title)
                
                #security
                cobj_sec = et.Element('SecurityTag')
                cobj_sec.text = args.securitytag
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
                gen_bs.text = Path(file_to_pack).name
                gen_bss.append(gen_bs)
        
                ##
                # Bitstream
                bit_stream =  et.Element('Bitstream')
                xip_root.append(bit_stream)
                
                #filename
                bs_file = et.Element('Filename')
                bs_file.text = Path(file_to_pack).name
                bit_stream.append(bs_file)
                        
                #filesize
                bs_size = et.Element('FileSize')
                bs_size_get = str(Path(file_to_pack).stat().st_size)
                bs_size.text = bs_size_get
                bit_stream.append(bs_size)
                
                #physicallocation
                bs_pl =  et.Element('PhysicalLocation')
                #bs_pl.text = Path(file_to_pack).name
                bit_stream.append(bs_pl)
                
                #fixities
                bs_fixities =  et.Element('Fixities')
                bit_stream.append(bs_fixities)
                
                #fixity
                bs_fixity =  et.Element('Fixity')
                bs_fixities.append(bs_fixity)
                
                # fixity
                hash_out, hash_algo = get_checksum(file_to_pack, args)
                
                ##fixitiy ALgo
                bs_fixity_algo =  et.Element('FixityAlgorithmRef')
                bs_fixity_algo.text = hash_algo
                bs_fixity.append(bs_fixity_algo)
                
                ##fixixty val
                bs_fixity_val =  et.Element('FixityValue')
                bs_checksum = hash_out
                bs_fixity_val.text = bs_checksum
                bs_fixity.append(bs_fixity_val)
                
                
                ## check for embedding metadata at IO level
                if args.iometadata:
                    meta_entity = iobj_uuid
                    md_embed_iobj = embed_metadata(args.iometadata, meta_entity)
                    xip_root.append(md_embed_iobj)
                    
                       # check of creting identifier at so level
                if args.ioidtype:
                    id_entity = iobj_uuid
                    id_iobj = gen_id(args, id_entity, 'io')
                    xip_root.append(id_iobj)
            elif Path(file_to_pack).is_dir():
                create_xip_recurse(file_to_pack, iobj_parent_set)
        ###







    content_path = args.input
    xip_root = et.Element('XIP')
    #et.register_namespace('XIP','http://preservica.com/XIP/v6.2')
    xip_root.attrib = {'xmlns':"http://preservica.com/XIP/v6.2"}
          
    
    if args.assetonly:
        sobj_uuid = None
        
        if args.parent == None:
            print('ERROR : Parent must be provided for assest only ingests')   
            exit()
        iobj_parent_set = args.parent
      
    else:
        
        # <StructuralObject>
        # move to outside of recursive funct
        sobj =  et.Element('StructuralObject')
        xip_root.append(sobj)
            
        # ref
        sobj_ref =  et.Element('Ref')
        sobj_uuid = str(uuid.uuid4())
        sobj_ref.text = sobj_uuid
        sobj.append(sobj_ref)
            
        # title
        sobj_title =  et.Element('Title')
        sobj_title.text = args.sotitle or str(Path(content_path).parts[-1])
        sobj.append(sobj_title)
        
        
        # description
        sobj_desc =  et.Element('Description')
        sobj_desc.text = args.sodescription
        sobj.append(sobj_desc)
            
        # security
        sobj_sec =  et.Element('SecurityTag')
        sobj_sec.text = args.securitytag
        sobj.append(sobj_sec)
        
        if args.parent != None:    
            # Parent
            sobj_par =  et.Element('Parent')
            sobj_par.text = args.parent
            sobj.append(sobj_par)
        
        

        iobj_parent_set = sobj_uuid

    for file_to_pack in Path(content_path).iterdir(): 
        if Path(file_to_pack).is_file():
            # call function for IO packing
            # elif dir call SO func and then IO func
            
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
            iobj_title.text = Path(file_to_pack).name
            iobj.append(iobj_title)
            
             # description
            iobj_desc =  et.Element('Description')
            iobj_desc.text = args.iodescription
            iobj.append(iobj_desc)
            
            # security
            iobj_sec =  et.Element('SecurityTag')
            iobj_sec.text = args.securitytag
            iobj.append(iobj_sec)
            
            # Parent
            iobj_par =  et.Element('Parent')
            iobj_par.text = iobj_parent_set
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
            cobj_title.text = Path(file_to_pack).name
            cobj.append(cobj_title)
            
            #security
            cobj_sec = et.Element('SecurityTag')
            cobj_sec.text = args.securitytag
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
            gen_bs.text = Path(file_to_pack).name
            gen_bss.append(gen_bs)

            ##
            # Bitstream
            bit_stream =  et.Element('Bitstream')
            xip_root.append(bit_stream)
            
            #filename
            bs_file = et.Element('Filename')
            bs_file.text = Path(file_to_pack).name
            bit_stream.append(bs_file)
                    
            #filesize
            bs_size = et.Element('FileSize')
            bs_size_get = str(Path(file_to_pack).stat().st_size)
            bs_size.text = bs_size_get
            bit_stream.append(bs_size)
            
            #physicallocation
            bs_pl =  et.Element('PhysicalLocation')
            #bs_pl.text = Path(file_to_pack).name
            bit_stream.append(bs_pl)
            
            #fixities
            bs_fixities =  et.Element('Fixities')
            bit_stream.append(bs_fixities)
            
            #fixity
            bs_fixity =  et.Element('Fixity')
            bs_fixities.append(bs_fixity)
            
            # fixity
            hash_out, hash_algo = get_checksum(file_to_pack, args)
            
            ##fixitiy ALgo
            bs_fixity_algo =  et.Element('FixityAlgorithmRef')
            bs_fixity_algo.text = hash_algo
            bs_fixity.append(bs_fixity_algo)
            
            ##fixixty val
            bs_fixity_val =  et.Element('FixityValue')
            bs_checksum = hash_out
            bs_fixity_val.text = bs_checksum
            bs_fixity.append(bs_fixity_val)
            
            '''
             ## IO handle parentless
            if iobj_parent_set == None:
                print('parentless')
                md_virt = parentless(iobj_uuid)
                xip_root.append(md_virt)
            '''
            ## check for embedding metadata at IO level
            if args.iometadata:
                meta_entity = iobj_uuid
                md_embed_iobj = embed_metadata(args.iometadata, meta_entity)
                xip_root.append(md_embed_iobj)
                
                   # check of creting identifier at so level
            if args.ioidtype:
                id_entity = iobj_uuid
                id_iobj = gen_id(args, id_entity, 'io')
                xip_root.append(id_iobj)
                
        elif Path(file_to_pack).is_dir():
            create_xip_recurse(file_to_pack, iobj_parent_set)
        
    
    ## SO handle parentless
    if sobj_uuid != None and args.parent == None:
        md_virt = parentless(sobj_uuid)
        xip_root.append(md_virt)
    
    ## check for embedding metadata at SO level
    if args.sometadata:
        meta_entity = sobj_uuid
        md_embed_sobj = embed_metadata(args.sometadata, meta_entity)
        xip_root.append(md_embed_sobj)
        
    # check of creting identifier at so level
    if args.soidtype:
        id_entity = sobj_uuid
        id_sobj = gen_id(args, id_entity, 'so')
        xip_root.append(id_sobj)
   
        
        
    if args.aspace:
        print('aspace AO ref: ', args.aspace)
        # TODO test with asset only

        # create ASpace metadata elements
        # ASPACE <StructuralObject>
        as_sobj =  et.Element('StructuralObject')
        xip_root.insert(0, as_sobj)
            
        # ref
        as_sobj_ref =  et.Element('Ref')
        as_sobj_uuid = str(uuid.uuid4())
        as_sobj_ref.text = as_sobj_uuid
        as_sobj.append(as_sobj_ref)
            
        # title
        as_sobj_title =  et.Element('Title')
        as_sobj_title.text = args.aspace
        as_sobj.append(as_sobj_title)
        
        # description
        as_sobj_desc =  et.Element('Description')
        # sobj_desc.text = args.
        as_sobj.append(as_sobj_desc)
            
        # security
        as_sobj_sec =  et.Element('SecurityTag')
        as_sobj_sec.text = args.securitytag
        as_sobj.append(as_sobj_sec)
        
        # change out SO parent ref
        sobj_par.text = as_sobj_uuid
        
        
        # identifier gp as_sobj
        id_as_gp_sobj =  et.Element('Identifier')
        xip_root.append(id_as_gp_sobj)
        
        # type
        id_as_gp_sobj_type =  et.Element('Type')
        id_as_gp_sobj_type.text = 'code'
        id_as_gp_sobj.append(id_as_gp_sobj_type)
        
        # value
        id_as_gp_sobj_val =  et.Element('Value')
        id_as_gp_sobj_val.text = args.aspace
        id_as_gp_sobj.append(id_as_gp_sobj_val)  
        
        # entity
        id_as_gp_sobj_ent =  et.Element('Entity')
        id_as_gp_sobj_ent.text = as_sobj_uuid
        id_as_gp_sobj.append(id_as_gp_sobj_ent)       
            

        ## refactor
        # aspace so grandparent ASpace sync, linked to empty parent SO 
        md_as_gp_sobj =  et.Element('Metadata')
        md_as_gp_sobj.attrib  = {'schemaUri' : "http://preservica.com/LegacyXIP"}
        xip_root.append(md_as_gp_sobj)
        
        # ref
        md_as_gp_sobj_ref =  et.Element('Ref')
        md_as_gp_sobj_uuid = str(uuid.uuid4())
        md_as_gp_sobj_ref.text = md_as_gp_sobj_uuid
        md_as_gp_sobj.append(md_as_gp_sobj_ref)
        
        # entity
        md_as_gp_sobj_ent =  et.Element('Entity')
        md_as_gp_sobj_ent.text = as_sobj_uuid
        md_as_gp_sobj.append(md_as_gp_sobj_ent)
        
        # content
        md_as_gp_sobj_ct =  et.Element('Content')
        md_as_gp_sobj.append(md_as_gp_sobj_ct)
            
            #legacy XIP
        md_as_gp_sobj_lx =  et.Element('LegacyXIP')
        md_as_gp_sobj_lx.attrib  = {'xmlns' : "http://preservica.com/LegacyXIP"}
        md_as_gp_sobj_ct.append(md_as_gp_sobj_lx)
            #virtual
        md_as_gp_sobj_v =  et.Element('Virtual')
        md_as_gp_sobj_v.text  = 'false'
        md_as_gp_sobj_lx.append(md_as_gp_sobj_v)
        
        
        # aspace so parent ASpace sync, linked parent SO 
        md_as_sobj =  et.Element('Metadata')
        md_as_sobj.attrib  = {'schemaUri' : "http://preservica.com/LegacyXIP"}
        xip_root.append(md_as_sobj)
        
        # ref
        md_as_sobj_ref =  et.Element('Ref')
        md_as_sobj_uuid = str(uuid.uuid4())
        md_as_sobj_ref.text = md_as_sobj_uuid
        md_as_sobj.append(md_as_sobj_ref)
        
        # entity
        md_as_sobj_ent =  et.Element('Entity')
        md_as_sobj_ent.text = sobj_uuid
        md_as_sobj.append(md_as_sobj_ent)
        
        # content
        md_as_sobj_ct =  et.Element('Content')
        md_as_sobj.append(md_as_sobj_ct)
            
            #legacy XIP
        md_as_sobj_lx =  et.Element('LegacyXIP')
        md_as_sobj_lx.attrib  = {'xmlns' : "http://preservica.com/LegacyXIP"}
        md_as_sobj_ct.append(md_as_sobj_lx)
            #AccessionRef
        md_as_sobj_aref =  et.Element('AccessionRef')
        md_as_sobj_aref.text  = 'catalogue'
        md_as_sobj_lx.append(md_as_sobj_aref)
        
        # identifier as_sobj
        id_as_sobj =  et.Element('Identifier')
        xip_root.append(id_as_sobj)
        
        # type
        id_as_sobj_type =  et.Element('Type')
        id_as_sobj_type.text = 'code'
        id_as_sobj.append(id_as_sobj_type)
        
        # value
        id_as_sobj_val =  et.Element('Value')
        id_as_sobj_val.text = args.aspace
        id_as_sobj.append(id_as_sobj_val)  
        
        # entity
        id_as_sobj_ent =  et.Element('Entity')
        id_as_sobj_ent.text = sobj_uuid
        id_as_sobj.append(id_as_sobj_ent)           

    
    
    Path(sips_out_path + localAIPstr).mkdir()
    xip_out_path = sips_out_path + localAIPstr + '/metadata.xml'  
    write_out(xip_root, xip_out_path)
    
    # create content folder, copy files
    if args.export:
        sip_content = sips_out_path + localAIPstr + '/content'
        Path(sip_content).mkdir()
        for file_to_pack in Path(content_path).rglob("*"): 
            if Path(file_to_pack).is_file():
                shutil.copy2(file_to_pack, sip_content)
                
        
          
    
    #print(validate_xml(xip_out_path, './XIP-V6.xsd')) 


def get_checksum(bs_file, args):
    if args.md5:
        #
        algo = 'MD5'
        bs_hash = hashlib.md5()
    elif args.sha1:
        #
        algo = 'SHA1'
        bs_hash = hashlib.sha1()
    elif args.sha256:
        #
        algo = 'SHA256'
        bs_hash = hashlib.sha256()
    elif args.sha512:
        #
        algo = 'SHA512'
        bs_hash = hashlib.sha512()
    else:
        algo = 'SHA512'
        bs_hash = hashlib.sha512()
        
    
    with open(bs_file,"rb") as f:
    # Read and update hash string value in blocks of 4K
        for byte_block in iter(lambda: f.read(4096),b""):
            bs_hash.update(byte_block)
        hash_out = bs_hash.hexdigest()
    return hash_out, algo

def gen_id(args, id_entity, obj_type):
    if 'so' in obj_type:
        id_type = args.soidtype
        id_value = args.soidvalue
    elif 'io' in obj_type:
        id_type = args.ioidtype
        id_value = args.ioidvalue
        
    # identifier sobj
    id_obj =  et.Element('Identifier')
  
        
    # type
    id_obj_type =  et.Element('Type')
    id_obj_type.text = id_type
    id_obj.append(id_obj_type)
       
    # value
    id_obj_val =  et.Element('Value')
    id_obj_val.text = id_value
    id_obj.append(id_obj_val)  
        
    # entity
    id_obj_ent =  et.Element('Entity')
    id_obj_ent.text = id_entity
    id_obj.append(id_obj_ent)        
       
    return id_obj

def embed_metadata(meta_file_embed, meta_entity):
    # read in xml
    doc_in_tree = et.parse(meta_file_embed)
    doc_in_root = doc_in_tree.getroot()
    
    #get namespace and parse for uri
    doc_in_ns = doc_in_tree.getroot().tag
    
    def xmlns_normalize(name):
        if name[0] == "{":
            uri, tag = name[1:].split("}")
            return uri, tag
        else:
            return name
    
    doc_ns_uri, doc_ns_name = xmlns_normalize(doc_in_ns)
    
    #print(doc_ns_uri)
    et.register_namespace(doc_ns_name , doc_ns_uri)
    # create elements
    md_embed_sobj =  et.Element('Metadata')   
    md_embed_sobj.attrib  = {'schemaUri' : doc_ns_uri}
    
    # ref
    md_embed_sobj_ref =  et.Element('Ref')
    md_embed_sobj_uuid = str(uuid.uuid4())
    md_embed_sobj_ref.text = md_embed_sobj_uuid
    md_embed_sobj.append(md_embed_sobj_ref)
    
    # entity
    md_embed_sobj_ent =  et.Element('Entity')
    md_embed_sobj_ent.text = meta_entity
    md_embed_sobj.append(md_embed_sobj_ent)
       
    # content
    md_embed_sobj_ct =  et.Element('Content')
    md_embed_sobj.append(md_embed_sobj_ct)
    
    #print(et.tostring(doc_in_root)) 
    # embed read in file
    md_embed_sobj_ct.append(doc_in_root)
    
    #print(meta_file_embed)
    
    return md_embed_sobj

## refactor
def parentless(entity_from):
    md_virt =  et.Element('Metadata')
    md_virt.attrib  = {'schemaUri' : "http://preservica.com/LegacyXIP"}
            
    # ref
    md_virt_ref =  et.Element('Ref')
    md_virt_uuid = str(uuid.uuid4())
    md_virt_ref.text = md_virt_uuid
    md_virt.append(md_virt_ref)
            
    # entity
    md_virt_ent =  et.Element('Entity')
    md_virt_ent.text = entity_from
    md_virt.append(md_virt_ent)

    # content
    md_virt_ct =  et.Element('Content')
    md_virt.append(md_virt_ct)
                
    #legacy XIP
    md_virt_lx =  et.Element('LegacyXIP')
    md_virt_lx.attrib  = {'xmlns' : "http://preservica.com/LegacyXIP"}
    md_virt_ct.append(md_virt_lx)

    #virtual
    md_virt_v =  et.Element('Virtual')
    md_virt_v.text  = 'false'
    md_virt_lx.append(md_virt_v)

    return md_virt

def write_out(xml_root, file_path):
    et.ElementTree(xml_root).write(file_path, encoding="utf-8", xml_declaration=True)

    return 0
    
def validate_xml(xml_path: str, xsd_path: str) -> bool:

    xmlschema_doc = etree.parse(xsd_path)
    xmlschema = etree.XMLSchema(xmlschema_doc)

    xml_doc = etree.parse(xml_path)

    xml_status = xmlschema.validate(xml_doc)
    return xml_status

    
def data_stats(data_path):
    
    file_list = [name for name in Path(data_path).rglob("*") if Path(name).is_file()]
    file_count = len(file_list)
    
    data_size = 0
    for f in file_list:
        data_size += Path(f).stat().st_size
    
    
    
    return file_count, data_size
    

def reporting_std_out(localAIPstr, file_count, data_size):
    
    print('uuid', localAIPstr)
    print('Files to be packaged: ', file_count)    
    print('Total size: ', data_size, 'bytes')


def main(args):
    global sips_out_path 
    """ Main entry point of the app """
    sips_out_path = os.path.join(args.output, '')
    
    data_in_path = os.path.join(args.input, '')
    
    create_protocol(data_in_path)
    create_xip(args)

if __name__ == "__main__":
    """ This is executed when run from the command line """
    
    parser = argparse.ArgumentParser()


    # Optional argument flag 
    parser.add_argument("-input", "-i", "--input", help='Directory containing content files')
    parser.add_argument("-output", "-o", "--output", help='Directory to export the SIP to')
    parser.add_argument("-sotitle", "-sot", "--sotitle", default=0, help='Title for structural object')
    parser.add_argument("-parent", "-p", "--parent", default=None, help='Parent or destination reference')
    parser.add_argument("-securitytag", "-s", "--securitytag", default=default_security_tag, help='Security tag for objects in sip')
    parser.add_argument("-assetonly", "-a", "--assetonly", action='store_true', help='Ingest files as assets (no folder)')
    parser.add_argument("-export", "-e", "--export", action='store_true', help='Export files to content subdirectory of sip')
    parser.add_argument("-aspace", "-ao", "--aspace", help='ArchivesSpace archival object reference: archival_object_5555555')
    parser.add_argument("-sodescription", "-sod", "--sodescription", help='Description field for Structural Objects')
    parser.add_argument("-iodescription", "-iod", "--iodescription", help='Description field for all Information Objects')
    
    parser.add_argument("-sometadata", "-som", "--sometadata", help='Embed content of XML file as metadata linked to SO')
    parser.add_argument("-iometadata", "-iom", "--iometadata", help='Embed content of XML file as metadata linked to IO')

    parser.add_argument("-ioidtype", "-ioidt", "--ioidtype", help='Identifier type for all IOs')
    parser.add_argument("-ioidvalue", "-ioidv", "--ioidvalue", help='Identifier value for all IOs')
    
    parser.add_argument("-soidtype", "-soidt", "--soidtype", help='Identifier type for all SO')
    parser.add_argument("-soidvalue", "-soidv", "--soidvalue", help='Identifier value for all SO')


    parser.add_argument("-md5", "--md5", action='store_true', help='fixity values will  be generated using the MD5 algorithm')
    parser.add_argument("-sha1", "--sha1", action='store_true', help='fixity values will be generated using the SHA1 algorithm')
    parser.add_argument("-sha256", "--sha256", action='store_true', help='fixity values will be generated using the SHA256 algorithm')
    parser.add_argument("-sha512", "--sha512", action='store_true', help='fixity values will be generated using the SHA512 algorithm')
    
    
    # TODO
        # CO - embed metadata xml file as metadata element

'''
    try:
        args = parser.parse_args()
        main(args)
    except:
        ## message for run with no args
        parser.print_help()
        sys.exit(0)
'''

# debug
args = parser.parse_args()
main(args)

