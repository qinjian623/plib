#!/bin/bash
folder="/home/qin/workspace/Tools/"
classes_folder="./bin"
dest_folder="/home/qin/workspace/Tools/build"
jar_name="kk.jar"

cd $folder; cd $classes_folder ; jar cvf $dest_folder/$jar_name ./
