from pathlib import Path

import environs

env = environs.Env()
env.read_env(str(Path(__file__).resolve().parent.parent.parent / "env/.local"))
