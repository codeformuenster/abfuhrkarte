{% if include_leaflet %}import abfuhrmap from '/map.js';{% endif %}

const hidePastDates = () => {
  const now = new Date();
  let today = now.getTime();
  today = today - (today % 86400000);

  const thisMonth = new Date(now.toISOString().slice(0, 7)).getTime();

  for (const dateLink of document.querySelectorAll("li[data-date]")) {
    const linkDate = new Date(dateLink.dataset.date).getTime();
    if (today > linkDate) {
      dateLink.setAttribute("hidden", true);
    } else {
      break;
    }
  }

  for (const calendar of document.querySelectorAll(".calendar[data-month]")) {
    const calendarMonth = new Date(calendar.dataset.month).getTime();
    if (thisMonth > calendarMonth) {
      calendar.setAttribute("hidden", true);
    } else {
      break;
    }
  }
};

const init = () => {
  hidePastDates();
  {% if include_leaflet %}abfuhrmap.initMap(){% endif %}
};

document.addEventListener("DOMContentLoaded", init);
