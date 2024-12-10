#!/bin/bash

dates=("2023-08-18" "2023-09-15" "2024-01-13" "2024-04-11" "2024-05-29_1" "2024-05-29_2" "2024-05-29_3")

for date in "${dates[@]}"; do
    echo "Processing date: $date"

    trials=("0" "1" "2" "3" "4")

    for trial in "${trials[@]}"; do
        echo "  Trial: $trial"

        ./build/mono_rover \
            ./Vocabulary/ORBvoc.txt \
            ./configs/Monocular/ROVER/d435i.yaml \
            "/workspace/mounted_directory/$date/d435i" \
            "./evaluation/mono/$date/$trial"

        ./build/rgbd_rover \
            ./Vocabulary/ORBvoc.txt \
            ./configs/RGB-D/ROVER/d435i.yaml \
            "/workspace/mounted_directory/$date/d435i" \
            "/workspace/mounted_directory/$date/d435i/associations.txt" \
            "./evaluation/rgbd/$date/$trial"
    done
done

echo "All dates processed."
