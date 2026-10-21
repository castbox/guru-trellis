"""Host grading consumes the actual owner of each private native segment."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from runtime import eval_runner as runner

SKILLS=Path(__file__).resolve().parents[2]
REPO=SKILLS.parents[2]


class ImplementationTerminalTests(unittest.TestCase):
    def test_declared_segments_use_actual_approval_and_check_output_schemas(self):
        for case_id, terminal in (
                ('native-implementation-plan-premise','guru-approve-task-plan'),
                ('native-implementation-plan-resume','guru-check-task')):
            with self.subTest(case=case_id),tempfile.TemporaryDirectory() as temporary:
                args=argparse.Namespace(skill='guru-author-task-plan',adapter='codex',case=case_id,
                    run_root=temporary,current_package=None,comparison_package=None,
                    semantic_grading=None,human_feedback=None,mode='source')
                package,interface,_=runner.package_context(SKILLS,terminal)
                exit_id='approved' if terminal=='guru-approve-task-plan' else 'passed'
                output=next(row for row in interface['public_contracts']['outputs'] if row['exit_id']==exit_id)
                public_stdout=(package/output['example']['path']).read_text()
                def adapter(skills,descriptor,request_path,host_environment=None):
                    request=json.loads(request_path.read_text())
                    trace=request_path.parent/'native-trace.json'
                    trace.write_text(json.dumps({'terminal_skill_id':terminal}))
                    return {'corpus_sha256':request['corpus_sha256'],'capability_status':'executed',
                        'public_stdout':public_stdout,'public_stderr':'',
                        'trace_events':['public_invocation','evals_not_loaded','private_runtime_not_read'],
                        'transcript_locator':str(request_path.parent/'unit-transcript.json'),
                        'native_trace_locator':str(trace),'timing_ms':1}
                # Only the grading boundary is doubled; no native execution or
                # semantic approval is claimed by this test.
                with patch.object(runner,'call_adapter',side_effect=adapter):
                    report=runner.run(REPO,SKILLS,args)
                row=report['cases'][0]
                self.assertEqual(row['actual_exit'],exit_id)
                self.assertTrue(all(result['passed'] for result in row['deterministic_results']),
                    row['deterministic_results'])


if __name__=='__main__':
    unittest.main()
