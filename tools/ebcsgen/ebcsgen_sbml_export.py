import argparse

from eBCSgen.Errors.ModelParsingError import ModelParsingError
from eBCSgen.Errors.UnspecifiedParsingError import UnspecifiedParsingError
from eBCSgen.Parsing.ParseBCSL import Parser

import libsbml


args_parser = argparse.ArgumentParser(description='Export SBML model with usage of SBML-multi package')

args_parser._action_groups.pop()
required = args_parser.add_argument_group('required arguments')

required.add_argument('--model', type=str, required=True)
required.add_argument('--output', type=str, required=True)

args = args_parser.parse_args()

model_parser = Parser("model")
model_str = open(args.model, "r").read()

model = model_parser.parse(model_str)
if model.success:
    document = model.data.export_sbml()
    libsbml.writeSBMLToFile(document, args.output)
else:
    if "error" in model.data:
        raise UnspecifiedParsingError(model.data["error"])
    raise ModelParsingError(model.data, model_str)
