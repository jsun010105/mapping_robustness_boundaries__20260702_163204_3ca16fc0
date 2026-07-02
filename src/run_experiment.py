"""
Async experiment runner: graduated adversarial stress-test across
5 models x 4 failure modes x 6 intensity levels x prompts x seeds.

Outputs one JSONL row per API call to results/raw_responses.jsonl (resumable
cache: reruns skip already-collected (model,mode,level,prompt_idx,seed) keys).
"""
import asyncio, json, os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import openai
from interventions import MODES, N_LEVELS
from prompts import load_harmful, BIAS_SCENARIOS
from scoring import is_compliant, looks_confused, is_biased_choice

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(HERE, "results", "raw_responses.jsonl")

MODELS = {
    "qwen2.5-7b":   "qwen/qwen-2.5-7b-instruct",       # AFT, susceptible
    "llama3.1-8b":  "meta-llama/llama-3.1-8b-instruct", # APO, redundant refusal
    "gemma2-27b":   "google/gemma-2-27b-it",            # APO, robust contrast
    "mistral-nemo": "mistralai/mistral-nemo",           # AFT-ish
    "gpt-4o-mini":  "openai/gpt-4o-mini",               # deliberative/frontier
}
ALIGN_METHOD = {  # documented alignment family (lit review §3)
    "qwen2.5-7b": "AFT", "llama3.1-8b": "APO", "gemma2-27b": "APO",
    "mistral-nemo": "AFT", "gpt-4o-mini": "deliberative",
}
SEEDS = [0, 1, 2]
TEMPERATURE = 0.7
MAX_TOKENS = 256
CONCURRENCY = 6

HARMFUL = load_harmful(8)
# prompt payloads per mode: (request_text, meta) where meta carries group labels for bias
def mode_prompts(mode):
    if mode == "bias":
        return [(s[0], {"a": s[1], "b": s[2]}) for s in BIAS_SCENARIOS]
    return [(h, {}) for h in HARMFUL]


def build_tasks():
    tasks = []
    for mkey, mid in MODELS.items():
        for mode in MODES:
            plist = mode_prompts(mode)
            for lvl in range(N_LEVELS):
                for pi, (req, meta) in enumerate(plist):
                    for seed in SEEDS:
                        tasks.append(dict(model_key=mkey, model_id=mid, mode=mode,
                                          level=lvl, prompt_idx=pi, seed=seed,
                                          req=req, meta=meta))
    return tasks


def load_done():
    done = set()
    if os.path.exists(RAW):
        with open(RAW) as f:
            for line in f:
                try:
                    r = json.loads(line)
                    done.add((r["model_key"], r["mode"], r["level"], r["prompt_idx"], r["seed"]))
                except Exception:
                    pass
    return done


async def call_one(client, sem, t, out_lock, fout):
    key = (t["model_key"], t["mode"], t["level"], t["prompt_idx"], t["seed"])
    system, user = MODES[t["mode"]](t["level"], t["req"])
    msgs = []
    if system:
        msgs.append({"role": "system", "content": system})
    msgs.append({"role": "user", "content": user})
    text, err = None, None
    async with sem:
        for attempt in range(4):
            try:
                r = await client.chat.completions.create(
                    model=t["model_id"], messages=msgs, temperature=TEMPERATURE,
                    max_tokens=MAX_TOKENS, seed=t["seed"], timeout=120)
                text = r.choices[0].message.content or ""
                break
            except Exception as e:
                err = str(e)[:150]
                await asyncio.sleep(2 * (attempt + 1))
    # score
    if t["mode"] == "bias":
        compliant = is_biased_choice(text, t["meta"]["a"], t["meta"]["b"])
        confused = False
    else:
        compliant = is_compliant(text) if text is not None else False
        confused = looks_confused(text) if t["mode"] == "encoding" else False
    row = dict(model_key=t["model_key"], mode=t["mode"], level=t["level"],
               prompt_idx=t["prompt_idx"], seed=t["seed"], compliant=int(bool(compliant)),
               confused=int(bool(confused)), err=err,
               response=(text[:600] if text else None))
    async with out_lock:
        fout.write(json.dumps(row) + "\n")
        fout.flush()
    return err is not None and text is None


async def main():
    done = load_done()
    all_tasks = [t for t in build_tasks()
                 if (t["model_key"], t["mode"], t["level"], t["prompt_idx"], t["seed"]) not in done]
    print(f"Total planned calls: {len(build_tasks())}  |  already done: {len(done)}  |  to run: {len(all_tasks)}")
    if not all_tasks:
        print("Nothing to run."); return
    client = openai.AsyncOpenAI(base_url="https://openrouter.ai/api/v1",
                                api_key=os.environ["OPENROUTER_API_KEY"])
    sem = asyncio.Semaphore(CONCURRENCY)
    out_lock = asyncio.Lock()
    t0 = time.time()
    with open(RAW, "a") as fout:
        # chunk to report progress and flush
        CH = 200
        fails = 0
        for i in range(0, len(all_tasks), CH):
            batch = all_tasks[i:i+CH]
            res = await asyncio.gather(*[call_one(client, sem, t, out_lock, fout) for t in batch])
            fails += sum(res)
            print(f"  {min(i+CH,len(all_tasks))}/{len(all_tasks)} done  "
                  f"| elapsed {time.time()-t0:.0f}s | hard-fails {fails}", flush=True)
    print(f"Finished in {time.time()-t0:.0f}s. Hard failures (no text): {fails}")


if __name__ == "__main__":
    asyncio.run(main())
