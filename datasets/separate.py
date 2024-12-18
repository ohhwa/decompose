import argparse, glob, os, cv2
import numpy as np

SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))

DEFAULT_IMAGE_DIR = os.path.join(SCRIPT_PATH, 'images/target')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images/target-bbox')

# opencv > B G R
color_red = (0, 0, 255)
color_blue = (255, 0, 0)
color_green = (0, 255, 0)

def separate(images_dir, output_dir):
    
    if not os.path.exists(output_dir):
        os.makedirs(os.path.join(output_dir))
    
    images_list = sorted(glob.glob(os.path.join(images_dir, '*.png')))

    for i in range(len(images_list)):
        filename = os.path.splitext(os.path.basename(images_list[i]))[0]
        split_filename = filename.split('_')
        
        fontno = split_filename[0]
        typeno = split_filename[1]
        char_unicode = split_filename[2]
        
        image = cv2.imread(images_list[i], cv2.IMREAD_GRAYSCALE)
        if image is None:
            print(f"Error reading image: {images_list[i]}")
            continue

        _, thresh = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY_INV)
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if contours:
            coordinates = np.concatenate([contour for contour in contours])
            x, y, w, h = cv2.boundingRect(coordinates)

            bbox_image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
            
            cv2.rectangle(bbox_image, (x, y), (x + w, y + h), color_red, 1)
            
            cv2.circle(bbox_image, (x,y), 2, color_blue, -1)
            cv2.circle(bbox_image, (x+w, y+h), 2, color_green, -1)

            output_path = os.path.join(output_dir, f"{filename}_bbox.png")
            cv2.imwrite(output_path, bbox_image)
            print(f"Processed and saved: {output_path}")
        else:
            print(f"No contours found in {images_list[i]}")
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    
    parser.add_argument('--img_dir', type=str, dest='images_dir', default=DEFAULT_IMAGE_DIR)
    parser.add_argument('--output_dir', type=str, dest='output_dir', default=DEFAULT_OUTPUT_DIR)
    
    args = parser.parse_args()
    
    separate(args.images_dir, args.output_dir)
        
        