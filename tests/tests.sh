 #!/bin/bash

date
echo 'content_01_a'
:'miminal package: single file, no options' 
python3 ../xip_protocol.py -i content/content_01_a -o ../sips/sips_out/ -e

echo ' '

date
echo 'content_01_b'
:'miminal package: single file, jpg, no options'
python3 ../xip_protocol.py -i content/content_01_b -o ../sips/sips_out/ -e

date
echo 'test_03'
:'aspace sync, no parent, minimal package'
python3 ../xip_protocol.py -i content/content_01_a -o ../sips/sips_out/ -e -ao archival_object_55555


:''


#date
#echo 'test_03'
#:''
