#!/bin/bash
# kira~
WORK_DIR=`pwd`
bopomofo_dir="$WORK_DIR"
scrcpy_dir="$WORK_DIR"
output_x=/tmp/ramfs/tmp_scrcpy_input_x
real_output_x=/tmp/ramfs/scrcpy_input_x
output_y=/tmp/ramfs/tmp_scrcpy_input_y
real_output_y=/tmp/ramfs/scrcpy_input_y
input_dir=/tmp/ramfs/scrcpy_capture
bopomofo_img=/tmp/ramfs/bopomofo.jpg
debug_dir=/tmp/ramfs/debug_capture

rm -rf $debug_dir
mkdir -p $debug_dir
mkdir -p $input_dir
touch $bopomofo_img
touch $output_x
touch $output_y
touch $real_output_x
touch $real_output_y

cd $scrcpy_dir && ./scrcpy x -m 1280 &
scrcpy_pid=$!
while [ -d /proc/$scrcpy_pid ]
do
  if [ $(ls $input_dir/*.jpg -F 2>/dev/null | wc -l) -lt 5 ]; then
#    echo "Waiting for buffer to fill"
    continue
  fi

  # Select image
  cd $input_dir/
  pwd
  current_file=$(ls -F | grep '.jpg' | sed -n 3p)
  echo $current_file

  cp $input_dir/$current_file $bopomofo_img
  # Call for bopomofo
  cd $bopomofo_dir && python3 ./main.py --input=$bopomofo_img --output_x=$output_x \
  --output_y=$output_y
#  sleep 0.3

# polling output file result. too lazy to solve.
  # cat $output_x
  # cat $output_y
  if [ $(cat $output_x) -ne -1 ] && [ $(cat $output_y) -ne -1 ]; then
    random_wait=$[ ( $RANDOM % 7 )  + 1 ]
    echo "Waiting for $random_wait second..."
    # sleep $random_wait
    cp $output_x $real_output_x
    cp $output_y $real_output_y
    sleep 0.2
    echo -1 > $real_output_x
    echo -1 > $real_output_y
  fi

  cp $input_dir/$current_file $debug_dir/$current_file
  cd $input_dir/ && rm -rf *.jpg
done

killall -9 scrcpy
