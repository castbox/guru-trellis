"""Thin installed CLI/Core migration boundary; no public state algorithm."""
from __future__ import annotations

import json
import subprocess
from pathlib import Path

from files import MigrationError


BRIDGE = r"""
import fs from 'node:fs';
import {pathToFileURL} from 'node:url';
const request=JSON.parse(fs.readFileSync(0,'utf8'));
const migration=await import(pathToFileURL(request.cli+'/dist/commands/migration2.js'));
const core=await import(pathToFileURL(request.core+'/dist/task/migration-v2.js'));
if(request.action==='templates') {
  const reviewed=request.sources===null?undefined:new Map(Object.entries(request.sources));
  const files=migration.collectMigration2Templates(process.cwd(),reviewed);
  process.stdout.write(JSON.stringify({...migration.migration2TemplateCandidate(files),
    contents:Object.fromEntries([...files].map(([p,v])=>[p,Buffer.from(v).toString('base64')]))}));
} else {
  for(const task of request.plan.tasks)
    if(task.record!==undefined && task.source!==null && task.disposition.startsWith('convert_'))
      core.validateTaskV2Projection(JSON.parse(Buffer.from(task.source.content_base64,'base64').toString('utf8')),task.record);
  const result=await migration.migrate2({from:request.plan.source.version,plan:'owner-private-plan2',dryRun:request.action==='preview'},request.plan);
  process.stdout.write(JSON.stringify(result));
}
"""


def packages(fork: Path) -> tuple[Path, Path]:
    for directory in fork.parents:
        manifest = directory / "package.json"
        if not manifest.is_file():
            continue
        value = json.loads(manifest.read_text())
        if value.get("name") == "@mindfoldhq/trellis":
            core = directory.parent / "trellis-core"
            other = json.loads((core / "package.json").read_text())
            if value.get("version") != "0.7.0-castbox.3" or other.get("version") != value["version"]:
                raise MigrationError("Delivery migration requires the matching installed CLI/Core candidate")
            return directory, core
    raise MigrationError("Use the reviewed installed CLI entrypoint and its matching Core package")


def call(root: Path, fork: Path, action: str, plan: dict | None = None, sources: dict | None = None) -> dict:
    cli, core = packages(fork)
    result = subprocess.run(["node", "--input-type=module", "-e", BRIDGE], cwd=root,
                            input=json.dumps({"cli": str(cli), "core": str(core), "action": action,
                                              "plan": plan, "sources": sources}), text=True, capture_output=True)
    if result.returncode:
        # No source/private business bytes in diagnostic output.
        raise MigrationError("Installed Plan2 " + action + " rejected current inventory or projection")
    return json.loads(result.stdout)
