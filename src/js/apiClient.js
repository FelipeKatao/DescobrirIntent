/**
 * Integração central com a API (mantido como global para compatibilidade
 * com o front estático atual, sem bundler).
 */
window.ApiClient = (function () {
  const BASE_URL = "http://127.0.0.1:5000";

  async function requestJson(path, options) {
    const res = await fetch(BASE_URL + path, options);
    if (!res.ok) {
      const text = await res.text().catch(() => "");
      throw new Error(`HTTP ${res.status} ${res.statusText} - ${text}`);
    }
    return await res.json();
  }

  function encodePathSegment(value) {
    return encodeURIComponent(String(value ?? ""));
  }

  return {
    async readConfig() {
      return await requestJson("/config/get", { method: "GET" });
    },

    async loginSession(password, username) {
      return await requestJson(
        `/config/security/${encodePathSegment(password)}/${encodePathSegment(username)}`,
        { method: "POST" }
      );
    },

    async sendMessage(message) {
      return await requestJson(`/sendmensage/API/${encodePathSegment(message)}`, {
        method: "GET",
      });
    },

    async sendForm(idname, payload) {
      return await requestJson(`/forms/send?data=${encodePathSegment(idname)}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload ?? {}),
      });
    },
  };
})();

