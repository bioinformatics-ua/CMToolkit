import argparse
import rdflib

def help():
    parser = argparse.ArgumentParser(description="Validate Ontology Mappings")
    configs = parser.add_argument_group('Global settings', 'Settings related with input/output files and dirs.')      
    configs.add_argument('-ip', '--inputprotege', dest='inputprotegefile', \
                        type=str, default="protege_output.txt", \
                        help='The output file generated from the OntologyManager.py (The Hyve scripts) (default: protege_output.txt)')
    configs.add_argument('-io', '--inputowl', dest='inputowlfile', \
                        type=str, default="root-ontology.owl", \
                        help='The owl file from the web protege (default: root-ontology.owl)')    
    configs.add_argument('-cf', '--conceptfile', dest='conceptfile', \
                        type=str, default="../../UsagiConceptMapping/Vocabularies/CONCEPT.csv", \
                        help='The CONCEPT CSV file in the OMOP CDM structure (default: ../../UsagiConceptMapping/Vocabularies/CONCEPT.csv)')
    configs.add_argument('-oo', '--outputowl', dest='outputowlfile', \
                        type=str, default="processed-ontology.owl", \
                        help='The owl output file to upload in the web protege (default: processed-ontology.owl)')
    executionMode = parser.add_argument_group('Execution Mode', 'Flags to select the execution mode!')
    executionMode.add_argument('-v', '--validate', default=False, action='store_true', \
                            help='In this mode, the script will validate the output file generated from the OntologyManager.py (default: False)')
    executionMode.add_argument('-a', '--addcc', default=False, action='store_true', \
                            help='In this mode, the script will add the concept codes from the protege pipeline(default: False)')
    return parser.parse_args()

def validateFile(file, concepts):
    counter = 0
    allConcepts = 0
    mappings = {}
    with open(file, 'r') as fp:
        for line in fp:
            line = line.strip()
            row = line.split("\t")
            if len(row) == 3:
                allConcepts += 1
                if row[2] == "None":
                    print(line)
                    counter += 1
                else:
                    if row[2] not in mappings:
                        mappings[row[2]] = line
                    else:
                        print("Match")
                        print(line)
                        print(mappings[row[2]])
            else:
                print("SOMETHING WRONG IN :" + line)
    print("Unmapped concepts: " + str(counter) + " of " + str(allConcepts))
    fp.close()

def addConceptCode(file, outputOWL, concepts):
    graph = rdflib.Graph()
    graph.load(file)
    addedList = []
    for subject, predicate, label in graph.triples((None, rdflib.namespace.RDFS.label, None)):
        if label.strip() in concepts:
            vocCode = concepts[label.strip()]
            addedList += [label.strip()]
            graph.add((subject, rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#conceptCode"), rdflib.Literal(vocCode)))
    graph.serialize(outputOWL, format="pretty-xml")
    
    conceptMissing = concepts
    for key in addedList:
        if key in conceptMissing:
            conceptMissing.pop(key)
    for key in conceptMissing:
        print("\"" + key + "\":\"" + conceptMissing[key] + "\",")

def loadConcepts(conceptFile):
    concepts = {}
    with open(conceptFile, 'r') as fp:
        next(fp)
        for line in fp:
            row = line.strip().split("\t")
            concepts[row[1]] = row[0]
    return concepts

def main():
    args = help()
    concepts = loadConcepts(args.conceptfile)
    if args.validate:
        validateFile(args.inputprotegefile, concepts)
    elif args.addcc:
        addConceptCode(args.inputowlfile, args.outputowlfile, concepts)





main()