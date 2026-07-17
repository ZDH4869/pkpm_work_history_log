from fastmcp import FastMCP
from pathlib import Path
import sys
import os
import json
import re
import unicodedata
from typing import Any, Dict, List, Optional, Tuple

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import *  # noqa: F403
from monitoring import monitor_mcp_tool

# 初始化 MCP 服务器
mcp = FastMCP("BIMBaseAI2PY_MCPServer")


# =========================
# Manifest / Retrieval Core
# =========================

_MANIFEST_CACHE: Optional[Dict[str, Any]] = None
_MANIFEST_CACHE_KEY: Optional[Tuple[bool]] = None  # (include_reference,)


def _normalize_text(s: str) -> str:
    """Normalize text for matching (case/width/punct/space)."""
    if s is None:
        return ""
    s = unicodedata.normalize("NFKC", str(s))
    s = s.lower()
    # Remove whitespace and common punctuation. Keep CJK characters.
    s = re.sub(r"[\s\-_./\\:;，。？！!?,()\[\]{}<>\"'`~@#$%^&*+=|]+", "", s)
    return s


def _safe_resolve_skill_path(rel_path: str) -> Path:
    """Resolve a skill relative path and enforce sandbox under SKILL_ROOT."""
    base = SKILL_ROOT.resolve()  # noqa: F405
    full = (SKILL_ROOT / rel_path).resolve()  # noqa: F405
    try:
        full.relative_to(base)
    except ValueError:
        raise ValueError("非法的文件路径访问。")
    if full.is_symlink() or any(p.is_symlink() for p in full.parents if str(p).startswith(str(base))):
        raise ValueError("不允许通过符号链接访问。")
    return full


def _parse_frontmatter(md_text: str) -> Tuple[Dict[str, str], str]:
    """
    Parse a minimal YAML-like frontmatter block:
    ---
    key: value
    ---
    Returns: (frontmatter_dict, remaining_markdown)
    """
    if not md_text.startswith("---"):
        return {}, md_text

    lines = md_text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, md_text

    fm: Dict[str, str] = {}
    end_idx = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            end_idx = i
            break
        line = lines[i].strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        k, v = line.split(":", 1)
        k = k.strip()
        v = v.strip().strip('"').strip("'")
        if k:
            fm[k] = v

    if end_idx is None:
        return {}, md_text

    remaining = "\n".join(lines[end_idx + 1 :]).lstrip("\n")
    return fm, remaining


def _infer_symbol_from_relpath(rel_path: str) -> str:
    """
    Infer a canonical symbol from the file name / folder conventions.
    This is intentionally deterministic to reduce ambiguity for Agents.
    """
    stem = Path(rel_path).stem  # e.g. geometry_Cube

    # Strong conventions
    if stem.startswith("geometry_"):
        return stem[len("geometry_") :]
    if stem.startswith("property_"):
        return stem[len("property_") :]

    # Interface docs
    if stem == "matrix_interface":
        # Keep snake id because Agents often refer to it by file name.
        return "matrix_interface"

    # snake_case -> PascalCase for other interfaces
    if stem.endswith("_interface"):
        parts = stem.split("_")
        return "".join(p[:1].upper() + p[1:] for p in parts)

    # Other docs (keep stem)
    return stem


def _infer_category(rel_path: str) -> str:
    p = rel_path.replace("\\", "/")
    if "/02_coding_standards_safety/" in p:
        return "safety"
    if "/03_professional_patterns/" in p:
        return "pattern"
    if "/01_sdk_interface_guide/test/" in p:
        return "reference"
    if "/01_sdk_interface_guide/geometric_interface/" in p:
        return "geometry"
    if "/01_sdk_interface_guide/" in p and p.endswith("_interface.md"):
        return "interface"
    if "/01_sdk_interface_guide/" in p:
        return "interface"
    return "misc"


def _load_manifest_overrides() -> Dict[str, Any]:
    try:
        p = SKILL_MANIFEST_OVERRIDES  # noqa: F405
        if not p.exists():
            return {}
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return {}


def _scan_skill_docs(include_reference: bool) -> List[Dict[str, Any]]:
    """
    Scan SKILL_ROOT for markdown docs and build base entries.
    Default behavior excludes:
    - summary_skill.md
    - test/* reference docs (unless include_reference=True)
    """
    base = SKILL_ROOT  # noqa: F405
    docs: List[Dict[str, Any]] = []

    for path in base.rglob("*.md"):
        rel = path.relative_to(base).as_posix()

        if rel == "summary_skill.md":
            continue
        if (not include_reference) and rel.startswith("01_sdk_interface_guide/test/"):
            continue

        try:
            text = path.read_text(encoding="utf-8")
        except Exception:
            continue

        fm, _ = _parse_frontmatter(text)
        symbol = _infer_symbol_from_relpath(rel)
        category = _infer_category(rel)

        entry: Dict[str, Any] = {
            "symbol": symbol,
            "path": rel,
            "category": category,
            "name": fm.get("name", ""),
            "description": fm.get("description", ""),
            "doc_type": fm.get("doc_type", ""),
            "version": fm.get("version", ""),
            "author": fm.get("author", ""),
            "aliases": [],
            "keywords": [],
            "related": [],
            "must_load_with": [],
            "priority": 0.5,
        }
        docs.append(entry)

    return docs


def _apply_overrides(entries: List[Dict[str, Any]], overrides: Dict[str, Any]) -> List[Dict[str, Any]]:
    if not overrides:
        return entries

    by_path = {e["path"]: e for e in entries if "path" in e}

    for sym, ov in overrides.items():
        target = None
        # Primary: symbol match
        for e in entries:
            if _normalize_text(e.get("symbol", "")) == _normalize_text(sym):
                target = e
                break
        # Secondary: path match
        if target is None and isinstance(ov, dict) and ov.get("path") in by_path:
            target = by_path[ov["path"]]

        if target is None:
            # Allow overrides to introduce a virtual entry if the doc exists.
            if isinstance(ov, dict) and ov.get("path"):
                try:
                    _safe_resolve_skill_path(ov["path"])
                except Exception:
                    continue
                target = {
                    "symbol": sym,
                    "path": ov["path"],
                    "category": ov.get("category", "misc"),
                    "name": "",
                    "description": ov.get("description", ""),
                    "doc_type": "",
                    "version": "",
                    "author": "",
                    "aliases": [],
                    "keywords": [],
                    "related": [],
                    "must_load_with": [],
                    "priority": 0.5,
                }
                entries.append(target)

        # Merge override fields
        if isinstance(ov, dict) and target is not None:
            for k in ["path", "category", "description", "doc_type", "version", "author"]:
                if k in ov and ov[k]:
                    target[k] = ov[k]
            for k in ["aliases", "keywords", "related", "must_load_with"]:
                if k in ov and isinstance(ov[k], list):
                    target[k] = ov[k]
            if "priority" in ov:
                try:
                    target["priority"] = float(ov["priority"])
                except Exception:
                    pass

            target["symbol"] = sym

    return entries


def _build_manifest(include_reference: bool) -> Dict[str, Any]:
    entries = _scan_skill_docs(include_reference=include_reference)
    overrides = _load_manifest_overrides()
    entries = _apply_overrides(entries, overrides)

    best: Dict[str, Dict[str, Any]] = {}
    for e in entries:
        key = _normalize_text(e.get("symbol", ""))
        if not key:
            continue
        existing = best.get(key)
        if existing is None:
            best[key] = e
            continue
        score_existing = float(existing.get("priority", 0.5)) + (0.1 if existing.get("description") else 0)
        score_new = float(e.get("priority", 0.5)) + (0.1 if e.get("description") else 0)
        if score_new > score_existing:
            best[key] = e

    skills = list(best.values())

    for e in skills:
        if e.get("symbol") == "basic_writing_style":
            continue
        category = e.get("category", "")
        must_load_with = list(e.get("must_load_with", []) or [])
        if category in {"geometry", "interface", "pattern"} and "basic_writing_style" not in must_load_with:
            must_load_with.append("basic_writing_style")
        e["must_load_with"] = must_load_with

    skills.sort(key=lambda x: (-float(x.get("priority", 0.5)), x.get("symbol", "")))

    return {
        "version": "1.0",
        "include_reference": include_reference,
        "skill_root": str(SKILL_ROOT),  # noqa: F405
        "count": len(skills),
        "skills": skills,
    }


def _get_manifest(include_reference: bool, force_refresh: bool = False) -> Dict[str, Any]:
    global _MANIFEST_CACHE, _MANIFEST_CACHE_KEY
    key = (include_reference,)
    if force_refresh or _MANIFEST_CACHE is None or _MANIFEST_CACHE_KEY != key:
        _MANIFEST_CACHE = _build_manifest(include_reference=include_reference)
        _MANIFEST_CACHE_KEY = key
    return _MANIFEST_CACHE


def _resolve_symbol(symbol_or_query: str, include_reference: bool) -> Optional[Dict[str, Any]]:
    manifest = _get_manifest(include_reference=include_reference, force_refresh=False)
    wanted = _normalize_text(symbol_or_query)
    for e in manifest["skills"]:
        if _normalize_text(e.get("symbol", "")) == wanted:
            return e
    return None


def _json_loads_safely(payload: Any) -> Dict[str, Any]:
    if not isinstance(payload, str):
        return {}
    try:
        data = json.loads(payload)
        return data if isinstance(data, dict) else {}
    except Exception:
        return {}


def _inspect_plain_error_string_result(args: Tuple[Any, ...], kwargs: Dict[str, Any], result: Any) -> Dict[str, Any]:
    if not isinstance(result, str):
        return {}

    error_prefixes = ("错误：", "读取文件时发生错误:")
    for prefix in error_prefixes:
        if result.startswith(prefix):
            return {
                "status": "error",
                "error_type": "BusinessError",
                "error_message": result,
            }
    return {}


def _inspect_json_error_payload_result(args: Tuple[Any, ...], kwargs: Dict[str, Any], result: Any) -> Dict[str, Any]:
    payload = _json_loads_safely(result)
    error_message = payload.get("error", "")
    if isinstance(error_message, str) and error_message:
        return {
            "status": "error",
            "error_type": "BusinessError",
            "error_message": error_message,
        }
    return {}


def _extract_agent_input_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    parameter_position: Optional[int],
) -> Dict[str, Any]:
    agent_input = _arg_or_kwarg(args, kwargs, "agent_input", parameter_position, "")
    if not isinstance(agent_input, str):
        return {"agent_input_present": False}

    normalized = agent_input.strip()
    if not normalized:
        return {"agent_input_present": False}

    return {
        "agent_input_present": True,
        "agent_input_size": len(agent_input),
        "agent_input_summary": normalized,
    }


def _merge_monitor_metadata(*items: Dict[str, Any]) -> Dict[str, Any]:
    merged: Dict[str, Any] = {}
    for item in items:
        if isinstance(item, dict):
            merged.update(item)
    return merged


def _arg_or_kwarg(args: Tuple[Any, ...], kwargs: Dict[str, Any], name: str, position: int, default: Any = None) -> Any:
    if name in kwargs:
        return kwargs[name]
    if len(args) > position:
        return args[position]
    return default


def _build_skill_record(
    symbol: str,
    include_reference: bool,
    source: str,
    path: str = "",
    category: str = "",
) -> Dict[str, Any]:
    record = {
        "symbol": symbol or "",
        "path": path or "",
        "source": source,
    }
    if category:
        record["category"] = category

    if record["path"] and category:
        return record

    entry = _resolve_symbol(symbol, include_reference=bool(include_reference))
    if entry is not None:
        record["path"] = record["path"] or entry.get("path", "")
        if entry.get("category", ""):
            record["category"] = entry.get("category", "")
    return record


def _extract_get_skill_doc_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    symbol = _arg_or_kwarg(args, kwargs, "symbol", 0, "")
    include_reference = bool(_arg_or_kwarg(args, kwargs, "include_reference", 1, False))
    requested = [symbol] if symbol else []
    metadata: Dict[str, Any] = _merge_monitor_metadata(
        {"requested_skills": requested},
        _extract_agent_input_monitor_fields(args, kwargs, 2),
    )

    if error is not None:
        return metadata

    payload = _json_loads_safely(result)
    if not payload:
        return metadata

    if payload.get("error"):
        metadata["missing_skills"] = requested
        return metadata

    resolved_symbol = payload.get("symbol", symbol)
    metadata["resolved_skills"] = [
        _build_skill_record(
            symbol=resolved_symbol,
            path=payload.get("path", ""),
            category="",
            include_reference=include_reference,
            source="resolved",
        )
    ]
    return metadata


def _extract_get_skill_bundle_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    symbols = _arg_or_kwarg(args, kwargs, "symbols", 0, []) or []
    include_reference = bool(_arg_or_kwarg(args, kwargs, "include_reference", 1, False))
    normalized_requested = {_normalize_text(s): s for s in symbols if s}
    metadata: Dict[str, Any] = _merge_monitor_metadata(
        {"requested_skills": list(normalized_requested.values())},
        _extract_agent_input_monitor_fields(args, kwargs, 3),
    )

    if error is not None:
        return metadata

    payload = _json_loads_safely(result)
    if not payload:
        return metadata

    resolved_skills = []
    for doc in payload.get("docs", []) or []:
        if not isinstance(doc, dict):
            continue
        symbol = doc.get("symbol", "")
        source = "explicit" if _normalize_text(symbol) in normalized_requested else "dependency"
        resolved_skills.append(
            _build_skill_record(
                symbol=symbol,
                path=doc.get("path", ""),
                category="",
                include_reference=include_reference,
                source=source,
            )
        )

    if resolved_skills:
        metadata["resolved_skills"] = resolved_skills

    missing_skills = []
    for item in payload.get("missing", []) or []:
        if isinstance(item, dict):
            missing_symbol = item.get("symbol") or item.get("query") or ""
        else:
            missing_symbol = str(item)
        if missing_symbol:
            missing_skills.append(missing_symbol)

    if missing_skills:
        metadata["missing_skills"] = missing_skills

    return metadata


def _extract_get_skill_content_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    file_path = _arg_or_kwarg(args, kwargs, "file_path", 0, "")
    metadata: Dict[str, Any] = _merge_monitor_metadata(
        {"requested_paths": [file_path] if file_path else []},
        _extract_agent_input_monitor_fields(args, kwargs, 1),
    )

    if error is not None:
        return metadata

    if isinstance(result, str) and not result.startswith("错误：") and not result.startswith("读取文件时发生错误:"):
        metadata["resolved_paths"] = [file_path] if file_path else []

    return metadata


def _extract_get_skill_manifest_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    return _extract_agent_input_monitor_fields(args, kwargs, 2)


def _extract_get_related_skills_monitor_fields(
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    symbol = _arg_or_kwarg(args, kwargs, "symbol", 0, "")
    return _merge_monitor_metadata(
        {"requested_skills": [symbol] if symbol else []},
        _extract_agent_input_monitor_fields(args, kwargs, 2),
    )



# 定义一个工具 (Tool)
@mcp.tool()
@monitor_mcp_tool()
def get_summary_document() -> str:
    """
    获取AI生成python模型脚本的概要文档,第一次场景生成python模型脚本时，一定要调用，无需传入任何参数。
    返回:
    str: Markdown 文件的完整内容。
    """
    DOC_PATH = SKILL_ROOT / "summary_skill.md"
    return DOC_PATH.read_text(encoding='utf-8')


# =========================
# New Retrieval Tools
# =========================

@mcp.tool()
@monitor_mcp_tool(detail_extractor=_extract_get_skill_manifest_monitor_fields)
def get_skill_manifest(include_reference: bool = False, force_refresh: bool = False, agent_input: str = "") -> str:
    """
    获取技能文档结构化索引（用于稳定检索）。

    参数:
      include_reference: 是否包含 test/ 下的参考笔记（默认 False，避免污染检索）
      force_refresh: 是否强制刷新缓存（默认 False）
      agent_input: Agent 调用该工具时的原始意图或上下文摘要（可选）
    返回:
      str: JSON 字符串
    """
    manifest = _get_manifest(include_reference=bool(include_reference), force_refresh=bool(force_refresh))
    return json.dumps(manifest, ensure_ascii=False)


@mcp.tool()
@monitor_mcp_tool(
    detail_extractor=_extract_get_skill_doc_monitor_fields,
    result_inspector=_inspect_json_error_payload_result,
)
def get_skill_doc(symbol: str, include_reference: bool = False, agent_input: str = "") -> str:
    """
    按标准 symbol 获取技能文档正文。

    参数:
      symbol: 标准函数名（例如 Cube / Sweep / Bool / matrix_interface）
      include_reference: 是否包含 test/（通常不需要）
      agent_input: Agent 调用该工具时的原始意图或上下文摘要（可选）
    返回:
      str: JSON 字符串，包含 symbol/path/content
    """
    entry = _resolve_symbol(symbol, include_reference=bool(include_reference))
    if entry is None:
        return json.dumps({"error": f"未找到符号 '{symbol}'，请优先调用 get_skill_manifest() 浏览所有可用的标准 symbol，不要猜测函数名。"}, ensure_ascii=False)

    try:
        full_path = _safe_resolve_skill_path(entry["path"])
        content = full_path.read_text(encoding="utf-8")
        return json.dumps(
            {"symbol": entry.get("symbol", ""), "path": entry.get("path", ""), "content": content},
            ensure_ascii=False,
        )
    except Exception as e:
        return json.dumps({"error": f"读取文档失败: {str(e)}", "symbol": symbol}, ensure_ascii=False)


@mcp.tool()
@monitor_mcp_tool(
    detail_extractor=_extract_get_related_skills_monitor_fields,
    result_inspector=_inspect_json_error_payload_result,
)
def get_related_skills(symbol: str, include_reference: bool = False, agent_input: str = "") -> str:
    """
    返回某个 symbol 的常见配套函数（基于 manifest.related）。

    参数:
      symbol: 标准函数名
      include_reference: 是否包含 test/（通常不需要）
      agent_input: Agent 调用该工具时的原始意图或上下文摘要（可选）
    返回:
      str: JSON 字符串
    """
    entry = _resolve_symbol(symbol, include_reference=bool(include_reference))
    if entry is None:
        return json.dumps({"error": "symbol 未找到，建议先调用 get_skill_manifest", "symbol": symbol}, ensure_ascii=False)

    manifest = _get_manifest(include_reference=bool(include_reference), force_refresh=False)
    by_sym = { _normalize_text(e.get("symbol","")): e for e in manifest["skills"] }

    related = []
    for r in entry.get("related", []) or []:
        r_entry = by_sym.get(_normalize_text(r))
        related.append({
            "symbol": r_entry.get("symbol", r) if r_entry else r,
            "path": r_entry.get("path", "") if r_entry else "",
            "category": r_entry.get("category", "") if r_entry else "",
            "description": (r_entry.get("description", "") or r_entry.get("name", "")) if r_entry else "",
        })

    result = {
        "symbol": entry.get("symbol", ""),
        "path": entry.get("path", ""),
        "related": related,
        "must_load_with": entry.get("must_load_with", []) or [],
    }
    return json.dumps(result, ensure_ascii=False)


@mcp.tool()
@monitor_mcp_tool(
    detail_extractor=_extract_get_skill_bundle_monitor_fields,
    result_inspector=_inspect_json_error_payload_result,
)
def get_skill_bundle(
    symbols: List[str],
    include_reference: bool = False,
    include_dependencies: bool = True,
    agent_input: str = "",
) -> str:
    """
    批量获取多个 symbol 的文档正文（减少多次工具调用）。

    参数:
      symbols: 标准函数名列表
      include_reference: 是否包含 test/（通常不需要）
      include_dependencies: 是否自动附带 must_load_with 依赖文档（默认 True）
      agent_input: Agent 调用该工具时的原始意图或上下文摘要（可选）
    返回:
      str: JSON 字符串
    """
    requested = []
    seen = set()

    def enqueue(sym: str):
        key = _normalize_text(sym)
        if not key or key in seen:
            return
        seen.add(key)
        requested.append(sym)

    for s in symbols or []:
        enqueue(s)

    if include_dependencies:
        for s in list(requested):
            entry = _resolve_symbol(s, include_reference=bool(include_reference))
            if entry is None:
                continue
            for dep in entry.get("must_load_with", []) or []:
                enqueue(dep)

    docs = []
    missing = []
    for s in requested:
        entry = _resolve_symbol(s, include_reference=bool(include_reference))
        if entry is None:
            missing.append({"query": s})
            continue
        try:
            full_path = _safe_resolve_skill_path(entry["path"])
            content = full_path.read_text(encoding="utf-8")
            docs.append({"symbol": entry.get("symbol", ""), "path": entry.get("path", ""), "content": content})
        except Exception as e:
            missing.append({"symbol": s, "error": str(e)})

    result = {"docs": docs, "missing": missing, "include_dependencies": bool(include_dependencies)}
    return json.dumps(result, ensure_ascii=False)

# =========================
# MCP Prompts
# =========================

@mcp.prompt()
def bimbase_modeling_guide() -> str:
    """
    BIMBase pyp3d 建模的标准工作流和提示词指导。
    当用户要求生成三维几何模型、编写 pyp3d 脚本时，客户端应附加此 Prompt 以指导 Agent。
    """
    return """
# BIMBase MCP 建模指南 (MCP Modeling Guide)

本指南用于指导你在处理用户的 pyp3d 几何建模需求时，如何正确使用 BIMBase MCP Server 提供的检索工具链，获取所需的 API 文档，并产出符合规范的 Python 代码。

## 工作流与策略 (Workflow & Strategy)

当你接到建模/编辑/重构模型任务时，请严格遵循以下步骤：

### 1. 检索和规划 (Search & Plan)
- **绝对不要凭记忆猜测函数名或参数**。pyp3d API 与其他常规 Python 库不同，禁止瞎猜参数。
- 第一步，使用 MCP 工具 `get_skill_manifest()` 浏览所有几何体或操作的API，思考你需要组合哪些函数来完成任务。
- 仔细阅读返回的 JSON，找到 `description` 符合预期的 `symbol`（如 `Cube`, `Sweep`, `Bool`）。

### 2. 批量获取文档 (Bundle Fetch)
- 规划好本次建模需要用到的所有 `symbol` 后，调用 `get_skill_bundle(symbols=["Cube", "Sweep", "Bool"])`。
- MCP Server 会一次性返回所有相关的完整 API 文档，并自动附带前置依赖规范。
- 如果你还需要该函数的配套操作，可使用 `get_related_skills(symbol)` 查找关联推荐。

### 3. 遵循编码规范 (Coding Standards)
在开始编写代码前，你必须严格遵守返回的 `basic_writing_style.md`（作为基础规范被 bundle 自动附带）中的规定。以下是绝对不能违反的规范底线：
- **引用**：顶部必须包含 `from pyp3d import *`
- **类结构**：文件中只能定义一个继承自 `Component` 的类。
- **参数定义**：使用 `self['参数名'] = Attr(...)` 显式定义参数（支持 `obvious=True`, `show=True`, `combo=[...]`），并在 `__init__` 中调用 `self.replace()`。
- **建模逻辑**：造型逻辑必须写在带有 `@export` 装饰器的 `replace(self)` 方法中。
- **变量提取**：在 `replace` 方法内通过 `L = self['长']` 提取参数使用，不要将数值写死。
- **结果输出**：在 `if __name__ == "__main__":` 下实例化类，并通过 `place(实例)` 将最终结果布置在视图中。
"""

if __name__ == "__main__":
    # 使用 STDIO 传输协议（Trae IDE command 型 MCP 通过标准输入输出通信）
    mcp.run(transport="stdio")
