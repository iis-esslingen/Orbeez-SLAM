import os
import argparse

def read_image_data(file_path):
    """Reads image data from a text file and returns a list of (timestamp, filepath) tuples."""
    image_data = []
    with open(file_path, 'r') as file:
        for line in file:
            # Skip comments and empty lines
            if line.startswith("#") or not line.strip():
                continue
            parts = line.split()
            timestamp = float(parts[0])
            filepath = parts[1]
            image_data.append((timestamp, filepath))
    return image_data

def associate_images(rgb_data, depth_data, max_diff=0.08):
    """Associates RGB and depth images based on timestamp differences."""
    associations = []
    depth_index = 0
    num_depth_images = len(depth_data)

    for rgb_timestamp, rgb_path in rgb_data:
        while depth_index < num_depth_images:
            depth_timestamp, depth_path = depth_data[depth_index]
            time_diff = rgb_timestamp - depth_timestamp

            if abs(time_diff) < max_diff:
                associations.append((rgb_timestamp, rgb_path, depth_timestamp, depth_path))
                depth_index += 1  # Move to the next depth image
                break
            elif time_diff < 0:
                # If depth timestamp is ahead of rgb, we break to prevent moving past the best match
                break
            else:
                depth_index += 1  # Move to the next depth image to find a closer match

    return associations

def write_associations(output_file, associations):
    """Writes the associations to a text file."""
    with open(output_file, 'w') as file:
        for assoc in associations:
            file.write(f"{assoc[0]:.6f} {assoc[1]} {assoc[2]:.6f} {assoc[3]}\n")

def main():
    parser = argparse.ArgumentParser(description="Associate RGB and depth images based on timestamps.")
    parser.add_argument('--base_path', type=str, required=True, 
                        help="Base path where the rgb.txt, depth.txt, and associations.txt files are stored.")
    
    args = parser.parse_args()

    rgb_file = os.path.join(args.base_path, 'rgb.txt')
    depth_file = os.path.join(args.base_path, 'depth.txt')
    output_file = os.path.join(args.base_path, 'associations.txt')

    # Read RGB and depth image data
    rgb_data = read_image_data(rgb_file)
    depth_data = read_image_data(depth_file)

    # Associate images
    associations = associate_images(rgb_data, depth_data)

    # Write associations to file
    write_associations(output_file, associations)

    print(f"Associations written to {output_file}")

if __name__ == "__main__":
    main()
