import parser

p = parser.Parser()
dependencies = p.parseToStanfordDependencies("Pick up the tire pallet.")
tupleResult = [(rel, gov.text, dep.text) for rel, gov, dep in dependencies.dependencies]

print str(tupleResult)

