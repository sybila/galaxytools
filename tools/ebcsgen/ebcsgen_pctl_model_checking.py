import argparse

from eBCSgen.Analysis.PCTL import PCTL
from eBCSgen.Parsing.ParseBCSL import load_TS_from_json
from eBCSgen.Errors.FormulaParsingError import FormulaParsingError
from eBCSgen.Errors.InvalidInputError import InvalidInputError
from eBCSgen.Parsing.ParsePCTLformula import PCTLparser


args_parser = argparse.ArgumentParser(description='Model checking')

args_parser._action_groups.pop()
required = args_parser.add_argument_group('required arguments')
optional = args_parser.add_argument_group('optional arguments')

required.add_argument('--transition_file', required=True)
required.add_argument('--output', type=str, required=True)
required.add_argument('--formula', type=str, required=True)

args = args_parser.parse_args()

ts = load_TS_from_json(args.transition_file)

if len(ts.params) != 0:
    raise InvalidInputError("Provided transition system is parametrised - model checking cannot be executed.")

formula = PCTLparser().parse(args.formula)
if formula.success:
    result = PCTL.model_checking(ts, formula, storm_local=True)
    f = open(args.output, "w")
    f.write(result.decode("utf-8"))
    f.close()
else:
    raise FormulaParsingError(formula.data, args.formula)
