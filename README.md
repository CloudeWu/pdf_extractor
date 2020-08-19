PDF EXTRACT 
====================  
 
preprocess.py
---------------------
A simple template to start preprocessing.  

extract_content.py
-------------------------
The function `extract_content(textpages)` get an array of fitz.textPage's output dict as input, and seperate text and image content into different dict.  
**Function Return: (texts, images)**

### Usage
```
usage: extract_content.py [-h] [-o [OUTPUT]] [-st] [-si] [-v [VERBOSE]]
                          pdf_file

positional arguments:
  pdf_file              target pdf file

optional arguments:
  -h, --help            show this help message and exit
  -o [OUTPUT], --output [OUTPUT]
                        where to write result
  -st, --skip-text
  -si, --skip-image
  -v [VERBOSE], --verbose [VERBOSE]
                        verbose level
```
for example:   
 + `python extract_content.py book.pdf -o ./book -si -v 3`  
   will extract all text but not image blocks from book.pdf and store result to ./book-text.json  


### read output data
You can refer to preprocess.py for details.  
```
import json
with open(file, 'r') as f:
    data = json.load(f)
for page_idx, blocks in data.items():
    pass
```

### return format
For more detailed information, please refer to [Official Documentation](https://pymupdf.readthedocs.io/en/latest/textpage.html#dictionary-structure-of-extractdict-and-extractrawdict)  
```
texts = {
  page_idx: [ {
    "bbox": [<x0>, <y0>, <x1>, <y1>], 
    "lines": [ {
      "wmode": 0, 
      "dir": [<x_dir>, <y_dir>], 
      "bbox": [<x0>, <y0>, <x1>, <y1>], 
      "spans": [ {
        "size": <size>, 
        "flags": <flag>, 
        "font": <string>, 
        "color": <color>, 
        "text": <text>, 
        "bbox": [<x0>, <y0>, <x1>, <y1>]
      } ]
    } ]
  } ]
}
images = {
  page_idx: [ {
      "bbox": [<x0>, <y0>, <x1>, <y1>], 
      "ext": <extension>,
      "width": <w>,
      "height": <h>,
      "colorspace": <n>,
      "xref": <x res>,
      "yref": <y res>,
      "bpc": <bit per comp>
      "image": <byte string>
  } ]
}
```