import argparse
import glob
import io
import os
from PIL import Image, ImageFont, ImageDraw


# Default data paths
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TXT_FILE = os.path.join(SCRIPT_PATH, 'characters/50characters.txt')
DEFAULT_FONTS_DIR = os.path.join(SCRIPT_PATH, 'fonts/target')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images/target')


# Width and height of the resulting image.
IMAGE_WIDTH = 256
IMAGE_HEIGHT = 256


# Generate font image using label file
def txt2img(txt_dir, fonts_dir, output_dir):

    with io.open(txt_dir, 'r', encoding='utf-8') as f:
        characters = f.read().splitlines()
    
    image_dir = os.path.join(output_dir)
    if not os.path.exists(image_dir):
        os.makedirs(os.path.join(image_dir))

    # Get a list of the fonts.
    fonts = glob.glob(os.path.join(fonts_dir, '*.ttf'))

    total_no = 0
    font_no = 1
    char_no = 0
    
    for character in characters:

        char_no += 1

        for font_path in fonts:

            total_no += 1

            try:                
                image = Image.new('RGB', (IMAGE_WIDTH,IMAGE_HEIGHT), (255, 255, 255))
                w, h = image.size
                
                drawing = ImageDraw.Draw(image)
                
                font = ImageFont.truetype(font_path, 170)
                
                new_box = drawing.textbbox((0, 0), character, font)
                new_w = new_box[2] - new_box[0]
                new_h = new_box[3] - new_box[1]
                
                box = new_box
                w = new_w
                h = new_h
                
                x = (IMAGE_WIDTH - w)//2 - box[0]
                y = (IMAGE_HEIGHT - h)//2 - box[1]
                
                drawing.text((x,y), character, fill=(0), font=font)
                file_string = f'{font_no}_{char_no:05d}.png'
                file_path = os.path.join(image_dir, file_string)
                image.save(file_path, 'PNG')
            except Exception as e:
                print(f"Error processing font {font_path}: {e}")
                pass
            
            font_no += 1
            
        font_no = 1
    char_no = 0

    print(f'Finished generating {total_no} images.')
    

if __name__ == '__main__':

    parser = argparse.ArgumentParser()

    parser.add_argument('--txt_dir', type=str, dest='txt_dir', default=DEFAULT_TXT_FILE, help='File containing newline delimited labels.')
    parser.add_argument('--fonts_dir', type=str, dest='fonts_dir', default=DEFAULT_FONTS_DIR, help='Directory of ttf fonts to use.')
    parser.add_argument('--output_dir', type=str, dest='output_dir', default=DEFAULT_OUTPUT_DIR, help='Output directory to store generated images.')

    args = parser.parse_args()

    txt2img(args.txt_dir, args.fonts_dir, args.output_dir)