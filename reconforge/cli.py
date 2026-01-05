# reconforge/cli.py
from __future__ import annotations

import sys


MENU = {
    "1": ("userrecon", "reconforge.modules.userrecon.entry"),
    "2": ("reconbrain", "reconforge.modules.reconbrain.entry"),
    "3": ("reconvault", "reconforge.modules.reconvault.entry"),
    "4": ("reconwatcher", "reconforge.modules.reconwatcher.entry"),
    "5": ("reconmapper", "reconforge.modules.reconmapper.entry"),
}


def clear() -> None:
    # Cross-platform-ish without imports
    print("\n" * 60)


def run_module(module_path: str) -> int:
    # Import the module and call main()
    mod = __import__(module_path, fromlist=["main"])
    if not hasattr(mod, "main"):
        print(f"[!] {module_path} has no main()")
        return 1

    rc = mod.main()
    if rc is None:
        return 0
    try:
        return int(rc)
    except Exception:
        return 0


def main() -> int:
    while True:
        clear()
        print("=== ReconForge ===")
        for k in sorted(MENU.keys(), key=int):
            name, _ = MENU[k]
            print(f"{k}. {name}")
        print("0. exit")

        choice = input("\n> ").strip()

        if choice in ("0", "q", "quit", "exit"):
            print("bye 🗿")
            return 0

        if choice not in MENU:
            print("invalid option")
            input("press enter...")
            continue

        name, module_path = MENU[choice]
        print(f"\n--- launching {name} ---\n")

        try:
            rc = run_module(module_path)
            print(f"\n--- {name} exited (code {rc}) ---")
        except KeyboardInterrupt:
            print("\n--- interrupted ---")
        except Exception as e:
            print(f"\n--- crashed: {e!r} ---")

        input("\npress enter to return...")


if __name__ == "__main__":
    raise SystemExit(main())
