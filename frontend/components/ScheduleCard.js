const { createElement: h } = React;

export function ScheduleCard({ item }) {
  const isBreak = item.slot_type === "break";

  const typeStyle = isBreak 
    ? "bg-amber-50 border-amber-200 text-amber-800" 
    : "bg-sky-50 border-sky-200 text-sky-900";
    
  const icon = isBreak ? "☕" : "📚";

  return h(
    "div",
    { className: "relative timeline-item pb-6" },
    h("div", { className: "timeline-line" }),
    h(
      "div",
      { className: "flex items-start gap-3 md:gap-5 relative z-10" },
      h(
        "div",
        { className: "w-16 md:w-20 shrink-0 text-right mt-1" },
        h("div", { className: "text-sm font-bold text-slate-700" }, item.start_time),
        h("div", { className: "text-xs text-slate-400" }, item.end_time)
      ),
      h("div", { className: `w-3 h-3 rounded-full mt-2 shrink-0 border-2 border-white shadow ${isBreak ? 'bg-amber-500' : 'bg-sky-500'}` }),
      h(
        "div",
        { className: `flex-1 rounded-xl border p-4 hover:-translate-y-0.5 transition-transform duration-200 ${typeStyle}` },
        h(
          "div",
          { className: "flex justify-between items-start gap-2 mb-1" },
          h("span", { className: "font-bold text-sm flex items-center gap-2" }, icon, item.subject),
          h("span", { className: `text-xs px-2 py-0.5 rounded-full font-semibold uppercase tracking-wide bg-white/60` }, item.slot_type)
        ),
        h("p", { className: "text-sm font-medium mt-2" }, item.topic),
        h(
          "p",
          { className: "text-xs opacity-80 flex items-start gap-1 mt-2" },
          h("span", { className: "font-semibold" }, "Note:"),
          item.notes
        )
      )
    )
  );
}
