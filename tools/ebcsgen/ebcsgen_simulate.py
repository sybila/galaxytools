import argparse

from eBCSgen.Errors import UnspecifiedParsingError
from eBCSgen.Errors.InvalidInputError import InvalidInputError
from eBCSgen.Errors.ModelParsingError import ModelParsingError
from eBCSgen.Errors.RatesNotSpecifiedError import RatesNotSpecifiedError
from eBCSgen.Parsing.ParseBCSL import Parser


args_parser = argparse.ArgumentParser(description='Simulation')

args_parser._action_groups.pop()
required = args_parser.add_argument_group('required arguments')

required.add_argument('--model', type=str, required=True)
required.add_argument('--output', type=str, required=True)
required.add_argument('--deterministic', required=True)
required.add_argument('--direct', required=True)
required.add_argument('--runs', type=int, required=True)
required.add_argument('--max_time', type=float, required=True)
required.add_argument('--volume', type=float, required=True)
required.add_argument('--step', type=float, required=True)

args = args_parser.parse_args()

model_parser = Parser("model")
model_str = open(args.model, "r").read()

model = model_parser.parse(model_str)

if model.success:
    if len(model.data.params) != 0:
        raise InvalidInputError("Provided model is parametrised - simulation cannot be executed.")
    if not model.data.all_rates:
        raise RatesNotSpecifiedError("Some rules do not have rates specified - simulation cannot be executed.")

    if eval(args.deterministic):
        vm = model.data.to_vector_model()
        df = vm.deterministic_simulation(args.max_time, args.volume, args.step)
    else:
        if eval(args.direct):
            df = model.data.network_free_simulation(args.max_time)
        else:
            vm = model.data.to_vector_model()
            df = vm.stochastic_simulation(args.max_time, args.runs)

    df.to_csv(args.output, index=None, header=True)
else:
    if "error" in model.data:
        raise UnspecifiedParsingError(model.data["error"])
    raise ModelParsingError(model.data, model_str)
