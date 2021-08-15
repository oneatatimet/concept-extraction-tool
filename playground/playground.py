# import xml.etree.cElementTree as ET

# root = ET.Element("root",xmlns="http://www.opengroup.org/xsd/archimate/3.0/",'xmlns:xsi'="http://www.w3.org/2001/XMLSchema-instance", xsi:schemaLocation="http://www.opengroup.org/xsd/archimate/3.0/ http://www.opengroup.org/xsd/archimate/3.0/archimate3_Diagram.xsd" identifier="id-1")
# doc = ET.SubElement(root, "doc")

# ET.SubElement(doc, "field1", name="blah").text = "some value1"
# ET.SubElement(doc, "field2", name="asdfasd").text = "some vlaue2"

# tree = ET.ElementTree(root)
# tree.write("filename.xml")


# XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
# XHTML = "{%s}" % XHTML_NAMESPACE


# NSMAP = {'XHTML2':XHTML_NAMESPACE2} # the default namespace (no prefix)
# #NSMAP2={None:XHTML_NAMESPACE2}

# xhtml = etree.Element( "model", nsmap=NSMAP) # lxml only!
# body = etree.SubElement(xhtml, XHTML + "body")
# body.text = "Hello World"

# print(etree.tostring(xhtml, pretty_print=True))
# tree = etree.ElementTree(xhtml)
# tree.write("filename.xml")

# XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
# XHTML = "{%s}" % XHTML_NAMESPACE

# root=etree.Element("html1",prefix="first")
# sub=etree.SubElement(root,"subhtml",subprefix=XHTML)
# tree=etree.ElementTree(root)


from lxml import etree
import random
import string
def id_generator(size=12, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# XHTML_NAMESPACE = "http://www.w3.org/1999/xhtml"
# XHTML = "{%s}" % XHTML_NAMESPACE
# HTML_NAMESPACE2 ="http://www.w3.org/2001/XMLSchema-instance"
# XHTML2 = "{%s}" % HTML_NAMESPACE2
# HTML_NAMESPACE3 ="http://www.opengroup.org/xsd/archimate/3.0/http://www.opengroup.org/xsd/archimate/3.0/archimate3_Diagram.xsd"
# XHTML3 = "{%s}" % HTML_NAMESPACE3 
#NSMAP = {None:XHTML_NAMESPACE,"xsi":HTML_NAMESPACE2,"schemaLocation":HTML_NAMESPACE3} # the default namespace (no prefix)

identifier="id-"+id_generator()
language="en"
elemntType=['Goal','Principle']
relationshipType=['Realization']



Name={None:language}


# NSMAP_elemnt=
# NSMAP_relationship=
# NSMAP2={"xsi":HTML_NAMESPACE2}
# NSMAP3={NSMAP2:HTML_NAMESPACE3}
# NSMAP4={NSMAP3:HTML_NAMESPACE4}


# <element identifier="id-707384ad-45a2-4a8a-a271-4f589864fd9c" xsi:type="Goal">
# <name xml:lang="en">(new model)</name>
# <relationship identifier="id-0b3d7cb2-dd7c-4aea-86b5-250ef1a2f19d" source="na1" target="id-707384ad-45a2-4a8a-a271-4f589864fd9c" xsi:type="Realization" />




# model = etree.Element( "model", nsmap=NSMAP,identifier=identifier) # lxml only!
# name = etree.SubElement(model, "name", nsmap={'lang': language,'xsi':'mvnvmbn'})
# name.text="first"
# element=etree.SubElement(name,"element")

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
                        {etree.QName(XMLNamespaces.xml, "lan"): language})
name.text="new model"
elements=etree.SubElement(model,"elements")
element = etree.SubElement(elements, "markList",
                             {etree.QName(XMLNamespaces.xsi, "type"): elemntType[0]},identifier=identifier)
name=etree.SubElement(element,"name",
                        {etree.QName(XMLNamespaces.xml, "lan"): language})                     
relationships=etree.SubElement(model,"relationships")

relationship=etree.SubElement(relationships,"relationship",{etree.QName(XMLNamespaces.xsi, relationshipType[0]): type[0]})
views=etree.SubElement(model,"views")
diagram=etree.SubElement(views,"diagram")
view=etree.SubElement(diagram,"view")
name=etree.SubElement(view,"name")
node=etree.SubElement(view,"node")
connection=etree.SubElement(view,"connection")





# <element identifier="id-707384ad-45a2-4a8a-a271-4f589864fd9c" xsi:type="Goal">
#       <name xml:lang="en">Goal</name>
#     </element>



tree=etree.ElementTree(model)
tree.write("filenamee.xml")
