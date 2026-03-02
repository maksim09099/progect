function readNum(form, name) {
  return Number(form.elements[name].value);
}

function calcIol({ k1, k2, acd, al, aConst }) {
  const meanK = (k1 + k2) / 2;
  const srk = aConst - 2.5 * al - 0.9 * meanK;

  const a0 = 1.0;
  const a1 = 0.4;
  const a2 = 0.1;
  const elp = a0 + a1 * acd + a2 * al;
  const haigis = 1000 / (al - elp) - meanK;

  return {
    srk: Number(srk.toFixed(2)),
    haigis: Number(haigis.toFixed(2)),
    recommended: Number((((srk + haigis) / 2).toFixed(2))),
  };
}

const iolForm = document.getElementById("iolForm");
const iolResult = document.getElementById("iolResult");

iolForm?.addEventListener("submit", (event) => {
  event.preventDefault();
  const values = {
    k1: readNum(iolForm, "k1"),
    k2: readNum(iolForm, "k2"),
    acd: readNum(iolForm, "acd"),
    al: readNum(iolForm, "al"),
    aConst: readNum(iolForm, "aConst"),
  };

  const { srk, haigis, recommended } = calcIol(values);
  iolResult.innerHTML = `
    <h3>Рекомендация</h3>
    <p><strong>SRK/T‑like:</strong> ${srk} D</p>
    <p><strong>Haigis‑like:</strong> ${haigis} D</p>
    <p><strong>Итоговая рекомендация:</strong> <span class="pill pill--green">${recommended} D</span></p>
    <small>Демо‑расчет для прототипа. Для клинического применения требуется валидация и сертифицированный калькулятор.</small>
  `;
});

const checklistForm = document.getElementById("checklistForm");
const checklistResult = document.getElementById("checklistResult");
const saveDraftBtn = document.getElementById("saveDraft");
const validateBtn = document.getElementById("validateChecklist");
const DRAFT_KEY = "okulus_checklist_draft";

function checklistState(form) {
  return {
    blood: form.elements.blood.checked,
    ecg: form.elements.ecg.checked,
    fluoro: form.elements.fluoro.checked,
    therapist: form.elements.therapist.checked,
    culture: form.elements.culture.checked,
    iolDate: form.elements.iolDate.value,
  };
}

function applyDraft(form, draft) {
  if (!draft) return;
  form.elements.blood.checked = Boolean(draft.blood);
  form.elements.ecg.checked = Boolean(draft.ecg);
  form.elements.fluoro.checked = Boolean(draft.fluoro);
  form.elements.therapist.checked = Boolean(draft.therapist);
  form.elements.culture.checked = Boolean(draft.culture);
  form.elements.iolDate.value = draft.iolDate || "";
}

saveDraftBtn?.addEventListener("click", () => {
  const state = checklistState(checklistForm);
  localStorage.setItem(DRAFT_KEY, JSON.stringify(state));
  checklistResult.innerHTML = '<h3>Результат проверки</h3><p><span class="pill pill--yellow">Черновик сохранен локально</span></p>';
});

validateBtn?.addEventListener("click", () => {
  const state = checklistState(checklistForm);
  const requiredDone = [state.blood, state.ecg, state.fluoro, state.therapist, state.culture, Boolean(state.iolDate)].every(Boolean);

  if (requiredDone) {
    checklistResult.innerHTML = '<h3>Результат проверки</h3><p><span class="pill pill--green">Пациент готов к отправке хирургу</span></p>';
  } else {
    checklistResult.innerHTML = '<h3>Результат проверки</h3><p><span class="pill pill--red">Не хватает обязательных пунктов</span></p>';
  }
});

try {
  const draftRaw = localStorage.getItem(DRAFT_KEY);
  if (draftRaw && checklistForm) {
    applyDraft(checklistForm, JSON.parse(draftRaw));
  }
} catch (error) {
  console.warn("Не удалось восстановить черновик:", error);
}

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("sw.js").catch((error) => {
      console.warn("Service worker registration failed:", error);
    });
  });
}
