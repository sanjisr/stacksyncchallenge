import subprocess
import tempfile
import os
import json

NSJAIL_PATH = "/usr/bin/nsjail"
NSJAIL_CONFIG = "/app/nsjail.cfg"

def run_script(user_input: str):
    with tempfile.TemporaryDirectory() as temp_dir:
        input_path = os.path.join(temp_dir, "user_input.py")
        execute_path = os.path.join(temp_dir, "runner.py")

        with open(input_path, "w") as f:
            f.write(user_input)

        with open(execute_path, "w") as f:
            f.write(f"""
import json
import sys
sys.path.insert(0, '{temp_dir}')
try:
    import user_input
    if not hasattr(user_input, 'main'):
        raise Exception("main() function not found")
    result = user_input.main()
    json_result = json.dumps(result)
    print('||RESULT||')
    print(json_result)
except Exception as e:
    print(f"||ERROR||{{str(e)}}", file=sys.stderr)
    sys.exit(1)
""")

        cmd = [
            NSJAIL_PATH,
            '--config', NSJAIL_CONFIG,
            '--',
            'python3', execute_path
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True)


        stdout = proc.stdout.strip()
        stderr = proc.stderr.strip()

        if proc.returncode != 0:
            raise Exception(stderr or "Execution failed")

        # Extract result
        if '||RESULT||' in stdout:
            result_part = stdout.split('||RESULT||')[-1].strip()
            try:
                result_json = json.loads(result_part)
                return result_json, stdout
            except json.JSONDecodeError:
                raise Exception("main function did not return a valid JSON")
        else:
            raise Exception("main function did not return a valid result")