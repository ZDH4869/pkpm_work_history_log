import functools
import inspect
import json
import os
import socket
import threading
import time
import traceback
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Callable, Dict, Optional

from config import (  # noqa: F401
    APP_NAME,
    DEBUG_MODE,
    LOG_PATH,
    MCP_MONITOR_CAPTURE_TRACEBACK,
    MCP_MONITOR_ENABLED,
    MCP_MONITOR_LOG_FILE,
    MCP_MONITOR_LOG_RESULT_PREVIEW,
    MCP_MONITOR_MAX_FIELD_LENGTH,
    MCP_MONITOR_METRICS_ENABLED,
    MCP_MONITOR_RECENT_FAILURE_LIMIT,
    MCP_MONITOR_STDOUT_ENABLED,
)


DetailExtractor = Callable[[tuple, dict, Any, Optional[Exception]], Dict[str, Any]]
ResultInspector = Callable[[tuple, dict, Any], Dict[str, Any]]


def _now_iso() -> str:
    return datetime.now().astimezone().isoformat(timespec="milliseconds")


def _truncate_text(text: str, max_length: int) -> str:
    if len(text) <= max_length:
        return text
    return f"{text[:max_length]}...<truncated:{len(text) - max_length}>"


def _estimate_size(value: Any) -> int:
    try:
        return len(json.dumps(value, ensure_ascii=False, default=str))
    except Exception:
        return len(str(value))


def _summarize_value(value: Any, max_length: int, depth: int = 0) -> Any:
    if depth >= 3:
        return _truncate_text(repr(value), max_length)

    if value is None or isinstance(value, (bool, int, float)):
        return value

    if isinstance(value, str):
        return _truncate_text(value, max_length)

    if isinstance(value, Path):
        return _truncate_text(str(value), max_length)

    if isinstance(value, (list, tuple)):
        items = list(value)
        limit = 10
        summarized = [_summarize_value(v, max_length, depth + 1) for v in items[:limit]]
        if len(items) > limit:
            summarized.append(f"...<truncated_items:{len(items) - limit}>")
        return summarized

    if isinstance(value, set):
        return _summarize_value(sorted(value), max_length, depth + 1)

    if isinstance(value, dict):
        result: Dict[str, Any] = {}
        limit = 20
        for idx, (k, v) in enumerate(value.items()):
            if idx >= limit:
                result["..."] = f"<truncated_keys:{len(value) - limit}>"
                break
            result[str(k)] = _summarize_value(v, max_length, depth + 1)
        return result

    return _truncate_text(repr(value), max_length)


class ToolInvocationMonitor:
    def __init__(self) -> None:
        self.enabled = bool(MCP_MONITOR_ENABLED)
        self.log_result_preview = bool(MCP_MONITOR_LOG_RESULT_PREVIEW)
        self.capture_traceback = bool(MCP_MONITOR_CAPTURE_TRACEBACK)
        self.max_field_length = int(MCP_MONITOR_MAX_FIELD_LENGTH)
        self.metrics_enabled = bool(MCP_MONITOR_METRICS_ENABLED)
        self.stdout_enabled = bool(MCP_MONITOR_STDOUT_ENABLED)
        self.log_file = Path(MCP_MONITOR_LOG_FILE)
        self.host = socket.gethostname()
        self.pid = os.getpid()
        self._write_lock = threading.Lock()
        self._metrics_lock = threading.Lock()
        self._metrics: Dict[str, Dict[str, Any]] = {}
        self._recent_failures = []

        if self.enabled:
            self.log_file.parent.mkdir(parents=True, exist_ok=True)
            Path(LOG_PATH).mkdir(parents=True, exist_ok=True)

    def _safe_write_event(self, event: Dict[str, Any]) -> None:
        if not self.enabled:
            return
        try:
            line = json.dumps(event, ensure_ascii=False, default=str)
            with self._write_lock:
                with self.log_file.open("a", encoding="utf-8") as handle:
                    handle.write(line + "\n")
        except Exception:
            # Monitoring must never break the tool execution path.
            pass

    def _compact_json(self, value: Any) -> str:
        try:
            return json.dumps(value, ensure_ascii=False, default=str)
        except Exception:
            return str(value)

    def _safe_print_event_summary(self, event: Dict[str, Any]) -> None:
        if not self.stdout_enabled:
            return

        try:
            lines = [
                "[MCP Monitor]",
                f"tool={event.get('tool_name', '')}",
                f"status={event.get('status', '')}",
                f"duration_ms={event.get('duration_ms', '')}",
            ]

            if event.get("agent_input_present"):
                lines.append(f"agent_input={event.get('agent_input_summary', '')}")
            if event.get("requested_skills"):
                lines.append(f"requested_skills={self._compact_json(event.get('requested_skills'))}")
            if event.get("requested_paths"):
                lines.append(f"requested_paths={self._compact_json(event.get('requested_paths'))}")
            if event.get("resolved_skills"):
                lines.append(f"resolved_skills={self._compact_json(event.get('resolved_skills'))}")
            if event.get("resolved_paths"):
                lines.append(f"resolved_paths={self._compact_json(event.get('resolved_paths'))}")
            if event.get("missing_skills"):
                lines.append(f"missing_skills={self._compact_json(event.get('missing_skills'))}")
            if event.get("error_message"):
                lines.append(f"error={event.get('error_message')}")

            with self._write_lock:
                print("\n".join(lines), flush=True)
        except Exception:
            # Console printing is best effort only.
            pass

    def _merge_metadata(self, event: Dict[str, Any], metadata: Optional[Dict[str, Any]]) -> None:
        if not isinstance(metadata, dict):
            return
        for key, value in metadata.items():
            event[key] = _summarize_value(value, self.max_field_length)

    def _update_metrics(self, tool_name: str, status: str, duration_ms: float, event: Dict[str, Any]) -> None:
        if not self.metrics_enabled:
            return

        try:
            with self._metrics_lock:
                item = self._metrics.setdefault(
                    tool_name,
                    {
                        "calls": 0,
                        "success": 0,
                        "error": 0,
                        "total_duration_ms": 0.0,
                        "avg_duration_ms": 0.0,
                        "last_called_at": None,
                        "last_error_at": None,
                    },
                )
                item["calls"] += 1
                item[status] += 1
                item["total_duration_ms"] += duration_ms
                item["avg_duration_ms"] = round(item["total_duration_ms"] / item["calls"], 3)
                item["last_called_at"] = event.get("finished_at")
                if status == "error":
                    item["last_error_at"] = event.get("finished_at")
                    self._recent_failures.append(
                        {
                            "tool_name": tool_name,
                            "finished_at": event.get("finished_at"),
                            "error_type": event.get("error_type"),
                            "error_message": event.get("error_message"),
                        }
                    )
                    limit = int(MCP_MONITOR_RECENT_FAILURE_LIMIT)
                    if len(self._recent_failures) > limit:
                        self._recent_failures = self._recent_failures[-limit:]
        except Exception:
            pass

    def record_start(self, tool_name: str, args: tuple, kwargs: dict) -> Dict[str, Any]:
        started_at = _now_iso()
        args_summary = _summarize_value(args, self.max_field_length)
        kwargs_summary = _summarize_value(kwargs, self.max_field_length)
        return {
            "event_id": uuid.uuid4().hex,
            "trace_id": uuid.uuid4().hex,
            "tool_name": tool_name,
            "app_name": APP_NAME,
            "server_name": "BIMBaseAI2PY_MCPServer",
            "transport": "http",
            "host": self.host,
            "pid": self.pid,
            "started_at": started_at,
            "args_summary": args_summary,
            "kwargs_summary": kwargs_summary,
            "input_size": _estimate_size({"args": args_summary, "kwargs": kwargs_summary}),
            "_perf_started": time.perf_counter(),
        }

    def record_success(self, context: Dict[str, Any], result: Any, metadata: Optional[Dict[str, Any]] = None) -> None:
        event = {k: v for k, v in context.items() if not k.startswith("_")}
        event["status"] = "success"
        event["finished_at"] = _now_iso()
        event["duration_ms"] = round((time.perf_counter() - context["_perf_started"]) * 1000, 3)
        event["result_type"] = type(result).__name__
        event["result_size"] = _estimate_size(result)
        if self.log_result_preview:
            event["result_preview"] = _summarize_value(result, self.max_field_length)
        self._merge_metadata(event, metadata)
        self._safe_write_event(event)
        self._safe_print_event_summary(event)
        self._update_metrics(context["tool_name"], "success", event["duration_ms"], event)

    def record_result_error(
        self,
        context: Dict[str, Any],
        result: Any,
        error_type: str,
        error_message: str,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> None:
        event = {k: v for k, v in context.items() if not k.startswith("_")}
        event["status"] = "error"
        event["error_source"] = "result"
        event["finished_at"] = _now_iso()
        event["duration_ms"] = round((time.perf_counter() - context["_perf_started"]) * 1000, 3)
        event["error_type"] = _truncate_text(error_type or "BusinessError", self.max_field_length)
        event["error_message"] = _truncate_text(error_message or "Tool returned an error result.", self.max_field_length)
        event["result_type"] = type(result).__name__
        event["result_size"] = _estimate_size(result)
        if self.log_result_preview:
            event["result_preview"] = _summarize_value(result, self.max_field_length)
        self._merge_metadata(event, metadata)
        self._safe_write_event(event)
        self._safe_print_event_summary(event)
        self._update_metrics(context["tool_name"], "error", event["duration_ms"], event)

    def record_error(self, context: Dict[str, Any], exc: Exception, metadata: Optional[Dict[str, Any]] = None) -> None:
        event = {k: v for k, v in context.items() if not k.startswith("_")}
        event["status"] = "error"
        event["error_source"] = "exception"
        event["finished_at"] = _now_iso()
        event["duration_ms"] = round((time.perf_counter() - context["_perf_started"]) * 1000, 3)
        event["error_type"] = type(exc).__name__
        event["error_message"] = _truncate_text(str(exc), self.max_field_length)
        if self.capture_traceback:
            event["stacktrace"] = _truncate_text(traceback.format_exc(), self.max_field_length * 20)
        self._merge_metadata(event, metadata)
        self._safe_write_event(event)
        self._safe_print_event_summary(event)
        self._update_metrics(context["tool_name"], "error", event["duration_ms"], event)

    def get_metrics_snapshot(self) -> Dict[str, Dict[str, Any]]:
        with self._metrics_lock:
            return json.loads(json.dumps(self._metrics, ensure_ascii=False, default=str))


monitor = ToolInvocationMonitor()


def _safe_extract_metadata(
    detail_extractor: Optional[DetailExtractor],
    args: tuple,
    kwargs: dict,
    result: Any,
    error: Optional[Exception],
) -> Dict[str, Any]:
    if detail_extractor is None:
        return {}
    try:
        data = detail_extractor(args, kwargs, result, error)
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        return {"monitor_detail_extractor_error": f"{type(exc).__name__}: {exc}"}


def _safe_inspect_result(
    result_inspector: Optional[ResultInspector],
    args: tuple,
    kwargs: dict,
    result: Any,
) -> Dict[str, Any]:
    if result_inspector is None:
        return {}
    try:
        data = result_inspector(args, kwargs, result)
        return data if isinstance(data, dict) else {}
    except Exception as exc:
        return {"monitor_result_inspector_error": f"{type(exc).__name__}: {exc}"}


def monitor_mcp_tool(
    tool_name: Optional[str] = None,
    detail_extractor: Optional[DetailExtractor] = None,
    result_inspector: Optional[ResultInspector] = None,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        resolved_name = tool_name or func.__name__

        if inspect.iscoroutinefunction(func):

            @functools.wraps(func)
            async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
                if not monitor.enabled:
                    return await func(*args, **kwargs)

                context = monitor.record_start(resolved_name, args, kwargs)
                try:
                    result = await func(*args, **kwargs)
                    metadata = _safe_extract_metadata(detail_extractor, args, kwargs, result, None)
                    inspection = _safe_inspect_result(result_inspector, args, kwargs, result)
                    if inspection:
                        metadata = {**metadata, **(inspection.get("metadata") or {})}
                        if inspection.get("monitor_result_inspector_error"):
                            metadata["monitor_result_inspector_error"] = inspection["monitor_result_inspector_error"]
                    if inspection.get("status") == "error":
                        monitor.record_result_error(
                            context,
                            result,
                            error_type=str(inspection.get("error_type", "BusinessError")),
                            error_message=str(inspection.get("error_message", "Tool returned an error result.")),
                            metadata=metadata,
                        )
                    else:
                        monitor.record_success(context, result, metadata=metadata)
                    return result
                except Exception as exc:
                    metadata = _safe_extract_metadata(detail_extractor, args, kwargs, None, exc)
                    monitor.record_error(context, exc, metadata=metadata)
                    raise

            return async_wrapper

        @functools.wraps(func)
        def sync_wrapper(*args: Any, **kwargs: Any) -> Any:
            if not monitor.enabled:
                return func(*args, **kwargs)

            context = monitor.record_start(resolved_name, args, kwargs)
            try:
                result = func(*args, **kwargs)
                metadata = _safe_extract_metadata(detail_extractor, args, kwargs, result, None)
                inspection = _safe_inspect_result(result_inspector, args, kwargs, result)
                if inspection:
                    metadata = {**metadata, **(inspection.get("metadata") or {})}
                    if inspection.get("monitor_result_inspector_error"):
                        metadata["monitor_result_inspector_error"] = inspection["monitor_result_inspector_error"]
                if inspection.get("status") == "error":
                    monitor.record_result_error(
                        context,
                        result,
                        error_type=str(inspection.get("error_type", "BusinessError")),
                        error_message=str(inspection.get("error_message", "Tool returned an error result.")),
                        metadata=metadata,
                    )
                else:
                    monitor.record_success(context, result, metadata=metadata)
                return result
            except Exception as exc:
                metadata = _safe_extract_metadata(detail_extractor, args, kwargs, None, exc)
                monitor.record_error(context, exc, metadata=metadata)
                raise

        return sync_wrapper

    return decorator
