"use strict";

const ui = Object.fromEntries(["reports", "connection", "target", "title", "kind", "source", "raw", "body"].map(id => [id, document.getElementById(id)]));
let reports = [];
let selected = new URLSearchParams(location.search).get("report");
let rendered = "";
let navigation = "";
let collectionCurrent = false;

function fileUrl(path) {
  return "/files/" + path.split("/").map(encodeURIComponent).join("/");
}

function notice(text, error = false) {
  if (ui.connection.textContent !== text) ui.connection.textContent = text;
  ui.connection.classList.toggle("error", error);
}

function render() {
  const report = reports.find(item => item.id === selected) || reports[0];
  selected = report.id;
  const tabs = JSON.stringify(reports.map(({id, title, kind}) => ({id, title, kind})));
  if (tabs !== navigation) {
    ui.reports.replaceChildren(...reports.map(item => {
      const button = document.createElement("button");
      button.className = "draft-tab";
      const type = document.createElement("small");
      type.textContent = item.kind === "pr" ? "PULL REQUEST" : "ISSUE";
      const title = document.createElement("strong");
      title.textContent = item.title;
      button.append(type, title);
      button.dataset.report = item.id;
      button.onclick = () => { selected = item.id; render(); };
      return button;
    }));
    navigation = tabs;
  }
  for (const tab of ui.reports.children) {
    if (tab.dataset.report === selected) tab.setAttribute("aria-current", "page");
    else tab.removeAttribute("aria-current");
  }
  const url = new URL(location.href);
  url.searchParams.set("report", selected);
  history.replaceState(null, "", url);
  const fingerprint = JSON.stringify(report);
  if (fingerprint !== rendered) {
    ui.title.textContent = report.title;
    document.title = `${report.title} · Draft review`;
    ui.target.textContent = report.target;
    ui.kind.textContent = report.kind === "pr" ? "Draft pull request" : "Draft issue";
    ui.raw.hidden = Boolean(report.error);
    ui.raw.href = fileUrl(report.path);
    ui.raw.target = "_blank";
    ui.raw.rel = "noopener noreferrer";
    ui.source.textContent = report.error ? report.path : `${report.path} · ${report.revision.slice(0, 12)}`;
    ui.body.dataset.source = report.path;
    if (report.error) {
      ui.body.textContent = report.error;
      delete ui.body.dataset.revision;
    } else {
      const html = marked.parse(report.markdown, {gfm: true, breaks: true});
      const fragment = DOMPurify.sanitize(html, {
        RETURN_DOM_FRAGMENT: true,
        USE_PROFILES: {html: true},
        FORBID_TAGS: ["style", "form", "iframe", "object", "embed"],
        FORBID_ATTR: ["style", "srcset", "autoplay"],
        SANITIZE_NAMED_PROPS: true,
      });
      const base = new URL(fileUrl(report.path), location.origin);
      for (const element of fragment.querySelectorAll("[href], [src], [poster]")) {
        for (const attribute of ["href", "src", "poster"]) {
          const value = element.getAttribute(attribute);
          if (!value || value.startsWith("#")) continue;
          const resolved = new URL(value, base);
          if (!["http:", "https:"].includes(resolved.protocol) && !(attribute === "src" && /^data:image\/(png|jpeg|gif|webp);base64,/i.test(value))) {
            element.removeAttribute(attribute);
            continue;
          }
          element.setAttribute(attribute, resolved.href);
        }
        if (element.tagName === "A") {
          element.target = "_blank";
          element.rel = "noopener noreferrer";
        }
      }
      // A direct video attachment link gets a player; the canonical Markdown remains untouched.
      for (const link of fragment.querySelectorAll("a[href]")) {
        if (/\.(mp4|webm|mov)(?:[?#]|$)/i.test(link.href)) {
          const video = document.createElement("video");
          video.controls = true;
          video.preload = "metadata";
          video.src = link.href;
          video.setAttribute("aria-label", link.textContent || "Video evidence");
          link.after(video);
        }
      }
      for (const video of fragment.querySelectorAll("video")) { video.controls = true; video.preload = "metadata"; }
      ui.body.replaceChildren(fragment);
      ui.body.dataset.revision = report.revision;
    }
    rendered = fingerprint;
  }
  if (!collectionCurrent) notice("Draft connection unavailable — preview may be stale", true);
  else notice(report.error ? "Source unavailable — preview is not current" : "Synced with Markdown · unpublished", Boolean(report.error));
}

async function refresh() {
  try {
    const response = await fetch("/api/reports", {cache: "no-store"});
    if (!response.ok) throw new Error("Cannot read drafts — check the collection manifest");
    const data = await response.json();
    reports = data.reports;
    if (!collectionCurrent) rendered = "";
    collectionCurrent = true;
    render();
  } catch (error) {
    collectionCurrent = false;
    notice(`${error.message}. Preview may be stale.`, true);
  } finally {
    setTimeout(refresh, 1200);
  }
}

if (!window.marked || !window.DOMPurify) {
  notice("Markdown renderer unavailable. Check CDN access and reload; no rendered preview is available.", true);
} else {
  refresh();
}
