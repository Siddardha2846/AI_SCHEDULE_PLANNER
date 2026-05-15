import { generateSchedule } from "../api/api.js";
import { SubjectRow } from "../components/SubjectRow.js";
import { ScheduleCard } from "../components/ScheduleCard.js";

const { createElement: h, useState } = React;

export function HomePage() {
  const [startTime, setStartTime] = useState("09:00");
  const [endTime, setEndTime] = useState("16:00");
  const [breakDuration, setBreakDuration] = useState(10);
  const [subjects, setSubjects] = useState([{ name: "", proficiency: 3 }]);
  const [schedule, setSchedule] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const updateSubject = (index, field, value) => {
    const newSubjects = [...subjects];
    newSubjects[index][field] = value;
    setSubjects(newSubjects);
  };

  const addSubject = () => {
    setSubjects([...subjects, { name: "", proficiency: 3 }]);
  };

  const removeSubject = (index) => {
    const newSubjects = [...subjects];
    newSubjects.splice(index, 1);
    setSubjects(newSubjects);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    // Validate
    const validSubjects = subjects.filter(s => s.name.trim() !== "");
    if (validSubjects.length === 0) {
      setError("Please add at least one subject.");
      return;
    }

    setLoading(true);
    try {
      const data = await generateSchedule({
        start_time: startTime,
        end_time: endTime,
        break_duration: breakDuration,
        subjects: validSubjects
      });
      setSchedule(data);
    } catch (err) {
      setError(err.message || "Failed to generate schedule.");
    } finally {
      setLoading(false);
    }
  };

  const reset = () => {
    setSchedule(null);
    setError("");
  };

  if (schedule) {
    return h(
      "div",
      { className: "min-h-screen" },
      h(
        "header",
        { className: "bg-white shadow-sm border-b sticky top-0 z-10" },
        h(
          "div",
          { className: "max-w-3xl mx-auto px-4 py-3 flex items-center gap-2" },
          h("div", { className: "bg-sky-500 p-1.5 rounded-lg text-white" }, "📅"),
          h("span", { className: "font-semibold text-slate-800" }, "AI Personalized Study Scheduler")
        )
      ),
      h(
        "main",
        { className: "max-w-3xl mx-auto px-4 py-8 fade-in" },
        h(
          "div",
          { className: "flex flex-col sm:flex-row justify-between items-start sm:items-center mb-8 gap-3" },
          h(
            "div",
            null,
            h("h2", { className: "text-2xl font-bold text-slate-800" }, "Your Study Plan"),
            h("p", { className: "text-slate-500 text-sm mt-1" }, `${startTime} to ${endTime}`)
          ),
          h(
            "button",
            { onClick: reset, className: "flex items-center gap-1.5 px-4 py-2 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-sm font-medium shadow-sm transition-colors" },
            "🔄 Plan Another Day"
          )
        ),
        schedule.length === 0 && h("p", { className: "text-slate-500" }, "No schedule could be generated for the given parameters."),
        h(
          "div",
          { className: "relative pl-6 md:pl-10" },
          schedule.map((item, idx) => h(ScheduleCard, { key: idx, item }))
        )
      )
    );
  }

  return h(
    "div",
    { className: "min-h-screen flex flex-col" },
    h(
      "header",
      { className: "bg-white shadow-sm border-b" },
      h(
        "div",
        { className: "max-w-3xl mx-auto px-4 py-3 flex items-center gap-2" },
        h("div", { className: "bg-sky-500 p-1.5 rounded-lg text-white" }, "📅"),
        h("span", { className: "font-semibold text-slate-800" }, "AI Personalized Study Scheduler")
      )
    ),
    h(
      "main",
      { className: "flex-1 flex items-start justify-center px-4 py-12" },
      h(
        "div",
        { className: "w-full max-w-xl" },
        h(
          "div",
          { className: "bg-white rounded-2xl border border-slate-200 shadow-sm overflow-hidden" },
          h(
            "div",
            { className: "bg-slate-50 border-b border-slate-100 px-6 py-5" },
            h("h2", { className: "font-semibold text-slate-800 flex items-center gap-2 text-lg" }, "✨ Create Your Study Plan"),
            h("p", { className: "text-slate-500 text-sm mt-1" }, "Enter your available time and subjects. We'll balance it optimally.")
          ),
          h(
            "form",
            { onSubmit: handleSubmit, className: "p-6" },
            
            // Time Range
            h(
              "div",
              { className: "grid grid-cols-2 gap-4 mb-6" },
              h(
                "div",
                null,
                h("label", { className: "block text-sm font-semibold text-slate-700 mb-1" }, "Start Time"),
                h("input", { type: "time", value: startTime, onChange: e => setStartTime(e.target.value), className: "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-400 outline-none", required: true })
              ),
              h(
                "div",
                null,
                h("label", { className: "block text-sm font-semibold text-slate-700 mb-1" }, "End Time"),
                h("input", { type: "time", value: endTime, onChange: e => setEndTime(e.target.value), className: "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-400 outline-none", required: true })
              )
            ),
            
            // Preferences
            h(
              "div",
              { className: "mb-6" },
              h("label", { className: "block text-sm font-semibold text-slate-700 mb-1" }, "Break Duration (mins)"),
              h("input", { type: "number", min: 0, max: 60, value: breakDuration, onChange: e => setBreakDuration(parseInt(e.target.value, 10)), className: "w-full px-3 py-2 border border-slate-300 rounded-lg text-sm focus:ring-2 focus:ring-sky-400 outline-none" })
            ),

            // Subjects
            h(
              "div",
              { className: "mb-6" },
              h("h3", { className: "text-sm font-semibold text-slate-700 mb-3 border-b pb-2" }, "Subjects"),
              subjects.map((sub, idx) => h(SubjectRow, { 
                key: idx, 
                index: idx, 
                subject: sub, 
                updateSubject, 
                removeSubject,
                canRemove: subjects.length > 1
              })),
              h(
                "button",
                { type: "button", onClick: addSubject, className: "text-sky-600 text-sm font-semibold hover:text-sky-700 flex items-center gap-1 mt-2" },
                "+ Add another subject"
              )
            ),

            error && h(
              "div",
              { className: "mb-6 p-3 bg-red-50 text-red-700 rounded-lg flex items-start gap-2 text-sm border border-red-100" },
              h("span", null, error)
            ),

            h(
              "div",
              { className: "flex justify-end pt-4 border-t" },
              h(
                "button",
                { type: "submit", disabled: loading, className: "px-6 py-2.5 bg-sky-600 hover:bg-sky-700 text-white rounded-lg font-medium text-sm flex items-center gap-2 disabled:opacity-60 disabled:cursor-not-allowed transition-colors shadow-sm" },
                loading ? "Generating..." : "✨ Generate Schedule"
              )
            )
          )
        )
      )
    )
  );
}
