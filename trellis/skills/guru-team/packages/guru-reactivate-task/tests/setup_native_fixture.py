"""Prepare Git and controlled gh facts only; the actual Agent authors its result.

Run with the matching GURU_UPSTREAM_DELIVERY_SCRIPTS, through the source managed
resolver: tests/setup_native_fixture.py --directory /absolute/absent-directory
With --repository, use an already fully installed empty fixture repository;
its workflow/scripts are preserved. Without it, the helper makes a minimal
source-test fixture which still needs full installation. The actual Agent reads
the installed entry and observes current facts before authoring its result. This
helper emits no semantic result or gate and never claims native recovery.
"""
import argparse
import json
from pathlib import Path
from test_existing_implementation import ExistingFixture


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True)
    parser.add_argument("--repository", help="Already fully installed empty temporary repository on main.")
    args = parser.parse_args()
    directory = Path(args.directory).resolve()
    fixture = ExistingFixture()
    fixture.setUp(directory, installed_repository=args.repository)
    try:
        public, setup = fixture.prepare_existing()
        (directory / "public-input.json").write_text(json.dumps(public, indent=2) + "\n")
        (directory / "provider-facts.json").write_text(json.dumps({"bookkeeping": fixture.prs, "implementation": fixture.implementation_pr}, indent=2) + "\n")
        # This fixture provider implements only read calls. An unexpected write
        # command is recorded and fails, with no GitHub connection.
        provider = directory / "provider"; provider.mkdir()
        gh = provider / "gh"
        gh.write_text("#!/usr/bin/env python3\n" +
            "import json,sys\nfrom pathlib import Path\n" +
            "base=Path(__file__).resolve().parents[1]\n" +
            "args=sys.argv[1:]\n" +
            "with (base/'provider-calls.jsonl').open('a') as log: log.write(json.dumps(args)+'\\n')\n" +
            "facts=json.loads((base/'provider-facts.json').read_text())\n" +
            "if args==['auth','status']: print('controlled fixture');sys.exit(0)\n" +
            "if args==['api','repos/example/repository']: print(json.dumps({'full_name':'example/repository'}));sys.exit(0)\n" +
            "if args==['api','repos/example/repository/pulls/838']: print(json.dumps(facts['implementation']));sys.exit(0)\n" +
            "if len(args)==2 and args[0]=='api' and args[1].startswith('repos/example/repository/commits/') and args[1].endswith('/pulls'): print(json.dumps(facts['bookkeeping']));sys.exit(0)\n" +
            "sys.exit('unsupported controlled provider call')\n")
        gh.chmod(0o755)
        # Objective seeds are not the AI's route or current semantic judgment.
        seeds = {"authority": setup["authority"], "acquisition": setup["acquisition"]}
        (directory / "objective-seeds.json").write_text(json.dumps(seeds, indent=2) + "\n")
        print(json.dumps({"repository": str(fixture.root), "public_input": str(directory / "public-input.json"),
                          "objective_seeds": str(directory / "objective-seeds.json"),
                          "controlled_provider_path": str(provider),
                          "provider_facts": str(directory / "provider-facts.json"),
                          "installed_repository_preserved": bool(args.repository),
                          "next": "The actual Agent verifies the matching full installation, reads the installed Skill, observes current facts, authors semantic result and invokes the installed wrapper."}, indent=2))
    finally:
        fixture.doCleanups()


if __name__ == "__main__":
    main()
