from PyPDF2 import PdfFileReader,PdfFileWriter
from pathlib import Path
import re



pdf=PdfFileReader('conops3.pdf')

#page 1
#page_1_object=pdf.getPage(0)
#rint(page_1_object)

#page_1_text=page_1_object.extractText()
# print("strat")
# print(pdf,"here")

# with Path('conops3.text').open(mode='w') as output_file:
#     text=''
#     for page in pdf.pages:
#         text+=page.extractText()
#     output_file.write(text)

search_words=['will']
concepts_dict={'Goal':['will be','proposed system'],'principle':['believe','should']}

concepts=[]
dict={}

for page in pdf.pages:
    page_num=page['/StructParents']
    page_text=page.extractText()
    #for text extracted from pdf sentences are better split by "." and not split line "\n" but is rstrip neccassary?
    #regular expressions could be used re.split('\.\W+|\?\W+|\!\W+', page_text)
    sentences = page_text.rstrip().split(".") 
    for sentence in sentences:
        for k in concepts_dict.keys():
            if any(word in sentence for word in concepts_dict[k]):
                #solves the problem with \n and other extra chars
                sentence=' '.join(sentence.split())
                key1=concepts_dict[k]
                dict[k]=[sentence,page_num]
                print(dict[k])

print(dict)





   # ELB("lb") >> group1 
        #print(' '.join(sentence.split()),"end")
        #print(sentence.replace('\n', ' ').replace('\r', '').replace('  ',' '),,"end")
    #print(sentence[0],page_num)
    #print(page_text,page_num,"text and page number")
    # for line in page_text.splitlines():
    #     if any(word in line for word in search_words):
    #         print(line)




# for i in range(0, num_pages):
#     page = object.getPage(i)
#     text = page.extractText()
#     for line in text.splitlines():
#         if re.match('House|Property|street', line):
#             print(line)



#     if 'Future' in page_text:
#         concepts.append(page_num)

# print(concepts,"page concepts")

# input_pdf=PdfFileReader('conops3.pdf')

# pdf_writer=PdfFileWriter()

# for page in concepts:
#     page_object=input_pdf.getPage(page)
    
#     pdf_writer.addPage(page_object)

# with Path('concepts.pdf').open(mode='wb') as output_file_2:
#     pdf_writer.write(output_file_2)





# # find the sentence where the concept resides
# pages_sentence=[]
# for page in pdf.pages:
#     page_num=page['/StructParents']
#     page_text=page.extractText()

#     if 'Future' in page_text:
#         concepts.append(page_num)

# print(concepts,"concepts")
