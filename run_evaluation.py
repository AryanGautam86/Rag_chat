# eval/run_evaluation.py
import json, os, time, subprocess, requests, shutil, tempfile
from pathlib import Path
from typing import List
import multiprocessing
import hashlib

SERVICE_URL = "http://127.0.0.1:8000/generate_code"
EVAL_FILE = "tests/eval_prompts.jsonl"

# Config
N_SAMPLES = 10   # number of generations per prompt (n in pass@k)
KS = [1,3,5]     # compute pass@k for these k values
TIMEOUT_PER_TEST = 10  # seconds for running test_script / import

def call_generate(user_task: str, language: str="python", temperature: float=0.7):
    data = {"user_task": user_task, "language": language, "run_tests": False}
    # add temperature if your endpoint supports it
    data["temperature"] = temperature
    resp = requests.post(SERVICE_URL, data=data, timeout=60)
    return resp.json()

def extract_code_from_response(resp):
    # naive attempt to extract fenced code block
    text = resp.get("code_or_questions") or resp.get("answer") or resp.get("text") or ""
    import re
    m = re.search(r"```(?:\w+)?\n(.*?)\n```", text, re.S)
    if m:
        return m.group(1)
    # fallback: return whole text
    return text

def run_test_with_code(code_str: str, test_script: str):
    """Write code to temp file, run test_script that imports it. Return True if tests pass."""
    with tempfile.TemporaryDirectory() as td:
        code_file = Path(td) / "generated_code.py"
        code_file.write_text(code_str)
        # copy test_script into temp and run it (adjust imports if needed)
        test_dst = Path(td) / Path(test_script).name
        shutil.copy(test_script, test_dst)
        # modify test file if it assumes import name; simplest: ensure it imports generated_code
        try:
            proc = subprocess.run(["python", str(test_dst)], capture_output=True, text=True, timeout=TIMEOUT_PER_TEST)
            ok = proc.returncode == 0
            return {"ok": ok, "stdout": proc.stdout, "stderr": proc.stderr, "returncode": proc.returncode}
        except Exception as e:
            return {"ok": False, "error": str(e)}

def compute_passk(results_per_prompt: List[bool], k: int):
    # results_per_prompt: list of booleans of length n indicating whether each sample passed
    # pass@k (empirical using first k samples): whether any of first k are True
    return any(results_per_prompt[:k])

def evaluate_prompt(prompt_entry, n_samples=N_SAMPLES, temperature=0.7):
    prompt = prompt_entry["prompt"]
    language = prompt_entry.get("language","python")
    test_script = prompt_entry["test_script"]
    samples_results = []
    latencies = []
    for i in range(n_samples):
        t0 = time.time()
        resp = call_generate(prompt, language=language, temperature=temperature)
        dt = time.time() - t0
        latencies.append(dt)
        code = extract_code_from_response(resp)
        test_res = run_test_with_code(code, test_script)
        samples_results.append(test_res["ok"])
    # compute metrics
    passk = {str(k): compute_passk(samples_results, k) for k in KS}
    pass_ratio = sum(1 for r in samples_results if r)/len(samples_results)
    return {
        "id": prompt_entry["id"],
        "n_samples": n_samples,
        "pass_ratio": pass_ratio,
        "passk": passk,
        "latency_mean": sum(latencies)/len(latencies),
        "latency_p95": sorted(latencies)[int(0.95*len(latencies))-1],
        "samples_results": samples_results
    }

def main():
    out = []
    with open(EVAL_FILE) as f:
        for line in f:
            entry = json.loads(line)
            print("Evaluating:", entry["id"])
            r = evaluate_prompt(entry)
            out.append(r)
            print(" ->", r["passk"], "pass_ratio:", r["pass_ratio"])
    # summary
    total = len(out)
    for k in KS:
        succ = sum(1 for r in out if r["passk"][str(k)])
        print(f"pass@{k}: {succ}/{total} = {succ/total:.3f}")
    # overall pass_ratio mean
    mean_pass_ratio = sum(r["pass_ratio"] for r in out)/total
    print("Mean pass_ratio@n:", mean_pass_ratio)
    # save results
    Path("eval_results.json").write_text(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
