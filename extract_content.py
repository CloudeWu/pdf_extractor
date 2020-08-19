import fitz

'''
'' logger utilities. usage: log('WARN', 'this is a warning', 3)
'' log level: 3-DEBUG, 2-INFO, 1-WARN, 0-ERROR
'''
LOG_LEVELS = ['ERROR', 'WARN', 'INFO', 'DEBUG']
def LOG(tag, content, verbose=0):
    log_level = -1
    for idx, level in enumerate(LOG_LEVELS):
        if tag.upper() == level: 
            log_level = idx
            break
    if verbose >= log_level:
        print(f' [ {tag.upper()} ] {content} ')

def process_text_block(blk, verbose=1):
    ret = {}
    ret['bbox'] = blk['bbox']
    ret['lines'] = blk['lines']
    
    ''' [TODO] add other preprocessing '''
    ''' [END TODO] '''
    
    return ret

def process_image_block(blk, verbose=1):
    ret = {}
    
    ''' [TODO] modify preprocessing step here '''
    for key, val in blk.items():
        if key != 'type':
            ret[key] = val
    ''' [END TODO] '''
    
    return ret

'''
'' Extract and seperate all text and image content from pymupdf data
'' @param textpages: 
''     array of textPage Content in dict
'' @param output_path: 
''     if set, the result will also be stored as {output_path}-[image|text].json
'''
def extract_content(textpages, skip_text=False, skip_image=False, output_path=None, verbose=2):
    LOG('INFO', f'start to extract content. #page = {len(textpages)}', verbose)
    
    book_content, book_images = {}, {}
    total_text_count, total_image_count = 0, 0
    for idx, page in enumerate(textpages):
        LOG('DEBUG', f'processing page {idx}...', verbose)
        page_text, page_images = [], []
        text_count, image_count = 0, 0
        for block in page['blocks']:
            if block['type'] == 0:    # text
                text_count += 1
                if not skip_text:
                    processed = process_text_block(block)
                    page_text.append(processed)
            elif block['type'] == 1:  # image
                image_count += 1
                if not skip_image:
                    processed = process_image_block(block)
                    page_images.append(processed)
            else:
                LOG('WARN',  f'unrecognized block type: {block["type"]}', verbose)

        book_content[idx] = page_text
        book_images[idx] = page_images
        total_text_count += text_count
        total_image_count += image_count
        LOG('DEBUG', f'  - get {text_count} text blocks, {image_count} image blocks', verbose)
    
    LOG('INFO', 'processed finished', verbose)
    LOG('DEBUG', f'  - get {text_count} text blocks, {image_count} image blocks', verbose)
    if output_path:
        import json
        if not skip_text:
            with open(f'{output_path}-text.json', 'w+') as f:
                LOG('INFO', f'writing file to {output_path}-text.json ...', verbose)
                json.dump(book_content, f)
        if not skip_image:
            with open(f'{output_path}-image.json', 'w+') as f:
                LOG('INFO', f'writing file to {output_path}-image.json ...', verbose)
                # json.dump(book_images, f)
                LOG('WARN', 'image output is not implemented so far', verbose)
        LOG('INFO', 'output finished', verbose)
    return book_content, book_images

if __name__ == '__main__':
    def parse_arg():
        import argparse
        parser = argparse.ArgumentParser()
        parser.add_argument('pdf_file', type=str, help='target pdf file')
        parser.add_argument('-o', '--output', nargs='?', default='./output', help='where to write result')
        parser.add_argument('-st', '--skip-text', action='store_true')
        parser.add_argument('-si', '--skip-image', action='store_true')
        parser.add_argument('-v', '--verbose', nargs='?', type=int, default=2, help='verbose level. 0~3')
        return parser.parse_args()
    args = parse_arg()

    LOG('INFO',  f'Get parameter: ')
    LOG('INFO',  f'  - input file: {arg.pdf_file}')
    LOG('DEBUG', f'  - output file: {arg.output}-text.json')
    LOG('DEBUG', f'  - skip text: {arg.st}')
    LOG('DEBUG', f'  - skip image: {arg.si}')
    LOG('DEBUG', f'  - verbose level: {arg.verbose}')

    LOG('INFO',  f'Gathering pdf content...')
    with fitz.open(args.pdf_file) as doc:
        pages = [page.getText('dict') for page in doc.pages()]
    extract_content(pages, 
                    skip_text=args.skip_text, 
                    skip_image=args.skip_image, 
                    output_path=args.output, 
                    verbose=args.verbose)
    
    
    
    