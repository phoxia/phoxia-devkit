#!/usr/bin/env python3
from __future__ import annotations

import argparse
import contextlib
import io
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tarfile
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

PACKAGE_ROOT = Path(__file__).resolve().parents[1]
TARGETS = ["claude", "codex"]
START = "<!-- PHOXIA-DEVKIT:START -->"
END = "<!-- PHOXIA-DEVKIT:END -->"
CURRENT_API_VERSION = "kit.phoxia.org/v1"
LEGACY_API_VERSIONS = frozenset({"phoxia.dev/v2"})


class DevKitError(RuntimeError):
    pass


def ensure_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)


def atomic_write(path: Path, text: str, executable: bool = False) -> None:
    ensure_dir(path.parent)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(text, encoding="utf-8", newline="\n")
    temp.replace(path)
    if executable and os.name != "nt":
        path.chmod(path.stat().st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)


def read_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise DevKitError(f"Invalid JSON file {path}: {exc}") from exc
    if not isinstance(value, dict):
        raise DevKitError(f"Expected an object in {path}")
    return value


def overlay_root(environ: Mapping[str, str] = os.environ) -> Path | None:
    raw = environ.get("PHOXIA_DEVKIT_OVERLAY", "").strip()
    if not raw:
        return None
    root = Path(raw).expanduser().resolve()
    manifest_path = root / "manifest.json"
    if not manifest_path.is_file():
        raise DevKitError(f"Overlay manifest.json not found: {manifest_path}")
    manifest = read_json(manifest_path)
    package = package_metadata()
    expected = {
        "schemaVersion": 1,
        "basePackage": package.get("package", PACKAGE_ROOT.name),
        "baseVersion": package.get("version", "unknown"),
    }
    for key, value in expected.items():
        if manifest.get(key) != value:
            raise DevKitError(f"Overlay {key} must be {value!r}: {manifest_path}")
    for path in root.rglob("*"):
        if path.is_file() and (PACKAGE_ROOT / path.relative_to(root)).exists():
            raise DevKitError(f"Overlay cannot replace public path: {path.relative_to(root)}")
    return root


def package_roots() -> tuple[Path, ...]:
    overlay = overlay_root()
    return (PACKAGE_ROOT, overlay) if overlay else (PACKAGE_ROOT,)


def resolve_component(relative: str, source_root: Path | None = None) -> Path:
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise DevKitError(f"Component path must be package-relative: {relative}")
    roots = [source_root, PACKAGE_ROOT, overlay_root()]
    for root in roots:
        if root is not None and (root / path).exists():
            return root / path
    raise DevKitError(f"Package component not found: {relative}")


def external_plugin_policy() -> dict[str, Any]:
    overlay = overlay_root()
    path = overlay / "policies" / "plugins.json" if overlay else PACKAGE_ROOT / "policies" / "plugins.json"
    if not path.exists():
        return {"required": [], "preserveIfPresent": [], "removeEvenIfPresent": []}
    return read_json(path)


def plugin_name(reference: str) -> str:
    return reference.split("@", 1)[0].strip().lower()


def read_json_optional(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}
    return value if isinstance(value, dict) else {}


def package_metadata() -> dict[str, Any]:
    return read_json_optional(PACKAGE_ROOT / "MANIFEST.json")


def discover_claude_plugin_state(home: Path) -> tuple[set[str], dict[str, Any]]:
    references: set[str] = set()
    settings = read_json_optional(home / ".claude" / "settings.json")
    enabled = settings.get("enabledPlugins", {})
    if isinstance(enabled, dict):
        references.update(str(key) for key, value in enabled.items() if bool(value))
    installed = read_json_optional(home / ".claude" / "plugins" / "installed_plugins.json")
    plugins = installed.get("plugins", {})
    if isinstance(plugins, dict):
        references.update(str(key) for key in plugins)
    known = read_json_optional(home / ".claude" / "plugins" / "known_marketplaces.json")
    return references, known


def source_from_marketplace_entry(entry: Any) -> str | None:
    if not isinstance(entry, dict):
        return None
    source = entry.get("source", entry)
    if not isinstance(source, dict):
        return None
    kind = str(source.get("source", ""))
    if kind == "github" and source.get("repo"):
        return str(source["repo"])
    if kind in {"git", "url"} and source.get("url"):
        return str(source["url"])
    if kind == "directory" and source.get("path"):
        return str(source["path"])
    return None


def external_plugin_selection(home: Path, mode: str) -> dict[str, Any]:
    policy = external_plugin_policy()
    existing, known = discover_claude_plugin_state(home)
    blocked = {
        str(item.get("name", "")).lower()
        for item in policy.get("removeEvenIfPresent", [])
        if isinstance(item, dict)
    }
    preserve = {str(item).lower() for item in policy.get("preserveIfPresent", [])}
    claude: list[str] = []
    codex: list[str] = []
    marketplaces: dict[str, str] = {}

    if mode == "curated":
        for item in policy.get("required", []):
            if not isinstance(item, dict):
                continue
            if item.get("claude"):
                claude.append(str(item["claude"]))
            if item.get("codex"):
                codex.append(str(item["codex"]))
            market = item.get("marketplace", {})
            if isinstance(market, dict) and market.get("name") and market.get("source"):
                marketplaces[str(market["name"])] = str(market["source"])

        for reference in sorted(existing):
            name = plugin_name(reference)
            if name in preserve and name not in blocked and reference not in claude:
                claude.append(reference)
                marketplace = reference.split("@", 1)[1] if "@" in reference else ""
                source = source_from_marketplace_entry(known.get(marketplace)) if marketplace else None
                if marketplace and source:
                    marketplaces[marketplace] = source

    selected_names = {plugin_name(ref) for ref in claude}
    removed = sorted(ref for ref in existing if plugin_name(ref) not in selected_names or plugin_name(ref) in blocked)
    return {
        "claude": sorted(dict.fromkeys(claude)),
        "codex": sorted(dict.fromkeys(codex)),
        "marketplaces": marketplaces,
        "existing": sorted(existing),
        "removed": removed,
    }


def backup_candidates(home: Path) -> list[Path]:
    result = [
        home / ".claude",
        home / ".claude.json",
        home / ".codex",
        home / ".agents",
        home / ".phoxia-devkit",
        home / ".claude-profiles",
        home / ".claude-plugins",
        home / ".claude-bin",
    ]
    bin_dir = home / ".local" / "bin"
    if bin_dir.exists():
        for path in sorted(bin_dir.iterdir()):
            if path.name == "phoxia-devkit" or path.name.startswith(("claude-", "codex-")):
                result.append(path)
    return [path for path in result if path.exists() or path.is_symlink()]


def create_authoritative_backup(home: Path, label: str = "authoritative") -> Path:
    backup_root = home / ".phoxia-devkit-backups"
    ensure_dir(backup_root)
    stamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    destination = backup_root / f"{label}-{stamp}.tar.gz"
    candidates = backup_candidates(home)
    with tarfile.open(destination, "w:gz") as archive:
        for path in candidates:
            archive.add(path, arcname=str(path.relative_to(home)), recursive=True)
        manifest = {
            "createdAt": datetime.now(timezone.utc).isoformat(),
            "home": str(home),
            "paths": [str(path.relative_to(home)) for path in candidates],
        }
        payload = (json.dumps(manifest, indent=2, ensure_ascii=False) + "\n").encode("utf-8")
        info = tarfile.TarInfo("PHOXIA-BACKUP-MANIFEST.json")
        info.size = len(payload)
        info.mtime = int(datetime.now().timestamp())
        import io
        archive.addfile(info, io.BytesIO(payload))
    return destination


def remove_path(path: Path) -> None:
    if path.is_symlink() or path.is_file():
        path.unlink(missing_ok=True)
    elif path.is_dir():
        shutil.rmtree(path)


def strip_mcp_configuration(value: Any) -> Any:
    blocked = {"mcpServers", "disabledMcpServers", "enabledMcpjsonServers"}
    if isinstance(value, dict):
        return {key: strip_mcp_configuration(item) for key, item in value.items() if key not in blocked}
    if isinstance(value, list):
        return [strip_mcp_configuration(item) for item in value]
    return value


def authoritative_cleanup(home: Path) -> None:
    for path in [
        home / ".claude" / "settings.json",
        home / ".claude" / "CLAUDE.md",
        home / ".claude" / "skills",
        home / ".claude" / "agents",
        home / ".claude" / "commands",
        home / ".claude" / "hooks",
        home / ".claude" / "output-styles",
        home / ".claude" / "plugins",
        home / ".codex" / "config.toml",
        home / ".codex" / "AGENTS.md",
        home / ".codex" / "agents",
        home / ".codex" / "hooks.json",
        home / ".codex" / "plugins",
        home / ".agents" / "skills",
        home / ".agents" / "plugins",
        home / ".claude-profiles",
        home / ".claude-plugins",
        home / ".claude-bin",
    ]:
        remove_path(path)

    claude_json = home / ".claude.json"
    data = read_json_optional(claude_json)
    if data:
        atomic_write(claude_json, json.dumps(strip_mcp_configuration(data), indent=2, ensure_ascii=False) + "\n")


def marketplace_settings(selection: dict[str, Any]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for name, source in selection.get("marketplaces", {}).items():
        source_value = str(source)
        if re.fullmatch(r"[^/\s]+/[^/\s]+", source_value):
            source_obj: dict[str, Any] = {"source": "github", "repo": source_value}
        elif source_value.startswith(("http://", "https://", "ssh://", "git@")):
            source_obj = {"source": "git", "url": source_value}
        else:
            source_obj = {"source": "directory", "path": source_value}
        result[str(name)] = {"source": source_obj, "autoUpdate": True}
    return result


def apply_authoritative_defaults(
    home: Path,
    default_profile: str,
    default_layers: list[str],
    targets: list[str],
    selection: dict[str, Any],
) -> None:
    instructions = profile_text(default_profile)
    if default_layers:
        instructions += "\n\n" + "\n\n".join(layer_addition(name) for name in default_layers)

    if "claude" in targets:
        claude_home = home / ".claude"
        ensure_dir(claude_home)
        atomic_write(claude_home / "CLAUDE.md", instructions + "\n")
        settings_path = Path(profile_manifest(default_profile)["path"]) / "settings.json"
        settings = read_json(settings_path) if settings_path.exists() else {}
        settings["enabledPlugins"] = {ref: True for ref in selection.get("claude", [])}
        settings["extraKnownMarketplaces"] = marketplace_settings(selection)
        atomic_write(claude_home / "settings.json", json.dumps(settings, indent=2, ensure_ascii=False) + "\n")
        for source, name in skill_sources(default_profile, default_layers):
            copy_skill(source, claude_home / "skills" / name, name, "claude")
        agent_dir = claude_home / "agents"
        ensure_dir(agent_dir)
        for source in agent_sources(default_profile, default_layers):
            shutil.copy2(source, agent_dir / source.name)

    if "codex" in targets:
        codex_home = home / ".codex"
        ensure_dir(codex_home / "agents")
        atomic_write(codex_home / "AGENTS.md", instructions + "\n")
        atomic_write(
            codex_home / "config.toml",
            'project_doc_fallback_filenames = ["CLAUDE.md"]\nproject_doc_max_bytes = 65536\n\n[agents]\nmax_threads = 6\nmax_depth = 1\n',
        )
        for source in agent_sources(default_profile, default_layers):
            name = parse_agent(source)[0]
            atomic_write(codex_home / "agents" / f"{name}.toml", codex_agent(source))


def run_external_command(command: list[str], home: Path, timeout: int = 180) -> tuple[bool, str]:
    executable = shutil.which(command[0])
    if not executable:
        return False, f"{command[0]} is not installed"
    env = os.environ.copy()
    env["HOME"] = str(home)
    try:
        completed = subprocess.run(
            command,
            cwd=home,
            env=env,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=timeout,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, str(exc)
    output = completed.stdout.strip()
    return completed.returncode == 0, output or f"exit code {completed.returncode}"


def install_external_plugins(home: Path, targets: list[str], selection: dict[str, Any], strict: bool) -> list[str]:
    warnings: list[str] = []
    marketplaces = selection.get("marketplaces", {})
    if "claude" in targets:
        for _, source in marketplaces.items():
            ok, output = run_external_command(["claude", "plugin", "marketplace", "add", str(source)], home)
            if not ok and "already" not in output.lower():
                warnings.append(f"Claude marketplace {source}: {output}")
        for reference in selection.get("claude", []):
            ok, output = run_external_command(["claude", "plugin", "install", str(reference), "--scope", "user"], home)
            if not ok:
                warnings.append(f"Claude plugin {reference}: {output}")

    if "codex" in targets:
        for name, source in marketplaces.items():
            run_external_command(["codex", "plugin", "marketplace", "remove", str(name)], home)
            ok, output = run_external_command(["codex", "plugin", "marketplace", "add", str(source), "--json"], home)
            if not ok and "already" not in output.lower():
                warnings.append(f"Codex marketplace {source}: {output}")
        for reference in selection.get("codex", []):
            ok, output = run_external_command(["codex", "plugin", "add", str(reference), "--json"], home)
            if not ok:
                warnings.append(f"Codex plugin {reference}: {output}")

    return warnings


def confirm_authoritative(args: argparse.Namespace) -> None:
    if bool(args.yes):
        return
    phrase = "REPLACE CLAUDE AND CODEX CONFIG"
    if not sys.stdin.isatty():
        raise DevKitError(f"Authoritative mode requires --yes in a non-interactive shell, or type {phrase!r} interactively")
    print("Authoritative mode will back up and replace Claude/Codex customization surfaces.")
    confirmation = input(f"Type {phrase} to continue: ").strip()
    if confirmation != phrase:
        raise DevKitError("Authoritative installation cancelled")


def safe_extract(archive: tarfile.TarFile, destination: Path) -> None:
    root = destination.resolve()
    for member in archive.getmembers():
        target = (destination / member.name).resolve()
        if target != root and root not in target.parents:
            raise DevKitError(f"Unsafe path in backup: {member.name}")
    try:
        archive.extractall(destination, filter="fully_trusted")
    except TypeError:
        archive.extractall(destination)


def available_profiles() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for package_root in package_roots():
        root = package_root / "profiles"
        if not root.exists():
            continue
        for path in sorted(root.iterdir()):
            manifest = path / "profile.json"
            if path.is_dir() and manifest.is_file():
                data = read_json(manifest)
                name = str(data.get("name") or path.name)
                if name in result:
                    raise DevKitError(f"Overlay profile conflicts with public profile: {name}")
                data["path"] = path
                data["sourceRoot"] = package_root
                result[name] = data
    return result


def available_layers() -> dict[str, dict[str, Any]]:
    result: dict[str, dict[str, Any]] = {}
    for package_root in package_roots():
        root = package_root / "layers"
        if not root.exists():
            continue
        for path in sorted(root.iterdir()):
            manifest = path / "layer.json"
            if path.is_dir() and manifest.is_file():
                data = read_json(manifest)
                name = str(data.get("name") or path.name)
                if name in result:
                    raise DevKitError(f"Overlay layer conflicts with public layer: {name}")
                data["path"] = path
                data["sourceRoot"] = package_root
                result[name] = data
    return result


def csv_values(value: str | None, allowed: list[str], label: str) -> list[str]:
    if not value or value == "all":
        return list(allowed)
    values: list[str] = []
    for item in value.split(","):
        normalized = item.strip().lower()
        if normalized and normalized not in values:
            values.append(normalized)
    invalid = [item for item in values if item not in allowed]
    if invalid:
        raise DevKitError(f"Unknown {label}: {', '.join(invalid)}")
    return values


def layer_values(values: list[str] | None, layers: dict[str, dict[str, Any]]) -> list[str]:
    result: list[str] = []
    for raw in values or []:
        for item in raw.split(","):
            item = item.strip().lower()
            if item and item not in result:
                result.append(item)
    invalid = [item for item in result if item not in layers]
    if invalid:
        raise DevKitError(f"Unknown or unavailable layer: {', '.join(invalid)}")
    return result


def preprocess_aliases(argv: list[str]) -> list[str]:
    """Convert conveniences such as --enable-<layer> and --<layer>."""
    layers = available_layers()
    result: list[str] = []
    for token in argv:
        install_match = next((name for name in layers if token == f"--enable-{name}"), None)
        project_match = next((name for name in layers if token == f"--{name}"), None)
        if install_match:
            result.extend(["--enable-layer", install_match])
        elif project_match:
            result.extend(["--layer", project_match])
        else:
            result.append(token)
    return result


def managed_merge(path: Path, block: str) -> None:
    current = path.read_text(encoding="utf-8") if path.exists() else ""
    managed = f"{START}\n{block.rstrip()}\n{END}"
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pattern.search(current):
        updated = pattern.sub(managed, current)
    elif current.strip():
        updated = current.rstrip() + "\n\n" + managed + "\n"
    else:
        updated = managed + "\n"
    atomic_write(path, updated)


def frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---\n"):
        return {}, text
    end = text.find("\n---\n", 4)
    if end < 0:
        return {}, text
    metadata: dict[str, str] = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            key, value = line.split(":", 1)
            metadata[key.strip()] = value.strip().strip('"')
    return metadata, text[end + 5 :]


def copy_skill(src: Path, dst: Path, name: str, target: str) -> None:
    metadata, body = frontmatter((src / "SKILL.md").read_text(encoding="utf-8"))
    description = metadata.get("description", "Phoxia workflow.")
    lines = ["---", f"name: {name}", f"description: {description}"]
    if target == "claude":
        for field in ("argument-hint", "disable-model-invocation"):
            if field in metadata:
                value = metadata[field]
                lines.append(f"{field}: {json.dumps(value) if field == 'argument-hint' else value}")
    lines.extend(["---", ""])
    if dst.exists():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    (dst / "SKILL.md").write_text("\n".join(lines) + body.lstrip("\n"), encoding="utf-8", newline="\n")


def profile_manifest(name: str) -> dict[str, Any]:
    profiles = available_profiles()
    if name not in profiles:
        raise DevKitError(f"Profile {name!r} is unavailable in this package")
    return profiles[name]


def profile_text(name: str) -> str:
    path = Path(profile_manifest(name)["path"])
    source = path / "AGENTS.md"
    if not source.exists():
        source = path / "CLAUDE.md"
    return source.read_text(encoding="utf-8").strip()


def layer_addition(name: str) -> str:
    data = available_layers()[name]
    path = Path(data["path"]) / str(data.get("instructionFile", "AGENTS.addition.md"))
    return path.read_text(encoding="utf-8").strip()


def plugin_paths(profile: str, layers: list[str], package_root: Path = PACKAGE_ROOT) -> list[Path]:
    data = profile_manifest(profile)
    paths: list[Path] = []
    for relative in data.get("claudePlugins", []):
        source = resolve_component(str(relative), Path(data["sourceRoot"]))
        path = installed_component(source, package_root)
        if path not in paths:
            paths.append(path)
    layer_map = available_layers()
    for name in layers:
        relative = layer_map[name].get("claudePlugin")
        if relative:
            source = Path(layer_map[name]["path"]) / str(relative)
            paths.append(installed_component(source, package_root))
    return paths


def installed_component(source: Path, package_root: Path) -> Path:
    overlay = overlay_root()
    if overlay and source.is_relative_to(overlay):
        return package_root / "overlay" / source.relative_to(overlay)
    if source.is_relative_to(PACKAGE_ROOT):
        return package_root / source.relative_to(PACKAGE_ROOT)
    raise DevKitError(f"Component is outside composed package: {source}")


def skill_sources(profile: str, layers: list[str]) -> list[tuple[Path, str]]:
    data = profile_manifest(profile)
    result: list[tuple[Path, str]] = []
    for item in data.get("skills", []):
        src = resolve_component(str(item["path"]), Path(data["sourceRoot"]))
        result.append((src, str(item["name"])))
    layer_map = available_layers()
    for layer in layers:
        root = Path(layer_map[layer]["path"])
        for item in layer_map[layer].get("skills", []):
            result.append((root / str(item["path"]), str(item["name"])))
    unique: dict[str, Path] = {}
    for src, name in result:
        unique[name] = src
    return [(src, name) for name, src in sorted(unique.items())]


def parse_agent(path: Path) -> tuple[str, str, str]:
    metadata, body = frontmatter(path.read_text(encoding="utf-8"))
    return metadata.get("name", path.stem), metadata.get("description", "Phoxia specialist agent."), body.strip()


def codex_agent(path: Path) -> str:
    name, description, body = parse_agent(path)
    body = body.replace('"""', '\\"\\"\\"')
    return (
        f"name = {json.dumps(name, ensure_ascii=False)}\n"
        f"description = {json.dumps(description, ensure_ascii=False)}\n"
        'sandbox_mode = "read-only"\n'
        'developer_instructions = """\n'
        f"{body}\n"
        '"""\n'
    )


def agent_sources(profile: str, layers: list[str]) -> list[Path]:
    data = profile_manifest(profile)
    result: list[Path] = []
    for relative in data.get("agentDirs", []):
        result.extend(sorted(resolve_component(str(relative), Path(data["sourceRoot"])).glob("*.md")))
    layer_map = available_layers()
    for layer in layers:
        root = Path(layer_map[layer]["path"])
        for relative in layer_map[layer].get("agentDirs", []):
            result.extend(sorted((root / str(relative)).glob("*.md")))
    unique: dict[str, Path] = {}
    for path in result:
        unique[parse_agent(path)[0]] = path
    return [unique[name] for name in sorted(unique)]


def startup_hint(target: str, locale: str) -> str:
    command = "$phoxia-devkit" if target == "codex" else "/phoxia-core:devkit"
    if locale.lower().replace("_", "-").startswith("pt"):
        return f"Precisa de direção? Use {command} project guide. Liste os comandos com {command} help."
    return f"Need direction? Use {command} project guide. List commands with {command} help."


def launcher_posix(command: str, environment: dict[str, str], arguments: str = '"$@"', hint: str | None = None) -> str:
    exports = "\n".join(f"export {key}={json.dumps(value)}" for key, value in environment.items())
    banner = f"printf '%s\\n' {json.dumps(hint, ensure_ascii=False)}\n" if hint else ""
    return f"#!/usr/bin/env bash\nset -euo pipefail\n{exports}\n{banner}exec {command} {arguments}\n"


def launcher_powershell(command: str, environment: dict[str, str], arguments: str = "@args", hint: str | None = None) -> str:
    assignments = "\n".join(f"$env:{key} = {json.dumps(value)}" for key, value in environment.items())
    banner = f"Write-Host {json.dumps(hint, ensure_ascii=False)}\n" if hint else ""
    return f'$ErrorActionPreference = "Stop"\n{assignments}\n{banner}& {command} {arguments}\nexit $LASTEXITCODE\n'


def cleanup_previous_install(home: Path) -> None:
    base = home / ".phoxia-devkit"
    state_path = base / "state.json"
    if state_path.exists():
        try:
            state = read_json(state_path)
        except DevKitError:
            state = {}
        for raw in state.get("managedFiles", []):
            path = Path(str(raw))
            if path.is_file() or path.is_symlink():
                path.unlink(missing_ok=True)
        for raw in sorted(state.get("managedDirs", []), key=lambda value: len(str(value)), reverse=True):
            path = Path(str(raw))
            if path != base and path.is_dir():
                shutil.rmtree(path)
    for relative in ("profiles", "package", "bin"):
        path = base / relative
        if path.exists():
            shutil.rmtree(path)


def install(args: argparse.Namespace) -> None:
    profiles_map = available_profiles()
    layers_map = available_layers()
    targets = csv_values(args.targets, TARGETS, "target")
    profiles = csv_values(args.profiles, list(profiles_map), "profile")
    layers = layer_values(args.enable_layer, layers_map)
    default_layers = layer_values(args.default_layer, layers_map)
    session_layers = [name for name in layers if not layers_map[name].get("allowedProjects")]
    home = Path(args.home).expanduser().resolve() if args.home else Path.home()
    previous_state = read_json_optional(home / ".phoxia-devkit" / "state.json")
    startup_hints = args.startup_hints if args.startup_hints is not None else bool(previous_state.get("startupHints", True))
    locale = args.locale or str(previous_state.get("locale") or os.environ.get("LANG", "en").split(".", 1)[0])

    if args.default_profile not in profiles_map:
        raise DevKitError(f"Default profile {args.default_profile!r} is unavailable")
    if args.default_profile not in profiles:
        raise DevKitError("The default profile must also be included in --profiles")
    if any(layer not in layers for layer in default_layers):
        raise DevKitError("Every --default-layer must also be enabled with --enable-layer")
    if any(layers_map[layer].get("allowedProjects") for layer in default_layers):
        raise DevKitError("Project-restricted layers cannot be authoritative defaults")

    selection = external_plugin_selection(home, args.external_plugins)
    backup_path: Path | None = None
    if args.authoritative:
        print("External plugin policy:")
        print("  keep for Claude: " + (", ".join(selection["claude"]) or "none"))
        print("  keep for Codex: " + (", ".join(selection["codex"]) or "none"))
        print("  remove: " + (", ".join(selection["removed"]) or "none detected"))
        confirm_authoritative(args)
        backup_path = create_authoritative_backup(home)
        authoritative_cleanup(home)

    cleanup_previous_install(home)
    base = home / ".phoxia-devkit"
    package_copy = base / "package"
    posix_bin = home / ".local" / "bin"
    windows_bin = base / "bin"
    ensure_dir(base)
    ensure_dir(posix_bin)
    ensure_dir(windows_bin)

    if package_copy.exists():
        shutil.rmtree(package_copy)
    shutil.copytree(PACKAGE_ROOT, package_copy, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    overlay = overlay_root()
    installed_overlay = package_copy / "overlay"
    if overlay:
        shutil.copytree(overlay, installed_overlay, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
    installed_tool = package_copy / "tools" / "phoxia_devkit.py"
    python = sys.executable

    managed_files: list[str] = []
    managed_dirs: list[str] = [str(base)]
    manager_environment = {"PHOXIA_DEVKIT_OVERLAY": str(installed_overlay)} if overlay else {}

    manager_posix = posix_bin / "phoxia-devkit"
    atomic_write(manager_posix, launcher_posix(json.dumps(python), manager_environment, json.dumps(str(installed_tool)) + ' "$@"'), True)
    managed_files.append(str(manager_posix))
    manager_ps = windows_bin / "phoxia-devkit.ps1"
    atomic_write(manager_ps, launcher_powershell(json.dumps(python), manager_environment, json.dumps(str(installed_tool)) + " @args"))
    managed_files.append(str(manager_ps))
    manager_cmd = windows_bin / "phoxia-devkit.cmd"
    command_environment = f'set "PHOXIA_DEVKIT_OVERLAY={installed_overlay}"\r\n' if overlay else ""
    atomic_write(manager_cmd, f'@echo off\r\n{command_environment}"{python}" "{installed_tool}" %*\r\n')
    managed_files.append(str(manager_cmd))

    selected: dict[str, Path] = {}
    for profile in profiles:
        for src, name in skill_sources(profile, session_layers):
            selected[name] = src
    skill_roots = {"claude": home / ".claude" / "skills", "codex": home / ".agents" / "skills"}
    for target in targets:
        skill_root = skill_roots[target]
        ensure_dir(skill_root)
        for name, src in sorted(selected.items()):
            destination = skill_root / name
            copy_skill(src, destination, name, target)
            managed_dirs.append(str(destination))

    for profile in profiles:
        suffixes: list[tuple[str, list[str]]] = [(profile, [])]
        if session_layers:
            suffixes.append((profile + "-" + "-".join(session_layers), session_layers))
        for launcher_name, active_layers in suffixes:
            if "claude" in targets:
                claude_home = base / "profiles" / "claude" / launcher_name
                ensure_dir(claude_home)
                atomic_write(claude_home / "CLAUDE.md", profile_text(profile) + ("\n\n" + "\n\n".join(layer_addition(x) for x in active_layers) if active_layers else "") + "\n")
                settings = Path(profile_manifest(profile)["path"]) / "settings.json"
                if settings.exists():
                    shutil.copy2(settings, claude_home / "settings.json")
                plugins = plugin_paths(profile, active_layers, package_copy)
                arguments = " ".join("--plugin-dir " + json.dumps(str(path)) for path in plugins) + ' "$@"'
                posix = posix_bin / f"claude-{launcher_name}"
                hint = startup_hint("claude", locale) if startup_hints else None
                atomic_write(posix, launcher_posix("claude", {"CLAUDE_CONFIG_DIR": str(claude_home)}, arguments, hint), True)
                managed_files.append(str(posix))
                ps = windows_bin / f"claude-{launcher_name}.ps1"
                ps_args = " ".join("--plugin-dir " + json.dumps(str(path)) for path in plugins) + " @args"
                atomic_write(ps, launcher_powershell("claude", {"CLAUDE_CONFIG_DIR": str(claude_home)}, ps_args, hint))
                managed_files.append(str(ps))
            if "codex" in targets:
                codex_home = base / "profiles" / "codex" / launcher_name
                ensure_dir(codex_home / "agents")
                instructions = profile_text(profile)
                if active_layers:
                    instructions += "\n\n" + "\n\n".join(layer_addition(x) for x in active_layers)
                atomic_write(codex_home / "AGENTS.md", instructions + "\n")
                atomic_write(
                    codex_home / "config.toml",
                    'project_doc_fallback_filenames = ["CLAUDE.md"]\nproject_doc_max_bytes = 65536\n\n[agents]\nmax_threads = 6\nmax_depth = 1\n',
                )
                for source in agent_sources(profile, active_layers):
                    name = parse_agent(source)[0]
                    atomic_write(codex_home / "agents" / f"{name}.toml", codex_agent(source))
                posix = posix_bin / f"codex-{launcher_name}"
                hint = startup_hint("codex", locale) if startup_hints else None
                atomic_write(posix, launcher_posix("codex", {"CODEX_HOME": str(codex_home)}, hint=hint), True)
                managed_files.append(str(posix))
                ps = windows_bin / f"codex-{launcher_name}.ps1"
                atomic_write(ps, launcher_powershell("codex", {"CODEX_HOME": str(codex_home)}, hint=hint))
                managed_files.append(str(ps))

    plugin_warnings: list[str] = []
    if args.authoritative:
        apply_authoritative_defaults(home, args.default_profile, default_layers, targets, selection)
        if not args.skip_plugin_install and args.external_plugins != "none":
            plugin_warnings = install_external_plugins(home, targets, selection, args.strict_plugins)

    metadata = package_metadata()
    state = {
        "package": metadata.get("package", PACKAGE_ROOT.name),
        "version": metadata.get("version", "unknown"),
        "installedAt": datetime.now(timezone.utc).isoformat(),
        "targets": targets,
        "profiles": profiles,
        "layers": layers,
        "authoritative": bool(args.authoritative),
        "defaultProfile": args.default_profile if args.authoritative else None,
        "defaultLayers": default_layers if args.authoritative else [],
        "externalPluginMode": args.external_plugins,
        "externalPlugins": selection if args.authoritative else {},
        "backupPath": str(backup_path) if backup_path else None,
        "pluginWarnings": plugin_warnings,
        "startupHints": startup_hints,
        "locale": locale,
        "managedFiles": managed_files,
        "managedDirs": managed_dirs,
    }
    atomic_write(base / "state.json", json.dumps(state, indent=2, ensure_ascii=False) + "\n")
    print(f"Installed targets: {', '.join(targets)}")
    print(f"Installed profiles: {', '.join(profiles)}")
    if layers:
        print(f"Installed optional layers: {', '.join(layers)}")
    if args.authoritative:
        print(f"Authoritative default: {args.default_profile}" + (" + " + ", ".join(default_layers) if default_layers else ""))
        print(f"Backup: {backup_path}")
        print("Replaced Claude/Codex customization surfaces; authentication, sessions and history were preserved.")
        if plugin_warnings:
            print("Plugin installation warnings:")
            for warning in plugin_warnings:
                print(f"  - {warning}")
    else:
        print("Existing ~/.claude and ~/.codex configuration was not changed.")
    print(f"POSIX launchers: {posix_bin}")
    print(f"PowerShell launchers: {windows_bin}")
    if plugin_warnings and args.strict_plugins:
        raise DevKitError("External plugin installation failed after the baseline was installed. Review state.json and retry plugin installation.\n" + "\n".join(plugin_warnings))


def project_block(
    profile: str,
    target: str,
    layers: list[str],
    fields: dict[tuple[str, ...], Any] | None = None,
) -> str:
    text = profile_text(profile)
    if layers:
        text += "\n\n" + "\n\n".join(layer_addition(name) for name in layers)
    if fields:
        context = [
            "## Project context",
            "",
            f"- Name: {fields.get(('metadata', 'name'), 'unspecified')}",
            f"- Purpose: {fields.get(('metadata', 'description'), 'unspecified')}",
            f"- Repository visibility: {fields.get(('repository', 'visibility'), 'unspecified')}",
            f"- Documentation visibility: {fields.get(('documentation', 'visibility'), 'unspecified')}",
            f"- Distribution model: {fields.get(('distribution', 'model'), 'unspecified')}",
        ]
        text += "\n\n" + "\n".join(context)
    text += (
        "\n\n## DevKit workflows\n\n"
        "- Inspect `.phoxia/project.yaml` before material changes.\n"
        "- Use the vendored Phoxia skills for development, project, release, documentation, UI and handoff workflows.\n"
        "- Preserve user-owned instructions outside the managed block.\n"
        "- A public version manifest change requires a changelog entry.\n"
        "- A user-facing contract or behavior change requires documentation.\n"
        "- Use a Feature Record for a significant capability, an ADR for an important local technical decision, and RFC analysis for cross-domain or governance changes.\n"
    )
    text += "- Run `/phoxia-devkit` to review DevKit configuration.\n" if target == "claude" else "- Run `$phoxia-devkit` to review DevKit configuration.\n"
    return text


def yaml_quote(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def spdx_owner(value: str) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", value).strip("-") or "Owner"


def global_skill_path(home: Path, target: str, name: str) -> Path:
    root = home / (".claude" if target == "claude" else ".agents") / "skills"
    return root / name


def ask(prompt: str, default: str) -> str:
    if not sys.stdin.isatty():
        return default
    value = input(f"{prompt} [{default}]: ").strip()
    return value or default


def validate_layer_project(project: str, layers: list[str], layer_map: dict[str, dict[str, Any]]) -> None:
    for layer in layers:
        allowed = layer_map[layer].get("allowedProjects", [])
        if allowed and project not in allowed:
            raise DevKitError(f"Layer {layer!r} is only allowed for project: {', '.join(allowed)}")


def project_init(args: argparse.Namespace) -> None:
    profiles_map = available_profiles()
    layers_map = available_layers()
    profile = args.profile
    if profile not in profiles_map:
        raise DevKitError(f"Profile {profile!r} is unavailable in this package")
    targets = csv_values(args.targets, TARGETS, "target")
    layers = layer_values(args.layer, layers_map)
    path = Path(args.path).expanduser().resolve()
    validate_layer_project(path.name, layers, layers_map)
    ensure_dir(path)

    profile_data = profiles_map[profile]
    owner = args.owner or str(profile_data.get("defaultOwner") or ask("Legal owner or maintainer", "replace-me"))
    company = args.company or owner
    description = args.description or path.name
    visibility = args.visibility or str(profile_data.get("defaultVisibility") or "unspecified")
    model = args.license_model or str(profile_data.get("defaultLicenseModel") or "unspecified")
    technical_maintainer = args.technical_maintainer or owner
    pull_request_approver = args.pull_request_approver or owner
    commercial_authority = args.commercial_authority or owner
    documentation_visibility = args.documentation_visibility or visibility

    phoxia = path / ".phoxia"
    ensure_dir(phoxia)
    project_yaml = (
        f"apiVersion: {CURRENT_API_VERSION}\n"
        "kind: ProjectContext\n"
        "metadata:\n"
        f"  name: {yaml_quote(path.name)}\n"
        f"  description: {yaml_quote(description)}\n"
        f"  profile: {yaml_quote(profile)}\n"
        f"  configuredAt: {yaml_quote(datetime.now(timezone.utc).isoformat())}\n"
        f"targets: {json.dumps(targets)}\n"
        f"layers: {json.dumps(layers)}\n"
        "ownership:\n"
        f"  owner: {yaml_quote(owner)}\n"
        f"  company: {yaml_quote(company)}\n"
        "governance:\n"
        f"  technicalMaintainer: {yaml_quote(technical_maintainer)}\n"
        f"  pullRequestApprover: {yaml_quote(pull_request_approver)}\n"
        f"  commercialAuthority: {yaml_quote(commercial_authority)}\n"
        "repository:\n"
        f"  visibility: {yaml_quote(visibility)}\n"
        "documentation:\n"
        f"  visibility: {yaml_quote(documentation_visibility)}\n"
        "distribution:\n"
        f"  model: {yaml_quote(model)}\n"
        "  legalReviewRequired: true\n"
    )
    atomic_write(phoxia / "project.yaml", project_yaml)
    project_fields = generated_yaml_fields(phoxia / "project.yaml")

    if bool(profile_data.get("licensingQuestions")):
        commercial = args.commercial_use or ask("Who may commercialize this software", "owner-only")
        redistribution = args.redistribution or ask("Redistribution policy", "written-permission")
        licensing = (
            "# Generated decision record; obtain qualified legal review.\n"
            f"model: {yaml_quote(model)}\n"
            f"owner: {yaml_quote(owner)}\n"
            f"company: {yaml_quote(company)}\n"
            f"visibility: {yaml_quote(visibility)}\n"
            f"commercialUse: {yaml_quote(commercial)}\n"
            f"redistribution: {yaml_quote(redistribution)}\n"
            f"spdxExpression: {yaml_quote('LicenseRef-' + spdx_owner(company) + '-Proprietary')}\n"
            "legalReviewRequired: true\n"
        )
        atomic_write(phoxia / "licensing.yaml", licensing)
        notice = path / "COMMERCIAL-USE.md"
        if not notice.exists():
            atomic_write(
                notice,
                f"# Commercial use\n\nThis repository is currently classified as **{model}**. Commercial use is recorded as **{commercial}** and redistribution as **{redistribution}**.\n\nThis is a project decision record, not legal advice. Final terms require approval by {owner} and qualified legal review.\n",
            )

    if "claude" in targets:
        managed_merge(path / "CLAUDE.md", project_block(profile, "claude", layers, project_fields))
    if "codex" in targets:
        managed_merge(path / "AGENTS.md", project_block(profile, "codex", layers, project_fields))

    for source, name in skill_sources(profile, layers):
        if "claude" in targets and (args.vendor_skills or not global_skill_path(Path.home(), "claude", name).is_dir()):
            copy_skill(source, path / ".claude" / "skills" / name, name, "claude")
        if "codex" in targets and (args.vendor_skills or not global_skill_path(Path.home(), "codex", name).is_dir()):
            copy_skill(source, path / ".agents" / "skills" / name, name, "codex")

    if "claude" in targets:
        agent_dir = path / ".claude" / "agents"
        ensure_dir(agent_dir)
        for source in agent_sources(profile, layers):
            shutil.copy2(source, agent_dir / source.name)
    if "codex" in targets:
        agent_dir = path / ".codex" / "agents"
        ensure_dir(agent_dir)
        for source in agent_sources(profile, layers):
            name = parse_agent(source)[0]
            atomic_write(agent_dir / f"{name}.toml", codex_agent(source))
        atomic_write(path / ".codex" / "config.toml", "[agents]\nmax_threads = 6\nmax_depth = 1\n")

    gitignore = path / ".gitignore"
    current = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""
    additions = [".phoxia/*.local.*", ".claude/settings.local.json"]
    missing = [item for item in additions if item not in current.splitlines()]
    if missing:
        atomic_write(gitignore, current.rstrip() + ("\n" if current else "") + "\n".join(missing) + "\n")

    details = f"Configured {path} as {profile} for {', '.join(targets)}"
    if layers:
        details += f" with layers {', '.join(layers)}"
    print(details + ".")


PROJECT_SURFACES = (".phoxia", ".claude", ".agents", ".codex", "AGENTS.md", "CLAUDE.md", ".gitignore", "COMMERCIAL-USE.md")


def project_files(root: Path) -> dict[Path, bytes]:
    files: dict[Path, bytes] = {}
    for name in PROJECT_SURFACES:
        surface = root / name
        paths = surface.rglob("*") if surface.is_dir() else [surface]
        for path in paths:
            if path.is_file() and ".phoxia/backups" not in path.relative_to(root).as_posix():
                files[path.relative_to(root)] = path.read_bytes()
    return files


def copy_project_surfaces(source: Path, destination: Path) -> None:
    ensure_dir(destination)
    for name in PROJECT_SURFACES:
        src = source / name
        dst = destination / name
        if not src.exists():
            continue
        if src.is_dir():
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns("backups"))
        else:
            ensure_dir(dst.parent)
            shutil.copy2(src, dst)


def project_init_transaction(args: argparse.Namespace) -> None:
    target = Path(args.path).expanduser().resolve()
    ensure_dir(target)
    managed = (target / ".phoxia" / "project.yaml").is_file() or any(
        START in (target / name).read_text(encoding="utf-8", errors="replace")
        for name in ("AGENTS.md", "CLAUDE.md") if (target / name).is_file()
    )
    if args.mode == "add" and managed:
        raise DevKitError("add mode refuses to replace an existing managed project; use --mode update or replace")
    if args.mode == "update" and not managed:
        raise DevKitError("update mode requires an existing managed project; use --mode add")

    with tempfile.TemporaryDirectory(prefix="phoxia-devkit-") as temporary:
        staged = Path(temporary) / target.name
        copy_project_surfaces(target, staged)
        staged_args = argparse.Namespace(**vars(args))
        staged_args.path = str(staged)
        with contextlib.redirect_stdout(io.StringIO()):
            project_init(staged_args)
        before, after = project_files(target), project_files(staged)
        changes = sorted(set(before) | set(after), key=lambda path: path.as_posix())
        changes = [path for path in changes if before.get(path) != after.get(path)]
        safe_add_updates = {Path("AGENTS.md"), Path("CLAUDE.md"), Path(".gitignore")}
        overwritten = [path for path in changes if path in before and path not in safe_add_updates]
        if args.mode == "add" and overwritten:
            raise DevKitError(
                "add mode would overwrite existing configuration: "
                + ", ".join(path.as_posix() for path in overwritten)
                + "; use --mode replace after reviewing the preview"
            )
        for path in changes:
            action = "CREATE" if path not in before else "DELETE" if path not in after else "UPDATE"
            print(f"{action} {path.as_posix()}")
        if not changes:
            print("No changes.")
            return
        if args.dry_run:
            return
        if not args.yes:
            if not sys.stdin.isatty():
                raise DevKitError("refusing to modify a non-interactive repository without --yes")
            if input("Apply these changes? [y/N]: ").strip().lower() not in {"y", "yes"}:
                print("Cancelled.")
                return

        existing = [path for path in changes if path in before]
        if existing:
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
            backup = target / ".phoxia" / "backups" / stamp
            for relative in existing:
                destination = backup / relative
                ensure_dir(destination.parent)
                destination.write_bytes(before[relative])
            print(f"BACKUP {backup.relative_to(target).as_posix()}/")

        for relative in changes:
            destination = target / relative
            source = staged / relative
            if relative not in after:
                destination.unlink(missing_ok=True)
                continue
            ensure_dir(destination.parent)
            temp = destination.with_name(destination.name + ".tmp")
            temp.write_bytes(after[relative])
            temp.replace(destination)
        print(f"Configured {target} in {args.mode} mode.")


def workspace_init(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    ensure_dir(root)
    targets = csv_values(args.targets, TARGETS, "target")
    layer_map = available_layers()
    layers = layer_values(args.layer, layer_map)
    validate_layer_project(root.name, layers, layer_map)
    if "claude" in targets:
        managed_merge(root / "CLAUDE.md", project_block(args.profile, "claude", layers))
    if "codex" in targets:
        managed_merge(root / "AGENTS.md", project_block(args.profile, "codex", layers))
    ensure_dir(root / ".phoxia")
    atomic_write(
        root / ".phoxia" / "workspace.yaml",
        f"apiVersion: {CURRENT_API_VERSION}\nkind: Workspace\nprofile: {yaml_quote(args.profile)}\nlayers: {json.dumps(layers)}\nrecursive: {str(bool(args.recursive)).lower()}\n",
    )

    repositories: list[Path] = []
    if args.recursive:
        for git in root.rglob(".git"):
            if git.is_dir():
                repositories.append(git.parent)
    for repository in sorted(set(repositories)):
        nested = argparse.Namespace(**vars(args))
        nested.path = str(repository)
        project_init(nested)
    print(f"Workspace configured: {root}. Repositories configured: {len(set(repositories))}.")


def status(args: argparse.Namespace) -> None:
    home = Path(args.home).expanduser().resolve() if args.home else Path.home()
    state = home / ".phoxia-devkit" / "state.json"
    if not state.exists():
        print("Phoxia DevKit is not installed for this home.")
        return
    print(state.read_text(encoding="utf-8"))


def generated_yaml_fields(path: Path) -> dict[tuple[str, ...], Any]:
    fields: dict[tuple[str, ...], Any] = {}
    stack: list[tuple[int, str]] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.match(r"^(\s*)([A-Za-z][A-Za-z0-9]*):(?:\s*(.*))$", line)
        if not match:
            continue
        indent, key, raw = len(match.group(1)), match.group(2), match.group(3)
        while stack and stack[-1][0] >= indent:
            stack.pop()
        field = tuple(item[1] for item in stack) + (key,)
        if raw:
            try:
                fields[field] = json.loads(raw)
            except json.JSONDecodeError:
                fields[field] = raw
        else:
            stack.append((indent, key))
    return fields


def manifest_api_version(path: Path) -> str:
    value = generated_yaml_fields(path).get(("apiVersion",))
    if not isinstance(value, str) or not value:
        raise DevKitError(f"Manifest {path} is missing apiVersion")
    if value != CURRENT_API_VERSION and value not in LEGACY_API_VERSIONS:
        raise DevKitError(f"Manifest {path} uses unsupported apiVersion {value!r}")
    return value


def upgrade_legacy_manifest(path: Path) -> bool:
    version = manifest_api_version(path)
    if version == CURRENT_API_VERSION:
        return False
    text = path.read_text(encoding="utf-8")
    updated, count = re.subn(
        rf"^apiVersion:\s*{re.escape(version)}\s*$",
        f"apiVersion: {CURRENT_API_VERSION}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise DevKitError(f"Manifest {path} has an invalid apiVersion declaration")
    atomic_write(path, updated)
    return True


def workspace_sync(args: argparse.Namespace) -> None:
    root = Path(args.path).expanduser().resolve()
    manifest = root / ".phoxia" / "workspace.yaml"
    if not manifest.is_file():
        raise DevKitError(f"Workspace manifest not found: {manifest}")
    upgrade_legacy_manifest(manifest)
    fields = generated_yaml_fields(manifest)
    if fields.get(("kind",)) != "Workspace":
        raise DevKitError(f"Manifest {manifest} is not a Workspace")
    print(f"Workspace synchronized: {root}.")


def skill_trees_equal(left: Path, right: Path) -> bool:
    def files(root: Path) -> dict[Path, bytes] | None:
        result: dict[Path, bytes] = {}
        for path in root.rglob("*"):
            if path.is_symlink():
                return None
            if path.is_file():
                result[path.relative_to(root)] = path.read_bytes()
        return result

    return left.is_dir() and right.is_dir() and files(left) == files(right)


def project_sync(args: argparse.Namespace) -> None:
    path = Path(args.path).expanduser().resolve()
    home = Path(args.home).expanduser().resolve() if args.home else Path.home()
    manifest = path / ".phoxia" / "project.yaml"
    if not manifest.is_file():
        raise DevKitError(f"Project manifest not found: {manifest}")
    upgrade_legacy_manifest(manifest)
    fields = generated_yaml_fields(manifest)
    profile = fields.get(("metadata", "profile"))
    targets = fields.get(("targets",), [])
    layers = fields.get(("layers",), [])
    if profile not in available_profiles():
        raise DevKitError(f"Project profile is unavailable: {profile!r}")
    if not isinstance(targets, list) or any(target not in TARGETS for target in targets):
        raise DevKitError(f"Project targets are invalid: {targets!r}")
    if not isinstance(layers, list) or any(layer not in available_layers() for layer in layers):
        raise DevKitError(f"Project layers are invalid: {layers!r}")
    validate_layer_project(str(fields.get(("metadata", "name"), path.name)), layers, available_layers())

    if "claude" in targets:
        managed_merge(path / "CLAUDE.md", project_block(str(profile), "claude", layers, fields))
    if "codex" in targets:
        managed_merge(path / "AGENTS.md", project_block(str(profile), "codex", layers, fields))

    conflicts: list[str] = []
    local_roots = {"claude": path / ".claude" / "skills", "codex": path / ".agents" / "skills"}
    for _, name in skill_sources(str(profile), layers):
        for target in targets:
            local = local_roots[target] / name
            global_path = global_skill_path(home, target, name)
            if not local.is_dir() or not global_path.is_dir():
                continue
            if skill_trees_equal(local, global_path):
                shutil.rmtree(local)
                print(f"Pruned redundant local {target} skill: {name}")
            else:
                conflicts.append(f"local {target} skill {name} conflicts with global {name}")
    if conflicts:
        print("\n".join(conflicts))
        raise SystemExit(1)
    print(f"Project synchronized: {path}.")


def project_health(path: Path, home: Path) -> tuple[list[str], list[str]]:
    errors: list[str] = []
    warnings: list[str] = []
    manifest = path / ".phoxia" / "project.yaml"
    if not manifest.is_file():
        return [f"{manifest} is missing"], warnings

    try:
        version = manifest_api_version(manifest)
    except DevKitError as exc:
        errors.append(str(exc))
    else:
        if version in LEGACY_API_VERSIONS:
            warnings.append(
                f"legacy manifest API version {version}; run phoxia-devkit project sync --path {path}"
            )

    fields = generated_yaml_fields(manifest)
    profile = fields.get(("metadata", "profile"))
    targets = fields.get(("targets",), [])
    layers = fields.get(("layers",), [])
    if profile not in available_profiles():
        errors.append(f"project profile is unavailable: {profile!r}")
    if not isinstance(targets, list) or any(target not in TARGETS for target in targets):
        errors.append(f"project targets are invalid: {targets!r}")
        targets = []
    layer_map = available_layers()
    if not isinstance(layers, list) or any(layer not in layer_map for layer in layers):
        errors.append(f"project layers are invalid: {layers!r}")
        layers = []
    else:
        try:
            validate_layer_project(str(fields.get(("metadata", "name"), path.name)), layers, layer_map)
        except DevKitError as exc:
            errors.append(str(exc))

    instruction_files = {"claude": "CLAUDE.md", "codex": "AGENTS.md"}
    for target in targets:
        instruction = path / instruction_files[target]
        text = instruction.read_text(encoding="utf-8") if instruction.is_file() else ""
        expected = f"{START}\n{project_block(str(profile), target, list(layers), fields).rstrip()}\n{END}"
        if START not in text or END not in text:
            errors.append(f"{instruction.name} is missing the managed DevKit block")
        elif expected not in text:
            errors.append(f"{instruction.name} managed DevKit block is stale")

    required_fields = [
        ("governance", "technicalMaintainer"),
        ("governance", "pullRequestApprover"),
        ("governance", "commercialAuthority"),
        ("documentation", "visibility"),
    ]
    for field in required_fields:
        if not fields.get(field):
            errors.append(f"project manifest is missing {'.'.join(field)}")

    if profile == "specialist":
        licensing = path / ".phoxia" / "licensing.yaml"
        if not licensing.is_file():
            errors.append("specialist project is missing .phoxia/licensing.yaml")
        else:
            licensing_fields = generated_yaml_fields(licensing)
            company = licensing_fields.get(("company",), "")
            expression = licensing_fields.get(("spdxExpression",))
            expected = f"LicenseRef-{spdx_owner(str(company))}-Proprietary"
            if expression != expected:
                errors.append(f"licensing SPDX expression must be {expected!r}")

    if profile in available_profiles():
        labels = {"claude": "Claude", "codex": "Codex"}
        local_roots = {"claude": path / ".claude" / "skills", "codex": path / ".agents" / "skills"}
        for _, name in skill_sources(str(profile), list(layers)):
            for target in targets:
                global_path = global_skill_path(home, target, name)
                local_path = local_roots[target] / name
                if global_path.is_dir() and local_path.is_dir():
                    if skill_trees_equal(local_path, global_path):
                        warnings.append(f"redundant local {labels[target]} skill {name}")
                    else:
                        errors.append(f"local {labels[target]} skill {name} conflicts with its global skill")
                elif not global_path.is_dir() and not local_path.is_dir():
                    errors.append(f"{labels[target]} skill {name} is unavailable globally and locally")
    return errors, warnings


def doctor(args: argparse.Namespace) -> None:
    errors: list[str] = []
    profiles = available_profiles()
    if not profiles:
        errors.append("No profile manifests were found")
    for name, data in profiles.items():
        root = Path(data["path"])
        if not (root / "CLAUDE.md").exists():
            errors.append(f"Profile {name} is missing CLAUDE.md")
        for plugin in data.get("claudePlugins", []):
            try:
                resolve_component(str(plugin), Path(data["sourceRoot"]))
            except DevKitError:
                errors.append(f"Profile {name} references missing plugin {plugin}")
    managed_skills: dict[Path, str] = {}
    for data in profiles.values():
        for item in data.get("skills", []):
            try:
                source = resolve_component(str(item["path"]), Path(data["sourceRoot"]))
            except DevKitError:
                source = Path(data["sourceRoot"]) / str(item["path"])
            managed_skills[source] = str(item["name"])
    for data in available_layers().values():
        root = Path(data["path"])
        for item in data.get("skills", []):
            managed_skills[root / str(item["path"])] = str(item["name"])
    for skill_root in sorted(managed_skills):
        skill = skill_root / "SKILL.md"
        if not skill.is_file():
            errors.append(f"Managed skill is missing SKILL.md: {skill_root}")
            continue
        metadata, _ = frontmatter(skill.read_text(encoding="utf-8"))
        if not metadata.get("name") or not metadata.get("description"):
            errors.append(f"Invalid skill metadata: {skill}")
        elif metadata["name"] != skill.parent.name:
            errors.append(f"Skill name does not match directory: {skill}")
    for name, data in available_layers().items():
        root = Path(data["path"])
        if not (root / str(data.get("instructionFile", "AGENTS.addition.md"))).exists():
            errors.append(f"Layer {name} is missing its instruction file")
    warnings: list[str] = []
    if getattr(args, "path", None):
        project_errors, warnings = project_health(
            Path(args.path).expanduser().resolve(),
            Path(args.home).expanduser().resolve() if args.home else Path.home(),
        )
        errors.extend(project_errors)
    for warning in warnings:
        print(f"warning: {warning}")
    if errors:
        print("\n".join(errors))
        raise SystemExit(1)
    metadata = package_metadata()
    identity = f"{metadata.get('package', PACKAGE_ROOT.name)} {metadata.get('version', 'unknown')}"
    print(
        f"Doctor passed: {identity}; profiles={', '.join(profiles)}; "
        f"targets=claude,codex; optional-layers={', '.join(available_layers()) or 'none'}."
    )
def uninstall(args: argparse.Namespace) -> None:
    home = Path(args.home).expanduser().resolve() if args.home else Path.home()
    base = home / ".phoxia-devkit"
    state_path = base / "state.json"
    state: dict[str, Any] = {}
    if state_path.exists():
        try:
            state = read_json(state_path)
        except DevKitError:
            state = {}
    for raw in state.get("managedFiles", []):
        path = Path(str(raw))
        if path.is_file() or path.is_symlink():
            path.unlink(missing_ok=True)
    for raw in sorted(state.get("managedDirs", []), key=lambda value: len(str(value)), reverse=True):
        path = Path(str(raw))
        if path == base:
            continue
        if path.is_dir():
            shutil.rmtree(path)
    if base.exists():
        shutil.rmtree(base)
    print("Removed only the files recorded as managed by Phoxia DevKit. Existing ~/.claude and ~/.codex were not changed.")


def restore_backup(args: argparse.Namespace) -> None:
    home = Path(args.home).expanduser().resolve() if args.home else Path.home()
    backup = Path(args.backup).expanduser().resolve()
    if not backup.is_file():
        raise DevKitError(f"Backup not found: {backup}")
    if not args.yes:
        phrase = "RESTORE PHOXIA BACKUP"
        if not sys.stdin.isatty():
            raise DevKitError("Restore requires --yes in a non-interactive shell")
        confirmation = input(f"Type {phrase} to replace current configuration: ").strip()
        if confirmation != phrase:
            raise DevKitError("Restore cancelled")
    safety_backup = create_authoritative_backup(home, "before-restore")
    for path in backup_candidates(home):
        remove_path(path)
    with tarfile.open(backup, "r:gz") as archive:
        safe_extract(archive, home)
    print(f"Restored backup: {backup}")
    print(f"Safety backup of the replaced state: {safety_backup}")


def add_project_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--path", default=".")
    parser.add_argument("--profile", choices=list(available_profiles()), default=next(iter(available_profiles()), None))
    parser.add_argument("--targets", default="all")
    parser.add_argument("--layer", action="append")
    parser.add_argument("--owner")
    parser.add_argument("--description")
    parser.add_argument("--company")
    parser.add_argument("--visibility")
    parser.add_argument("--license-model")
    parser.add_argument("--commercial-use")
    parser.add_argument("--redistribution")
    parser.add_argument("--technical-maintainer")
    parser.add_argument("--pull-request-approver")
    parser.add_argument("--commercial-authority")
    parser.add_argument("--documentation-visibility")
    parser.add_argument("--vendor-skills", action="store_true")


def add_install_args(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--targets", default="all")
    parser.add_argument("--profiles", default="all")
    parser.add_argument("--enable-layer", action="append")
    parser.add_argument("--home")
    parser.add_argument("--authoritative", action="store_true")
    parser.add_argument("--default-profile", choices=list(available_profiles()), default="personal")
    parser.add_argument("--default-layer", action="append")
    parser.add_argument("--external-plugins", choices=["curated", "none"], default="curated")
    parser.add_argument("--skip-plugin-install", action="store_true")
    parser.add_argument("--strict-plugins", action="store_true")
    parser.add_argument("--yes", action="store_true")
    hints = parser.add_mutually_exclusive_group()
    hints.add_argument("--startup-hints", dest="startup_hints", action="store_true")
    hints.add_argument("--no-startup-hints", dest="startup_hints", action="store_false")
    parser.set_defaults(startup_hints=None)
    parser.add_argument("--locale")


def update(args: argparse.Namespace) -> None:
    if PACKAGE_ROOT == (Path(args.home).expanduser().resolve() if args.home else Path.home()) / ".phoxia-devkit" / "package":
        raise DevKitError("Run update from a newer DevKit source package; an installed package cannot update itself")
    install(args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="phoxia-devkit", description="Phoxia DevKit manager for Claude Code and Codex.")
    sub = parser.add_subparsers(dest="command", required=True)

    init_parser = sub.add_parser("init", help="configure the current repository")
    add_project_args(init_parser)
    init_parser.add_argument("--mode", choices=["add", "update", "replace"], default="add")
    init_parser.add_argument("--yes", action="store_true", help="apply the preview without prompting")
    init_parser.add_argument("--dry-run", action="store_true", help="print the impact without writing")
    init_parser.set_defaults(func=project_init_transaction)

    install_parser = sub.add_parser("install")
    add_install_args(install_parser)
    install_parser.set_defaults(func=install)

    update_parser = sub.add_parser("update")
    add_install_args(update_parser)
    update_parser.set_defaults(func=update)

    status_parser = sub.add_parser("status")
    status_parser.add_argument("--home")
    status_parser.set_defaults(func=status)

    doctor_parser = sub.add_parser("doctor")
    doctor_parser.add_argument("--home")
    doctor_parser.set_defaults(func=doctor)

    uninstall_parser = sub.add_parser("uninstall")
    uninstall_parser.add_argument("--home")
    uninstall_parser.set_defaults(func=uninstall)

    restore_parser = sub.add_parser("restore")
    restore_parser.add_argument("--backup", required=True)
    restore_parser.add_argument("--home")
    restore_parser.add_argument("--yes", action="store_true")
    restore_parser.set_defaults(func=restore_backup)
    return parser


def main() -> None:
    try:
        arguments = build_parser().parse_args(preprocess_aliases(sys.argv[1:]))
        arguments.func(arguments)
    except DevKitError as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(2) from exc


if __name__ == "__main__":
    main()
