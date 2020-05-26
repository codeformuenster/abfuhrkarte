const makeAttribution = () => {
  return (
    'Geodaten &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>-Mitwirkende, ' +
    'Abfuhrtermine <a href="https://opendata.stadt-muenster.de/dataset/entsorgungskalender-2020-der-abfallwirtschaftsbetriebe-m%C3%BCnster-awm">Stadt Münster</a>'
  );
};

const hidePastDates = () => {
  let today = Date.now();
  today = today - (today % 86400000);
  for (const dateLink of document.querySelectorAll('li[data-date]')) {
    const linkDate = new Date(dateLink.dataset.date).getTime();
    if (today > linkDate) {
      dateLink.setAttribute('hidden', true);
    } else {
      break;
    }
  }
}

const init = () => {
  // var mymap = L.map("map").setView([51.96, 7.62], 11);

  // L.tileLayer("https://geo.stadt-muenster.de/basiskarte/{z}/{x}/{y}.png", {
  //   maxZoom: 18,
  //   attribution: makeAttribution(),
  // }).addTo(mymap);
  hidePastDates();
};

document.addEventListener("DOMContentLoaded", init);