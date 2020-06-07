const makeAttribution = () => {
  return (
    'Geodaten &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a>-Mitwirkende, ' +
    'Abfuhrtermine <a href="https://opendata.stadt-muenster.de/dataset/entsorgungskalender-2020-der-abfallwirtschaftsbetriebe-m%C3%BCnster-awm">Stadt Münster</a>'
  );
};

const map = L.map("map").setView([51.96, 7.62], 12);

L.tileLayer("https://{s}.tile.openstreetmap.de/{z}/{x}/{y}.png", {
  maxZoom: 18,
  attribution: makeAttribution(),
}).addTo(map);

const streetsLayer = L.geoJSON({ features: [], type: 'FeatureCollection' }).addTo(map);

let state = {
  selectedDate: null,
  selectedWaste: null,
  calendar: null,
  geometries: null,
}

const updateState = (newState) => {
  state = { ...state, ...newState };

  const { calendar, selectedDate, selectedWaste, geometries } = state;

  for (const link of document.querySelectorAll("a[role=button]")) {
    const { date, wastetype } = link.dataset;
    if (date === selectedDate || wastetype === selectedWaste) {
      link.classList.add('selected');
    } else {
      link.classList.remove('selected');
    }
  }

  streetsLayer.clearLayers();
  let numNoGeometries = 0;
  calendar[selectedDate]
    .filter(({ waste_type }) => waste_type === selectedWaste)
    .forEach(({ street_name }) => {
      if (geometries[street_name]) {
        streetsLayer.addData(geometries[street_name]);
      } else {
        console.log(`No geometries for ${street_name}`);
        numNoGeometries++;
      }
    });
  console.log(`No geometries for ${numNoGeometries} streets`);
  map.fitBounds(streetsLayer.getBounds())
}

const fetchData = async () => {
  const [geometriesResp, calendarResp] = await Promise.all([fetch('/geometries.json'), fetch('/calendar.json')]);
  return Promise.all([geometriesResp.json(), calendarResp.json()]);
}

const init = async () => {
  const [geometries, calendar] = await fetchData();

  for (const wasteLink of document.querySelectorAll("a[data-wastetype]")) {
    const { wastetype } = wasteLink.dataset;

    if (state.selectedWaste === null) {
      state.selectedWaste = wastetype;
    }

    wasteLink.addEventListener('click', () => updateState({ selectedWaste: wastetype }));
  }

  for (const dateLink of document.querySelectorAll("li:not([hidden=true]) a[role=button]")) {
    const { date } = dateLink.dataset;

    if (state.selectedDate === null) {
      state.selectedDate = date;
    }

    dateLink.addEventListener('click', () => updateState({ selectedDate: date }));
  }

  updateState({ geometries, calendar });
  console.log({ state })
}

init();
