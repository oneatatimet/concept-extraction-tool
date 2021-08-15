from lxml import etree
from PyPDF2 import PdfFileReader
import random
import string
import spacy
from spacy.matcher import Matcher
import json
 
pdf=PdfFileReader('conops3.pdf')
key_count=0

def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

identifier="id-"+id_generator()

match_elem_tbl=dict()
relations=dict()
nodes=dict()

Goal = [[{'TEXT':'must'},{'IS_ASCII': True, 'OP': '*'},{'POS':'ADJ'}],
                    [{'TEXT':'will'},{'TEXT':'be'}],[{'LOWER':'proposed'},{'LOWER':'system'}],
                    [{'TEXT':'future'},{'TEXT':'system'}]] #no model aux # Extra search add nouns ending with ility +future aux

Principle=[[{'LEMMA':'believe'}]]

################################################ NLP: spaCy Matcher ######################################
nlp = spacy.load('en_core_web_sm')
matcher = Matcher(nlp.vocab)
matcher.add('Goal',Goal)
matcher.add('Principle',Principle)

for page in pdf.pages:
    page=page.extractText().rstrip()
    cleanPage=' '.join(page.split())
    doc=nlp(cleanPage)
    for num,sentence in enumerate(doc.sents):
        match=matcher(sentence)
        if(match):
             for match_id, start, end in match:
                 string_id = nlp.vocab.strings[match_id]  # Get string representation
                 span = doc[start:end]  # The matched span
                 #print(match_id, string_id, start, end, span.text,'->',sentence)
                 if string_id in match_elem_tbl:
                     match_elem_tbl[string_id].append(["id-"+id_generator(), string_id,str(sentence)])
                 else:
                    match_elem_tbl[string_id]=[]
                    key_count+=1
                    match_elem_tbl[string_id].append(["id-"+id_generator(),string_id,str(sentence)])
                    

         
#print(match_elem_tbl)
# for page in pdf.pages:
#     # print(page.extractText())
#     page=page.extractText().rstrip()
#     cleanSentence=' '.join(page.split())
#     page_doc=nlp(cleanSentence)
#     for num,sentence in enumerate(page_doc.sents):
#         sentence1=sentence
#         for word in sentence1:
#             print(f'{num}:{sentence1}')
#             #print(word,word.pos_)
# print(displacy.render(doc))

################################################ section system overview of ConOps ######################################
# Definition:
# there is one main goal that relates to many goals and princibles. (1:n)
# Motivation extension elements: Goal, Principle.
# Initial high-level goals.
######################################################################################


################################################ without NLP ######################################
concepts_dict={'Goal':['will be','proposed system','future system'],'principle':['believe','should']}

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
                dict[k]=[sentence,page_num,"id-"+id_generator()] 


################################################ ArchiMate Modeles ######################################
language="en"
relationshipType=['Realization','Association']
################################################ Main Model ######################################

Name={None:language}
attr_qname = etree.QName('http://www.w3.org/2001/XMLSchema-instance', 'schemaLocation') #one way to work out prefix using Qname
class XMLNamespaces: #another way using class 
   xsi = "http://www.w3.org/2001/XMLSchema-instance"
   xml= "http://www.w3.org/XML/1998/namespace"

model = etree.Element('model',
                     {attr_qname: 'http://www.opengroup.org/xsd/archimate/3.0/http://www.opengroup.org/xsd/archimate/3.0/archimate3_Diagram.xsd'},
                     nsmap={None: 'http://www.opengroup.org/xsd/archimate/3.0/',
                            'xsi': 'http://www.w3.org/2001/XMLSchema-instance'},
                            identifier=identifier
                            )
name=etree.SubElement(model,"name",
                        {etree.QName(XMLNamespaces.xml, "lang"): language})
name.text="new model"


################################################ Elements ######################################
elements=etree.SubElement(model,"elements")

# for k in dict.keys():
#     print(dict[k][2],k)
#     element = etree.SubElement(elements, "element",
#                              {etree.QName(XMLNamespaces.xsi, "type"): k},identifier=dict[k][2])
#     name=etree.SubElement(element,"name",
#                         {etree.QName(XMLNamespaces.xml, "lan"): language})
#     name.text=dict[k][0]

all_elem_id=[]
for k in match_elem_tbl.keys():
    for e in match_elem_tbl[k]:
        element = etree.SubElement(elements, "element",{etree.QName(XMLNamespaces.xsi, "type"): k},identifier=e[0])
        name=etree.SubElement(element,"name",{etree.QName(XMLNamespaces.xml, "lang"): language})
        name.text=e[2]
        all_elem_id.append(e[0])

print(all_elem_id)

################################################ relationShips ######################################
# determine number of relationships
# determine type of each relation?
# determine direction of the relation?

relationships=etree.SubElement(model,"relationships")
for k in match_elem_tbl:
    for elem in range(len(match_elem_tbl[k])-1):
        print("elem",elem)
        rel_id="id-"+id_generator()
        relationship=etree.SubElement(relationships,'relationship',{etree.QName(XMLNamespaces.xsi,"type"): relationshipType[1]},
        identifier=rel_id,source=match_elem_tbl[k][0][0],target=match_elem_tbl[k][elem+1][0])
        if rel_id in relations:
            relations[rel_id].append([match_elem_tbl[k][0][0],match_elem_tbl[k][elem+1][0]])
        else:
            relations[rel_id]=[]
            relations[rel_id].append([match_elem_tbl[k][0][0],match_elem_tbl[k][elem+1][0]])

print("relations",relations)

################################################ views #############################################
views=etree.SubElement(model,"views")
diagrams=etree.SubElement(views,"diagrams")
view=etree.SubElement(diagrams,"view",{etree.QName(XMLNamespaces.xsi,"type"): "Diagram"},identifier="id-"+id_generator())
name=etree.SubElement(view,"name",{etree.QName(XMLNamespaces.xml, "lang"): language})
name.text="default view"
xc=528
yc=168
wc=133
hc=121
for id in all_elem_id:
    xc+=50
    yc+=50
    wc+=50
    hc+=50
    node_id="id-"+id_generator()
    node=etree.SubElement(view,"node",{etree.QName(XMLNamespaces.xsi,"type"): "Element"},identifier=node_id,x=str(xc), y=str(yc), w=str(wc), h=str(hc),elementRef=id)
    nodes[id]=node_id

print(nodes,"nodes")


# for id in relations:
#     for ts in relations[id]:
#         connection=etree.SubElement(view,"connection",{etree.QName(XMLNamespaces.xsi,"type"): "Relationship"},identifier="id-"+id_generator(),relationshipRef=id,source=ts[0],target=ts[1])
#         # print(id,ts[0],ts[1])

for id in relations:
    for ts in relations[id]:
        print(relations[id],'element',ts[0],nodes[ts[0]],'source',nodes[ts[1]],'target')
        connection=etree.SubElement(view,"connection",{etree.QName(XMLNamespaces.xsi,"type"): "Relationship"},identifier="id-"+id_generator(),relationshipRef=id,source=nodes[ts[0]],target=nodes[ts[1]])
    
    
tree=etree.ElementTree(model)
tree.write("model.xml",pretty_print=True)







