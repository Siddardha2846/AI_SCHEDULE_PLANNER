export async function generateSchedule(data) {
  const res = await fetch("/generate-schedule", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  
  if (!res.ok) {
    let errStr = `API error ${res.status}: ${res.statusText}`;
    try {
      const errData = await res.json();
      if (errData.detail) errStr = errData.detail;
    } catch (e) {}
    throw new Error(errStr);
  }
  
  return await res.json();
}
