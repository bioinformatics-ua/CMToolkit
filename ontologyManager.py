#!/usr/bin/env python3
import os
import sys
import traceback
import rdflib
from argparse import ArgumentParser, RawDescriptionHelpFormatter
from collections import OrderedDict

__version__ = 0.1
__date__    = "2015-12-15"
__updated__ = "2019-07-09"


class RDFObject(object):
    parent = None
    method = None
    
    def __init__(self, subject_id, label, vocCode=None):
        self.vocCode            = vocCode
        self.id                 = subject_id
        self.label              = label
        self.namespace          = self._get_name_space()
        self.visit_independent  = False 

    def _get_name_space(self):
        if len(str(self.id).split("#")) > 1:
            return str(self.id).split("#")[0]+"#"
        else:
            return str(self.id).split("/")
        

def clean_path(path):
    cleaned_path = path[0:-1]
    cleaned_path = cleaned_path.replace(" ","_")
    #cleaned_path = cleaned_path.replace("/","+")     
    return cleaned_path
    
def test_duplication(value, own_value, diction):
    if value in diction:
        msg = "Double label: {} with value {} in diction and own value of {}".format(value, diction[value], own_value)
        raise IncorrectDataException(msg)

#TODO refactor into clear recursion structure (base case or recursion)
def get_children(parent, path,result, object_list):
    """
    makes one big list, without separation of labels and paths
    """
    children = filter(lambda rdf_object: rdf_object.parent==parent.id, object_list)
    #clean_label = parent.label.replace("/","@")
    path += parent.label+"+"
    cleaned_path = clean_path(path)
    result.append(cleaned_path)
    for child in children:
        get_children(child,path,result, object_list)
    
    return result

#TODO refactor into clear recursion structure (base case or recursion)
def get_label_children(parent, path, result, object_list):
    #children = filter(lambda rdf_object: rdf_object.parent ==parent.id, object_list)
    children = [rdf_object for rdf_object in object_list if rdf_object.parent == parent.id]
    test_duplication(parent.label, path, result)
    cleaned_path = clean_path(path)
    if "Blood" in str(parent.label):
        pass
    result[parent.label] = (parent.vocCode ,cleaned_path)
    if len(children) != 0:
        path += parent.label+"+"
        for child in children:
            result = get_label_children(child, path, result, object_list)
    return result

def get_objects(graph):
    object_diction = dict()
    for subject, predicate, label in graph.triples((None, rdflib.namespace.RDFS.label, None)):
#         if str(label) == "Functional Activities Questionnaire":
#             continue
        #print(subject + " --- " + predicate + " --- " + label)
        if "Blood" in str(label):
            print(label)
        if "Diagnosis" in str(label):
            print(label)
        if subject not in object_diction:
            object_diction[subject]=RDFObject(subject, label)
        else:
            print("dublication {}".format(str(label)))
            print(subject)
            print("already in: {}".format(str(object_diction[subject].label)))
        
        object_diction[subject].method="natural"
        #{"label":o, "parent":None, "method":"natural"}

    for subject, predicate, parent in graph.triples((None, rdflib.namespace.RDFS.subClassOf, None)):
        if subject not in object_diction:
            if len(str(subject).split("#")) <2:
                continue
            else:
                label = str(subject).split("#")[1]
                if subject not in object_diction:
                    object_diction[subject]=RDFObject(subject,label)
                    object_diction[subject].method="class-based"
                else:
                    print("dublication {}".format(str(label)))
                    print(subject)
                    print("already in: {}".format(str(object_diction[subject].label)))
                #{"label":str(s).split("#")[1],"parent":o, "method":"class"}
        
        
        object_diction[subject].parent=parent
        
    for subject, predicate, boolean in graph.triples((None, rdflib.URIRef("http://www.semanticweb.org/emif/ontologies/2015/AD/isVisitIndependent"),None)):
        if subject not in object_diction:
            print("Wtf")
            continue
        if str(boolean) == "true":
            object_diction[subject].visit_independent = True
        else:
            print("False?")

    #To load the conceptCodes (ex: 200000512)
    for subject, predicate, label in graph.triples((None, rdflib.URIRef("http://www.w3.org/2000/01/rdf-schema#conceptCode"), None)):
        if subject in object_diction:
            #print(subject)
            if "http://www.semanticweb.org/acortesc/ontologies/2014/6/untitled-ontology-18#Langu" in subject:
                print(subject)
            object_diction[subject].vocCode = label.value
        else:
            print("\nSome concept code without object in list\n")
        
    return object_diction.values()

def get_label_path_diction(object_list, graph, extra_top_nodes=None):
    if extra_top_nodes == None:
        extra_top_nodes=list()
        
    #top_nodes = filter(lambda rdf_object: rdf_object.parent==None and rdf_object.namespace== str(graph.store.namespace("")), object_list)

    top_nodes = [rdf_object for rdf_object in object_list
                 if rdf_object.parent is None and rdf_object.namespace == str(graph.store.namespace(""))]
    #work around for missed by filter
    top_nodes.extend(extra_top_nodes)
    
    end = list()
    for top_node in top_nodes:
        print(top_node.label)
        #using recursion get all the children
        end.append(get_label_children(top_node, "", {}, object_list))

    final_diction =dict()
    for diction in end:
        #print(diction)
        for label, path in diction.items():
            if "Blood" in str(label):
                print(label)
#             if "Diagnosis" == str(label):
#                 if "Diagnosis" not in path:
#                     continue
            if "Diagnosis" in str(label):
                print(label)
            test_duplication(label, path, final_diction)
            final_diction[label]=path
    
    return final_diction

def sort_result(result, sort_path):
    result_list = list(result.items())
    if sort_path:
        result_list.sort(key=lambda x:x[1])
    else:
        result_list.sort()
    ordered_result = OrderedDict(result_list)
    return ordered_result

def output_result(ordered_result, output_filename):
    handle = open(output_filename,"w")
         
    template = "{label}\t{path}\t{code}\n"
    for label, path in ordered_result.items():
        line = template.format(label=label, path=path[1], code=path[0])
        handle.write(line)
        #print(line[:-1])
     
    handle.close()
    
def output_visits(visit_independence, visit_output_filename):
    with open(visit_output_filename,'w') as handle:
        template = "{label}\t{visit}\n"
        for rdf_object in visit_independence:
            row = template.format(label=rdf_object.label, visit=rdf_object.visit_independent)
            handle.write(row)

def main(arguments):
    program = os.path.basename(arguments.pop(0))
    nice_version = "{} v{!s}".format(program, __version__)
    description = "{}\n{}V{}\nMade on {}\nUpdated on {}".format(program, __doc__, __version__, __date__, __updated__)
    debug = True

    parser = ArgumentParser(description=description, formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument("-d", "--debug", dest="debug", action="store_true",
                        help="Set if you wish the original python error")
    parser.add_argument("-v", "--version", action="version", version=nice_version)
    parser.add_argument("-o", "--output", dest="output_filename", help="Provide the filename for the output")
    parser.add_argument("-s", "--sort", dest="sort_path", action="store_true", default=False,
                        help="Set the sorting on path, else the list is sorted on label")
    parser.add_argument(dest="filename", help="Provide the filename of the owl file")
    parser.add_argument("-i", "--visit-independent", dest="visit_output_filename",
                        help="Set the visit independent outputfile")
    try:
        args = parser.parse_args(arguments)
        debug = args.debug
        filename = args.filename
        output_filename = args.output_filename
        sort_path = args.sort_path
        visit_output_filename = args.visit_output_filename

        if not os.path.isfile(filename):
            print("input filename is not a file")
            sys.exit(2)

        if output_filename == None:
            output_filename = "protege_output.txt"
            print("output filename set to {}".format(output_filename))

        if visit_output_filename == None:
            visit_output_filename = "visit_independent_output.txt"
            print("visit output filename set to {}".format(visit_output_filename))

        graph = rdflib.Graph()
        graph.load(filename)

        object_list = get_objects(graph)
        for rdf_object in object_list:
            if "Blood" in str(rdf_object.label):
                print(rdf_object.label)

        # workaround for demographics and study information
        #TODO: add the concept Code here (?????)
        extra_top_nodes = list()
        for rdf_object in object_list:
            if str(rdf_object.label) == "Study Information":
                extra_top_nodes.append(rdf_object)
        demographics = RDFObject(
            rdflib.URIRef("http://www.semanticweb.org/acortesc/ontologies/2014/6/untitled-ontology-18#Demographics"),
            "Demographics",
            "2000000548") 
        demographics.method = "manual"
        extra_top_nodes.append(demographics)

        # Create the dictionary & sort  
        result = get_label_path_diction(object_list, graph, extra_top_nodes)
        ordered_result = sort_result(result, sort_path)

        visit_independence = filter(lambda rdf_object: rdf_object.visit_independent, object_list)
        output_visits(visit_independence, visit_output_filename)
        # output
        output_result(ordered_result, output_filename)

    except Exception as e:
        if debug:
            print(traceback.format_exc())
            raise
        indent = len(program) * " "
        sys.stderr.write(program + ": " + repr(e) + "\n")
        sys.stderr.write(indent + "  for help use --help or -h \n")

if __name__=="__main__":
    sys.exit(main(sys.argv))