"""Automated P1 smoke runner for the stateless P0 Compose demo."""

import json
import shutil
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
COMPOSE = ["docker", "compose", "--env-file", ".env"]


def run_compose(args: list[str]) -> subprocess.CompletedProcess:
    """Run a docker compose command from repository root."""
    return subprocess.run(
        COMPOSE + args,
        cwd=REPO_ROOT,
        check=False,
        text=True,
        capture_output=True,
    )


def dump_logs() -> None:
    """Dump up to 100 log lines for simulator and api to stderr."""
    for service in ("simulator", "api"):
        sys.stderr.write(f"\n--- Logs for {service} ---\n")
        proc = run_compose(["logs", "--no-color", "--tail=100", service])
        if proc.stdout:
            sys.stderr.write(proc.stdout)
        if proc.stderr:
            sys.stderr.write(proc.stderr)


def check_health(service_name: str, url: str) -> None:
    """Verify a health endpoint returns HTTP 200 with status: ok."""
    req = urllib.request.Request(url, method="GET")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            status_code = resp.status
            raw_body = resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        raise RuntimeError(f"Health check failed for {service_name} ({url}): {err}") from err

    if status_code != 200:
        raise RuntimeError(
            f"Health check {service_name} returned status {status_code}, expected 200"
        )

    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError as err:
        raise RuntimeError(
            f"Health check {service_name} returned non-JSON body: {raw_body}"
        ) from err

    if not isinstance(data, dict):
        raise RuntimeError(
            f"Health check {service_name} response is not a JSON object: {data}"
        )

    if data.get("status") != "ok":
        raise RuntimeError(
            f"Health check {service_name} expected status 'ok', got {data.get('status')}"
        )


def check_sync() -> None:
    """Verify invoice sync endpoint returns HTTP 200 and valid response envelope."""
    url = "http://localhost:8000/api/v1/sync/invoices"
    req = urllib.request.Request(url, data=b"", method="POST")
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            status_code = resp.status
            raw_body = resp.read().decode("utf-8")
    except (urllib.error.HTTPError, urllib.error.URLError) as err:
        raise RuntimeError(f"Sync invoices request failed ({url}): {err}") from err

    if status_code != 200:
        raise RuntimeError(f"Sync invoices returned status {status_code}, expected 200")

    try:
        data = json.loads(raw_body)
    except json.JSONDecodeError as err:
        raise RuntimeError(f"Sync invoices returned non-JSON body: {raw_body}") from err

    if not isinstance(data, dict):
        raise RuntimeError(f"Sync invoices response is not a JSON object: {data}")

    if data.get("status") != "success":
        raise RuntimeError(
            f"Sync invoices expected status 'success', got {data.get('status')}"
        )

    fetched_count = data.get("fetched_count")
    if not isinstance(fetched_count, int) or isinstance(fetched_count, bool):
        raise RuntimeError(
            f"Sync invoices fetched_count must be an integer, got: {type(fetched_count)}"
        )

    invoices = data.get("invoices")
    if not isinstance(invoices, list):
        raise RuntimeError(
            f"Sync invoices 'invoices' must be a list, got: {type(invoices)}"
        )

    if fetched_count != len(invoices):
        raise RuntimeError(
            f"Sync invoices fetched_count ({fetched_count}) does not match invoices length ({len(invoices)})"
        )


def parse_ps_json(output: str) -> list[dict]:
    """Parse docker compose ps --format json output."""
    output = output.strip()
    if not output:
        return []
    if output.startswith("["):
        try:
            return json.loads(output)
        except json.JSONDecodeError:
            pass
    items = []
    for line in output.splitlines():
        line = line.strip()
        if line:
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                pass
    return items


def main() -> int:
    compose_yaml = REPO_ROOT / "compose.yaml"
    env_example = REPO_ROOT / ".env.example"
    env_file = REPO_ROOT / ".env"

    if not compose_yaml.exists():
        sys.stderr.write(f"Error: {compose_yaml} does not exist.\n")
        return 1
    if not env_example.exists():
        sys.stderr.write(f"Error: {env_example} does not exist.\n")
        return 1

    created_env = False
    if env_file.exists():
        created_env = False
    else:
        shutil.copyfile(env_example, env_file)
        created_env = True

    started = False
    try:
        # Validate Compose
        config_proc = run_compose(["config"])
        if config_proc.returncode != 0:
            sys.stderr.write(f"docker compose config failed:\n{config_proc.stderr}\n")
            return 1

        # Start Compose
        up_proc = run_compose(["up", "--build", "-d"])
        if up_proc.returncode != 0:
            sys.stderr.write(f"docker compose up failed:\n{up_proc.stderr}\n")
            return 1
        started = True

        # Poll for health (up to 90 seconds)
        start_time = time.time()
        timeout_seconds = 90.0
        both_healthy = False

        while time.time() - start_time < timeout_seconds:
            ps_proc = run_compose(["ps", "--format", "json"])
            containers = parse_ps_json(ps_proc.stdout)

            api_healthy = False
            sim_healthy = False

            for c in containers:
                svc = c.get("Service") or c.get("service")
                health = (c.get("Health") or "").lower()
                status = (c.get("Status") or "").lower()
                is_healthy = health == "healthy" or "(healthy)" in status

                if svc == "api" and is_healthy:
                    api_healthy = True
                elif svc == "simulator" and is_healthy:
                    sim_healthy = True

            if api_healthy and sim_healthy:
                both_healthy = True
                break

            time.sleep(2)

        if not both_healthy:
            raise RuntimeError(
                "Timed out waiting for api and simulator to report healthy status (90s)"
            )

        # Loopback checks
        check_health("simulator", "http://localhost:5000/health")
        check_health("api", "http://localhost:8000/health")
        check_sync()

        print("P0 Compose smoke validation passed successfully.")
        return 0

    except KeyboardInterrupt:
        sys.stderr.write("\nInterrupted by user (Ctrl+C).\n")
        return 130
    except Exception as exc:
        sys.stderr.write(f"\nSmoke test failure: {exc}\n")
        if started:
            dump_logs()
        return 1
    finally:
        if started:
            run_compose(["down"])
        if created_env and env_file.exists():
            env_file.unlink()


if __name__ == "__main__":
    sys.exit(main())
