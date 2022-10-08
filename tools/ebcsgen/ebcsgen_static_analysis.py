import argparse

from eBCSgen.Errors.ComplexParsingError import ComplexParsingError
from eBCSgen.Errors.ModelParsingError import ModelParsingError
from eBCSgen.Errors.UnspecifiedParsingError import UnspecifiedParsingError
from eBCSgen.Parsing.ParseBCSL import Parser


def save_model(model, filename):
    f = open(filename, "w")
    f.write(repr(model))
    f.close()


args_parser = argparse.ArgumentParser(description='Static analysis')

args_parser._action_groups.pop()
required = args_parser.add_argument_group('required arguments')
optional = args_parser.add_argument_group('optional arguments')

required.add_argument('--model', type=str, required=True)
required.add_argument('--output', type=str, required=True)
required.add_argument('--method', type=str, required=True)
optional.add_argument('--complex')

args = args_parser.parse_args()

model_parser = Parser("model")
model_str = open(args.model, "r").read()
model = model_parser.parse(model_str)

if model.success:
    if args.method == "reduce":
        model.data.reduce_context()
        save_model(model.data, args.output)
    elif args.method == "eliminate":
        model.data.eliminate_redundant()
        save_model(model.data, args.output)
    else:
        complex_parser = Parser("rate_complex")
        complex = complex_parser.parse(args.complex)
        if complex.success:
            result = model.data.static_non_reachability(complex.data.children[0])
            f = open(args.output, "w")
            s = "can possibly" if result else "cannot"
            message = "The given agent\n\t{}\n{} be reached in the model.".format(complex.data.children[0], s)
            f.write(message)
            f.close()
        else:
            raise ComplexParsingError(complex.data, args.complex)
else:
    if "error" in model.data:
        raise UnspecifiedParsingError(model.data["error"])
    raise ModelParsingError(model.data, model_str)
