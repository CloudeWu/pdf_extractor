import json

def use_module():
    # load module
    import fitz
    from extract_content import extract_content

    # read pdf
    filename = 'file.pdf'
    with fitz.open(filename) as doc:
        pages = [page.getText('dict') for page in doc.pages()]
    
    text_content, image_content = extract_content(pages)

    # deal with text...
    for page_idx, blocks in text_content.items():
        for block in blocks:
            block_bbox = block['bbox']
            for line in block['lines']:
                word_mode = line['wmode']
                word_dir = line['dir']
                bbox = line['bbox']
                for span in line['spans']:
                    size = span['size']
                    font_flag = span['flags']
                    font = span['font']
                    color = span['color']
                    text = span['text']
                    bbox = span['bbox']

                    # do something...

    # deal with images...
    for page_idx, blocks in image_content.items():
        for block in blocks:
            bbox = block['bbox']
            extension = block['ext']
            w, h = block['width'], block['height']
            colorspace = block['colorspace']
            x_resolution, y_resolution = block['xref'], block['yref']
            bit_per_component = block['bpc']
            data = block['image']

            # do something...

def load_data():
    filename = 'output-text.json'
    with open(filename) as f:
        d = json.load(f)
    for idx, blocks in d.items():
        # do something... (refer to use_module() for more details)
        pass
