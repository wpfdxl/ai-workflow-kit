#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# python3 my/doc/sbdoc_web.py --port 9121

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, unquote, urlparse


DOC_ROOT = Path(__file__).resolve().parent
CONFIG_FILE = DOC_ROOT / "hfdoc_config.json"

DEFAULT_VIEWER_CONFIG = {
    "viewer": {
        "title": "HFDoc Viewer",
        "subtitle": "进行中目录在下方列表；已归档请点右上角按钮。\n默认只维护 json 文档。",
    },
    "api_debug": {
        "default_client": 1,
        "open_button_text": "打开测试地址",
        "clients": {
            "1": {
                "label": "测试主站",
                "base_url": "https://test-www.com",
            }
        },
    },
}


HTML_PAGE = """<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>HFDoc Viewer</title>
  <style>
    * { box-sizing: border-box; }
    body {
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", "PingFang SC",
        "Microsoft YaHei", Arial, sans-serif;
      background: #f5f7fb;
      color: #263238;
    }
    .app {
      display: flex;
      min-height: 100vh;
    }
    .sidebar {
      width: 360px;
      border-right: 1px solid #e5e9f2;
      background: #fff;
      padding: 20px 16px;
      overflow-y: auto;
      position: sticky;
      top: 0;
      height: 100vh;
    }
    .main {
      flex: 1;
      padding: 24px;
      overflow-y: auto;
    }
    ::-webkit-scrollbar { width: 8px; height: 8px; }
    ::-webkit-scrollbar-thumb {
      background: #c9d3e6;
      border-radius: 999px;
    }
    ::-webkit-scrollbar-thumb:hover { background: #a9b8d8; }
    ::-webkit-scrollbar-track { background: transparent; }
    .title {
      margin: 0;
      font-size: 22px;
      font-weight: 700;
    }
    .sidebar-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 10px;
      margin-bottom: 8px;
    }
    .subtitle {
      margin: 0 0 14px;
      color: #607083;
      font-size: 13px;
      line-height: 1.6;
    }
    .search {
      width: 100%;
      padding: 10px 12px;
      border: 1px solid #d7dee8;
      border-radius: 10px;
      font-size: 14px;
      outline: none;
    }
    .archive-entry {
      flex-shrink: 0;
      padding: 5px 10px;
      border: 1px solid #f0c78a;
      border-radius: 999px;
      background: linear-gradient(135deg, #fff6e8, #ffe8c8);
      color: #8a5a00;
      font-size: 12px;
      font-weight: 700;
      line-height: 1.3;
      white-space: nowrap;
      cursor: pointer;
      box-shadow: 0 2px 6px rgba(196, 130, 20, 0.12);
    }
    .archive-entry:hover {
      border-color: #e0a84a;
      background: linear-gradient(135deg, #ffe8c8, #ffd8a0);
    }
    .archive-entry.active {
      border-color: #d4891a;
      background: linear-gradient(135deg, #ffe0a8, #ffd08a);
    }
    .group-title {
      margin: 18px 0 10px;
      color: #243b53;
      font-size: 14px;
      font-weight: 700;
    }
    .dir-list, .doc-list {
      display: flex;
      flex-direction: column;
      gap: 10px;
    }
    .dir-item, .doc-item {
      display: block;
      width: 100%;
      padding: 12px;
      border: 1px solid #e5e9f2;
      border-radius: 12px;
      background: #fbfcff;
      text-align: left;
      cursor: pointer;
      transition: border-color 0.15s ease, background 0.15s ease,
        box-shadow 0.15s ease;
    }
    .dir-item:hover, .doc-item:hover {
      border-color: #aebffc;
      box-shadow: 0 4px 12px rgba(91, 124, 250, 0.12);
    }
    .dir-item.active, .doc-item.active {
      border-color: #5b7cfa;
      background: #eef2ff;
    }
    .dir-name, .doc-name {
      font-size: 14px;
      font-weight: 700;
      word-break: break-all;
    }
    .dir-path, .doc-path {
      margin-top: 6px;
      color: #607083;
      font-size: 12px;
      word-break: break-all;
      line-height: 1.5;
    }
    .doc-group {
      border: 1px solid #e5e9f2;
      border-radius: 14px;
      background: #fff;
      overflow: hidden;
      transition: border-color 0.15s ease, box-shadow 0.15s ease;
    }
    .doc-group.active {
      border-color: #5b7cfa;
      box-shadow: 0 6px 18px rgba(91, 124, 250, 0.14);
    }
    .doc-group .doc-item {
      border: 0;
      border-radius: 0;
      background: linear-gradient(180deg, #f8faff, #f1f4fd);
      border-bottom: 1px solid #e9edf7;
    }
    .doc-group.active .doc-item {
      background: linear-gradient(135deg, #5b7cfa, #7c4dff);
    }
    .doc-group.active .doc-name { color: #fff; }
    .doc-group.active .doc-path { color: rgba(255, 255, 255, 0.82); }
    .iface-list {
      display: flex;
      flex-direction: column;
      padding: 6px;
      gap: 2px;
    }
    .iface-item {
      display: flex;
      align-items: center;
      gap: 8px;
      width: 100%;
      padding: 8px 10px;
      border: 0;
      border-radius: 10px;
      background: transparent;
      text-align: left;
      cursor: pointer;
      transition: background 0.15s ease;
    }
    .iface-item:hover { background: #f1f4fd; }
    .iface-item.active {
      background: #eef2ff;
    }
    .iface-item.active .iface-name {
      color: #4338ca;
      font-weight: 700;
    }
    .iface-name {
      flex: 1;
      font-size: 13px;
      color: #344563;
      line-height: 1.45;
      word-break: break-all;
    }
    .mini-method {
      flex-shrink: 0;
      min-width: 42px;
      padding: 2px 6px;
      border-radius: 6px;
      font-size: 10px;
      font-weight: 800;
      text-align: center;
      letter-spacing: 0.4px;
    }
    .hero {
      padding: 20px 22px;
      border-radius: 16px;
      color: #fff;
      background: linear-gradient(135deg, #5b7cfa, #7c4dff);
      box-shadow: 0 10px 24px rgba(91, 124, 250, 0.18);
    }
    .hero h2 {
      margin: 0 0 8px;
      font-size: 28px;
    }
    .hero p {
      margin: 0;
      opacity: 0.92;
      line-height: 1.6;
    }
    .stats {
      margin-top: 16px;
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
    }
    .stat {
      padding: 8px 12px;
      border-radius: 999px;
      background: rgba(255, 255, 255, 0.18);
      font-size: 13px;
    }
    .toolbar {
      margin: 18px 0;
      display: flex;
      justify-content: space-between;
      align-items: center;
      gap: 12px;
      flex-wrap: wrap;
    }
    .count {
      color: #607083;
      font-size: 13px;
    }
    .overview-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
      gap: 14px;
      margin-top: 18px;
    }
    .overview-card {
      padding: 18px;
      border: 1px solid #e5e9f2;
      border-radius: 16px;
      background: #fff;
      box-shadow: 0 8px 24px rgba(31, 45, 61, 0.06);
      cursor: pointer;
    }
    .overview-card h3 {
      margin: 0 0 8px;
      font-size: 17px;
    }
    .overview-card p {
      margin: 0;
      color: #607083;
      font-size: 13px;
      line-height: 1.6;
    }
    .section-card {
      margin-top: 18px;
      padding: 20px;
      border: 1px solid #e5e9f2;
      border-radius: 16px;
      background: #fff;
      box-shadow: 0 8px 24px rgba(31, 45, 61, 0.06);
      scroll-margin-top: 16px;
    }
    .section-card.highlight {
      animation: cardFlash 1.6s ease;
    }
    @keyframes cardFlash {
      0% {
        border-color: #5b7cfa;
        box-shadow: 0 0 0 4px rgba(91, 124, 250, 0.25);
      }
      100% {
        border-color: #e5e9f2;
        box-shadow: 0 8px 24px rgba(31, 45, 61, 0.06);
      }
    }
    .section-top {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      flex-wrap: wrap;
    }
    .section-title {
      margin: 0;
      font-size: 28px;
      font-weight: 800;
      color: #1f2d3d;
    }
    .badges {
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
    }
    .badge {
      display: inline-flex;
      align-items: center;
      min-height: 28px;
      padding: 4px 10px;
      border-radius: 999px;
      font-size: 12px;
      font-weight: 700;
    }
    .method-GET { background: #e8f5ff; color: #1264a3; }
    .method-POST { background: #ecfdf3; color: #147a3f; }
    .method-PUT { background: #fff7e6; color: #ad6800; }
    .method-DELETE { background: #fff1f0; color: #cf1322; }
    .url-badge {
      background: #dbeafe;
      color: #1d4ed8;
      font-size: 15px;
      font-weight: 800;
      padding: 8px 14px;
    }
    .action-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 36px;
      padding: 8px 14px;
      border: 1px solid #c7d2fe;
      border-radius: 999px;
      background: #fff;
      color: #4338ca;
      font-size: 13px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
      text-decoration: none;
    }
    .action-btn:hover {
      background: #eef2ff;
      border-color: #a5b4fc;
      box-shadow: 0 4px 12px rgba(99, 102, 241, 0.16);
    }
    .table-wrap { overflow-x: auto; margin-top: 14px; }
    .response-wrap {
      margin-top: 14px;
      padding: 18px;
      border-radius: 18px;
      background: #ffffff;
      border: 1px solid #e5e9f2;
      box-shadow: 0 10px 24px rgba(15, 23, 42, 0.06);
    }
    .response-tabs {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 14px;
    }
    .response-tab {
      display: inline-flex;
      align-items: center;
      min-height: 34px;
      padding: 6px 14px;
      border-radius: 999px;
      background: #ecfdf3;
      color: #147a3f;
      font-size: 13px;
      font-weight: 700;
      border: 1px solid #bbf7d0;
    }
    .response-meta {
      display: flex;
      gap: 10px;
      flex-wrap: wrap;
      margin-bottom: 16px;
    }
    .response-meta-badge {
      display: inline-flex;
      align-items: center;
      min-height: 30px;
      padding: 4px 12px;
      border-radius: 999px;
      background: #f8fafc;
      color: #334155;
      font-size: 12px;
      font-weight: 700;
      border: 1px solid #e2e8f0;
    }
    .response-doc-panel,
    .response-example-panel {
      min-width: 0;
      border: 1px solid #e5e9f2;
      border-radius: 16px;
      background: #fbfcff;
      overflow: hidden;
    }
    .response-panel-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 12px 14px;
      background: #f8fafc;
      border-bottom: 1px solid #e5e9f2;
    }
    .response-panel-title {
      color: #243b53;
      font-size: 13px;
      font-weight: 800;
    }
    .response-fields {
      padding: 14px;
      display: flex;
      flex-direction: column;
      gap: 12px;
    }
    .response-field-card {
      border: 1px solid #e5e9f2;
      border-radius: 14px;
      background: #ffffff;
      overflow: hidden;
    }
    .response-field-row {
      display: grid;
      grid-template-columns: minmax(160px, 1.1fr) 90px 70px minmax(180px, 1.4fr) minmax(120px, 1fr);
      gap: 10px;
      padding: 12px 14px;
      align-items: start;
    }
    .response-field-row + .response-field-row {
      border-top: 1px solid #eef2f7;
    }
    .response-col-label {
      display: block;
      margin-bottom: 6px;
      color: #64748b;
      font-size: 11px;
      font-weight: 700;
      letter-spacing: 0.2px;
    }
    .response-col-value {
      color: #0f172a;
      font-size: 13px;
      line-height: 1.65;
      word-break: break-word;
    }
    .response-required {
      display: inline-flex;
      align-items: center;
      min-height: 24px;
      padding: 2px 8px;
      border-radius: 999px;
      background: #eef2ff;
      color: #4338ca;
      font-size: 11px;
      font-weight: 700;
    }
    .response-required.optional {
      background: #f8fafc;
      color: #64748b;
    }
    .response-nested {
      margin: 0 14px 14px;
      border-left: 3px solid #c7d2fe;
      background: #f8faff;
      border-radius: 0 12px 12px 0;
      padding: 12px 12px 0 12px;
    }
    .response-nested-title {
      margin: 0 0 12px;
      color: #4338ca;
      font-size: 12px;
      font-weight: 800;
    }
    .json-preview {
      margin-top: 16px;
      border: 1px solid #1e293b;
      border-radius: 12px;
      overflow: hidden;
      background: #0b1220;
    }
    .json-preview-head {
      display: flex;
      align-items: center;
      justify-content: space-between;
      gap: 12px;
      padding: 10px 14px;
      background: #0f172a;
      border-bottom: 1px solid #1e293b;
    }
    .json-preview-title {
      color: #f8fafc;
      font-size: 13px;
      font-weight: 700;
    }
    .copy-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      min-height: 28px;
      padding: 4px 12px;
      border: 1px solid #6366f1;
      border-radius: 999px;
      background: #4338ca;
      color: #eef2ff;
      font-size: 12px;
      font-weight: 700;
      cursor: pointer;
      transition: all 0.15s ease;
    }
    .copy-btn:hover {
      background: #4f46e5;
      border-color: #818cf8;
    }
    .json-code {
      margin: 0;
      padding: 14px 16px;
      overflow-x: auto;
      color: #e2e8f0;
      font-family: Menlo, Consolas, "SF Mono", monospace;
      font-size: 12px;
      line-height: 1.6;
      white-space: pre-wrap;
      word-break: break-word;
    }
    table {
      width: 100%;
      border-collapse: collapse;
      background: #fff;
    }
    th, td {
      padding: 10px 12px;
      border: 1px solid #e6ebf1;
      text-align: left;
      vertical-align: top;
      font-size: 13px;
    }
    th {
      background: #f8fafc;
      color: #334e68;
      font-weight: 700;
    }
    code {
      padding: 2px 6px;
      border-radius: 6px;
      background: #eef2ff;
      color: #304ffe;
      font-family: Menlo, Consolas, monospace;
      font-size: 12px;
    }
    .empty, .loading, .error {
      padding: 24px;
      border: 1px dashed #c8d2dc;
      border-radius: 16px;
      background: #fff;
      color: #607083;
      text-align: center;
    }
    .error {
      color: #cf1322;
      border-color: #ffccc7;
      background: #fff2f0;
    }
    .sub-title {
      margin: 18px 0 8px;
      font-size: 15px;
      color: #243b53;
      font-weight: 700;
    }
    .nested {
      margin-top: 12px;
      padding: 12px;
      border-radius: 12px;
      background: #fbfcfe;
      border: 1px solid #eef2f7;
    }
    .footer-tip {
      margin-top: 20px;
      color: #607083;
      font-size: 12px;
    }
    @media (max-width: 960px) {
      .app { display: block; }
      .sidebar {
        width: auto;
        border-right: 0;
        border-bottom: 1px solid #e5e9f2;
      }
      .response-field-row {
        grid-template-columns: 1fr;
      }
    }
  </style>
</head>
<body>
  <div class="app">
    <aside class="sidebar">
      <div class="sidebar-head">
        <h1 id="viewerTitle" class="title">HFDoc Viewer</h1>
        <button id="archiveEntry" class="archive-entry" type="button" title="查看已归档文档">
          已归档 · <span id="archiveIfaceCount">0</span>
        </button>
      </div>
      <p id="viewerSubtitle" class="subtitle">
        进行中目录在下方列表；已归档请点右上角按钮。<br>
        默认只维护 json 文档。
      </p>
      <input id="searchInput" class="search" placeholder="搜索目录名或文件名" />
      <div id="dirTitle" class="group-title">目录</div>
      <div id="dirList" class="dir-list"></div>
      <div id="docTitle" class="group-title">文档</div>
      <div id="docList" class="doc-list"></div>
    </aside>
    <main class="main">
      <div id="content" class="loading">正在加载文档目录...</div>
    </main>
  </div>
  <script>
    const TYPE_LABEL_MAP = {
      0: '字符串',
      1: 'number',
      3: '数组',
      4: 'map',
    };

    const ARCHIVE_ROOT = 'archive';

    const state = {
      docs: [],
      dirs: [],
      filteredDocs: [],
      filteredDirs: [],
      activeDir: '',
      activeFile: '',
      activeDoc: null,
      activeIfaceIndex: -1,
      searchKeyword: '',
      config: {},
    };

    function escapeHtml(text) {
      return String(text ?? '')
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#39;');
    }

    function getQueryState() {
      const params = new URLSearchParams(window.location.search);
      return {
        dir: params.get('dir') || '',
        file: params.get('file') || '',
      };
    }

    function setQueryState(dir, file) {
      const url = new URL(window.location.href);
      if (dir) {
        url.searchParams.set('dir', dir);
      } else {
        url.searchParams.delete('dir');
      }
      if (file) {
        url.searchParams.set('file', file);
      } else {
        url.searchParams.delete('file');
      }
      history.replaceState(null, '', url.toString());
    }

    async function fetchJson(url) {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('请求失败: ' + response.status);
      }
      return response.json();
    }

    function getDirLabel(dirPath) {
      if (!dirPath) {
        return 'doc';
      }
      if (dirPath === ARCHIVE_ROOT) {
        return '已归档';
      }
      return dirPath;
    }

    function isArchivePath(dirPath) {
      return dirPath === ARCHIVE_ROOT || dirPath.startsWith(ARCHIVE_ROOT + '/');
    }

    function getParentDir(dirPath) {
      if (!dirPath) {
        return '';
      }
      const idx = dirPath.lastIndexOf('/');
      if (idx < 0) {
        return '';
      }
      return dirPath.slice(0, idx);
    }

    /** 是否为 parentDir 的直接子目录（根目录下只展示一级） */
    function isImmediateChildDir(parentDir, childDir) {
      if (!childDir) {
        return false;
      }
      if (!parentDir) {
        return childDir.indexOf('/') < 0;
      }
      const prefix = parentDir + '/';
      if (!childDir.startsWith(prefix)) {
        return false;
      }
      const rest = childDir.slice(prefix.length);
      return rest !== '' && rest.indexOf('/') < 0;
    }

    function getArchiveIfaceCount() {
      const archiveMeta = state.dirs.find((dir) => dir.path === ARCHIVE_ROOT);
      if (!archiveMeta) {
        return 0;
      }
      return archiveMeta.iface_count || 0;
    }

    function renderArchiveEntry() {
      const btn = document.getElementById('archiveEntry');
      const countEl = document.getElementById('archiveIfaceCount');
      if (!btn || !countEl) {
        return;
      }
      countEl.textContent = String(getArchiveIfaceCount());
      if (isArchivePath(state.activeDir)) {
        btn.classList.add('active');
      } else {
        btn.classList.remove('active');
      }
    }

    function getTypeLabel(typeValue) {
      if (Object.prototype.hasOwnProperty.call(TYPE_LABEL_MAP, typeValue)) {
        return TYPE_LABEL_MAP[typeValue];
      }
      const numValue = Number(typeValue);
      if (Object.prototype.hasOwnProperty.call(TYPE_LABEL_MAP, numValue)) {
        return TYPE_LABEL_MAP[numValue];
      }
      return String(typeValue ?? '');
    }

    function getApiDebugConfig() {
      return state.config.api_debug || {};
    }

    function getClientConfig(clientKey) {
      const clients = getApiDebugConfig().clients || {};
      if (clientKey !== '' && clientKey !== null && clientKey !== undefined && clients[clientKey]) {
        return clients[clientKey];
      }
      const defaultClient = getApiDebugConfig().default_client;
      if (defaultClient !== '' && defaultClient !== null && defaultClient !== undefined && clients[defaultClient]) {
        return clients[defaultClient];
      }
      return {
        label: '',
        base_url: '',
      };
    }

    function getClientKey(doc, item) {
      const ifaceMeta = item && item._hfdoc ? item._hfdoc : {};
      if (ifaceMeta.client !== '' && ifaceMeta.client !== null && ifaceMeta.client !== undefined) {
        return ifaceMeta.client;
      }
      const docMeta = doc && doc._hfdoc ? doc._hfdoc : {};
      if (docMeta.client !== '' && docMeta.client !== null && docMeta.client !== undefined) {
        return docMeta.client;
      }
      const itemUrl = String(item && item.url ? item.url : '');
      if (/^\\/interapi\\//.test(itemUrl)) {
        return 2;
      }
      return getApiDebugConfig().default_client;
    }

    function getOpenButtonText() {
      return getApiDebugConfig().open_button_text || '打开测试地址';
    }

    function normalizeInterfacePath(path, clientKey) {
      const cleanPath = String(path || '').trim();
      if (!cleanPath) {
        return '';
      }
      if (String(clientKey) === '2') {
        return cleanPath.replace(/^\\/interapi(?=\\/|$)/, '') || '/';
      }
      return cleanPath;
    }

    function buildDebugUrl(path, doc, item) {
      const clientKey = getClientKey(doc, item);
      const clientConfig = getClientConfig(clientKey);
      const apiBaseUrl = String(clientConfig.base_url || '').trim();
      const cleanPath = normalizeInterfacePath(path, clientKey);
      if (!cleanPath) {
        return apiBaseUrl;
      }
      if (/^https?:\\/\\//i.test(cleanPath)) {
        return cleanPath;
      }
      const base = apiBaseUrl.replace(/\\/+$/, '');
      const relative = cleanPath.replace(/^\\/+/, '');
      return base + '/' + relative;
    }

    function applyViewerConfig() {
      const viewerConfig = state.config.viewer || {};
      const titleEl = document.getElementById('viewerTitle');
      const subtitleEl = document.getElementById('viewerSubtitle');
      if (titleEl && viewerConfig.title) {
        titleEl.textContent = viewerConfig.title;
      }
      if (subtitleEl && viewerConfig.subtitle) {
        subtitleEl.innerHTML = escapeHtml(viewerConfig.subtitle).replace(/\\n/g, '<br>');
      }
    }

    function docMatchesDir(doc, dirPath) {
      if (!dirPath) {
        return true;
      }
      // 当前目录只展示本层 json，子目录里的文档点进子目录再看
      return doc.dir === dirPath;
    }

    function applyFilters() {
      const keyword = state.searchKeyword.trim().toLowerCase();
      state.filteredDirs = state.dirs.filter((dir) => {
        if (!isImmediateChildDir(state.activeDir, dir.path)) {
          return false;
        }
        // 根目录不展示 archive（用顶部「已归档文档」入口）
        if (!state.activeDir && dir.path === ARCHIVE_ROOT) {
          return false;
        }
        if (!keyword) {
          return true;
        }
        const text = (dir.path + ' ' + dir.name).toLowerCase();
        return text.includes(keyword);
      });
      state.filteredDocs = state.docs.filter((doc) => {
        if (!state.activeDir) {
          return false;
        }
        if (!docMatchesDir(doc, state.activeDir)) {
          return false;
        }
        if (!keyword) {
          return true;
        }
        const text = (doc.name + ' ' + doc.file + ' ' + doc.dir).toLowerCase();
        return text.includes(keyword);
      });
    }

    function renderDirList() {
      const list = document.getElementById('dirList');
      const dirTitle = document.getElementById('dirTitle');
      renderArchiveEntry();
      if (isArchivePath(state.activeDir)) {
        dirTitle.textContent = state.activeDir === ARCHIVE_ROOT
          ? '已归档 · 需求目录'
          : '已归档 · ' + getDirLabel(state.activeDir);
      } else if (state.activeDir) {
        dirTitle.textContent = '子目录 · ' + getDirLabel(state.activeDir);
      } else {
        dirTitle.textContent = '进行中目录';
      }
      dirTitle.style.display = 'block';
      list.style.display = 'flex';
      const items = [];
      if (state.activeDir) {
        const parentLabel = state.activeDir === ARCHIVE_ROOT
          ? '进行中目录'
          : getDirLabel(getParentDir(state.activeDir));
        items.push(`
          <button class="dir-item" data-dir-back="1">
            <div class="dir-name">← 返回上级</div>
            <div class="dir-path">${escapeHtml(parentLabel)}</div>
          </button>
        `);
      }
      state.filteredDirs.forEach((dir) => {
        const active = dir.path === state.activeDir ? 'active' : '';
        items.push(`
          <button class="dir-item ${active}" data-dir="${escapeHtml(dir.path)}">
            <div class="dir-name">${escapeHtml(dir.name)}</div>
            <div class="dir-path">
              ${escapeHtml(dir.path)} · 接口数：${dir.iface_count || 0}
            </div>
          </button>
        `);
      });
      if (!state.filteredDirs.length && !state.activeDir) {
        list.innerHTML = '<div class="empty">没有进行中的接口文档目录</div>';
        renderArchiveEntry();
        return;
      }
      list.innerHTML = items.join('');
      list.querySelectorAll('[data-dir-back]').forEach((button) => {
        button.addEventListener('click', () => {
          if (state.activeDir === ARCHIVE_ROOT) {
            openDirectory('');
            return;
          }
          openDirectory(getParentDir(state.activeDir));
        });
      });
      list.querySelectorAll('[data-dir]').forEach((button) => {
        button.addEventListener('click', () => {
          const dir = button.dataset.dir || '';
          openDirectory(dir);
        });
      });
      renderArchiveEntry();
    }

    function renderDocList() {
      const list = document.getElementById('docList');
      const docTitle = document.getElementById('docTitle');
      if (!state.activeDir) {
        docTitle.style.display = 'none';
        list.style.display = 'none';
        list.innerHTML = '';
        return;
      }
      docTitle.style.display = 'block';
      docTitle.textContent = '接口文档';
      list.style.display = 'flex';
      if (!state.filteredDocs.length) {
        list.innerHTML = '<div class="empty">当前范围下没有 json 文档</div>';
        return;
      }
      list.innerHTML = state.filteredDocs.map((doc) => {
        const active = doc.file === state.activeFile;
        const ifaceItems = (doc.interfaces || []).map((iface) => {
          const ifaceActive = active && state.activeIfaceIndex === iface.index;
          return `
            <button
              class="iface-item ${ifaceActive ? 'active' : ''}"
              data-file="${escapeHtml(doc.file)}"
              data-index="${iface.index}"
            >
              <span class="mini-method method-${escapeHtml(iface.method || 'GET')}">
                ${escapeHtml(iface.method || '-')}
              </span>
              <span class="iface-name">${escapeHtml(iface.name || iface.url || '')}</span>
            </button>
          `;
        }).join('');
        return `
          <div class="doc-group ${active ? 'active' : ''}">
            <button class="doc-item ${active ? 'active' : ''}" data-file="${escapeHtml(doc.file)}">
              <div class="doc-name">${escapeHtml(doc.name || doc.file)}</div>
              <div class="doc-path">
                ${escapeHtml(doc.file)}
                <br>
                目录：${escapeHtml(getDirLabel(doc.dir))} · 接口数：${(doc.interfaces || []).length}
              </div>
            </button>
            ${ifaceItems ? `<div class="iface-list">${ifaceItems}</div>` : ''}
          </div>
        `;
      }).join('');
      list.querySelectorAll('.doc-item').forEach((button) => {
        button.addEventListener('click', () => {
          state.activeIfaceIndex = -1;
          openDoc(button.dataset.file);
        });
      });
      list.querySelectorAll('.iface-item').forEach((button) => {
        button.addEventListener('click', () => {
          openInterface(
            button.dataset.file,
            parseInt(button.dataset.index, 10)
          );
        });
      });
    }

    function renderParamRows(params, depth = 0) {
      if (!Array.isArray(params) || !params.length) {
        return '<div class="empty">无</div>';
      }
      const rows = params.map((item) => {
        const name = item.name === null ? '(数组项)' : (item.name || '');
        const itemType = getParamItemType(item);
        const itemMock = getParamItemMock(item);
        return `
          <tr>
            <td>${'&nbsp;'.repeat(depth * 4)}<code>${escapeHtml(name)}</code></td>
            <td>${escapeHtml(getTypeLabel(itemType))}</td>
            <td>${escapeHtml(getMustLabel(item.must))}</td>
            <td>${escapeHtml(item.remark || '')}</td>
            <td>${escapeHtml(itemMock)}</td>
          </tr>
          ${
            Array.isArray(item.data) && item.data.length
              ? '<tr><td colspan="5"><div class="nested">' +
                renderParamTable(item.data, depth + 1) +
                '</div></td></tr>'
              : ''
          }
        `;
      }).join('');
      return `
        <div class="table-wrap">
          <table>
            <thead>
              <tr>
                <th>字段</th>
                <th>类型</th>
                <th>必填</th>
                <th>说明</th>
                <th>示例</th>
              </tr>
            </thead>
            <tbody>${rows}</tbody>
          </table>
        </div>
      `;
    }

    function renderParamTable(params, depth = 0) {
      return renderParamRows(params, depth);
    }

    function getParamItemType(item) {
      if (item && item.type !== undefined && item.type !== null && item.type !== '') {
        return item.type;
      }
      if (item && item.value && item.value.type !== undefined && item.value.type !== null) {
        return item.value.type;
      }
      return '';
    }

    function getParamItemMock(item) {
      if (item && item.mock !== undefined && item.mock !== null && item.mock !== '') {
        return item.mock;
      }
      if (
        item
        && item.value
        && Array.isArray(item.value.data)
        && item.value.data.length
      ) {
        return item.value.data
          .map((valueItem) => valueItem && valueItem.value !== undefined ? String(valueItem.value) : '')
          .filter((valueText) => valueText !== '')
          .join(' / ');
      }
      return '';
    }

    function getMustLabel(mustValue) {
      return Number(mustValue) === 1 ? '是' : '否';
    }

    function toCamelSegment(segment) {
      if (!segment || segment.indexOf('_') === -1) {
        return segment || '';
      }
      return segment.replace(/_([a-zA-Z0-9])/g, (match, char) => char.toUpperCase());
    }

    function getDisplayUrl(url, clientKey) {
      const normalizedUrl = normalizeInterfacePath(url, clientKey);
      if (!normalizedUrl) {
        return '';
      }
      const segments = normalizedUrl.split('/');
      const lastIndex = segments.length - 1;
      return segments.map((segment, index) => {
        if (index === 0) {
          return segment;
        }
        if (index === lastIndex) {
          return segment;
        }
        return toCamelSegment(segment);
      }).join('/');
    }

    function getScalarExample(item) {
      const typeValue = Number(item.type);
      const mockValue = item.mock;
      if (typeValue === 1) {
        if (mockValue === '' || mockValue === null || mockValue === undefined) {
          return 0;
        }
        const numberValue = Number(mockValue);
        if (!Number.isNaN(numberValue)) {
          return numberValue;
        }
        return mockValue;
      }
      if (mockValue !== '' && mockValue !== null && mockValue !== undefined) {
        return mockValue;
      }
      if (typeValue === 0) {
        return '';
      }
      return null;
    }

    function buildExampleValue(item) {
      if (!item || typeof item !== 'object') {
        return null;
      }
      const typeValue = Number(item.type);
      const children = Array.isArray(item.data) ? item.data : [];
      if (typeValue === 4) {
        return buildExampleObject(children);
      }
      if (typeValue === 3) {
        if (!children.length) {
          return [];
        }
        const firstChild = children[0];
        if (firstChild && firstChild.name === null) {
          return [buildExampleValue(firstChild)];
        }
        return [buildExampleObject(children)];
      }
      return getScalarExample(item);
    }

    function buildExampleObject(params) {
      const result = {};
      if (!Array.isArray(params)) {
        return result;
      }
      params.forEach((item) => {
        if (!item || item.name === null || item.name === undefined || item.name === '') {
          return;
        }
        result[item.name] = buildExampleValue(item);
      });
      return result;
    }

    function buildResponseExample(outParam) {
      return JSON.stringify(buildExampleObject(outParam), null, 2);
    }

    function renderResponseFields(params, depth = 0, parentName = '') {
      if (!Array.isArray(params) || !params.length) {
        return '<div class="empty">无</div>';
      }

      const cards = params.map((item) => {
        const fieldName = item.name === null ? '(数组项)' : (item.name || '');
        const hasChildren = Array.isArray(item.data) && item.data.length;
        const nestedTitle = parentName
          ? parentName + '.' + fieldName + ' 字段说明'
          : fieldName + ' 字段说明';
        return `
          <div class="response-field-card">
            <div class="response-field-row">
              <div>
                <span class="response-col-label">字段</span>
                <div class="response-col-value"><code>${escapeHtml(fieldName)}</code></div>
              </div>
              <div>
                <span class="response-col-label">类型</span>
                <div class="response-col-value">${escapeHtml(getTypeLabel(item.type))}</div>
              </div>
              <div>
                <span class="response-col-label">必填</span>
                <div class="response-col-value">
                  <span class="response-required ${Number(item.must) === 1 ? '' : 'optional'}">
                    ${escapeHtml(getMustLabel(item.must))}
                  </span>
                </div>
              </div>
              <div>
                <span class="response-col-label">说明</span>
                <div class="response-col-value">${escapeHtml(item.remark || '')}</div>
              </div>
              <div>
                <span class="response-col-label">示例</span>
                <div class="response-col-value">${escapeHtml(item.mock || '')}</div>
              </div>
            </div>
            ${
              hasChildren
                ? '<div class="response-nested">' +
                  '<div class="response-nested-title">' + escapeHtml(nestedTitle) + '</div>' +
                  renderResponseFields(item.data, depth + 1, fieldName) +
                  '</div>'
                : ''
            }
          </div>
        `;
      }).join('');

      return '<div class="response-fields">' + cards + '</div>';
    }

    async function copyText(text) {
      if (navigator.clipboard && navigator.clipboard.writeText) {
        await navigator.clipboard.writeText(text);
        return;
      }
      const textArea = document.createElement('textarea');
      textArea.value = text;
      document.body.appendChild(textArea);
      textArea.select();
      document.execCommand('copy');
      document.body.removeChild(textArea);
    }

    function bindCopyButtons() {
      document.querySelectorAll('[data-copy-text]').forEach((button) => {
        button.addEventListener('click', async () => {
          const rawText = button.getAttribute('data-copy-text') || '';
          try {
            await copyText(rawText);
            const originalText = button.textContent;
            button.textContent = '已复制';
            setTimeout(() => {
              button.textContent = originalText;
            }, 1200);
          } catch (error) {
            button.textContent = '复制失败';
            setTimeout(() => {
              button.textContent = '复制返回结构';
            }, 1200);
          }
        });
      });
    }

    function renderInterface(item, index) {
      const param = Array.isArray(item.param) && item.param.length ? item.param[0] : {};
      const queryParam = param.queryParam || [];
      const bodyParam = param.bodyParam || [];
      const outParam = param.outParam || [];
      const clientKey = getClientKey(state.activeDoc, item);
      const debugUrl = buildDebugUrl(item.url || '', state.activeDoc, item);
      const displayUrl = getDisplayUrl(item.url || '', clientKey);
      const clientConfig = getClientConfig(clientKey);
      const responseExample = buildResponseExample(outParam);
      return `
        <section class="section-card" id="iface-${index}">
          <div class="section-top">
            <h3 class="section-title">${escapeHtml(item.name || '')}</h3>
            <div class="badges">
              <span class="badge method-${escapeHtml(item.method || 'GET')}">
                ${escapeHtml(item.method || '')}
              </span>
              <span class="badge url-badge">${escapeHtml(displayUrl)}</span>
              ${
                clientConfig.label
                  ? `<span class="badge">${escapeHtml(clientConfig.label)}</span>`
                  : ''
              }
              <a
                class="action-btn"
                href="${escapeHtml(debugUrl)}"
                target="_blank"
                rel="noopener noreferrer"
              >
                ${escapeHtml(getOpenButtonText())}
              </a>
            </div>
          </div>
          ${item.remark ? `<div class="footer-tip">${escapeHtml(item.remark)}</div>` : ''}
          <div class="sub-title">Query 参数</div>
          ${renderParamTable(queryParam)}
          <div class="sub-title">Body 参数</div>
          ${renderParamTable(bodyParam)}
          <div class="sub-title">返回结构</div>
          <div class="response-wrap">
            <div class="response-tabs">
              <span class="response-tab">200 成功响应</span>
            </div>
            <div class="response-meta">
              <span class="response-meta-badge">HTTP 状态码: 200</span>
              <span class="response-meta-badge">application/json</span>
            </div>
            <div class="response-doc-panel">
              <div class="response-panel-head">
                <div class="response-panel-title">字段说明</div>
              </div>
              ${renderResponseFields(outParam)}
            </div>
            <div class="json-preview">
              <div class="json-preview-head">
                <div class="json-preview-title">返回 JSON 示例</div>
                <button
                  class="copy-btn"
                  type="button"
                  data-copy-text="${escapeHtml(responseExample)}"
                >
                  复制返回结构
                </button>
              </div>
              <pre class="json-code">${escapeHtml(responseExample)}</pre>
            </div>
          </div>
        </section>
      `;
    }

    function renderDirectoryOverview() {
      const content = document.getElementById('content');
      const inArchive = isArchivePath(state.activeDir);
      const currentLabel = getDirLabel(state.activeDir);
      const dirCards = state.filteredDirs.map((dir) => `
            <div class="overview-card" data-dir-card="${escapeHtml(dir.path)}">
              <h3>${escapeHtml(dir.name)}</h3>
              <p>
                ${escapeHtml(dir.path)} · 接口数：${dir.iface_count || 0}
              </p>
            </div>
          `).join('');
      content.innerHTML = `
        <section class="hero">
          <h2>${escapeHtml(currentLabel)}</h2>
          <p>${
            inArchive
              ? '已归档文档。点需求目录查看该需求下的接口 json。'
              : state.activeDir
                ? '当前为子目录列表。点需求目录后查看接口文档。'
                : '下方为进行中的接口文档目录。已归档请点右上角「已归档」按钮。'
          }</p>
          <div class="stats">
            <span class="stat">目录数：${state.filteredDirs.length}</span>
            <span class="stat">本层文档：${state.filteredDocs.length}</span>
            ${!state.activeDir ? `<span class="stat">已归档接口：${getArchiveIfaceCount()}</span>` : ''}
          </div>
        </section>
        <div class="toolbar">
          <div class="count">共 ${state.filteredDirs.length} 个目录</div>
        </div>
        <div class="group-title">${inArchive ? '已归档需求' : '目录总览'}</div>
        ${dirCards ? `<div class="overview-grid">${dirCards}</div>` : '<div class="empty">没有匹配的目录</div>'}
      `;
      content.querySelectorAll('[data-dir-card]').forEach((card) => {
        card.addEventListener('click', () => openDirectory(card.dataset.dirCard || ''));
      });
    }

    function renderDoc() {
      const content = document.getElementById('content');
      const doc = state.activeDoc;
      if (!doc) {
        renderDirectoryOverview();
        return;
      }
      const interfaces = Array.isArray(doc.data) ? doc.data : [];
      content.innerHTML = `
        <section class="hero">
          <h2>${escapeHtml(doc.name || state.activeFile)}</h2>
          <p>当前展示的是 HFDoc JSON 文档内容。</p>
          <div class="stats">
            <span class="stat">目录：${escapeHtml(getDirLabel(state.activeDir))}</span>
            <span class="stat">文件：${escapeHtml(state.activeFile)}</span>
            <span class="stat">接口数：${interfaces.length}</span>
          </div>
        </section>
        <div class="toolbar">
          <div class="count">共 ${interfaces.length} 个接口</div>
        </div>
        ${
          interfaces.length
            ? interfaces.map((item, index) => renderInterface(item, index)).join('')
            : '<div class="empty">该文档没有接口数据</div>'
        }
      `;
      bindCopyButtons();
    }

    function scrollToInterface(index) {
      const target = document.getElementById('iface-' + index);
      if (!target) {
        return;
      }
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      target.classList.remove('highlight');
      void target.offsetWidth;
      target.classList.add('highlight');
    }

    async function openInterface(file, index) {
      state.activeIfaceIndex = index;
      if (state.activeFile !== file || !state.activeDoc) {
        await openDoc(file);
      } else {
        renderDocList();
      }
      requestAnimationFrame(() => scrollToInterface(index));
    }

    async function openDoc(file) {
      try {
        const docMeta = state.docs.find((item) => item.file === file);
        if (!docMeta) {
          throw new Error('未找到文档: ' + file);
        }
        state.activeDir = docMeta.dir || '';
        state.activeFile = file;
        state.activeDoc = null;
        applyFilters();
        renderDirList();
        renderDocList();
        setQueryState(state.activeDir, state.activeFile);
        document.getElementById('content').innerHTML =
          '<div class="loading">正在加载文档内容...</div>';
        state.activeDoc = await fetchJson('/api/doc?file=' + encodeURIComponent(file));
        renderDoc();
      } catch (error) {
        document.getElementById('content').innerHTML =
          '<div class="error">' + escapeHtml(error.message) + '</div>';
      }
    }

    function openDirectory(dirPath) {
      state.activeDir = dirPath || '';
      state.activeFile = '';
      state.activeDoc = null;
      state.activeIfaceIndex = -1;
      applyFilters();
      renderDirList();
      renderDocList();
      setQueryState(state.activeDir, '');
      // 有子目录：先展示目录总览（如 archive → 小对话）
      if (state.filteredDirs.length) {
        renderDirectoryOverview();
        return;
      }
      // 本层直接有 json：打开第一份
      if (state.filteredDocs.length) {
        openDoc(state.filteredDocs[0].file);
        return;
      }
      document.getElementById('content').innerHTML =
        '<div class="empty">当前目录下没有子目录或 json 文档</div>';
    }

    function bindSearch() {
      const input = document.getElementById('searchInput');
      input.addEventListener('input', () => {
        state.searchKeyword = input.value || '';
        applyFilters();
        renderDirList();
        renderDocList();
        if (state.activeDoc) {
          renderDoc();
        } else {
          renderDirectoryOverview();
        }
      });
      const archiveBtn = document.getElementById('archiveEntry');
      if (archiveBtn) {
        archiveBtn.addEventListener('click', () => {
          openDirectory(ARCHIVE_ROOT);
        });
      }
    }

    async function init() {
      try {
        const meta = await fetchJson('/api/meta');
        state.docs = Array.isArray(meta.docs) ? meta.docs : [];
        state.dirs = Array.isArray(meta.dirs) ? meta.dirs : [];
        state.config = meta.config || {};
        applyViewerConfig();
        bindSearch();
        const query = getQueryState();
        if (query.file) {
          const docMeta = state.docs.find((doc) => doc.file === query.file);
          if (docMeta) {
            state.activeDir = query.dir || docMeta.dir || '';
            applyFilters();
            renderDirList();
            renderDocList();
            await openDoc(query.file);
            return;
          }
        }
        state.activeDir = query.dir || '';
        applyFilters();
        renderDirList();
        renderDocList();
        if (state.activeDir) {
          if (state.filteredDirs.length) {
            renderDirectoryOverview();
            return;
          }
          if (state.filteredDocs.length) {
            await openDoc(state.filteredDocs[0].file);
            return;
          }
          document.getElementById('content').innerHTML =
            '<div class="empty">当前目录下没有子目录或 json 文档</div>';
          return;
        }
        renderDirectoryOverview();
      } catch (error) {
        document.getElementById('content').innerHTML =
          '<div class="error">' + escapeHtml(error.message) + '</div>';
      }
    }

    init();
  </script>
</body>
</html>
"""


def doc_in_dir(doc_item, dir_path):
    doc_dir = doc_item.get("dir", "")
    if not dir_path:
        return True
    return doc_dir == dir_path or doc_dir.startswith(dir_path + "/")


def list_doc_files():
    files = []
    for path in sorted(DOC_ROOT.rglob("*.json")):
        if path.name.startswith("."):
            continue
        if path.name == CONFIG_FILE.name:
            continue
        if "__pycache__" in path.parts:
            continue
        rel_path = path.relative_to(DOC_ROOT).as_posix()
        rel_dir = path.parent.relative_to(DOC_ROOT).as_posix()
        if rel_dir == ".":
            rel_dir = ""
        interfaces = []
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
            name = data.get("name") or path.stem
            hfdoc_meta = data.get("_hfdoc")
            if not isinstance(hfdoc_meta, dict):
                hfdoc_meta = {}
            doc_data = data.get("data")
            if isinstance(doc_data, list):
                for idx, iface in enumerate(doc_data):
                    if not isinstance(iface, dict):
                        continue
                    interfaces.append(
                        {
                            "index": idx,
                            "name": iface.get("name") or "",
                            "method": iface.get("method") or "",
                            "url": iface.get("url") or "",
                        }
                    )
        except Exception:
            name = path.stem
            hfdoc_meta = {}
        files.append(
            {
                "file": rel_path,
                "name": name,
                "dir": rel_dir,
                "interfaces": interfaces,
                "hfdoc": hfdoc_meta,
            }
        )
    return files


def list_directories(docs):
    dir_map = {}
    for path in sorted(DOC_ROOT.rglob("*")):
        if not path.is_dir():
            continue
        if path.name.startswith(".") or path.name == "__pycache__":
            continue
        rel_path = path.relative_to(DOC_ROOT).as_posix()
        dir_map[rel_path] = {
            "path": rel_path,
            "name": path.name,
            "depth": len(path.relative_to(DOC_ROOT).parts),
        }
    dirs = []
    for item in dir_map.values():
        matched = [doc for doc in docs if doc_in_dir(doc, item["path"])]
        item["doc_count"] = len(matched)
        item["iface_count"] = sum(
            len(doc.get("interfaces") or []) for doc in matched
        )
        dirs.append(item)
    dirs.sort(key=lambda item: (item["depth"], item["path"]))
    return dirs


def deep_merge_dict(base, extra):
    result = dict(base)
    for key, value in extra.items():
        if (
            key in result
            and isinstance(result[key], dict)
            and isinstance(value, dict)
        ):
            result[key] = deep_merge_dict(result[key], value)
        else:
            result[key] = value
    return result


def load_viewer_config():
    config = DEFAULT_VIEWER_CONFIG
    if not CONFIG_FILE.is_file():
        return config
    try:
        user_config = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
    except Exception:
        return config
    if not isinstance(user_config, dict):
        return config
    return deep_merge_dict(config, user_config)


def build_meta():
    docs = list_doc_files()
    dirs = list_directories(docs)
    return {
        "docs": docs,
        "dirs": dirs,
        "config": load_viewer_config(),
    }


def safe_doc_path(file_name):
    if not file_name:
        return None
    target = (DOC_ROOT / unquote(file_name)).resolve()
    if not str(target).startswith(str(DOC_ROOT.resolve())):
        return None
    if not target.is_file() or target.suffix.lower() != ".json":
        return None
    return target


class HFDocHandler(BaseHTTPRequestHandler):
    server_version = "HFDocViewer/2.0"

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/":
            return self.send_html(HTML_PAGE)
        if parsed.path == "/api/meta":
            return self.send_json(build_meta())
        if parsed.path == "/api/doc":
            query = parse_qs(parsed.query)
            file_name = query.get("file", [""])[0]
            file_path = safe_doc_path(file_name)
            if file_path is None:
                return self.send_error_json(
                    HTTPStatus.BAD_REQUEST,
                    "无效的文件路径",
                )
            try:
                content = json.loads(file_path.read_text(encoding="utf-8"))
            except Exception as exc:
                return self.send_error_json(
                    HTTPStatus.INTERNAL_SERVER_ERROR,
                    "读取 json 失败: %s" % exc,
                )
            return self.send_json(content)
        return self.send_error_json(HTTPStatus.NOT_FOUND, "接口不存在")

    def log_message(self, fmt, *args):
        return

    def send_html(self, html):
        data = html.encode("utf-8")
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def send_error_json(self, status, message):
        self.send_json({"error": message, "status": int(status)}, status=status)


def parse_args():
    parser = argparse.ArgumentParser(
        description="启动本地 HFDoc JSON 文档查看器"
    )
    parser.add_argument(
        "--host",
        default="127.0.0.1",
        help="监听地址，默认 127.0.0.1",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8000,
        help="监听端口，默认 8000",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    server = ThreadingHTTPServer((args.host, args.port), HFDocHandler)
    print("HFDoc Viewer 已启动")
    print("文档目录: %s" % DOC_ROOT)
    print("访问地址: http://%s:%s" % (args.host, args.port))
    print("目录筛选示例: http://%s:%s/?dir=%s" % (args.host, args.port, "小对话"))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()


if __name__ == "__main__":
    main()
