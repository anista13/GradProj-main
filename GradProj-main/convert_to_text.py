from image_preprocess import *
from extract_infos import *
from check_grammar import *

def convert_to_text(img):
    processed_img=image_preprocess(img)
    extracted_img=extract_infos(processed_img)

    #ocr
    #email
    reader_en = easyocr.Reader(['en'])
    raw_email = reader_en.readtext(extracted_img[0], detail=0, height_ths=1, width_ths=100)
    #띄어쓰기 없애기
    email = "".join(raw_email).replace(" ", "")
    #@뒤는 한정짓기
    #####
    print(email)

    #title
    reader_ko = easyocr.Reader(['ko'])
    raw_title = reader_ko.readtext(extracted_img[1], detail=0, height_ths=1, width_ths=100)
    
    #check grammar of title
    title=check_grammar(raw_title)
    print(title)

    #info
    info = reader_ko.readtext(extracted_img[2], detail=0, height_ths=1, width_ths=100)
    print(info)
    #check grammar of each sentence in info
    refined_text=check_grammar(info)

    #insert newline
    text='\n'.join(refined_text)

    # return (email, title, text) -->tuple!!
    return (email, title, text)

#print(convert_to_text("processed.png"))