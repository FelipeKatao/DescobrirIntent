/* global Vue, ApiClient */

(function () {
  const { createApp, nextTick } = Vue;

  function normalizeFields(fieldValue) {
    if (!fieldValue) return [];
    if (Array.isArray(fieldValue)) return fieldValue.map(String);
    // backend hoje parece mandar string tipo "['a','b']"
    return String(fieldValue)
      .replaceAll("[", "")
      .replaceAll("]", "")
      .split(",")
      .map((s) => s.replaceAll("'", "").trim())
      .filter(Boolean);
  }

  function makeId(prefix) {
    return `${prefix}_${Math.random().toString(16).slice(2)}_${Date.now()}`;
  }

  createApp({
    data() {
      return {
        ui: {
          sidebarCollapsed: false,
          loginModalOpen: false,
        },
        auth: {
          username: "",
          password: "",
          loading: false,
        },
        dropdown: {
          chatId: null,
        },
        editing: {
          chatId: null,
          draft: "",
        },
        renameInputRefs: new Map(),
        chats: [],
        activeChatId: null,
        composer: {
          text: "",
          loading: false,
        },
      };
    },

    computed: {
      activeChat() {
        return this.chats.find((c) => c.id === this.activeChatId) || null;
      },
    },

    methods: {
      setRenameInputRef(chatId) {
        return (el) => {
          if (!el) {
            this.renameInputRefs.delete(chatId);
            return;
          }
          this.renameInputRefs.set(chatId, el);
        };
      },

      hideDropdowns() {
        this.dropdown.chatId = null;
      },

      toggleDropdown(chatId) {
        this.dropdown.chatId = this.dropdown.chatId === chatId ? null : chatId;
      },

      toggleSidebar() {
        this.ui.sidebarCollapsed = !this.ui.sidebarCollapsed;
        document.body.classList.toggle("sidebar-collapsed", this.ui.sidebarCollapsed);
      },

      createNewChat(name) {
        const id = makeId("chat");
        const chat = {
          id,
          name: name && String(name).trim() ? String(name).trim() : `ChatBot${String(this.chats.length + 1).padStart(2, "0")}`,
          isFirst: true,
          messages: [],
        };
        this.chats.unshift(chat);
        this.switchToChat(chat.id);
      },

      switchToChat(chatId) {
        this.hideDropdowns();
        this.editing.chatId = null;
        this.activeChatId = chatId;
        this.scrollToBottomSoon();
      },

      startRename(chatId) {
        const chat = this.chats.find((c) => c.id === chatId);
        if (!chat) return;
        this.hideDropdowns();
        this.editing.chatId = chatId;
        this.editing.draft = chat.name;
        nextTick(() => {
          const el = this.renameInputRefs.get(chatId);
          if (el) {
            el.focus();
            el.select?.();
          }
        });
      },

      cancelRename() {
        this.editing.chatId = null;
        this.editing.draft = "";
      },

      commitRename() {
        const chatId = this.editing.chatId;
        if (!chatId) return;
        const chat = this.chats.find((c) => c.id === chatId);
        const nextName = String(this.editing.draft || "").trim();
        if (chat && nextName) chat.name = nextName;
        this.cancelRename();
      },

      deleteChat(chatId) {
        if (this.chats.length <= 1) {
          alert("Não é possível excluir o último chat!");
          return;
        }
        if (!confirm("Tem certeza que deseja excluir este chat?")) return;

        this.hideDropdowns();
        const idx = this.chats.findIndex((c) => c.id === chatId);
        if (idx === -1) return;
        const wasActive = this.activeChatId === chatId;
        this.chats.splice(idx, 1);
        if (wasActive) {
          this.activeChatId = this.chats[0]?.id ?? null;
        }
      },

      focusPassword() {
        document.getElementById("password")?.focus();
      },

      async bootSecurity() {
        try {
          const cfg = await ApiClient.readConfig();
          if (cfg && cfg.security_enabled === true) {
            this.ui.loginModalOpen = true;
          }
        } catch (e) {
          // se backend não estiver no ar, não trava a UI
          console.warn("Falha ao ler config:", e);
        }
      },

      async login() {
        if (this.auth.loading) return;
        if (!this.auth.username.trim() || !this.auth.password) {
          alert("Por favor, preencha todos os campos!");
          return;
        }
        this.auth.loading = true;
        try {
          const res = await ApiClient.loginSession(this.auth.password, this.auth.username);
          if (res && res.success === true) {
            this.ui.loginModalOpen = false;
            this.auth.password = "";
          } else {
            alert("Login ou senha incorretos");
          }
        } catch (e) {
          console.error(e);
          alert("Não foi possível efetuar login (API offline?)");
        } finally {
          this.auth.loading = false;
        }
      },

      scrollToBottomSoon() {
        nextTick(() => {
          const viewport = this.$refs.messagesViewport;
          if (!viewport) return;
          viewport.scrollTop = viewport.scrollHeight;
        });
      },

      async sendMessage() {
        if (!this.activeChat) return;
        const text = String(this.composer.text || "").trim();
        if (!text || this.composer.loading) return;

        const chat = this.activeChat;
        chat.isFirst = false;
        chat.messages.push({ role: "user", text });
        this.composer.text = "";
        this.composer.loading = true;
        this.scrollToBottomSoon();

        try {
          const data = await ApiClient.sendMessage(text);

          const wantsForm = data?.Config?.FormResponse === "true" || data?.Config?.FormResponse === true;
          if (wantsForm) {
            const fields = normalizeFields(data?.Field);
            const form = {};
            fields.forEach((f) => (form[f] = ""));
            chat.messages.push({
              role: "bot",
              type: "form",
              fields,
              form,
              submitting: false,
              submitted: false,
              idname: "base",
            });
          } else {
            chat.messages.push({
              role: "bot",
              type: "html",
              html: String(data?.Response ?? ""),
            });
          }
        } catch (e) {
          console.error("Erro ao chamar API:", e);
          chat.messages.push({
            role: "bot",
            type: "html",
            html: "Erro ao chamar API. Verifique se o backend está rodando.",
          });
        } finally {
          this.composer.loading = false;
          this.scrollToBottomSoon();
        }
      },

      async submitForm(message) {
        if (!this.activeChat || !message || message.submitting || message.submitted) return;
        message.submitting = true;
        try {
          const res = await ApiClient.sendForm(message.idname || "base", message.form || {});
          message.submitted = true;

          const resp = res?.Response;
          let html = "";
          if (Array.isArray(resp) && resp.length > 1 && typeof resp[1] === "string") {
            html = String(resp[1]).split(":").slice(1).join(":").replaceAll("\"", "").trim();
          } else if (typeof resp === "string") {
            html = resp;
          } else {
            html = "Form enviado.";
          }

          this.activeChat.messages.push({ role: "bot", type: "html", html });
        } catch (e) {
          console.error(e);
          this.activeChat.messages.push({
            role: "bot",
            type: "html",
            html: "Erro ao enviar formulário.",
          });
        } finally {
          message.submitting = false;
          this.scrollToBottomSoon();
        }
      },
    },

    async mounted() {
      document.body.classList.toggle("sidebar-collapsed", this.ui.sidebarCollapsed);

      // fechar dropdown ao clicar fora
      document.addEventListener("click", (e) => {
        if (!e.target.closest(".chat-item")) this.hideDropdowns();
      });

      this.createNewChat("ChatBot01");
      await this.bootSecurity();
    },
  }).mount("#app");
})();

