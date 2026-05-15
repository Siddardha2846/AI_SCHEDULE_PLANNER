const { createElement: h } = React;

export function SubjectRow({ subject, index, updateSubject, removeSubject, canRemove }) {
  return h(
    "div",
    { className: "flex items-center gap-3 mb-3 bg-slate-50 p-3 rounded-xl border border-slate-200" },
    h(
      "div",
      { className: "flex-1" },
      h("label", { className: "block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider" }, `Subject ${index + 1}`),
      h("input", {
        type: "text",
        value: subject.name,
        onChange: (e) => updateSubject(index, "name", e.target.value),
        placeholder: "e.g., DBMS",
        className: "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-400 outline-none transition-all",
        required: true
      })
    ),
    h(
      "div",
      { className: "w-32" },
      h("label", { className: "block text-xs font-semibold text-slate-500 mb-1 uppercase tracking-wider" }, "Proficiency"),
      h(
        "select",
        {
          value: subject.proficiency,
          onChange: (e) => updateSubject(index, "proficiency", parseInt(e.target.value, 10)),
          className: "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm bg-white focus:ring-2 focus:ring-sky-400 outline-none transition-all"
        },
        [1, 2, 3, 4, 5].map(level => h("option", { key: level, value: level }, `${level} / 5`))
      )
    ),
    canRemove && h(
      "button",
      {
        type: "button",
        onClick: () => removeSubject(index),
        className: "mt-5 p-2 text-red-500 hover:bg-red-50 rounded-lg transition-colors",
        title: "Remove Subject"
      },
      h(
        "svg",
        { width: 18, height: 18, viewBox: "0 0 24 24", fill: "none", stroke: "currentColor", strokeWidth: "2", strokeLinecap: "round", strokeLinejoin: "round" },
        h("path", { d: "M18 6 6 18" }),
        h("path", { d: "m6 6 12 12" })
      )
    )
  );
}
