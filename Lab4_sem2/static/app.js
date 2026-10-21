// Вкладки и построение дерева

document.addEventListener("DOMContentLoaded", () => {
  // --- вкладки ---
  document.querySelectorAll(".tab").forEach(btn => {
    btn.addEventListener("click", () => {
      document.querySelectorAll(".tab").forEach(t => t.classList.remove("active"));
      document.querySelectorAll(".tab-panel").forEach(p => p.classList.remove("active"));
      btn.classList.add("active");
      const panel = document.getElementById("panel-" + btn.dataset.tab);
      if (panel) panel.classList.add("active");
    });
  });

  // --- синтаксическое дерево ---
  const btnTree = document.getElementById("btn-tree");
  if (btnTree) {
    btnTree.addEventListener("click", async () => {
      const sel = document.getElementById("sentence");
      const out = document.getElementById("tree-out");
      const msg = document.getElementById("tree-msg");
      if (!sel || !out) return;

      const sentence = sel.value;
      out.textContent = "Строю дерево…";
      msg.textContent = "";

      try {
        const form = new FormData();
        form.append("sentence", sentence);
        const resp = await fetch("/tree", { method: "POST", body: form });
        const data = await resp.json();
        out.textContent = data.tree || "(пусто)";
        msg.textContent = data.msg || "";
      } catch (e) {
        out.textContent = "Не удалось построить дерево.";
        msg.textContent = String(e);
      }
    });
  }
});
