import argparse, glob, io, os
from PIL import Image, ImageFont, ImageDraw


# Default data paths
SCRIPT_PATH = os.path.dirname(os.path.abspath(__file__))
DEFAULT_TXT_FILE = os.path.join(SCRIPT_PATH, 'characters/50characters.txt')
DEFAULT_FONTS_DIR = os.path.join(SCRIPT_PATH, 'fonts/target')
DEFAULT_OUTPUT_DIR = os.path.join(SCRIPT_PATH, 'images/target')
DEFAULT_START_IDX = 0


# Width and height of the resulting image.
IMAGE_WIDTH = 64
IMAGE_HEIGHT = 64


# Generate font image using label file
def txt2img(txt_dir, fonts_dir, output_dir, start_idx):

    with io.open(txt_dir, 'r', encoding='utf-8') as f:
        characters = f.read().splitlines()
    
    image_dir = os.path.join(output_dir)
    if not os.path.exists(image_dir):
        os.makedirs(os.path.join(image_dir))

    # Get a list of the fonts.
    fonts = glob.glob(os.path.join(fonts_dir, '*.ttf'))

    total_no = 0
    font_no = start_idx
    char_no = 0
    
    sylla_type_1 = ['게', '랴', '져', '커', '테', '폐']
    sylla_type_2 = ['뉴', '듀', '츄', '크', '표', '소', '쑈']
    sylla_type_3 = ['돼', '뛰', '의', '최'] 
    sylla_type_4 = ['긴', '깎', '넋', '닭', '떻', '많', '뱀', '집', '쨟', '핥', '실', '싫', '쌕', '썢', '앉', '엾']
    sylla_type_5 = ['굶', '뜻', '롶', '묻', '용', '읊', '줄', '쪽', '틈', '횿', '붓', '뽕']
    sylla_type_6 = ['관', '꿠', '봤', '퓥', '횤']
    
    for character in characters:

        char_no += 1
        
        if character in sylla_type_1:
            comb_type = 1
        elif character in sylla_type_2:
            comb_type = 2
        elif character in sylla_type_3:
            comb_type = 3
        elif character in sylla_type_4:
            comb_type = 4
        elif character in sylla_type_5:
            comb_type = 5
        elif character in sylla_type_6:
            comb_type = 6

        for font_path in fonts:

            total_no += 1

            try:                
                image = Image.new('RGB', (IMAGE_WIDTH,IMAGE_HEIGHT), (255, 255, 255))
                w, h = image.size
                
                drawing = ImageDraw.Draw(image)
                
                font = ImageFont.truetype(font_path, 48)
                
                new_box = drawing.textbbox((0, 0), character, font)
                new_w = new_box[2] - new_box[0]
                new_h = new_box[3] - new_box[1]
                
                box = new_box
                w = new_w
                h = new_h
                
                x = (IMAGE_WIDTH - w)//2 - box[0]
                y = (IMAGE_HEIGHT - h)//2 - box[1]
                
                drawing.text((x,y), character, fill=(0), font=font)
                file_string = f'{font_no}_{comb_type}_{ord(character):04X}.png'
                file_path = os.path.join(image_dir, file_string)
                image.save(file_path, 'PNG')
                
            except Exception as e:
                print(f"Error processing font {font_path}: {e}")
                pass
            
            font_no += 1
        font_no = start_idx
    char_no = 0
    print(f'Finished generating {total_no} images.')
    
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--txt_dir', type=str, dest='txt_dir', default=DEFAULT_TXT_FILE, help='File containing newline delimited labels.')
    parser.add_argument('--fonts_dir', type=str, dest='fonts_dir', default=DEFAULT_FONTS_DIR, help='Directory of ttf fonts to use.')
    parser.add_argument('--output_dir', type=str, dest='output_dir', default=DEFAULT_OUTPUT_DIR, help='Output directory to store generated images.')
    parser.add_argument('--start_idx', type=int, dest='start_idx', default=DEFAULT_START_IDX )
    args = parser.parse_args()
    txt2img(args.txt_dir, args.fonts_dir, args.output_dir, args.start_idx)