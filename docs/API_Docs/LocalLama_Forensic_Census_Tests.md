# LocalLama Forensic Census Tests

**Exact test-function count: 49**

| # | Test | Production target |
|---:|---|---|
| 1 | `test_ollama_list_models_parsing` | `OllamaBackend.list_models` |
| 2 | `test_config_save_load_roundtrip` | `AppConfig.save/load` |
| 3 | `test_scroll_restore_policy_near_bottom_pins` | `compute_scroll_restore_plan` |
| 4 | `test_scroll_restore_policy_scrolled_up_preserves_position` | `compute_scroll_restore_plan` |
| 5 | `test_visible_messages_exclude_internal_system` | `visible_chat_messages` |
| 6 | `test_assistant_label_prefers_message_model_then_fallback_active_model` | `assistant_label` |
| 7 | `test_request_redaction_only_for_internal_system_prompt` | `redacted_request_messages` |
| 8 | `test_config_load_save_roundtrip` | `AppConfig` |
| 9 | `test_reasoning_mode_persists_in_config` | `GenerationParameters`, config |
| 10 | `test_reasoning_mode_is_exclusive_via_single_enum` | `GenerationParameters.__post_init__` |
| 11 | `test_legacy_generation_parameters_load_but_do_not_emit_strict_backend_options` | `to_backend_options` |
| 12 | `test_legacy_unversioned_config_migrates_to_current_schema` | `_migrate_data` |
| 13 | `test_future_config_schema_is_rejected` | `AppConfig.load` |
| 14 | `test_chat_controller_invalid_prompt_no_crash` | `ChatController.send_message` |
| 15 | `test_model_controller_invalid_model_name_no_crash` | `ModelController.pull_model/push_model` |
| 16 | `test_send_and_regenerate_regression` | `ChatController.send_message/regenerate` |
| 17 | `test_save_current_regression` | `ChatController.save_current` |
| 18 | `test_edit_message_uses_visible_index_and_skips_internal_system` | `ChatController.edit_message` |
| 19 | `test_delete_message_uses_visible_index_and_skips_internal_system` | `ChatController.delete_message` |
| 20 | `test_model_create_delegates_to_editor` | `ModelController.create_model` |
| 21 | `test_plugin_reload_regression` | `PluginController.reload_plugins` |
| 22 | `test_logging_record_uses_structured_diagnostics_format` | `QtLogHandler.emit` |
| 23 | `test_line_buffered_stream_emits_complete_lines_and_flushes_partial_text` | `LineBufferedStream` |
| 24 | `test_append_output_is_cursor_safe` | `append_output` |
| 25 | `test_operation_stream_parser_assembles_partial_json_and_collapses_statuses` | `OperationStreamParser.feed` |
| 26 | `test_operation_update_refreshes_live_status_and_progress_without_history_spam` | `MainWindow.update_operation` |
| 27 | `test_delete_model_without_selection_shows_info` | `ModelController.delete_model` |
| 28 | `test_delete_model_confirmed_runs_async` | `ModelController.delete_model` |
| 29 | `test_model_metadata_table_items_are_non_editable_and_selectable` | `_build_readonly_table_item` |
| 30 | `test_run_async_routes_lifecycle_to_operations_before_dialog` | `MainWindow.run_async` |
| 31 | `test_pull_stream_collapses_repeated_status_and_updates_progress` | `ModelController.pull_model` |
| 32 | `test_pull_partial_chunks_do_not_create_corrupt_history` | `OperationStreamParser` |
| 33 | `test_stream_error_updates_operations_before_dialog` | `ModelController.push_model` |
| 34 | `test_clone_strips_names_and_delete_contract_remains_public` | `ModelController.clone_model` |
| 35 | `test_create_stream_uses_operations_without_console_output` | `MainWindow.build_model_from_modelfile` |
| 36 | `test_templates_require_a_selected_model` | `MainWindow.open_template_viewer` |
| 37 | `test_templates_route_lifecycle_to_operations_before_dialog` | `MainWindow.open_template_viewer` |
| 38 | `test_list_models_parses_missing_and_partial_fields` | `OllamaBackend.list_models` |
| 39 | `test_test_connection_returns_disconnected_on_http_error` | `OllamaBackend.test_connection` |
| 40 | `test_test_connection_returns_disconnected_on_timeout` | `OllamaBackend.test_connection` |
| 41 | `test_chat_payload_emits_only_selected_reasoning_mode` | `OllamaBackend.chat/build_chat_payload` |
| 42 | `test_sanitize_options_preserves_supported_and_filters_invalid_and_stop_fragments` | `sanitize_options` |
| 43 | `test_sanitize_request_fields_only_forwards_supported_top_level_fields` | `sanitize_request_fields` |
| 44 | `test_stream_endpoint_raises_for_successful_http_response_with_error_payload` | `_stream_endpoint` |
| 45 | `test_plugin_lifecycle_discover_validate_trust_enable_disable_reload_untrust_remove` | `PluginManager` |
| 46 | `test_plugin_discovery_reports_manifest_validation_error` | plugin discovery/trust |
| 47 | `test_api_key_is_not_serialized_to_config` | `CredentialStore`, `AppConfig.save` |
| 48 | `test_plugin_discovery_does_not_execute_module_code` | `PluginManager.discover` |
| 49 | `test_untrusted_plugin_is_rejected_before_import` | `PluginManager.enable` |

## Test doubles and boundaries

- fake `httpx.AsyncClient`
- fake HTTP/stream responses
- fake windows/session managers
- fake Qt signals/tasks
- `monkeypatch`
- `tmp_path`
- `pytest.raises`
- PySide6 QApplication/UI objects in diagnostics tests

No active packaging-installer test file exists under `tests/`.
No dedicated model-browser/setup-wizard test module exists.
