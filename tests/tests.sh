 #!/bin/bash

date
echo 'content_01_a'
:'miminal package: single file, no options, parent in test, sod' 
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -sod 'miminal package: single file, no options, parent in test'${EPOCHSECONDS}  -e -p 31a37504-cc41-4186-9562-94d919f4b07a

echo ' '


date
echo 'content_01_a'
:'miminal package: single file, no options, parent in test, sod, sot' 
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -sod 'miminal package: single file, no options, parent in test, sod,sot'${EPOCHSECONDS} -sot content_01_a${EPOCHSECONDS}  -e -p 31a37504-cc41-4186-9562-94d919f4b07a

echo ' '


date
echo 'content_01_a'
:'miminal package: single file, no options, parent in test, sod, sot, security tag' 
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -sod 'miminal package: single file, no options, parent in test, sod,sot'${EPOCHSECONDS} -sot content_01_a${EPOCHSECONDS}  -e -p 31a37504-cc41-4186-9562-94d919f4b07a -s closed

echo ' '

date
echo 'content_01_a'
:'miminal package: single file, no options, parent in test, sa, iot, iod, s' 
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/  -iot content_01_a${EPOCHSECONDS} -iod 'asset only mode for file' -e -p 31a37504-cc41-4186-9562-94d919f4b07a -s closed -a

echo ' '


date
echo 'test_03'
:'aspace sync, no parent, minimal package, with parent'
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -e -ao archival_object_55555 -sod 'aspace sync, no parent, minimal package, with parent'${EPOCHSECONDS} -p 31a37504-cc41-4186-9562-94d919f4b07a

date
echo 'test_03'
:'aspace sync, no parent, minimal package'
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -e -ao archival_object_55555 -sod 'aspace sync, no parent, minimal package'${EPOCHSECONDS} 





date
echo 'content_01_b'
:'miminal package: single file, jpg, no options'
python3 ../yesc.py -i content/content_01_b -o ../sips/sips_out/ -e -sod 'miminal package: single file, jpg, no options' -p 31a37504-cc41-4186-9562-94d919f4b07a




date
echo 'test_03'
:'aspace sync, no parent, minimal package, NO parent'
python3 ../yesc.py -i content/content_01_a -o ../sips/sips_out/ -e -sod 'aspace sync, no parent, minimal package, NO parent' -ao archival_object_55555 




date
echo 'content_04_a'
:'multi manifestions'
python3 ../yesc.py -i content/content_04_a -o ../sips/sips_out/ -e -sod 'multi-representation' -p 5830d793-e6cd-48b0-b9bc-2508a90ada31 -r -s DIGIPRES_CLOSED




:''


#date
#echo 'test_03'
#:''
