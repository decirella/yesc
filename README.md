# yesc
## Yale Easy Sip Creator

`yesc.py` provides a command line interface for create `XIP` version 6 SIPs for ingest to Preservica.

## Releases
### Commandline interface
- [Windows binary](https://github.com/decirella/yesc/releases/tag/0.1-alpha)

### Desktop GUI
- [Source](https://github.com/decirella/yes_creator)
- [Windows binary](https://github.com/decirella/yes_creator/releases/tag/0.1-alpha)


```
$ python3 yesc.py -h
usage: yesc.py [-h] [-input INPUT] [-output OUTPUT] [-sotitle SOTITLE]
               [-parent PARENT] [-securitytag SECURITYTAG] [-assetonly]
               [-singleasset] [-iotitle IOTITLE] [-export] [-aspace ASPACE]
               [-sodescription SODESCRIPTION] [-iodescription IODESCRIPTION]
               [-sometadata SOMETADATA] [-iometadata IOMETADATA]
               [-ioidtype IOIDTYPE] [-ioidvalue IOIDVALUE]
               [-soidtype SOIDTYPE] [-soidvalue SOIDVALUE] [-representations]
               [-sipconfig SIPCONFIG] [-storage STORAGE]
               [-storageconfig STORAGECONFIG] [-md5] [-sha1] [-sha256]
               [-sha512] [-excludedFileNames EXCLUDEDFILENAMES]
               [-prefix PREFIX]

options:
  -h, --help            show this help message and exit
  -input INPUT, -i INPUT, --input INPUT
                        Directory containing content files
  -output OUTPUT, -o OUTPUT, --output OUTPUT
                        Directory to export the SIP to
  -sotitle SOTITLE, -sot SOTITLE, --sotitle SOTITLE
                        Title for structural object
  -parent PARENT, -p PARENT, --parent PARENT
                        Parent or destination reference
  -securitytag SECURITYTAG, -s SECURITYTAG, --securitytag SECURITYTAG
                        Security tag for objects in sip
  -assetonly, -a, --assetonly
                        Ingest files as assets (no folder) each file will be
                        an asset, -parent uuid required
  -singleasset, -sa, --singleasset
                        Ingest multiple files as single asset, -IO title
                        required, -parent uuid required
  -iotitle IOTITLE, -iot IOTITLE, --iotitle IOTITLE
                        Title for IO, Applies in asset only mode
  -export, -e, --export
                        Export files to content subdirectory of sip
  -aspace ASPACE, -ao ASPACE, --aspace ASPACE
                        ArchivesSpace archival object reference:
                        archival_object_5555555
  -sodescription SODESCRIPTION, -sod SODESCRIPTION, --sodescription SODESCRIPTION
                        Description field for Structural Objects
  -iodescription IODESCRIPTION, -iod IODESCRIPTION, --iodescription IODESCRIPTION
                        Description field for all Information Objects, Applies
                        in asset only mode
  -sometadata SOMETADATA, -som SOMETADATA, --sometadata SOMETADATA
                        Embed content of XML file as metadata linked to SO
  -iometadata IOMETADATA, -iom IOMETADATA, --iometadata IOMETADATA
                        Embed content of XML file as metadata linked to IO
  -ioidtype IOIDTYPE, -ioidt IOIDTYPE, --ioidtype IOIDTYPE
                        Identifier type for all IOs
  -ioidvalue IOIDVALUE, -ioidv IOIDVALUE, --ioidvalue IOIDVALUE
                        Identifier value for all IOs
  -soidtype SOIDTYPE, -soidt SOIDTYPE, --soidtype SOIDTYPE
                        Identifier type for all SO
  -soidvalue SOIDVALUE, -soidv SOIDVALUE, --soidvalue SOIDVALUE
                        Identifier value for all SO
  -representations, -manifestations, -r, --representations
                        Structure should follow the multiple manifestation
                        package definition with manifestation folders of the
                        form *preservica_(presentation| preservation, use with
                        -iot options to set IO title
  -sipconfig SIPCONFIG, -sc SIPCONFIG, --sipconfig SIPCONFIG
                        Location of sip config, use with -r representations
                        option
  -storage STORAGE, -sk STORAGE, --storage STORAGE
                        path to storage keyword doc
  -storageconfig STORAGECONFIG, -skc STORAGECONFIG, --storageconfig STORAGECONFIG
                        Location of storage config
  -md5, --md5           fixity values will be generated using the MD5
                        algorithm
  -sha1, --sha1         fixity values will be generated using the SHA1
                        algorithm
  -sha256, --sha256     fixity values will be generated using the SHA256
                        algorithm
  -sha512, --sha512     fixity values will be generated using the SHA512
                        algorithm
  -excludedFileNames EXCLUDEDFILENAMES, -ef EXCLUDEDFILENAMES, --excludedFileNames EXCLUDEDFILENAMES
                        Comma separated list of file names to exclude during
                        SIP creation
  -prefix PREFIX, -pf PREFIX, --prefix PREFIX
                        String to prefix SO title with



```





## Use

### Python use

### Windows Binary
Dowload from release page  
Run from `powershell` :

```PS C:\Users\name> yesc.exe -i input_folder -o output_location -e```


### Build Instructions
Using `pyinstaller` to build on windows  

```pyinstaller.exe --onefile --exclude-module _bootlocale .\yesc.py```





#### Contact:
David Cirella  

