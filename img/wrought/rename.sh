 #!/bin/sh
counter = 1
for i in *.jpg *.JPG; do
    let "counter += 1"
    echo "$counter"
    echo $i 
    mv $i wrought_$counter.jpg
done
