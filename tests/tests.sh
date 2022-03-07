 #!/bin/bash

date
echo 'content_01_a'
python3 ../xip_protocol.py -i content/content_01_a -o ../sips/sips_out/ -e

echo ' '

date
echo 'content_01_b'
python3 ../xip_protocol.py -i content/content_01_b -o ../sips/sips_out/ -e
