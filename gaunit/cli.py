import pprint
import sys

import click

import gaunit
from gaunit.utils import (
    filter_keys,
    get_ga_requests_from_har,
    open_json,
    parse_ga_request,
)

from .__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help", "help"]})
@click.version_option(
    prog_name="GAUnit", version=__version__, message="%(prog)s %(version)s"
)
@click.pass_context
def cli(context):
    pass


@click.command(help="Print this help")
def help():
    with click.Context(cli) as context:
        click.echo(cli.get_help(context))


@click.command("check", help="Check events against an existing tracking plan")
@click.argument("har_file", type=click.Path())
@click.argument("test_case")
@click.option(
    "-t",
    "--tracking_plan",
    type=click.Path(),
    default="./tracking_plan.json",
)
@click.option(
    "-a",
    "--all",
    is_flag=True,
    help="print all expected events (missing and found)",
)
@click.option(
    "-tu",
    "--transport_url",
    help="custom transport URL for server side GTM",
    default="https://www.google-analytics.com",
)
def check(test_case, har_file, tracking_plan, all, transport_url):
    # TODO : test_case should be optionnal if tracking plan has only one test_case
    # if args.tracking_plan:
    #  ..
    # else:
    #     if 1 test case in tracking plan
    #         r = gaunit.check_har(args.test_case, args.tracking_plan, har_path=args.har_file)
    #     # N test case
    #     else:
    #     # # error
    #     # print("error: more than one test case in tracking plan, please specify a '--test-case' parameter ")
    #     # pass

    tp = gaunit.TrackingPlan.from_json(tracking_plan)
    r = gaunit.check_har(
        test_case, tracking_plan=tp, har_path=har_file, transport_url=transport_url
    )

    r.print_result(display_ok=all)
    if False in r.checklist_expected_events:
        sys.exit(1)  # end with return code 1 if check failed


@click.command("extract", help="From a HAR file, extract and print GA events")
@click.argument("har_file")
@click.option(
    "-f",
    "--filter",
    help="list of specific events parameters to extract seperated by `,` (other params are filtered out). Example: '--filter a,b,c'",
)
@click.option(
    "-tu",
    "--transport_url",
    help="custom transport URL for server side GTM",
    default="https://www.google-analytics.com",
)
def extract(har_file, filter, transport_url):
    har = open_json(har_file)
    requests = get_ga_requests_from_har(har, transport_url)
    events = []
    for r in requests:
        events.extend(parse_ga_request(r))

    if filter:
        param_filter = filter.split(",")
        events = [filter_keys(e, param_filter) for e in events]
    pprint.pprint(events)


cli.add_command(help)
cli.add_command(check)
cli.add_command(extract)

if __name__ == "__main__":
    cli()  # pylint: disable=no-value-for-parameter
