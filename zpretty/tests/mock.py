from zpretty.cli import CLIRunner


class MockCLIRunner(CLIRunner):
    def __init__(self, *args) -> None:
        self.errors = []
        self.config = self.parser.parse_args(args)
