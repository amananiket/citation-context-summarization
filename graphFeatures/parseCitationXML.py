import xml.etree.ElementTree as ET 
from xml.parsers import expat

tree = ET.parse('instanNewA.xml',parser=expat.ParserCreate('UTF-8') )
xml_file = 'instanNewA.xml'
#root = ET.parse(xml_file, parser=expat.ParserCreate('UTF-8') )
print tree
try:
	root = ET.parse(xml_file, parser=expat.ParserCreate('UTF-8') )
	print root
except:
	try:
		root = ET.parse(xml_file, parser=expat.ParserCreate('UTF-16') )
		print root
	except:
		try:

			root = ET.parse(xml_file, parser=expat.ParserCreate('ISO-8859-1') )
			print root

		except:
			try:
				root = ET.parse(xml_file, parser=expat.ParserCreate('ASCII') )
			except:
				print "no parse possible"

#for child in root:
#	print child.tag, child.attrib