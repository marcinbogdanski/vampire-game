# Architecture

Dark-fantasy vampire visual novel with turn-based RPG combat. All visuals generated at runtime via local AI.

## Subsystems

Four runtime concerns, three Python packages, two processes (plus the browser).

1. **Game engine** — pure logic: world state, combat, NPCs, heat, save/load. No I/O, no network.
2. **Asset generation** — translates engine JSON specs into prompts + ComfyUI workflows; manages cache and job state.
3. **App / server** — FastAPI; imports engine + assetgen; serves frontend; HTTP + WebSocket.
4. **ComfyUI** — external process, separate install. Treated as a remote service over HTTP/WS.

```
[Browser / Pywebview] --HTTP/WS--> [FastAPI app] --calls--> [engine]
                                          \--calls--> [assetgen] --HTTP/WS--> [ComfyUI]
```

## Tech stack

- **Python 3.12+**, managed by **uv** (lockfile, venv, Python versions).
- **FastAPI** for the app server. Async, native WebSockets, Pydantic schemas.
- **Plain HTML/CSS/JS** for frontend (Vite/React optional later). 16:9 letterboxed stage; everything positioned relative to a `#stage` container.
- **Dev:** Flask-style — run FastAPI, open in a browser. Real devtools.
- **Ship:** wrap with **Pywebview** (one window pointing at localhost). Future upgrade path to Electron/Tauri if needed — preserved by keeping all Python↔frontend traffic over HTTP/WS, no JS bridge.
- **Packaging:** PyInstaller bundles app + engine + assetgen into one binary. ComfyUI ships/installs separately.

## Layout

```
vampire-game/
  pyproject.toml
  vengine/          # pure game logic
  vassetgen/        # asset specs, prompts, ComfyUI client, workflows/*.json
  app/              # FastAPI server, static frontend, templates
  docs/
```

## Boundary rules

- `vengine` imports nothing from `vassetgen` or `app`.
- `vassetgen` imports nothing from `vengine` or `app`.
- `app` is the only coordinator; it imports both libraries.
- All cross-package data is JSON (Pydantic models at the boundary). No shared mutable state.
- ComfyUI workflows live with `vassetgen` (they are assetgen's data).
- Frontend talks to backend only via HTTP/WS — no Pywebview `js_api`.

A dedicated 5th "orchestrator" package is deferred. `app/` plays that role until orchestration grows real complexity (queues, dependency graphs, batching).

## Alternatives considered and rejected

**Frontend / UI shell**
- *Ren'Py* — purpose-built for VNs, free dialogue/saves/transitions, easiest distribution. Rejected: combat + crafting + dynamic AI-asset injection fight the framework; engine/frontend separation gets muddled.
- *Pygame CE* — pure Python, simplest possible loop. Rejected: every menu, button, dialogue box hand-rolled; UI is the bulk of this game and HTML/CSS does it 10× faster.
- *PySide6 / Qt + QML* — strongest native Python option, great 2D/video. Rejected: heavier learning curve, larger bundle, QML is another language anyway. Defensible runner-up if Python-everywhere becomes a hard requirement.
- *Flet* — trendy, Flutter-based, single-language. Rejected: widget-tree model is shaped for dashboards, not full-bleed backgrounds with layered overlays and video.
- *NiceGUI / Streamlit / Gradio* — fast for tools. Rejected: dashboard-shaped abstractions; you'd drop to raw HTML anyway, and packaging to a single exe is awkward.
- *Electron / Tauri now* — best UI fidelity. Rejected for now: most moving parts, Node toolchain, signing/notarization headaches. Reserved as the upgrade target.
- *Eel* — Python↔JS bridge. Rejected: proprietary bridge doesn't port to Electron; defeats the upgrade path.
